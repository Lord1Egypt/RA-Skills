"""
Generate Qwen-Image keyframes with a direct ComfyUI workflow.

This is the primary still-image path for the local video pipeline. It avoids the
local Qwen GUI builder so shot prompts keep their director language, camera
angles, and prompt-level character lock tokens intact.
"""
import argparse
import json
import os
import shutil
import time
import urllib.request
from pathlib import Path


DEFAULT_OUTPUT = r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output"

DEFAULT_NEGATIVE = (
    "two people, duplicate person, twins, friend, group photo, extra person, "
    "collage, storyboard, comic panel, manga panel, split screen, multiple panels, "
    "triptych, diptych, film strip, contact sheet, sequence frames, before and after, "
    "three images, four images, repeated same person, text, logo, watermark, "
    "minor sexualization, childlike body, distorted face, bad hands, blurry, "
    "overexposed, plastic skin"
)

SINGLE_FRAME_LOCK = (
    "One single full-frame photograph, one camera exposure, one continuous scene, "
    "one protagonist appears once, no panels, no collage, no split screen."
)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def post_prompt(comfy, workflow, client_id):
    body = json.dumps({"prompt": workflow, "client_id": client_id}).encode("utf-8")
    req = urllib.request.Request(
        f"{comfy}/prompt",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.loads(res.read().decode("utf-8"))


def newest_png(output_dir, prefix, after_ts):
    candidates = []
    for current, _, files in os.walk(output_dir):
        current_path = Path(current)
        for name in files:
            if not name.startswith(prefix) or not name.lower().endswith(".png"):
                continue
            p = current_path / name
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


def first_lock_tokens(bible, prompts):
    for char in bible.get("characters") or []:
        tokens = (char.get("lock_tokens") or "").strip()
        if tokens:
            return tokens
    return (prompts.get("character_identity") or "").strip()


def detail_lock_tokens(prompts):
    return (
        prompts.get("character_body_identity")
        or "same adult Korean female protagonist, celebrity-level Instagram-model styling, fitted fashion silhouette, glamorous adult model proportions, consistent outfit silhouette and accessories"
    ).strip()


def identity_prefix(shot, prompts, lock_tokens):
    if not bool(shot.get("needs_character", True)):
        return ""
    framing = (shot.get("identity_framing") or "").strip().lower()
    if framing == "environment_only":
        return ""
    if framing in {"body_detail", "hands_only", "feet_only", "no_face"}:
        return detail_lock_tokens(prompts)
    if framing == "back_view":
        return (
            detail_lock_tokens(prompts)
            + ", back view or side-back view, face not emphasized, same outfit silhouette"
        )
    return lock_tokens


def shot_prompt(shot, prompts, global_style, lock_tokens):
    sid = shot["shot_id"]
    custom = (prompts.get(sid) or "").strip()
    needs_character = bool(shot.get("needs_character", True))
    parts = []
    prefix = identity_prefix(shot, prompts, lock_tokens)
    if needs_character and prefix:
        parts.append(prefix)
    if global_style:
        parts.append(global_style)
    expression = (shot.get("emotional_expression") or "").strip()
    if needs_character and expression:
        parts.append(
            f"Facial expression and body language: {expression}. "
            "Keep the expression subtle, realistic, age-appropriate, and non-theatrical"
        )
    framing = (shot.get("identity_framing") or "").strip().lower()
    if framing in {"body_detail", "hands_only", "feet_only", "no_face"}:
        parts.append("Frame only the requested body detail. Face is not visible. Do not turn this into a portrait or full-body character shot")
    elif framing == "back_view":
        parts.append("Prefer back view or side-back view. Do not turn toward camera unless the shot action says so")
    if custom:
        parts.append(custom)
    else:
        parts.extend([
            f"{shot.get('shot_type', 'MS')} shot",
            f"{shot.get('angle', 'eye-level')} angle",
            f"{shot.get('lens_mm', 35)}mm lens",
            f"camera motion feel: {shot.get('camera_motion', 'static')}",
            f"location: {shot.get('location', '')}",
            f"action: {shot.get('action', '')}",
            f"mood: {shot.get('mood', '')}",
            f"lighting: {shot.get('lighting', '')}",
            f"composition: {shot.get('composition', '')}",
            f"actor direction: {shot.get('actor_direction', '')}",
            f"director intent: {shot.get('director_intent', '')}",
            f"continuity: {shot.get('continuity', '')}",
        ])
    parts.append(SINGLE_FRAME_LOCK)
    return ". ".join(p.strip().rstrip(".") for p in parts if str(p).strip()) + "."


def build_workflow(prompt, negative, seed, prefix, width, height, steps, cfg, shift):
    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {"unet_name": "qwen_image_2512_bf16.safetensors", "weight_dtype": "default"},
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image",
                "device": "default",
            },
        },
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_vae.safetensors"}},
        "4": {"class_type": "ModelSamplingAuraFlow", "inputs": {"model": ["1", 0], "shift": shift}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": negative}},
        "7": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1},
        },
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["4", 0],
                "positive": ["5", 0],
                "negative": ["6", 0],
                "latent_image": ["7", 0],
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0,
            },
        },
        "9": {"class_type": "VAEDecode", "inputs": {"samples": ["8", 0], "vae": ["3", 0]}},
        "10": {"class_type": "SaveImage", "inputs": {"images": ["9", 0], "filename_prefix": prefix}},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--shots", nargs="*", help="Shot IDs to generate. Default: all.")
    ap.add_argument("--comfy", default="http://127.0.0.1:8194")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--out-subdir", default="keyframes")
    ap.add_argument("--width", type=int, default=480)
    ap.add_argument("--height", type=int, default=832)
    ap.add_argument("--seed-base", type=int, default=26070000)
    ap.add_argument("--steps", type=int, default=24)
    ap.add_argument("--cfg", type=float, default=4.0)
    ap.add_argument("--shift", type=float, default=3.1)
    ap.add_argument("--timeout", type=int, default=1800)
    args = ap.parse_args()

    project = Path(args.project)
    bible_path = project / "bible.json"
    bible = read_json(bible_path) if bible_path.exists() else {}
    shotlist = read_json(project / "shotlist" / "shotlist.json")
    prompts_path = project / "prompts" / "prompts.json"
    prompts = read_json(prompts_path) if prompts_path.exists() else {}

    global_style = prompts.get("global_style") or bible.get("world_style") or "cinematic realistic film still"
    negative = prompts.get("negative") or bible.get("negative") or DEFAULT_NEGATIVE
    lock_tokens = first_lock_tokens(bible, prompts)
    wanted = set(args.shots or [])
    selected = [s for s in shotlist if not wanted or s["shot_id"] in wanted]

    out_dir = project / args.out_subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    (project / "meta").mkdir(parents=True, exist_ok=True)
    log = []

    for index, shot in enumerate(selected, start=1):
        sid = shot["shot_id"]
        seed = args.seed_base + index * 101
        prefix = f"local_video_direct_{sid}_{seed}"
        prompt = shot_prompt(shot, prompts, global_style, lock_tokens)
        t0 = time.time()
        workflow = build_workflow(prompt, negative, seed, prefix, args.width, args.height, args.steps, args.cfg, args.shift)
        post_prompt(args.comfy, workflow, "local-video-ad-pipeline-direct")
        print(f"{sid}: queued direct Qwen keyframe seed={seed}")

        found = None
        deadline = time.time() + args.timeout
        while time.time() < deadline:
            time.sleep(2)
            found = newest_png(args.output_dir, prefix, t0)
            if found:
                break
        if not found:
            raise TimeoutError(f"{sid}: keyframe output not found for prefix {prefix}")

        dest = out_dir / f"{sid}.png"
        shutil.copy2(found, dest)
        print(f"{sid}: copied {dest}")
        log.append({"shot_id": sid, "seed": seed, "src": str(found), "dest": str(dest), "prompt": prompt})

    (project / "meta" / "direct_keyframes_log.json").write_text(
        json.dumps({"items": log}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
