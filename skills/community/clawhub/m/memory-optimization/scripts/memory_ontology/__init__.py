"""
Memory Ontology Package

Provides knowledge graph management for agent memory with:
- Entity CRUD operations with strength/decay tracking
- Relation management
- Schema validation
- Phase 6 Value-Aware Retrieval
- Phase 8 Write-Time Gating
- Cold storage archiving

Backward-compatible re-exports for existing imports.
"""

# Re-export from config module
from .config import (
    load_env_file,
    SCRIPT_DIR,
    WORKSPACE_ROOT,
    ONTOLOGY_DIR,
    GRAPH_FILE,
    SCHEMA_FILE,
    BASE_SCHEMA_FILE,
    DECAY_RATES,
    DECAY_THRESHOLD,
    ACCESS_DECAY_THRESHOLD_HOURS,
    LOCK_TIMEOUT_SECONDS,
)

# Re-export from schema module
from .schema import (
    load_schema,
    validate_entity,
)

# Re-export from storage module
from .storage import (
    _acquire_lock_with_timeout,
    _write_to_graph,
    ensure_ontology_dir,
    load_all_entities,
    load_all_relations,
    compact_graph,
)

# Re-export from entity_ops module
from .entity_ops import (
    generate_entity_id,
    get_default_decay_rate,
    add_memory_evolution_fields,
    create_entity,
    _read_entity_from_graph,
    get_entity,
    refresh_entity_strength,
    apply_decay_to_entity,
    mark_entity_consolidated,
    get_entities_by_strength,
    get_entities_by_type,
    get_strength_distribution,
)

# Re-export from relation_ops module
from .relation_ops import (
    create_relation,
    get_related_entities,
)

# Re-export from query module
from .query import (
    query_entities,
    validate_graph,
    export_to_markdown,
)

# Re-export from gating module
from .gating import (
    get_or_create_source,
    update_source_reliability,
    get_default_gating_policy,
    get_all_active_entities,
    get_all_archived_entities,
)

# Re-export from archived_memory module
from .archived_memory import (
    archive_entity_to_cold_storage,
    recover_entity_from_cold_storage,
    list_cold_storage_entities,
)

# Re-export from cli module
from .cli import (
    print_entity,
    main,
)

# Re-export from value_score module (Phase 6)
from .value_score import (
    ValueScoreCalculator,
    value_aware_sort,
    DEFAULT_WEIGHTS,
)

# Re-export from retrieval module (Phase 6)
from .retrieval import (
    ValueAwareRetriever,
    retrieve_value_aware,
)

__all__ = [
    # config
    'load_env_file',
    'SCRIPT_DIR',
    'WORKSPACE_ROOT',
    'ONTOLOGY_DIR',
    'GRAPH_FILE',
    'SCHEMA_FILE',
    'BASE_SCHEMA_FILE',
    'DECAY_RATES',
    'DECAY_THRESHOLD',
    'ACCESS_DECAY_THRESHOLD_HOURS',
    'LOCK_TIMEOUT_SECONDS',
    # schema
    'load_schema',
    'validate_entity',
    # storage
    '_acquire_lock_with_timeout',
    '_write_to_graph',
    'ensure_ontology_dir',
    'load_all_entities',
    'load_all_relations',
    'compact_graph',
    # entity_ops
    'generate_entity_id',
    'get_default_decay_rate',
    'add_memory_evolution_fields',
    'create_entity',
    '_read_entity_from_graph',
    'get_entity',
    'refresh_entity_strength',
    'apply_decay_to_entity',
    'mark_entity_consolidated',
    'get_entities_by_strength',
    'get_entities_by_type',
    'get_strength_distribution',
    # relation_ops
    'create_relation',
    'get_related_entities',
    # query
    'query_entities',
    'validate_graph',
    'export_to_markdown',
    # gating
    'get_or_create_source',
    'update_source_reliability',
    'get_default_gating_policy',
    'get_all_active_entities',
    'get_all_archived_entities',
    # archived_memory
    'archive_entity_to_cold_storage',
    'recover_entity_from_cold_storage',
    'list_cold_storage_entities',
    # cli
    'print_entity',
    'main',
    # value_score (Phase 6)
    'ValueScoreCalculator',
    'value_aware_sort',
    'DEFAULT_WEIGHTS',
    # retrieval (Phase 6)
    'ValueAwareRetriever',
    'retrieve_value_aware',
]