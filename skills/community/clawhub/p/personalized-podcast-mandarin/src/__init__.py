"""AI Podcast Dual-Host Skill Package"""

__version__ = "2.1.0"

from .schema import (
    TokenUsage,
    ResearchTopic,
    TopicAbstraction,
    ResearchSummary,
    OutlineSegment,
    Outline,
    DialogueLine,
    ScriptVersion,
    PodcastOutput,
)
from .tts_controller import VolcanoTTSController, generate_dual_audio
from .persona_extractor import PersonaExtractor, get_preset_persona, extract_persona
from .persona_manager import (
    PersonaManager,
    DoublePersonaManager,
    check_first_time,
    list_user_personas,
    delete_persona,
)
from .memory_skill import MemorySkill, quick_retrieve

__all__ = [
    "TokenUsage",
    "ResearchTopic",
    "TopicAbstraction",
    "ResearchSummary",
    "OutlineSegment",
    "Outline",
    "DialogueLine",
    "ScriptVersion",
    "PodcastOutput",
    "VolcanoTTSController",
    "generate_dual_audio",
    "PersonaExtractor",
    "get_preset_persona",
    "extract_persona",
    "PersonaManager",
    "DoublePersonaManager",
    "check_first_time",
    "list_user_personas",
    "delete_persona",
    "MemorySkill",
    "quick_retrieve",
]