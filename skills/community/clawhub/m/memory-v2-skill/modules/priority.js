/**
 * Priority Module
 * Automatic message priority classification and scoring
 */

class PriorityModule {
    constructor(db) {
        this.db = db;
        this.keywords = {
            critical: ['urgent', 'emergency', 'critical', 'asap', 'immediately', 'deadline', 'blocked'],
            high: ['important', 'priority', 'required', 'needed', 'should', 'recommend'],
            medium: ['consider', 'maybe', 'optional', 'suggestion', 'idea'],
            low: ['nice to have', 'someday', 'eventually', 'wish', 'dream']
        };
    }

    /**
     * Analyze message and determine priority
     * @param {string} message - Message content
     * @param {object} context - Additional context
     * @returns {object} Priority analysis result
     */
    async analyze(message, context = {}) {
        const content = message.toLowerCase();
        let priorityLevel = 4; // Default: Low
        let importanceScore = 0;
        const detectedKeywords = [];

        // Check for critical keywords
        for (const keyword of this.keywords.critical) {
            if (content.includes(keyword)) {
                priorityLevel = Math.min(priorityLevel, 1);
                importanceScore += 25;
                detectedKeywords.push({ word: keyword, level: 'critical' });
            }
        }

        // Check for high priority keywords
        for (const keyword of this.keywords.high) {
            if (content.includes(keyword)) {
                priorityLevel = Math.min(priorityLevel, 2);
                importanceScore += 15;
                detectedKeywords.push({ word: keyword, level: 'high' });
            }
        }

        // Check for medium priority keywords
        for (const keyword of this.keywords.medium) {
            if (content.includes(keyword)) {
                priorityLevel = Math.min(priorityLevel, 3);
                importanceScore += 10;
                detectedKeywords.push({ word: keyword, level: 'medium' });
            }
        }

        // Context-based scoring
        if (context.isMentioned) importanceScore += 10;
        if (context.isReply) importanceScore += 5;
        if (context.isDirectMessage) importanceScore += 10;

        // Cap score at 100
        importanceScore = Math.min(importanceScore, 100);

        return {
            priorityLevel,
            importanceScore,
            keywords: detectedKeywords,
            contextSummary: this.generateSummary(message, detectedKeywords)
        };
    }

    /**
     * Store priority record
     */
    async store(messageId, conversationId, analysis) {
        const sql = `
            INSERT INTO memory_priorities 
            (message_id, conversation_id, priority_level, importance_score, keywords, context_summary)
            VALUES (?, ?, ?, ?, ?, ?)
        `;
        
        await this.db.run(sql, [
            messageId,
            conversationId,
            analysis.priorityLevel,
            analysis.importanceScore,
            JSON.stringify(analysis.keywords),
            analysis.contextSummary
        ]);

        return { success: true, messageId, priority: analysis.priorityLevel };
    }

    /**
     * Get messages by priority level
     */
    async getByPriority(level, limit = 50) {
        const sql = `
            SELECT * FROM memory_priorities 
            WHERE priority_level = ? 
            ORDER BY importance_score DESC, created_at DESC 
            LIMIT ?
        `;
        return await this.db.all(sql, [level, limit]);
    }

    /**
     * Get high priority messages
     */
    async getHighPriority(limit = 20) {
        const sql = `
            SELECT * FROM v_high_priority_messages 
            LIMIT ?
        `;
        return await this.db.all(sql, [limit]);
    }

    /**
     * Search by priority range
     */
    async searchByPriorityRange(minLevel = 1, maxLevel = 4) {
        const sql = `
            SELECT * FROM memory_priorities 
            WHERE priority_level BETWEEN ? AND ? 
            ORDER BY priority_level ASC, importance_score DESC
        `;
        return await this.db.all(sql, [minLevel, maxLevel]);
    }

    /**
     * Auto-cleanup low priority old records
     */
    async cleanupOldLowPriority(days = 30) {
        const sql = `
            DELETE FROM memory_priorities 
            WHERE priority_level = 4 
            AND created_at < datetime('now', '-${days} days')
        `;
        const result = await this.db.run(sql);
        return { deleted: result.changes };
    }

    /**
     * Generate context summary
     */
    generateSummary(message, keywords) {
        const sentences = message.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const firstSentence = sentences[0]?.trim() || message.substring(0, 100);
        
        return {
            firstSentence,
            keywordCount: keywords.length,
            detectedWords: keywords.map(k => k.word)
        };
    }

    /**
     * Get priority statistics
     */
    async getStats() {
        const sql = `
            SELECT 
                priority_level,
                COUNT(*) as count,
                AVG(importance_score) as avg_score
            FROM memory_priorities 
            GROUP BY priority_level
            ORDER BY priority_level
        `;
        return await this.db.all(sql);
    }
}

module.exports = PriorityModule;