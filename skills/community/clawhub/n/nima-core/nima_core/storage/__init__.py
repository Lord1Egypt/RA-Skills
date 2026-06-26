"""
NIMA Core — Storage Layer
==========================

Provides cognitive memory primitives for ACT-R temporal decay,
Hebbian associative learning, Bayesian confidence scoring, and
protocol governance.

Modules
-------
temporal_decay
    ACT-R base-level activation scorer.  Tracks access history and
    computes activation scores using the formula B_i = ln(Σ t_j^(-d)).

hebbian_updater
    Hebbian edge-weight manager for the memory graph.  Strengthens
    associations between co-activated memories and decays unused edges.

bayesian_scorer
    Beta-distribution confidence scorer.  Tracks recall successes/failures
    and maintains a posterior confidence estimate per memory node.

protocol_store
    Constitutional governance layer.  Stores and retrieves ProtocolNodes:
    rules that govern agent reasoning, retrieved contextually by keyword/domain.

hyperbolic_memory
    Semantic memory using Poincaré ball embeddings for hierarchical
    knowledge representation (is-a relationships, taxonomies).

memory_graph
    SQLite-backed knowledge graph connecting memories through entities
    and relationships (people, topics, events, emotions).

memory_manager
    Auto-prune old data, enforce memory limits, archive old memories
    and manage storage quotas.

persistent_memory
    Binary format persistence with auto-save and date-based checkpoints
    for VSA memory systems.

migration_manager
    Database schema migration manager with version tracking and
    transaction-safe migrations.

Typical import::

    from nima_core.storage.hebbian_updater import HebbianGraphUpdater
    from nima_core.storage.protocol_store  import ProtocolStore, seed_protocols
    from nima_core.storage.hyperbolic_memory import HyperbolicSemanticMemory
    from nima_core.storage.memory_graph import MemoryGraph
    from nima_core.storage.memory_manager import MemoryManager
    from nima_core.storage.persistent_memory import PersistentMemory
"""

from .hebbian_updater import HebbianGraphUpdater
from .protocol_store  import ProtocolStore, seed_protocols
from .ladybug_guard   import ladybug_open_safe, ladybug_health_check, get_recovery_history
from .memory_graph import MemoryGraph
from .memory_manager import MemoryManager, MemoryLimits

# Optional: requires torch
try:
    from .persistent_memory import PersistentMemory, PersistenceConfig
    HAS_PERSISTENT = True
except ImportError:
    PersistentMemory = None  # type: ignore
    PersistenceConfig = None  # type: ignore
    HAS_PERSISTENT = False
try:
    from nima_core.experimental.hyperbolic_memory import HyperbolicSemanticMemory, build_default_hierarchy
    HAS_HYPERBOLIC = True
except ImportError:
    HyperbolicSemanticMemory = None  # type: ignore
    build_default_hierarchy = None  # type: ignore
    HAS_HYPERBOLIC = False

__all__ = [
    # Core scoring primitives
    "ACTRDecayScorer",
    "HebbianGraphUpdater",
    "BayesianScorer",
    # Protocol governance
    "ProtocolStore",
    "seed_protocols",
    # Ladybug safety
    "ladybug_open_safe",
    "ladybug_health_check",
    "get_recovery_history",
    # Memory architecture (forward-ported from lilu_core)
    "HyperbolicSemanticMemory",
    "build_default_hierarchy",
    "MemoryGraph",
    "MemoryManager",
    "MemoryLimits",
    "PersistentMemory",
    "PersistenceConfig",
]