function getDefaultStorageLayout() {
  return {
    store: 'memory/knowledge/knowledge_store.jsonl',
    links: 'memory/knowledge/knowledge_links.jsonl',
    index: 'memory/knowledge/knowledge_index.json',
    entities: 'memory/knowledge/entity_index.json',
  };
}

function describeRuntime() {
  return {
    name: 'openclaw-knowledge-runtime',
    layers: ['working', 'episodic', 'semantic', 'procedural', 'policy'],
    scopes: ['session', 'shared', 'published'],
    records: ['knowledge_entry', 'knowledge_link', 'entity'],
    retrieval: ['metadata_filter', 'keyword_overlap', 'typed_link_expansion', 'light_rerank'],
    adapterSurfaces: [
      'query_builder',
      'retrieval_selector',
      'task_ranker',
      'prompt_context',
      'write_back',
      'observability',
    ],
    outputs: [
      'knowledge_hits',
      'knowledge_bias_tags',
      'linked_entities',
      'linked_genes',
      'memory_layers',
      'knowledge_context_preview',
    ],
  };
}

module.exports = {
  describeRuntime,
  getDefaultStorageLayout,
};
