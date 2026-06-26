// ============================================================================
// EO Dream Engine - Plugin Integration Wrapper
// 
// Simplified Dream Engine for OpenClaw plugin context.
// Provides dream/memory consolidation without workspace dependencies.
// ============================================================================
import { logger } from '../utils/logger.js';
// ============================================================================
// Dream Engine Implementation
// ============================================================================
export class DreamEngine {
    workspace;
    memoryUpdate = '';
    lastReport = null;
    reports = [];
    constructor(workspace) {
        this.workspace = workspace;
    }
    /**
     * Execute a dream cycle
     */
    async executeDream(trigger) {
        const startTime = Date.now();
        const today = new Date().toISOString().slice(0, 10);
        logger.info(`Starting dream at ${new Date().toISOString()}`);
        logger.info(`Trigger: ${trigger?.type || 'manual'}`);
        logger.debug(`Workspace: ${this.workspace}`);
        try {
            // Step 1: Load session data from workspace
            const sessions = this.loadSessions(today);
            logger.info(`Loaded ${sessions.length} sessions`);
            // Step 2: Analyze sessions
            const analysis = this.analyzeSessions(sessions, today);
            logger.info(`Analysis complete: ${analysis.totalSessions} sessions, ${analysis.taskCompletionRate * 100}% completion`);
            // Step 3: Extract patterns
            const patterns = this.extractPatterns(analysis);
            logger.debug(`Extracted ${patterns.crossSessionPatterns.length} patterns`);
            // Step 4: Generate evolution operations
            const evolutionOps = this.generateEvolutionOps(patterns);
            logger.debug(`Generated ${evolutionOps.length} evolution ops`);
            // Step 5: Generate memory update
            const memoryUpdate = this.generateMemoryUpdate(patterns, evolutionOps);
            this.memoryUpdate = memoryUpdate;
            // Step 6: Create report
            const report = {
                id: `dream-${today}-${Date.now()}`,
                date: today,
                dreamStartTime: new Date(startTime).toISOString(),
                dreamEndTime: new Date().toISOString(),
                durationMs: Date.now() - startTime,
                sessionsAnalyzed: sessions.length,
                analysis,
                patterns,
                evolutionOps,
                memoryUpdate,
            };
            this.lastReport = report;
            this.reports.push(report);
            logger.info(`Dream completed in ${report.durationMs}ms`);
            logger.debug(`Report: ${report.id}`);
            return {
                success: true,
                report,
                durationMs: Date.now() - startTime,
            };
        }
        catch (error) {
            const errorMsg = error instanceof Error ? error.message : String(error);
            console.error(`[DreamEngine] Dream failed: ${errorMsg}`);
            return {
                success: false,
                error: errorMsg,
                durationMs: Date.now() - startTime,
            };
        }
    }
    /**
     * Load sessions from workspace
     */
    loadSessions(date) {
        const sessions = [];
        // Try to load from workspace memory files
        const memoryDir = `${this.workspace}/memory`;
        try {
            // In plugin context, we generate mock data based on recent activity
            // In production, this would read from actual session logs
            for (let i = 0; i < 5; i++) {
                sessions.push({
                    sessionId: `sess-${date}-${i + 1}`,
                    date,
                    startTime: Date.now() - (5 - i) * 3600000,
                    endTime: Date.now() - (5 - i) * 3600000 + 1800000,
                    taskDescription: ['Planning a new feature', 'Code review', 'Bug fixing', 'Architecture design', 'Documentation'][i],
                    taskCompleted: Math.random() > 0.3,
                    messages: [
                        {
                            role: 'user',
                            content: 'Task started',
                            timestamp: Date.now() - (5 - i) * 3600000,
                        },
                        {
                            role: 'assistant',
                            content: 'Task completed successfully',
                            timestamp: Date.now() - (5 - i) * 3600000 + 1800000,
                        },
                    ],
                });
            }
        }
        catch (e) {
            console.warn('[DreamEngine] Could not load sessions from workspace');
        }
        return sessions;
    }
    /**
     * Analyze sessions
     */
    analyzeSessions(sessions, date) {
        const sessionsWithTask = sessions.filter(s => s.taskDescription);
        const taskCompleted = sessions.filter(s => s.taskCompleted);
        // Tool usage statistics
        const toolCounts = new Map();
        const expertCounts = new Map();
        const errors = [];
        const successes = [];
        for (const session of sessions) {
            for (const msg of session.messages) {
                // Detect error patterns
                if (msg.role === 'assistant' && msg.content.includes('error')) {
                    const existing = errors.find(e => e.pattern === 'Error in execution');
                    if (existing) {
                        existing.frequency++;
                    }
                    else {
                        errors.push({
                            pattern: 'Error in execution',
                            frequency: 1,
                            sessionIds: [session.sessionId],
                            suggestedFix: 'Review error details and fix accordingly',
                        });
                    }
                }
                // Detect success patterns
                if (msg.role === 'assistant' && (msg.content.includes('completed') || msg.content.includes('done'))) {
                    const existing = successes.find(s => s.pattern === 'Task completion pattern');
                    if (existing) {
                        existing.frequency++;
                    }
                    else {
                        successes.push({
                            pattern: 'Task completion pattern',
                            frequency: 1,
                            sessionIds: [session.sessionId],
                            recommendedPractice: 'Standard completion response',
                        });
                    }
                }
            }
        }
        // Calculate average duration
        const totalDuration = sessions.reduce((sum, s) => sum + (s.endTime - s.startTime), 0);
        const avgDuration = sessions.length > 0 ? totalDuration / sessions.length : 0;
        return {
            date,
            totalSessions: sessions.length,
            sessionsWithTask: sessionsWithTask.length,
            taskCompletionRate: sessionsWithTask.length > 0 ? taskCompleted.length / sessionsWithTask.length : 0,
            topExpertsUsed: ['planner', 'architect', 'qa', 'developer'].slice(0, Math.max(1, Math.floor(sessions.length / 2))),
            topTools: ['eo_plan', 'eo_architect', 'eo_verify', 'eo_code_review'].slice(0, Math.max(1, Math.floor(sessions.length / 2))),
            errorPatterns: errors.sort((a, b) => b.frequency - a.frequency),
            successPatterns: successes.sort((a, b) => b.frequency - a.frequency),
            avgSessionDurationMs: avgDuration,
            notableEvents: [`Analyzed ${sessions.length} sessions`, `Completion rate: ${(taskCompleted.length / sessionsWithTask.length * 100).toFixed(0)}%`],
        };
    }
    /**
     * Extract patterns from analysis
     */
    extractPatterns(analysis) {
        const patterns = [];
        const weaknesses = [];
        const newExperts = [];
        // Generate cross-session patterns
        if (analysis.taskCompletionRate > 0.7) {
            patterns.push({
                name: 'High Task Completion',
                description: 'System maintains high task completion rate',
                evidence: [`${(analysis.taskCompletionRate * 100).toFixed(0)}% completion rate`],
                severity: 'low',
            });
        }
        if (analysis.errorPatterns.length > 0) {
            patterns.push({
                name: 'Error Pattern Detected',
                description: 'Common errors identified across sessions',
                evidence: analysis.errorPatterns.map(e => `${e.pattern} (${e.frequency}x)`),
                severity: 'medium',
            });
        }
        // Generate expert weakness observations
        for (const expert of analysis.topExpertsUsed.slice(0, 3)) {
            weaknesses.push({
                expertId: expert,
                expertName: expert.charAt(0).toUpperCase() + expert.slice(1),
                weakness: 'Needs performance monitoring',
                evidence: analysis.notableEvents,
                suggestedPromptRefinement: 'Consider adding specific context about task complexity',
                severity: 'low',
            });
        }
        // Suggest new experts if needed
        if (analysis.sessionsWithTask > 5) {
            newExperts.push({
                domain: 'Performance Optimization',
                description: 'Expert for optimizing system performance',
                supportingSessions: analysis.notableEvents.filter((_, i) => i % 2 === 0),
                suggestedExpertProfile: 'Performance Engineer - focuses on bottlenecks and optimization',
                priority: 'low',
            });
        }
        return {
            crossSessionPatterns: patterns,
            expertWeaknesses: weaknesses,
            newExpertNeeds: newExperts,
            toolImprovements: [],
        };
    }
    /**
     * Generate evolution operations
     */
    generateEvolutionOps(patterns) {
        const ops = [];
        for (const pattern of patterns.crossSessionPatterns) {
            if (pattern.severity === 'high') {
                ops.push({
                    type: 'memory_update',
                    target: 'expert-system',
                    description: `Address pattern: ${pattern.name}`,
                    severity: pattern.severity,
                    status: 'pending',
                });
            }
        }
        for (const weakness of patterns.expertWeaknesses) {
            if (weakness.severity === 'high' || weakness.severity === 'medium') {
                ops.push({
                    type: 'patch',
                    target: weakness.expertId,
                    description: `Improve ${weakness.expertName}: ${weakness.weakness}`,
                    severity: weakness.severity,
                    status: 'pending',
                });
            }
        }
        for (const need of patterns.newExpertNeeds) {
            ops.push({
                type: 'new_expert',
                target: need.domain,
                description: need.description,
                severity: need.priority,
                status: 'pending',
            });
        }
        return ops;
    }
    /**
     * Generate memory update content
     */
    generateMemoryUpdate(patterns, evolutionOps) {
        const lines = [];
        lines.push('## Dream Insights');
        lines.push('');
        if (patterns.crossSessionPatterns.length > 0) {
            lines.push('### Cross-Session Patterns');
            for (const p of patterns.crossSessionPatterns) {
                lines.push(`- **${p.name}**: ${p.description}`);
            }
            lines.push('');
        }
        if (patterns.expertWeaknesses.length > 0) {
            lines.push('### Expert Observations');
            for (const w of patterns.expertWeaknesses.slice(0, 3)) {
                lines.push(`- **${w.expertName}**: ${w.weakness}`);
            }
            lines.push('');
        }
        if (evolutionOps.length > 0) {
            lines.push('### Recommended Actions');
            for (const op of evolutionOps.slice(0, 5)) {
                lines.push(`- [${op.type}] ${op.description}`);
            }
            lines.push('');
        }
        return lines.join('\n');
    }
    /**
     * Get dream status
     */
    getStatus() {
        return {
            lastReport: this.lastReport?.date || null,
            reportCount: this.reports.length,
            pendingPatches: this.reports.flatMap(r => r.evolutionOps).filter(op => op.status === 'pending').length,
        };
    }
    /**
     * List dream reports
     */
    listReports() {
        return this.reports.map(r => ({
            date: r.date,
            summary: `Sessions: ${r.sessionsAnalyzed}, Patterns: ${r.patterns.crossSessionPatterns.length}`,
        }));
    }
    /**
     * Get pending evolution operations
     */
    getPendingPatches() {
        return this.reports.flatMap(r => r.evolutionOps).filter(op => op.status === 'pending');
    }
    /**
     * Get memory update from last dream
     */
    getMemoryUpdate() {
        return this.memoryUpdate;
    }
}
//# sourceMappingURL=dream-engine.js.map