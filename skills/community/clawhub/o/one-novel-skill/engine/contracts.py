"""
contracts.py — 所有跨模块调用的数据契约定义
Phase 3: 契约锁死。统一引擎接口，enum替换裸str。
"""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class Platform(str, Enum):
    FANQIE = "番茄"
    QIDIAN = "起点"
    JINJIANG = "晋江"
    QIMAO = "七猫"
    FEILU = "飞卢"
    UNKNOWN = "未知平台"


class Genre(str, Enum):
    XUANHUAN = "玄幻"
    XIANXIA = "仙侠"
    DUSHI = "都市"
    KEXUAN = "科幻"
    XUANYI = "悬疑"
    YANQING = "言情"
    LISHI = "历史"
    YOUXI = "游戏"
    XIUXIAN = "修仙"
    GENERAL = "通用"


class EndingType(str, Enum):
    CLIFFHANGER = "悬疑收尾"
    RESOLUTION = "解决收尾"
    HOOK = "钩子收尾"
    TRANSITION = "过渡收尾"


class DetectionLevel(str, Enum):
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"


class EngineStatus(str, Enum):
    OK = "ok"
    DEGRADED = "degraded"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class EngineAnalyzeResult:
    """所有93引擎 analyze() 的统一返回格式"""
    engine_name: str
    status: EngineStatus = EngineStatus.OK
    verdict: str = ""
    issues: List[str] = field(default_factory=list)
    score: Optional[float] = None
    details: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    elapsed_ms: float = 0.0
    error: Optional[str] = None

    @classmethod
    def ok(cls, name: str, verdict: str = "通过", **kw) -> "EngineAnalyzeResult":
        return cls(engine_name=name, status=EngineStatus.OK, verdict=verdict, **kw)

    @classmethod
    def degraded(cls, name: str, issues: List[str], **kw) -> "EngineAnalyzeResult":
        return cls(engine_name=name, status=EngineStatus.DEGRADED, issues=issues, **kw)

    @classmethod
    def failed(cls, name: str, error: str, **kw) -> "EngineAnalyzeResult":
        return cls(engine_name=name, status=EngineStatus.FAILED, error=error, **kw)

    @classmethod
    def skipped(cls, name: str, reason: str = "") -> "EngineAnalyzeResult":
        return cls(engine_name=name, status=EngineStatus.SKIPPED, verdict=reason)


@dataclass
class PlanContext:
    """输入适配层输出 — 单章规划上下文"""
    chapter_id: int
    total_chapters: int
    platform: Platform = Platform.FANQIE
    genre: Genre = Genre.GENERAL
    core_summary: str = ""
    plot_points: List[str] = field(default_factory=list)
    word_count: int = 2500
    ending_type: EndingType = EndingType.CLIFFHANGER
    must_happen: List[str] = field(default_factory=list)
    suggested_tension: float = 0.5
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    reference_notes: str = ""


@dataclass
class GenerationSpec:
    """生成管线输出 — 规格"""
    word_count: int = 2500
    must_happen: List[str] = field(default_factory=list)
    core_summary: str = ""
    ending_type: str = "悬疑收尾"
    tension_curve: List[Dict] = field(default_factory=list)
    dopamine_phase: str = ""
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    """生成管线输出 — LLM生成结果"""
    text: str = ""
    tokens_used: int = 0
    provider: str = ""
    model: str = ""
    temperature: float = 0.0
    success: bool = False
    error: str = ""


@dataclass
class QualityReport:
    """质量门控输出 — 检测+重写结果"""
    text: str = ""
    classification: str = "GREEN"
    issues: List[str] = field(default_factory=list)
    rewrite_count: int = 0
    original_hash: str = ""
    passed: bool = True


@dataclass
class PersistResult:
    """持久化层输出 — 写入结果"""
    written_path: str = ""
    chapter_id: int = 0
    word_count: int = 0
    state_snapshot: str = ""
    success: bool = False
    error: str = ""


@dataclass
class ChapterResult:
    """统一章节输出"""
    chapter: int
    text: str = ""
    word_count: int = 0
    passed_quality_gate: bool = False
    issues: List[str] = field(default_factory=list)
    engine_results: List[EngineAnalyzeResult] = field(default_factory=list)
    events: List[Any] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return len(self.text) > 50 and self.passed_quality_gate


@dataclass
class DetectorResult:
    issues: List[str] = field(default_factory=list)
    classification: str = 'GREEN'
    weighted_score: float = 0.0
    passed: bool = True

    def __post_init__(self):
        if not (0.0 <= self.weighted_score <= 1.0):
            raise ValueError(f"weighted_score 必须在 [0, 1] 范围内，当前: {self.weighted_score}")


@dataclass
class SpecBuilderInput:
    chapter: int = 1
    ratio: float = 0.01
    core: str = ''
    ending: str = '悬念收尾'
    suggested_word_count: int = 2500
    dopamine_phase: str = ''
    suggested_emotion: str = ''
    platform: str = ''
    book_dir: str = ''
    novel_state: Any = None


def validate_plan_context(ctx: PlanContext) -> List[str]:
    errors = []
    if ctx.chapter_id < 1:
        errors.append("chapter_id must be >= 1")
    if ctx.total_chapters < 1:
        errors.append("total_chapters must be >= 1")
    if ctx.chapter_id > ctx.total_chapters:
        errors.append("chapter_id cannot exceed total_chapters")
    if ctx.word_count < 500 or ctx.word_count > 10000:
        errors.append("word_count out of range [500, 10000]")
    return errors


def validate_spec_builder_input(inp: SpecBuilderInput) -> List[str]:
    errors = []
    if inp.chapter < 1:
        errors.append('chapter must be >= 1')
    if not inp.core:
        errors.append('core must not be empty')
    if inp.suggested_word_count < 500 or inp.suggested_word_count > 10000:
        errors.append('word_count out of range [500, 10000]')
    if inp.ratio < 0 or inp.ratio > 1.0:
        errors.append('ratio must be in [0.0, 1.0]')
    return errors
