#!/usr/bin/env python3
from __future__ import annotations
"""
集中定义输入输出契约、枚举、默认路径、版本号。
把散落在脚本和schema文档中的字段，收敛成统一Python数据结构。
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from collections.abc import Iterable
from datetime import datetime
import json
import re


class SemanticRole(Enum):
    """语义角色枚举"""
    BACKGROUND = "background"
    PROBLEM = "problem"
    OBJECTIVE = "objective"
    METHOD = "method"
    EVIDENCE = "evidence"
    RESULT = "result"
    SUMMARY = "summary"
    TRANSITION = "transition"
    UNKNOWN = "unknown"


class IssueDimension(Enum):
    """问题维度"""
    STRUCTURE = "structure"
    LOGIC = "logic"
    FORMAT = "format"
    CONSISTENCY = "consistency"


class SourceType(Enum):
    """问题来源类型"""
    STYLE_DEVIATION = "style_deviation"  # 对 refs 的写作风格偏离
    FORMAT = "format"            # 格式检查
    TERMINOLOGY = "terminology"  # 术语验证
    LOGIC = "logic"              # 逻辑不通顺（基于经验）
    HISTORICAL_FORMAT = "historical_format"  # 往届格式问题


class DiffType(Enum):
    """修改类型"""
    DELETE = "-"
    ADD = "+"
    REPLACE = "~"
    KEEP = "="


class ConfidenceLevel(Enum):
    """置信度等级"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class HumanReviewRequired(Enum):
    """人工审阅需求"""
    NOT_REQUIRED = "not_required"
    RECOMMENDED = "recommended"
    REQUIRED = "required"


class AIPatternType(Enum):
    """AI模式类型"""
    TEMPLATE_TRANSITION = "template_transition"
    OVER_EVEN_PARAGRAPHING = "over_even_paragraphing"
    ABSTRACT_SUMMARY_WITHOUT_ANCHOR = "abstract_summary_without_anchor"
    CLAIM_BEFORE_EVIDENCE = "claim_before_evidence"
    BALANCED_BUT_EMPTY_SENTENCE = "balanced_but_empty_sentence"
    GENERIC_CONCLUSION_TAIL = "generic_conclusion_tail"


class FormatCheckType(Enum):
    """格式检查类型"""
    FONT_SIZE = "font_size"
    FONT_NAME = "font_name"
    LINE_SPACING = "line_spacing"
    PARAGRAPH_SPACING = "paragraph_spacing"
    INDENTATION = "indentation"
    ALIGNMENT = "alignment"
    HEADING_LEVEL = "heading_level"
    PAGE_MARGIN = "page_margin"


class AnchorKind(Enum):
    """结构化锚点类型。主线优先消费它，而不是退回 location/source_text 猜定位。"""
    BODY_PARAGRAPH = "body_paragraph"
    TABLE_CELL = "table_cell"
    SECTION_PROXY = "section_proxy"
    HEADER_PROXY = "header_proxy"
    FOOTER_PROXY = "footer_proxy"
    DOCUMENT_PROXY = "document_proxy"


ANCHOR_CONTRACT_VERSION = "2.0-mainline"
STRUCTURED_ANCHOR_REQUIRED_SOURCES = {
    SourceType.FORMAT.value,
    SourceType.TERMINOLOGY.value,
    SourceType.LOGIC.value,
    SourceType.STYLE_DEVIATION.value,
}


def normalize_anchor_text(text: str) -> str:
    normalized = re.sub(r"\s+", "", text or "")
    return (
        normalized
        .replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
        .replace("「", '"')
        .replace("」", '"')
    )


def source_type_value(value: Any) -> str:
    return value.value if isinstance(value, SourceType) else str(value or "")


def source_requires_structured_anchor(value: Any) -> bool:
    return source_type_value(value) in STRUCTURED_ANCHOR_REQUIRED_SOURCES


def normalize_anchor_dict(anchor: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not isinstance(anchor, dict):
        return None
    normalized = {k: v for k, v in anchor.items() if v is not None}
    kind = normalized.get("kind")
    if isinstance(kind, AnchorKind):
        normalized["kind"] = kind.value
    elif kind is not None:
        normalized["kind"] = str(kind)
    for key in (
        "paragraph_index",
        "xml_paragraph_index",
        "section_index",
        "table_index",
        "row_index",
        "column_index",
        "cell_paragraph_index",
        "proxy_paragraph_index",
        "proxy_xml_paragraph_index",
        "start_offset",
        "end_offset",
    ):
        if key in normalized:
            try:
                normalized[key] = int(normalized[key])
            except Exception:
                normalized.pop(key, None)
    for key in ("node_id", "presentation_node_id", "presentation_kind", "selection_mode", "resolver", "matched_from", "attach_text_source"):
        if key in normalized and normalized.get(key) is not None:
            normalized[key] = str(normalized[key])
    section_path = normalized.get("section_path")
    if isinstance(section_path, tuple):
        normalized["section_path"] = list(section_path)
    elif isinstance(section_path, Iterable) and not isinstance(section_path, (str, bytes, dict)):
        normalized["section_path"] = [str(item) for item in section_path if str(item).strip()]
    if "attach_text" in normalized and isinstance(normalized["attach_text"], str):
        normalized["attach_text"] = normalized["attach_text"].strip()
    normalized.setdefault("contract_version", ANCHOR_CONTRACT_VERSION)
    return normalized


@dataclass
class Location:
    """位置信息"""
    chapter: Optional[str] = None
    section: Optional[str] = None
    paragraph: Optional[int] = None
    sentence: Optional[int] = None
    line: Optional[int] = None
    page: Optional[int] = None
    text_range: Optional[Tuple[int, int]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Segment:
    """文本片段"""
    text: str
    kind: str
    location: Location
    semantic_roles: List[SemanticRole] = field(default_factory=list)
    primary_role: Optional[SemanticRole] = None
    chapter: Optional[str] = None
    section_path: Optional[str] = None
    provenance: str = ""  # 来源说明
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "kind": self.kind,
            "location": self.location.to_dict(),
            "semantic_roles": [role.value for role in self.semantic_roles],
            "primary_role": self.primary_role.value if self.primary_role else None,
            "chapter": self.chapter,
            "section_path": self.section_path,
            "provenance": self.provenance
        }


@dataclass
class StyleFeature:
    """风格特征"""
    feature_id: str
    dimension: str  # structure, logic, format, expression, anti-ai
    description: str
    support_ratio: float  # 在多少refs中出现
    discriminative_power: float  # 区分度
    conflict_ratio: float  # refs内部分歧
    importance_score: float  # 最终权重
    evidence_refs: List[str] = field(default_factory=list)  # 证据参照ID
    sample_evidence: List[str] = field(default_factory=list)  # 示例文本
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IssueItem:
    """问题项"""
    id: str
    dimension: IssueDimension
    location: Location
    source_text: str
    basis_from_refs: List[str]  # 参照依据ID
    problem: str
    risk: str
    fix_direction: str
    human_review_required: HumanReviewRequired
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    ai_pattern_type: Optional[AIPatternType] = None
    format_check_type: Optional[FormatCheckType] = None
    term_issue: Optional[str] = None
    severity: str = "medium"  # low, medium, high, critical
    priority: int = 5  # 1-10, 1为最高优先级
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["dimension"] = self.dimension.value
        result["human_review_required"] = self.human_review_required.value
        result["confidence"] = self.confidence.value
        if self.ai_pattern_type:
            result["ai_pattern_type"] = self.ai_pattern_type.value
        if self.format_check_type:
            result["format_check_type"] = self.format_check_type.value
        return result


@dataclass
class UnifiedAnnotation:
    """统一批注项，聚合所有检测器发现的问题"""
    id: str
    source: SourceType
    issue_type: str  # 细粒度问题类型，如 font_size, variant_usage, logic_coherence
    location: Optional[Location] = None
    location_hint: Optional[str] = None  # 人类可读位置提示，如 "第3段"
    source_text: str = ""
    problem: str = ""
    suggestion: str = ""
    basis: str = ""  # 依据说明，例如 refs 依据、规则依据、经验依据
    risk: str = ""
    diff_type: Optional[DiffType] = None  # 若涉及改写，建议的修改类型
    human_review_required: HumanReviewRequired = HumanReviewRequired.RECOMMENDED
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    severity: str = "medium"
    anchor: Optional[Dict[str, Any]] = None  # 结构化锚点契约；优先于 location_hint/source_text fallback
    sentence_text: Optional[str] = None  # 句子级锚点文本，优先于整段 source_text
    focus_text: Optional[str] = None  # 句内更小的短语级锚点文本，可选
    rewrite_text: Optional[str] = None  # 局部增删改示例文本
    # 以下字段用于内部映射
    dimension: Optional[IssueDimension] = None
    ai_pattern_type: Optional[AIPatternType] = None
    format_check_type: Optional[FormatCheckType] = None
    term_issue: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # 转换枚举值为字符串
        result["source"] = self.source.value
        if self.location:
            result["location"] = self.location.to_dict()
        if self.diff_type:
            result["diff_type"] = self.diff_type.value
        result["human_review_required"] = self.human_review_required.value
        result["confidence"] = self.confidence.value
        if self.dimension:
            result["dimension"] = self.dimension.value
        if self.ai_pattern_type:
            result["ai_pattern_type"] = self.ai_pattern_type.value
        if self.format_check_type:
            result["format_check_type"] = self.format_check_type.value
        result["anchor"] = normalize_anchor_dict(self.anchor)
        # 移除None值
        result = {k: v for k, v in result.items() if v is not None}
        return result
    
    @classmethod
    def from_issue_item(cls, issue: IssueItem) -> UnifiedAnnotation:
        """从现有IssueItem转换"""
        source = SourceType.FORMAT
        if issue.format_check_type:
            source = SourceType.FORMAT
        return UnifiedAnnotation(
            id=issue.id,
            source=source,
            issue_type=issue.dimension.value,
            location=issue.location,
            source_text=issue.source_text,
            problem=issue.problem,
            suggestion=issue.fix_direction,
            basis=", ".join(issue.basis_from_refs) if issue.basis_from_refs else "",
            risk=issue.risk,
            human_review_required=issue.human_review_required,
            confidence=issue.confidence,
            severity=issue.severity,
            anchor=getattr(issue, "anchor", None),
            dimension=issue.dimension,
            ai_pattern_type=issue.ai_pattern_type,
            format_check_type=issue.format_check_type,
            term_issue=issue.term_issue,
        )
    
    @classmethod
    def from_format_issue(cls, issue: Dict[str, Any]) -> UnifiedAnnotation:
        """从format_checker.py输出的格式问题字典转换"""
        # 假设issue字典包含字段：id, location, paragraphIndex, styleName, checkType, expected, actual, sourceText, problem, fixDirection
        return UnifiedAnnotation(
            id=issue.get("id", f"format-{issue.get('paragraphIndex', 0)}"),
            source=SourceType.FORMAT,
            issue_type=issue.get("checkType", "unknown"),
            location_hint=issue.get("location", ""),
            source_text=issue.get("sourceText", ""),
            problem=issue.get("problem", ""),
            suggestion=issue.get("fixDirection", ""),
            basis="文档样式一致性检查",
            risk="格式不一致可能影响评审印象",
            human_review_required=HumanReviewRequired.RECOMMENDED,
            confidence=ConfidenceLevel.HIGH,
            severity="low",
            anchor=issue.get("anchor"),
            format_check_type=FormatCheckType(issue["checkType"]) if "checkType" in issue and hasattr(FormatCheckType, issue["checkType"].upper()) else None,
        )
    
    @classmethod
    def from_term_issue(cls, issue: Dict[str, Any]) -> UnifiedAnnotation:
        """从正式术语报告输出的术语问题字典转换"""
        return UnifiedAnnotation(
            id=issue.get("id", f"term-{issue.get('term', '')}"),
            source=SourceType.TERMINOLOGY,
            issue_type=issue.get("issueType", "unknown"),
            location_hint=issue.get("locationHint", ""),
            source_text=issue.get("sourceText", ""),
            problem=issue.get("problem", ""),
            suggestion=issue.get("suggestion", ""),
            basis=issue.get("cnkiSearchHint", "术语一致性检查"),
            risk="术语混用可能降低专业性",
            human_review_required=HumanReviewRequired.RECOMMENDED,
            confidence=ConfidenceLevel(issue.get("confidence", "medium")),
            severity="medium",
            anchor=issue.get("anchor"),
            term_issue=issue.get("term", ""),
        )


@dataclass
class RewriteItem:
    """改写项"""
    location: Location
    diff_type: DiffType
    original: str
    suggested: str
    basis_from_refs: List[str]
    reason: str
    risk: str
    human_review_required: HumanReviewRequired
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "location": self.location.to_dict(),
            "diff_type": self.diff_type.value,
            "original": self.original,
            "suggested": self.suggested,
            "basis_from_refs": self.basis_from_refs,
            "reason": self.reason,
            "risk": self.risk,
            "human_review_required": self.human_review_required.value,
            "confidence": self.confidence.value
        }


@dataclass
class ScoreReport:
    """评分报告"""
    overall_score: float
    dimension_scores: Dict[str, float]  # structure, logic, format, ai-alignment, semantic-alignment
    resolved_issues: List[str]  # 已解决的问题ID
    remaining_issues: List[str]  # 未解决的问题ID
    new_risks: List[str]  # 新引入的风险
    acceptance_decision: str  # pass, revise, human-review
    score_details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ParsedDocument:
    """解析后的文档"""
    title: str
    author: Optional[str]
    blocks: List[Dict[str, Any]]
    chapters: List[Dict[str, Any]]
    extraction_risks: List[str]
    file_path: str
    file_type: str  # docx, pdf, md
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "author": self.author,
            "blocks_count": len(self.blocks),
            "chapters_count": len(self.chapters),
            "extraction_risks": self.extraction_risks,
            "file_path": self.file_path,
            "file_type": self.file_type
        }


@dataclass
class SegmentSet:
    """片段集合"""
    segments: List[Segment]
    document_id: str
    extraction_rules: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_id": self.document_id,
            "segment_count": len(self.segments),
            "segments": [segment.to_dict() for segment in self.segments],
            "extraction_rules": self.extraction_rules
        }


# 默认路径和常量
DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_STYLE_PROFILE_FILE = "style-profile.json"
DEFAULT_REF_STYLE_BASIS_FILE = "ref-style-basis.md"
DEFAULT_FINAL_ADVICE_FILE = "final-advice.md"
DEFAULT_REVISION_SCORE_REPORT_FILE = "revision-score-report.json"

# 版本号
CONTRACT_VERSION = "1.0"
SCHEMA_VERSION = "1.0"

# 默认阈值
DEFAULT_CONFIDENCE_THRESHOLD = 0.7
DEFAULT_IMPORTANCE_THRESHOLD = 0.5
DEFAULT_SEVERITY_THRESHOLD = "medium"

# 语义角色映射
SEMANTIC_ROLE_KEYWORDS = {
    SemanticRole.BACKGROUND: ["背景", "随着", "近年来", "由于", "鉴于", "在...背景下"],
    SemanticRole.PROBLEM: ["问题", "挑战", "难点", "不足", "缺陷", "局限性", "亟待解决"],
    SemanticRole.OBJECTIVE: ["目标", "目的", "旨在", "为了", "试图", "期望"],
    SemanticRole.METHOD: ["方法", "方案", "算法", "模型", "框架", "技术", "实现"],
    SemanticRole.EVIDENCE: ["实验", "数据", "结果", "证明", "验证", "分析", "统计"],
    SemanticRole.RESULT: ["结果", "效果", "性能", "准确率", "提升", "降低", "优于"],
    SemanticRole.SUMMARY: ["总结", "小结", "综上所述", "总而言之", "总的来说", "本章小结"],
    SemanticRole.TRANSITION: ["接下来", "下面", "然后", "进一步", "此外", "同时", "另一方面"]
}


def to_json(obj: Any, indent: int = 2) -> str:
    """将对象转换为JSON字符串"""
    if hasattr(obj, 'to_dict'):
        return json.dumps(obj.to_dict(), ensure_ascii=False, indent=indent)
    elif isinstance(obj, dict):
        return json.dumps(obj, ensure_ascii=False, indent=indent)
    elif isinstance(obj, list):
        return json.dumps([item.to_dict() if hasattr(item, 'to_dict') else item 
                          for item in obj], ensure_ascii=False, indent=indent)
    else:
        return json.dumps(asdict(obj) if hasattr(obj, '__dataclass_fields__') else obj,
                         ensure_ascii=False, indent=indent)


def from_json(data: Dict[str, Any], cls: type) -> Any:
    """从JSON字典创建对象"""
    # 处理枚举字段
    field_types = {f.name: f.type for f in cls.__dataclass_fields__.values()}
    
    kwargs = {}
    for field_name, field_type in field_types.items():
        if field_name not in data:
            continue
            
        value = data[field_name]
        
        # 处理枚举类型
        if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
            # Union类型，检查是否为枚举
            for arg in field_type.__args__:
                if hasattr(arg, '__members__'):
                    field_type = arg
                    break
        
        if hasattr(field_type, '__members__'):
            # 枚举类型
            if value is not None:
                if isinstance(value, str):
                    kwargs[field_name] = field_type(value)
                elif isinstance(value, field_type):
                    kwargs[field_name] = value
            else:
                kwargs[field_name] = None
        else:
            kwargs[field_name] = value
    
    return cls(**kwargs)


if __name__ == "__main__":
    # 测试契约
    location = Location(chapter="第一章", paragraph=2, sentence=1)
    print("Location:", to_json(location))
    
    segment = Segment(
        text="本文旨在研究目标问题的解决方法。",
        kind="chapter1_research_objective",
        location=location,
        semantic_roles=[SemanticRole.OBJECTIVE],
        primary_role=SemanticRole.OBJECTIVE
    )
    print("\nSegment:", to_json(segment))
    
    issue = IssueItem(
        id="issue-001",
        dimension=IssueDimension.LOGIC,
        location=location,
        source_text="实验结果表明...",
        basis_from_refs=["ref-style-01", "ref-style-02"],
        problem="结论前置，证据后置",
        risk="可能削弱论证力度",
        fix_direction="先写实验设置，再给结果",
        human_review_required=HumanReviewRequired.RECOMMENDED,
        ai_pattern_type=AIPatternType.CLAIM_BEFORE_EVIDENCE
    )
    print("\nIssue:", to_json(issue))
