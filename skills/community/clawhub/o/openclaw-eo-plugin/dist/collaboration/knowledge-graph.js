// ============================================================================
// EO Agent Knowledge Graph - Phase 3.1: Agent Knowledge Sharing
//
// Implements cross-agent experience transfer, shared knowledge graph,
// and expert knowledge base synchronization.
// ============================================================================
// ============================================================================
// Knowledge Graph Core
// ============================================================================
export class AgentKnowledgeGraph {
    graph;
    storagePath;
    constructor(storagePath) {
        this.graph = {
            nodes: new Map(),
            edges: new Map(),
            indexByTag: new Map(),
            indexByType: new Map(),
            indexByExpert: new Map(),
        };
        this.storagePath = storagePath;
    }
    // ============================================================================
    // Node Operations
    // ============================================================================
    /**
     * Add a new knowledge node to the graph.
     */
    addNode(node) {
        const id = node.type + '-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
        const now = Date.now();
        const fullNode = {
            ...node,
            id,
            createdAt: now,
            updatedAt: now,
            usageCount: 0,
        };
        this.graph.nodes.set(id, fullNode);
        // Update indexes
        node.tags.forEach(tag => {
            if (!this.graph.indexByTag.has(tag)) {
                this.graph.indexByTag.set(tag, new Set());
            }
            this.graph.indexByTag.get(tag).add(id);
        });
        if (!this.graph.indexByType.has(node.type)) {
            this.graph.indexByType.set(node.type, new Set());
        }
        this.graph.indexByType.get(node.type).add(id);
        if (node.expertSource) {
            if (!this.graph.indexByExpert.has(node.expertSource)) {
                this.graph.indexByExpert.set(node.expertSource, new Set());
            }
            this.graph.indexByExpert.get(node.expertSource).add(id);
        }
        return id;
    }
    /**
     * Update an existing node.
     */
    updateNode(id, updates) {
        const node = this.graph.nodes.get(id);
        if (!node)
            return false;
        const updated = { ...node, ...updates, id, updatedAt: Date.now() };
        this.graph.nodes.set(id, updated);
        return true;
    }
    /**
     * Increment usage count for a node (when it's retrieved/applied).
     */
    touchNode(id) {
        const node = this.graph.nodes.get(id);
        if (node) {
            node.usageCount++;
            node.updatedAt = Date.now();
        }
    }
    /**
     * Update success rate after outcome is known.
     */
    recordOutcome(id, success) {
        const node = this.graph.nodes.get(id);
        if (!node)
            return;
        const totalOutcomes = node.usageCount;
        if (totalOutcomes <= 1) {
            node.successRate = success ? 1 : 0;
        }
        else {
            // Rolling average
            node.successRate = (node.successRate * (totalOutcomes - 1) + (success ? 1 : 0)) / totalOutcomes;
        }
        node.updatedAt = Date.now();
    }
    /**
     * Get a node by ID.
     */
    getNode(id) {
        const node = this.graph.nodes.get(id);
        if (node)
            this.touchNode(id);
        return node;
    }
    // ============================================================================
    // Edge Operations
    // ============================================================================
    /**
     * Add a relationship between two nodes.
     */
    addEdge(edge) {
        const { sourceId, targetId } = edge;
        // Verify nodes exist
        if (!this.graph.nodes.has(sourceId) || !this.graph.nodes.has(targetId)) {
            return null;
        }
        // Check for duplicate edge
        const existingEdge = this.findEdge(sourceId, targetId);
        if (existingEdge) {
            // Update weight if edge already exists
            existingEdge.weight = Math.max(existingEdge.weight, edge.weight);
            return existingEdge.id;
        }
        const id = 'edge-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
        const fullEdge = {
            ...edge,
            id,
            createdAt: Date.now(),
        };
        this.graph.edges.set(id, fullEdge);
        return id;
    }
    /**
     * Find edge between two nodes.
     */
    findEdge(sourceId, targetId) {
        return Array.from(this.graph.edges.values()).find(e => (e.sourceId === sourceId && e.targetId === targetId) ||
            (e.sourceId === targetId && e.targetId === sourceId));
    }
    // ============================================================================
    // Query Operations
    // ============================================================================
    /**
     * Query knowledge based on multiple criteria.
     */
    query(criteria) {
        let results = Array.from(this.graph.nodes.values());
        if (criteria.tags && criteria.tags.length > 0) {
            const tagMatches = new Set();
            criteria.tags.forEach(tag => {
                const nodeIds = this.graph.indexByTag.get(tag);
                if (nodeIds) {
                    nodeIds.forEach(id => tagMatches.add(id));
                }
            });
            results = results.filter(n => tagMatches.has(n.id));
        }
        if (criteria.types && criteria.types.length > 0) {
            results = results.filter(n => criteria.types.includes(n.type));
        }
        if (criteria.expertId) {
            const expertNodes = this.graph.indexByExpert.get(criteria.expertId);
            if (expertNodes) {
                results = results.filter(n => expertNodes.has(n.id));
            }
        }
        if (criteria.minConfidence !== undefined) {
            results = results.filter(n => n.confidence >= criteria.minConfidence);
        }
        if (criteria.minSuccessRate !== undefined) {
            results = results.filter(n => n.successRate >= criteria.minSuccessRate);
        }
        if (criteria.searchText) {
            const search = criteria.searchText.toLowerCase();
            results = results.filter(n => n.content.toLowerCase().includes(search) ||
                n.tags.some(t => t.toLowerCase().includes(search)));
        }
        // Sort by relevance (confidence * usage * successRate)
        results.sort((a, b) => {
            const scoreA = a.confidence * (1 + Math.log(a.usageCount + 1)) * a.successRate;
            const scoreB = b.confidence * (1 + Math.log(b.usageCount + 1)) * b.successRate;
            return scoreB - scoreA;
        });
        return criteria.limit ? results.slice(0, criteria.limit) : results;
    }
    /**
     * Find related knowledge (nodes connected via edges).
     */
    findRelated(nodeId, maxResults = 5) {
        const relatedIds = new Set();
        this.graph.edges.forEach(edge => {
            if (edge.sourceId === nodeId)
                relatedIds.add(edge.targetId);
            if (edge.targetId === nodeId)
                relatedIds.add(edge.sourceId);
        });
        return Array.from(relatedIds)
            .map(id => this.graph.nodes.get(id))
            .filter((n) => n !== undefined)
            .sort((a, b) => b.confidence - a.confidence)
            .slice(0, maxResults);
    }
    /**
     * Find conflicting knowledge.
     */
    findConflicts(nodeId) {
        const conflicts = [];
        this.graph.edges.forEach(edge => {
            if (edge.relation === 'conflicts' || edge.relation === 'contradicts') {
                if (edge.sourceId === nodeId) {
                    const target = this.graph.nodes.get(edge.targetId);
                    if (target)
                        conflicts.push(target);
                }
                if (edge.targetId === nodeId) {
                    const source = this.graph.nodes.get(edge.sourceId);
                    if (source)
                        conflicts.push(source);
                }
            }
        });
        return conflicts;
    }
    // ============================================================================
    // Experience Integration
    // ============================================================================
    /**
     * Extract knowledge from an experience and add to graph.
     */
    integrateExperience(experience) {
        const nodeIds = [];
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
            });
            nodeIds.push(nodeId);
        });
        return nodeIds;
    }
    /**
     * Suggest knowledge for a task based on context.
     */
    suggestKnowledge(context, domains) {
        // First try exact domain match
        let suggestions = this.query({
            tags: domains,
            minConfidence: 0.5,
            minSuccessRate: 0.5,
            limit: 5,
        });
        // If not enough, broaden search
        if (suggestions.length < 3) {
            const broader = this.query({
                searchText: context,
                minConfidence: 0.4,
                limit: 5,
            });
            suggestions = [...suggestions, ...broader].slice(0, 5);
        }
        return suggestions;
    }
    // ============================================================================
    // Statistics & Export
    // ============================================================================
    /**
     * Get knowledge graph statistics.
     */
    getStats() {
        const nodes = Array.from(this.graph.nodes.values());
        const edges = Array.from(this.graph.edges.values());
        const byType = {};
        const byTag = {};
        const expertCounts = {};
        nodes.forEach(node => {
            byType[node.type] = (byType[node.type] || 0) + 1;
            node.tags.forEach(tag => {
                byTag[tag] = (byTag[tag] || 0) + 1;
            });
            if (node.expertSource) {
                expertCounts[node.expertSource] = (expertCounts[node.expertSource] || 0) + 1;
            }
        });
        const avgConfidence = nodes.length > 0
            ? nodes.reduce((sum, n) => sum + n.confidence, 0) / nodes.length
            : 0;
        const avgSuccessRate = nodes.length > 0
            ? nodes.reduce((sum, n) => sum + n.successRate, 0) / nodes.length
            : 0;
        const topExperts = Object.entries(expertCounts)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([expertId, count]) => ({ expertId, count }));
        return {
            totalNodes: nodes.length,
            totalEdges: edges.length,
            byType,
            byTag,
            averageConfidence: avgConfidence,
            averageSuccessRate: avgSuccessRate,
            topExperts,
        };
    }
    /**
     * Export graph as JSON-serializable object.
     */
    export() {
        return {
            nodes: Array.from(this.graph.nodes.values()),
            edges: Array.from(this.graph.edges.values()),
            exportedAt: Date.now(),
        };
    }
    /**
     * Import graph from exported data.
     */
    import(data) {
        this.graph.nodes.clear();
        this.graph.edges.clear();
        this.graph.indexByTag.clear();
        this.graph.indexByType.clear();
        this.graph.indexByExpert.clear();
        data.nodes.forEach(node => {
            this.graph.nodes.set(node.id, node);
            node.tags.forEach(tag => {
                if (!this.graph.indexByTag.has(tag)) {
                    this.graph.indexByTag.set(tag, new Set());
                }
                this.graph.indexByTag.get(tag).add(node.id);
            });
            if (!this.graph.indexByType.has(node.type)) {
                this.graph.indexByType.set(node.type, new Set());
            }
            this.graph.indexByType.get(node.type).add(node.id);
            if (node.expertSource) {
                if (!this.graph.indexByExpert.has(node.expertSource)) {
                    this.graph.indexByExpert.set(node.expertSource, new Set());
                }
                this.graph.indexByExpert.get(node.expertSource).add(node.id);
            }
        });
        data.edges.forEach(edge => {
            this.graph.edges.set(edge.id, edge);
        });
    }
}
// ============================================================================
// Experience Tracker - captures agent experiences for learning
// ============================================================================
export class ExperienceTracker {
    experiences = [];
    maxExperiences;
    storagePath;
    constructor(maxExperiences = 1000, storagePath) {
        this.maxExperiences = maxExperiences;
        this.storagePath = storagePath;
    }
    /**
     * Record a new experience.
     */
    record(experience) {
        const id = 'exp-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
        const full = {
            ...experience,
            id,
            timestamp: Date.now(),
        };
        this.experiences.push(full);
        // Trim if over max
        if (this.experiences.length > this.maxExperiences) {
            this.experiences = this.experiences.slice(-this.maxExperiences);
        }
        return id;
    }
    /**
     * Get recent experiences.
     */
    getRecent(limit = 10) {
        return this.experiences.slice(-limit).reverse();
    }
    /**
     * Get experiences by outcome.
     */
    getByOutcome(outcome) {
        return this.experiences.filter(e => e.outcome === outcome);
    }
    /**
     * Get experiences by task type.
     */
    getByTaskType(taskType) {
        return this.experiences.filter(e => e.taskType === taskType);
    }
    /**
     * Get experiences by expert.
     */
    getByExpert(expertId) {
        return this.experiences.filter(e => e.expertId === expertId);
    }
    /**
     * Get experience statistics.
     */
    getStats() {
        const total = this.experiences.length;
        const successCount = this.experiences.filter(e => e.outcome === 'success').length;
        const byTaskType = {};
        const byExpert = {};
        this.experiences.forEach(e => {
            byTaskType[e.taskType] = (byTaskType[e.taskType] || 0) + 1;
            byExpert[e.expertId] = (byExpert[e.expertId] || 0) + 1;
        });
        return {
            total,
            successRate: total > 0 ? successCount / total : 0,
            byTaskType,
            byExpert,
        };
    }
}
// ============================================================================
// Global Instances
// ============================================================================
export const knowledgeGraph = new AgentKnowledgeGraph();
export const experienceTracker = new ExperienceTracker();
export default AgentKnowledgeGraph;
//# sourceMappingURL=knowledge-graph.js.map