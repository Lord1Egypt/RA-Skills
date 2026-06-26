// ============================================================================
// EO Dream Module v2 - Enhanced with historical session analysis
//
// The "Dream" module runs during idle periods to analyze past sessions,
// extract patterns, and update proactive memory. Unlike v1 which only
// tracked session lifecycle, v2 actively learns from historical content.
// ============================================================================
import * as fs from 'fs';
import * as path from 'path';
import { createSessionArchiver } from './session-archiver.js';
import { logger } from '../utils/logger.js';
// ---------------------------------------------------------------------------
// Default Configuration
// ---------------------------------------------------------------------------
const DEFAULT_CONFIG = {
    enabled: true,
    triggerOnSessionEnd: true,
    triggerOnIdle: true,
    idleTimeoutMs: 30 * 60 * 1000, // 30 minutes
    maxSessionsPerDream: 20,
    workspaceRoot: process.cwd(),
    memoryPath: '.eo-dream/memory.json',
    notifier: undefined,
    feishuChatId: undefined,
    enableProactiveReport: true,
};
// ---------------------------------------------------------------------------
// Dream Module
// ---------------------------------------------------------------------------
export class DreamModule {
    config;
    archiver;
    memory;
    lastDreamAt = 0;
    idleSince = 0;
    isDreaming = false;
    constructor(config = {}) {
        this.config = { ...DEFAULT_CONFIG, ...config };
        this.archiver = createSessionArchiver(this.config.workspaceRoot);
        this.memory = new DreamMemory(this.config.memoryPath);
    }
    // ---------------------------------------------------------------------------
    // Idle Detection
    // ---------------------------------------------------------------------------
    /**
     * Call this when a session message is received
     */
    recordActivity() {
        this.idleSince = Date.now();
    }
    /**
     * Check if we should trigger idle dream
     */
    shouldDreamOnIdle() {
        if (!this.config.enabled || !this.config.triggerOnIdle)
            return false;
        if (this.isDreaming)
            return false;
        return Date.now() - this.idleSince > this.config.idleTimeoutMs;
    }
    // ---------------------------------------------------------------------------
    // Dream Triggers
    // ---------------------------------------------------------------------------
    /**
     * Trigger dream analysis
     * Called automatically on session end or idle
     */
    async dream(sessionKey) {
        if (!this.config.enabled) {
            return {
                sessionsAnalyzed: 0,
                patternsExtracted: 0,
                insightsGenerated: 0,
                memoryUpdated: false,
                suggestions: [],
                durationMs: 0,
                errors: ['Dream module disabled'],
            };
        }
        const startTime = Date.now();
        this.isDreaming = true;
        const errors = [];
        logger.info('🌙 Starting dream analysis...');
        try {
            // Step 1: Get recent sessions to analyze
            const sessionsToAnalyze = await this.getRecentSessions(sessionKey);
            logger.info(`Found ${sessionsToAnalyze.length} sessions to analyze`);
            // Step 2: Index any new sessions
            for (const key of sessionsToAnalyze) {
                await this.archiver.indexSession(key);
            }
            // Step 3: Extract cross-session patterns
            const patterns = this.analyzePatterns(sessionsToAnalyze);
            logger.debug(`Extracted ${patterns.length} patterns`);
            // Step 4: Generate insights
            const insights = this.generateInsights(sessionsToAnalyze, patterns);
            logger.debug(`Generated ${insights.length} insights`);
            // Step 5: Update memory
            for (const insight of insights) {
                this.memory.addInsight(insight);
            }
            this.memory.save();
            logger.debug(`Updated memory with ${insights.length} insights`);
            // Step 6: Generate suggestions
            const suggestions = this.generateSuggestions(insights);
            logger.debug(`Generated ${suggestions.length} suggestions`);
            // Step 7: Sync to long-term memory (MEMORY.md)
            if (insights.length > 0) {
                await this.syncToLongTermMemory(insights);
            }
            this.lastDreamAt = Date.now();
            // Step 8: Proactive report (send notification if enabled)
            if (this.config.enableProactiveReport && this.config.notifier) {
                await this.sendProactiveReport({
                    sessionsAnalyzed: sessionsToAnalyze.length,
                    patternsExtracted: patterns.length,
                    insightsGenerated: insights.length,
                    suggestions,
                    durationMs: Date.now() - startTime,
                });
            }
            return {
                sessionsAnalyzed: sessionsToAnalyze.length,
                patternsExtracted: patterns.length,
                insightsGenerated: insights.length,
                memoryUpdated: true,
                suggestions,
                durationMs: Date.now() - startTime,
                errors,
            };
        }
        catch (err) {
            errors.push(err instanceof Error ? err.message : String(err));
            // Notify on error too
            if (this.config.enableProactiveReport && this.config.notifier) {
                await this.config.notifier.notify('warning', '⚠️ EO 做梦分析异常', `Dream Module 分析失败: ${err instanceof Error ? err.message : String(err)}`, ['feishu'], { feishuChatId: this.config.feishuChatId }).catch(e => console.error('[Dream v2] Failed to send error notification:', e));
            }
            console.error('[Dream v2] Dream analysis failed:', err);
        }
        finally {
            this.isDreaming = false;
        }
        return {
            sessionsAnalyzed: 0,
            patternsExtracted: 0,
            insightsGenerated: 0,
            memoryUpdated: false,
            suggestions: [],
            durationMs: Date.now() - startTime,
            errors,
        };
    }
    /**
     * Get list of recent sessions to analyze
     */
    async getRecentSessions(currentSessionKey) {
        const sessions = new Set();
        // Add current session if provided
        if (currentSessionKey) {
            sessions.add(currentSessionKey);
        }
        // Search recent sessions from archiver
        const archiveIndex = this.archiver.getArchiveIndex();
        // Get sessions from patterns (they track which sessions they appeared in)
        for (const pattern of archiveIndex.patterns) {
            for (const sessionKey of pattern.sessions) {
                sessions.add(sessionKey);
            }
        }
        // Get sessions from decisions
        for (const decision of archiveIndex.decisions.slice(-50)) {
            sessions.add(decision.sessionKey);
        }
        // Limit to maxSessionsPerDream
        return Array.from(sessions).slice(-this.config.maxSessionsPerDream);
    }
    // ---------------------------------------------------------------------------
    // Pattern Analysis
    // ---------------------------------------------------------------------------
    analyzePatterns(sessionKeys) {
        const patterns = [];
        const archiveIndex = this.archiver.getArchiveIndex();
        // Group patterns by type and find cross-session ones
        const byType = new Map();
        for (const pattern of archiveIndex.patterns) {
            if (sessionKeys.some(k => pattern.sessions.includes(k))) {
                const existing = byType.get(pattern.type);
                if (existing) {
                    existing.push(pattern);
                }
                else {
                    byType.set(pattern.type, [pattern]);
                }
            }
        }
        // Find recurring patterns (appear in multiple sessions)
        for (const [type, typePatterns] of byType) {
            const recurring = typePatterns.filter(p => p.sessions.length > 1);
            for (const pattern of recurring) {
                patterns.push({
                    id: pattern.id,
                    type: pattern.type,
                    description: pattern.description,
                    occurrences: pattern.occurrences,
                    sessions: pattern.sessions,
                    consistency: pattern.sessions.length / sessionKeys.length,
                });
            }
        }
        return patterns;
    }
    /**
     * Generate insights from sessions and patterns
     */
    generateInsights(sessionKeys, patterns) {
        const insights = [];
        // Insight 1: Recurring workflows (if same pattern appears often)
        const frequentWorkflows = patterns
            .filter(p => p.type === 'command' || p.type === 'workflow')
            .filter(p => p.occurrences >= 3);
        for (const workflow of frequentWorkflows) {
            insights.push({
                id: `insight-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
                category: 'workflow',
                content: `经常使用 "${workflow.description}" (出现 ${workflow.occurrences} 次)`,
                confidence: Math.min(1, workflow.occurrences / 10),
                evidenceSessions: workflow.sessions,
                recommendation: `考虑将此工作流固化为标准流程`,
                createdAt: Date.now(),
            });
        }
        // Insight 2: Topic trends
        const archiveIndex = this.archiver.getArchiveIndex();
        const recentTopics = Array.from(archiveIndex.topics.entries())
            .filter(([_, entry]) => entry.lastDiscussedAt > Date.now() - 7 * 24 * 60 * 60 * 1000) // Last 7 days
            .sort((a, b) => b[1].messageCount - a[1].messageCount)
            .slice(0, 5);
        if (recentTopics.length > 0) {
            insights.push({
                id: `insight-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
                category: 'pattern',
                content: `最近主要讨论: ${recentTopics.map(([t]) => t).join(', ')}`,
                confidence: 0.8,
                evidenceSessions: recentTopics.flatMap(([_, entry]) => entry.sessionKeys),
                createdAt: Date.now(),
            });
        }
        // Insight 3: Expert usage patterns
        const expertPatterns = patterns.filter(p => p.type === 'expert');
        if (expertPatterns.length > 0) {
            insights.push({
                id: `insight-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
                category: 'pattern',
                content: `使用了 ${expertPatterns.length} 种不同的专家协作模式`,
                confidence: 0.7,
                evidenceSessions: expertPatterns.flatMap(p => p.sessions),
                createdAt: Date.now(),
            });
        }
        return insights;
    }
    // ---------------------------------------------------------------------------
    // Suggestions
    // ---------------------------------------------------------------------------
    generateSuggestions(insights) {
        const suggestions = [];
        for (const insight of insights) {
            if (insight.recommendation) {
                suggestions.push(insight.recommendation);
            }
        }
        // Add general suggestions based on stats
        const stats = this.archiver.getStats();
        if (stats.sessionCount > 10 && stats.topicCount < 3) {
            suggestions.push('建议: 你的工作领域似乎很集中,可以尝试扩展到更多场景');
        }
        return suggestions;
    }
    // ---------------------------------------------------------------------------
    // Proactive Reporting
    // ---------------------------------------------------------------------------
    /**
     * Send proactive report after dream analysis completes
     */
    async sendProactiveReport(result) {
        if (!this.config.notifier)
            return;
        const { sessionsAnalyzed, patternsExtracted, insightsGenerated, suggestions, durationMs } = result;
        // Build notification message
        const lines = [
            `🌙 **EO 做梦分析报告**`,
            ``,
            `📊 **分析统计**`,
            `- 分析会话数:${sessionsAnalyzed}`,
            `- 提取模式数:${patternsExtracted}`,
            `- 生成洞察数:${insightsGenerated}`,
            `- 分析耗时:${(durationMs / 1000).toFixed(1)}秒`,
            ``,
        ];
        // Add top insights if any
        const insights = this.memory.getInsights().slice(-3);
        if (insights.length > 0) {
            lines.push(`💡 **最新洞察**`);
            for (const insight of insights) {
                const emoji = insight.category === 'workflow' ? '⚙️' :
                    insight.category === 'pattern' ? '📈' : '💡';
                lines.push(`${emoji} ${insight.content}`);
            }
            lines.push(``);
        }
        // Add suggestions
        if (suggestions.length > 0) {
            lines.push(`🎯 **建议**`);
            for (const suggestion of suggestions.slice(0, 3)) {
                lines.push(`• ${suggestion}`);
            }
            lines.push(``);
        }
        lines.push(`⏰ ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
        try {
            await this.config.notifier.notify('info', '🌙 EO 做梦分析完成', lines.join('\n'), ['feishu'], { feishuChatId: this.config.feishuChatId });
            logger.info('Proactive report sent successfully');
        }
        catch (err) {
            console.error('[Dream v2] Failed to send proactive report:', err);
        }
    }
    // ---------------------------------------------------------------------------
    // Long-term Memory Sync
    // ---------------------------------------------------------------------------
    /**
     * Sync insights to MEMORY.md for long-term persistence.
     * This ensures learnings survive session resets and influence future behavior.
     */
    async syncToLongTermMemory(insights) {
        try {
            const memoryPath = path.join(this.config.workspaceRoot, 'MEMORY.md');
            // Read existing MEMORY.md
            let existingContent = '';
            if (fs.existsSync(memoryPath)) {
                existingContent = fs.readFileSync(memoryPath, 'utf-8');
            }
            // Build new section
            const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
            const insightsSection = insights.map((insight) => {
                const emoji = insight.category === 'workflow' ? '⚙️' :
                    insight.category === 'decision' ? '📋' :
                        insight.category === 'preference' ? '💡' : '📈';
                return `| ${emoji} | ${insight.content} | ${(insight.confidence * 100).toFixed(0)}% |`;
            }).join('\n');
            const newSection = `\n\n---\n\n## 🔄 自进化学习 (${timestamp})\n\n| 类型 | 洞察 | 置信度 |\n|------|------|--------|\n${insightsSection}\n\n**备注**: 本章节由 DreamModule v2 自动生成\n`;
            // Append to existing content
            existingContent = existingContent.trimEnd() + newSection;
            // Write back
            fs.writeFileSync(memoryPath, existingContent, 'utf-8');
            logger.info(`✅ Synced ${insights.length} insights to MEMORY.md`);
        }
        catch (err) {
            console.error('[Dream v2] ❌ Failed to sync to MEMORY.md:', err);
        }
    }
    /**
     * Configure proactive notifier (can be called to update notifier at runtime)
     */
    setNotifier(notifier, feishuChatId) {
        this.config.notifier = notifier;
        if (feishuChatId) {
            this.config.feishuChatId = feishuChatId;
        }
    }
    // ---------------------------------------------------------------------------
    // Status
    // ---------------------------------------------------------------------------
    getStatus() {
        return {
            enabled: this.config.enabled,
            isDreaming: this.isDreaming,
            lastDreamAt: this.lastDreamAt,
            idleForMs: Date.now() - this.idleSince,
            stats: this.archiver.getStats(),
        };
    }
    /**
     * Get current memory (learnings)
     */
    getMemory() {
        return this.memory.getInsights();
    }
}
// ---------------------------------------------------------------------------
// Dream Memory (Persistent Storage)
// ---------------------------------------------------------------------------
class DreamMemory {
    path;
    insights = [];
    constructor(memoryPath) {
        this.path = memoryPath;
        this.load();
    }
    load() {
        try {
            if (fs.existsSync(this.path)) {
                const data = fs.readFileSync(this.path, 'utf-8');
                this.insights = JSON.parse(data);
            }
        }
        catch (e) {
            console.warn('[DreamMemory] Failed to load:', e);
            this.insights = [];
        }
    }
    save() {
        try {
            const dir = path.dirname(this.path);
            if (!fs.existsSync(dir)) {
                fs.mkdirSync(dir, { recursive: true });
            }
            fs.writeFileSync(this.path, JSON.stringify(this.insights, null, 2));
        }
        catch (e) {
            console.error('[DreamMemory] Failed to save:', e);
        }
    }
    addInsight(insight) {
        // Don't add duplicate insights
        const exists = this.insights.some(i => i.category === insight.category && i.content === insight.content);
        if (!exists) {
            this.insights.push(insight);
            // Keep only last 100 insights
            if (this.insights.length > 100) {
                this.insights = this.insights.slice(-100);
            }
        }
    }
    getInsights() {
        return this.insights;
    }
}
// ---------------------------------------------------------------------------
// Convenience Factory
// ---------------------------------------------------------------------------
let globalDreamModule = null;
export function getDreamModule(config) {
    if (!globalDreamModule) {
        globalDreamModule = new DreamModule(config);
    }
    return globalDreamModule;
}
export function createDreamModule(config) {
    return new DreamModule(config);
}
//# sourceMappingURL=eo-dream-enhanced.js.map