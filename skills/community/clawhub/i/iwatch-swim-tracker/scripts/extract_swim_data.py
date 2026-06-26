#!/usr/bin/env python3
"""提取并保存游泳训练数据。

接收 JSON 格式的结构化游泳数据（由 AI vision 提取后传入），
校验必填字段后按日期归档保存到 swim_data/YYYY/MM/YYYY-MM-DD.json。
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "swim_data"

REQUIRED_FIELDS = [
    "date",
    "time_range",
    "pool_length",
    "total_distance",
    "laps",
    "strokes",
    "duration",
    "duration_seconds",
    "avg_pace",
    "avg_pace_seconds",
    "avg_heart_rate",
]


def validate(data: dict) -> list[str]:
    """校验必填字段，返回缺失字段列表。"""
    return [f for f in REQUIRED_FIELDS if f not in data or data[f] is None]


def save(data: dict) -> dict:
    """按日期归档保存，同一天多次训练追加到数组。返回结果字典。"""
    date_str = data["date"]  # YYYY-MM-DD
    year, month, _ = date_str.split("-")

    dir_path = DATA_DIR / year / month
    dir_path.mkdir(parents=True, exist_ok=True)

    file_path = dir_path / f"{date_str}.json"

    # 同一天的数据直接覆盖（用户可能重发截图以更正数据）
    file_path.write_text(json.dumps([data], ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "status": "saved",
        "file": str(file_path),
        "date": date_str,
        "total_distance": data["total_distance"],
    }


def check_date(date_str: str) -> dict:
    """检查某日期是否已有训练记录。"""
    year, month, _ = date_str.split("-")
    file_path = DATA_DIR / year / month / f"{date_str}.json"
    if file_path.exists():
        existing = json.loads(file_path.read_text(encoding="utf-8"))
        if not isinstance(existing, list):
            existing = [existing]
        return {
            "exists": True,
            "date": date_str,
            "sessions": len(existing),
            "data": existing,
        }
    return {"exists": False, "date": date_str}


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_swim_data.py '<json_string>'", file=sys.stderr)
        print("       extract_swim_data.py --check-date YYYY-MM-DD", file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "--check-date":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "reason": "missing date argument"}))
            sys.exit(1)
        print(json.dumps(check_date(sys.argv[2]), ensure_ascii=False))
        return

    raw = sys.argv[1]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(json.dumps({"status": "error", "reason": f"invalid_json: {e}"}))
        sys.exit(1)

    missing = validate(data)
    if missing:
        print(json.dumps({
            "status": "error",
            "reason": "missing_fields",
            "fields": missing,
        }))
        sys.exit(1)

    result = save(data)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
