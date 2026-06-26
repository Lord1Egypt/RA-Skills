/**
 * EO Dream Tool Handler v2
 * Dream Module with MEMORY.md sync
 */
import { textResult } from '../formatters/index.js';
import { getContextLoader } from '../session/context-loader.js';
import * as fs from 'fs';
import * as path from 'path';
import { PLUGIN_VERSION } from '../config.js';
import { toolLogger } from '../utils/logger.js';
export async function handleDream(params) {
    const trigger = params?.trigger || 'manual';
    const startTime = Date.now();
    toolLogger.log(`Dream Module triggered by: ${trigger}`);
    try {
        // Load learnings from MEMORY.md
        const workspaceRoot = process.cwd();
        const loader = getContextLoader({ workspaceRoot });
        const learnings = loader.loadSelfEvolutionLearnings();
        // Analyze learnings
        const insights = learnings.map(l => ({
            type: l.type,
            content: l.content.slice(0, 200),
            timestamp: l.timestamp
        }));
        // Sync to MEMORY.md
        await syncInsightsToMemory(workspaceRoot, insights);
        // Build output
        const output = buildDreamOutput(insights, {
            trigger,
            durationMs: Date.now() - startTime,
            learningsCount: learnings.length
        });
        return textResult(output, {
            success: true,
            insightsGenerated: insights.length,
            durationMs: Date.now() - startTime
        });
    }
    catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err);
        console.error(`[eo_dream v2] Error: ${errorMsg}`);
        return textResult(`❌ Dream Module Error: ${errorMsg}`, {
            success: false,
            error: errorMsg
        });
    }
}
async function syncInsightsToMemory(workspaceRoot, insights) {
    const memoryPath = path.join(workspaceRoot, 'MEMORY.md');
    if (!fs.existsSync(memoryPath)) {
        toolLogger.warn(`MEMORY.md not found at ${memoryPath}`);
        return;
    }
    try {
        const content = fs.readFileSync(memoryPath, 'utf-8');
        const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);
        const section = `\n\n---\n\n## 🌙 Dream Module Insights (${timestamp})\n\n`;
        const insightLines = insights.map(i => `- **[${i.type}]** ${i.content}${i.timestamp ? ` (${new Date(i.timestamp).toLocaleString()})` : ''}`).join('\n');
        const fullSection = section + insightLines;
        fs.writeFileSync(memoryPath, content.trimEnd() + fullSection, 'utf-8');
        toolLogger.info(`Synced ${insights.length} insights to MEMORY.md`);
    }
    catch (err) {
        console.error(`[eo_dream] Failed to sync to MEMORY.md: ${err}`);
    }
}
function buildDreamOutput(insights, stats) {
    const lines = [
        `🌙 **EO Dream Module v${PLUGIN_VERSION}**`,
        ``,
        `**Trigger:** ${stats.trigger}`,
        `**Learnings Loaded:** ${stats.learningsCount}`,
        `**Insights Generated:** ${insights.length}`,
        `**Duration:** ${stats.durationMs}ms`,
        ``
    ];
    if (insights.length > 0) {
        lines.push(`### Insights`);
        lines.push(``);
        for (const insight of insights) {
            lines.push(`- **[${insight.type}]** ${insight.content}`);
        }
    }
    else {
        lines.push(`*No learnings yet. Keep working to accumulate patterns.*`);
    }
    lines.push(``);
    lines.push(`💾 Insights synced to MEMORY.md`);
    return lines.join('\n');
}
//# sourceMappingURL=dream.js.map