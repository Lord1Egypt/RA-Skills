#!/usr/bin/env python3
import argparse
from pathlib import Path

from identity_rules import brand_guidance, detect_explicit_brand
from skill_paths import require_live_input
from validate_json import load_json
from validate_self_intro_submission import validate_submission


TARGET_SPEC = {
    "master_width": 960,
    "master_height": 720,
    "safe_margin": 64,
    "usage_note": "This image will be used in the poster photo area of the card. Keep the character centered and readable after mild cover-cropping.",
}


def build_prompt(submission: dict) -> str:
    agent = submission["agent"]
    identity = submission["identity"]
    style = identity["character_style"]
    explicit_brand = detect_explicit_brand(submission)
    neutral_default = explicit_brand is None and style != "lobster"
    if neutral_default:
        subject_hint = "neutral anthropomorphic AI agent character"
        style_guard = "The character silhouette must read as this specific neutral agent, not a generic mascot."
    else:
        subject_hint = "anthropomorphic lobster agent mascot" if style == "lobster" else "anthropomorphic AI agent character"
        style_guard = (
            "The lobster silhouette must read clearly as lobster: visible claws, segmented body, antennae or shell cues."
            if style == "lobster"
            else "The character silhouette must read as this specific agent, not a generic mascot."
        )
    return f"""Image brief for {agent['name']}

Goal:
- create a final 8-bit character image outside this repo
- this repo does not auto-draw the final image
- the job here is to guide the artist / image model and then review whether the result matches the agent identity

Required style:
- standard 8-bit pixel art
- low-resolution sprite logic
- hard edges
- strong silhouette
- one clearly recognizable character
- no smooth gradients
- no painterly rendering
- no reused repo sample composition
- no old mascot template
- do not imitate the existing repo sample image composition
- do not produce a minor variation of the current sample mascot
- build the silhouette and props strictly from the current agent identity
- no abstract icon, no pure geometry, no symbol-only solution
- no photorealism

Character direction:
- subject: {subject_hint}
- role: {identity['role']}
- visual brief: {identity['visual_brief']}
- persona tags: {", ".join(identity['persona_tags'])}
- top capabilities: {", ".join(identity['top_capabilities'])}
- proof anchor: {identity['proof_anchor']}
- {style_guard}
- {brand_guidance(submission)}
- before drawing, identify one clear character concept in one sentence
- before drawing, identify the 1 to 3 visual signals that prove the role
- if the concept cannot be described clearly in words, do not draw yet; rewrite the concept first

Composition:
- 3/4 portrait or upper-body character framing
- centered composition
- transparent background or fully empty background only
- do not draw scenery, interface backdrops, posters, dashboards, stickers, or environment decoration
- props are allowed only when they directly communicate one of the listed capabilities
- every visible prop must map back to the role, persona tags, or top capabilities
- leave safe space around the character silhouette

Canvas spec:
- output PNG
- target size: {TARGET_SPEC['master_width']} x {TARGET_SPEC['master_height']}
- keep at least {TARGET_SPEC['safe_margin']} px safe margin around the main silhouette
- {TARGET_SPEC['usage_note']}
- preferred delivery: transparent PNG

Prompt draft:
{identity['selfie_prompt']}

Priority:
- the rules above override any conflicting wording in the draft
- use the draft for subject clues, not for background or layout
- if the draft mentions a background, ignore it unless it says the image must be empty or transparent

Review checklist:
- can a stranger infer the role from the silhouette and 1-2 props alone
- does the design reflect the actual agent traits instead of a generic agent mascot
- does the image avoid any background art
- can a stranger name the subject as a character instead of calling it an abstract shape
- for lobster mode: would a viewer immediately call it a lobster rather than a random creature
- are the persona tags and capability cues visible without text overlay

Delivery rules:
- return a final PNG image
- generate a fresh image for this exact agent identity; do not reuse a sample image from this repo
- if the image model only outputs square images, crop or extend to {TARGET_SPEC['master_width']}x{TARGET_SPEC['master_height']} while keeping the subject centered and the background empty
- if the result fails the review checklist, redo it instead of attaching it
- after image generation, attach it back into the share card with:
  python3 scripts/attach_generated_image.py path/to/share-card.json --image-url <URL>
"""


def main():
    parser = argparse.ArgumentParser(description="Build an external image-generation task from a validated self-intro submission")
    parser.add_argument("submission_json", help="Path to validated self-intro submission JSON")
    parser.add_argument("--out", default="image-task-prompt.txt", help="Output prompt path")
    args = parser.parse_args()

    input_path = Path(args.submission_json)
    require_live_input(input_path, "submission_json")
    payload = load_json(input_path)
    validate_submission(payload)
    prompt = build_prompt(payload)
    Path(args.out).write_text(prompt.rstrip() + "\n", encoding="utf-8")
    print(f"[OK] Wrote image-task prompt to {args.out}")


if __name__ == "__main__":
    main()
