// ============================================================================
// EO Agent Knowledge Graph - Phase 3.1: Agent Knowledge Sharing
//
// Implements cross-agent experience transfer, shared knowledge graph,
// and expert knowledge base synchronization.
// ============================================================================

// ============================================================================
// Types
// ============================================================================

export interface KnowledgeNode {
  id: string
  type: 'concept' | 'pattern' | 'solution' | 'lesson' | 'rule'
  content: string
  tags: string[]
  expertSource?: string      // which expert contributed this
  confidence: number         // 0-1, trust level
  usageCount: number         // times this knowledge was applied
  successRate: number        // 0-1, how often it worked
  createdAt: number
  updatedAt: number
  metadata?: Record<string, any>
}

export interface KnowledgeEdge {
  id: string
  sourceId: string
  targetId: string
  relation: 'implies' | 'conflicts' | 'similar' | 'refines' | 'contradicts'
  weight: number             // 0-1, strength of relation
  createdAt: number
}

export interface KnowledgeGraph {
  nodes: Map<string, KnowledgeNode>
  edges: Map<string, KnowledgeEdge>
  indexByTag: Map<string, Set<string>>    // tag -> nodeIds
  indexByType: Map<string, Set<string>>   // type -> nodeIds
  indexByExpert: Map<string, Set<string>> // expert -> nodeIds
}

export interface Experience {
  id: string
  taskType: string
  context: string
  actions: string[]
  outcome: 'success' | 'partial' | 'failure'
  outcomeDetails?: string
  keyInsights: string[]
  expertId: string
  timestamp: number
  sessionId?: string
  applicableDomains: string[]
}

export interface KnowledgeQuery {
  tags?: string[]
  types?: KnowledgeNode['type'][]
  expertId?: string
  minConfidence?: number
  minSuccessRate?: number
  searchText?: string
  limit?: number
}

export interface KnowledgeStats {
  totalNodes: number
  totalEdges: number
  byType: Record<string, number>
  byTag: Record<string, number>
  averageConfidence: number
  averageSuccessRate: number
  topExperts: { expertId: string; count: number }[]
}

// ============================================================================
// Knowledge Graph Core
// ============================================================================

export class AgentKnowledgeGraph {
  private graph: KnowledgeGraph
  private storagePath?: string
  
  constructor(storagePath?: string) {
    this.graph = {
      nodes: new Map(),
      edges: new Map(),
      indexByTag: new Map(),
      indexByType: new Map(),
      indexByExpert: new Map(),
    }
    this.storagePath = storagePath
  }
  
  // ============================================================================
  // Node Operations
  // ============================================================================
  
  /**
   * Add a new knowledge node to the graph.
   */
  addNode(node: Omit<KnowledgeNode, 'id' | 'createdAt' | 'updatedAt' | 'usageCount'>): string {
    const id = node.type + '-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8)
    const now = Date.now()
    
    const fullNode: KnowledgeNode = {
      ...node,
      id,
      createdAt: now,
      updatedAt: now,
      usageCount: 0,
    }
    
    this.graph.nodes.set(id, fullNode)
    
    // Update indexes
    node.tags.forEach(tag => {
      if (!this.graph.indexByTag.has(tag)) {
        this.graph.indexByTag.set(tag, new Set())
      }
      this.graph.indexByTag.get(tag)!.add(id)
    })
    
    if (!this.graph.indexByType.has(node.type)) {
      this.graph.indexByType.set(node.type, new Set())
    }
    this.graph.indexByType.get(node.type)!.add(id)
    
    if (node.expertSource) {
      if (!this.graph.indexByExpert.has(node.expertSource)) {
        this.graph.indexByExpert.set(node.expertSource, new Set())
      }
      this.graph.indexByExpert.get(node.expertSource)!.add(id)
    }
    
    return id
  }
  
  /**
   * Update an existing node.
   */
  updateNode(id: string, updates: Partial<KnowledgeNode>): boolean {
    const node = this.graph.nodes.get(id)
    if (!node) return false
    
    const updated = { ...node, ...updates, id, updatedAt: Date.now() }
    this.graph.nodes.set(id, updated)
    return true
  }
  
  /**
   * Increment usage count for a node (when it's retrieved/applied).
   */
  touchNode(id: string): void {
    const node = this.graph.nodes.get(id)
    if (node) {
      node.usageCount++
      node.updatedAt = Date.now()
    }
  }
  
  /**
   * Update success rate after outcome is known.
   */
  recordOutcome(id: string, success: boolean): void {
    const node = this.graph.nodes.get(id)
    if (!node) return
    
    const totalOutcomes = node.usageCount
    if (totalOutcomes <= 1) {
      node.successRate = success ? 1 : 0
    } else {
      // Rolling average
      node.successRate = (node.successRate * (totalOutcomes - 1) + (success ? 1 : 0)) / totalOutcomes
    }
    node.updatedAt = Date.now()
  }
  
  /**
   * Get a node by ID.
   */
  getNode(id: string): KnowledgeNode | undefined {
    const node = this.graph.nodes.get(id)
    if (node) this.touchNode(id)
    return node
  }
  
  // ============================================================================
  // Edge Operations
  // ============================================================================
  
  /**
   * Add a relationship between two nodes.
   */
  addEdge(edge: Omit<KnowledgeEdge, 'id' | 'createdAt'>): string | null {
    const { sourceId, targetId } = edge
    
    // Verify nodes exist
    if (!this.graph.nodes.has(sourceId) || !this.graph.nodes.has(targetId)) {
      return null
    }
    
    // Check for duplicate edge
    const existingEdge = this.findEdge(sourceId, targetId)
    if (existingEdge) {
      // Update weight if edge already exists
      existingEdge.weight = Math.max(existingEdge.weight, edge.weight)
      return existingEdge.id
    }
    
    const id = 'edge-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6)
    const fullEdge: KnowledgeEdge = {
      ...edge,
      id,
      createdAt: Date.now(),
    }
    
    this.graph.edges.set(id, fullEdge)
    return id
  }
  
  /**
   * Find edge between two nodes.
   */
  findEdge(sourceId: string, targetId: string): KnowledgeEdge | undefined {
    return Array.from(this.graph.edges.values()).find(
      e => (e.sourceId === sourceId && e.targetId === targetId) ||
           (e.sourceId === targetId && e.targetId === sourceId)
    )
  }
  
  // ============================================================================
  // Query Operations
  // ============================================================================
  
  /**
   * Query knowledge based on multiple criteria.
   */
  query(criteria: KnowledgeQuery): KnowledgeNode[] {
    let results = Array.from(this.graph.nodes.values())
    
    if (criteria.tags && criteria.tags.length > 0) {
      const tagMatches = new Set<string>()
      criteria.tags.forEach(tag => {
        const nodeIds = this.graph.indexByTag.get(tag)
        if (nodeIds) {
          nodeIds.forEach(id => tagMatches.add(id))
        }
      })
      results = results.filter(n => tagMatches.has(n.id))
    }
    
    if (criteria.types && criteria.types.length > 0) {
      results = results.filter(n => criteria.types!.includes(n.type))
    }
    
    if (criteria.expertId) {
      const expertNodes = this.graph.indexByExpert.get(criteria.expertId)
      if (expertNodes) {
        results = results.filter(n => expertNodes.has(n.id))
      }
    }
    
    if (criteria.minConfidence !== undefined) {
      results = results.filter(n => n.confidence >= criteria.minConfidence!)
    }
    
    if (criteria.minSuccessRate !== undefined) {
      results = results.filter(n => n.successRate >= criteria.minSuccessRate!)
    }
    
    if (criteria.searchText) {
      const search = criteria.searchText.toLowerCase()
      results = results.filter(n => 
        n.content.toLowerCase().includes(search) ||
        n.tags.some(t => t.toLowerCase().includes(search))
      )
    }
    
    // Sort by relevance (confidence * usage * successRate)
    results.sort((a, b) => {
      const scoreA = a.confidence * (1 + Math.log(a.usageCount + 1)) * a.successRate
      const scoreB = b.confidence * (1 + Math.log(b.usageCount + 1)) * b.successRate
      return scoreB - scoreA
    })
    
    return criteria.limit ? results.slice(0, criteria.limit) : results
  }
  
  /**
   * Find related knowledge (nodes connected via edges).
   */
  findRelated(nodeId: string, maxResults = 5): KnowledgeNode[] {
    const relatedIds = new Set<string>()
    
    this.graph.edges.forEach(edge => {
      if (edge.sourceId === nodeId) relatedIds.add(edge.targetId)
      if (edge.targetId === nodeId) relatedIds.add(edge.sourceId)
    })
    
    return Array.from(relatedIds)
      .map(id => this.graph.nodes.get(id))
      .filter((n): n is KnowledgeNode => n !== undefined)
      .sort((a, b) => b.confidence - a.confidence)
      .slice(0, maxResults)
  }
  
  /**
   * Find conflicting knowledge.
   */
  findConflicts(nodeId: string): KnowledgeNode[] {
    const conflicts: KnowledgeNode[] = []
    
    this.graph.edges.forEach(edge => {
      if (edge.relation === 'conflicts' || edge.relation === 'contradicts') {
        if (edge.sourceId === nodeId) {
          const target = this.graph.nodes.get(edge.targetId)
          if (target) conflicts.push(target)
        }
        if (edge.targetId === nodeId) {
          const source = this.graph.nodes.get(edge.sourceId)
          if (source) conflicts.push(source)
        }
      }
    })
    
    return conflicts
  }
  
  // ============================================================================
  // Experience Integration
  // ============================================================================
  
  /**
   * Extract knowledge from an experience and add to graph.
   */
  integrateExperience(experience: Experience): string[] {
    const nodeIds: string[] = []
    
    // Add each key insight as a knowledge node
    experience.keyInsights.forEach(insight => {
      const nodeId = this.addNode({
        type: 'lesson',
        content: insight,
        tags: [...experience.applicableDomains, experience.taskType],
        expertSource: experience.expertId,
        confidence: experience.outcome === 'success' ? 0.8 : 
                    experience.outcome === 'partial' ? 0.5 : 0.3,
        successRate: experience.outcome === 'success' ? 1 :
                    experience.outcome === 'partial' ? 0.5 : 0,
      })
      nodeIds.push(nodeId)
    })
    
    return nodeIds
  }
  
  /**
   * Suggest knowledge for a task based on context.
   */
  suggestKnowledge(context: string, domains: string[]): KnowledgeNode[] {
    // First try exact domain match
    let suggestions = this.query({
      tags: domains,
      minConfidence: 0.5,
      minSuccessRate: 0.5,
      limit: 5,
    })
    
    // If not enough, broaden search
    if (suggestions.length < 3) {
      const broader = this.query({
        searchText: context,
        minConfidence: 0.4,
        limit: 5,
      })
      suggestions = [...suggestions, ...broader].slice(0, 5)
    }
    
    return suggestions
  }
  
  // ============================================================================
  // Statistics & Export
  // ============================================================================
  
  /**
   * Get knowledge graph statistics.
   */
  getStats(): KnowledgeStats {
    const nodes = Array.from(this.graph.nodes.values())
    const edges = Array.from(this.graph.edges.values())
    
    const byType: Record<string, number> = {}
    const byTag: Record<string, number> = {}
    const expertCounts: Record<string, number> = {}
    
    nodes.forEach(node => {
      byType[node.type] = (byType[node.type] || 0) + 1
      node.tags.forEach(tag => {
        byTag[tag] = (byTag[tag] || 0) + 1
      })
      if (node.expertSource) {
        expertCounts[node.expertSource] = (expertCounts[node.expertSource] || 0) + 1
      }
    })
    
    const avgConfidence = nodes.length > 0 
      ? nodes.reduce((sum, n) => sum + n.confidence, 0) / nodes.length 
      : 0
    
    const avgSuccessRate = nodes.length > 0 
      ? nodes.reduce((sum, n) => sum + n.successRate, 0) / nodes.length 
      : 0
    
    const topExperts = Object.entries(expertCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([expertId, count]) => ({ expertId, count }))
    
    return {
      totalNodes: nodes.length,
      totalEdges: edges.length,
      byType,
      byTag,
      averageConfidence: avgConfidence,
      averageSuccessRate: avgSuccessRate,
      topExperts,
    }
  }
  
  /**
   * Export graph as JSON-serializable object.
   */
  export(): object {
    return {
      nodes: Array.from(this.graph.nodes.values()),
      edges: Array.from(this.graph.edges.values()),
      exportedAt: Date.now(),
    }
  }
  
  /**
   * Import graph from exported data.
   */
  import(data: { nodes: KnowledgeNode[], edges: KnowledgeEdge[] }): void {
    this.graph.nodes.clear()
    this.graph.edges.clear()
    this.graph.indexByTag.clear()
    this.graph.indexByType.clear()
    this.graph.indexByExpert.clear()
    
    data.nodes.forEach(node => {
      this.graph.nodes.set(node.id, node)
      node.tags.forEach(tag => {
        if (!this.graph.indexByTag.has(tag)) {
          this.graph.indexByTag.set(tag, new Set())
        }
        this.graph.indexByTag.get(tag)!.add(node.id)
      })
      if (!this.graph.indexByType.has(node.type)) {
        this.graph.indexByType.set(node.type, new Set())
      }
      this.graph.indexByType.get(node.type)!.add(node.id)
      if (node.expertSource) {
        if (!this.graph.indexByExpert.has(node.expertSource)) {
          this.graph.indexByExpert.set(node.expertSource, new Set())
        }
        this.graph.indexByExpert.get(node.expertSource)!.add(node.id)
      }
    })
    
    data.edges.forEach(edge => {
      this.graph.edges.set(edge.id, edge)
    })
  }
}

// ============================================================================
// Experience Tracker - captures agent experiences for learning
// ============================================================================

export class ExperienceTracker {
  private experiences: Experience[] = []
  private maxExperiences: number
  private storagePath?: string
  
  constructor(maxExperiences = 1000, storagePath?: string) {
    this.maxExperiences = maxExperiences
    this.storagePath = storagePath
  }
  
  /**
   * Record a new experience.
   */
  record(experience: Omit<Experience, 'id' | 'timestamp'>): string {
    const id = 'exp-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6)
    
    const full: Experience = {
      ...experience,
      id,
      timestamp: Date.now(),
    }
    
    this.experiences.push(full)
    
    // Trim if over max
    if (this.experiences.length > this.maxExperiences) {
      this.experiences = this.experiences.slice(-this.maxExperiences)
    }
    
    return id
  }
  
  /**
   * Get recent experiences.
   */
  getRecent(limit = 10): Experience[] {
    return this.experiences.slice(-limit).reverse()
  }
  
  /**
   * Get experiences by outcome.
   */
  getByOutcome(outcome: Experience['outcome']): Experience[] {
    return this.experiences.filter(e => e.outcome === outcome)
  }
  
  /**
   * Get experiences by task type.
   */
  getByTaskType(taskType: string): Experience[] {
    return this.experiences.filter(e => e.taskType === taskType)
  }
  
  /**
   * Get experiences by expert.
   */
  getByExpert(expertId: string): Experience[] {
    return this.experiences.filter(e => e.expertId === expertId)
  }
  
  /**
   * Get experience statistics.
   */
  getStats(): {
    total: number
    successRate: number
    byTaskType: Record<string, number>
    byExpert: Record<string, number>
  } {
    const total = this.experiences.length
    const successCount = this.experiences.filter(e => e.outcome === 'success').length
    
    const byTaskType: Record<string, number> = {}
    const byExpert: Record<string, number> = {}
    
    this.experiences.forEach(e => {
      byTaskType[e.taskType] = (byTaskType[e.taskType] || 0) + 1
      byExpert[e.expertId] = (byExpert[e.expertId] || 0) + 1
    })
    
    return {
      total,
      successRate: total > 0 ? successCount / total : 0,
      byTaskType,
      byExpert,
    }
  }
}

// ============================================================================
// Global Instances
// ============================================================================

export const knowledgeGraph = new AgentKnowledgeGraph()
export const experienceTracker = new ExperienceTracker()

export default AgentKnowledgeGraph
