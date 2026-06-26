/**
 * RAG Updater
 * Updates the RAG knowledge base with new patterns and knowledge
 */
export class RAGUpdater {
    rag;
    updateLog = [];
    constructor(rag) {
        this.rag = rag;
    }
    /**
     * Update RAG with extracted patterns
     */
    async update(patterns) {
        const result = {
            success: false,
            chunksAdded: 0,
            chunksRemoved: 0,
            errors: [],
        };
        try {
            // Index new patterns into RAG
            for (const pattern of patterns) {
                await this.rag.indexChunk({
                    layer: 2, // Pattern layer
                    content: this.formatPatternContent(pattern),
                    metadata: {
                        source: 'pattern-extractor',
                        patternName: pattern.name,
                        timestamp: Date.now(),
                    },
                });
                result.chunksAdded++;
                this.logUpdate('add', pattern.id);
            }
            result.success = true;
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            result.errors.push(errorMsg);
        }
        return result;
    }
    /**
     * Update RAG with session data
     */
    async updateWithSession(session) {
        const result = {
            success: false,
            chunksAdded: 0,
            chunksRemoved: 0,
            errors: [],
        };
        try {
            // Add session summary to RAG
            await this.rag.indexChunk({
                layer: 5, // Session memory layer
                content: this.formatSessionContent(session),
                metadata: {
                    source: 'session-analyzer',
                    taskId: session.sessionId,
                    timestamp: session.timestamp,
                },
            });
            result.chunksAdded++;
            this.logUpdate('add', session.sessionId);
            result.success = true;
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            result.errors.push(errorMsg);
        }
        return result;
    }
    /**
     * Index expert knowledge
     */
    async indexExpertKnowledge(expertId, knowledge) {
        await this.rag.indexChunk({
            layer: 1, // Expert profile layer
            content: knowledge,
            metadata: {
                source: 'expert-knowledge',
                expertId,
                timestamp: Date.now(),
            },
        });
        this.logUpdate('add', `expert-${expertId}`);
    }
    /**
     * Index ETP (Experience Transfer Protocol) record
     */
    async indexETPRecord(taskId, taskDescription, outcome, lessons) {
        await this.rag.indexChunk({
            layer: 4, // ETP layer
            content: `ETP: ${taskDescription}\nOutcome: ${outcome}\nLessons: ${lessons?.join('; ') || 'None'}`,
            metadata: {
                source: 'etp-protocol',
                taskId,
                timestamp: Date.now(),
            },
        });
        this.logUpdate('add', `etp-${taskId}`);
    }
    /**
     * Format pattern content for RAG
     */
    formatPatternContent(pattern) {
        return [
            `Pattern: ${pattern.name}`,
            `Description: ${pattern.description}`,
            `Type: ${pattern.type}`,
            `Severity: ${pattern.severity}`,
            `Frequency: ${pattern.frequency}`,
            `Evidence: ${pattern.evidence.join(' | ')}`,
            pattern.suggestedAction ? `Suggested Action: ${pattern.suggestedAction}` : '',
        ]
            .filter(Boolean)
            .join('\n');
    }
    /**
     * Format session content for RAG
     */
    formatSessionContent(session) {
        return [
            `Session: ${session.sessionId}`,
            `Workflow: ${session.workflowType}`,
            `Topics: ${session.keyTopics.join(', ')}`,
            `Tools: ${session.toolsUsed.join(', ')}`,
            `Messages: ${session.messageCount}`,
            `Success Indicators: ${session.successIndicators.length}`,
            `Error Indicators: ${session.errorIndicators.length}`,
        ].join('\n');
    }
    /**
     * Log update operation
     */
    logUpdate(action, chunkId) {
        this.updateLog.push({
            timestamp: Date.now(),
            action,
            chunkId,
        });
    }
    /**
     * Get update statistics
     */
    getStats() {
        const now = Date.now();
        const recentThreshold = 3600000; // Last hour
        return {
            totalUpdates: this.updateLog.length,
            recentUpdates: this.updateLog.filter(u => now - u.timestamp < recentThreshold).length,
        };
    }
    /**
     * Clear stale entries (placeholder for actual cleanup logic)
     */
    async clearStaleEntries(_maxAgeMs = 604800000) {
        // In a real implementation, this would query and remove old chunks
        return 0;
    }
}
//# sourceMappingURL=rag-updater.js.map