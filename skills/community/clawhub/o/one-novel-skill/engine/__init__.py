"""Engine package - exports all engines and new Phase 2/3 modules"""
from .novel_state import NovelState, PipelineState
from .log import info, warn, error
from .spec_builder import SpecBuilder
from .detector_wrapper import DetectorWrapper
from .generator import TextGenerator
from .scheduler import Scheduler
# Orchestrator deprecated — import explicitly: from engine.orchestrator import Orchestrator
from .registry import list_all, summary
from .circuit_breaker import CircuitBreaker, retry_with_backoff, check_idempotent_chapter

# Phase 2/3 modules
from .contracts import (PlanContext, GenerationSpec, GenerationResult, QualityReport, PersistResult,
                        EngineAnalyzeResult, EngineStatus, ChapterResult as ContractChapterResult,
                        Platform, Genre, EndingType, DetectionLevel)
from .input_adapter import build_plan_context
from .quality_gate import QualityGate
# GenerationPipeline deprecated — import explicitly: from engine.pipeline import GenerationPipeline
from .event_bus import EventBus, Event, EventType, get_event_bus
from .global_rollback import SideEffectTracker, GlobalRollbackContext

# Engines (preserve existing API)
from .engines_planning import PlanningEngine
from .engines_analysis import AnalysisEngine
from .engines_utils import DataEngine, DigitalEngine, LearningEngine, StatisticsEngine
from .engines_logic import LogicEngine
from .engines_reasoning import ReasoningEngine
from .engines_architecture import ArchitectureEngine
from .engines_writing import WritingEngine
from .engines_nlp import NLPEngine
from .engines_dialogue import DialogueEngine
from .engines_tension import TensionEngine
from .engines_psychology import PsychologyEngine
from .engines_algorithm import AlgorithmEngine
from .engines_literature import LiteratureEngine
from .engines_inspiration import InspirationEngine
from .engines_development import DevelopmentEngine
from .engines_screenplay import ScreenplayEngine
from .engines_timeline import TimelineEngine
from .engines_manager import ManagerEngine
from .simulation import SimulationEngine
from .worldbuilder import WorldBuilder
from .reference_engine import ReferenceEngine
from .research_engine import ResearchEngine

# Phase 3 — New Engine Suite
from .config import PipelineConfig, ErrorMessages
from .agent_coordinator import AgentCoordinator, create_coordinator
from .arc_manager import ArcManager
# ChapterTransaction deprecated — import explicitly: from engine.chapter_transaction import ChapterTransaction
from .character_state_engine import CharacterStateEngine
from .checkpoint_manager import CheckpointManager
from .context_builder import ContextBuilder, WorkingMemory, EpisodicMemory, SemanticMemory
from .engine_base import EngineBase, EngineRegistry
from .exceptions import (
    NovelEngineError, EngineConfigError, EngineRuntimeError,
    EngineAnalysisError, EngineInputError, EngineIntegrityError
)
from .foreshadow_engine import ForeshadowEngine
from .fractal_engine import FractalEngine, FractalBeat, FractalChapter
from .global_memory_engine import GlobalMemoryEngine
from .identity_provider import get_identity, get_prompt, get_platform_prefs
from .working_memory import WorkingMemory
from .episodic_memory import EpisodicMemory
from .semantic_memory import SemanticMemory
from .importer import ProjectImporter
from .l2_modules import L2Module, BodyLaw, MemoryTrace, ItchLaw, ShowNotTell
from .multi_line_engine import MultiLineNarrativeEngine
from .reflection_engine import ReflectionEngine
from .stability_checker import StabilityChecker
from .story_gate import StoryGate
from .style_router import StyleRouter
from .world_engine import WorldEngine
from .writing_notes import build_writing_notes

# 新增引擎 — SKILL.md 声明功能补全
from .narrative_structure import NarrativeStructureEngine
from .chapter_contract import ChapterContractEngine, ChapterContract as ChapterContractCls
from .prewriting_analyzer import PrewritingAnalyzer
from .semantic_review import SemanticReviewEngine, L3ContentQualityEngine, L4ReadingExperienceEngine
from .short_story_mode import ShortStoryModeEngine
from .platform_article import PlatformArticleEngine
from .memory_hierarchy import MemoryHierarchyEngine, TriggeredLearningEngine
from .multi_agent_collaboration import MultiAgentCollaborationEngine, CollaborationMode, TeamRole

__all__ = [
    "NovelState", "PipelineState",
    "SpecBuilder", "DetectorWrapper", "TextGenerator",
    "Scheduler",
    "CircuitBreaker", "retry_with_backoff", "check_idempotent_chapter",
    "PlanContext", "GenerationSpec", "GenerationResult", "QualityReport", "PersistResult",
    "EngineAnalyzeResult", "EngineStatus", "ContractChapterResult",
    "Platform", "Genre", "EndingType", "DetectionLevel",
    "build_plan_context", "QualityGate",
    "EventBus", "Event", "EventType", "get_event_bus",
    "SideEffectTracker", "GlobalRollbackContext",
    "PlanningEngine", "AnalysisEngine", "DigitalEngine", "LearningEngine",
    "StatisticsEngine", "DataEngine", "LogicEngine", "ReasoningEngine",
    "ArchitectureEngine", "WritingEngine", "NLPEngine", "DialogueEngine",
    "TensionEngine", "PsychologyEngine", "AlgorithmEngine", "LiteratureEngine",
    "InspirationEngine", "DevelopmentEngine", "ScreenplayEngine", "TimelineEngine",
    "ManagerEngine", "SimulationEngine", "WorldBuilder", "ReferenceEngine", "ResearchEngine",
    # Phase 3 — New Engine Suite
    "PipelineConfig", "ErrorMessages",
    "AgentCoordinator", "create_coordinator",
    "ArcManager",
    "CharacterStateEngine",
    "CheckpointManager",
    "ContextBuilder", "WorkingMemory", "EpisodicMemory", "SemanticMemory",
    # "DigitalEngine"  (dup, auto-removed),
    "EngineBase", "EngineRegistry",
    # "LearningEngine"  (dup, auto-removed),
    "NovelEngineError", "EngineConfigError", "EngineRuntimeError",
    "EngineAnalysisError", "EngineInputError", "EngineIntegrityError",
    "ForeshadowEngine",
    "FractalEngine", "FractalBeat", "FractalChapter",
    "GlobalMemoryEngine",
    "get_identity", "get_prompt", "get_platform_prefs",
    # "WorkingMemory"  (dup, auto-removed),
    # "EpisodicMemory"  (dup, auto-removed),
    # "SemanticMemory"  (dup, auto-removed),
    "ProjectImporter",
    "L2Module", "BodyLaw", "MemoryTrace", "ItchLaw", "ShowNotTell",
    "MultiLineNarrativeEngine",
    "ReflectionEngine",
    "StabilityChecker",
    # "StatisticsEngine"  (dup, auto-removed),
    "StoryGate",
    "StyleRouter",
    "WorldEngine",
    "build_writing_notes",
    "info", "warn", "error",
    "list_all", "summary",
    # 新增引擎 — SKILL.md 声明功能补全
    "NarrativeStructureEngine",
    "ChapterContractEngine", "ChapterContractCls",
    "PrewritingAnalyzer",
    "SemanticReviewEngine", "L3ContentQualityEngine", "L4ReadingExperienceEngine",
    "ShortStoryModeEngine",
    "PlatformArticleEngine",
    "MemoryHierarchyEngine", "TriggeredLearningEngine",
    "MultiAgentCollaborationEngine", "CollaborationMode", "TeamRole",
]