#!/usr/bin/env python3
"""
Agent Memory Ontology Manager
知识图谱记忆管理工具

提供命令行接口用于创建、查询和管理 Agent 记忆实体

使用方法:
    python3 memory_ontology.py create --type Decision --props '{"title":"...","rationale":"..."}'
    python3 memory_ontology.py query --type Finding --tags "#memory"
    python3 memory_ontology.py relate --from find_001 --rel led_to_decision --to dec_001
    python3 memory_ontology.py validate

NOTE: This file is now a backward-compatible shim.
The actual implementation has been moved to the memory_ontology package.
"""

# Re-export all public API from the memory_ontology package for backward compatibility
from memory_ontology import (
    # config
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
    # schema
    load_schema,
    validate_entity,
    # storage
    _acquire_lock_with_timeout,
    _write_to_graph,
    ensure_ontology_dir,
    load_all_entities,
    load_all_relations,
    compact_graph,
    # entity_ops
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
    # relation_ops
    create_relation,
    get_related_entities,
    # query
    query_entities,
    validate_graph,
    export_to_markdown,
    # gating
    get_or_create_source,
    update_source_reliability,
    get_default_gating_policy,
    get_all_active_entities,
    get_all_archived_entities,
    # archived_memory
    archive_entity_to_cold_storage,
    recover_entity_from_cold_storage,
    list_cold_storage_entities,
    # cli
    print_entity,
    main,
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
]


if __name__ == '__main__':
    main()