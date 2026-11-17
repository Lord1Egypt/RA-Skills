"""ocal_recurrence — 结构化定期规则校验、格式化、出现次数估算与参数构造。"""
import json
from datetime import datetime, timedelta

from ocal_errors import CalError
from ocal_i18n import t, get_lang, idx_name, weekday_names
from ocal_time import LOCAL_TZ_NAME, _parse_dt_arg

# 注意：Python weekday() 0=周一 ... 6=周日，这两个数组必须从周一对齐
EN_DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
WEEK_INDEX = ("first", "second", "third", "fourth", "last")
_INT32_MAX = 2_147_483_647
_PATTERN_FIELDS = {
    "daily": {"type", "interval"},
    "weekly": {"type", "interval", "daysOfWeek", "firstDayOfWeek"},
    "absoluteMonthly": {"type", "interval", "dayOfMonth"},
    "relativeMonthly": {"type", "interval", "daysOfWeek", "index"},
    "absoluteYearly": {"type", "interval", "month", "dayOfMonth"},
    "relativeYearly": {"type", "interval", "month", "daysOfWeek", "index"},
}


def _pattern_error(detail):
    raise CalError(t("err_repeat_field", detail=detail))


def _unique_object(pairs):
    """JSON duplicate keys are errors, never silently last-value-wins."""
    result = {}
    for key, value in pairs:
        if key in result:
            _pattern_error(f"duplicate field: {key}")
        result[key] = value
    return result


def _pattern_int(pattern, name, minimum, maximum):
    value = pattern[name]
    if type(value) is not int or not minimum <= value <= maximum:
        _pattern_error(f"{name} must be an integer from {minimum} to {maximum}")


def _parse_recurrence(raw, start_date):
    """Validate an explicit Graph recurrencePattern JSON object.

    All fields applicable to the selected type are mandatory, including weekly
    firstDayOfWeek and relative index. No language interpretation or inferred
    weekdays/default interval happens here. Invalid input raises CalError.
    """
    if not isinstance(raw, str):
        raise CalError(t("err_repeat_json"))
    try:
        pattern = json.loads(raw, object_pairs_hook=_unique_object)
    except (ValueError, RecursionError):
        raise CalError(t("err_repeat_json")) from None
    if not isinstance(pattern, dict):
        raise CalError(t("err_repeat_json"))
    kind = pattern.get("type")
    if not isinstance(kind, str) or kind not in _PATTERN_FIELDS:
        _pattern_error("type must be one of: " + ", ".join(_PATTERN_FIELDS))
    fields = _PATTERN_FIELDS[kind]
    missing = fields - pattern.keys()
    if missing:
        _pattern_error(f"{kind} requires: " + ", ".join(sorted(missing)))
    extra = pattern.keys() - fields
    if extra:
        _pattern_error(f"{kind} does not accept: " + ", ".join(sorted(extra)))
    _pattern_int(pattern, "interval", 1, _INT32_MAX)
    if "dayOfMonth" in fields:
        _pattern_int(pattern, "dayOfMonth", 1, 31)
    if "month" in fields:
        _pattern_int(pattern, "month", 1, 12)
    if kind == "absoluteYearly":
        try:
            # A leap year admits February 29 but rejects dates that never exist.
            datetime(2000, pattern["month"], pattern["dayOfMonth"])
        except ValueError:
            _pattern_error("month/dayOfMonth must be a valid calendar date")
    if "daysOfWeek" in fields:
        days = pattern["daysOfWeek"]
        if (not isinstance(days, list) or not days
                or any(not isinstance(day, str) or day not in EN_DAYS for day in days)):
            _pattern_error("daysOfWeek must be a nonempty array containing only: " + ", ".join(EN_DAYS))
        if len(days) != len(set(days)):
            _pattern_error("daysOfWeek must not contain duplicates")
    if "firstDayOfWeek" in fields and pattern["firstDayOfWeek"] not in EN_DAYS:
        _pattern_error("firstDayOfWeek must be one of: " + ", ".join(EN_DAYS))
    if "index" in fields and pattern["index"] not in WEEK_INDEX:
        _pattern_error("index must be one of: " + ", ".join(WEEK_INDEX))
    start_date = start_date.date() if isinstance(start_date, datetime) else start_date
    recurrence = {
        "pattern": pattern,
        "range": {"type": "noEnd", "startDate": start_date.isoformat()},
    }
    return recurrence, _fmt_recurrence(recurrence)


def _fmt_recurrence(rec):
    """把 recurrence 对象翻译成人话（read/list 里显示用）。

    :param rec: Graph 的 recurrence 对象
    :return: 人类可读描述；空对象返回空串
    """
    if not rec:
        return ""
    p = rec.get("pattern", {})
    r = rec.get("range", {})
    ttype = p.get("type", "")
    interval = p.get("interval", 1)
    names = weekday_names()
    if ttype == "daily":
        desc = t("rec_daily") if interval == 1 else t("rec_every_n_days", n=interval)
    elif ttype == "weekly":
        days = [names[i] for i, d in enumerate(EN_DAYS) if d in p.get("daysOfWeek", [])]
        if p.get("daysOfWeek") and set(p["daysOfWeek"]) == {"monday", "tuesday", "wednesday", "thursday", "friday"}:
            # 周一至周五 = 每个工作日
            desc = t("rec_weekdays") if interval == 1 else t("rec_week_n_weekdays", n=interval)
        else:
            head = t("rec_weekly") if interval == 1 else t("rec_every_n_weeks", n=interval)
            desc = head + t("rec_day_join").join(days)
    elif ttype == "absoluteMonthly":
        key = "rec_monthly_day" if interval == 1 else "rec_every_n_months_day"
        desc = t(key, n=interval, day=p.get('dayOfMonth', '?'))
    elif ttype in ("relativeMonthly", "relativeYearly"):
        idx = idx_name(p.get("index", ""))
        days = [names[i] for i, d in enumerate(EN_DAYS) if d in p.get("daysOfWeek", [])]
        if ttype == "relativeMonthly":
            key = "rec_monthly_idx" if interval == 1 else "rec_every_n_months_idx"
        else:
            key = "rec_yearly_idx" if interval == 1 else "rec_every_n_years_idx"
        desc = t(key, n=interval, idx=idx, day=t("rec_day_join").join(days) if days else '?',
                 m=p.get("month", "?"))
        if get_lang() == "zh":
            desc = desc.replace("最后个", "最后一个")
        if len(days) > 1:
            desc += t("rec_first_matching")
    elif ttype == "absoluteYearly":
        key = "rec_yearly" if interval == 1 else "rec_every_n_years"
        desc = t(key, n=interval, m=p.get('month', '?'), d=p.get('dayOfMonth', '?'))
    else:
        desc = ttype
    rtype = r.get("type", "")
    if rtype == "numbered":
        desc += t("rec_count", n=r.get('numberOfOccurrences', '?'))
    elif rtype == "endDate":
        desc += t("rec_until", d=r.get('endDate', '?'))
    return desc


def _occurrence_number(rec, occ_dt):
    """数一下 occ 在系列里是第几次出现；算不出来返回 None。

    只计算逐日和每周规则。多周/月/年规则交给 Graph 展开，避免本地
    估算忽略周起点、缺失日期等细节而显示错误序号。

    :param rec: recurrence 对象
    :param occ_dt: 某个出现的 start.dateTime
    :return: 第 N 次（从 1 起）；无法计算返回 None
    """
    if not rec or not occ_dt:
        return None
    try:
        p = rec.get('pattern', {})
        r = rec.get('range', {})
        start = datetime.strptime(r.get('startDate', '')[:10], "%Y-%m-%d").date()
        occ = datetime.strptime(occ_dt[:10], "%Y-%m-%d").date()
    except Exception:
        return None
    ttype = p.get('type', '')
    interval = p.get('interval', 1)
    if type(interval) is not int or interval < 1 or occ < start:
        return None
    if ttype == 'daily':
        elapsed = (occ - start).days
        return elapsed // interval + 1 if elapsed % interval == 0 else None
    if ttype == 'weekly' and interval == 1:
        days = p.get('daysOfWeek', [])
        if not isinstance(days, list) or not days or any(day not in EN_DAYS for day in days):
            return None
        n = 1
        d = start
        while d <= occ:
            if (d - start).days > 3650:
                return None
            if EN_DAYS[d.weekday()] in days:
                if d == occ:
                    return n
                n += 1
            d += timedelta(days=1)
        return None
    return None

def _build_recurrence(repeat, repeat_until, repeat_times, start_dt):
    """按明确参数拼定期规则（JSON pattern + 结束条件），add/update 共用。

    :param repeat: Graph recurrencePattern 的 JSON 字符串
    :param repeat_until: 结束日期（YYYY-MM-DD），可空
    :param repeat_times: 总次数，可空
    :param start_dt: 开始时间（用来定 range.startDate）
    :return: (recurrence dict, 人类可读描述)
    :raises CalError: 结构或字段非法 / 结束条件非法或冲突
    """
    recurrence, _ = _parse_recurrence(repeat, start_dt)
    start_date = start_dt.date() if isinstance(start_dt, datetime) else start_dt
    # Graph 对定期事件若不显式指定 recurrenceTimeZone 会默认按 UTC 锚定循环，
    # 结果 originalStartTimeZone=UTC 而 originalEndTimeZone=本地时区，Outlook
    # 显示"开始是 UTC、结束是本地时间"。这里与 start/end 的 timeZone 保持一致
    recurrence["range"]["recurrenceTimeZone"] = LOCAL_TZ_NAME
    if repeat_until is not None and repeat_times is not None:
        raise CalError(t("err_repeat_end_conflict"))
    if repeat_until is not None:
        try:
            until = _parse_dt_arg(repeat_until, date_only=True)
        except CalError:
            raise CalError(t("err_repeat_until_fmt", d=repeat_until)) from None
        if until.date() < start_date:
            raise CalError(t("err_repeat_until_before", u=repeat_until, s=start_date))
        recurrence["range"]["type"] = "endDate"
        recurrence["range"]["endDate"] = until.date().isoformat()
    elif repeat_times is not None:
        if type(repeat_times) is not int or not 1 <= repeat_times <= _INT32_MAX:
            raise CalError(t("err_repeat_count"))
        recurrence["range"]["type"] = "numbered"
        recurrence["range"]["numberOfOccurrences"] = repeat_times
    return recurrence, _fmt_recurrence(recurrence)
