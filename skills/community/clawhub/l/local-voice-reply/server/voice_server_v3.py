from __future__ import annotations

from pathlib import Path
from typing import Dict
import logging
import os
import time
import uuid

import torch
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from voice_engine import (
    DEFAULT_CFG,
    DEFAULT_EXAGGERATION,
    DEFAULT_SPEED,
    DEFAULT_VOICE_NAME,
    PIPELINE_SINGLE,
    PIPELINE_STREAM,
    VoiceEngine,
)


def _configure_logging() -> None:
    level_name = os.getenv("TARVIS_VOICE_LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


_configure_logging()
log = logging.getLogger("tarvis.voice.api")


def pick_device() -> str:
    forced = (os.getenv("TARVIS_VOICE_DEVICE") or "").strip().lower()
    if forced in {"cuda", "gpu"}:
        if torch.cuda.is_available():
            return "cuda"
        log.warning("TARVIS_VOICE_DEVICE=%s requested but CUDA is unavailable; falling back", forced)
    elif forced == "mps":
        if torch.backends.mps.is_available():
            return "mps"
        log.warning("TARVIS_VOICE_DEVICE=mps requested but MPS is unavailable; falling back")
    elif forced == "cpu":
        return "cpu"

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


DEVICE = pick_device()
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Tarvis Voice Server v3", version="3.4")
engine = VoiceEngine(device=DEVICE, base_dir=BASE_DIR)


def _opus_response(path: Path, headers: Dict[str, str]) -> FileResponse:
    return FileResponse(
        str(path),
        media_type="audio/ogg",
        filename=path.name,
        headers=headers,
    )


@app.middleware("http")
async def trace_requests(request: Request, call_next):
    trace_id = request.headers.get("X-Request-Id") or uuid.uuid4().hex[:12]
    request.state.trace_id = trace_id
    started = time.perf_counter()
    log.debug("request_start trace_id=%s method=%s path=%s", trace_id, request.method, request.url.path)
    try:
        response = await call_next(request)
    except Exception:
        log.exception("request_failed trace_id=%s method=%s path=%s", trace_id, request.method, request.url.path)
        raise
    elapsed_ms = (time.perf_counter() - started) * 1000.0
    response.headers["X-Request-Id"] = trace_id
    response.headers["X-Process-Ms"] = f"{elapsed_ms:.2f}"
    log.debug(
        "request_done trace_id=%s method=%s path=%s status=%s elapsed_ms=%.2f",
        trace_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.on_event("startup")
def startup_checks():
    log.info("startup device=%s base_dir=%s", DEVICE, BASE_DIR)
    if not engine.ffmpeg_ok:
        raise RuntimeError("ffmpeg is required for Opus-only mode but was not found in PATH")
    if not engine.bootstrap_default_voice(DEFAULT_VOICE_NAME):
        raise RuntimeError("Default voice 'juno' not found. Place sample at local-voice-reply/voice/juno_ref.wav")
    log.info("startup_ready voices=%s", list(engine.voice_registry.keys()))


@app.get("/health")
def health():
    return {
        "ok": True,
        "device": DEVICE,
        "ffmpeg_ok": engine.ffmpeg_ok,
        "outputs_dir": str(engine.outputs_dir),
        "registered_voices": list(engine.voice_registry.keys()),
        "embedding_cache_keys": engine.cache.keys(),
        "phrase_ram_cache_keys": engine.phrase_ram_cache.keys(),
        "encode_method": engine.encode_method_name,
        "generate_with_embedding_method": engine.generate_embedding_method_name,
        "benchmark": engine.benchmark_summary(),
    }


@app.get("/benchmark")
def benchmark():
    return {"ok": True, "summary": engine.benchmark_summary()}


@app.post("/voice/register")
async def register_voice(request: Request, voice_name: str = Form(...), audio: UploadFile = File(...)):
    data = await audio.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty audio upload")
    trace_id = getattr(request.state, "trace_id", "")
    log.debug(
        "voice_register_request trace_id=%s voice_name=%s filename=%s bytes=%s",
        trace_id,
        voice_name,
        audio.filename,
        len(data),
    )
    return JSONResponse(engine.register_voice(voice_name, audio, data))


@app.post("/voice/warm")
def warm_voice(request: Request, voice_name: str = Form(...)):
    trace_id = getattr(request.state, "trace_id", "")
    normalized = engine._normalize_voice_name(voice_name)
    if normalized not in engine.voice_registry:
        raise HTTPException(status_code=404, detail=f"Voice '{normalized}' not registered")
    log.debug("voice_warm_request trace_id=%s voice_name=%s", trace_id, normalized)
    emb = engine._load_or_build_embedding(normalized)
    return {"ok": True, "voice_name": normalized, "embedding_ready": emb is not None}


@app.post("/speak")
def speak(
    request: Request,
    text: str = Form(...),
    voice_name: str = Form(DEFAULT_VOICE_NAME),
    speed: float = Form(DEFAULT_SPEED),
    exaggeration: float = Form(DEFAULT_EXAGGERATION),
    cfg: float = Form(DEFAULT_CFG),
):
    trace_id = getattr(request.state, "trace_id", "")
    log.debug(
        "speak_request trace_id=%s voice_name=%s text_len=%s speed=%.3f exaggeration=%.3f cfg=%.3f",
        trace_id,
        voice_name,
        len(text or ""),
        speed,
        exaggeration,
        cfg,
    )
    result = engine.synthesize(
        voice_name=voice_name,
        text=text,
        exaggeration=exaggeration,
        cfg=cfg,
        speed=speed,
        trace_id=trace_id or None,
    )
    out_file = Path(result["path"])
    meta = result["meta"]

    return _opus_response(
        out_file,
        headers={
            "X-Pipeline": PIPELINE_SINGLE,
            "X-Voice": voice_name,
            "X-Trace-Id": str(meta.get("trace_id", trace_id)),
            "X-Cache-Hits": str(meta.get("cache_hits", 0)),
            "X-Total-Ms": str(meta["latency_ms"].get("total_ms", 0)),
            "X-Speed": f"{float(meta.get('speed', DEFAULT_SPEED)):.2f}",
            "X-Output-Format": out_file.suffix.lstrip("."),
        },
    )


@app.post("/speak_stream")
def speak_stream(
    request: Request,
    text: str = Form(...),
    voice_name: str = Form(DEFAULT_VOICE_NAME),
    speed: float = Form(DEFAULT_SPEED),
    exaggeration: float = Form(DEFAULT_EXAGGERATION),
    cfg: float = Form(DEFAULT_CFG),
):
    trace_id = getattr(request.state, "trace_id", "")
    log.debug(
        "speak_stream_request trace_id=%s voice_name=%s text_len=%s speed=%.3f exaggeration=%.3f cfg=%.3f",
        trace_id,
        voice_name,
        len(text or ""),
        speed,
        exaggeration,
        cfg,
    )
    result = engine.synthesize_stream(
        voice_name=voice_name,
        text=text,
        exaggeration=exaggeration,
        cfg=cfg,
        speed=speed,
        trace_id=trace_id or None,
    )
    out_file = Path(result["path"])
    meta = result["meta"]

    return _opus_response(
        out_file,
        headers={
            "X-Pipeline": PIPELINE_STREAM,
            "X-Voice": voice_name,
            "X-Trace-Id": str(meta.get("trace_id", trace_id)),
            "X-Chunk-Count": str(meta.get("chunk_count", 0)),
            "X-Cache-Hits": str(meta.get("cache_hits", 0)),
            "X-Total-Ms": str(meta["latency_ms"].get("total_ms", 0)),
            "X-Speed": f"{float(meta.get('speed', DEFAULT_SPEED)):.2f}",
            "X-Output-Format": out_file.suffix.lstrip("."),
        },
    )


@app.post("/output/cleanup")
def cleanup_output(request: Request, path: str = Form(...)):
    trace_id = getattr(request.state, "trace_id", "")
    log.debug("cleanup_request trace_id=%s path=%s", trace_id, path)
    return JSONResponse(engine.cleanup_output(path))
