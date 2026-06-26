"""
Fire-and-forget Wan2.2 warmup: queue one small job to make the server load
the fp16 dual model. After this returns, the server keeps models resident and
subsequent jobs run at warm speed.

Usage:
  python fire_warmup.py [--comfy http://IP:PORT] [--input-dir <wsl-input-path>]
"""
import argparse
import json
import urllib.request
from pathlib import Path

from PIL import Image


DEFAULTS = {
    "comfy": "http://127.0.0.1:8192",
    "input_dir": r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\input",
    "model_high": "wan2.2_i2v_high_noise_14B_fp16.safetensors",
    "model_low": "wan2.2_i2v_low_noise_14B_fp16.safetensors",
    "vae": "wan_2.1_vae.safetensors",
    "clip": "umt5_xxl_fp16.safetensors",
    "lora_high": "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors",
    "lora_low": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",
}


def build_workflow(d):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": d["model_high"], "weight_dtype": "default"}},
        "2": {"class_type": "UNETLoader", "inputs": {"unet_name": d["model_low"], "weight_dtype": "default"}},
        "1L": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": d["lora_high"], "strength_model": 1.0}},
        "2L": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["2", 0], "lora_name": d["lora_low"], "strength_model": 1.0}},
        "3": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1L", 0], "shift": 8.0}},
        "4": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["2L", 0], "shift": 8.0}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": d["vae"]}},
        "6": {"class_type": "CLIPLoader", "inputs": {"clip_name": d["clip"], "type": "wan"}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["6", 0], "text": "warmup"}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["6", 0], "text": ""}},
        "9": {"class_type": "LoadImage", "inputs": {"image": "fire_warmup.png"}},
        "10": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["7", 0], "negative": ["8", 0], "vae": ["5", 0],
            "width": 256, "height": 256, "length": 17,
            "batch_size": 1, "start_image": ["9", 0]}},
        "11": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["3", 0], "positive": ["10", 0], "negative": ["10", 1], "latent_image": ["10", 2],
            "add_noise": "enable", "noise_seed": 42, "steps": 4, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple",
            "start_at_step": 0, "end_at_step": 2, "return_with_leftover_noise": "enable"}},
        "12": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["4", 0], "positive": ["10", 0], "negative": ["10", 1], "latent_image": ["11", 0],
            "add_noise": "disable", "noise_seed": 0, "steps": 4, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple",
            "start_at_step": 2, "end_at_step": 1000, "return_with_leftover_noise": "disable"}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["5", 0]}},
        "14": {"class_type": "VHS_VideoCombine", "inputs": {
            "images": ["13", 0], "frame_rate": 16.0, "loop_count": 0,
            "filename_prefix": "fire_warmup_out", "format": "video/h264-mp4",
            "pingpong": False, "save_output": True, "pix_fmt": "yuv420p",
            "crf": 18, "save_metadata": False, "trim_to_audio": False}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comfy", default=DEFAULTS["comfy"])
    ap.add_argument("--input-dir", default=DEFAULTS["input_dir"])
    args = ap.parse_args()

    d = dict(DEFAULTS, comfy=args.comfy, input_dir=args.input_dir)
    in_dir = Path(d["input_dir"])
    in_dir.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (256, 256), (128, 64, 32)).save(in_dir / "fire_warmup.png", "PNG")

    body = json.dumps({"prompt": build_workflow(d)}).encode()
    req = urllib.request.Request(f"{d['comfy']}/prompt", data=body,
                                 headers={"Content-Type": "application/json"})
    res = json.loads(urllib.request.urlopen(req, timeout=60).read())
    print(f"queued pid={res.get('prompt_id', '?')}")
    print("EXITING. Do not poll. First fp16 load is usually 9-10 minutes.")


if __name__ == "__main__":
    main()
