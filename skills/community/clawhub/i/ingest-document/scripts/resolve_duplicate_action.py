from __future__ import annotations

import argparse
import json

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def normalize(value: str) -> str:
    text = (value or "").strip().lower()
    if text.startswith("duplicate:"):
        text = text.split(":", 1)[1]
    mapping = {
        "overwrite": "overwrite",
        "覆盖": "overwrite",
        "save_new": "save_new",
        "new": "save_new",
        "继续保存": "save_new",
        "cancel": "cancel",
        "取消": "cancel",
    }
    return mapping.get(text, text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action_value", required=True)
    parser.add_argument("--existing_path", default="")
    args = parser.parse_args()

    decision = normalize(args.action_value)
    if decision not in {"overwrite", "save_new", "cancel"}:
        out(json_fail("unknown_duplicate_action", "无法识别重复资料处理动作。"))
        return
    out({
        "success": True,
        "decision": decision,
        "should_save": decision in {"overwrite", "save_new"},
        "overwrite_existing": decision == "overwrite",
        "existing_path": args.existing_path,
    })


if __name__ == "__main__":
    main()
