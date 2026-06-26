// ============================================================================
// EO RAG System v2 - Persistent Storage with Access Control
// ============================================================================
export * from './types.js';
import * as fs from 'fs';
import * as path from 'path';
import { logger } from '../utils/logger.js';
// ============================================================================
// Persistent RAG System
// ============================================================================
export class EORAGSystem {
    config;
    chunks = [];
    initialized = false;
    currentAgentId = 'global';
    constructor(config) {
        this.config = {
            enabled: true,
            persistPath: './.eo-rag/knowledge-base.json',
            defaultTopK: 5,
            enableReranking: true,
            defaultACL: 'public',
            ...config,
        };
    }
    /**
     * Set the current agent context for access control
     */
    setAgentContext(agentId) {
        this.currentAgentId = agentId;
    }
    /**
     * Check if current agent can access a chunk
     */
    canAccess(chunk) {
        const acl = chunk.metadata.acl || this.config.defaultACL;
        const allowedAgents = chunk.metadata.allowedAgents || [];
        if (acl === 'public')
            return true;
        if (acl === 'private')
            return chunk.metadata.expertId === this.currentAgentId;
        if (acl === 'shared')
            return allowedAgents.includes(this.currentAgentId);
        return false;
    }
    /**
     * Initialize the RAG system - load from disk or seed default
     */
    async initialize() {
        logger.info('Initializing EO RAG System (persistent mode)...');
        // Ensure directory exists
        const dir = path.dirname(this.config.persistPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }
        // Load from disk
        if (fs.existsSync(this.config.persistPath)) {
            try {
                const data = JSON.parse(fs.readFileSync(this.config.persistPath, 'utf-8'));
                this.chunks = data.chunks || [];
                logger.info(`Loaded ${this.chunks.length} chunks from disk`);
            }
            catch (e) {
                logger.warn('Failed to load, starting fresh');
                this.seedDefaultKnowledge();
            }
        }
        else {
            this.seedDefaultKnowledge();
            await this.persist();
        }
        this.initialized = true;
        logger.info(`Initialized with ${this.chunks.length} knowledge chunks`);
    }
    /**
     * Seed default knowledge
     */
    seedDefaultKnowledge() {
        this.chunks = [
            {
                id: 'expert-plan-001',
                layer: 1,
                content: 'Planner Expert (plan-001): Specializes in project planning, WBS creation, milestone definition, and team composition.',
                metadata: { source: 'expert-library', expertId: 'plan-001', acl: 'public' },
                score: 1.0,
            },
            {
                id: 'expert-arch-001',
                layer: 1,
                content: 'System Architect (arch-001): Specializes in system architecture design, technology stack selection, module breakdown, and risk assessment.',
                metadata: { source: 'expert-library', expertId: 'arch-001', acl: 'public' },
                score: 1.0,
            },
            {
                id: 'expert-qa-001',
                layer: 1,
                content: 'QA Engineer (qa-001): Specializes in testing strategy, quality assurance, checkpoint verification, and test coverage.',
                metadata: { source: 'expert-library', expertId: 'qa-001', acl: 'public' },
                score: 1.0,
            },
            {
                id: 'pattern-mvp',
                layer: 2,
                content: 'MVP Development Pattern: Start with minimum viable product, then iterate.适用于需求不明确的项目。',
                metadata: { source: 'pattern-library', patternName: 'mvp-development', acl: 'public' },
                score: 1.0,
            },
            {
                id: 'pattern-parallel',
                layer: 2,
                content: 'Parallel Expert Execution: When tasks are independent, execute them in parallel using multiple experts simultaneously.',
                metadata: { source: 'pattern-library', patternName: 'parallel-experts', acl: 'public' },
                score: 1.0,
            },
        ];
    }
    /**
     * Persist chunks to disk
     */
    async persist() {
        try {
            const data = {
                version: '2.0',
                updatedAt: new Date().toISOString(),
                chunkCount: this.chunks.length,
                chunks: this.chunks,
            };
            fs.writeFileSync(this.config.persistPath, JSON.stringify(data, null, 2));
        }
        catch (e) {
            console.error('[RAG v2] Failed to persist:', e);
        }
    }
    /**
     * Search the knowledge base with access control
     */
    async search(query) {
        const startTime = Date.now();
        const topK = query.topK || this.config.defaultTopK;
        if (!this.initialized) {
            await this.initialize();
        }
        logger.debug(`Searching for: "${query.query}" (agent=${this.currentAgentId}, topK=${topK})`);
        const queryLower = query.query.toLowerCase();
        const keywords = queryLower.split(/\s+/).filter(w => w.length > 2);
        const scored = this.chunks
            .filter(chunk => this.canAccess(chunk))
            .map(chunk => {
            let score = 0;
            const contentLower = chunk.content.toLowerCase();
            for (const keyword of keywords) {
                if (contentLower.includes(keyword)) {
                    score += 1;
                    if (contentLower.includes(queryLower))
                        score += 2;
                }
            }
            // Layer boost
            if (query.strategy) {
                const strategyLayerMap = {
                    'expert_retrieval': 1,
                    'pattern_retrieval': 2,
                    'checkpoint_retrieval': 3,
                    'history_retrieval': 5,
                };
                if (strategyLayerMap[query.strategy] === chunk.layer) {
                    score *= 1.5;
                }
            }
            return { chunk, score };
        });
        const results = scored
            .filter(s => s.score > 0)
            .sort((a, b) => b.score - a.score)
            .slice(0, topK);
        const chunks = results.map(r => ({ ...r.chunk, score: r.score }));
        const scores = results.map(r => r.score);
        logger.debug(`Found ${results.length} results in ${Date.now() - startTime}ms`);
        return { chunks, scores, strategy: query.strategy || 'hybrid', queryTimeMs: Date.now() - startTime };
    }
    /**
     * Quick search
     */
    async quickSearch(query, topK) {
        return this.search({ query, topK });
    }
    /**
     * Inject relevant knowledge into context
     */
    async injectContext(request) {
        const result = await this.search({ query: request.query, topK: request.topK || 3 });
        const injection = result.chunks
            .map((c, i) => `**${i + 1}. [${c.metadata.source}]** ${c.content}`)
            .join('\n\n');
        return {
            chunks: result.chunks,
            injection,
            sources: [...new Set(result.chunks.map(c => c.metadata.source))],
        };
    }
    /**
     * Index a new chunk with access control
     */
    async indexChunk(chunk, agentId) {
        if (!this.initialized)
            await this.initialize();
        const ownerAgent = agentId || this.currentAgentId;
        const id = `chunk-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
        const newChunk = {
            ...chunk,
            id,
            metadata: {
                ...chunk.metadata,
                timestamp: Date.now(),
                acl: chunk.metadata.acl || this.config.defaultACL,
                allowedAgents: chunk.metadata.allowedAgents || [],
            },
        };
        this.chunks.push(newChunk);
        await this.persist();
        logger.debug(`Indexed chunk: ${id} (owner: ${ownerAgent})`);
        return id;
    }
    /**
     * Index a document (batch by paragraphs)
     */
    async indexDocument(doc) {
        if (!this.initialized)
            await this.initialize();
        const paragraphs = doc.content.split(/\n\n+/).filter(p => p.trim().length > 20);
        let indexed = 0;
        for (const paragraph of paragraphs) {
            await this.indexChunk({
                layer: doc.layer || 2,
                content: paragraph.trim(),
                metadata: {
                    source: doc.source,
                    acl: doc.acl || 'public',
                    allowedAgents: doc.allowedAgents || [],
                },
            });
            indexed++;
        }
        return indexed;
    }
    /**
     * Get chunks by source
     */
    async getChunksBySource(source) {
        return this.chunks.filter(c => c.metadata.source === source && this.canAccess(c));
    }
    /**
     * Delete chunks by source
     */
    async deleteBySource(source, agentId) {
        const before = this.chunks.length;
        this.chunks = this.chunks.filter(c => {
            if (c.metadata.source === source) {
                return c.metadata.expertId !== agentId;
            }
            return true;
        });
        const deleted = before - this.chunks.length;
        if (deleted > 0)
            await this.persist();
        return deleted;
    }
    /**
     * Get system statistics
     */
    async getStats() {
        const byLayer = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
        const byACL = { public: 0, private: 0, shared: 0 };
        for (const chunk of this.chunks) {
            byLayer[chunk.layer] = (byLayer[chunk.layer] || 0) + 1;
            const acl = chunk.metadata.acl || 'public';
            byACL[acl] = (byACL[acl] || 0) + 1;
        }
        return {
            enabled: this.config.enabled,
            totalChunks: this.chunks.length,
            byLayer,
            byACL,
            storagePath: this.config.persistPath,
        };
    }
    isEnabled() {
        return this.config.enabled;
    }
    createETP(record) {
        const etpId = `etp-${Date.now()}`;
        this.indexChunk({
            layer: 4,
            content: `ETP Record: ${record.taskDescription}\nOutcome: ${record.outcome}\nExperts: ${record.participatingExperts.join(', ')}\nLessons: ${record.lessons?.join('; ') || 'None'}`,
            metadata: {
                source: 'etp-protocol',
                taskId: record.taskId,
                acl: 'shared',
                allowedAgents: record.participatingExperts,
            },
        });
        return etpId;
    }
}
// ============================================================================
// Shared Singleton (per Gateway process - all agents share this)
// ============================================================================
let sharedSystem = null;
export function getSharedRAGSystem(config) {
    if (!sharedSystem) {
        sharedSystem = new EORAGSystem(config);
    }
    return sharedSystem;
}
export function resetSharedRAGSystem() {
    sharedSystem = null;
}
// ============================================================================
// Convenience Functions
// ============================================================================
export async function search(query, options) {
    const system = getSharedRAGSystem();
    return system.search({ query, topK: options?.topK, strategy: options?.strategy });
}
export async function inject(request) {
    const system = getSharedRAGSystem();
    return system.injectContext(request);
}
//# sourceMappingURL=rag-system.js.map