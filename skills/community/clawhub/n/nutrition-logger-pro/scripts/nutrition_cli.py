from __future__ import annotations

import argparse
import json
import sys

from log_store import (
    StoreError,
    append_entry,
    get_log_dir,
    summary_day,
    summary_week,
    undo_last,
    update_entry,
)
from nutrition_math import (
    NutritionError,
    calculate_per_100g,
    calculate_per_serving,
)


class ChineseArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        write_json({"ok": False, "error": "参数错误，请检查命令和参数。"})
        raise SystemExit(2)


def read_json_stdin():
    raw = sys.stdin.buffer.read().decode("utf-8").strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise StoreError("输入必须是有效 JSON。") from exc


def write_json(payload):
    data = json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    sys.stdout.buffer.write(data.encode("utf-8"))


def handle_calculate_label(payload):
    label_per = str(payload.get("label_per", "")).lower()
    food = payload.get("food") or ""
    nutrition = payload.get("nutrition_per_unit") or {}
    if label_per in {"100g", "per_100g", "每100g"}:
        return calculate_per_100g(food, payload.get("eaten_amount_g"), nutrition)
    if label_per in {"serving", "per_serving", "每份"}:
        return calculate_per_serving(food, payload.get("servings_eaten"), nutrition)
    raise NutritionError("label_per 只支持 100g 或 serving。")


def run_command(args, payload):
    log_dir = get_log_dir(args.log_dir)
    if args.command == "calculate-label":
        return handle_calculate_label(payload)
    if args.command == "append-entry":
        return {"ok": True, "entry": append_entry(log_dir, payload)}
    if args.command == "summary-day":
        return summary_day(log_dir, payload.get("date"), payload.get("timezone"))
    if args.command == "summary-week":
        return summary_week(log_dir, payload.get("week_start"), payload.get("timezone"))
    if args.command == "undo-last":
        entry = undo_last(log_dir)
        return {"ok": True, "message": "已撤销上一条饮食记录。", "undone_entry": entry}
    if args.command == "update-entry":
        entry = update_entry(log_dir, payload)
        return {"ok": True, "message": "已修正记录并重新计算合计。", "entry": entry}
    raise StoreError(f"不支持的命令：{args.command}")


def build_parser():
    parser = ChineseArgumentParser(description="nutrition_logger 本地日志工具")
    parser.add_argument("--log-dir", help="日志目录；默认使用 NUTRITION_LOG_DIR 或当前工作区 nutrition-log/")
    parser.add_argument(
        "command",
        choices=[
            "calculate-label",
            "append-entry",
            "summary-day",
            "summary-week",
            "undo-last",
            "update-entry",
        ],
    )
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        payload = read_json_stdin()
        result = run_command(args, payload)
        write_json(result)
        return 0
    except StoreError as exc:
        result = {"ok": False, "error": str(exc)}
        candidates = getattr(exc, "candidates", None)
        if candidates is not None:
            result["candidates"] = candidates
        write_json(result)
        return 1
    except NutritionError as exc:
        write_json({"ok": False, "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
