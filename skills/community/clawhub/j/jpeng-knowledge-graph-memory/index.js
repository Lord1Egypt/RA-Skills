/**
 * Knowledge Graph Memory - Long-term memory with concept drift handling
 * 
 * Features:
 * - Knowledge graph with nodes and edges
 * - Concept drift detection using statistical methods
 * - Temporal reasoning and queries
 * - Memory consolidation and forgetting
 * 
 * Usage:
 *   const { KnowledgeGraph, Concept, Memory } = require('./skills/knowledge-graph-memory');
 *   const kg = new KnowledgeGraph();
 *   kg.addConcept('AI', { category: 'technology' });
 *   kg.link('AI', 'Machine Learning', 'includes');
 */

/**
 * Concept drift detection methods
 */
const DriftMethod = {
  ADWIN: 'adwin',           // Adaptive Windowing
  DDM: 'ddm',               // Drift Detection Method
  EDDM: 'eddm',             // Early Drift Detection Method
  PAGE_HINKLEY: 'page_hinkley',
  STATISTICAL: 'statistical' // Simple statistical drift
};

/**
 * Node types in the knowledge graph
 */
const NodeType = {
  CONCEPT: 'concept',
  ENTITY: 'entity',
  EVENT: 'event',
  FACT: 'fact',
  RELATION: 'relation'
};

/**
 * Edge types for relationships
 */
const EdgeType = {
  IS_A: 'is_a',
  HAS_A: 'has_a',
  RELATED_TO: 'related_to',
  CAUSES: 'causes',
  PRECEDES: 'precedes',
  INCLUDES: 'includes',
  SIMILAR_TO: 'similar_to',
  DERIVED_FROM: 'derived_from'
};

/**
 * Concept node in the knowledge graph
 */
class Concept {
  constructor(options = {}) {
    this.id = options.id || `concept_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.name = options.name || this.id;
    this.type = options.type || NodeType.CONCEPT;
    this.properties = options.properties || {};
    this.createdAt = options.createdAt || new Date().toISOString();
    this.updatedAt = options.updatedAt || this.createdAt;
    this.accessCount = options.accessCount || 0;
    this.lastAccessed = options.lastAccessed || this.createdAt;
    this.importance = options.importance || 0.5;
    this.version = options.version || 1;
    this.history = options.history || []; // Track concept evolution
  }

  access() {
    this.accessCount++;
    this.lastAccessed = new Date().toISOString();
    return this;
  }

  update(properties) {
    // Record history before update
    this.history.push({
      version: this.version,
      properties: { ...this.properties },
      updatedAt: this.updatedAt
    });
    
    this.properties = { ...this.properties, ...properties };
    this.updatedAt = new Date().toISOString();
    this.version++;
    return this;
  }
}

/**
 * Edge representing a relationship between concepts
 */
class Edge {
  constructor(options = {}) {
    this.id = options.id || `edge_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.source = options.source;
    this.target = options.target;
    this.type = options.type || EdgeType.RELATED_TO;
    this.weight = options.weight || 1.0;
    this.properties = options.properties || {};
    this.createdAt = options.createdAt || new Date().toISOString();
    this.confidence = options.confidence || 1.0;
  }
}

/**
 * Concept Drift Detector
 */
class DriftDetector {
  constructor(options = {}) {
    this.method = options.method || DriftMethod.STATISTICAL;
    this.windowSize = options.windowSize || 100;
    this.threshold = options.threshold || 2.0; // Standard deviations
    this.minSamples = options.minSamples || 30;
    
    // Statistics tracking
    this.samples = [];
    this.mean = 0;
    this.variance = 0;
    this.driftDetected = false;
    this.warningLevel = false;
  }

  addSample(value) {
    this.samples.push({
      value,
      timestamp: Date.now()
    });

    // Maintain window size
    if (this.samples.length > this.windowSize) {
      this.samples.shift();
    }

    return this.detect();
  }

  detect() {
    if (this.samples.length < this.minSamples) {
      return { drift: false, warning: false };
    }

    const values = this.samples.map(s => s.value);
    const n = values.length;
    
    // Calculate current statistics
    const currentMean = values.reduce((a, b) => a + b, 0) / n;
    const currentVariance = values.reduce((a, b) => a + Math.pow(b - currentMean, 2), 0) / n;
    const stdDev = Math.sqrt(currentVariance);

    // Compare with historical statistics
    if (this.mean > 0) {
      const zScore = Math.abs(currentMean - this.mean) / (stdDev || 1);
      
      this.warningLevel = zScore > this.threshold * 0.7;
      this.driftDetected = zScore > this.threshold;
    }

    // Update historical statistics
    this.mean = currentMean;
    this.variance = currentVariance;

    return {
      drift: this.driftDetected,
      warning: this.warningLevel,
      mean: this.mean,
      stdDev,
      sampleCount: n
    };
  }

  reset() {
    this.samples = [];
    this.mean = 0;
    this.variance = 0;
    this.driftDetected = false;
    this.warningLevel = false;
  }
}

/**
 * Temporal Reasoner for time-based queries
 */
class TemporalReasoner {
  constructor() {
    this.timeline = [];
  }

  addEvent(event) {
    this.timeline.push({
      ...event,
      timestamp: event.timestamp || new Date().toISOString()
    });
    
    // Sort by timestamp
    this.timeline.sort((a, b) => 
      new Date(a.timestamp) - new Date(b.timestamp)
    );
  }

  getEventsInRange(start, end) {
    const startTime = new Date(start).getTime();
    const endTime = new Date(end).getTime();
    
    return this.timeline.filter(e => {
      const t = new Date(e.timestamp).getTime();
      return t >= startTime && t <= endTime;
    });
  }

  getEventsBefore(time) {
    const targetTime = new Date(time).getTime();
    return this.timeline.filter(e => 
      new Date(e.timestamp).getTime() < targetTime
    );
  }

  getEventsAfter(time) {
    const targetTime = new Date(time).getTime();
    return this.timeline.filter(e => 
      new Date(e.timestamp).getTime() > targetTime
    );
  }

  getRecentEvents(count = 10) {
    return this.timeline.slice(-count);
  }

  getEventSequence(conceptId) {
    return this.timeline.filter(e => 
      e.conceptId === conceptId || e.relatedConcepts?.includes(conceptId)
    );
  }
}

/**
 * Knowledge Graph - Main class
 */
class KnowledgeGraph {
  constructor(options = {}) {
    this.nodes = new Map();
    this.edges = new Map();
    this.adjacency = new Map(); // Adjacency list for fast lookups
    this.driftDetector = new DriftDetector(options.driftDetection || {});
    this.temporalReasoner = new TemporalReasoner();
    this.indexCounter = 0;
    
    // Memory management
    this.maxNodes = options.maxNodes || 10000;
    this.consolidationThreshold = options.consolidationThreshold || 0.1;
    this.forgettingFactor = options.forgettingFactor || 0.95;
  }

  /**
   * Add a concept to the graph
   */
  addConcept(name, properties = {}) {
    const concept = new Concept({
      name,
      properties,
      id: properties.id || `concept_${++this.indexCounter}`
    });
    
    this.nodes.set(concept.id, concept);
    this.adjacency.set(concept.id, new Set());
    
    // Record in temporal reasoner
    this.temporalReasoner.addEvent({
      type: 'concept_added',
      conceptId: concept.id,
      name: concept.name
    });
    
    return concept;
  }

  /**
   * Get a concept by ID or name
   */
  getConcept(idOrName) {
    // Try by ID first
    let concept = this.nodes.get(idOrName);
    if (concept) return concept.access();
    
    // Try by name
    for (const [id, node] of this.nodes) {
      if (node.name === idOrName) {
        return node.access();
      }
    }
    
    return null;
  }

  /**
   * Link two concepts with an edge
   */
  link(sourceId, targetId, type = EdgeType.RELATED_TO, properties = {}) {
    const source = this.getConcept(sourceId);
    const target = this.getConcept(targetId);
    
    if (!source || !target) {
      throw new Error('Source or target concept not found');
    }
    
    const edge = new Edge({
      source: source.id,
      target: target.id,
      type,
      properties
    });
    
    this.edges.set(edge.id, edge);
    
    // Update adjacency list
    this.adjacency.get(source.id).add(edge.id);
    
    // Record event
    this.temporalReasoner.addEvent({
      type: 'link_created',
      sourceId: source.id,
      targetId: target.id,
      edgeType: type
    });
    
    return edge;
  }

  /**
   * Get related concepts
   */
  getRelated(conceptId, edgeType = null) {
    const concept = this.getConcept(conceptId);
    if (!concept) return [];
    
    const related = [];
    const edgeIds = this.adjacency.get(concept.id) || new Set();
    
    for (const edgeId of edgeIds) {
      const edge = this.edges.get(edgeId);
      if (edge && (!edgeType || edge.type === edgeType)) {
        const target = this.nodes.get(edge.target);
        if (target) {
          related.push({ concept: target, edge });
        }
      }
    }
    
    return related;
  }

  /**
   * Find path between two concepts
   */
  findPath(startId, endId, maxDepth = 5) {
    const start = this.getConcept(startId);
    const end = this.getConcept(endId);
    
    if (!start || !end) return null;
    
    // BFS
    const queue = [{ id: start.id, path: [start.id] }];
    const visited = new Set([start.id]);
    
    while (queue.length > 0 && visited.size < maxDepth * 10) {
      const { id, path } = queue.shift();
      
      if (id === end.id) {
        return path.map(id => this.nodes.get(id));
      }
      
      const related = this.getRelated(id);
      for (const { concept } of related) {
        if (!visited.has(concept.id)) {
          visited.add(concept.id);
          queue.push({ 
            id: concept.id, 
            path: [...path, concept.id] 
          });
        }
      }
    }
    
    return null;
  }

  /**
   * Detect concept drift for a concept
   */
  detectDrift(conceptId) {
    const concept = this.getConcept(conceptId);
    if (!concept) return null;
    
    // Use property changes as drift indicator
    const historyLength = concept.history.length;
    if (historyLength > 0) {
      const driftResult = this.driftDetector.addSample(historyLength);
      
      if (driftResult.drift) {
        this.temporalReasoner.addEvent({
          type: 'drift_detected',
          conceptId: concept.id,
          driftScore: driftResult.mean
        });
      }
      
      return driftResult;
    }
    
    return { drift: false, warning: false };
  }

  /**
   * Search concepts by properties
   */
  search(query) {
    const results = [];
    
    for (const [id, concept] of this.nodes) {
      let matches = true;
      
      // Check name
      if (query.name && !concept.name.toLowerCase().includes(query.name.toLowerCase())) {
        matches = false;
      }
      
      // Check type
      if (query.type && concept.type !== query.type) {
        matches = false;
      }
      
      // Check properties
      if (query.properties) {
        for (const [key, value] of Object.entries(query.properties)) {
          if (concept.properties[key] !== value) {
            matches = false;
            break;
          }
        }
      }
      
      if (matches) {
        results.push(concept);
      }
    }
    
    return results;
  }

  /**
   * Consolidate memory - remove low-importance, rarely accessed concepts
   */
  consolidate() {
    const toRemove = [];
    const now = Date.now();
    
    for (const [id, concept] of this.nodes) {
      const lastAccessed = new Date(concept.lastAccessed).getTime();
      const age = (now - lastAccessed) / (1000 * 60 * 60 * 24); // Days
      
      // Calculate importance score
      const importanceScore = 
        concept.importance * 0.4 +
        (concept.accessCount / 100) * 0.3 +
        (1 / (age + 1)) * 0.3;
      
      if (importanceScore < this.consolidationThreshold) {
        toRemove.push(id);
      }
    }
    
    // Remove low-importance concepts
    for (const id of toRemove) {
      this.removeConcept(id);
    }
    
    return toRemove.length;
  }

  /**
   * Remove a concept and its edges
   */
  removeConcept(id) {
    const concept = this.nodes.get(id);
    if (!concept) return false;
    
    // Remove edges
    const edgeIds = this.adjacency.get(id) || new Set();
    for (const edgeId of edgeIds) {
      this.edges.delete(edgeId);
    }
    
    // Remove from adjacency
    this.adjacency.delete(id);
    
    // Remove node
    this.nodes.delete(id);
    
    return true;
  }

  /**
   * Get graph statistics
   */
  getStats() {
    return {
      nodeCount: this.nodes.size,
      edgeCount: this.edges.size,
      avgConnections: this.edges.size / (this.nodes.size || 1),
      eventCount: this.temporalReasoner.timeline.length
    };
  }

  /**
   * Export graph to JSON
   */
  toJSON() {
    return {
      nodes: Array.from(this.nodes.values()),
      edges: Array.from(this.edges.values()),
      events: this.temporalReasoner.timeline
    };
  }

  /**
   * Import graph from JSON
   */
  static fromJSON(data) {
    const kg = new KnowledgeGraph();
    
    for (const node of data.nodes || []) {
      const concept = new Concept(node);
      kg.nodes.set(concept.id, concept);
      kg.adjacency.set(concept.id, new Set());
    }
    
    for (const edge of data.edges || []) {
      const e = new Edge(edge);
      kg.edges.set(e.id, e);
      kg.adjacency.get(e.source)?.add(e.id);
    }
    
    for (const event of data.events || []) {
      kg.temporalReasoner.addEvent(event);
    }
    
    return kg;
  }
}

/**
 * Memory manager for long-term storage
 */
class Memory {
  constructor(options = {}) {
    this.knowledgeGraph = new KnowledgeGraph(options);
    this.shortTermMemory = new Map();
    this.shortTermMaxSize = options.shortTermMaxSize || 100;
    this.consolidationInterval = options.consolidationInterval || 3600000; // 1 hour
  }

  /**
   * Store a memory
   */
  remember(key, value, options = {}) {
    // Store in short-term memory
    this.shortTermMemory.set(key, {
      value,
      createdAt: new Date().toISOString(),
      accessCount: 0,
      importance: options.importance || 0.5
    });
    
    // Maintain short-term memory size
    if (this.shortTermMemory.size > this.shortTermMaxSize) {
      this._evictFromShortTerm();
    }
    
    // Also store in knowledge graph if it's a concept
    if (options.isConcept) {
      this.knowledgeGraph.addConcept(key, value);
    }
    
    return true;
  }

  /**
   * Recall a memory
   */
  recall(key) {
    // Check short-term memory first
    const stm = this.shortTermMemory.get(key);
    if (stm) {
      stm.accessCount++;
      return stm.value;
    }
    
    // Check knowledge graph
    const concept = this.knowledgeGraph.getConcept(key);
    if (concept) {
      return concept.properties;
    }
    
    return null;
  }

  /**
   * Forget a memory
   */
  forget(key) {
    this.shortTermMemory.delete(key);
    this.knowledgeGraph.removeConcept(key);
    return true;
  }

  /**
   * Consolidate short-term to long-term memory
   */
  consolidate() {
    const toPromote = [];
    
    for (const [key, entry] of this.shortTermMemory) {
      if (entry.accessCount >= 3 || entry.importance >= 0.7) {
        toPromote.push({ key, entry });
      }
    }
    
    for (const { key, entry } of toPromote) {
      this.knowledgeGraph.addConcept(key, entry.properties || { value: entry.value });
      this.shortTermMemory.delete(key);
    }
    
    // Also consolidate knowledge graph
    const removed = this.knowledgeGraph.consolidate();
    
    return { promoted: toPromote.length, removed };
  }

  /**
   * Evict least recently used from short-term memory
   */
  _evictFromShortTerm() {
    let oldest = null;
    let oldestKey = null;
    
    for (const [key, entry] of this.shortTermMemory) {
      if (!oldest || new Date(entry.createdAt) < new Date(oldest.createdAt)) {
        oldest = entry;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      this.shortTermMemory.delete(oldestKey);
    }
  }
}

module.exports = {
  // Main classes
  KnowledgeGraph,
  Concept,
  Edge,
  Memory,
  DriftDetector,
  TemporalReasoner,
  
  // Constants
  NodeType,
  EdgeType,
  DriftMethod
};
