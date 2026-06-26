#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timedelta


FORMATS = [
    "%Y-%m-%d %H:%M",
    "%Y/%m/%d %H:%M",
    "%Y.%m.%d %H:%M",
    "%Y年%m月%d日 %H:%M",
    "%Y年%m月%d日%H:%M",
    "%Y-%m-%dT%H:%M",
]


def normalize(text: str) -> str:
    text = text.strip()
    text = text.replace("上午", " ").replace("下午", " ")
    text = re.sub(r"\s+", " ", text)
    return text


def parse_dt(text: str) -> datetime:
    text = normalize(text)
    for fmt in FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError("Unsupported datetime format. Use e.g. 2026-03-20 14:30")


def main() -> int:
    p = argparse.ArgumentParser(description="Generate 3 reminder times before a medical appointment")
    p.add_argument("--appointment", required=True, help="Appointment datetime, e.g. 2026-03-20 14:30")
    args = p.parse_args()

    dt = parse_dt(args.appointment)
    reminders = [
        ("T-12h", dt - timedelta(hours=12)),
        ("T-6h", dt - timedelta(hours=6)),
        ("T-2h", dt - timedelta(hours=2)),
    ]
    output = {
        "appointment": dt.strftime("%Y-%m-%d %H:%M"),
        "reminders": [
            {"label": label, "time": when.strftime("%Y-%m-%d %H:%M")} for label, when in reminders
        ],
        "note": "默认输出提前半天内的3次提醒：12小时、6小时、2小时。",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
