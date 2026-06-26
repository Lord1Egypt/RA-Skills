from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Iterable, List, Sequence

AIRPORT_NAMES = {
    "GMP": "김포",
    "CJU": "제주",
    "PUS": "부산",
    "TAE": "대구",
    "CJJ": "청주",
    "KWJ": "광주",
    "RSU": "여수",
    "USN": "울산",
    "HIN": "사천",
    "KPO": "포항경주",
    "YNY": "양양",
    "MWX": "무안",
    "SEL": "서울",
}

AIRPORT_ALIASES = {
    "김포": "GMP",
    "제주": "CJU",
    "제주도": "CJU",
    "부산": "PUS",
    "김해": "PUS",
    "대구": "TAE",
    "청주": "CJJ",
    "광주": "KWJ",
    "여수": "RSU",
    "울산": "USN",
    "사천": "HIN",
    "진주": "HIN",
    "포항": "KPO",
    "포항경주": "KPO",
    "양양": "YNY",
    "무안": "MWX",
    "서울": "SEL",
    "gimpo": "GMP",
    "jeju": "CJU",
    "busan": "PUS",
    "daegu": "TAE",
    "cheongju": "CJJ",
    "gwangju": "KWJ",
    "yeosu": "RSU",
    "ulsan": "USN",
    "sacheon": "HIN",
    "pohang": "KPO",
    "yangyang": "YNY",
    "muan": "MWX",
    "seoul": "SEL",
}

WEEKDAY_ALIASES = {
    "월": 0,
    "월요일": 0,
    "화": 1,
    "화요일": 1,
    "수": 2,
    "수요일": 2,
    "목": 3,
    "목요일": 3,
    "금": 4,
    "금요일": 4,
    "토": 5,
    "토요일": 5,
    "일": 6,
    "일요일": 6,
}

TIME_BUCKETS = {
    "새벽": (0, 5),
    "아침": (6, 10),
    "오전": (6, 11),
    "점심": (11, 13),
    "오후": (12, 17),
    "저녁": (18, 21),
    "밤": (20, 23),
    "야간": (20, 23),
    "늦은": (18, 23),
}


def airport_label(code: str) -> str:
    code = (code or "").upper()
    return f"{AIRPORT_NAMES.get(code, code)}({code})" if code else ""


def normalize_airport(value: str) -> str:
    if not value:
        raise ValueError("공항 값이 비어 있습니다.")
    raw = value.strip()
    upper = raw.upper()
    if upper in AIRPORT_NAMES:
        return upper
    lowered = raw.lower()
    if lowered in AIRPORT_ALIASES:
        return AIRPORT_ALIASES[lowered]
    if raw in AIRPORT_ALIASES:
        return AIRPORT_ALIASES[raw]
    raise ValueError(f"지원하지 않는 공항 입력입니다: {value}")


def _base_today() -> datetime:
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def _parse_month_day(raw: str, today: datetime) -> datetime | None:
    match = re.fullmatch(r"(\d{1,2})[./\-월\s]+(\d{1,2})(?:일)?", raw)
    if not match:
        return None
    month = int(match.group(1))
    day = int(match.group(2))
    year = today.year
    candidate = datetime(year, month, day)
    if candidate < today:
        candidate = datetime(year + 1, month, day)
    return candidate


def _parse_relative_days(raw: str, today: datetime) -> datetime | None:
    match = re.fullmatch(r"(\d+)\s*(?:일 뒤|일후|days? later)", raw)
    if match:
        return today + timedelta(days=int(match.group(1)))
    match = re.fullmatch(r"(\d+)\s*(?:주 뒤|주후)", raw)
    if match:
        return today + timedelta(days=7 * int(match.group(1)))
    return None


def _next_weekday(today: datetime, weekday: int, week_offset: int = 0) -> datetime:
    days_ahead = (weekday - today.weekday()) % 7
    candidate = today + timedelta(days=days_ahead + week_offset * 7)
    if week_offset == 0 and candidate < today:
        candidate += timedelta(days=7)
    return candidate


def _parse_weekday(raw: str, today: datetime) -> datetime | None:
    raw = raw.strip()
    for prefix, offset in (("이번주 ", 0), ("이번 주 ", 0), ("다음주 ", 1), ("다음 주 ", 1), ("오는 ", 0)):
        if raw.startswith(prefix):
            tail = raw[len(prefix):].strip()
            if tail in WEEKDAY_ALIASES:
                return _next_weekday(today, WEEKDAY_ALIASES[tail], offset)
    if raw in WEEKDAY_ALIASES:
        return _next_weekday(today, WEEKDAY_ALIASES[raw], 0)
    if raw in ("주말", "이번주말", "이번 주말"):
        return _next_weekday(today, 5, 0)
    if raw in ("다음주말", "다음 주말"):
        return _next_weekday(today, 5, 1)
    return None


def parse_flexible_date(value: str) -> datetime:
    raw = value.strip().lower()
    today = _base_today()
    mapping = {
        "today": 0,
        "오늘": 0,
        "tomorrow": 1,
        "내일": 1,
        "day after tomorrow": 2,
        "모레": 2,
        "글피": 3,
    }
    if raw in mapping:
        return today + timedelta(days=mapping[raw])
    relative = _parse_relative_days(raw, today)
    if relative:
        return relative
    weekday = _parse_weekday(raw, today)
    if weekday:
        return weekday
    month_day = _parse_month_day(raw.replace("  ", " "), today)
    if month_day:
        return month_day
    for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y.%m.%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(f"지원하지 않는 날짜 형식입니다: {value}")


def parse_date_range_text(value: str) -> tuple[datetime, datetime]:
    raw = value.strip().lower()
    today = _base_today()
    m = re.fullmatch(r"(.+?)부터\s*(\d+)일", raw)
    if m:
        start = parse_flexible_date(m.group(1))
        days = int(m.group(2))
        return start, start + timedelta(days=max(days - 1, 0))
    if raw in ("이번주말", "이번 주말", "주말"):
        start = _next_weekday(today, 5, 0)
        return start, start + timedelta(days=1)
    if raw in ("다음주말", "다음 주말"):
        start = _next_weekday(today, 5, 1)
        return start, start + timedelta(days=1)

    explicit_patterns = [
        r"^\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*~\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*$",
        r"^\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*to\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*$",
        r"^\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*부터\s*(\d{4}[-./]\d{1,2}[-./]\d{1,2}|\d{8})\s*(?:까지)?\s*$",
    ]
    for pattern in explicit_patterns:
        match = re.fullmatch(pattern, value, re.IGNORECASE)
        if match:
            start = parse_flexible_date(match.group(1).strip())
            end = parse_flexible_date(match.group(2).strip())
            return start, end

    parts = re.split(r"\s*(?:~|부터|to)\s*", value, maxsplit=1)
    if len(parts) == 2 and all(part.strip() for part in parts):
        start = parse_flexible_date(parts[0].strip())
        end = parse_flexible_date(parts[1].strip())
        return start, end
    single = parse_flexible_date(value)
    return single, single


def pretty_date(value: datetime) -> str:
    return value.strftime("%Y-%m-%d")


def compact_date(value: datetime) -> str:
    return value.strftime("%Y%m%d")


def cabin_label(code: str) -> str:
    return {
        "ECONOMY": "이코노미",
        "BUSINESS": "비즈니스",
        "FIRST": "일등석",
    }.get((code or "").upper(), code or "")


def format_price(value: int | float | None) -> str:
    return f"{int(value or 0):,}원"


def format_time_or_fallback(value: str | None, fallback: str = "시간 정보 없음") -> str:
    text = str(value or "").strip()
    return text or fallback


def join_nonempty(parts: Sequence[str | None], sep: str = " · ") -> str:
    return sep.join([str(part) for part in parts if part])


def add_section(lines: list[str], title: str, body: Sequence[str | None]) -> None:
    items = [str(item) for item in body if item]
    if not items:
        return
    if lines:
        lines.append("")
    lines.append(f"[{title}]")
    lines.extend(items)


def summarize_price_gap(best_price: int, next_price: int | None) -> str | None:
    if not best_price or not next_price or next_price <= best_price:
        return None
    gap = next_price - best_price
    ratio = round((gap / best_price) * 100)
    return f"2위보다 {gap:,}원 저렴해 가성비가 좋습니다{f' (약 {ratio}% 차이)' if ratio >= 5 else ''}."


def recommendation_line(subject: str, best_price: int, next_price: int | None = None) -> str:
    gap_text = summarize_price_gap(best_price, next_price)
    if gap_text:
        return f"추천: 이번 조건에서는 {subject}이(가) 가장 유리합니다. {gap_text}"
    return f"추천: 이번 조건에서는 {subject}이(가) 가장 무난한 최저가 선택입니다."


def explain_recommendation(subject: str, best_price: int, next_price: int | None = None, reasons: Sequence[str] | None = None) -> str:
    parts: list[str] = [f"추천 사유: {subject} 기준"]
    if best_price > 0:
        parts.append(f"최저가 {format_price(best_price)}")
    gap_text = summarize_price_gap(best_price, next_price)
    if gap_text:
        parts.append(gap_text)
    if reasons:
        parts.extend([reason for reason in reasons if reason])
    return " · ".join(parts) + "."


def bullet_rank_lines(items: Sequence[dict], label_key: str, price_key: str, detail_builder=None, limit: int = 5) -> List[str]:
    lines: List[str] = []
    for idx, item in enumerate(items[:limit], start=1):
        label = item.get(label_key, "옵션")
        price = item.get(price_key, 0)
        if price and price > 0:
            detail = detail_builder(item) if detail_builder else ""
            suffix = f" · {detail}" if detail else ""
            lines.append(f"{idx}. {label} · {format_price(price)}{suffix}")
        else:
            lines.append(f"{idx}. {label} · 결과 없음")
    return lines


def build_price_calendar(rows: Sequence[dict], date_key: str = "departure_date", price_key: str = "price") -> list[dict]:
    available_prices = [int(item.get(price_key, 0) or 0) for item in rows if int(item.get(price_key, 0) or 0) > 0]
    if not rows:
        return []

    cheapest = min(available_prices) if available_prices else 0
    median = sorted(available_prices)[len(available_prices) // 2] if available_prices else 0

    calendar = []
    for item in rows:
        price = int(item.get(price_key, 0) or 0)
        if price <= 0:
            band = "unavailable"
            badge = "⚪"
            note = "결과 없음"
        elif cheapest and price == cheapest:
            band = "best"
            badge = "🟢"
            note = "최저가"
        elif median and price <= median:
            band = "good"
            badge = "🟡"
            note = "양호"
        else:
            band = "high"
            badge = "🔴"
            note = "상대적으로 높음"
        calendar.append({
            "date": item.get(date_key),
            "price": price,
            "band": band,
            "badge": badge,
            "label": f"{item.get(date_key)} {badge} {format_price(price) if price > 0 else '결과 없음'} · {note}",
        })
    return calendar


def unique_codes(values: Iterable[str]) -> list[str]:
    seen = set()
    output = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output


def parse_time_to_minutes(value: str | None) -> int | None:
    if not value:
        return None
    raw = str(value).strip()
    match = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?", raw)
    if not match:
        return None
    hour = int(match.group(1))
    minute = int(match.group(2) or 0)
    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return hour * 60 + minute
    return None


@dataclass
class TimePreference:
    depart_min: int | None = None
    depart_max: int | None = None
    return_min: int | None = None
    return_max: int | None = None
    exclude_before_depart: int | None = None
    prefer: str | None = None
    raw: str = ""

    def active(self) -> bool:
        return any(
            value is not None for value in [self.depart_min, self.depart_max, self.return_min, self.return_max, self.exclude_before_depart]
        ) or bool(self.prefer)

    def describe(self) -> str | None:
        parts: list[str] = []
        if self.depart_min is not None:
            parts.append(f"출발 {format_minutes(self.depart_min)} 이후")
        if self.depart_max is not None:
            parts.append(f"출발 {format_minutes(self.depart_max)} 이전")
        if self.return_min is not None:
            parts.append(f"복귀 {format_minutes(self.return_min)} 이후")
        if self.return_max is not None:
            parts.append(f"복귀 {format_minutes(self.return_max)} 이전")
        if self.exclude_before_depart is not None:
            parts.append(f"너무 이른 비행 제외({format_minutes(self.exclude_before_depart)} 이전 제외)")
        if self.prefer:
            prefer_map = {
                "late": "늦은 시간대 선호",
                "morning": "오전 선호",
                "afternoon": "오후 선호",
                "evening": "저녁 선호",
            }
            parts.append(prefer_map.get(self.prefer, self.prefer))
        return " · ".join(parts) if parts else None


def _set_min(current: int | None, value: int) -> int:
    return value if current is None else max(current, value)


def _set_max(current: int | None, value: int) -> int:
    return value if current is None else min(current, value)


def _split_time_segments(text: str) -> list[str]:
    if not text:
        return []
    parts = [part.strip() for part in re.split(r"\s*(?:,|/|\||;| 그리고 | and )\s*", text) if part.strip()]
    return parts or [text.strip()]


def _segment_scope(segment: str) -> str:
    if any(keyword in segment for keyword in ["복귀", "귀환", "오는편", "오는 편", "리턴"]):
        return "return"
    return "depart"


def _apply_bucket(pref: TimePreference, scope: str, start_hour: int, end_hour: int) -> None:
    start_minutes = start_hour * 60
    end_minutes = end_hour * 60 + 59
    if scope == "return":
        pref.return_min = _set_min(pref.return_min, start_minutes)
        pref.return_max = _set_max(pref.return_max, end_minutes)
    else:
        pref.depart_min = _set_min(pref.depart_min, start_minutes)
        pref.depart_max = _set_max(pref.depart_max, end_minutes)


def _normalize_time_ranges(pref: TimePreference, raw: str) -> None:
    if pref.depart_min is not None and pref.depart_max is not None and pref.depart_min > pref.depart_max:
        if "출발" in raw and "이후" in raw:
            pref.depart_max = None
        elif "출발" in raw and "이전" in raw:
            pref.depart_min = None
    if pref.return_min is not None and pref.return_max is not None and pref.return_min > pref.return_max:
        if any(token in raw for token in ["복귀", "귀환", "오는편", "오는 편"]) and "이후" in raw:
            pref.return_max = None
        elif any(token in raw for token in ["복귀", "귀환", "오는편", "오는 편"]) and "이전" in raw:
            pref.return_min = None


def apply_time_overrides(pref: TimePreference, *, depart_after: str | None = None, return_after: str | None = None, exclude_early_before: str | None = None, prefer: str | None = None) -> TimePreference:
    if depart_after:
        minutes = parse_time_to_minutes(str(depart_after))
        if minutes is None:
            raise ValueError(f"지원하지 않는 출발 시간 형식입니다: {depart_after}")
        pref.depart_min = _set_min(pref.depart_min, minutes)
    if return_after:
        minutes = parse_time_to_minutes(str(return_after))
        if minutes is None:
            raise ValueError(f"지원하지 않는 복귀 시간 형식입니다: {return_after}")
        pref.return_min = _set_min(pref.return_min, minutes)
    if exclude_early_before:
        minutes = parse_time_to_minutes(str(exclude_early_before))
        if minutes is None:
            raise ValueError(f"지원하지 않는 제외 시간 형식입니다: {exclude_early_before}")
        pref.exclude_before_depart = _set_min(pref.exclude_before_depart, minutes)
    if prefer:
        pref.prefer = prefer
    return pref


def parse_time_preference_args(args) -> TimePreference:
    return apply_time_overrides(
        parse_time_preference_text(getattr(args, "time_pref", None)),
        depart_after=getattr(args, "depart_after", None),
        return_after=getattr(args, "return_after", None),
        exclude_early_before=getattr(args, "exclude_early_before", None),
        prefer=getattr(args, "prefer", None),
    )


def time_preference_cli_args(time_pref: dict | None) -> list[str]:
    tp = time_pref or {}
    args: list[str] = []
    if tp.get("time_pref"):
        args.extend(["--time-pref", str(tp["time_pref"])])
    if tp.get("depart_after"):
        args.extend(["--depart-after", str(tp["depart_after"])])
    if tp.get("return_after"):
        args.extend(["--return-after", str(tp["return_after"])])
    if tp.get("exclude_early_before"):
        args.extend(["--exclude-early-before", str(tp["exclude_early_before"])])
    if tp.get("prefer"):
        args.extend(["--prefer", str(tp["prefer"])])
    return args


def describe_time_preference_payload(time_pref: dict | None) -> str | None:
    tp = time_pref or {}
    pref = apply_time_overrides(
        parse_time_preference_text(tp.get("time_pref")),
        depart_after=tp.get("depart_after"),
        return_after=tp.get("return_after"),
        exclude_early_before=tp.get("exclude_early_before"),
        prefer=tp.get("prefer"),
    )
    return pref.describe()

def format_minutes(value: int | None) -> str:
    if value is None:
        return ""
    hour = value // 60
    minute = value % 60
    return f"{hour:02d}:{minute:02d}"


def parse_time_preference_text(text: str | None) -> TimePreference:
    pref = TimePreference(raw=text or "")
    if not text:
        return pref

    normalized = str(text).strip().lower()
    normalized = normalized.replace("시 이후", "시이후").replace("시 이전", "시이전").replace("시 전", "시이전")

    for segment in _split_time_segments(normalized):
        scope = _segment_scope(segment)

        for key, (start_hour, end_hour) in TIME_BUCKETS.items():
            if key in segment:
                prefer_only = f"{key} 선호" in segment or f"{key}시간 선호" in segment or f"{key} 시간 선호" in segment
                if not prefer_only:
                    _apply_bucket(pref, scope, start_hour, end_hour)

        if "늦은 시간" in segment or "늦게" in segment:
            pref.prefer = pref.prefer or "late"
        elif "오전 선호" in segment:
            pref.prefer = pref.prefer or "morning"
        elif "오후 선호" in segment:
            pref.prefer = pref.prefer or "afternoon"
        elif "저녁 선호" in segment:
            pref.prefer = pref.prefer or "evening"

        for pattern, target in [
            (r"출발\s*(\d{1,2})(?::(\d{2}))?\s*시?이후", "depart_min"),
            (r"출발\s*(\d{1,2})(?::(\d{2}))?\s*시?이전", "depart_max"),
            (r"복귀\s*(\d{1,2})(?::(\d{2}))?\s*시?이후", "return_min"),
            (r"귀환\s*(\d{1,2})(?::(\d{2}))?\s*시?이후", "return_min"),
            (r"오는편\s*(\d{1,2})(?::(\d{2}))?\s*시?이후", "return_min"),
            (r"오는 편\s*(\d{1,2})(?::(\d{2}))?\s*시?이후", "return_min"),
            (r"복귀\s*(\d{1,2})(?::(\d{2}))?\s*시?이전", "return_max"),
            (r"귀환\s*(\d{1,2})(?::(\d{2}))?\s*시?이전", "return_max"),
            (r"오는편\s*(\d{1,2})(?::(\d{2}))?\s*시?이전", "return_max"),
            (r"오는 편\s*(\d{1,2})(?::(\d{2}))?\s*시?이전", "return_max"),
            (r"너무\s*이른\s*비행\s*제외.*?(\d{1,2})(?::(\d{2}))?\s*시", "exclude_before_depart"),
            (r"(\d{1,2})(?::(\d{2}))?\s*시\s*이전\s*비행\s*제외", "exclude_before_depart"),
        ]:
            match = re.search(pattern, segment)
            if match:
                minutes = int(match.group(1)) * 60 + int(match.group(2) or 0)
                current = getattr(pref, target)
                if target.endswith("_max"):
                    setattr(pref, target, _set_max(current, minutes) if current is not None else minutes)
                elif target == "exclude_before_depart":
                    setattr(pref, target, _set_min(current, minutes) if current is not None else minutes)
                else:
                    setattr(pref, target, _set_min(current, minutes) if current is not None else minutes)

        _normalize_time_ranges(pref, segment)

    return pref

def _within_range(value_minutes: int | None, min_minutes: int | None, max_minutes: int | None) -> bool:
    if value_minutes is None:
        return False
    if min_minutes is not None and value_minutes < min_minutes:
        return False
    if max_minutes is not None and value_minutes > max_minutes:
        return False
    return True


def _score_time_preference(item: dict, pref: TimePreference) -> int:
    depart = parse_time_to_minutes(item.get("departure_time"))
    ret = parse_time_to_minutes(item.get("return_departure_time"))
    score = 0
    if pref.prefer == "late":
        score += depart or 0
        score += (ret or 0) // 2
    elif pref.prefer == "morning":
        score -= abs((depart or 12 * 60) - 9 * 60)
    elif pref.prefer == "afternoon":
        score -= abs((depart or 12 * 60) - 15 * 60)
    elif pref.prefer == "evening":
        score -= abs((depart or 12 * 60) - 19 * 60)
    return score


def filter_and_rank_by_time_preference(items: Sequence[dict], pref: TimePreference) -> tuple[list[dict], list[dict]]:
    if not pref.active():
        return list(items), sorted(list(items), key=lambda x: x.get("price", 0) if x.get("price", 0) > 0 else 10**12)

    filtered = []
    for item in items:
        depart = parse_time_to_minutes(item.get("departure_time"))
        ret = parse_time_to_minutes(item.get("return_departure_time"))
        if pref.exclude_before_depart is not None and (depart is None or depart < pref.exclude_before_depart):
            continue
        if (pref.depart_min is not None or pref.depart_max is not None) and not _within_range(depart, pref.depart_min, pref.depart_max):
            continue
        if item.get("is_round_trip") and (pref.return_min is not None or pref.return_max is not None) and not _within_range(ret, pref.return_min, pref.return_max):
            continue
        filtered.append(item)

    ranked = sorted(
        filtered,
        key=lambda x: (
            -_score_time_preference(x, pref),
            x.get("price", 0) if x.get("price", 0) > 0 else 10**12,
        ),
    )
    filtered.sort(key=lambda x: x.get("price", 0) if x.get("price", 0) > 0 else 10**12)
    return filtered, ranked


def choose_preferred_option(items: Sequence[dict], pref: TimePreference) -> dict | None:
    _, ranked = filter_and_rank_by_time_preference(items, pref)
    return ranked[0] if ranked else None


def choose_balanced_round_trip_option(items: Sequence[dict], pref: TimePreference | None = None) -> dict | None:
    candidates = [item for item in items if (item.get("price", 0) or 0) > 0]
    if not candidates:
        return None

    candidates = sorted(candidates, key=lambda x: x.get("price", 0))
    cheapest_price = candidates[0].get("price", 0) or 0
    price_cap = int(cheapest_price * 1.15) if cheapest_price else 0
    pool = [item for item in candidates if (item.get("price", 0) or 0) <= price_cap][:5] or candidates[:3]

    def score(item: dict) -> tuple:
        price = int(item.get("price", 0) or 0)
        depart = parse_time_to_minutes(item.get("departure_time")) or 0
        ret = parse_time_to_minutes(item.get("return_departure_time")) or 0
        time_score = _score_time_preference(item, pref or TimePreference()) if pref else (depart // 2 + ret)
        return (
            -time_score,
            price,
        )

    return sorted(pool, key=score)[0] if pool else candidates[0]


def round_trip_balance_recommendation(balanced: dict | None, cheapest: dict | None, pref: TimePreference | None = None) -> str | None:
    if not balanced:
        return None
    label = balanced.get("airline") or "옵션"
    depart = format_time_or_fallback(balanced.get("departure_time"))
    ret = format_time_or_fallback(balanced.get("return_departure_time"))
    if cheapest and cheapest.get("price", 0) and balanced.get("price", 0):
        gap = int(balanced.get("price", 0)) - int(cheapest.get("price", 0))
        gap_text = "최저가와 동일 가격" if gap == 0 else (f"최저가 대비 {gap:,}원 추가" if gap > 0 else f"최저가보다 {-gap:,}원 저렴")
    else:
        gap_text = "가격 비교 정보 없음"
    reason = pref.describe() if pref and pref.describe() else "왕복 시간 균형"
    return f"왕복 균형 추천: {reason} 기준으로는 {label} 가는편 {depart}, 오는편 {ret} 조합이 무난합니다 ({gap_text})."


def build_best_option_reasons(best: dict | None, next_price: int | None = None, pref: TimePreference | None = None) -> list[str]:
    if not best:
        return []
    reasons: list[str] = []
    airline = best.get("airline")
    depart = best.get("departure_time")
    arrival = best.get("arrival_time")
    if airline:
        if depart and arrival:
            reasons.append(f"항공사 {airline}, 가는편 {depart}→{arrival}")
        else:
            reasons.append(f"항공사 {airline}")
    if best.get("return_departure_time") or best.get("return_arrival_time"):
        ret_depart = format_time_or_fallback(best.get("return_departure_time"))
        ret_arrive = best.get("return_arrival_time")
        if ret_arrive:
            reasons.append(f"오는편 {ret_depart}→{ret_arrive}")
        else:
            reasons.append(f"오는편 {ret_depart} 출발")
    if pref and pref.describe():
        reasons.append(f"시간 조건 '{pref.describe()}' 반영")
    price = int(best.get("price", 0) or best.get("cheapest_price", 0) or 0)
    if next_price and price and next_price > price:
        reasons.append(f"차상위 대비 {next_price - price:,}원 저렴")
    return reasons


def build_balanced_option_reasons(balanced: dict | None, cheapest: dict | None = None, pref: TimePreference | None = None) -> list[str]:
    if not balanced:
        return []
    reasons: list[str] = []
    depart = format_time_or_fallback(balanced.get("departure_time"))
    ret = format_time_or_fallback(balanced.get("return_departure_time"))
    reasons.append(f"왕복 시간대 {depart} / {ret} 조합")
    if pref and pref.describe():
        reasons.append(f"시간 선호 '{pref.describe()}'에 더 잘 맞음")
    price = int(balanced.get("price", 0) or 0)
    cheapest_price = int((cheapest or {}).get("price", 0) or 0)
    if price and cheapest_price:
        gap = price - cheapest_price
        if gap == 0:
            reasons.append("최저가와 동일한 가격")
        elif gap > 0:
            reasons.append(f"최저가 대비 추가 비용 {gap:,}원 수준")
    return reasons


def time_preference_recommendation(preferred: dict | None, cheapest: dict | None, pref: TimePreference) -> str | None:
    if not pref.active() or not preferred:
        return None
    subject = preferred.get("airline", "옵션")
    depart = format_time_or_fallback(preferred.get("departure_time"))
    price = preferred.get("price", 0)
    if cheapest and cheapest is not preferred and cheapest.get("price", 0) > 0 and price > 0:
        gap = price - cheapest.get("price", 0)
        gap_text = f"최저가 대비 {gap:,}원 추가" if gap > 0 else "최저가와 동일 가격"
    else:
        gap_text = "최저가와 같은 옵션"
    detail = pref.describe() or "시간 선호"
    if preferred.get("is_round_trip") and preferred.get("return_departure_time"):
        return f"시간대 추천: {detail} 기준으로는 {subject} 가는편 {depart}, 오는편 {format_time_or_fallback(preferred.get('return_departure_time'))} 옵션이 적합합니다 ({gap_text})."
    return f"시간대 추천: {detail} 기준으로는 {subject} {depart} 출발 옵션이 적합합니다 ({gap_text})."
