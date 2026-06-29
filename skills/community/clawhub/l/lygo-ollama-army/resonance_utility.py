#!/usr/bin/env python3
"""
LYGO Resonance Utility Bridge for the Ollama Army
Makes the new lygo-ollama-army skill a perfect companion/utility for the LYGO RESONANCE skill.

Usage examples:
  python resonance_utility.py --prepare-batch ./my_images --action both
  python resonance_utility.py --queue-profile image.jpg --champion SEPHRAEL

It generates task JSONs that the army daemons (especially "resonance-analyst" role) can pick up.
The analyst daemon then recommends or directly calls the Resonance skill scripts (resonance_engine.py / lygo_profile.py).

Drop the generated .task.json files into the army's ollama_queue/ folder while resonance-analyst daemons are running.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

HERE = Path(__file__).resolve().parent
QUEUE = HERE / "ollama_queue"

def ensure_queue():
    QUEUE.mkdir(parents=True, exist_ok=True)

def create_task(role: str, payload: dict, task_id: str = None):
    ensure_queue()
    if not task_id:
        task_id = f"res-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    task = {"id": task_id, "role": role, "payload": payload, "created": datetime.now().isoformat()}
    path = QUEUE / f"{task_id}.task.json"
    path.write_text(json.dumps(task, indent=2), encoding="utf-8")
    print(f"✓ Queued {role} task → {path.name}")
    return path

def prepare_batch(image_folder: str, action: str = "both"):
    folder = Path(image_folder)
    images = list(folder.glob("*.jpg")) + list(folder.glob("*.png")) + list(folder.glob("*.jpeg"))
    if not images:
        print("No images found.")
        return
    for img in images:
        if action in ("profile", "both"):
            create_task("resonance-analyst", {"image_path": str(img), "action": "profile"})
        if action in ("soundscape", "both"):
            create_task("resonance-analyst", {"image_path": str(img), "action": "soundscape"})
    print(f"\nBatch prepared for {len(images)} images. Run resonance-analyst daemons (with or without champion) to process.")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Utility bridge: Ollama Army ↔ LYGO Resonance skill")
    ap.add_argument("--prepare-batch", help="Folder of images to queue for the army + Resonance tools")
    ap.add_argument("--action", choices=["both", "profile", "soundscape"], default="both")
    ap.add_argument("--queue-profile", help="Single image for profile generation (queues resonance-analyst task)")
    ap.add_argument("--queue-soundscape", help="Single image for soundscape (queues resonance-analyst task)")
    ap.add_argument("--champion", help="Optional champion to associate with the task (e.g. SEPHRAEL for creative translation)")
    args = ap.parse_args()

    if args.prepare_batch:
        prepare_batch(args.prepare_batch, args.action)
    elif args.queue_profile:
        payload = {"image_path": args.queue_profile, "action": "profile"}
        if args.champion: payload["champion_hint"] = args.champion
        create_task("resonance-analyst", payload)
    elif args.queue_soundscape:
        payload = {"image_path": args.queue_soundscape, "action": "soundscape"}
        if args.champion: payload["champion_hint"] = args.champion
        create_task("resonance-analyst", payload)
    else:
        print("Use --prepare-batch FOLDER or --queue-profile IMAGE [--champion NAME]")
        print("See SKILL.md for full integration with https://deepseekoracle.github.io/Excavationpro/LYGORESONANCE.html")