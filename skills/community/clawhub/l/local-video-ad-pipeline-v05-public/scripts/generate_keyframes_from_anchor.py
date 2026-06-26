"""
Generate shot keyframes from one protagonist anchor using Qwen Image Edit.

This is the character-consistency path:
  1. Create or provide <project>/character/anchor.png.
  2. Use this script to edit the same protagonist into each shot.
  3. Inspect the generated contact sheet before Wan2.2 video rendering.
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


def newest_png(output_dir, prefix, after_ts):
    candidates = []
    for p in Path(output_dir).rglob("*.png"):
        if not p.name.startswith(prefix):
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
            with urllib.request.urlopen(f"{url}/history/{pid}", timeout=10) as res:
                history = json.loads(res.read().decode("utf-8"))
        except Exception:
            continue
        if pid in history:
            status = history[pid].get("status", {}).get("status_str", "done")
            if status == "error":
                raise RuntimeError(f"Qwen edit failed: {history[pid].get('status')}")
            return
    raise TimeoutError(f"Timed out waiting for {pid}")


def shot_instruction(shot, identity, global_style):
    sid = shot["shot_id"]
    return (
        f"Create keyframe {sid} for a video while preserving the exact same protagonist from the reference image. "
        f"Identity lock: {identity}. "
        "Exactly one visible person in the frame. No duplicate, no twin, no friend, no second person, no group photo. "
        "Keep the same face, hair, age, body type, and clothing identity. "
        "Do not change the protagonist into another person. "
        f"Scene: {shot.get('action', '')}. "
        f"Shot type: {shot.get('shot_type', 'medium shot')}. "
        f"Camera angle: {shot.get('angle', 'eye-level')}. Lens: {shot.get('lens_mm', 35)}mm. "
        f"Camera motion cue for later video: {shot.get('camera_motion', 'locked')}. "
        f"Director intent: {shot.get('director_intent', '')}. "
        f"Actor direction: {shot.get('actor_direction', '')}. "
        f"Composition: {shot.get('composition', '')}. "
        f"Continuity cue: {shot.get('continuity', '')}. "
        f"Mood: {shot.get('mood', '')}. Lighting: {shot.get('lighting', '')}. "
        f"Style: {global_style}. "
        "Photorealistic cinematic frame, clear composition, no visible subtitle text, no watermark. "
        "If the reference is close-up, reinterpret it as the same single protagonist in the requested scene rather than placing the reference image beside another person."
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--anchor", help="Reference protagonist image. Defaults to <project>/character/anchor.png.")
    ap.add_argument("--style-ref", action="append", default=[],
                    help="Optional extra reference image, up to two. Use for outfit/style boards.")
    ap.add_argument("--shots", nargs="*", help="Shot IDs to generate. Default: all.")
    ap.add_argument("--qwen-gui-dir", default=DEFAULT_QWEN_GUI)
    ap.add_argument("--module", default="qwen_gui_v6", help="qwen-gui module to import, usually qwen_gui_v6.")
    ap.add_argument("--comfy", default="http://127.0.0.1:8194")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--seed-base", type=int, default=26050700)
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--target-pixels", type=float, default=1.0)
    ap.add_argument("--no-lightning", action="store_true")
    ap.add_argument("--anypose", action="store_true")
    ap.add_argument("--anypose-strength", type=float, default=0.55)
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    project = Path(args.project)
    anchor = Path(args.anchor) if args.anchor else project / "character" / "anchor.png"
    if not anchor.exists():
        raise FileNotFoundError(anchor)

    shotlist = json.loads((project / "shotlist" / "shotlist.json").read_text(encoding="utf-8-sig"))
    prompts_path = project / "prompts" / "prompts.json"
    prompts = json.loads(prompts_path.read_text(encoding="utf-8-sig")) if prompts_path.exists() else {}
    global_style = prompts.get("global_style", "cinematic realistic video keyframe")
    identity = prompts.get(
        "character_identity",
        "the same single protagonist from the reference image, same face, hair, age, and wardrobe identity",
    )
    wanted = set(args.shots or [])

    sys.path.insert(0, args.qwen_gui_dir)
    qwen = __import__(args.module)  # type: ignore

    qwen.COMFYUI_URL = args.comfy
    qwen.OUTPUT_DIR = args.output_dir
    if hasattr(qwen, "INPUT_DIR") and args.output_dir.endswith("output"):
        qwen.INPUT_DIR = str(Path(args.output_dir).with_name("input"))

    refs = [qwen.upload_to_input(str(anchor), print)]
    for ref in args.style_ref[:2]:
        refs.append(qwen.upload_to_input(str(Path(ref)), print))

    keyframes = project / "keyframes"
    keyframes.mkdir(parents=True, exist_ok=True)
    log = []

    selected = [s for s in shotlist if not wanted or s["shot_id"] in wanted]
    for index, shot in enumerate(selected, start=1):
        sid = shot["shot_id"]
        seed = args.seed_base + index * 101
        instruction = shot_instruction(shot, identity, global_style)
        t0 = time.time()
        workflow = qwen.build_edit_workflow(
            refs,
            instruction,
            seed,
            args.steps,
            not args.no_lightning,
            args.target_pixels,
            args.anypose,
            args.anypose_strength,
        )
        pid = post(args.comfy, workflow)
        print(f"{sid}: queued edit pid={pid} seed={seed}")
        wait_history(args.comfy, pid, args.timeout)
        src = (
            newest_png(args.output_dir, f"qwen_edit_{seed}", t0)
            or newest_png(args.output_dir, f"qwen_edit_v5_{seed}", t0)
        )
        if not src:
            raise FileNotFoundError(f"{sid}: no qwen_edit_{seed} output found")
        dest = keyframes / f"{sid}.png"
        shutil.copy2(src, dest)
        print(f"{sid}: copied {dest}")
        log.append({"shot_id": sid, "seed": seed, "src": str(src), "dest": str(dest), "instruction": instruction})

    meta = project / "meta"
    meta.mkdir(parents=True, exist_ok=True)
    (meta / "anchor_edit_keyframes_log.json").write_text(
        json.dumps(log, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
