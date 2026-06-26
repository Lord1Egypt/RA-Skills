"""
Generate video keyframes with Qwen-Image T2I, prioritizing scene/camera control.

Use this when each shot needs a different location, angle, or composition.
It does not rely on one image-edit anchor as the main generation source; identity
is carried by a short recurring character phrase and optional character LoRA.
"""
import argparse
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path


DEFAULT_QWEN_GUI = r"C:\Users\k0103\Downloads\qwen-gui"
DEFAULT_OUTPUT = r"\\wsl.localhost\Ubuntu\home\choi_g16\comfy\ComfyUI\output"


NEGATIVE = (
    "two people, duplicate person, twins, friend, group photo, extra person, "
    "collage, storyboard, comic panel, manga panel, split screen, multiple panels, "
    "triptych, diptych, film strip, contact sheet, sequence frames, before and after, "
    "stacked frames, three images, four images, repeated same person, repeated portrait, "
    "minor sexualization, childlike body, distorted face, bad hands, watermark, "
    "text, logo, blurry, overexposed, creepy smile, plastic skin"
)


def newest_png(output_dir, prefixes, after_ts):
    candidates = []
    root = Path(output_dir)
    for p in root.rglob("*.png"):
        if not any(p.name.startswith(prefix) for prefix in prefixes):
            continue
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


def post(url, workflow):
    body = json.dumps(workflow).encode("utf-8")
    req = urllib.request.Request(f"{url}/prompt", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.loads(res.read().decode("utf-8"))["prompt_id"]


def wait_history(url, pid, timeout):
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(5)
        try:
            with urllib.request.urlopen(f"{url}/history/{pid}", timeout=15) as res:
                history = json.loads(res.read().decode("utf-8"))
        except Exception:
            continue
        if pid in history:
            status = history[pid].get("status", {}).get("status_str", "done")
            if status == "error":
                raise RuntimeError(f"T2I failed: {history[pid].get('status')}")
            return
    raise TimeoutError(f"Timed out waiting for {pid}")


def compact_shot_prompt(shot, identity, global_style, negative):
    identity = (
        identity
        .replace("same face in every shot", "consistent character design")
        .replace("in every shot", "across the project")
    )
    global_style = (
        global_style
        .replace("keyframe", "photograph")
        .replace("campaign film", "public-service photo")
        .replace("YouTube Shorts", "vertical portrait")
    )
    framing = f"{shot.get('shot_type', 'MS')}, {shot.get('angle', 'eye-level')} camera angle, {shot.get('lens_mm', 35)}mm lens"
    parts = [
        "A single uninterrupted vertical photograph of one moment.",
        "One person appears once in the image.",
        f"The person is {identity}.",
        f"She is at {shot.get('location', '')}.",
        f"{shot.get('action', '')}",
        f"The photo uses {framing}.",
        f"{shot.get('composition', '')}",
        f"{shot.get('actor_direction', '')}",
        f"{shot.get('lighting', '')}",
        f"{global_style}.",
        "Natural realistic photo, one camera exposure, one scene filling the whole canvas.",
    ]
    return " ".join(p for p in parts if p.strip())


def load_loras(path):
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    out = []
    for item in data:
        if isinstance(item, dict):
            name = item.get("name") or item.get("lora_name")
            strength = float(item.get("strength", 0.6))
        else:
            name, strength = item[0], float(item[1])
        if name and strength > 0:
            out.append((name, strength))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--shots", nargs="*", help="Shot IDs to generate. Default: all.")
    ap.add_argument("--qwen-gui-dir", default=DEFAULT_QWEN_GUI)
    ap.add_argument("--module", default="qwen_gui_v6")
    ap.add_argument("--comfy", default="http://127.0.0.1:8194")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--width", type=int, default=480)
    ap.add_argument("--height", type=int, default=832)
    ap.add_argument("--seed-base", type=int, default=26070000)
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--shift", type=float, default=2.01)
    ap.add_argument("--no-lightning", action="store_true")
    ap.add_argument("--lora-json", help="Optional JSON list of character/style LoRAs: [{'name':'x.safetensors','strength':0.6}]")
    ap.add_argument("--negative", default=NEGATIVE)
    ap.add_argument("--timeout", type=int, default=1200)
    args = ap.parse_args()

    project = Path(args.project)
    shotlist = json.loads((project / "shotlist" / "shotlist.json").read_text(encoding="utf-8-sig"))
    prompts_path = project / "prompts" / "prompts.json"
    prompts = json.loads(prompts_path.read_text(encoding="utf-8-sig")) if prompts_path.exists() else {}
    global_style = prompts.get("global_style", "photorealistic cinematic campaign keyframe")
    identity = prompts.get("character_identity", "same single recurring protagonist")
    wanted = set(args.shots or [])

    sys.path.insert(0, args.qwen_gui_dir)
    qwen = __import__(args.module)  # type: ignore
    qwen.COMFYUI_URL = args.comfy
    qwen.OUTPUT_DIR = args.output_dir
    qwen.PROMPT_PREFIX = ""
    qwen.PROMPT_SUFFIX = ""

    lora_stack = load_loras(args.lora_json)
    keyframes = project / "keyframes_t2i"
    keyframes.mkdir(parents=True, exist_ok=True)
    log = []

    selected = [s for s in shotlist if not wanted or s["shot_id"] in wanted]
    for index, shot in enumerate(selected, start=1):
        sid = shot["shot_id"]
        seed = args.seed_base + index * 101
        prompt = compact_shot_prompt(shot, identity, global_style, args.negative)
        t0 = time.time()
        workflow = qwen.build_t2i_workflow(
            prompt,
            args.width,
            args.height,
            seed,
            args.steps,
            lora_stack,
            not args.no_lightning,
            args.shift,
            False,
            snofs_on=False,
            abliterated=False,
        )
        pid = post(args.comfy, workflow)
        print(f"{sid}: queued T2I pid={pid} seed={seed}")
        wait_history(args.comfy, pid, args.timeout)
        src = newest_png(args.output_dir, [f"qwen_v6_{seed}_pass2", f"qwen_v6_{seed}"], t0)
        if not src:
            raise FileNotFoundError(f"{sid}: no qwen_v6_{seed} output found")
        dest = keyframes / f"{sid}.png"
        shutil.copy2(src, dest)
        print(f"{sid}: copied {dest}")
        log.append({"shot_id": sid, "seed": seed, "src": str(src), "dest": str(dest), "prompt": prompt})

    meta = project / "meta"
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "t2i_keyframes_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
