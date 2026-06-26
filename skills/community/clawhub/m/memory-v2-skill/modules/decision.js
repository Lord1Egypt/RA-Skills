/**
 * Decision Module
 * Track decisions, outcomes, and reviews
 */

class DecisionModule {
    constructor(db) {
        this.db = db;
        this.decisionTypes = ['framework', 'vendor', 'migration', 'publish', 'spend', 'other'];
        
        // Keywords for automatic decision type detection
        this.typeKeywords = {
            framework: ['framework', 'library', 'architecture', 'stack', 'technology'],
            vendor: ['vendor', 'provider', 'service', 'platform', 'tool'],
            migration: ['migrate', 'upgrade', 'update', 'move', 'transfer', 'switch'],
            publish: ['publish', 'release', 'deploy', 'launch', 'ship'],
            spend: ['budget', 'cost', 'price', 'purchase', 'buy', 'invest', 'spend'],
            other: ['decide', 'choice', 'option', 'select', 'pick']
        };
    }

    /**
     * Detect decision type from message
     */
    detectType(message) {
        const content = message.toLowerCase();
        const scores = {};

        for (const [type, keywords] of Object.entries(this.typeKeywords)) {
            scores[type] = 0;
            for (const keyword of keywords) {
                if (content.includes(keyword)) {
                    scores[type] += 1;
                }
            }
        }

        // Find highest score
        let detectedType = 'other';
        let maxScore = 0;

        for (const [type, score] of Object.entries(scores)) {
            if (score > maxScore) {
                maxScore = score;
                detectedType = type;
            }
        }

        return {
            type: detectedType,
            confidence: maxScore > 0 ? Math.min(maxScore / 3, 1) : 0,
            scores
        };
    }

    /**
     * Extract decision question
     */
    extractQuestion(message) {
        // Look for question patterns
        const patterns = [
            /(?:should|need to|want to|decide|choose)\s+(.+?)(?:\?|\.|$)/i,
            /which\s+(.+?)(?:\?|\.|$)/i,
            /what\s+(.+?)(?:\?|\.|$)/i,
            /how\s+(.+?)(?:\?|\.|$)/i
        ];

        for (const pattern of patterns) {
            const match = message.match(pattern);
            if (match) {
                return match[1].trim();
            }
        }

        // Fallback: first sentence
        const sentences = message.split(/[.!?]+/);
        return sentences[0]?.trim() || message.substring(0, 100);
    }

    /**
     * Create new decision record
     */
    async createDecision(messageId, conversationId, decisionData) {
        const sql = `
            INSERT INTO memory_decisions 
            (message_id, conversation_id, decision_type, decision_question, 
             decision_context, options_considered, chosen_option, rationale, 
             confidence_level, expected_outcome, review_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        `;

        // Auto-detect type if not provided
        const typeDetection = decisionData.type 
            ? { type: decisionData.type, confidence: 1 } 
            : this.detectType(decisionData.question || decisionData.context);

        // Calculate review date (default: 30 days)
        const reviewDate = new Date();
        reviewDate.setDate(reviewDate.getDate() + (decisionData.reviewDays || 30));

        const result = await this.db.run(sql, [
            messageId,
            conversationId,
            typeDetection.type,
            decisionData.question || this.extractQuestion(decisionData.context),
            decisionData.context,
            JSON.stringify(decisionData.options || []),
            decisionData.chosenOption,
            decisionData.rationale,
            decisionData.confidence || 3,
            decisionData.expectedOutcome,
            reviewDate.toISOString()
        ]);

        return {
            success: true,
            decisionId: result.id,
            type: typeDetection.type,
            reviewDate: reviewDate.toISOString()
        };
    }

    /**
     * Update decision outcome
     */
    async updateOutcome(decisionId, outcomeData) {
        const sql = `
            UPDATE memory_decisions 
            SET outcome_status = ?, actual_outcome = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        `;

        await this.db.run(sql, [
            outcomeData.status,
            outcomeData.description,
            decisionId
        ]);

        return { success: true, decisionId };
    }

    /**
     * Schedule review
     */
    async scheduleReview(decisionId, reviewDate) {
        const sql = `
            UPDATE memory_decisions 
            SET review_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        `;

        await this.db.run(sql, [reviewDate, decisionId]);
        return { success: true };
    }

    /**
     * Complete review
     */
    async completeReview(decisionId, reviewData) {
        const sql = `
            UPDATE memory_decisions 
            SET reviewed_at = CURRENT_TIMESTAMP, review_notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        `;

        await this.db.run(sql, [reviewData.notes, decisionId]);
        return { success: true };
    }

    /**
     * Get pending decisions
     */
    async getPendingDecisions(limit = 20) {
        const sql = `SELECT * FROM v_pending_decisions LIMIT ?`;
        return await this.db.all(sql, [limit]);
    }

    /**
     * Get decisions by type
     */
    async getByType(type, limit = 20) {
        const sql = `
            SELECT * FROM memory_decisions 
            WHERE decision_type = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        `;
        return await this.db.all(sql, [type, limit]);
    }

    /**
     * Get decisions needing review
     */
    async getDueReviews(days = 7) {
        const sql = `
            SELECT * FROM memory_decisions 
            WHERE outcome_status = 'pending'
            AND review_date <= datetime('now', '+${days} days')
            AND reviewed_at IS NULL
            ORDER BY review_date ASC
        `;
        return await this.db.all(sql);
    }

    /**
     * Get decision statistics
     */
    async getStats() {
        const sql = `
            SELECT 
                decision_type,
                outcome_status,
                COUNT(*) as count
            FROM memory_decisions 
            GROUP BY decision_type, outcome_status
        `;
        return await this.db.all(sql);
    }

    /**
     * Analyze decision patterns
     */
    async analyzePatterns() {
        const sql = `
            SELECT 
                decision_type,
                AVG(confidence_level) as avg_confidence,
                COUNT(CASE WHEN outcome_status = 'successful' THEN 1 END) as success_count,
                COUNT(CASE WHEN outcome_status = 'failed' THEN 1 END) as failure_count,
                COUNT(*) as total
            FROM memory_decisions 
            WHERE outcome_status != 'pending'
            GROUP BY decision_type
        `;
        
        const patterns = await this.db.all(sql);
        
        return patterns.map(p => ({
            ...p,
            success_rate: p.total > 0 ? (p.success_count / p.total * 100).toFixed(2) : 0
        }));
    }

    /**
     * Get similar past decisions
     */
    async getSimilarDecisions(question, limit = 5) {
        const keywords = question.toLowerCase().split(/\s+/).filter(w => w.length > 3);
        
        if (keywords.length === 0) return [];

        const conditions = keywords.map(() => 'decision_question LIKE ?').join(' OR ');
        const sql = `
            SELECT * FROM memory_decisions 
            WHERE ${conditions}
            ORDER BY created_at DESC 
            LIMIT ?
        `;

        const params = keywords.map(k => `%${k}%`);
        params.push(limit);

        return await this.db.all(sql, params);
    }
}

module.exports = DecisionModule;
