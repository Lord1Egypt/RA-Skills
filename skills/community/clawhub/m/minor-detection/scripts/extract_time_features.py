#!/usr/bin/env python3
# 模块说明：
# - bundled skill 的时间脚本入口。
# - 当 payload 带时间线索时由总控脚本调用。

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from _skill_time_utils import build_time_feature_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract structured time features from a normalized timestamp string.",
    )
    parser.add_argument(
        "--timestamp",
        required=True,
        help="Raw timestamp text such as '2026-03-18 周三 08:59' or '2026-03-18 23:40:00'.",
    )
    parser.add_argument(
        "--timezone",
        default="Asia/Shanghai",
        help="Timezone label kept in the output payload.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_time_feature_payload(args.timestamp, args.timezone)
    # Keep subprocess output ASCII-safe so Windows parents using legacy decoders can still read it.
    print(json.dumps(payload, ensure_ascii=True))


if __name__ == "__main__":
    main()
