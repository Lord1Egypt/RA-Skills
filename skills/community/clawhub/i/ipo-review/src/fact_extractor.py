from __future__ import annotations

from dataclasses import dataclass
import re

from .models import Evidence, FinancialFact

NUMBER_RE = re.compile(r"(?P<num>-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(?P<pct>\s*%)?")
PERIOD_RE = re.compile(r"(截至\s*20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日|20\d{2}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日|20\d{2}\s*年(?:度)?|报告期(?:各期|内)?)")
VAGUE_PERIODS = {"报告期", "报告期内", "报告期各期"}
UNIT_CONFIDENCE = {
    "explicit_value": 1.00,
    "column_header": 0.98,
    "table_header": 0.95,
    "nearby_text": 0.85,
    "document_default": 0.75,
    "unknown": 0.0,
}

BINDING_WORDS = ("为", "分别为", "金额为", "余额为", "账面价值为", "：", ":")
STOP_INDICATORS = (
    "市盈率", "融资规模", "募集资金", "销售额", "采购额", "收入占比", "单价", "数量",
    "倍数", "每股", "估值", "发行费用", "发行规模", "募投项目", "补充流动资金",
)
VALUATION_WORDS = ("市盈率", "市净率", "估值", "倍数", "每股", "摊薄", "发行价格")
FINANCING_WORDS = ("融资规模", "募集资金", "发行规模", "发行费用", "募投项目", "补充流动资金", "募集资金额")
BASIS_WORDS = ("基于", "计算依据", "为计算依据", "以", "假设", "预计", "不低于", "敏感性测算")
AMOUNT_HINT_WORDS = ("金额", "销售额", "采购额", "收入", "成本", "费用", "万元", "亿元", "元")
MARGIN_CONTEXT_WORDS = ("毛利率", "净利率", "占比", "比例")
MARGIN_NOT_PRIMARY_WORDS = ("百分点", "影响", "差异率", "变动率", "拉低", "提升")
ADJUSTMENT_PATTERNS = (
    ("不考虑股份支付影响", "剔除股份支付影响"),
    ("剔除股份支付影响", "剔除股份支付影响"),
    ("不含股份支付", "剔除股份支付影响"),
    ("考虑股份支付影响前", "剔除股份支付影响"),
    ("调整后", "调整后"),
    ("模拟", "模拟"),
    ("备考", "备考"),
    ("剔除", "剔除"),
    ("扣除", "扣除"),
    ("假设", "假设"),
    ("预测", "预测"),
    ("测算", "测算"),
)
FORECAST_PATTERNS = ("假定同比增长", "假设增长", "预计", "预测", "测算", "不低于", "敏感性", "估值定价", "发行市盈率")


@dataclass
class MetricSegment:
    metric_alias: str
    metric_canonical_exact: str
    metric_category: str
    segment_text: str
    start_pos: int
    end_pos: int
    caliber_modifier: str = ""
    adjustment_type: str = ""
    base_metric: str = ""
    is_adjusted_metric: bool = False
    semantic_role: str = "primary_metric_value"
    is_calculated: bool = False


def extract_financial_facts(evidence: list[Evidence], metric_config: dict[str, dict[str, str]]) -> list[FinancialFact]:
    facts: list[FinancialFact] = []
    for ev in evidence:
        haystack = " ".join([ev.row_name, ev.col_name, ev.text, ev.section])
        if _skip_column(ev):
            continue
        for segment in _split_metric_segments(ev, metric_config):
            scan_text = segment.segment_text
            bound_periods = _bound_periods(haystack)
            matches = list(NUMBER_RE.finditer(scan_text))
            amount_index = 0
            for match in matches:
                raw = match.group(0).strip()
                if _must_skip_number(scan_text, match, ev):
                    continue
                belongs, binding_reason = _number_belongs_to_metric(scan_text, segment.metric_alias, match, ev)
                if not belongs:
                    continue
                value_type = _value_type(match, segment.metric_canonical_exact, scan_text)
                semantic_role = segment.semantic_role if segment.semantic_role != "primary_metric_value" else _semantic_role(binding_reason, value_type)
                raw_unit = _unit_for_value(ev, value_type)
                unit_source = _unit_source_for_value(ev, raw_unit)
                value = parse_number(match.group("num"))
                if amount_index < len(bound_periods):
                    period, period_exact, period_type = bound_periods[amount_index], True, "期间"
                else:
                    period, period_exact, period_type = _period(ev, haystack)
                if _is_non_report_period(period):
                    period_exact = False
                    period_type = "非报告期"
                amount_index += 1
                fact = FinancialFact(
                    fact_id=f"F{len(facts)+1:06d}",
                    metric=segment.metric_canonical_exact,
                    raw_metric=segment.metric_alias,
                    metric_canonical_exact=segment.metric_canonical_exact,
                    metric_category=segment.metric_category,
                    raw_value=raw,
                    raw_value_text=raw,
                    value=value,
                    currency="人民币",
                    raw_unit=raw_unit,
                    unit_source=unit_source,
                    unit_confidence=UNIT_CONFIDENCE.get(unit_source, 0.0),
                    unit=raw_unit,
                    period=period,
                    period_exact=period_exact,
                    period_type=period_type,
                    scope=_scope(haystack, ev.filename),
                    subject="发行人",
                    category=_category(ev),
                    value_type=value_type,
                    is_percent=value_type in {"percent", "percentage_point"},
                    is_calculated=segment.is_calculated,
                    source_doc_id=ev.doc_id,
                    filename=ev.filename,
                    page=ev.page,
                    position=ev.position or (f"P{ev.page}" if ev.page else ""),
                    evidence_id=ev.evidence_id,
                    context=haystack[:300],
                    raw_decimal_places=decimal_places(match.group("num")),
                    confidence=_confidence(ev, period_exact, raw_unit, value_type),
                    value_binding_reason=binding_reason,
                    semantic_role=semantic_role,
                    caliber_modifier=segment.caliber_modifier,
                    adjustment_type=segment.adjustment_type,
                    is_adjusted_metric=segment.is_adjusted_metric,
                    base_metric=segment.base_metric,
                    cutoff_date=_cutoff_date(haystack),
                    data_nature=_data_nature(segment.metric_canonical_exact, haystack, value_type),
                )
                facts.append(fact)
    return facts


def parse_number(raw: str) -> float:
    return float(raw.replace(",", ""))


def decimal_places(raw: str) -> int:
    raw = raw.replace(",", "")
    return len(raw.split(".", 1)[1]) if "." in raw else 0


def _find_metric(text: str, metric_config: dict[str, dict[str, str]]) -> tuple[str, str, str]:
    for alias in sorted(metric_config, key=len, reverse=True):
        if alias and alias in text:
            meta = metric_config[alias]
            return alias, meta["exact"], meta["category"]
    return "", "", ""


def _split_metric_segments(ev: Evidence, metric_config: dict[str, dict[str, str]]) -> list[MetricSegment]:
    text = " ".join([ev.row_name, ev.col_name, ev.text, ev.section]) if ev.kind == "table" else ev.text
    if not text:
        return []
    matches = []
    for alias in sorted(metric_config, key=len, reverse=True):
        if not alias:
            continue
        for match in re.finditer(re.escape(alias), text):
            matches.append((match.start(), match.end(), alias, metric_config[alias]))
    if not matches:
        return []
    chosen = []
    occupied: list[tuple[int, int]] = []
    for start, end, alias, meta in sorted(matches, key=lambda x: (x[0], -(x[1] - x[0]))):
        if any(not (end <= s or start >= e) for s, e in occupied):
            continue
        chosen.append((start, end, alias, meta))
        occupied.append((start, end))
    chosen.sort(key=lambda x: x[0])
    segments: list[MetricSegment] = []
    for index, (start, end, alias, meta) in enumerate(chosen):
        metric_exact = meta["exact"]
        metric_category = meta["category"]
        next_start = chosen[index + 1][0] if index + 1 < len(chosen) else len(text)
        segment_text = text[start:next_start]
        adjusted = _adjusted_metric_at(metric_exact, text, start)
        if adjusted:
            metric_exact, caliber_modifier, adjustment_type, base_metric = adjusted
            metric_category = f"{metric_category}/调整口径"
            is_adjusted_metric = True
        else:
            caliber_modifier, adjustment_type, base_metric, is_adjusted_metric = "", "", "", False
        forecast = _is_forecast_or_assumption(text, start, next_start)
        segments.append(MetricSegment(
            metric_alias=alias,
            metric_canonical_exact=metric_exact,
            metric_category=metric_category,
            segment_text=segment_text,
            start_pos=start,
            end_pos=next_start,
            caliber_modifier=caliber_modifier,
            adjustment_type=adjustment_type,
            base_metric=base_metric,
            is_adjusted_metric=is_adjusted_metric,
            semantic_role="forecast_or_assumption" if forecast else "primary_metric_value",
            is_calculated=forecast,
        ))
    return segments


def _adjusted_metric(metric_exact: str, text: str) -> tuple[str, str, str, str] | None:
    if metric_exact != "扣非归母净利润":
        return None
    window = text[max(0, text.find("扣非归母净利润") - 24):text.find("扣非归母净利润") + 40] if "扣非归母净利润" in text else text
    for phrase, normalized in ADJUSTMENT_PATTERNS:
        if phrase in window:
            if normalized == "剔除股份支付影响":
                return "扣非归母净利润_剔除股份支付影响", normalized, "share_based_payment_excluded", metric_exact
            return f"{metric_exact}_{normalized}", normalized, "adjusted_or_simulated", metric_exact
    if re.search(r"不考虑.{0,12}影响", window):
        return f"{metric_exact}_剔除特定影响", "不考虑某项影响", "effect_excluded", metric_exact
    return None


def _adjusted_metric_at(metric_exact: str, text: str, metric_start: int) -> tuple[str, str, str, str] | None:
    if metric_exact != "扣非归母净利润":
        return None
    window = text[max(0, metric_start - 24):metric_start + 40]
    for phrase, normalized in ADJUSTMENT_PATTERNS:
        if phrase in window:
            if normalized == "剔除股份支付影响":
                return "扣非归母净利润_剔除股份支付影响", normalized, "share_based_payment_excluded", metric_exact
            if normalized in {"假设", "预测", "测算"}:
                continue
            return f"{metric_exact}_{normalized}", normalized, "adjusted_or_simulated", metric_exact
    if re.search(r"不考虑.{0,12}影响", window):
        return f"{metric_exact}_剔除特定影响", "不考虑某项影响", "effect_excluded", metric_exact
    return None


def _is_forecast_or_assumption(text: str, start: int, end: int) -> bool:
    window = text[max(0, start - 16):min(len(text), end + 24)]
    return any(pattern in window for pattern in FORECAST_PATTERNS)


def _cutoff_date(text: str) -> str:
    match = re.search(r"(?:统计)?(?:截止|截至|截止日期为)\s*(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(?:(\d{1,2})\s*日|末)", text)
    if not match:
        return ""
    year, month, day = match.group(1), int(match.group(2)), match.group(3)
    if day:
        return f"{year}-{month:02d}-{int(day):02d}"
    return f"{year}-{month:02d}"


def _data_nature(metric_exact: str, text: str, value_type: str) -> str:
    if "期后回款比例" in metric_exact or ("期后回款" in text and value_type == "percent"):
        return "collection_ratio"
    if "期后回款金额" in metric_exact or ("期后回款" in text and value_type == "amount"):
        return "collection_amount"
    if "未回款比例" in metric_exact:
        return "uncollected_ratio"
    if "未回款金额" in metric_exact:
        return "uncollected_amount"
    if "账面价值" in metric_exact:
        return "book_value"
    if "余额" in metric_exact or "账面余额" in metric_exact:
        return "balance"
    if "收入" in metric_exact:
        return "revenue"
    if "利润" in metric_exact:
        return "profit"
    if "率" in metric_exact:
        return "margin"
    return ""


def _skip_column(ev: Evidence) -> bool:
    label = f"{ev.row_name} {ev.col_name}"
    return bool(re.search(r"序号|编号|题号|页码|No\.|序列", label, re.I))


def _must_skip_number(text: str, match: re.Match, ev: Evidence) -> bool:
    raw = match.group("num").replace(",", "").lstrip("-")
    if raw.isdigit() and 1900 <= int(raw) <= 2035:
        return True
    if _is_period_number(text, match) or _is_identifier_number(text, match):
        return True
    if _is_range_number(text, match):
        return True
    if _skip_column(ev):
        return True
    return False


def _is_range_number(text: str, match: re.Match) -> bool:
    before = text[max(0, match.start() - 4):match.start()]
    after = text[match.end():match.end() + 8]
    if re.search(r"[%％]?\s*(?:-|－|—|~|～|至)\s*$", before):
        return True
    if re.match(r"\s*[%％]?\s*(?:-|－|—|~|～|至)\s*-?\d", after):
        return True
    return False


def _is_period_number(text: str, match: re.Match) -> bool:
    raw = match.group("num").replace(",", "").lstrip("-")
    prefix = text[max(0, match.start() - 1):match.start()]
    suffix = text[match.end():match.end() + 2]
    return raw.startswith("20") and len(raw) == 4 and ("年" in suffix or prefix in {"-", "－", "—", "至"})


def _is_identifier_number(text: str, match: re.Match) -> bool:
    before = text[max(0, match.start() - 2):match.start()]
    after = text[match.end():match.end() + 2]
    return bool(re.search(r"[A-Za-z]-?$|^-?[A-Za-z]|[-_/]", before + after))


def _scan_segment(ev: Evidence, metric_alias: str) -> str:
    if ev.kind == "table":
        return ev.text
    pos = ev.text.find(metric_alias)
    if pos < 0:
        return ev.text
    segment = ev.text[pos:pos + 110]
    stops = [p for p in [segment.find("。"), segment.find("；"), segment.find(";")] if p > 0]
    return segment[:min(stops)] if stops else segment


def _number_belongs_to_metric(text: str, metric_alias: str, match: re.Match, evidence: Evidence) -> tuple[bool, str]:
    """Return whether this numeric token is a primary value of the matched metric."""
    around = text[max(0, match.start() - 24):match.end() + 24]
    metric_pos = text.find(metric_alias)
    if evidence.kind == "table":
        return _metric_value_type_allowed(metric_alias, match, around)
    if metric_pos < 0:
        return False, "metric_window_too_far"
    between = text[metric_pos + len(metric_alias):match.start()]
    compact_between = re.sub(r"\s+", "", between)
    if any(w in around or w in compact_between for w in VALUATION_WORDS):
        return False, "valuation_multiple"
    if any(w in around or w in compact_between for w in FINANCING_WORDS):
        return False, "financing_amount"
    if any(w in compact_between for w in STOP_INDICATORS):
        return False, "unrelated_later_number"
    if _basis_phrase_before_metric(text, metric_pos, match.start()) and any(w in around for w in VALUATION_WORDS + FINANCING_WORDS):
        return False, "derived_metric_context"
    if len(compact_between) > 40 and not any(w in compact_between for w in BINDING_WORDS):
        return False, "metric_window_too_far"
    if not any(w in compact_between for w in BINDING_WORDS) and len(compact_between) > 18:
        return False, "unrelated_later_number"
    return _metric_value_type_allowed(metric_alias, match, around)


def _basis_phrase_before_metric(text: str, metric_pos: int, number_pos: int) -> bool:
    left = text[max(0, metric_pos - 12):number_pos]
    return any(w in left for w in BASIS_WORDS)


def _metric_value_type_allowed(metric_alias: str, match: re.Match, around: str) -> tuple[bool, str]:
    has_percent = bool(match.group("pct"))
    if "百分点" in around:
        return False, "percentage_point_not_percent"
    if "率" in metric_alias or "占比" in metric_alias or "比例" in metric_alias:
        if any(w in around for w in MARGIN_NOT_PRIMARY_WORDS):
            return False, "percentage_point_not_percent"
        if any(w in around for w in ("15%-20%", "15%至20%")):
            return False, "range_value"
        if not has_percent:
            if any(w in around for w in AMOUNT_HINT_WORDS):
                return False, "sales_amount_not_margin"
            return False, "sales_amount_not_margin"
        return True, "primary_metric_value"
    if has_percent and ("占比" in around or "比例" in around):
        return True, "primary_metric_value"
    if has_percent:
        return False, "percentage_point_not_percent"
    if "倍" in around or any(w in around for w in VALUATION_WORDS):
        return False, "valuation_multiple"
    return True, "primary_metric_value"


def _semantic_role(binding_reason: str, value_type: str) -> str:
    if binding_reason == "primary_metric_value":
        return "primary_metric_value"
    if binding_reason == "percentage_point_not_percent":
        return "percentage_point_difference"
    if binding_reason in {"valuation_multiple", "financing_amount", "sales_amount_not_margin", "range_value"}:
        return binding_reason
    if value_type == "multiple":
        return "valuation_multiple"
    return binding_reason


def _value_type(match: re.Match, metric: str, text: str) -> str:
    around = text[max(0, match.start() - 10):match.end() + 10] if hasattr(match, "start") else text
    if "百分点" in around:
        return "percentage_point"
    if "倍" in around:
        return "multiple"
    if match.group("pct") or "%" in around or "百分比" in around:
        return "percent"
    if "率" in metric or "占比" in metric:
        return "percent"
    return "amount"


def _unit_for_value(ev: Evidence, value_type: str) -> str:
    if value_type == "percent":
        return "%"
    if value_type == "percentage_point":
        return "百分点"
    if value_type == "multiple":
        return "倍"
    if ev.unit and ev.unit != "unknown":
        return ev.unit
    return _default_unit_by_file(ev.filename)


def _unit_source_for_value(ev: Evidence, raw_unit: str) -> str:
    if raw_unit == "unknown":
        return "unknown"
    if ev.unit and ev.unit != "unknown":
        return ev.unit_source
    return "document_default"


def _default_unit_by_file(filename: str) -> str:
    if any(k in filename for k in ["财务报表", "附注", "年报"]):
        return "元"
    if any(k in filename for k in ["招股说明书", "问询函的回复", "问询回复"]):
        return "万元"
    return "unknown"


def _period(ev: Evidence, text: str) -> tuple[str, bool, str]:
    candidates = []
    if ev.kind == "table":
        candidates.extend([ev.col_name, ev.row_name])
    candidates.append(text)
    joined = " ".join(candidates)
    match = PERIOD_RE.search(joined)
    if not match:
        return "", False, _period_type(text)
    period = re.sub(r"\s+", "", match.group(1))
    if period in VAGUE_PERIODS:
        return period, False, _period_type(text)
    if period.startswith("截至") or re.search(r"\d{1,2}月\d{1,2}日", period):
        return period, True, "时点"
    if period.endswith("年度") or period.endswith("年"):
        return period.replace("年", "年度") if not period.endswith("年度") else period, True, _period_type(text)
    return period, True, _period_type(text)


def _period_type(text: str) -> str:
    if any(k in text for k in ["余额", "账面价值", "账面余额", "资产", "负债", "所有者权益", "截至"]):
        return "时点"
    return "期间"


def _scope(text: str, filename: str = "") -> str:
    if any(k in text for k in ["母公司报表", "母公司口径", "母公司财务报表"]):
        return "母公司"
    if any(k in text for k in ["合并报表", "合并口径", "本集团"]):
        return "合并"
    if any(k in filename for k in ["专项核查", "核查报告"]) and not any(k in text for k in ["发行人", "公司", "本公司"]):
        return "口径待确认"
    return "发行人合并"


def _bound_periods(text: str) -> list[str]:
    if "分别为" not in text:
        return []
    range_match = re.search(r"(20[2-3]\d)\s*[-－—至]\s*(20[2-3]\d)\s*年", text)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2))
        if 2020 <= start <= end <= 2025 and end - start <= 5:
            return [f"{year}年度" for year in range(start, end + 1)]
    years = [int(y) for y in re.findall(r"20[2-3]\d(?=\s*年度|\s*年)", text)]
    years = [y for y in years if 2020 <= y <= 2025]
    unique = []
    for y in years:
        if y not in unique:
            unique.append(y)
    return [f"{y}年度" for y in unique]


def _is_non_report_period(period: str) -> bool:
    match = re.search(r"(20\d{2})", period or "")
    if not match:
        return False
    year = int(match.group(1))
    return year < 2020 or year > 2025


def _category(ev: Evidence) -> str:
    if ev.row_name and ev.col_name:
        row = re.sub(r"\s+", "", ev.row_name)
        col = re.sub(r"\s+", "", ev.col_name)
        # 分类维度不得把年度列混入，年度已经进入period。
        if re.search(r"20\d{2}", col):
            return row or "未分类"
        return f"{row}/{col}"
    return "未分类"


def _confidence(ev: Evidence, period_exact: bool, unit: str, value_type: str) -> float:
    score = 0.5
    if ev.kind == "table" and ev.table_structure_confidence >= 0.6:
        score += 0.15
    if period_exact:
        score += 0.15
    if unit != "unknown":
        score += 0.15
    if value_type in {"amount", "percent"}:
        score += 0.05
    return min(score, 0.95)


def normalize_value(raw: str, unit: str, is_percent: bool = False) -> float | None:
    if unit == "unknown":
        return None
    value = parse_number(raw)
    if is_percent:
        return value
    if "亿元" in unit:
        return value * 100_000_000
    if "万元" in unit:
        return value * 10_000
    if "千元" in unit:
        return value * 1_000
    return value
