/**
 * Learning Module
 * Track learning intents, progress, and milestones
 */

class LearningModule {
    constructor(db) {
        this.db = db;
        this.learningPatterns = [
            { pattern: /learn|study|understand|master|grasp/i, category: 'skill' },
            { pattern: /read|book|article|paper|research/i, category: 'knowledge' },
            { pattern: /practice|exercise|train|drill/i, category: 'practice' },
            { pattern: /course|tutorial|lesson|lecture/i, category: 'course' },
            { pattern: /language|english|chinese|spanish|japanese/i, category: 'language' }
        ];
    }

    /**
     * Detect learning intent in message
     */
    async detectIntent(message) {
        const content = message.toLowerCase();
        let detectedCategory = null;
        let confidence = 0;

        for (const { pattern, category } of this.learningPatterns) {
            if (pattern.test(content)) {
                detectedCategory = category;
                confidence += 0.2;
            }
        }

        // Extract topic using simple heuristics
        const topic = this.extractTopic(message);

        return {
            isLearning: confidence > 0,
            category: detectedCategory || 'general',
            confidence: Math.min(confidence, 1),
            topic,
            suggestedResources: this.suggestResources(topic, detectedCategory)
        };
    }

    /**
     * Extract learning topic from message
     */
    extractTopic(message) {
        // Simple extraction - can be enhanced with NLP
        const patterns = [
            /learn(?:ing)?\s+(?:about\s+)?(.+?)(?:\.|,|;|$)/i,
            /study(?:ing)?\s+(?:about\s+)?(.+?)(?:\.|,|;|$)/i,
            /how\s+to\s+(.+?)(?:\.|,|;|$)/i,
            /master(?:ing)?\s+(.+?)(?:\.|,|;|$)/i
        ];

        for (const pattern of patterns) {
            const match = message.match(pattern);
            if (match) {
                return match[1].trim();
            }
        }

        return 'general learning';
    }

    /**
     * Create new learning record
     */
    async createLearning(messageId, conversationId, intent, notes = '') {
        const sql = `
            INSERT INTO memory_learning 
            (message_id, conversation_id, learning_topic, topic_category, progress_status, notes)
            VALUES (?, ?, ?, ?, 'started', ?)
        `;

        const result = await this.db.run(sql, [
            messageId,
            conversationId,
            intent.topic,
            intent.category,
            notes
        ]);

        return {
            success: true,
            learningId: result.id,
            topic: intent.topic,
            category: intent.category
        };
    }

    /**
     * Update learning progress
     */
    async updateProgress(learningId, progressData) {
        const updates = [];
        const values = [];

        if (progressData.percentage !== undefined) {
            updates.push('progress_percentage = ?');
            values.push(progressData.percentage);
        }

        if (progressData.status) {
            updates.push('progress_status = ?');
            values.push(progressData.status);
        }

        if (progressData.notes) {
            updates.push('notes = ?');
            values.push(progressData.notes);
        }

        if (progressData.completionDate) {
            updates.push('actual_completion_date = ?');
            values.push(progressData.completionDate);
        }

        if (updates.length === 0) return { success: false, error: 'No updates provided' };

        const sql = `UPDATE memory_learning SET ${updates.join(', ')} WHERE id = ?`;
        values.push(learningId);

        await this.db.run(sql, values);
        return { success: true, learningId };
    }

    /**
     * Add milestone to learning
     */
    async addMilestone(learningId, milestone) {
        const sql = `
            INSERT INTO memory_learning_milestones 
            (learning_id, milestone_name, description, target_date)
            VALUES (?, ?, ?, ?)
        `;

        const result = await this.db.run(sql, [
            learningId,
            milestone.name,
            milestone.description,
            milestone.targetDate
        ]);

        // Update milestone count
        await this.db.run(
            `UPDATE memory_learning SET milestone_count = milestone_count + 1 WHERE id = ?`,
            [learningId]
        );

        return { success: true, milestoneId: result.id };
    }

    /**
     * Complete milestone
     */
    async completeMilestone(milestoneId) {
        const sql = `
            UPDATE memory_learning_milestones 
            SET is_completed = 1, completed_date = CURRENT_TIMESTAMP 
            WHERE id = ?
        `;

        await this.db.run(sql, [milestoneId]);

        // Get learning ID and update completed count
        const milestone = await this.db.get(
            'SELECT learning_id FROM memory_learning_milestones WHERE id = ?',
            [milestoneId]
        );

        if (milestone) {
            await this.db.run(
                `UPDATE memory_learning 
                 SET completed_milestones = completed_milestones + 1 
                 WHERE id = ?`,
                [milestone.learning_id]
            );
        }

        return { success: true };
    }

    /**
     * Get active learning items
     */
    async getActiveLearning(limit = 20) {
        const sql = `SELECT * FROM v_active_learning LIMIT ?`;
        return await this.db.all(sql, [limit]);
    }

    /**
     * Get learning by topic
     */
    async getByTopic(topic, limit = 10) {
        const sql = `
            SELECT * FROM memory_learning 
            WHERE learning_topic LIKE ? 
            ORDER BY created_at DESC 
            LIMIT ?
        `;
        return await this.db.all(sql, [`%${topic}%`, limit]);
    }

    /**
     * Get learning statistics
     */
    async getStats() {
        const sql = `
            SELECT 
                progress_status,
                COUNT(*) as count,
                AVG(progress_percentage) as avg_progress
            FROM memory_learning 
            GROUP BY progress_status
        `;
        return await this.db.all(sql);
    }

    /**
     * Generate weekly report
     */
    async generateWeeklyReport() {
        const sql = `SELECT * FROM v_weekly_learning_report LIMIT 4`;
        const weeklyData = await this.db.all(sql);

        const activeLearning = await this.getActiveLearning(10);

        return {
            weeklyTrend: weeklyData,
            activeTopics: activeLearning,
            summary: {
                totalActive: activeLearning.length,
                avgProgress: activeLearning.reduce((sum, item) => sum + item.progress_percentage, 0) / activeLearning.length || 0
            }
        };
    }

    /**
     * Suggest resources based on topic
     */
    suggestResources(topic, category) {
        const resources = {
            skill: [
                { type: 'practice', name: 'Hands-on exercises' },
                { type: 'project', name: 'Build a small project' }
            ],
            knowledge: [
                { type: 'reading', name: 'Related articles' },
                { type: 'video', name: 'Tutorial videos' }
            ],
            language: [
                { type: 'app', name: 'Language learning app' },
                { type: 'practice', name: 'Conversation practice' }
            ],
            course: [
                { type: 'online', name: 'Online course platform' },
                { type: 'documentation', name: 'Official documentation' }
            ]
        };

        return resources[category] || resources.knowledge;
    }
}

module.exports = LearningModule;