"""Kokoro-82M TTS, 默认 bf16 autocast → AMX-BF16 (Intel CPU). 中/英/多语种."""
import os, gc, wave, argparse, contextlib, numpy as np
os.environ.setdefault("ONEDNN_DEFAULT_FPMATH_MODE", "BF16")

ap = argparse.ArgumentParser()
ap.add_argument("text")
ap.add_argument("-o", "--output", default="output.wav")
ap.add_argument("-v", "--voice", default="zf_xiaobei",
                help="zf_/zm_=zh, af_/am_=en-US, bf_/bm_=en-GB, jf_/jm_=ja, ...")
ap.add_argument("-l", "--lang", default=None,
                help="lang code: z=zh, a=en-US, b=en-GB, j=ja, ... 默认按 voice 前缀推断")
ap.add_argument("--fp32", action="store_true",
                help="关闭 bf16 autocast, 用 fp32 推理")
args = ap.parse_args()

LANG_BY_PREFIX = {"z": "z", "a": "a", "b": "b", "e": "e", "f": "f", "h": "h",
                  "i": "i", "j": "j", "p": "p"}
lang = args.lang or LANG_BY_PREFIX.get(args.voice[0], "a")

import torch
from kokoro import KPipeline

pipe = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
amp = (contextlib.nullcontext() if args.fp32
       else torch.autocast(device_type="cpu", dtype=torch.bfloat16))
parts = []
with torch.inference_mode(), amp:
    for _, _, a in pipe(args.text, voice=args.voice):
        parts.append(a.float().cpu()); gc.collect()
audio = torch.cat(parts).numpy()

pcm = (np.clip(audio, -1, 1) * 32767).astype(np.int16)
with wave.open(args.output, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
    w.writeframes(pcm.tobytes())
print(f"{args.output}  {len(audio)/24000:.2f}s  lang={lang}  "
      f"mode={'fp32' if args.fp32 else 'bf16/AMX'}")
