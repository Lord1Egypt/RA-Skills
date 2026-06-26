#!/usr/bin/env python3
"""
Gipformer ASR Serving - Model server with VAD chunking and batching.

Serves the gipformer-65M-rnnt model via HTTP API with:
- Accepts audio of any length (server-side VAD chunking)
- Dynamic request batching for throughput optimization
- Supports WAV, FLAC, OGG, MP3, M4A formats
- Returns full transcript with per-chunk details

Usage:
    python serve.py
    python serve.py --port 8910 --quantize int8 --max-batch-size 16
    python serve.py --host 0.0.0.0 --num-threads 8
"""

import argparse
import asyncio
import base64
import io
import os
import subprocess
import sys
import tempfile
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import List

import numpy as np
import soundfile as sf

try:
    import sherpa_onnx
except ImportError:
    print("Error: sherpa-onnx not installed. Run: pip install sherpa-onnx")
    sys.exit(1)

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Error: huggingface_hub not installed. Run: pip install huggingface_hub")
    sys.exit(1)

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    print("Error: FastAPI not installed. Run: pip install fastapi uvicorn")
    sys.exit(1)

# Import chunking from sibling module
sys.path.insert(0, os.path.dirname(__file__))
from chunk_audio import chunk_audio_samples, preload_vad

# ── Constants ────────────────────────────────────────────────────────────────

REPO_ID = "g-group-ai-lab/gipformer-65M-rnnt"
SAMPLE_RATE = 16000
FEATURE_DIM = 80
MAX_BATCH_CHUNKS = 64  # max chunks submitted to engine concurrently

ONNX_FILES = {
    "fp32": {
        "encoder": "encoder-epoch-35-avg-6.onnx",
        "decoder": "decoder-epoch-35-avg-6.onnx",
        "joiner": "joiner-epoch-35-avg-6.onnx",
    },
    "int8": {
        "encoder": "encoder-epoch-35-avg-6.int8.onnx",
        "decoder": "decoder-epoch-35-avg-6.int8.onnx",
        "joiner": "joiner-epoch-35-avg-6.int8.onnx",
    },
}


# ── Request/Response models ──────────────────────────────────────────────────


class TranscribeRequest(BaseModel):
    audio_b64: str  # base64-encoded audio (WAV/FLAC/OGG/MP3/M4A)
    sample_rate: int = SAMPLE_RATE  # hint for raw PCM only


class ChunkResult(BaseModel):
    text: str
    start_s: float
    end_s: float


class TranscribeResponse(BaseModel):
    transcript: str  # full merged text
    duration_s: float  # total audio duration
    process_time_s: float
    chunks: List[ChunkResult]  # per-chunk details


class HealthResponse(BaseModel):
    status: str
    model: str
    quantize: str
    uptime_s: float


# ── Batching engine ──────────────────────────────────────────────────────────


@dataclass
class PendingRequest:
    samples: np.ndarray
    sample_rate: int
    future: asyncio.Future = field(default=None)


class BatchingEngine:
    """Collects incoming requests and processes them in batches."""

    def __init__(
        self,
        recognizer: sherpa_onnx.OfflineRecognizer,
        max_batch_size: int = 8,
        max_wait_ms: float = 100,
    ):
        self.recognizer = recognizer
        self.max_batch_size = max_batch_size
        self.max_wait_ms = max_wait_ms
        self._queue: list[PendingRequest] = []
        self._lock = asyncio.Lock()
        self._timer_task = None

    async def submit(self, samples: np.ndarray, sample_rate: int) -> str:
        loop = asyncio.get_running_loop()
        req = PendingRequest(samples=samples, sample_rate=sample_rate, future=loop.create_future())

        batch_to_process = None
        async with self._lock:
            self._queue.append(req)
            if len(self._queue) >= self.max_batch_size:
                batch_to_process = self._queue[:]
                self._queue.clear()
                if self._timer_task and not self._timer_task.done():
                    self._timer_task.cancel()
                    self._timer_task = None
            elif len(self._queue) == 1:
                self._timer_task = asyncio.create_task(self._wait_and_flush())

        if batch_to_process is not None:
            asyncio.create_task(self._process_batch(batch_to_process))

        return await req.future

    async def _wait_and_flush(self):
        await asyncio.sleep(self.max_wait_ms / 1000.0)
        batch = None
        async with self._lock:
            if self._queue:
                batch = self._queue[:]
                self._queue.clear()
                self._timer_task = None
        if batch:
            await self._process_batch(batch)

    async def _process_batch(self, batch: list[PendingRequest]):
        loop = asyncio.get_running_loop()
        try:
            results = await loop.run_in_executor(None, self._infer_batch, batch)
            for req, text in zip(batch, results):
                if not req.future.done():
                    req.future.set_result(text)
        except Exception as e:
            for req in batch:
                if not req.future.done():
                    req.future.set_exception(e)

    def _infer_batch(self, batch: list[PendingRequest]) -> list[str]:
        streams = []
        for req in batch:
            stream = self.recognizer.create_stream()
            stream.accept_waveform(req.sample_rate, req.samples)
            streams.append(stream)
        self.recognizer.decode_streams(streams)
        return [s.result.text.strip() for s in streams]


# ── Audio decoding ───────────────────────────────────────────────────────────


def _resample_linear(samples: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    if sr_in == sr_out:
        return samples
    ratio = sr_out / sr_in
    new_len = int(len(samples) * ratio)
    indices = np.linspace(0, len(samples) - 1, new_len)
    return np.interp(indices, np.arange(len(samples)), samples).astype(np.float32)


def _decode_with_ffmpeg(raw: bytes) -> tuple[np.ndarray, int]:
    """Decode audio bytes using ffmpeg (handles M4A, MP3, and other formats)."""
    with tempfile.NamedTemporaryFile(suffix=".audio", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y", "-i", tmp_path,
                "-f", "wav", "-ar", str(SAMPLE_RATE), "-ac", "1",
                "-acodec", "pcm_s16le", "pipe:1",
            ],
            capture_output=True,
            timeout=120,
        )
        if result.returncode != 0:
            raise ValueError(f"ffmpeg failed: {result.stderr.decode(errors='replace')[:200]}")
        buf = io.BytesIO(result.stdout)
        samples, sr = sf.read(buf, dtype="float32")
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        return samples, sr
    finally:
        os.unlink(tmp_path)


def decode_audio_b64(audio_b64: str) -> tuple[np.ndarray, int]:
    """Decode base64-encoded audio to float32 mono 16kHz numpy array.

    Supports WAV, FLAC, OGG, MP3 (via soundfile) and M4A (via ffmpeg).
    """
    raw = base64.b64decode(audio_b64)
    if len(raw) == 0:
        raise ValueError("Empty audio data")

    # Try soundfile first (handles WAV, FLAC, OGG, MP3)
    try:
        buf = io.BytesIO(raw)
        samples, sr = sf.read(buf, dtype="float32")
        if samples.ndim > 1:
            samples = samples.mean(axis=1)
        if len(samples) == 0:
            raise ValueError("Audio file contains no samples")
        samples = _resample_linear(samples, sr, SAMPLE_RATE)
        return samples, SAMPLE_RATE
    except ValueError:
        raise
    except Exception:
        pass

    # Fallback: ffmpeg for M4A and other formats
    try:
        samples, sr = _decode_with_ffmpeg(raw)
        samples = _resample_linear(samples, sr, SAMPLE_RATE)
        return samples, SAMPLE_RATE
    except Exception as e:
        raise ValueError(f"Cannot decode audio (tried soundfile + ffmpeg): {e}")


# ── App factory ──────────────────────────────────────────────────────────────

_state = {}


def create_app(args: argparse.Namespace) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Download ASR model
        print(f"Downloading {args.quantize} model from {REPO_ID}...")
        files = ONNX_FILES[args.quantize]
        paths = {}
        for key, filename in files.items():
            paths[key] = hf_hub_download(repo_id=REPO_ID, filename=filename)
        paths["tokens"] = hf_hub_download(repo_id=REPO_ID, filename="tokens.txt")
        print("Model downloaded.")

        # Load ASR recognizer
        recognizer = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=paths["encoder"],
            decoder=paths["decoder"],
            joiner=paths["joiner"],
            tokens=paths["tokens"],
            num_threads=args.num_threads,
            sample_rate=SAMPLE_RATE,
            feature_dim=FEATURE_DIM,
            decoding_method=args.decoding_method,
        )
        print(f"ASR model loaded. Decoding: {args.decoding_method}, threads: {args.num_threads}")

        # Preload VAD model
        preload_vad()
        print("VAD model loaded.")

        engine = BatchingEngine(
            recognizer=recognizer,
            max_batch_size=args.max_batch_size,
            max_wait_ms=args.max_wait_ms,
        )

        _state["recognizer"] = recognizer
        _state["engine"] = engine
        _state["start_time"] = time.time()
        _state["quantize"] = args.quantize

        print(f"Server ready on {args.host}:{args.port}")
        yield

        _state.clear()

    app = FastAPI(
        title="Gipformer ASR Server",
        description="Vietnamese speech recognition — send audio of any length, get transcript",
        version="2.0.0",
        lifespan=lifespan,
    )

    @app.get("/health", response_model=HealthResponse)
    async def health():
        return HealthResponse(
            status="ok",
            model=REPO_ID,
            quantize=_state["quantize"],
            uptime_s=round(time.time() - _state["start_time"], 2),
        )

    @app.post("/transcribe", response_model=TranscribeResponse)
    async def transcribe(req: TranscribeRequest):
        """Transcribe audio of any length.

        The server automatically chunks long audio using VAD,
        infers each chunk via the batching engine, and merges
        the results into a single transcript.
        """
        engine: BatchingEngine = _state["engine"]
        t0 = time.time()

        try:
            samples, sr = decode_audio_b64(req.audio_b64)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid audio: {e}")

        duration = len(samples) / sr

        # Chunk with VAD (short audio returns a single chunk)
        chunks = chunk_audio_samples(samples, sr)

        # Infer chunks in batches of MAX_BATCH_CHUNKS
        all_texts = []
        for i in range(0, len(chunks), MAX_BATCH_CHUNKS):
            batch = chunks[i : i + MAX_BATCH_CHUNKS]
            tasks = [engine.submit(c.samples, c.sample_rate) for c in batch]
            texts = await asyncio.gather(*tasks)
            all_texts.extend(texts)

        # Build response
        transcript = " ".join(t for t in all_texts if t)
        chunk_results = []
        for chunk, text in zip(chunks, all_texts):
            chunk_results.append(
                ChunkResult(
                    text=text,
                    start_s=round(chunk.start_time, 3),
                    end_s=round(chunk.end_time, 3),
                )
            )

        return TranscribeResponse(
            transcript=transcript,
            duration_s=round(duration, 3),
            process_time_s=round(time.time() - t0, 3),
            chunks=chunk_results,
        )

    return app


# ── CLI ──────────────────────────────────────────────────────────────────────


def parse_args():
    parser = argparse.ArgumentParser(
        description="Gipformer ASR Server with batching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8910, help="Bind port (default: 8910)")
    parser.add_argument(
        "--quantize",
        choices=["fp32", "int8"],
        default="int8",
        help="Model precision (default: int8)",
    )
    parser.add_argument("--num-threads", type=int, default=4, help="Inference threads (default: 4)")
    parser.add_argument(
        "--decoding-method",
        choices=["greedy_search", "modified_beam_search"],
        default="modified_beam_search",
        help="Decoding method (default: modified_beam_search)",
    )
    parser.add_argument("--max-batch-size", type=int, default=16, help="Max batch size (default: 16)")
    parser.add_argument(
        "--max-wait-ms", type=float, default=100, help="Max wait before flushing batch (default: 100ms)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    app = create_app(args)
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")
