"""
Fire BGM via ACE-Step Gradio. Blocks until generation completes.

Usage:
  python fire_bgm.py --out <project>/audio/bgm.wav --duration 30 \
                     --prompt "dark cinematic trap, hard 808 bass, ..."
"""
import argparse
import shutil
import time
from pathlib import Path

from gradio_client import Client


DEFAULT_PROMPT = (
    "dark cinematic trap, hard-hitting 808 bass, gritty distorted synths, "
    "tense crescendo, percussive hi-hats, ominous atmosphere, "
    "130 bpm, instrumental, no vocals, commercial sting, builds to climax"
)


def find_generation_index(client, preferred=None):
    deps = client.config["dependencies"]
    if preferred is not None and 0 <= preferred < len(deps):
        return preferred

    candidates = []
    for i, dep in enumerate(deps):
        api_name = (dep.get("api_name") or "").lower()
        inputs = dep.get("inputs") or []
        labels = []
        comps = {x["id"]: x for x in client.config["components"]}
        for cid in inputs:
            labels.append(str(comps.get(cid, {}).get("props", {}).get("label", "")).lower())
        haystack = " ".join([api_name, *labels])
        if "generation" in haystack and "music caption" in haystack:
            candidates.append(i)
        elif "music caption" in haystack and "audio duration" in haystack:
            candidates.append(i)

    if not candidates:
        raise RuntimeError("Could not find ACE-Step generation endpoint. Pass --fn-index explicitly.")
    return candidates[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output WAV path")
    ap.add_argument("--duration", type=int, default=30)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--ace", default="http://127.0.0.1:7860")
    ap.add_argument("--fn-index", type=int,
                    help="Override Gradio fn_index if automatic endpoint discovery fails")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"connecting to ACE-Step {args.ace} ...")
    c = Client(args.ace, verbose=False)
    fn_index = find_generation_index(c, args.fn_index)
    print(f"using Gradio fn_index={fn_index}")

    gen = c.config["dependencies"][fn_index]
    comps = {x["id"]: x for x in c.config["components"]}
    skip = [t.is_state or t.skip for t in c.endpoints[fn_index].input_component_types]

    inputs, slot = [], []
    for i, cid in enumerate(gen["inputs"]):
        if skip[i]:
            continue
        cm = comps.get(cid, {})
        typ = cm.get("type")
        props = cm.get("props", {})
        val = props.get("value")
        if val is None:
            if typ == "slider":
                val = props.get("minimum", 0)
            elif typ == "number":
                val = 0
            elif typ == "checkbox":
                val = False
            elif typ == "checkboxgroup":
                val = []
            elif typ in ("file", "audio", "image", "video"):
                val = None
            else:
                val = ""
        slot.append(props.get("label"))
        inputs.append(val)

    def at(label):
        if label not in slot:
            raise RuntimeError(f"ACE-Step input label not found: {label}")
        return slot.index(label)

    inputs[at("Music Caption")] = args.prompt
    inputs[at("Lyrics")] = ""
    inputs[at("Audio Duration (seconds)")] = args.duration
    inputs[at("Batch Size")] = 1
    inputs[at("Track Name")] = "vocals"

    print(f"queuing {args.duration}s BGM: {args.prompt[:60]}...")
    t0 = time.time()
    job = c.submit(*inputs, fn_index=fn_index)
    result = job.result()
    print(f"done in {time.time() - t0:.1f}s")

    src = result[0]["value"]
    shutil.copy(src, out)
    print(f"saved -> {out}")


if __name__ == "__main__":
    main()
