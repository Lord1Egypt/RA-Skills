/**
 * Pattern Learning Tool - Extract and retrieve successful patterns
 */
import { patternLearner } from '../session/pattern-learner.js';
import { textResult, errorResult } from '../formatters/index.js';
import * as fs from 'fs';
import * as path from 'path';
import { toolLogger } from '../utils/logger.js';
/**
 * Handle pattern learning operations
 */
export async function handlePatternLearn(params, agentId) {
    try {
        switch (params.action) {
            case 'learn':
                return await handleLearn(params, agentId);
            case 'retrieve':
                return await handleRetrieve(params);
            case 'stats':
                return await handleStats();
            case 'list':
                return await handleList();
            default:
                return errorResult(`Unknown action: ${params.action}`);
        }
    }
    catch (err) {
        return errorResult(`Pattern learn error: ${err instanceof Error ? err.message : String(err)}`);
    }
}
/**
 * Learn patterns from a session file
 */
async function handleLearn(params, agentId) {
    const sessions = [];
    if (params.sessionFile && fs.existsSync(params.sessionFile)) {
        // Learn from specific session file
        const content = fs.readFileSync(params.sessionFile, 'utf-8');
        const lines = content.split('\n').filter(l => l.trim());
        const messages = [];
        for (const line of lines) {
            try {
                const entry = JSON.parse(line);
                if (entry.type === 'message') {
                    messages.push(entry.message);
                }
            }
            catch (e) { }
        }
        sessions.push({
            key: params.sessionFile,
            data: { messages, messageCount: messages.length },
        });
    }
    else {
        // Learn from recent sessions
        const sessionDir = '/home/zzy/.openclaw/agents/jisu-admin/sessions';
        const files = fs.readdirSync(sessionDir)
            .filter(f => f.endsWith('.jsonl') && !f.includes('checkpoint'))
            .sort()
            .reverse()
            .slice(0, 10); // Last 10 sessions
        for (const file of files) {
            try {
                const filePath = path.join(sessionDir, file);
                const content = fs.readFileSync(filePath, 'utf-8');
                const lines = content.split('\n').filter(l => l.trim());
                const messages = [];
                for (const line of lines) {
                    try {
                        const entry = JSON.parse(line);
                        if (entry.type === 'message') {
                            messages.push(entry.message);
                        }
                    }
                    catch (e) { }
                }
                sessions.push({
                    key: file,
                    data: { messages, messageCount: messages.length },
                });
            }
            catch (e) { }
        }
    }
    if (sessions.length === 0) {
        return errorResult('No sessions found to learn from');
    }
    toolLogger.info(`Learning from ${sessions.length} sessions...`);
    const result = await patternLearner.learnFromSessions(sessions);
    const output = `🧠 **Pattern Learning Complete**

**Sessions analyzed:** ${sessions.length}
**Patterns identified:** ${result.patternsLearned}
**High-confidence patterns stored:** ${result.highConfidence}

**Patterns stored in RAG L2** (Layer: Pattern Library)

These patterns will now be used to:
- Provide relevant execution paths for new tasks
- Reduce user intervention by following proven patterns
- Accelerate similar task completion

Use \`/eo_pattern retrieve task=<your-task>\` to retrieve relevant patterns.`;
    return textResult(output);
}
/**
 * Retrieve relevant patterns for a task
 */
async function handleRetrieve(params) {
    if (!params.taskQuery) {
        return errorResult('Provide taskQuery to retrieve patterns');
    }
    const patterns = await patternLearner.retrievePatterns(params.taskQuery, 3);
    if (patterns.length === 0) {
        return textResult(`🔍 **No patterns found for:** "${params.taskQuery}"

No similar successful patterns in the pattern library yet.
Run \`/eo_pattern learn\` first to build the pattern library.`);
    }
    const lines = [
        `🔍 **Patterns for:** "${params.taskQuery}"\n`,
        `Found ${patterns.length} relevant patterns:\n`,
    ];
    for (let i = 0; i < patterns.length; i++) {
        const p = patterns[i];
        lines.push(`### ${i + 1}. ${p.name}`);
        lines.push(`**Type:** ${p.taskType}`);
        lines.push(`**Confidence:** ${(p.confidence * 100).toFixed(0)}%`);
        lines.push(`**Steps:** ${p.pattern.substring(0, 100)}...`);
        lines.push('');
    }
    lines.push('---');
    lines.push('*Inject these patterns into context to follow proven execution paths.*');
    return textResult(lines.join('\n'));
}
/**
 * Get pattern statistics
 */
async function handleStats() {
    const stats = await patternLearner.getStats();
    const lines = [
        '📊 **Pattern Library Statistics**',
        '',
        `**Total Patterns:** ${stats.totalPatterns}`,
        '',
        '### By Task Type',
    ];
    for (const [type, count] of Object.entries(stats.byType)) {
        lines.push(`- ${type}: ${count}`);
    }
    return textResult(lines.join('\n'));
}
/**
 * List all patterns
 */
async function handleList() {
    const stats = await patternLearner.getStats();
    return textResult(`📚 **Pattern Library**

Total patterns: ${stats.totalPatterns}

Use \`/eo_pattern retrieve task=<task-description>\` to retrieve relevant patterns for your current task.

Use \`/eo_pattern learn\` to analyze recent sessions and add new patterns.`);
}
//# sourceMappingURL=pattern-learn.js.map