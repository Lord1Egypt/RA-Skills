export interface KnowledgeNode {
    id: string;
    type: 'concept' | 'pattern' | 'solution' | 'lesson' | 'rule';
    content: string;
    tags: string[];
    expertSource?: string;
    confidence: number;
    usageCount: number;
    successRate: number;
    createdAt: number;
    updatedAt: number;
    metadata?: Record<string, any>;
}
export interface KnowledgeEdge {
    id: string;
    sourceId: string;
    targetId: string;
    relation: 'implies' | 'conflicts' | 'similar' | 'refines' | 'contradicts';
    weight: number;
    createdAt: number;
}
export interface KnowledgeGraph {
    nodes: Map<string, KnowledgeNode>;
    edges: Map<string, KnowledgeEdge>;
    indexByTag: Map<string, Set<string>>;
    indexByType: Map<string, Set<string>>;
    indexByExpert: Map<string, Set<string>>;
}
export interface Experience {
    id: string;
    taskType: string;
    context: string;
    actions: string[];
    outcome: 'success' | 'partial' | 'failure';
    outcomeDetails?: string;
    keyInsights: string[];
    expertId: string;
    timestamp: number;
    sessionId?: string;
    applicableDomains: string[];
}
export interface KnowledgeQuery {
    tags?: string[];
    types?: KnowledgeNode['type'][];
    expertId?: string;
    minConfidence?: number;
    minSuccessRate?: number;
    searchText?: string;
    limit?: number;
}
export interface KnowledgeStats {
    totalNodes: number;
    totalEdges: number;
    byType: Record<string, number>;
    byTag: Record<string, number>;
    averageConfidence: number;
    averageSuccessRate: number;
    topExperts: {
        expertId: string;
        count: number;
    }[];
}
export declare class AgentKnowledgeGraph {
    private graph;
    private storagePath?;
    constructor(storagePath?: string);
    /**
     * Add a new knowledge node to the graph.
     */
    addNode(node: Omit<KnowledgeNode, 'id' | 'createdAt' | 'updatedAt' | 'usageCount'>): string;
    /**
     * Update an existing node.
     */
    updateNode(id: string, updates: Partial<KnowledgeNode>): boolean;
    /**
     * Increment usage count for a node (when it's retrieved/applied).
     */
    touchNode(id: string): void;
    /**
     * Update success rate after outcome is known.
     */
    recordOutcome(id: string, success: boolean): void;
    /**
     * Get a node by ID.
     */
    getNode(id: string): KnowledgeNode | undefined;
    /**
     * Add a relationship between two nodes.
     */
    addEdge(edge: Omit<KnowledgeEdge, 'id' | 'createdAt'>): string | null;
    /**
     * Find edge between two nodes.
     */
    findEdge(sourceId: string, targetId: string): KnowledgeEdge | undefined;
    /**
     * Query knowledge based on multiple criteria.
     */
    query(criteria: KnowledgeQuery): KnowledgeNode[];
    /**
     * Find related knowledge (nodes connected via edges).
     */
    findRelated(nodeId: string, maxResults?: number): KnowledgeNode[];
    /**
     * Find conflicting knowledge.
     */
    findConflicts(nodeId: string): KnowledgeNode[];
    /**
     * Extract knowledge from an experience and add to graph.
     */
    integrateExperience(experience: Experience): string[];
    /**
     * Suggest knowledge for a task based on context.
     */
    suggestKnowledge(context: string, domains: string[]): KnowledgeNode[];
    /**
     * Get knowledge graph statistics.
     */
    getStats(): KnowledgeStats;
    /**
     * Export graph as JSON-serializable object.
     */
    export(): object;
    /**
     * Import graph from exported data.
     */
    import(data: {
        nodes: KnowledgeNode[];
        edges: KnowledgeEdge[];
    }): void;
}
export declare class ExperienceTracker {
    private experiences;
    private maxExperiences;
    private storagePath?;
    constructor(maxExperiences?: number, storagePath?: string);
    /**
     * Record a new experience.
     */
    record(experience: Omit<Experience, 'id' | 'timestamp'>): string;
    /**
     * Get recent experiences.
     */
    getRecent(limit?: number): Experience[];
    /**
     * Get experiences by outcome.
     */
    getByOutcome(outcome: Experience['outcome']): Experience[];
    /**
     * Get experiences by task type.
     */
    getByTaskType(taskType: string): Experience[];
    /**
     * Get experiences by expert.
     */
    getByExpert(expertId: string): Experience[];
    /**
     * Get experience statistics.
     */
    getStats(): {
        total: number;
        successRate: number;
        byTaskType: Record<string, number>;
        byExpert: Record<string, number>;
    };
}
export declare const knowledgeGraph: AgentKnowledgeGraph;
export declare const experienceTracker: ExperienceTracker;
export default AgentKnowledgeGraph;
//# sourceMappingURL=knowledge-graph.d.ts.map