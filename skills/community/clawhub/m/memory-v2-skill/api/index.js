/**
 * Memory V2.0 Unified API
 * Single entry point for all memory operations
 */

const PriorityModule = require('../modules/priority');
const LearningModule = require('../modules/learning');
const DecisionModule = require('../modules/decision');
const EvolutionModule = require('../modules/evolution');
const VersionManager = require('../modules/version');
const QueryModule = require('../modules/query');
const MemoryDatabase = require('../database/init');

class MemoryAPI {
    constructor(dbPath = './memory-v2.db') {
        this.dbPath = dbPath;
        this.db = new MemoryDatabase(dbPath);
        this.modules = {};
    }

    /**
     * Initialize API and all modules
     */
    async init() {
        await this.db.init();
        await this.db.runSchema();

        // Initialize modules
        this.modules = {
            priority: new PriorityModule(this.db),
            learning: new LearningModule(this.db),
            decision: new DecisionModule(this.db),
            evolution: new EvolutionModule(this.db),
            version: new VersionManager(this.db),
            query: new QueryModule({ dbPath: this.dbPath })
        };

        // Initialize query module
        await this.modules.query.init();

        console.log('✅ Memory V2.5 API initialized');
        return this;
    }

    // =========================================
    // PRIORITY API
    // =========================================

    async analyzePriority(message, context = {}) {
        return await this.modules.priority.analyze(message, context);
    }

    async storePriority(messageId, conversationId, analysis) {
        return await this.modules.priority.store(messageId, conversationId, analysis);
    }

    async getHighPriority(limit = 20) {
        return await this.modules.priority.getHighPriority(limit);
    }

    // =========================================
    // LEARNING API
    // =========================================

    async detectLearningIntent(message) {
        return await this.modules.learning.detectIntent(message);
    }

    async startLearning(messageId, conversationId, message) {
        const intent = await this.detectLearningIntent(message);
        if (!intent.isLearning) {
            return { success: false, error: 'No learning intent detected' };
        }
        return await this.modules.learning.createLearning(messageId, conversationId, intent, message);
    }

    async updateLearningProgress(learningId, progressData) {
        return await this.modules.learning.updateProgress(learningId, progressData);
    }

    async addMilestone(learningId, milestone) {
        return await this.modules.learning.addMilestone(learningId, milestone);
    }

    async getActiveLearning(limit = 20) {
        return await this.modules.learning.getActiveLearning(limit);
    }

    async getWeeklyLearningReport() {
        return await this.modules.learning.generateWeeklyReport();
    }

    // =========================================
    // DECISION API
    // =========================================

    async recordDecision(messageId, conversationId, decisionData) {
        return await this.modules.decision.createDecision(messageId, conversationId, decisionData);
    }

    async updateDecisionOutcome(decisionId, outcomeData) {
        return await this.modules.decision.updateOutcome(decisionId, outcomeData);
    }

    async getPendingDecisions(limit = 20) {
        return await this.modules.decision.getPendingDecisions(limit);
    }

    async getDueReviews(days = 7) {
        return await this.modules.decision.getDueReviews(days);
    }

    async getDecisionStats() {
        return await this.modules.decision.getStats();
    }

    async analyzeDecisionPatterns() {
        return await this.modules.decision.analyzePatterns();
    }

    // =========================================
    // EVOLUTION API
    // =========================================

    async recordSkillUsage(skillName, category, result = 'success', metrics = {}) {
        return await this.modules.evolution.recordUsage(skillName, category, result, metrics);
    }

    async getSkill(skillName) {
        return await this.modules.evolution.getSkill(skillName);
    }

    async getTopSkills(limit = 10) {
        return await this.modules.evolution.getTopSkills(limit);
    }

    async getSkillGrowthReport(days = 30) {
        return await this.modules.evolution.generateGrowthReport(days);
    }

    async suggestSkillsToPractice() {
        return await this.modules.evolution.suggestPractice();
    }

    // =========================================
    // VERSION API
    // =========================================

    async createBackup(description = '') {
        return await this.modules.version.createBackup(description, 'full');
    }

    async listVersions() {
        return await this.modules.version.listVersions();
    }

    async rollbackToVersion(versionId) {
        return await this.modules.version.rollbackToVersion(versionId);
    }

    async getBackupStats() {
        return await this.modules.version.getBackupStats();
    }

    // =========================================
    // UNIFIED QUERY API
    // =========================================

    /**
     * Search across all memory modules
     */
    async search(query, options = {}) {
        const results = {
            query,
            timestamp: new Date().toISOString(),
            modules: {}
        };

        // Search priorities
        if (options.modules?.includes('priority') || !options.modules) {
            results.modules.priority = await this.modules.priority.searchByPriorityRange();
        }

        // Search learning
        if (options.modules?.includes('learning') || !options.modules) {
            results.modules.learning = await this.modules.learning.getByTopic(query);
        }

        // Search decisions
        if (options.modules?.includes('decision') || !options.modules) {
            results.modules.decisions = await this.modules.decision.getSimilarDecisions(query);
        }

        return results;
    }

    /**
     * Get comprehensive dashboard data
     */
    async getDashboard() {
        return {
            priority: {
                high: await this.modules.priority.getHighPriority(5),
                stats: await this.modules.priority.getStats()
            },
            learning: {
                active: await this.modules.learning.getActiveLearning(5),
                weekly: await this.modules.learning.generateWeeklyReport()
            },
            decisions: {
                pending: await this.modules.decision.getPendingDecisions(5),
                dueReviews: await this.modules.decision.getDueReviews(7)
            },
            evolution: {
                top: await this.modules.evolution.getTopSkills(5),
                needsPractice: await this.modules.evolution.suggestPractice()
            },
            version: {
                stats: await this.modules.version.getBackupStats()
            }
        };
    }

    /**
     * Health check
     */
    async health() {
        return await this.db.healthCheck();
    }

    /**
     * Close database connection
     */
    async close() {
        await this.db.close();
    }
}

// CLI usage
if (require.main === module) {
    const api = new MemoryAPI();
    
    (async () => {
        try {
            await api.init();
            
            // Example usage
            console.log('\n📊 Dashboard:');
            const dashboard = await api.getDashboard();
            console.log(JSON.stringify(dashboard, null, 2));
            
            await api.close();
        } catch (err) {
            console.error('❌ Error:', err);
            process.exit(1);
        }
    })();
}

module.exports = MemoryAPI;
