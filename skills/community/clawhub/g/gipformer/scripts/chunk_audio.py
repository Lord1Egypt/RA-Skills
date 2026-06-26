#!/usr/bin/env python3
"""
Audio chunking utility for long audio files.

Uses Silero VAD (ONNX) to split audio on speech boundaries, then merges
small VAD segments into chunks of up to MAX_CHUNK_SECONDS (20s).
If a single VAD segment exceeds HARD_CUT_SECONDS (30s), it is hard-cut
into non-overlapping 30s pieces as a last resort.

Usage as library:
    from chunk_audio import chunk_audio_file, chunk_audio_samples
    chunks = chunk_audio_file("long_audio.wav")

Usage as CLI:
    python chunk_audio.py input.wav -o chunks/
    python chunk_audio.py input.wav --max-chunk 15
"""

import argparse
import io
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf

MAX_CHUNK_SECONDS = 20.0   # target max when merging VAD segments
HARD_CUT_SECONDS = 30.0    # absolute max — hard-cut if VAD segment exceeds this
MIN_CHUNK_SECONDS = 0.5    # discard chunks shorter than this
TARGET_SAMPLE_RATE = 16000


@dataclass
class AudioChunk:
    """A chunk of audio with metadata."""

    samples: np.ndarray  # float32
    sample_rate: int
    start_time: float  # offset in original audio (seconds)
    end_time: float
    index: int

    @property
    def duration(self) -> float:
        return self.end_time - self.start_time


# ── Audio loading ────────────────────────────────────────────────────────────


def load_audio(path: str, target_sr: int = TARGET_SAMPLE_RATE) -> tuple[np.ndarray, int]:
    """Load audio file, convert to mono float32, resample if needed."""
    samples, sr = sf.read(path, dtype="float32")
    if samples.ndim > 1:
        samples = samples.mean(axis=1)

    if sr != target_sr:
        try:
            import resampy

            samples = resampy.resample(samples, sr, target_sr)
        except ImportError:
            # Linear interpolation fallback
            ratio = target_sr / sr
            new_len = int(len(samples) * ratio)
            indices = np.linspace(0, len(samples) - 1, new_len)
            samples = np.interp(indices, np.arange(len(samples)), samples).astype(np.float32)
        sr = target_sr

    return samples, sr


# ── VAD-based chunking ───────────────────────────────────────────────────────


_silero_cache = None


def _load_silero_vad():
    """Load Silero VAD model via silero-vad + onnxruntime (lightweight, no torch)."""
    global _silero_cache
    if _silero_cache is not None:
        return _silero_cache

    from silero_vad import load_silero_vad, get_speech_timestamps

    model = load_silero_vad(onnx=True)
    _silero_cache = (model, get_speech_timestamps)
    return _silero_cache


def preload_vad():
    """Preload VAD model (call at server startup to avoid cold-start latency)."""
    _load_silero_vad()


def _resample_for_vad(samples: np.ndarray, sr_in: int, sr_out: int) -> np.ndarray:
    """Resample audio to target rate for VAD using linear interpolation."""
    if sr_in == sr_out:
        return samples
    ratio = sr_out / sr_in
    new_len = int(len(samples) * ratio)
    indices = np.linspace(0, len(samples) - 1, new_len)
    return np.interp(indices, np.arange(len(samples)), samples).astype(np.float32)


def _hard_cut(
    samples: np.ndarray,
    sample_rate: int,
    max_s: float = HARD_CUT_SECONDS,
    offset: float = 0.0,
) -> list[AudioChunk]:
    """Non-overlapping hard cut — last resort for oversized segments."""
    total = len(samples)
    chunk_len = int(max_s * sample_rate)
    chunks = []
    pos = 0
    while pos < total:
        end = min(pos + chunk_len, total)
        dur = (end - pos) / sample_rate
        if dur >= MIN_CHUNK_SECONDS:
            chunks.append(
                AudioChunk(
                    samples=samples[pos:end].copy(),
                    sample_rate=sample_rate,
                    start_time=offset + pos / sample_rate,
                    end_time=offset + end / sample_rate,
                    index=len(chunks),
                )
            )
        pos = end
    return chunks


def _append_chunk(
    chunks: list[AudioChunk],
    samples: np.ndarray,
    sr: int,
    start_sample: int,
    end_sample: int,
    min_chunk_s: float,
):
    """Append a chunk if it meets minimum duration."""
    # Add padding around speech boundaries
    pad = int(0.1 * sr)  # 100ms padding
    start_sample = max(0, start_sample - pad)
    end_sample = min(len(samples), end_sample + pad)

    duration = (end_sample - start_sample) / sr
    if duration >= min_chunk_s:
        chunks.append(
            AudioChunk(
                samples=samples[start_sample:end_sample].copy(),
                sample_rate=sr,
                start_time=start_sample / sr,
                end_time=end_sample / sr,
                index=len(chunks),
            )
        )


def chunk_vad(
    samples: np.ndarray,
    sample_rate: int,
    max_chunk_s: float = MAX_CHUNK_SECONDS,
    min_chunk_s: float = MIN_CHUNK_SECONDS,
) -> list[AudioChunk]:
    """Split audio using Silero VAD speech timestamps.

    VAD segments are merged into chunks up to max_chunk_s (20s).
    Segments exceeding HARD_CUT_SECONDS (30s) are hard-cut as last resort.
    """
    model, get_speech_timestamps = _load_silero_vad()

    # Silero VAD expects 16kHz
    if sample_rate != 16000:
        vad_samples = _resample_for_vad(samples, sample_rate, 16000)
        vad_sr = 16000
    else:
        vad_samples = samples
        vad_sr = sample_rate

    # Get speech timestamps — tighten params to produce smaller segments
    speech_timestamps = get_speech_timestamps(
        vad_samples,
        model,
        sampling_rate=vad_sr,
        min_silence_duration_ms=200,
        speech_pad_ms=100,
        min_speech_duration_ms=200,
    )

    if not speech_timestamps:
        # No speech detected — hard-cut if too long, else return as-is
        dur = len(samples) / sample_rate
        if dur <= max_chunk_s:
            return [
                AudioChunk(
                    samples=samples,
                    sample_rate=sample_rate,
                    start_time=0,
                    end_time=dur,
                    index=0,
                )
            ]
        return _hard_cut(samples, sample_rate, HARD_CUT_SECONDS)

    # Scale timestamps back to original sample rate
    scale = sample_rate / vad_sr
    segments = [
        (int(ts["start"] * scale), int(ts["end"] * scale)) for ts in speech_timestamps
    ]

    # Group (merge) segments into chunks respecting max duration
    chunks = []
    chunk_start = segments[0][0]
    chunk_end = segments[0][1]

    for seg_start, seg_end in segments[1:]:
        potential_duration = (seg_end - chunk_start) / sample_rate

        if potential_duration > max_chunk_s:
            # Current group exceeds max — finalize current chunk
            _append_chunk(chunks, samples, sample_rate, chunk_start, chunk_end, min_chunk_s)
            chunk_start = seg_start
            chunk_end = seg_end
        else:
            chunk_end = seg_end

    # Final chunk
    _append_chunk(chunks, samples, sample_rate, chunk_start, chunk_end, min_chunk_s)

    # Hard-cut any chunk that still exceeds HARD_CUT_SECONDS
    final_chunks = []
    for chunk in chunks:
        if chunk.duration > HARD_CUT_SECONDS:
            sub = _hard_cut(chunk.samples, chunk.sample_rate, HARD_CUT_SECONDS, offset=chunk.start_time)
            final_chunks.extend(sub)
        else:
            final_chunks.append(chunk)

    # Re-index
    for i, c in enumerate(final_chunks):
        c.index = i

    return final_chunks


# ── Public API ───────────────────────────────────────────────────────────────


def chunk_audio_file(
    path: str,
    max_chunk_s: float = MAX_CHUNK_SECONDS,
    target_sr: int = TARGET_SAMPLE_RATE,
) -> list[AudioChunk]:
    """Load audio file and split into chunks using VAD.

    Args:
        path: Path to audio file (WAV, FLAC, OGG, etc.)
        max_chunk_s: Target max chunk duration in seconds (default 20)
        target_sr: Target sample rate (default 16000)

    Returns:
        List of AudioChunk objects
    """
    samples, sr = load_audio(path, target_sr)
    return chunk_audio_samples(samples, sr, max_chunk_s)


def chunk_audio_samples(
    samples: np.ndarray,
    sample_rate: int,
    max_chunk_s: float = MAX_CHUNK_SECONDS,
) -> list[AudioChunk]:
    """Split audio samples into chunks using VAD.

    Args:
        samples: float32 mono audio array
        sample_rate: Sample rate of audio
        max_chunk_s: Target max chunk duration in seconds

    Returns:
        List of AudioChunk objects
    """
    total_duration = len(samples) / sample_rate

    # Short audio — no chunking needed
    if total_duration <= max_chunk_s:
        return [
            AudioChunk(
                samples=samples,
                sample_rate=sample_rate,
                start_time=0,
                end_time=total_duration,
                index=0,
            )
        ]

    return chunk_vad(samples, sample_rate, max_chunk_s)


def chunk_to_wav_bytes(chunk: AudioChunk) -> bytes:
    """Convert an AudioChunk to WAV bytes for transmission."""
    buf = io.BytesIO()
    sf.write(buf, chunk.samples, chunk.sample_rate, format="WAV", subtype="PCM_16")
    return buf.getvalue()


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Chunk audio files for ASR processing")
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("-o", "--output-dir", default="chunks", help="Output directory (default: chunks/)")
    parser.add_argument(
        "--max-chunk",
        type=float,
        default=MAX_CHUNK_SECONDS,
        help=f"Max chunk duration in seconds (default: {MAX_CHUNK_SECONDS})",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: file not found: {args.input}")
        sys.exit(1)

    chunks = chunk_audio_file(args.input, max_chunk_s=args.max_chunk)

    os.makedirs(args.output_dir, exist_ok=True)
    stem = Path(args.input).stem

    print(f"Input: {args.input}")
    print(f"Chunks: {len(chunks)}")
    print()

    for chunk in chunks:
        out_path = os.path.join(args.output_dir, f"{stem}_chunk{chunk.index:03d}.wav")
        sf.write(out_path, chunk.samples, chunk.sample_rate)
        print(
            f"  [{chunk.index:3d}] {chunk.start_time:7.2f}s - {chunk.end_time:7.2f}s "
            f"({chunk.duration:.2f}s) -> {out_path}"
        )


if __name__ == "__main__":
    main()
