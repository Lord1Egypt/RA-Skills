from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from html import escape
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any

try:
    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
except ImportError:  # pragma: no cover
    try:
        from backports.zoneinfo import ZoneInfo, ZoneInfoNotFoundError  # type: ignore[no-redef]
    except ImportError:  # pragma: no cover
        ZoneInfo = None  # type: ignore[assignment]
        ZoneInfoNotFoundError = None  # type: ignore[assignment]

from .jms_analytics import (
    _extract_account,
    _extract_asset,
    _extract_datetime,
    _extract_direction,
    _extract_duration,
    _extract_protocol,
    _extract_source_ip,
    _extract_status,
    _extract_user,
    _fetch_command_records,
    _fetch_file_transfer_records,
    _fetch_session_records,
    _first_field,
    _is_failed_login,
    _login_records,
    _string_value,
    license_detail_query,
    resolve_command_storage_context,
    suspicious_operation_summary,
)
from .jms_runtime import CLIError, GLOBAL_ORG_ID, list_accessible_orgs, parse_bool


SKILL_DIR = Path(__file__).resolve().parents[2]
REPORT_TEMPLATE_PATH = SKILL_DIR / "template" / "bastion-daily-usage-template.html"
REPORT_METADATA_PATH = SKILL_DIR / "references" / "metadata" / "daily_usage_report_template_fields.json"
PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z0-9_]+)\s*\}\}")
DATE_COMPACT_RE = re.compile(r"^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})$")
DATE_CN_RE = re.compile(r"^(?:(?P<year>\d{4})\s*年)?\s*(?P<month>\d{1,2})\s*月\s*(?P<day>\d{1,2})\s*[日号]$")
EMPTY_TEXT = "暂无数据"
if ZoneInfo is None:
    SHANGHAI_TZ = None
else:
    try:
        SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")
    except ZoneInfoNotFoundError:  # pragma: no cover
        SHANGHAI_TZ = None
TEXT_CONTRACT = "text"
TBODY_ROWS_CONTRACT = "tbody_rows"
REQUIRED_KEY_FIELDS = ("login_total", "login_failed", "session_total", "risk_event_total")
SESSION_ERROR_REASON_LABEL_MAP = {
    "Connect failed": "连接失败",
    "connect_failed": "连接失败",
    "Replay unsupported": "不支持回放",
    "replay_unsupported": "不支持回放",
}
CHINESE_TEXT_RE = re.compile(r"[\u4e00-\u9fff]")
COMPONENT_PREFIX_RE = re.compile(r"^\[([^\[\]]+)\]")
LOGIN_REMAINING_TRIES_RE = re.compile(r"try\s+(\d+)\s+times?", re.IGNORECASE)
LOGIN_LOCKED_REASON_TEXT = "账号已锁定，请联系管理员解锁或 5 分钟后重试"
LOGIN_INVALID_CREDENTIALS_TEXT = "用户名或密码错误"


def _local_now() -> datetime:
    if SHANGHAI_TZ is not None:
        return datetime.now(SHANGHAI_TZ)
    return datetime.now().astimezone()


def load_report_metadata() -> dict[str, Any]:
    payload = json.loads(REPORT_METADATA_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise CLIError("Report metadata must be a JSON object.")
    return payload


def load_report_template() -> str:
    return REPORT_TEMPLATE_PATH.read_text(encoding="utf-8")


def _default_report_output_path(report_date: str) -> Path:
    date_token = str(report_date or "").strip() or _local_now().date().isoformat()
    return SKILL_DIR / "reports" / ("JumpServer-%s.html" % date_token)


def extract_template_fields(template_html: str) -> list[str]:
    return sorted(set(PLACEHOLDER_RE.findall(template_html)))


def _normalize_report_org_context(org_id: str | None) -> dict[str, Any]:
    accessible_orgs = list_accessible_orgs()
    target_org_id = str(org_id or GLOBAL_ORG_ID).strip()
    selected = next((item for item in accessible_orgs if str(item.get("id") or "").strip() == target_org_id), None)
    if selected is None:
        raise CLIError(
            "Organization %s is not accessible in the current environment." % target_org_id,
            payload={
                "requested_org_id": target_org_id,
                "candidate_orgs": accessible_orgs,
            },
        )
    effective_org = dict(selected)
    effective_org["source"] = "explicit" if org_id else "report_default_global"
    switchable_orgs = [
        item
        for item in accessible_orgs
        if str(item.get("id") or "").strip() and str(item.get("id") or "").strip() != target_org_id
    ]
    return {
        "effective_org": effective_org,
        "switchable_orgs": switchable_orgs,
        "switchable_org_count": len(switchable_orgs),
        "candidate_orgs": accessible_orgs,
        "target_org_id": target_org_id,
    }


@contextmanager
def _temporary_org_context(org_id: str):
    previous = os.environ.get("JMS_ORG_ID")
    os.environ["JMS_ORG_ID"] = org_id
    try:
        yield
    finally:
        if previous is None:
            os.environ.pop("JMS_ORG_ID", None)
        else:
            os.environ["JMS_ORG_ID"] = previous


def _parse_date_expr(value: str, *, reference_date: date) -> date:
    text = str(value or "").strip()
    compact = text.replace(" ", "")
    if not compact:
        raise CLIError("Date expression is required.")
    if compact == "昨天":
        return reference_date - timedelta(days=1)
    for fmt in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(compact, fmt).date()
        except ValueError:
            continue
    match = DATE_COMPACT_RE.fullmatch(compact)
    if match:
        return date(int(match.group("year")), int(match.group("month")), int(match.group("day")))
    match = DATE_CN_RE.fullmatch(compact)
    if match:
        year = int(match.group("year") or reference_date.year)
        return date(year, int(match.group("month")), int(match.group("day")))
    raise CLIError("Unsupported date expression: %s" % value)


def _parse_datetime_expr(value: str, *, end_of_day: bool = False) -> datetime:
    text = str(value or "").strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S"):
        try:
            parsed = datetime.strptime(text, fmt)
            return parsed.replace(tzinfo=SHANGHAI_TZ) if SHANGHAI_TZ else parsed.astimezone()
        except ValueError:
            continue
    parsed_date = _parse_date_expr(text, reference_date=_local_now().date())
    hour, minute, second = (23, 59, 59) if end_of_day else (0, 0, 0)
    parsed = datetime(parsed_date.year, parsed_date.month, parsed_date.day, hour, minute, second)
    return parsed.replace(tzinfo=SHANGHAI_TZ) if SHANGHAI_TZ else parsed.astimezone()


def _normalize_time_window(
    *,
    date_expr: str | None,
    period_expr: str | None,
    date_from_expr: str | None,
    date_to_expr: str | None,
) -> dict[str, str]:
    now = _local_now()
    modes = sum(
        [
            bool(str(date_expr or "").strip()),
            bool(str(period_expr or "").strip()),
            bool(str(date_from_expr or "").strip() or str(date_to_expr or "").strip()),
        ]
    )
    if modes != 1:
        raise CLIError("Provide exactly one of --date, --period, or --date-from/--date-to.")

    if str(date_from_expr or "").strip() or str(date_to_expr or "").strip():
        if not str(date_from_expr or "").strip() or not str(date_to_expr or "").strip():
            raise CLIError("Both --date-from and --date-to are required for explicit ranges.")
        date_from = _parse_datetime_expr(str(date_from_expr), end_of_day=False)
        date_to = _parse_datetime_expr(str(date_to_expr), end_of_day=True)
    elif str(date_expr or "").strip():
        parsed_date = _parse_date_expr(str(date_expr), reference_date=now.date())
        date_from = datetime(parsed_date.year, parsed_date.month, parsed_date.day, 0, 0, 0, tzinfo=now.tzinfo)
        date_to = datetime(parsed_date.year, parsed_date.month, parsed_date.day, 23, 59, 59, tzinfo=now.tzinfo)
    else:
        period = str(period_expr or "").strip()
        if period == "上周":
            this_week_start = now.date() - timedelta(days=now.date().weekday())
            period_start = this_week_start - timedelta(days=7)
            period_end = period_start + timedelta(days=6)
        elif period == "本月":
            period_start = now.date().replace(day=1)
            period_end = now.date()
        else:
            raise CLIError("Unsupported period expression: %s" % period)
        date_from = datetime(period_start.year, period_start.month, period_start.day, 0, 0, 0, tzinfo=now.tzinfo)
        date_to = datetime(period_end.year, period_end.month, period_end.day, 23, 59, 59, tzinfo=now.tzinfo)

    if date_to < date_from:
        raise CLIError("date_to must be greater than or equal to date_from.")

    report_date = date_to.date().isoformat()
    generated_at = now.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "report_date": report_date,
        "date_from": date_from.strftime("%Y-%m-%d %H:%M:%S"),
        "date_to": date_to.strftime("%Y-%m-%d %H:%M:%S"),
        "generated_at": generated_at,
        "current_date": generated_at,
    }


def _unwrap_single_result_layers(payload: Any) -> Any:
    current = payload
    while isinstance(current, dict) and "result" in current:
        other_keys = [key for key in current if key not in {"ok", "result"}]
        if other_keys:
            break
        current = current.get("result")
    return current


def _extract_city(item: dict[str, Any]) -> str:
    return _string_value(
        _first_field(
            item,
            "city",
            "city_display",
            "location",
            "location_display",
            "geoip.city",
            "addr_city",
            "detail.city",
        )
    ).strip()


def _extract_reason(item: dict[str, Any]) -> str:
    return _string_value(
        _first_field(
            item,
            "error_reason.label",
            "error_reason.value",
            "error_reason",
            "reason",
            "detail",
            "message",
            "error",
            "type",
        )
    ).strip()


def _extract_session_error_reason(item: dict[str, Any]) -> str:
    return _string_value(_first_field(item, "error_reason.label", "error_reason.value")).strip()


def _display_session_error_reason(item: dict[str, Any]) -> str:
    label = _string_value(_first_field(item, "error_reason.label")).strip()
    value = _string_value(_first_field(item, "error_reason.value")).strip()
    if label:
        if CHINESE_TEXT_RE.search(label):
            return label
        return SESSION_ERROR_REASON_LABEL_MAP.get(label, label)
    if value:
        return SESSION_ERROR_REASON_LABEL_MAP.get(value, value)
    return ""


def _extract_bracket_component(value: Any) -> str:
    text = _string_value(value).strip()
    if not text:
        return ""
    match = COMPONENT_PREFIX_RE.match(text)
    if match:
        component = str(match.group(1) or "").strip()
        if component:
            return component
    return text


def _extract_component(item: dict[str, Any]) -> str:
    for candidate in (
        "terminal_display",
        "terminal.name",
        "terminal",
        "component",
        "component_display",
        "terminal_name",
        "terminal.type",
        "terminal_type",
    ):
        value = _first_field(item, candidate)
        if value in {None, ""}:
            continue
        component = _extract_bracket_component(value)
        if component:
            return component
    return ""


def _extract_login_failure_reason(item: dict[str, Any]) -> str:
    return _string_value(
        _first_field(
            item,
            "reason",
            "detail",
            "message",
            "error",
            "type.label",
            "type.value",
            "type",
        )
    ).strip()


def _display_login_failure_reason(item: dict[str, Any]) -> str:
    raw_reason = _extract_login_failure_reason(item)
    if not raw_reason:
        return ""
    if CHINESE_TEXT_RE.search(raw_reason):
        return raw_reason
    lowered = raw_reason.lower()
    if "account has been locked" in lowered:
        return LOGIN_LOCKED_REASON_TEXT
    if "username or password" in lowered and ("incorrect" in lowered or "wrong" in lowered):
        match = LOGIN_REMAINING_TRIES_RE.search(raw_reason)
        if match:
            return "%s，还可再尝试 %s 次" % (LOGIN_INVALID_CREDENTIALS_TEXT, match.group(1))
        return LOGIN_INVALID_CREDENTIALS_TEXT
    return raw_reason


def _display_login_failure_status(_: dict[str, Any]) -> str:
    return "失败"


def _extract_command_text(item: dict[str, Any]) -> str:
    return _string_value(
        _first_field(
            item,
            "input",
            "command",
            "command_text",
            "cmd",
            "content",
            "output",
        )
    ).strip()


def _looks_failed_session(item: dict[str, Any]) -> bool:
    if _extract_session_error_reason(item):
        return True
    return not parse_bool(item.get("is_success"), default=True)


def _session_failure_status(item: dict[str, Any]) -> str:
    if _looks_failed_session(item):
        return "失败"
    status = _extract_status(item)
    return status or EMPTY_TEXT


def _format_datetime(value: Any) -> str:
    if isinstance(value, datetime):
        dt = value.astimezone(SHANGHAI_TZ) if SHANGHAI_TZ and value.tzinfo else value
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    if value in {None, ""}:
        return EMPTY_TEXT
    text = str(value).strip()
    try:
        parsed = _extract_datetime({"date_from": text})
    except Exception:  # noqa: BLE001
        parsed = None
    if parsed is not None:
        return _format_datetime(parsed)
    return text


def _format_duration(value: Any) -> str:
    if value in {None, ""}:
        return EMPTY_TEXT
    try:
        total_seconds = max(int(float(value)), 0)
    except (TypeError, ValueError):
        return str(value)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append("%s小时" % hours)
    if minutes:
        parts.append("%s分" % minutes)
    if seconds or not parts:
        parts.append("%s秒" % seconds)
    return "".join(parts)


def _percent(value: int, total: int) -> str:
    if total <= 0:
        return "0%"
    return "%.2f%%" % ((float(value) / float(total)) * 100.0)


def _top_summary(counter: Counter[str], *, limit: int = 3) -> str:
    rows = []
    for key, count in counter.most_common(limit):
        label = str(key or "").strip() or "unknown"
        rows.append("%s(%s)" % (label, count))
    return " / ".join(rows) if rows else EMPTY_TEXT


def _top_records_summary(rows: list[dict[str, Any]], *, keys: tuple[str, ...], count_key: str = "count", limit: int = 3) -> str:
    final = []
    for item in rows[:limit]:
        name = ""
        for key in keys:
            name = str(item.get(key) or "").strip()
            if name:
                break
        final.append("%s(%s)" % (name or "unknown", item.get(count_key) or 0))
    return " / ".join(final) if final else EMPTY_TEXT


def _risk_level_label(risk_event_total: int, login_failed: int, high_risk_command_total: int, file_transfer_total: int) -> str:
    if risk_event_total >= 10 or high_risk_command_total >= 5 or login_failed >= 10:
        return "高风险"
    if risk_event_total >= 3 or high_risk_command_total > 0 or login_failed >= 3 or file_transfer_total >= 20:
        return "中风险"
    return "低风险"


def _empty_row(colspan: int, text: str = EMPTY_TEXT) -> str:
    return '<tr class="table-empty-row"><td colspan="%s">%s</td></tr>' % (colspan, escape(text))


def _row(cells: list[Any]) -> str:
    return "<tr>%s</tr>" % "".join("<td>%s</td>" % escape(str(cell or EMPTY_TEXT)) for cell in cells)


def _render_login_rows(records: list[dict[str, Any]]) -> str:
    if not records:
        return _empty_row(4)
    return "".join(
        _row(
            [
                _extract_user(item),
                _extract_city(item),
                _extract_source_ip(item),
                _extract_status(item) or ("失败" if _is_failed_login(item) else "成功"),
            ]
        )
        for item in records[:10]
    )


def _render_login_failed_rows(records: list[dict[str, Any]], *, common_ips: set[str]) -> str:
    if not records:
        return _empty_row(6)
    return "".join(
        _row(
            [
                _extract_user(item),
                _extract_city(item),
                _extract_source_ip(item),
                "是" if _extract_source_ip(item) in common_ips else "否",
                _display_login_failure_reason(item),
                _display_login_failure_status(item),
            ]
        )
        for item in records[:10]
    )


def _render_distribution_rows(counter: Counter[str], *, total: int, first_label: str, colspan: int = 3) -> str:
    if not counter:
        return _empty_row(colspan)
    rows = []
    for key, count in counter.most_common(10):
        rows.append(_row([key or first_label, count, _percent(count, total)]))
    return "".join(rows)


def _render_asset_rows(counter: Counter[str]) -> str:
    if not counter:
        return _empty_row(2)
    return "".join(_row([asset or "unknown", count]) for asset, count in counter.most_common(10))


def _render_duration_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return _empty_row(3)
    return "".join(_row([item.get("user"), item.get("asset"), _format_duration(item.get("duration_seconds"))]) for item in rows[:10])


def _render_session_failed_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return _empty_row(5)
    return "".join(
        _row(
            [
                _extract_user(item),
                _extract_asset(item),
                _extract_protocol(item),
                _display_session_error_reason(item),
                _session_failure_status(item),
            ]
        )
        for item in rows[:10]
    )


def _render_command_risk_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return _empty_row(7)
    return "".join(
        _row(
            [
                _extract_user(item),
                _extract_asset(item),
                _extract_account(item),
                _extract_command_text(item),
                _format_datetime(_extract_datetime(item)),
                _format_datetime(_first_field(item, "date_end", "date_finished", "date_to")),
                _string_value(_first_field(item, "risk_level_display", "risk_level.value", "risk_level")),
            ]
        )
        for item in rows[:10]
    )


def _normalize_direction(value: str) -> str:
    text = str(value or "").strip().lower()
    if any(token in text for token in ("upload", "up", "上传")):
        return "upload"
    if any(token in text for token in ("download", "down", "下载")):
        return "download"
    return text or "unknown"


def _get_path_value(payload: dict[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def _evaluate_output_expression(payload: dict[str, Any], expression: str) -> Any:
    match = re.fullmatch(r"\s*([a-zA-Z0-9_.]+)\s*-\s*([a-zA-Z0-9_.]+)\s*", expression)
    if not match:
        return _get_path_value(payload, expression)
    left = _get_path_value(payload, match.group(1))
    right = _get_path_value(payload, match.group(2))
    try:
        return int(left or 0) - int(right or 0)
    except (TypeError, ValueError):
        return None


def _normalize_license_source() -> dict[str, Any]:
    payload = _unwrap_single_result_layers(license_detail_query({}))
    records = payload.get("records") if isinstance(payload, dict) else None
    record = records[0] if isinstance(records, list) and records else {}
    return dict(record or {})


def _normalize_login_source(filters: dict[str, Any]) -> dict[str, Any]:
    records = list(_login_records(filters))
    records.sort(key=lambda item: _extract_datetime(item) or datetime.min.replace(tzinfo=_local_now().tzinfo), reverse=True)
    failed_records = [item for item in records if _is_failed_login(item)]
    success_records = [item for item in records if not _is_failed_login(item)]
    city_counter = Counter(city for city in (_extract_city(item) for item in records) if city)
    ip_counter = Counter(ip for ip in (_extract_source_ip(item) for item in records) if ip)
    common_ips = {ip for ip, count in ip_counter.items() if count > 1}
    if not common_ips and ip_counter:
        common_ips = {ip for ip, _ in ip_counter.most_common(3)}
    return {
        "login_total": len(records),
        "login_success": len(success_records),
        "login_failed": len(failed_records),
        "unique_login_city_count": len(city_counter),
        "top_login_ip_summary": _top_summary(ip_counter),
        "rows_html": _render_login_rows(records),
        "login_failed_rows": _render_login_failed_rows(failed_records, common_ips=common_ips),
        "records": records,
        "failed_records": failed_records,
    }


def _normalize_session_source(filters: dict[str, Any]) -> dict[str, Any]:
    records = list(_fetch_session_records(filters))
    records.sort(key=lambda item: _extract_datetime(item) or datetime.min.replace(tzinfo=_local_now().tzinfo), reverse=True)
    durations = [value for value in (_extract_duration(item) for item in records) if value is not None]
    total_duration = sum(durations) if durations else 0.0
    protocol_counter = Counter(_extract_protocol(item) or "unknown" for item in records)
    component_counter = Counter(_extract_component(item) or "unknown" for item in records)
    user_counter = Counter(_extract_user(item) or "unknown" for item in records)
    asset_counter = Counter(_extract_asset(item) or "unknown" for item in records)
    duration_rows = []
    for item in records:
        duration = _extract_duration(item)
        if duration is None:
            continue
        duration_rows.append(
            {
                "user": _extract_user(item),
                "asset": _extract_asset(item),
                "duration_seconds": duration,
                "timestamp": _extract_datetime(item),
            }
        )
    duration_rows.sort(key=lambda item: item.get("duration_seconds") or 0, reverse=True)
    failed_records = [item for item in records if _looks_failed_session(item)]
    return {
        "session_total": len(records),
        "session_total_duration": _format_duration(total_duration),
        "avg_session_duration": _format_duration((total_duration / len(durations)) if durations else None),
        "longest_session": (
            "%s / %s / %s"
            % (
                duration_rows[0].get("user") or "unknown",
                duration_rows[0].get("asset") or "unknown",
                _format_duration(duration_rows[0].get("duration_seconds")),
            )
            if duration_rows
            else EMPTY_TEXT
        ),
        "protocol_distribution_rows": _render_distribution_rows(protocol_counter, total=len(records), first_label="协议"),
        "component_distribution_rows": _render_distribution_rows(component_counter, total=len(records), first_label="组件"),
        "session_user_top10_rows": _render_distribution_rows(user_counter, total=len(records), first_label="用户"),
        "session_asset_top10_rows": _render_asset_rows(asset_counter),
        "session_duration_top10_rows": _render_duration_rows(duration_rows),
        "session_failed_rows": _render_session_failed_rows(failed_records),
        "records": records,
        "failed_records": failed_records,
    }


def _build_command_filters(filters: dict[str, Any], command_storage_id: str | None) -> dict[str, Any]:
    payload = {
        "date_from": filters["date_from"],
        "date_to": filters["date_to"],
        "limit": 50,
    }
    if command_storage_id:
        payload["command_storage_id"] = str(command_storage_id)
    else:
        payload["command_storage_scope"] = "all"
    return payload


def _normalize_command_source(filters: dict[str, Any], command_storage_id: str | None) -> dict[str, Any]:
    command_filters = _build_command_filters(filters, command_storage_id)
    records = list(_fetch_command_records(command_filters))
    risk_counter = Counter(str(_string_value(_first_field(item, "risk_level_display", "risk_level.value", "risk_level")) or "unknown") for item in records)
    user_counter = Counter(_extract_user(item) or "unknown" for item in records)
    asset_counter = Counter(_extract_asset(item) or "unknown" for item in records)
    storage_context = resolve_command_storage_context(command_filters)
    return {
        "command_total": len(records),
        "top_command_users": _top_summary(user_counter),
        "top_command_assets": _top_summary(asset_counter),
        "risk_levels": [{"name": key, "count": value} for key, value in risk_counter.most_common(10)],
        "records": records,
        **storage_context,
    }


def _normalize_high_risk_command_source(command_source: dict[str, Any]) -> dict[str, Any]:
    records = [
        item
        for item in command_source.get("records", [])
        if int(_first_field(item, "risk_level.value", "risk_level") or 0) >= 4
    ]
    return {
        "high_risk_command_total": len(records),
        "rows_html": _render_command_risk_rows(records),
        "records": records,
    }


def _normalize_file_transfer_source(filters: dict[str, Any]) -> dict[str, Any]:
    records = list(_fetch_file_transfer_records(filters))
    direction_counter = Counter(_normalize_direction(_extract_direction(item)) for item in records)
    user_counter = Counter(_extract_user(item) or "unknown" for item in records)
    asset_counter = Counter(_extract_asset(item) or "unknown" for item in records)
    return {
        "file_transfer_total": len(records),
        "file_upload_total": int(direction_counter.get("upload") or 0),
        "file_download_total": int(direction_counter.get("download") or 0),
        "file_transfer_users": _top_summary(user_counter),
        "file_transfer_assets": _top_summary(asset_counter),
        "records": records,
    }


def _normalize_suspicious_source(filters: dict[str, Any]) -> dict[str, Any]:
    payload = _unwrap_single_result_layers(suspicious_operation_summary(filters))
    summary = payload.get("summary") if isinstance(payload, dict) else {}
    return {
        "risk_event_total": int((summary or {}).get("suspicious_event_count") or 0),
        "records": payload.get("records") if isinstance(payload, dict) else [],
    }


def _source_key(source: dict[str, Any]) -> str:
    capability_id = str(source.get("capability_id") or "").strip()
    if capability_id:
        return "capability:%s" % capability_id
    entrypoint = str(source.get("entrypoint") or "").strip()
    if entrypoint == "report runtime context":
        return "runtime"
    return "entrypoint:%s" % entrypoint


def _collect_source_payloads(
    metadata: dict[str, Any],
    *,
    runtime_context: dict[str, Any],
    filters: dict[str, Any],
    command_storage_id: str | None,
) -> dict[str, dict[str, Any]]:
    cache: dict[str, dict[str, Any]] = {}

    def fetch(source_key: str) -> dict[str, Any]:
        if source_key in cache:
            return cache[source_key]
        if source_key == "runtime":
            payload = dict(runtime_context)
        elif source_key == "entrypoint:python3 scripts/jumpserver_api/jms_diagnose.py license-detail":
            payload = _normalize_license_source()
        elif source_key == "entrypoint:python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type login":
            payload = _normalize_login_source(filters)
        elif source_key == "capability:session-record-query":
            payload = _normalize_session_source(filters)
        elif source_key == "capability:session-duration-ranking":
            session_payload = fetch("capability:session-record-query")
            payload = {
                "longest_session": session_payload.get("longest_session"),
                "rows_html": session_payload.get("session_duration_top10_rows"),
            }
        elif source_key == "capability:protocol-usage-distribution":
            session_payload = fetch("capability:session-record-query")
            payload = {"rows_html": session_payload.get("protocol_distribution_rows")}
        elif source_key == "capability:recent-active-users-ranking":
            session_payload = fetch("capability:session-record-query")
            payload = {"rows_html": session_payload.get("session_user_top10_rows")}
        elif source_key == "capability:recent-active-assets-ranking":
            session_payload = fetch("capability:session-record-query")
            payload = {"rows_html": session_payload.get("session_asset_top10_rows")}
        elif source_key == "capability:command-record-query":
            payload = _normalize_command_source(filters, command_storage_id)
        elif source_key == "capability:high-risk-command-audit":
            payload = _normalize_high_risk_command_source(fetch("capability:command-record-query"))
        elif source_key == "capability:file-transfer-log-query":
            payload = _normalize_file_transfer_source(filters)
        elif source_key == "capability:file-transfer-heavy-ranking":
            file_payload = fetch("capability:file-transfer-log-query")
            payload = {
                "top_users_summary": file_payload.get("file_transfer_users"),
                "top_assets_summary": file_payload.get("file_transfer_assets"),
            }
        elif source_key == "capability:suspicious-operation-summary":
            payload = _normalize_suspicious_source(filters)
        elif source_key == "capability:failed-login-statistics":
            login_payload = fetch("entrypoint:python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type login")
            payload = {
                "login_failed": login_payload.get("login_failed"),
                "rows_html": login_payload.get("login_failed_rows"),
                "top_source_ips_summary": login_payload.get("top_login_ip_summary"),
            }
        else:
            raise CLIError("Unsupported report source: %s" % source_key)
        cache[source_key] = _unwrap_single_result_layers(payload) or {}
        return cache[source_key]

    for field_spec in metadata.get("fields") or []:
        if not isinstance(field_spec, dict):
            continue
        for source in field_spec.get("sources") or []:
            if isinstance(source, dict):
                fetch(_source_key(source))
    return cache


def _resolve_simple_field(field_spec: dict[str, Any], source_payloads: dict[str, dict[str, Any]]) -> Any:
    field_name = str(field_spec.get("field") or "")
    for source in field_spec.get("sources") or []:
        if not isinstance(source, dict):
            continue
        payload = source_payloads.get(_source_key(source), {})
        output_field = source.get("output_field")
        if output_field:
            value = _evaluate_output_expression(payload, str(output_field))
            if value not in {None, ""}:
                return value
        elif field_name and field_name in payload and payload.get(field_name) not in {None, ""}:
            return payload.get(field_name)
    return None


def _derive_fields(
    resolved: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    command_payload = source_payloads.get("capability:command-record-query", {})
    high_risk_payload = source_payloads.get("capability:high-risk-command-audit", {})
    risk_level = _risk_level_label(
        int(resolved.get("risk_event_total") or 0),
        int(resolved.get("login_failed") or 0),
        int(resolved.get("high_risk_command_total") or 0),
        int(resolved.get("file_transfer_total") or 0),
    )
    derived = {
        "daily_summary": (
            "统计时段内共发生 %s 次登录，失败 %s 次；产生 %s 个会话、%s 条命令记录、%s 次文件传输，识别到 %s 项风险/异常事件。"
            % (
                resolved.get("login_total") or 0,
                resolved.get("login_failed") or 0,
                resolved.get("session_total") or 0,
                resolved.get("command_total") or 0,
                resolved.get("file_transfer_total") or 0,
                resolved.get("risk_event_total") or 0,
            )
        ),
        "command_summary": (
            "本时段共采集 %s 条命令记录，其中高危命令 %s 条；主要操作用户为 %s，主要操作资产为 %s。"
            % (
                resolved.get("command_total") or 0,
                resolved.get("high_risk_command_total") or 0,
                resolved.get("top_command_users") or EMPTY_TEXT,
                resolved.get("top_command_assets") or EMPTY_TEXT,
            )
        ),
        "command_compliance_analysis": (
            "若高危命令占比持续升高，应优先复核高危命令明细、确认执行账号与资产范围，并结合操作目的评估是否需要收紧规范。"
            if int(resolved.get("high_risk_command_total") or 0) > 0
            else "本时段未发现高危命令集中爆发迹象，命令执行整体较为平稳。"
        ),
        "risk_level": risk_level,
        "risk_summary": (
            "综合登录失败、高危命令和文件传输情况，本时段风险等级判定为%s；风险/异常事件总数为 %s。"
            % (risk_level, resolved.get("risk_event_total") or 0)
        ),
        "risk_login_analysis": (
            "失败登录 %s 次，主要来源 IP 为 %s，覆盖来源城市 %s 个。"
            % (
                resolved.get("login_failed") or 0,
                resolved.get("top_login_ip_summary") or EMPTY_TEXT,
                resolved.get("unique_login_city_count") or 0,
            )
        ),
        "risk_command_analysis": (
            "高危命令 %s 条，主要集中在用户 %s 与资产 %s。"
            % (
                resolved.get("high_risk_command_total") or 0,
                resolved.get("top_command_users") or EMPTY_TEXT,
                resolved.get("top_command_assets") or EMPTY_TEXT,
            )
        ),
        "risk_transfer_analysis": (
            "文件传输共 %s 次，其中上传 %s 次、下载 %s 次；主要涉及用户 %s，主要涉及资产 %s。"
            % (
                resolved.get("file_transfer_total") or 0,
                resolved.get("file_upload_total") or 0,
                resolved.get("file_download_total") or 0,
                resolved.get("file_transfer_users") or EMPTY_TEXT,
                resolved.get("file_transfer_assets") or EMPTY_TEXT,
            )
        ),
        "risk_action": (
            "建议优先复核失败登录来源与高危命令明细，确认是否存在异常来源 IP、共享账号滥用或高风险批量操作；必要时结合文件传输记录做进一步取证。"
            if risk_level in {"高风险", "中风险"}
            else "建议继续保持现有审计频率，关注失败登录与高危命令的波动趋势。"
        ),
        "file_transfer_summary": (
            "本时段文件传输共 %s 次，其中上传 %s 次、下载 %s 次；主要传输用户为 %s，主要传输资产为 %s。"
            % (
                resolved.get("file_transfer_total") or 0,
                resolved.get("file_upload_total") or 0,
                resolved.get("file_download_total") or 0,
                resolved.get("file_transfer_users") or EMPTY_TEXT,
                resolved.get("file_transfer_assets") or EMPTY_TEXT,
            )
        ),
    }
    return derived


def _resolve_field_value(
    field_spec: dict[str, Any],
    *,
    resolved_values: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
    derived_values: dict[str, Any],
) -> Any:
    field_name = str(field_spec.get("field") or "").strip()
    raw_value = resolved_values.get(field_name)
    if raw_value not in {None, ""}:
        return raw_value
    raw_value = _resolve_simple_field(field_spec, source_payloads)
    if raw_value not in {None, ""}:
        return raw_value
    return derived_values.get(field_name)


def _render_field_value(field_spec: dict[str, Any], value: Any) -> str:
    contract = str(field_spec.get("render_contract") or TEXT_CONTRACT)
    if contract == TBODY_ROWS_CONTRACT:
        if value not in {None, ""}:
            return str(value)
        columns = field_spec.get("table_columns")
        colspan = len(columns) if isinstance(columns, list) and columns else 1
        return _empty_row(colspan)
    if value in {None, ""}:
        return EMPTY_TEXT
    if isinstance(value, (int, float)):
        return str(value)
    return escape(str(value))


def render_report_html(template_html: str, field_values: dict[str, str]) -> str:
    rendered = template_html
    for key, value in field_values.items():
        rendered = re.sub(r"\{\{\s*%s\s*\}\}" % re.escape(key), lambda _: value, rendered)
    return rendered


def _build_minimal_context(
    *,
    date_expr: str | None,
    period_expr: str | None,
    date_from_expr: str | None,
    date_to_expr: str | None,
    org_id: str | None,
    command_storage_id: str | None,
) -> dict[str, Any]:
    runtime_context = _normalize_time_window(
        date_expr=date_expr,
        period_expr=period_expr,
        date_from_expr=date_from_expr,
        date_to_expr=date_to_expr,
    )
    org_context = _normalize_report_org_context(org_id)
    filters = {
        "date_from": runtime_context["date_from"],
        "date_to": runtime_context["date_to"],
    }
    if command_storage_id:
        filters["command_storage_id"] = str(command_storage_id)
    return {
        "runtime_context": runtime_context,
        "org_context": org_context,
        "filters": filters,
        "command_storage_id": str(command_storage_id or "").strip() or None,
    }


def validate_report_contract(
    *,
    metadata: dict[str, Any] | None = None,
    template_html: str | None = None,
    sample_values: dict[str, str] | None = None,
) -> dict[str, Any]:
    metadata_payload = metadata or load_report_metadata()
    template_payload = template_html or load_report_template()
    template_fields = extract_template_fields(template_payload)
    metadata_fields = [
        item.get("field")
        for item in metadata_payload.get("fields", [])
        if isinstance(item, dict) and item.get("field")
    ]
    required_fields = [
        item.get("field")
        for item in metadata_payload.get("fields", [])
        if isinstance(item, dict) and item.get("required") and item.get("field")
    ]
    dummy_values = dict(sample_values or {})
    for item in metadata_payload.get("fields", []):
        if not isinstance(item, dict):
            continue
        field_name = str(item.get("field") or "").strip()
        if not field_name or field_name in dummy_values:
            continue
        if item.get("render_contract") == TBODY_ROWS_CONTRACT:
            dummy_values[field_name] = "<tr><td>contract-ok</td></tr>"
        elif item.get("value_type") == "number_string":
            dummy_values[field_name] = "1"
        elif item.get("value_type") == "datetime_string":
            dummy_values[field_name] = "2026-03-10 12:00:00"
        else:
            dummy_values[field_name] = "sample_%s" % field_name
    rendered = render_report_html(template_payload, dummy_values)
    placeholder_residue = sorted(set(PLACEHOLDER_RE.findall(rendered)))
    required_unbound = sorted([field for field in required_fields if field not in dummy_values or dummy_values[field] in {"", None}])
    return {
        "template_field_count": len(template_fields),
        "metadata_field_count": len(metadata_fields),
        "missing_in_metadata": sorted(set(template_fields) - set(metadata_fields)),
        "missing_in_template": sorted(set(metadata_fields) - set(template_fields)),
        "required_unbound_fields": required_unbound,
        "placeholder_residue": placeholder_residue,
        "contract_passed": not (
            set(template_fields) - set(metadata_fields)
            or set(metadata_fields) - set(template_fields)
            or required_unbound
            or placeholder_residue
        ),
    }


def _validate_report_output(
    *,
    rendered_html: str,
    field_values: dict[str, str],
    metadata: dict[str, Any],
    source_payloads: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []
    placeholder_residue = sorted(set(PLACEHOLDER_RE.findall(rendered_html)))
    if placeholder_residue:
        failures.append("Rendered HTML still contains placeholders: %s" % ", ".join(placeholder_residue))

    required_fields = [
        item.get("field")
        for item in metadata.get("fields", [])
        if isinstance(item, dict) and item.get("required") and item.get("field")
    ]
    missing_required = [field for field in required_fields if field_values.get(str(field), "") in {"", None}]
    if missing_required:
        failures.append("Required fields are empty: %s" % ", ".join(sorted(missing_required)))

    for key in REQUIRED_KEY_FIELDS:
        value = str(field_values.get(key) or "").strip()
        if not value:
            failures.append("Key field %s is empty." % key)

    login_payload = source_payloads.get("entrypoint:python3 scripts/jumpserver_api/jms_query.py audit-list --audit-type login", {})
    session_payload = source_payloads.get("capability:session-record-query", {})
    risk_payload = source_payloads.get("capability:suspicious-operation-summary", {})
    for field_name, source_total in (
        ("login_total", int(login_payload.get("login_total") or 0)),
        ("session_total", int(session_payload.get("session_total") or 0)),
        ("risk_event_total", int(risk_payload.get("risk_event_total") or 0)),
    ):
        rendered_value = str(field_values.get(field_name) or "").strip()
        if source_total > 0 and rendered_value in {"0", EMPTY_TEXT, ""}:
            failures.append("Field %s lost non-empty source data during rendering." % field_name)

    if rendered_html.count(EMPTY_TEXT) > 12:
        warnings.append("Rendered report still contains many '%s' markers." % EMPTY_TEXT)

    return {
        "passed": not failures,
        "failure_count": len(failures),
        "warning_count": len(warnings),
        "validation_failures": failures,
        "validation_warnings": warnings,
    }


def build_daily_usage_report(
    *,
    output_path: str | None = None,
    date_expr: str | None = None,
    period_expr: str | None = None,
    date_from_expr: str | None = None,
    date_to_expr: str | None = None,
    org_id: str | None = None,
    command_storage_id: str | None = None,
) -> dict[str, Any]:
    context = _build_minimal_context(
        date_expr=date_expr,
        period_expr=period_expr,
        date_from_expr=date_from_expr,
        date_to_expr=date_to_expr,
        org_id=org_id,
        command_storage_id=command_storage_id,
    )
    metadata = load_report_metadata()
    template_html = load_report_template()
    contract = validate_report_contract(metadata=metadata, template_html=template_html)
    if not contract.get("contract_passed"):
        raise CLIError(
            "Report contract validation failed before generation.",
            payload=contract,
        )

    with _temporary_org_context(context["org_context"]["target_org_id"]):
        source_payloads = _collect_source_payloads(
            metadata,
            runtime_context=context["runtime_context"],
            filters=context["filters"],
            command_storage_id=context["command_storage_id"],
        )

    resolved_values: dict[str, Any] = {}
    for item in metadata.get("fields", []):
        if not isinstance(item, dict):
            continue
        field_name = str(item.get("field") or "").strip()
        if not field_name or item.get("source_kind") == "derived":
            continue
        resolved_values[field_name] = _resolve_simple_field(item, source_payloads)

    derived_values = _derive_fields(resolved_values, source_payloads)
    rendered_fields: dict[str, str] = {}
    for item in metadata.get("fields", []):
        if not isinstance(item, dict):
            continue
        field_name = str(item.get("field") or "").strip()
        if not field_name:
            continue
        raw_value = _resolve_field_value(
            item,
            resolved_values=resolved_values,
            source_payloads=source_payloads,
            derived_values=derived_values,
        )
        rendered_fields[field_name] = _render_field_value(item, raw_value)

    rendered_html = render_report_html(template_html, rendered_fields)
    validation = _validate_report_output(
        rendered_html=rendered_html,
        field_values=rendered_fields,
        metadata=metadata,
        source_payloads=source_payloads,
    )
    if not validation.get("passed"):
        raise CLIError(
            "Report generation failed validation. 生成失败，需要修复模板填充逻辑。",
            payload=validation,
        )

    output = _default_report_output_path(context["runtime_context"]["report_date"])
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=str(output.parent), suffix=".html") as handle:
        handle.write(rendered_html)
        temp_name = handle.name
    os.replace(temp_name, output)

    command_source = source_payloads.get("capability:command-record-query", {})
    return {
        "output_path": str(output),
        "template_path": str(REPORT_TEMPLATE_PATH.relative_to(SKILL_DIR)),
        "metadata_path": str(REPORT_METADATA_PATH.relative_to(SKILL_DIR)),
        "effective_org": context["org_context"]["effective_org"],
        "switchable_orgs": context["org_context"]["switchable_orgs"],
        "queried_command_storage_ids": command_source.get("queried_command_storage_ids") or [],
        "queried_command_storage_count": int(command_source.get("queried_command_storage_count") or 0),
        "report_date": context["runtime_context"]["report_date"],
        "date_from": context["runtime_context"]["date_from"],
        "date_to": context["runtime_context"]["date_to"],
        "validation_summary": validation,
    }
