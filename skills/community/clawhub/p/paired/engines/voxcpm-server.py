"""paired voice-cloning service: VoxCPM2 HTTP server.

Lazy-loads VoxCPM2 model on first request. Listens on port 8056.
Compatible with paired-voice-synth client.
Model: openbmb/VoxCPM2 (Apache-2.0).
"""
import base64
import os
import threading
import time
from pathlib import Path

os.environ["TORCH_COMPILE_DISABLE"] = "1"
os.environ["TORCHDYNAMO_DISABLE"] = "1"

import torch
try:
    torch._dynamo.config.suppress_errors = True
    torch._dynamo.config.disable = True
except Exception:
    pass

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from voxcpm import VoxCPM

app = FastAPI()
MODEL = None
MODEL_LOAD_TIME = 0.0
MODEL_LOADING = False
MODEL_LOAD_LOCK = threading.Lock()


def load_model_sync():
    global MODEL, MODEL_LOAD_TIME, MODEL_LOADING
    with MODEL_LOAD_LOCK:
        if MODEL is not None:
            return
        MODEL_LOADING = True
        print("[voxcpm-server] Loading VoxCPM2 from HF...", flush=True)
        t0 = time.time()
        try:
            MODEL = VoxCPM.from_pretrained("openbmb/VoxCPM2")
        finally:
            MODEL_LOADING = False
        MODEL_LOAD_TIME = time.time() - t0
        print(f"[voxcpm-server] Model loaded in {MODEL_LOAD_TIME:.1f}s", flush=True)


@app.on_event("startup")
async def startup():
    t = threading.Thread(target=load_model_sync, daemon=True)
    t.start()


@app.get("/health")
def health():
    gpu = torch.cuda.is_available()
    vram_free = None
    if gpu:
        try:
            free, total = torch.cuda.mem_get_info(0)
            vram_free = free / (1024 ** 3)
        except Exception:
            pass
    return {
        "ok": True, "gpu": gpu, "vram_free_gb": vram_free,
        "model_loaded": MODEL is not None, "model_loading": MODEL_LOADING,
        "model_load_time_sec": round(MODEL_LOAD_TIME, 1), "engine": "voxcpm2",
    }


class SynthRequest(BaseModel):
    text: str
    reference: str
    ref_text: str | None = None
    output: str = "/tmp/voxcpm-out.wav"


@app.post("/synth")
def synth(req: SynthRequest):
    if MODEL is None:
        if MODEL_LOADING:
            raise HTTPException(503, "Model still loading, retry in 60s")
        load_model_sync()
    if not Path(req.reference).is_file():
        raise HTTPException(400, f"Reference not found: {req.reference}")

    t0 = time.time()
    try:
        kwargs = {"text": req.text, "reference_wav_path": req.reference}
        if req.ref_text and req.ref_text.strip():
            kwargs["prompt_wav_path"] = req.reference
            kwargs["prompt_text"] = req.ref_text
            kwargs.pop("reference_wav_path", None)

        result = MODEL.generate(**kwargs)

        import numpy as np
        import soundfile as sf
        if isinstance(result, tuple):
            audio, sr = result
        elif isinstance(result, np.ndarray):
            audio, sr = result, 48000
        else:
            raise RuntimeError(f"Unexpected generate() return type: {type(result)}")

        Path(req.output).parent.mkdir(parents=True, exist_ok=True)
        sf.write(req.output, audio, sr)
        elapsed = time.time() - t0

        with open(req.output, "rb") as f:
            audio_b64 = base64.b64encode(f.read()).decode()

        return {
            "ok": True, "elapsed_sec": round(elapsed, 2),
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "sample_rate": sr, "audio_base64": audio_b64,
            "output_path": req.output,
            "mode": "continuation" if req.ref_text else "reference_clone",
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"ok": False, "error": str(e), "elapsed_sec": round(time.time() - t0, 2)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8056, timeout_keep_alive=600)
