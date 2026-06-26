"""NIMA Core cognition module."""

# Sparse Block VSA for memory efficiency
from .sparse_block_vsa import SparseBlockHDVector

# Sparse Block Memory - VSA episodic memory
from .sparse_block_memory import (
    SparseBlockMemory,
    SparseBlockConfig,
    BlockSelectionLearner,
)

# phi_estimator moved to nima_core.experimental


# Schema Extractor - Knowledge extraction from memories
from .schema_extractor import (
    SchemaExtractor,
    Schema,
    Entity,
    Relationship,
    EventPattern,
)

# theory_of_mind moved to nima_core.experimental

# Cross-affect interactions
from .affect_interactions import (
    apply_cross_affect_interactions,
    get_interaction_effects,
    explain_interactions,
    INTERACTION_MATRIX,
    INTERACTION_THRESHOLD,
)

# Emotion history
from .affect_history import (
    AffectSnapshot,
    AffectHistory,
)

# Correlation analysis
from .affect_correlation import (
    AffectCorrelation,
    StateTransition,
    detect_emotional_patterns,
)

# Exceptions
from .exceptions import (
    NimaError,
    AffectVectorError,
    InvalidAffectNameError,
    AffectValueError,
    BaselineValidationError,
    StatePersistenceError,
    ProfileNotFoundError,
    EmotionDetectionError,
    ArchetypeError,
    UnknownArchetypeError,
)

# Dynamic Affect System
from .dynamic_affect import (
    DynamicAffectSystem,
    AffectVector,
    get_affect_system,
    get_current_affect,
    process_emotional_input,
    AFFECTS,
    AFFECT_INDEX,
    DEFAULT_BASELINE,
)
from .personality_profiles import PersonalityManager, get_profile, list_profiles
from .emotion_detection import map_emotions_to_affects, detect_affect_from_text
from .response_modulator_v2 import GenericResponseModulator, ResponseGuidance, modulate_response
from .archetypes import (
    ARCHETYPES,
    get_archetype,
    list_archetypes,
    baseline_from_archetype,
    baseline_from_description
)

__all__ = [
    # Sparse Block VSA
    "SparseBlockHDVector",
    "SparseBlockConfig",
    # Sparse Block Memory
    "SparseBlockMemory",
    "BlockSelectionLearner",
    # Schema Extractor
    "SchemaExtractor",
    "Schema",
    "Entity",
    "Relationship",
    "EventPattern",
    # Cross-affect interactions
    "apply_cross_affect_interactions",
    "get_interaction_effects",
    "explain_interactions",
    "INTERACTION_MATRIX",
    "INTERACTION_THRESHOLD",
    # Emotion history
    "AffectSnapshot",
    "AffectHistory",
    # Correlation analysis
    "AffectCorrelation",
    "StateTransition",
    "detect_emotional_patterns",
    # Exceptions
    "NimaError",
    "AffectVectorError",
    "InvalidAffectNameError",
    "AffectValueError",
    "BaselineValidationError",
    "StatePersistenceError",
    "ProfileNotFoundError",
    "EmotionDetectionError",
    "ArchetypeError",
    "UnknownArchetypeError",
    # Dynamic Affect System
    "DynamicAffectSystem",
    "AffectVector",
    "get_affect_system",
    "get_current_affect",
    "process_emotional_input",
    "AFFECTS",
    "AFFECT_INDEX",
    "DEFAULT_BASELINE",
    "PersonalityManager",
    "get_profile",
    "list_profiles",
    "map_emotions_to_affects",
    "detect_affect_from_text",
    "GenericResponseModulator",
    "ResponseGuidance",
    "modulate_response",
    # Archetypes
    "ARCHETYPES",
    "get_archetype",
    "list_archetypes",
    "baseline_from_archetype",
    "baseline_from_description",
]
