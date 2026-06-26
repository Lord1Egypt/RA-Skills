#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from skill_paths import SHARE_CARD_SCHEMA_PATH, require_live_input
from validate_json import load_json, validate
from validate_self_intro_submission import validate_submission


def build_share_card(submission: dict) -> dict:
    identity = submission["identity"]
    owner = submission["owner"]
    agent = submission["agent"]
    card_id = f"card:{agent['name']}-submitted".replace(" ", "-")

    return {
        "schema_version": "share-card/1.0",
        "card_id": card_id,
        "name": agent["name"],
        "role": identity["role"],
        "tagline": identity["tagline"],
        "value_line": identity.get("value_line") or identity["best_for"],
        "top_capabilities": identity["top_capabilities"],
        "best_for": identity["best_for"],
        "proof_anchor": identity["proof_anchor"],
        "owner": owner,
        "visual_brief": identity["visual_brief"],
        "character_style": identity["character_style"],
        "image": {
            "placeholder": "image"
        },
        "qr": {
            "placeholder": "qr"
        },
        "image_strategy": "image-gen",
        "selfie_prompt": identity["selfie_prompt"],
        "spread_line": f"{identity['role']}，一句话就能看懂：{identity['tagline']}",
        "memory_basis": identity["memory_basis"],
        "share_keywords": identity["share_keywords"],
        "source_count": identity["source_count"],
        "poster_headline": identity["poster_headline"],
        "poster_subline": identity["poster_subline"],
        "persona_tags": identity["persona_tags"],
        "share_caption": identity["share_caption"],
    }


def main():
    parser = argparse.ArgumentParser(description="Convert a validated self-intro submission into share-card JSON")
    parser.add_argument("submission_json", help="Path to self-intro submission JSON")
    parser.add_argument("--out", default="share-card.json", help="Output share-card JSON path")
    args = parser.parse_args()

    input_path = Path(args.submission_json)
    require_live_input(input_path, "submission_json")
    payload = load_json(input_path)
    validate_submission(payload)
    share_card = build_share_card(payload)
    validate(share_card, load_json(SHARE_CARD_SCHEMA_PATH))

    out_path = Path(args.out)
    out_path.write_text(json.dumps(share_card, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[OK] Wrote share card to {out_path}")


if __name__ == "__main__":
    main()
