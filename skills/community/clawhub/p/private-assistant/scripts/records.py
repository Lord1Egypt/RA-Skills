#!/usr/bin/env python3
"""Local record store and CLI for the private-assistant Hermes skill."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Any, Iterable

msvcrt = None
try:
    import fcntl
except ImportError:
    fcntl = None
    try:
        import msvcrt
    except ImportError:
        pass


DEFAULT_SOURCE = "skill/private-assistant"
DEFAULT_CURRENCY = "CNY"
DEFAULT_EXPENSE_CATEGORIES = [
    "餐饮",
    "交通",
    "购物",
    "住房",
    "娱乐",
    "医疗",
    "学习",
    "人情",
    "其他",
]
DEFAULT_INCOME_CATEGORIES = [
    "工资",
    "报销",
    "副业",
    "转账",
    "理财",
    "红包",
    "其他",
]
DEFAULT_INSIGHT_PREFERENCES = {
    "weekly_enabled": False,
    "monthly_enabled": False,
    "focus": "spend_first",
    "memo_context_enabled": True,
    "suggestion_style": "single_action",
    "low_signal_mode": "silent",
    "weekly_cron_job_id": None,
    "monthly_cron_job_id": None,
}
DEFAULT_SETTINGS = {
    "default_currency": DEFAULT_CURRENCY,
    "expense_categories": DEFAULT_EXPENSE_CATEGORIES,
    "income_categories": DEFAULT_INCOME_CATEGORIES,
    "reply_style": "compact_single_message",
    "insight_preferences": DEFAULT_INSIGHT_PREFERENCES,
}
DEFAULT_INDEX = {
    "last_transaction_id": None,
    "last_memo_id": None,
    "last_query_context": {},
}
REFLECTION_KEYWORDS = {
    "感悟",
    "感受",
    "心情",
    "焦虑",
    "烦",
    "难过",
    "开心",
    "复盘",
    "反思",
    "觉得",
    "想法",
    "情绪",
    "状态",
    "压力",
    "失眠",
    "沮丧",
    "高兴",
    "幸福",
}
NOTE_KEYWORDS = {"提醒", "待办", "联系", "记一下", "别忘了", "安排", "需要"}
EXPENSE_CATEGORY_KEYWORDS = {
    "餐饮": ["饭", "午饭", "晚饭", "早餐", "咖啡", "奶茶", "外卖", "餐", "吃", "火锅"],
    "交通": ["地铁", "公交", "打车", "滴滴", "高铁", "机票", "火车", "停车", "加油"],
    "购物": ["淘宝", "京东", "拼多多", "买", "购物", "衣服", "鞋", "日用品"],
    "住房": ["房租", "租金", "水电", "物业", "燃气", "宽带"],
    "娱乐": ["电影", "游戏", "ktv", "演出", "旅游", "门票"],
    "医疗": ["医院", "药", "体检", "牙", "挂号"],
    "学习": ["课程", "书", "培训", "学费", "考试"],
    "人情": ["红包", "礼金", "随礼", "请客"],
}
INCOME_CATEGORY_KEYWORDS = {
    "工资": ["工资", "薪水", "salary", "bonus", "奖金"],
    "报销": ["报销", "reimburse"],
    "副业": ["副业", "稿费", "兼职", "consulting"],
    "转账": ["转账", "转来", "退款", "还款"],
    "理财": ["利息", "理财", "分红", "收益"],
    "红包": ["红包", "压岁钱"],
}


def _get_hermes_home() -> Path:
    try:
        from hermes_constants import get_hermes_home

        return Path(get_hermes_home())
    except Exception:
        raw = os.environ.get("HERMES_HOME")
        if raw:
            return Path(raw).expanduser()
        return Path.home() / ".hermes"


def _local_tz():
    return datetime.now().astimezone().tzinfo


def now_local() -> datetime:
    return datetime.now().astimezone()


def iso_now() -> str:
    return now_local().isoformat()


def _format_amount(value: Any) -> float:
    return round(float(value), 2)


def _parse_list_value(values: Iterable[str] | None) -> list[str]:
    result: list[str] = []
    if not values:
        return result
    for value in values:
        if value is None:
            continue
        for item in str(value).split(","):
            text = _repair_mojibake(item.strip())
            if text and text not in result:
                result.append(text)
    return result


def _repair_mojibake(value: Any) -> str:
    text = str(value)
    if not text:
        return text
    try:
        repaired = text.encode("gbk").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text
    return repaired if repaired else text


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = _repair_mojibake(str(value).strip())
    return text or None


def _load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(default)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return dict(default)
    if not isinstance(data, dict):
        return dict(default)
    merged = dict(default)
    merged.update(data)
    return merged


def _merge_default_settings(data: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(DEFAULT_SETTINGS)
    if isinstance(data, dict):
        merged.update(data)

    insight_preferences = dict(DEFAULT_INSIGHT_PREFERENCES)
    raw_preferences = merged.get("insight_preferences")
    if isinstance(raw_preferences, dict):
        insight_preferences.update(raw_preferences)
    merged["insight_preferences"] = insight_preferences
    return merged


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False))
        handle.write("\n")


def _load_jsonl(path: Path) -> tuple[list[dict[str, Any]], int]:
    if not path.exists():
        return [], 0
    records: list[dict[str, Any]] = []
    skipped = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if isinstance(item, dict):
                records.append(item)
            else:
                skipped += 1
    return records, skipped


def _rewrite_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), prefix=path.name, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False))
                handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _contains_keyword(text: str, keyword: str) -> bool:
    return keyword.lower() in text.lower()


def infer_transaction_category(kind: str, seed_text: str | None) -> str:
    text = (seed_text or "").lower()
    keyword_map = EXPENSE_CATEGORY_KEYWORDS if kind == "expense" else INCOME_CATEGORY_KEYWORDS
    for category, keywords in keyword_map.items():
        for keyword in keywords:
            if _contains_keyword(text, keyword):
                return category
    return "其他"


def infer_memo_kind(title: str | None, content: str | None) -> str:
    text = " ".join(filter(None, [title, content])).lower()
    if any(_contains_keyword(text, keyword) for keyword in REFLECTION_KEYWORDS):
        return "reflection"
    if any(_contains_keyword(text, keyword) for keyword in NOTE_KEYWORDS):
        return "note"
    return "note"


def _title_from_content(content: str) -> str:
    text = " ".join(content.split())
    if len(text) <= 24:
        return text
    return text[:24].rstrip() + "..."


def _as_datetime(value: str | None, *, boundary: str = "start") -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    date_only = len(text) == 10 and text[4] == "-" and text[7] == "-"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        dt = None
    if dt is None:
        for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%Y/%m/%d", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(text, fmt)
                break
            except ValueError:
                continue
    if dt is None:
        raise ValueError(f"Invalid datetime: {value}")
    if dt.tzinfo is None:
        if date_only:
            base_time = time.min if boundary == "start" else time(23, 59, 59)
            dt = datetime.combine(dt.date(), base_time, tzinfo=_local_tz())
        else:
            dt = dt.replace(tzinfo=_local_tz())
    return dt.astimezone()


def _resolve_range(range_name: str | None) -> tuple[datetime | None, datetime | None]:
    if not range_name:
        return None, None
    name = range_name.strip().lower()
    current = now_local()
    start = None
    end = None
    if name == "today":
        start = datetime.combine(current.date(), time.min, tzinfo=current.tzinfo)
        end = start + timedelta(days=1)
    elif name == "week":
        start = datetime.combine(current.date(), time.min, tzinfo=current.tzinfo) - timedelta(days=current.weekday())
        end = start + timedelta(days=7)
    elif name == "month":
        start = datetime(current.year, current.month, 1, tzinfo=current.tzinfo)
        if current.month == 12:
            end = datetime(current.year + 1, 1, 1, tzinfo=current.tzinfo)
        else:
            end = datetime(current.year, current.month + 1, 1, tzinfo=current.tzinfo)
    elif name.endswith("d") and name[:-1].isdigit():
        days = int(name[:-1])
        end = current + timedelta(seconds=1)
        start = end - timedelta(days=days)
    else:
        raise ValueError(f"Unsupported range: {range_name}")
    return start, end


def _dt_in_range(value: str | None, since: datetime | None, until: datetime | None) -> bool:
    if not value:
        return True
    dt = _as_datetime(value)
    if dt is None:
        return True
    if since and dt < since:
        return False
    if until and dt >= until:
        return False
    return True


def _match_keyword(candidate: dict[str, Any], keyword: str | None, fields: list[str]) -> bool:
    if not keyword:
        return True
    needle = keyword.lower()
    for field in fields:
        value = candidate.get(field)
        if value is None:
            continue
        if isinstance(value, list):
            haystack = " ".join(str(item) for item in value)
        else:
            haystack = str(value)
        if needle in haystack.lower():
            return True
    return False


@dataclass
class RecordPaths:
    root: Path
    transactions: Path
    memos: Path
    settings: Path
    index: Path
    lock: Path


class RecordStore:
    def __init__(self, root: Path | None = None):
        base = root or (_get_hermes_home() / "data" / "private-assistant")
        self.paths = RecordPaths(
            root=base,
            transactions=base / "transactions.jsonl",
            memos=base / "memos.jsonl",
            settings=base / "settings.json",
            index=base / "index.json",
            lock=base / ".store.lock",
        )
        self._ensure_initialized()

    def _ensure_initialized(self) -> None:
        self.paths.root.mkdir(parents=True, exist_ok=True)
        if not self.paths.transactions.exists():
            self.paths.transactions.touch()
        if not self.paths.memos.exists():
            self.paths.memos.touch()
        if not self.paths.settings.exists():
            _write_json(self.paths.settings, DEFAULT_SETTINGS)
        if not self.paths.index.exists():
            _write_json(self.paths.index, DEFAULT_INDEX)

    @contextmanager
    def lock(self):
        self.paths.lock.parent.mkdir(parents=True, exist_ok=True)
        if not self.paths.lock.exists():
            self.paths.lock.write_text(" ", encoding="utf-8")
        handle = open(self.paths.lock, "r+", encoding="utf-8")
        try:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            elif msvcrt is not None:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            elif msvcrt is not None:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
            handle.close()

    def settings(self) -> dict[str, Any]:
        return _merge_default_settings(_load_json(self.paths.settings, DEFAULT_SETTINGS))

    def get_insight_preferences(self) -> dict[str, Any]:
        settings = self.settings()
        preferences = settings.get("insight_preferences") or {}
        merged = dict(DEFAULT_INSIGHT_PREFERENCES)
        if isinstance(preferences, dict):
            merged.update(preferences)
        return merged

    def update_insight_preferences(self, **updates: Any) -> dict[str, Any]:
        with self.lock():
            settings = self.settings()
            preferences = self.get_insight_preferences()
            for key, value in updates.items():
                if value is not None:
                    preferences[key] = value
            settings["insight_preferences"] = preferences
            _write_json(self.paths.settings, settings)
        return preferences

    def index(self) -> dict[str, Any]:
        return _load_json(self.paths.index, DEFAULT_INDEX)

    def _save_index(self, data: dict[str, Any]) -> None:
        _write_json(self.paths.index, data)

    def _load_transactions(self) -> tuple[list[dict[str, Any]], int]:
        return _load_jsonl(self.paths.transactions)

    def _load_memos(self) -> tuple[list[dict[str, Any]], int]:
        return _load_jsonl(self.paths.memos)

    def add_transaction(
        self,
        *,
        kind: str,
        amount: float,
        category: str | None = None,
        currency: str | None = None,
        occurred_at: str | None = None,
        counterparty: str | None = None,
        note: str | None = None,
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        settings = self.settings()
        resolved_category = _normalize_text(category)
        record = {
            "id": uuid.uuid4().hex[:12],
            "type": kind,
            "amount": _format_amount(amount),
            "currency": (currency or settings["default_currency"]).upper(),
            "category": resolved_category or infer_transaction_category(kind, " ".join(filter(None, [note, counterparty]))),
            "occurred_at": (_as_datetime(occurred_at) or now_local()).isoformat(),
            "counterparty": _normalize_text(counterparty),
            "note": _normalize_text(note),
            "tags": _parse_list_value(tags),
            "source": DEFAULT_SOURCE,
            "created_at": iso_now(),
            "updated_at": iso_now(),
        }
        with self.lock():
            _append_jsonl(self.paths.transactions, record)
            index = self.index()
            index["last_transaction_id"] = record["id"]
            self._save_index(index)
        return record

    def list_transactions(
        self,
        *,
        kind: str | None = None,
        category: list[str] | None = None,
        keyword: str | None = None,
        range_name: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        records, skipped = self._load_transactions()
        range_since, range_until = _resolve_range(range_name)
        since_dt = _as_datetime(since, boundary="start") if since else range_since
        until_dt = _as_datetime(until, boundary="end") if until else range_until
        categories = set(_parse_list_value(category))
        filtered = []
        for record in records:
            if kind and record.get("type") != kind:
                continue
            if categories and record.get("category") not in categories:
                continue
            if not _dt_in_range(record.get("occurred_at"), since_dt, until_dt):
                continue
            if not _match_keyword(record, keyword, ["category", "counterparty", "note", "tags"]):
                continue
            filtered.append(record)
        filtered.sort(key=lambda item: item.get("occurred_at", ""), reverse=True)
        if limit > 0:
            filtered = filtered[:limit]
        return {
            "count": len(filtered),
            "transactions": filtered,
            "summary": self._summarize_transactions(filtered),
            "skipped_corrupt_lines": skipped,
        }

    def summarize_transactions(self, **kwargs: Any) -> dict[str, Any]:
        result = self.list_transactions(limit=0, **kwargs)
        records = result["transactions"]
        return {
            "count": len(records),
            "summary": self._summarize_transactions(records),
            "skipped_corrupt_lines": result["skipped_corrupt_lines"],
        }

    def _summarize_transactions(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        income_total = 0.0
        expense_total = 0.0
        by_category: dict[str, float] = {}
        currency = DEFAULT_CURRENCY
        for record in records:
            amount = _format_amount(record.get("amount", 0))
            currency = str(record.get("currency") or currency)
            category = str(record.get("category") or "其他")
            by_category[category] = round(by_category.get(category, 0.0) + amount, 2)
            if record.get("type") == "income":
                income_total += amount
            else:
                expense_total += amount
        return {
            "currency": currency,
            "income_total": round(income_total, 2),
            "expense_total": round(expense_total, 2),
            "net_total": round(income_total - expense_total, 2),
            "by_category": dict(sorted(by_category.items(), key=lambda item: (-item[1], item[0]))),
        }

    def _resolve_transaction_id(self, record_id: str | None = None, *, use_last: bool = False) -> str:
        if record_id:
            return record_id
        if use_last:
            last = self.index().get("last_transaction_id")
            if last:
                return str(last)
        records, _ = self._load_transactions()
        if not records:
            raise ValueError("No transaction records found.")
        records.sort(key=lambda item: item.get("occurred_at", ""), reverse=True)
        return str(records[0]["id"])

    def update_transaction(self, record_id: str | None = None, *, use_last: bool = False, **updates: Any) -> dict[str, Any]:
        target_id = self._resolve_transaction_id(record_id, use_last=use_last)
        with self.lock():
            records, _ = self._load_transactions()
            updated_record = None
            for record in records:
                if record.get("id") != target_id:
                    continue
                for field in ["type", "category", "currency", "counterparty", "note"]:
                    value = updates.get(field)
                    if value is not None:
                        record[field] = value if field in {"type", "currency"} else _normalize_text(value)
                if updates.get("amount") is not None:
                    record["amount"] = _format_amount(updates["amount"])
                if updates.get("occurred_at") is not None:
                    record["occurred_at"] = _as_datetime(updates["occurred_at"]).isoformat()
                if updates.get("tags") is not None:
                    record["tags"] = _parse_list_value(updates["tags"])
                record["updated_at"] = iso_now()
                updated_record = record
                break
            if updated_record is None:
                raise ValueError(f"Transaction not found: {target_id}")
            _rewrite_jsonl(self.paths.transactions, records)
            index = self.index()
            index["last_transaction_id"] = updated_record["id"]
            self._save_index(index)
        return updated_record

    def delete_transaction(self, record_id: str | None = None, *, use_last: bool = False) -> dict[str, Any]:
        target_id = self._resolve_transaction_id(record_id, use_last=use_last)
        with self.lock():
            records, _ = self._load_transactions()
            kept = []
            deleted = None
            for record in records:
                if record.get("id") == target_id and deleted is None:
                    deleted = record
                    continue
                kept.append(record)
            if deleted is None:
                raise ValueError(f"Transaction not found: {target_id}")
            _rewrite_jsonl(self.paths.transactions, kept)
            kept.sort(key=lambda item: item.get("occurred_at", ""), reverse=True)
            index = self.index()
            index["last_transaction_id"] = kept[0]["id"] if kept else None
            self._save_index(index)
        return deleted

    def add_memo(
        self,
        *,
        kind: str | None = None,
        title: str | None = None,
        content: str,
        tags: list[str] | None = None,
        mood: str | None = None,
        reminder_at: str | None = None,
        cron_job_id: str | None = None,
    ) -> dict[str, Any]:
        normalized_content = _repair_mojibake(content.strip())
        resolved_title = _normalize_text(title) or _title_from_content(normalized_content)
        resolved_kind = kind or infer_memo_kind(resolved_title, normalized_content)
        record = {
            "id": uuid.uuid4().hex[:12],
            "kind": resolved_kind,
            "title": resolved_title,
            "content": normalized_content,
            "tags": _parse_list_value(tags),
            "mood": _normalize_text(mood),
            "created_at": iso_now(),
            "updated_at": iso_now(),
            "reminder_at": _as_datetime(reminder_at).isoformat() if reminder_at else None,
            "cron_job_id": _normalize_text(cron_job_id),
            "source": DEFAULT_SOURCE,
        }
        with self.lock():
            _append_jsonl(self.paths.memos, record)
            index = self.index()
            index["last_memo_id"] = record["id"]
            self._save_index(index)
        return record

    def list_memos(
        self,
        *,
        kind: str | None = None,
        keyword: str | None = None,
        tags: list[str] | None = None,
        range_name: str | None = None,
        since: str | None = None,
        until: str | None = None,
        limit: int = 20,
        reminders_only: bool = False,
        upcoming_only: bool = False,
    ) -> dict[str, Any]:
        records, skipped = self._load_memos()
        range_since, range_until = _resolve_range(range_name)
        since_dt = _as_datetime(since, boundary="start") if since else range_since
        until_dt = _as_datetime(until, boundary="end") if until else range_until
        tag_set = set(_parse_list_value(tags))
        current = now_local()
        filtered = []
        for record in records:
            if kind and record.get("kind") != kind:
                continue
            if reminders_only and not record.get("reminder_at"):
                continue
            if upcoming_only:
                reminder_at = _as_datetime(record.get("reminder_at"))
                if reminder_at is None or reminder_at < current:
                    continue
            if tag_set and not tag_set.issubset(set(record.get("tags") or [])):
                continue
            if not _dt_in_range(record.get("created_at"), since_dt, until_dt):
                continue
            if not _match_keyword(record, keyword, ["title", "content", "tags", "mood"]):
                continue
            filtered.append(record)
        filtered.sort(key=lambda item: item.get("created_at", ""), reverse=True)
        if limit > 0:
            filtered = filtered[:limit]
        return {
            "count": len(filtered),
            "memos": filtered,
            "skipped_corrupt_lines": skipped,
        }

    def _resolve_memo_id(self, record_id: str | None = None, *, use_last: bool = False, reminders_only: bool = False) -> str:
        if record_id:
            return record_id
        if use_last:
            last = self.index().get("last_memo_id")
            if last:
                return str(last)
        records, _ = self._load_memos()
        if reminders_only:
            records = [record for record in records if record.get("cron_job_id")]
        if not records:
            raise ValueError("No memo records found.")
        records.sort(key=lambda item: item.get("created_at", ""), reverse=True)
        return str(records[0]["id"])

    def update_memo(self, record_id: str | None = None, *, use_last: bool = False, **updates: Any) -> dict[str, Any]:
        target_id = self._resolve_memo_id(record_id, use_last=use_last)
        with self.lock():
            records, _ = self._load_memos()
            updated_record = None
            for record in records:
                if record.get("id") != target_id:
                    continue
                for field in ["kind", "title", "content", "mood", "cron_job_id"]:
                    value = updates.get(field)
                    if value is not None:
                        if field == "kind":
                            record[field] = value
                        elif field in {"content", "cron_job_id"}:
                            record[field] = _repair_mojibake(str(value))
                        else:
                            record[field] = _normalize_text(value)
                if updates.get("tags") is not None:
                    record["tags"] = _parse_list_value(updates["tags"])
                if updates.get("reminder_at") is not None:
                    raw = updates["reminder_at"]
                    record["reminder_at"] = _as_datetime(raw).isoformat() if raw else None
                record["updated_at"] = iso_now()
                updated_record = record
                break
            if updated_record is None:
                raise ValueError(f"Memo not found: {target_id}")
            _rewrite_jsonl(self.paths.memos, records)
            index = self.index()
            index["last_memo_id"] = updated_record["id"]
            self._save_index(index)
        return updated_record

    def delete_memo(self, record_id: str | None = None, *, use_last: bool = False) -> dict[str, Any]:
        target_id = self._resolve_memo_id(record_id, use_last=use_last)
        with self.lock():
            records, _ = self._load_memos()
            kept = []
            deleted = None
            for record in records:
                if record.get("id") == target_id and deleted is None:
                    deleted = record
                    continue
                kept.append(record)
            if deleted is None:
                raise ValueError(f"Memo not found: {target_id}")
            _rewrite_jsonl(self.paths.memos, kept)
            kept.sort(key=lambda item: item.get("created_at", ""), reverse=True)
            index = self.index()
            index["last_memo_id"] = kept[0]["id"] if kept else None
            self._save_index(index)
        return deleted

    def get_memo(self, record_id: str | None = None, *, use_last: bool = False, reminders_only: bool = False) -> dict[str, Any]:
        target_id = self._resolve_memo_id(record_id, use_last=use_last, reminders_only=reminders_only)
        records, _ = self._load_memos()
        for record in records:
            if record.get("id") == target_id:
                return record
        raise ValueError(f"Memo not found: {target_id}")


def _print(payload: dict[str, Any], *, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Private assistant record CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    t_add = sub.add_parser("transaction-add")
    t_add.add_argument("--type", choices=["expense", "income"], required=True)
    t_add.add_argument("--amount", type=float, required=True)
    t_add.add_argument("--currency")
    t_add.add_argument("--category")
    t_add.add_argument("--occurred-at")
    t_add.add_argument("--counterparty")
    t_add.add_argument("--note")
    t_add.add_argument("--tag", action="append")

    t_list = sub.add_parser("transaction-list")
    t_list.add_argument("--type", choices=["expense", "income"])
    t_list.add_argument("--category", action="append")
    t_list.add_argument("--keyword")
    t_list.add_argument("--range")
    t_list.add_argument("--since")
    t_list.add_argument("--until")
    t_list.add_argument("--limit", type=int, default=20)

    t_summary = sub.add_parser("transaction-summary")
    t_summary.add_argument("--type", choices=["expense", "income"])
    t_summary.add_argument("--category", action="append")
    t_summary.add_argument("--keyword")
    t_summary.add_argument("--range")
    t_summary.add_argument("--since")
    t_summary.add_argument("--until")

    t_update = sub.add_parser("transaction-update")
    t_update.add_argument("--id")
    t_update.add_argument("--last", action="store_true")
    t_update.add_argument("--type", choices=["expense", "income"])
    t_update.add_argument("--amount", type=float)
    t_update.add_argument("--currency")
    t_update.add_argument("--category")
    t_update.add_argument("--occurred-at")
    t_update.add_argument("--counterparty")
    t_update.add_argument("--note")
    t_update.add_argument("--tag", action="append")

    t_delete = sub.add_parser("transaction-delete")
    t_delete.add_argument("--id")
    t_delete.add_argument("--last", action="store_true")

    m_add = sub.add_parser("memo-add")
    m_add.add_argument("--kind", choices=["note", "reflection"])
    m_add.add_argument("--title")
    m_add.add_argument("--content", required=True)
    m_add.add_argument("--tag", action="append")
    m_add.add_argument("--mood")
    m_add.add_argument("--reminder-at")
    m_add.add_argument("--cron-job-id")

    m_list = sub.add_parser("memo-list")
    m_list.add_argument("--kind", choices=["note", "reflection"])
    m_list.add_argument("--keyword")
    m_list.add_argument("--tag", action="append")
    m_list.add_argument("--range")
    m_list.add_argument("--since")
    m_list.add_argument("--until")
    m_list.add_argument("--limit", type=int, default=20)
    m_list.add_argument("--reminders-only", action="store_true")
    m_list.add_argument("--upcoming-only", action="store_true")

    m_update = sub.add_parser("memo-update")
    m_update.add_argument("--id")
    m_update.add_argument("--last", action="store_true")
    m_update.add_argument("--kind", choices=["note", "reflection"])
    m_update.add_argument("--title")
    m_update.add_argument("--content")
    m_update.add_argument("--tag", action="append")
    m_update.add_argument("--mood")
    m_update.add_argument("--reminder-at")
    m_update.add_argument("--cron-job-id")

    m_delete = sub.add_parser("memo-delete")
    m_delete.add_argument("--id")
    m_delete.add_argument("--last", action="store_true")

    m_get = sub.add_parser("memo-get")
    m_get.add_argument("--id")
    m_get.add_argument("--last", action="store_true")
    m_get.add_argument("--reminders-only", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> None:
    args = _build_parser().parse_args(argv)
    store = RecordStore()
    try:
        if args.command == "transaction-add":
            record = store.add_transaction(
                kind=args.type,
                amount=args.amount,
                category=args.category,
                currency=args.currency,
                occurred_at=args.occurred_at,
                counterparty=args.counterparty,
                note=args.note,
                tags=args.tag,
            )
            _print({"success": True, "record": record})

        if args.command == "transaction-list":
            result = store.list_transactions(
                kind=args.type,
                category=args.category,
                keyword=args.keyword,
                range_name=args.range,
                since=args.since,
                until=args.until,
                limit=args.limit,
            )
            _print({"success": True, **result})

        if args.command == "transaction-summary":
            result = store.summarize_transactions(
                kind=args.type,
                category=args.category,
                keyword=args.keyword,
                range_name=args.range,
                since=args.since,
                until=args.until,
            )
            _print({"success": True, **result})

        if args.command == "transaction-update":
            record = store.update_transaction(
                args.id,
                use_last=args.last,
                type=args.type,
                amount=args.amount,
                currency=args.currency,
                category=args.category,
                occurred_at=args.occurred_at,
                counterparty=args.counterparty,
                note=args.note,
                tags=args.tag,
            )
            _print({"success": True, "record": record})

        if args.command == "transaction-delete":
            record = store.delete_transaction(args.id, use_last=args.last)
            _print({"success": True, "deleted": record})

        if args.command == "memo-add":
            record = store.add_memo(
                kind=args.kind,
                title=args.title,
                content=args.content,
                tags=args.tag,
                mood=args.mood,
                reminder_at=args.reminder_at,
                cron_job_id=args.cron_job_id,
            )
            _print({"success": True, "record": record})

        if args.command == "memo-list":
            result = store.list_memos(
                kind=args.kind,
                keyword=args.keyword,
                tags=args.tag,
                range_name=args.range,
                since=args.since,
                until=args.until,
                limit=args.limit,
                reminders_only=args.reminders_only,
                upcoming_only=args.upcoming_only,
            )
            _print({"success": True, **result})

        if args.command == "memo-update":
            record = store.update_memo(
                args.id,
                use_last=args.last,
                kind=args.kind,
                title=args.title,
                content=args.content,
                tags=args.tag,
                mood=args.mood,
                reminder_at=args.reminder_at,
                cron_job_id=args.cron_job_id,
            )
            _print({"success": True, "record": record})

        if args.command == "memo-delete":
            record = store.delete_memo(args.id, use_last=args.last)
            _print({"success": True, "deleted": record})

        if args.command == "memo-get":
            record = store.get_memo(args.id, use_last=args.last, reminders_only=args.reminders_only)
            _print({"success": True, "record": record})

        _print({"success": False, "error": f"Unhandled command: {args.command}"}, exit_code=1)
    except Exception as exc:
        _print({"success": False, "error": str(exc)}, exit_code=1)


if __name__ == "__main__":
    main()
