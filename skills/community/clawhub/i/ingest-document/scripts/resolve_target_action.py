from __future__ import annotations

import argparse
import json

from utils import json_fail


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--action_value", required=True)
    args = parser.parse_args()

    value = args.action_value.strip()
    if value.startswith("ingest_target:"):
        target = value.split(":", 1)[1]
        if target not in {"personal", "team", "both"}:
            out(json_fail("bad_ingest_target", "无法识别入库目标。"))
            return
        out({
            "success": True,
            "action": "select_ingest_target",
            "explicit_target": target,
            "next": "call_ingest_one_again",
        })
        return
    out(json_fail("unknown_card_action", "无法识别 ingest_document 卡片动作。"))


if __name__ == "__main__":
    main()
