"""
Fire-and-forget Wan2.2 batch: queue shots from a shotlist and exit.
Do not poll ComfyUI while a render is running.

Usage:
  python fire_videos.py --project <project-dir> [--shots S01 S02 ...] [--comfy URL]
                        [--width 832] [--height 480] [--frames 33]
  python fire_videos.py --project <project-dir> --collect

project-dir layout:
  <project>/keyframes/<sid>.png
  <project>/shotlist/shotlist.json
  <project>/videos/<sid>.mp4
"""
import argparse
import json
import os
import shutil
import time
import urllib.request
from pathlib import Path

from PIL import Image


DEFAULTS = {
    "comfy": "http://127.0.0.1:8192",
    "input_dir": r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\input",
    "output_dir": r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output",
    "model_high": "wan2.2_i2v_high_noise_14B_fp16.safetensors",
    "model_low": "wan2.2_i2v_low_noise_14B_fp16.safetensors",
    "vae": "wan_2.1_vae.safetensors",
    "clip": "umt5_xxl_fp16.safetensors",
    "lora_high": "wan2.2_i2v_lightx2v_4steps_lora_v1_high_noise.safetensors",
    "lora_low": "wan2.2_i2v_lightx2v_4steps_lora_v1_low_noise.safetensors",
    "negative": "blurry, distorted, low quality, deformed, watermark, cgi",
    "steps": 4,
    "fps": 16,
}


def newest_output(output_dir, prefix, after_ts=0):
    root = Path(output_dir)
    if not root.exists():
        return None
    candidates = []
    for current, _, files in os.walk(root):
        cur = Path(current)
        for name in files:
            if not name.startswith(prefix) or not name.lower().endswith(".mp4"):
                continue
            p = cur / name
            try:
                mtime = p.stat().st_mtime
            except OSError:
                continue
            if mtime >= after_ts:
                candidates.append((mtime, p))
    if not candidates:
        return None
    candidates.sort(reverse=True)
    return candidates[0][1]


def collect_outputs(project, shot_ids, output_dir, prefix_base, after_ts=0):
    videos = project / "videos"
    videos.mkdir(parents=True, exist_ok=True)
    copied = []
    missing = []
    for sid in shot_ids:
        src = newest_output(output_dir, f"{prefix_base}_{sid}", after_ts)
        if not src:
            missing.append(sid)
            continue
        dest = videos / f"{sid}.mp4"
        shutil.copy2(src, dest)
        copied.append({"shot_id": sid, "src": str(src), "dest": str(dest)})
        print(f"  {sid} copied -> {dest}")
    return copied, missing


def build_wf(d, image_name, prompt, seed, prefix):
    mid = max(1, d["steps"] // 2)
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": d["model_high"], "weight_dtype": "default"}},
        "2": {"class_type": "UNETLoader", "inputs": {"unet_name": d["model_low"], "weight_dtype": "default"}},
        "1L": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": d["lora_high"], "strength_model": 1.0}},
        "2L": {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["2", 0], "lora_name": d["lora_low"], "strength_model": 1.0}},
        "3": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["1L", 0], "shift": 8.0}},
        "4": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["2L", 0], "shift": 8.0}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": d["vae"]}},
        "6": {"class_type": "CLIPLoader", "inputs": {"clip_name": d["clip"], "type": "wan"}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["6", 0], "text": prompt}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["6", 0], "text": d["negative"]}},
        "9": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "10": {"class_type": "WanImageToVideo", "inputs": {
            "positive": ["7", 0], "negative": ["8", 0], "vae": ["5", 0],
            "width": d["width"], "height": d["height"], "length": d["frames"],
            "batch_size": 1, "start_image": ["9", 0]}},
        "11": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["3", 0], "positive": ["10", 0], "negative": ["10", 1], "latent_image": ["10", 2],
            "add_noise": "enable", "noise_seed": seed, "steps": d["steps"], "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple",
            "start_at_step": 0, "end_at_step": mid, "return_with_leftover_noise": "enable"}},
        "12": {"class_type": "KSamplerAdvanced", "inputs": {
            "model": ["4", 0], "positive": ["10", 0], "negative": ["10", 1], "latent_image": ["11", 0],
            "add_noise": "disable", "noise_seed": 0, "steps": d["steps"], "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple",
            "start_at_step": mid, "end_at_step": 1000, "return_with_leftover_noise": "disable"}},
        "13": {"class_type": "VAEDecode", "inputs": {"samples": ["12", 0], "vae": ["5", 0]}},
        "14": {"class_type": "VHS_VideoCombine", "inputs": {
            "images": ["13", 0], "frame_rate": float(d["fps"]), "loop_count": 0,
            "filename_prefix": prefix, "format": "video/h264-mp4",
            "pingpong": False, "save_output": True, "pix_fmt": "yuv420p",
            "crf": 16, "save_metadata": False, "trim_to_audio": False}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Project dir with keyframes/ and shotlist/")
    ap.add_argument("--shots", nargs="*", help="Shot IDs to queue or collect (default: all)")
    ap.add_argument("--comfy", default=DEFAULTS["comfy"])
    ap.add_argument("--input-dir", default=DEFAULTS["input_dir"])
    ap.add_argument("--output-dir", default=DEFAULTS["output_dir"])
    ap.add_argument("--width", type=int, default=832)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--frames", type=int, default=33, help="Frames per clip (33 = 2s @ 16fps)")
    ap.add_argument("--prefix", default="film_video", help="Output filename prefix")
    ap.add_argument("--collect", action="store_true",
                    help="Collect finished mp4s from ComfyUI output into project/videos and exit")
    ap.add_argument("--since", type=float, default=0,
                    help="Only collect output files modified after this Unix timestamp")
    args = ap.parse_args()

    d = dict(DEFAULTS, comfy=args.comfy, input_dir=args.input_dir, output_dir=args.output_dir,
             width=args.width, height=args.height, frames=args.frames)

    project = Path(args.project)
    shotlist = json.loads((project / "shotlist" / "shotlist.json").read_text(encoding="utf-8-sig"))
    want = set(args.shots) if args.shots else None
    selected = [s["shot_id"] for s in shotlist if not want or s["shot_id"] in want]

    if args.collect:
        copied, missing = collect_outputs(project, selected, d["output_dir"], args.prefix, args.since)
        log_dir = project / "meta"
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / "step7_collect_log.json").write_text(
            json.dumps({"copied": copied, "missing": missing}, indent=2), encoding="utf-8")
        print(f"\ncollected {len(copied)} clips; missing {missing}")
        return

    keyframes = project / "keyframes"
    in_dir = Path(d["input_dir"])
    in_dir.mkdir(parents=True, exist_ok=True)

    queued = []
    t0 = time.time()
    for s in shotlist:
        sid = s["shot_id"]
        if want and sid not in want:
            continue
        kf = keyframes / f"{sid}.png"
        if not kf.exists():
            print(f"  {sid}: no keyframe, skip")
            continue

        in_name = f"{project.name}_{sid}.png"
        Image.open(kf).convert("RGB").resize((d["width"], d["height"]), Image.LANCZOS).save(in_dir / in_name, "PNG")

        prompt = (
            f"{s.get('camera_motion', 'locked').replace('_', ' ')} camera, {s.get('shot_type', 'MS')} shot, "
            f"{s.get('action', '')}, {s.get('mood', '')} mood, {s.get('lighting', '')} lighting, "
            f"natural subtle motion, cinematic"
        )
        seed = 1000 + int("".join(c for c in sid if c.isdigit()) or "1") * 1111
        prefix = f"{args.prefix}_{sid}"
        wf = build_wf(d, in_name, prompt, seed, prefix)
        body = json.dumps({"prompt": wf}).encode()
        try:
            res = json.loads(urllib.request.urlopen(
                urllib.request.Request(f"{d['comfy']}/prompt", data=body,
                                       headers={"Content-Type": "application/json"}),
                timeout=60).read())
            print(f"  {sid} queued pid={res.get('prompt_id', '?')[:8]}")
            queued.append(sid)
        except Exception as e:
            print(f"  {sid} QUEUE FAIL: {e}")

    print(f"\nqueued {len(queued)} shots: {queued}")
    print("EXITING. Models stay resident. Check output dir later (~5-10 min/clip).")
    if queued:
        print(f"Collect later with: python {Path(__file__).name} --project \"{project}\" --shots {' '.join(queued)} --collect --since {t0:.0f}")


if __name__ == "__main__":
    main()
