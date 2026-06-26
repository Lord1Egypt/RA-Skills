#!/usr/bin/env python3
"""Deterministic insight generation and subscription helpers for the private-assistant skill."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from records import (  # noqa: E402
    DEFAULT_CURRENCY,
    EXPENSE_CATEGORY_KEYWORDS,
    RecordStore,
    _as_datetime,
    now_local,
)


DEFAULT_WEEKLY_SCHEDULE = "0 10 * * 1"
DEFAULT_MONTHLY_SCHEDULE = "0 10 1 * *"
LIFESTYLE_KEYWORDS = ("熬夜", "晚睡", "失眠", "焦虑", "压力", "累", "疲惫", "状态", "开心", "复盘")
WEEKDAY_LABELS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
PERIOD_LABELS = {
    "week": "本周",
    "month": "本月",
    "7d": "最近7天",
    "30d": "最近30天",
}
NEXT_PERIOD_LABELS = {
    "week": "下周",
    "month": "下月",
    "7d": "接下来几天",
    "30d": "下个阶段",
}
LOW_SIGNAL_MIN_TRANSACTIONS = {
    "week": 3,
    "month": 5,
    "7d": 3,
    "30d": 5,
}


@dataclass
class InsightWindow:
    period: str
    label: str
    start: datetime
    end: datetime
    previous_start: datetime | None
    previous_end: datetime | None


def _print(payload: dict[str, Any], *, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def _parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on"}:
        return True
    if text in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def _format_number(value: float) -> str:
    text = f"{float(value):.2f}".rstrip("0").rstrip(".")
    return text or "0"


def _format_money(value: float, currency: str = DEFAULT_CURRENCY) -> str:
    amount_text = _format_number(value)
    if str(currency or DEFAULT_CURRENCY).upper() == "CNY":
        return f"{amount_text} 元"
    return f"{amount_text} {currency}"


def _format_change_text(current: float, previous: float) -> str:
    if previous <= 0:
        return "新增" if current > 0 else "持平"
    delta = current - previous
    if abs(delta) < 0.01:
        return "持平"
    pct = (delta / previous) * 100
    return f"{pct:+.0f}%"


def _truncate(text: str | None, limit: int = 18) -> str:
    raw = " ".join(str(text or "").split())
    if len(raw) <= limit:
        return raw
    return raw[:limit].rstrip() + "…"


def _weekday_label(value: datetime) -> str:
    return WEEKDAY_LABELS[value.weekday()]


def _format_date_label(value: str | None, *, period: str) -> str | None:
    dt = _as_datetime(value)
    if dt is None:
        return None
    if period == "week":
        return _weekday_label(dt)
    if period == "month":
        return dt.strftime("%m-%d")
    return dt.strftime("%m-%d")


def _resolve_window(period: str) -> InsightWindow:
    current = now_local()
    if period == "week":
        start = datetime.combine(current.date(), datetime.min.time(), tzinfo=current.tzinfo) - timedelta(days=current.weekday())
        end = start + timedelta(days=7)
        previous_start = start - timedelta(days=7)
        previous_end = start
    elif period == "month":
        start = datetime(current.year, current.month, 1, tzinfo=current.tzinfo)
        if current.month == 12:
            end = datetime(current.year + 1, 1, 1, tzinfo=current.tzinfo)
        else:
            end = datetime(current.year, current.month + 1, 1, tzinfo=current.tzinfo)
        if start.month == 1:
            previous_start = datetime(start.year - 1, 12, 1, tzinfo=start.tzinfo)
        else:
            previous_start = datetime(start.year, start.month - 1, 1, tzinfo=start.tzinfo)
        previous_end = start
    elif period.endswith("d") and period[:-1].isdigit():
        days = int(period[:-1])
        end = current + timedelta(seconds=1)
        start = end - timedelta(days=days)
        previous_end = start
        previous_start = start - timedelta(days=days)
    else:
        raise ValueError(f"Unsupported insight period: {period}")
    return InsightWindow(
        period=period,
        label=PERIOD_LABELS.get(period, period),
        start=start,
        end=end,
        previous_start=previous_start,
        previous_end=previous_end,
    )


def _category_totals(records: list[dict[str, Any]]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for record in records:
        category = str(record.get("category") or "其他")
        totals[category] = round(totals.get(category, 0.0) + float(record.get("amount") or 0.0), 2)
    return totals


def _top_categories(records: list[dict[str, Any]], *, limit: int = 3) -> list[dict[str, Any]]:
    totals = _category_totals(records)
    total_amount = round(sum(totals.values()), 2)
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    results = []
    for name, amount in ranked[:limit]:
        share = round((amount / total_amount), 4) if total_amount else 0.0
        results.append({"category": name, "amount": amount, "share": share})
    return results


def _frequency_categories(records: list[dict[str, Any]], *, limit: int = 3) -> list[dict[str, Any]]:
    counts = Counter(str(record.get("category") or "其他") for record in records)
    totals = _category_totals(records)
    ranked = sorted(counts.items(), key=lambda item: (-item[1], -totals.get(item[0], 0.0), item[0]))
    return [
        {"category": name, "count": count, "amount": totals.get(name, 0.0)}
        for name, count in ranked[:limit]
    ]


def _largest_expense_day(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not records:
        return None
    totals: dict[str, float] = defaultdict(float)
    for record in records:
        occurred_at = _as_datetime(record.get("occurred_at"))
        if occurred_at is None:
            continue
        day_key = occurred_at.date().isoformat()
        totals[day_key] += float(record.get("amount") or 0.0)
    if not totals:
        return None
    day, amount = max(totals.items(), key=lambda item: (item[1], item[0]))
    return {"date": day, "amount": round(amount, 2)}


def _build_anomalies(
    current_totals: dict[str, float],
    previous_totals: dict[str, float],
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    anomalies: list[dict[str, Any]] = []
    largest_change: dict[str, Any] | None = None

    for category in sorted(set(current_totals) | set(previous_totals)):
        current = round(current_totals.get(category, 0.0), 2)
        previous = round(previous_totals.get(category, 0.0), 2)
        delta = round(current - previous, 2)

        candidate = {
            "category": category,
            "current": current,
            "previous": previous,
            "delta": delta,
            "change_text": _format_change_text(current, previous),
        }

        if largest_change is None or delta > largest_change["delta"]:
            largest_change = dict(candidate)

        if current <= 0 or delta <= 0:
            continue
        if previous == 0 and current >= 80:
            candidate["signal"] = "new_high_spend"
            anomalies.append(candidate)
            continue
        if previous > 0 and delta >= 50 and current >= previous * 1.5:
            candidate["signal"] = "surge"
            anomalies.append(candidate)

    anomalies.sort(key=lambda item: (-item["delta"], item["category"]))
    return anomalies, largest_change


def _memo_score(memo: dict[str, Any], top_categories: list[dict[str, Any]]) -> int:
    text = " ".join(
        filter(
            None,
            [
                str(memo.get("title") or ""),
                str(memo.get("content") or ""),
                " ".join(str(tag) for tag in (memo.get("tags") or [])),
            ],
        )
    ).lower()
    score = 0
    if memo.get("kind") == "reflection":
        score += 2
    if any(keyword.lower() in text for keyword in LIFESTYLE_KEYWORDS):
        score += 2
    for category in top_categories:
        for keyword in EXPENSE_CATEGORY_KEYWORDS.get(category["category"], []):
            if keyword.lower() in text:
                score += 3
                break
    return score


def _related_memos(memos: list[dict[str, Any]], top_categories: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored = []
    for memo in memos:
        score = _memo_score(memo, top_categories)
        if score <= 0:
            continue
        scored.append((score, memo))
    scored.sort(key=lambda item: (item[0], item[1].get("created_at", "")), reverse=True)
    selected = [memo for _, memo in scored[:2]]
    selected.sort(key=lambda item: item.get("created_at", ""), reverse=True)
    return selected


def _format_memo_line(memos: list[dict[str, Any]], *, period: str) -> str | None:
    if not memos:
        return None
    parts = []
    for memo in memos[:2]:
        label = _format_date_label(memo.get("created_at"), period=period) or "近期"
        content = _truncate(memo.get("content") or memo.get("title"), 16)
        parts.append(f"{label}提到“{content}”")
    return "；".join(parts)


def _quality_metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {
            "missing_note_count": 0,
            "other_category_count": 0,
            "note_coverage": 0.0,
            "other_category_share": 0.0,
        }
    missing_note_count = sum(
        1
        for record in records
        if not (str(record.get("note") or "").strip() or str(record.get("counterparty") or "").strip())
    )
    other_category_count = sum(1 for record in records if str(record.get("category") or "其他") == "其他")
    total = len(records)
    return {
        "missing_note_count": missing_note_count,
        "other_category_count": other_category_count,
        "note_coverage": round((total - missing_note_count) / total, 4),
        "other_category_share": round(other_category_count / total, 4),
    }


def _format_top_categories(categories: list[dict[str, Any]], currency: str, *, limit: int) -> str | None:
    if not categories:
        return None
    return "/".join(
        f"{entry['category']} {_format_money(entry['amount'], currency)}"
        for entry in categories[:limit]
    )


def _format_frequency(categories: list[dict[str, Any]]) -> str | None:
    if not categories:
        return None
    return "/".join(f"{entry['category']} {entry['count']}笔" for entry in categories)


def _format_anomaly_line(anomalies: list[dict[str, Any]], currency: str) -> str:
    if not anomalies:
        return "暂未发现明显异常"
    parts = []
    for item in anomalies[:2]:
        if item["previous"] <= 0:
            parts.append(f"{item['category']} 新增 {_format_money(item['current'], currency)}")
        else:
            parts.append(f"{item['category']} {item['change_text']}（+{_format_money(item['delta'], currency)}）")
    return "；".join(parts)


def _choose_suggestion(
    *,
    period: str,
    anomalies: list[dict[str, Any]],
    top_categories: list[dict[str, Any]],
    related_memos: list[dict[str, Any]],
    quality: dict[str, Any],
) -> str | None:
    next_period = NEXT_PERIOD_LABELS.get(period, "接下来")
    if anomalies:
        category = anomalies[0]["category"]
        return f"{next_period}先盯住{category}支出，看它是一次性还是开始变成常态。"
    if quality["other_category_share"] >= 0.35 or quality["note_coverage"] < 0.6:
        return "下次尽量补上分类和备注，后续更容易识别异常消费。"
    if top_categories and top_categories[0]["share"] >= 0.45:
        return f"{next_period}先只盯{top_categories[0]['category']}支出。"
    if related_memos:
        return f"{next_period}留意作息和消费是否继续一起波动。"
    if top_categories:
        return f"{next_period}先关注{top_categories[0]['category']}，看能不能把波动压小。"
    return None


class InsightEngine:
    def __init__(self, store: RecordStore | None = None):
        self.store = store or RecordStore()

    def get_preferences(self) -> dict[str, Any]:
        return self.store.get_insight_preferences()

    def update_preferences(self, **updates: Any) -> dict[str, Any]:
        normalized = dict(updates)
        for field in ("weekly_cron_job_id", "monthly_cron_job_id"):
            if field in normalized and normalized[field] == "":
                normalized[field] = None
        return self.store.update_insight_preferences(**normalized)

    def create_payload(self, *, period: str, schedule: str | None = None) -> dict[str, Any]:
        if period not in {"week", "month"}:
            raise ValueError("Only week and month digests can be scheduled.")
        resolved_schedule = schedule or (
            DEFAULT_WEEKLY_SCHEDULE if period == "week" else DEFAULT_MONTHLY_SCHEDULE
        )
        script_path = Path(__file__).resolve()
        title = "每周消费简报" if period == "week" else "月度消费复盘"
        prompt = (
            "This cron job was created by the private-assistant skill.\n"
            f"Run this exact command once: python {script_path} digest --period {period} --mode scheduled --view summary\n"
            'If the resulting JSON field "should_deliver" is false or the JSON field "message" equals "[SILENT]", '
            'respond with exactly "[SILENT]".\n'
            'Otherwise respond with exactly the JSON field "message" as one single Chinese message.\n'
            "Do not add headers, markdown, process notes, or extra explanation.\n"
            "Do not write digest content into memory."
        )
        return {
            "period": period,
            "schedule": resolved_schedule,
            "name": title,
            "deliver": "origin",
            "prompt": prompt,
            "skills": ["private-assistant"],
        }

    def generate_digest(
        self,
        *,
        period: str,
        mode: str = "manual",
        view: str = "summary",
    ) -> dict[str, Any]:
        window = _resolve_window(period)
        preferences = self.get_preferences()
        current_result = self.store.list_transactions(
            since=window.start.isoformat(),
            until=window.end.isoformat(),
            limit=0,
        )
        previous_result = self.store.list_transactions(
            since=window.previous_start.isoformat() if window.previous_start else None,
            until=window.previous_end.isoformat() if window.previous_end else None,
            limit=0,
        )
        current_transactions = current_result["transactions"]
        previous_transactions = previous_result["transactions"]

        current_expenses = [record for record in current_transactions if record.get("type") == "expense"]
        current_incomes = [record for record in current_transactions if record.get("type") == "income"]
        previous_expenses = [record for record in previous_transactions if record.get("type") == "expense"]

        current_expense_total = round(sum(float(record.get("amount") or 0.0) for record in current_expenses), 2)
        current_income_total = round(sum(float(record.get("amount") or 0.0) for record in current_incomes), 2)
        previous_expense_total = round(sum(float(record.get("amount") or 0.0) for record in previous_expenses), 2)
        currency = str((current_transactions[:1] or previous_transactions[:1] or [{"currency": DEFAULT_CURRENCY}])[0].get("currency") or DEFAULT_CURRENCY)

        top_categories = _top_categories(current_expenses, limit=3)
        frequency_categories = _frequency_categories(current_expenses, limit=3)
        largest_day = _largest_expense_day(current_expenses)
        anomalies, largest_change = _build_anomalies(
            _category_totals(current_expenses),
            _category_totals(previous_expenses),
        )

        memos = []
        related_memos: list[dict[str, Any]] = []
        if preferences.get("memo_context_enabled", True):
            memos = self.store.list_memos(
                since=window.start.isoformat(),
                until=window.end.isoformat(),
                limit=0,
            )["memos"]
            related_memos = _related_memos(memos, top_categories)

        quality = _quality_metrics(current_expenses)
        suggestion = _choose_suggestion(
            period=period,
            anomalies=anomalies,
            top_categories=top_categories,
            related_memos=related_memos,
            quality=quality,
        )
        should_deliver = self._should_deliver(
            period=period,
            mode=mode,
            current_transactions=current_transactions,
            anomalies=anomalies,
        )

        message = self._build_message(
            period=period,
            view=view,
            currency=currency,
            current_expense_total=current_expense_total,
            current_income_total=current_income_total,
            previous_expense_total=previous_expense_total,
            top_categories=top_categories,
            frequency_categories=frequency_categories,
            largest_day=largest_day,
            largest_change=largest_change,
            anomalies=anomalies,
            related_memos=related_memos,
            suggestion=suggestion,
            memo_count=len(memos),
            transaction_count=len(current_transactions),
        )
        if mode == "scheduled" and not should_deliver:
            message = "[SILENT]"

        return {
            "success": True,
            "period": period,
            "period_label": window.label,
            "mode": mode,
            "view": view,
            "should_deliver": should_deliver if mode == "scheduled" else True,
            "message": message,
            "metrics": {
                "currency": currency,
                "transaction_count": len(current_transactions),
                "expense_count": len(current_expenses),
                "income_count": len(current_incomes),
                "memo_count": len(memos),
                "expense_total": current_expense_total,
                "income_total": current_income_total,
                "net_total": round(current_income_total - current_expense_total, 2),
                "previous_expense_total": previous_expense_total,
                "comparison_text": _format_change_text(current_expense_total, previous_expense_total),
                "top_categories": top_categories,
                "frequency_categories": frequency_categories,
                "largest_expense_day": largest_day,
                "largest_change": largest_change,
                "quality": quality,
            },
            "signals": {
                "anomalies": anomalies,
                "related_memos": [
                    {
                        "id": memo.get("id"),
                        "kind": memo.get("kind"),
                        "created_at": memo.get("created_at"),
                        "content": memo.get("content"),
                    }
                    for memo in related_memos
                ],
                "suggestion": suggestion,
            },
        }

    def _should_deliver(
        self,
        *,
        period: str,
        mode: str,
        current_transactions: list[dict[str, Any]],
        anomalies: list[dict[str, Any]],
    ) -> bool:
        if mode != "scheduled":
            return True
        minimum = LOW_SIGNAL_MIN_TRANSACTIONS.get(period, 3)
        if len(current_transactions) >= minimum:
            return True
        return bool(anomalies)

    def _build_message(
        self,
        *,
        period: str,
        view: str,
        currency: str,
        current_expense_total: float,
        current_income_total: float,
        previous_expense_total: float,
        top_categories: list[dict[str, Any]],
        frequency_categories: list[dict[str, Any]],
        largest_day: dict[str, Any] | None,
        largest_change: dict[str, Any] | None,
        anomalies: list[dict[str, Any]],
        related_memos: list[dict[str, Any]],
        suggestion: str | None,
        memo_count: int,
        transaction_count: int,
    ) -> str:
        if transaction_count == 0:
            parts = [self._title_for(period, view), f"范围：{PERIOD_LABELS.get(period, period)}", "账单：0 笔"]
            if memo_count:
                parts.append(f"同期记录：{memo_count} 条")
            parts.append("建议：先继续随手记几笔账，再看趋势会更有价值。")
            return "｜".join(parts)

        parts = [self._title_for(period, view)]
        if view == "anomaly":
            parts.append(f"范围：{PERIOD_LABELS.get(period, period)}")
            parts.append(f"支出：{_format_money(current_expense_total, currency)}")
            parts.append(f"异常：{_format_anomaly_line(anomalies, currency)}")
            frequency_line = _format_frequency(frequency_categories[:2])
            if frequency_line:
                parts.append(f"高频：{frequency_line}")
        elif view == "combined":
            parts.append(f"范围：{PERIOD_LABELS.get(period, period)}")
            parts.append(f"支出：{_format_money(current_expense_total, currency)}")
            comparison_text = _format_change_text(current_expense_total, previous_expense_total)
            if period in {"week", "month", "7d", "30d"}:
                compare_label = "较上期" if period in {"7d", "30d"} else ("较上周" if period == "week" else "较上月")
                parts.append(f"{compare_label}：{comparison_text}")
            top_line = _format_top_categories(top_categories, currency, limit=2)
            if top_line:
                parts.append(f"Top：{top_line}")
        else:
            parts.append(f"支出：{_format_money(current_expense_total, currency)}")
            if period == "week":
                parts.append(f"较上周：{_format_change_text(current_expense_total, previous_expense_total)}")
            elif period == "month":
                parts.append(f"收入：{_format_money(current_income_total, currency)}")
                parts.append(f"净额：{_format_money(current_income_total - current_expense_total, currency)}")
            else:
                parts.append(f"较上期：{_format_change_text(current_expense_total, previous_expense_total)}")
            if period != "month" and current_income_total > 0:
                parts.append(f"收入：{_format_money(current_income_total, currency)}")
            if period != "month":
                parts.append(f"净额：{_format_money(current_income_total - current_expense_total, currency)}")
            if top_categories:
                limit = 1 if period == "week" else 3
                label = "Top1" if limit == 1 else "Top3"
                top_line = _format_top_categories(top_categories, currency, limit=limit)
                if top_line:
                    parts.append(f"{label}：{top_line}")
            if largest_day is not None:
                date_label = _format_date_label(largest_day["date"], period=period) or "近期"
                parts.append(f"高峰日：{date_label} {_format_money(largest_day['amount'], currency)}")
            if period == "month" and largest_change and largest_change["delta"] > 0:
                parts.append(f"最大变化：{largest_change['category']} {largest_change['change_text']}")

        memo_line = _format_memo_line(related_memos, period=period)
        if memo_line:
            parts.append(f"同期记录：{memo_line}")
        if suggestion:
            parts.append(f"建议：{suggestion}")
        return "｜".join(parts)

    @staticmethod
    def _title_for(period: str, view: str) -> str:
        if view == "anomaly":
            return "最近消费观察"
        if view == "combined":
            if period == "week":
                return "本周消费与备忘"
            if period == "month":
                return "本月消费与备忘"
            return "最近消费与备忘"
        if period == "week":
            return "本周消费简报"
        if period == "month":
            return "本月复盘"
        return "最近消费简报"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Private assistant insights CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    digest = sub.add_parser("digest")
    digest.add_argument("--period", choices=["week", "month", "7d", "30d"], required=True)
    digest.add_argument("--mode", choices=["manual", "scheduled"], default="manual")
    digest.add_argument("--view", choices=["summary", "combined", "anomaly"], default="summary")

    prefs_get = sub.add_parser("prefs-get")
    prefs_get.add_argument("--json", action="store_true")

    prefs_update = sub.add_parser("prefs-update")
    prefs_update.add_argument("--weekly-enabled")
    prefs_update.add_argument("--monthly-enabled")
    prefs_update.add_argument("--focus")
    prefs_update.add_argument("--memo-context-enabled")
    prefs_update.add_argument("--suggestion-style")
    prefs_update.add_argument("--low-signal-mode")
    prefs_update.add_argument("--weekly-cron-job-id")
    prefs_update.add_argument("--monthly-cron-job-id")

    create_payload = sub.add_parser("create-payload")
    create_payload.add_argument("--period", choices=["week", "month"], required=True)
    create_payload.add_argument("--schedule")

    return parser


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    engine = InsightEngine()
    try:
        if args.command == "digest":
            _print(
                engine.generate_digest(
                    period=args.period,
                    mode=args.mode,
                    view=args.view,
                )
            )

        if args.command == "prefs-get":
            _print({"success": True, "preferences": engine.get_preferences()})

        if args.command == "prefs-update":
            _print(
                {
                    "success": True,
                    "preferences": engine.update_preferences(
                        weekly_enabled=_parse_bool(args.weekly_enabled),
                        monthly_enabled=_parse_bool(args.monthly_enabled),
                        focus=args.focus,
                        memo_context_enabled=_parse_bool(args.memo_context_enabled),
                        suggestion_style=args.suggestion_style,
                        low_signal_mode=args.low_signal_mode,
                        weekly_cron_job_id=args.weekly_cron_job_id,
                        monthly_cron_job_id=args.monthly_cron_job_id,
                    ),
                }
            )

        if args.command == "create-payload":
            _print({"success": True, **engine.create_payload(period=args.period, schedule=args.schedule)})

        _print({"success": False, "error": f"Unhandled command: {args.command}"}, exit_code=1)
    except Exception as exc:
        _print({"success": False, "error": str(exc)}, exit_code=1)


if __name__ == "__main__":
    main()
