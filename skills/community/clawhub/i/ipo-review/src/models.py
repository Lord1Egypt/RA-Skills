from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class DocumentInfo:
    doc_id: str
    path: str
    filename: str
    suffix: str
    role: str
    role_name: str
    priority: int
    version: str
    sha256: str
    pages: int = 0
    parse_status: str = "pending"
    error: str = ""


@dataclass
class Evidence:
    evidence_id: str
    doc_id: str
    filename: str
    page: int
    kind: str
    position: str = ""
    section: str = ""
    question_no: str = ""
    paragraph_no: int = 0
    table_no: str = ""
    table_name: str = ""
    row_index: int = 0
    col_index: int = 0
    row_name: str = ""
    col_name: str = ""
    text: str = ""
    unit: str = "unknown"
    unit_source: str = "unknown"
    table_structure_confidence: float = 0.0


@dataclass
class FinancialFact:
    fact_id: str
    metric: str
    raw_metric: str
    metric_canonical_exact: str
    metric_category: str
    raw_value: str
    raw_value_text: str
    value: float | None
    currency: str
    raw_unit: str
    unit_source: str
    unit_confidence: float
    unit: str
    period: str
    period_exact: bool
    period_type: str
    scope: str
    subject: str
    category: str
    value_type: str
    is_percent: bool
    is_calculated: bool
    source_doc_id: str
    filename: str
    page: int
    position: str
    evidence_id: str
    context: str
    raw_decimal_places: int = 0
    comparison_unit: str = ""
    converted_value_unrounded: float | None = None
    converted_value_rounded: float | None = None
    comparison_decimal_places: int = 0
    rounding_interval: float = 0.0
    confidence: float = 0.65
    value_binding_reason: str = "primary_metric_value"
    extraction_skip_reason: str = ""
    semantic_role: str = "primary_metric_value"
    caliber_modifier: str = ""
    adjustment_type: str = ""
    is_adjusted_metric: bool = False
    base_metric: str = ""
    cutoff_date: str = ""
    data_nature: str = ""

    @property
    def comparable_key(self) -> str:
        return "|".join([
            self.subject or "发行人",
            self.metric_canonical_exact,
            self.period if self.period_exact else "模糊期间",
            self.period_type or "未知属性",
            self.scope or "未明口径",
            self.category or "未分类",
            self.value_type,
            self.currency or "人民币",
        ])

    @property
    def is_strictly_comparable(self) -> bool:
        return (
            self.value is not None
            and self.unit_confidence >= 0.6
            and self.period_exact
            and self.metric_canonical_exact != ""
            and self.value_type in {"amount", "percent", "percentage_point", "multiple"}
            and self.raw_unit != "unknown"
            and self.semantic_role == "primary_metric_value"
        )


@dataclass
class Issue:
    issue_id: str
    level: str
    category: str
    round: str
    files: list[str]
    item: str
    conclusion: str
    source_1: str = ""
    source_2: str = ""
    diff_amount: float | None = None
    diff_ratio: float | None = None
    caliber_analysis: str = ""
    evidence_pages: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    comparison_unit: str = ""
    source_1_converted_unrounded: float | None = None
    source_2_converted_unrounded: float | None = None
    source_1_converted_rounded: float | None = None
    source_2_converted_rounded: float | None = None
    comparison_decimal_places: int = 0
    rounding_interval: float = 0.0
    secondary_verified: bool = False
    source_1_text: str = ""
    source_2_text: str = ""
    basis: str = ""
    suggestion: str = ""
    extraction_confidence: float = 0.0
    judgement_confidence: float = 0.0
    need_manual_review: bool = True
    status: str = "MANUAL_REVIEW_CANDIDATE"
    # 复核优先级：key=重点待人工复核 / normal=一般 / noise=噪声或参考。
    review_priority: str = "normal"
    count_in_exception_total: bool = True
    display_default: bool = True
    noise_reason: str = ""
    arithmetic_rule_type: str = ""
    arithmetic_confidence: float = 0.0
    formula_complexity: str = ""
    detail_range_status: str = ""
    arithmetic_skip_reason: str = ""


def to_dict(obj: Any) -> dict[str, Any]:
    return asdict(obj)
