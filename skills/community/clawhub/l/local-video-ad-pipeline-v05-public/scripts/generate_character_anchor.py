"""
Generate a reusable protagonist anchor image with the local Qwen-Image GUI stack.

Output:
  <project>/character/anchor.png
  <project>/character/character_bible.json

Requires the Qwen-Image GUI/ComfyUI edit stack, normally on http://127.0.0.1:8189.
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
                raise RuntimeError(f"Qwen anchor generation failed: {history[pid].get('status')}")
            return
    raise TimeoutError(f"Timed out waiting for {pid}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--prompt", required=True, help="Stable protagonist description.")
    ap.add_argument("--qwen-gui-dir", default=DEFAULT_QWEN_GUI)
    ap.add_argument("--module", default="qwen_gui_v6", help="qwen-gui module to import, usually qwen_gui_v6.")
    ap.add_argument("--comfy", default="http://127.0.0.1:8194")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT)
    ap.add_argument("--width", type=int, default=832)
    ap.add_argument("--height", type=int, default=480)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--steps", type=int, default=8)
    ap.add_argument("--no-lightning", action="store_true")
    ap.add_argument("--timeout", type=int, default=900)
    args = ap.parse_args()

    sys.path.insert(0, args.qwen_gui_dir)
    qwen = __import__(args.module)  # type: ignore

    qwen.COMFYUI_URL = args.comfy
    qwen.OUTPUT_DIR = args.output_dir
    if hasattr(qwen, "INPUT_DIR") and args.output_dir.endswith("output"):
        qwen.INPUT_DIR = str(Path(args.output_dir).with_name("input"))

    seed = args.seed or int(time.time()) % 100000000
    raw_stack = getattr(qwen, "T2I_LORA_STACK", [])
    lora_stack = []
    for item in raw_stack:
        if len(item) == 3:
            _, lora_name, strength = item
        else:
            lora_name, strength = item
        lora_stack.append((lora_name, strength))
    try:
        workflow = qwen.build_t2i_workflow(
            args.prompt, args.width, args.height, seed, args.steps,
            lora_stack,
            not args.no_lightning, 3.0, True,
        )
    except TypeError:
        workflow = qwen.build_t2i_workflow(
            args.prompt, args.width, args.height, seed, args.steps,
            1.0, not args.no_lightning, 3.0, True,
        )
    t0 = time.time()
    pid = post(args.comfy, workflow)
    print(f"queued anchor pid={pid} seed={seed}")
    wait_history(args.comfy, pid, args.timeout)

    src = newest_png(args.output_dir, f"qwen_gui_{seed}", t0) or newest_png(args.output_dir, f"qwen_v6_{seed}", t0)
    if not src:
        raise FileNotFoundError(f"No anchor output found for qwen_gui_{seed}")

    project = Path(args.project)
    char_dir = project / "character"
    char_dir.mkdir(parents=True, exist_ok=True)
    dest = char_dir / "anchor.png"
    shutil.copy2(src, dest)
    bible = {
        "anchor": str(dest),
        "prompt": args.prompt,
        "seed": seed,
        "width": args.width,
        "height": args.height,
        "identity_rules": [
            "Keep the same face, hair, age, body type, and clothing identity unless the user explicitly requests a change.",
            "Only change pose, camera angle, lighting, and scene action for each shot.",
            "When the protagonist is a minor, school-age, childlike, or age-ambiguous character, keep clothing and presentation conservative and age-safe. For clearly adult protagonists, do not suppress glamour, fitted fashion, swimwear, lingerie, or body-forward styling by default.",
        ],
    }
    (char_dir / "character_bible.json").write_text(json.dumps(bible, indent=2, ensure_ascii=False), encoding="utf-8")
    print(dest)


if __name__ == "__main__":
    main()
