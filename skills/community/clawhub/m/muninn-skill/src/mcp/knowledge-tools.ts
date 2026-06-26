// Knowledge Graph MCP Tools - Add to server.ts tools array

export const KNOWLEDGE_TOOLS = [
  {
    name: 'knowledge_entities',
    description: 'List all entities in the knowledge graph with their types and mention counts.',
    inputSchema: {
      type: 'object',
      properties: {
        type: {
          type: 'string',
          enum: ['organization', 'person', 'project', 'technology', 'location'],
          description: 'Filter by entity type',
        },
        limit: {
          type: 'number',
          description: 'Maximum number of entities to return',
          default: 50
        }
      }
    }
  },
  {
    name: 'knowledge_relationships',
    description: 'Query relationships from the knowledge graph. Get all relationships for an entity, or filter by type.',
    inputSchema: {
      type: 'object',
      properties: {
        entity: {
          type: 'string',
          description: 'Entity name to get relationships for'
        },
        type: {
          type: 'string',
          enum: ['has_target', 'has_customer', 'uses', 'built_by', 'employs', 'has_priority', 'part_of', 'went_to', 'works_at', 'knows', 'has_interest', 'has_identity', 'has_plan', 'co_occurs_with'],
          description: 'Filter by relationship type'
        },
        direction: {
          type: 'string',
          enum: ['outgoing', 'incoming', 'both'],
          description: 'Relationship direction (default: both)',
          default: 'both'
        }
      }
    }
  },
  {
    name: 'knowledge_history',
    description: 'Get the temporal history of an entity\'s relationships. Shows how values changed over time.',
    inputSchema: {
      type: 'object',
      properties: {
        entity: {
          type: 'string',
          description: 'Entity name to get history for'
        },
        type: {
          type: 'string',
          description: 'Relationship type to track (e.g., has_target)',
        }
      },
      required: ['entity']
    }
  },
  {
    name: 'knowledge_contradictions',
    description: 'Find all contradictions in the knowledge graph where a newer relationship supersedes an older one.',
    inputSchema: {
      type: 'object',
      properties: {}
    }
  }
];

// Handler functions for knowledge graph tools
export const KNOWLEDGE_HANDLERS = {
  knowledge_entities: (store: any, args: any) => {
    const entityStore = store.getEntityStore();
    const { type, limit = 50 } = args;
    
    let entities = type 
      ? entityStore.getByType(type)
      : entityStore.getAll();
    
    entities = entities.slice(0, limit);
    
    return {
      count: entities.length,
      entities: entities.map((e: any) => ({
        id: e.id,
        name: e.name,
        type: e.type,
        mentions: e.mentions,
        aliases: e.aliases,
        firstSeen: e.firstSeen,
        lastSeen: e.lastSeen
      }))
    };
  },

  knowledge_relationships: (store: any, args: any) => {
    const relationshipStore = store.getRelationshipStore();
    const entityStore = store.getEntityStore();
    const { entity, type, direction = 'both' } = args;
    
    let relationships: any[] = [];
    
    if (entity) {
      const entityRecord = entityStore.findEntity(entity);
      if (!entityRecord) {
        return { count: 0, relationships: [], error: 'Entity not found' };
      }
      
      const entityId = entityRecord.id;
      
      if (direction === 'outgoing' || direction === 'both') {
        relationships.push(...relationshipStore.getBySource(entityId));
      }
      if (direction === 'incoming' || direction === 'both') {
        relationships.push(...relationshipStore.getByTarget(entityId));
      }
    } else if (type) {
      relationships = relationshipStore.getByType(type);
    } else {
      relationships = relationshipStore.getAll();
    }
    
    // Resolve entity names
    const resolved = relationships.map((rel: any) => {
      const sourceEntity = entityStore.getById(rel.source);
      const targetEntity = entityStore.getById(rel.target);
      
      return {
        id: rel.id,
        source: sourceEntity?.name || rel.source,
        target: targetEntity?.name || rel.target,
        type: rel.type,
        value: rel.value,
        timestamp: rel.timestamp,
        confidence: rel.confidence,
        supersededBy: rel.supersededBy
      };
    });
    
    return {
      count: resolved.length,
      relationships: resolved
    };
  },

  knowledge_history: (store: any, args: any) => {
    const relationshipStore = store.getRelationshipStore();
    const entityStore = store.getEntityStore();
    const { entity, type } = args;
    
    const entityRecord = entityStore.findEntity(entity);
    if (!entityRecord) {
      return { count: 0, history: [], error: 'Entity not found' };
    }
    
    const history = relationshipStore.getHistory(entityRecord.id, type);
    
    const resolved = history.map((rel: any) => {
      const sourceEntity = entityStore.getById(rel.source);
      const targetEntity = entityStore.getById(rel.target);
      
      return {
        timestamp: rel.timestamp,
        source: sourceEntity?.name || rel.source,
        target: targetEntity?.name || rel.target,
        type: rel.type,
        value: rel.value,
        confidence: rel.confidence,
        supersededBy: rel.supersededBy
      };
    });
    
    return {
      entity: entityRecord.name,
      count: resolved.length,
      history: resolved
    };
  },

  knowledge_contradictions: (store: any, args: any) => {
    const relationshipStore = store.getRelationshipStore();
    const entityStore = store.getEntityStore();
    
    const contradictions = relationshipStore.getContradictions();
    
    const resolved = contradictions.map(({ current, superseded }: any) => {
      const currentSource = entityStore.getById(current.source);
      const supersededSource = entityStore.getById(superseded.source);
      
      return {
        entity: currentSource?.name || current.source,
        type: current.type,
        oldValue: superseded.value,
        oldTimestamp: superseded.timestamp,
        newValue: current.value,
        newTimestamp: current.timestamp
      };
    });
    
    return {
      count: resolved.length,
      contradictions: resolved
    };
  }
};
