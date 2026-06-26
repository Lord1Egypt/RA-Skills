/**
 * EO Plan Tool Handler v5
 * Simplified - returns structured plan directly
 */
import { textResult } from '../formatters/index.js';
import { EXPERTS } from '../experts/data.js';
import { PLUGIN_VERSION } from '../config.js';
import { toolLogger } from '../utils/logger.js';
export async function handlePlan(params) {
    const task = params?.task || 'New Project';
    const priority = params?.priority || 'medium';
    const teamTemplate = params?.team || 'fullstack';
    const startTime = Date.now();
    toolLogger.log(`Planning: ${task.slice(0, 50)}...`);
    try {
        // Define expert team for planning
        const expertConfigs = {
            fullstack: ['Project Planner', 'Tech Lead', 'QA Engineer', 'DevOps Engineer'],
            web: ['Project Planner', 'Frontend Lead', 'Backend Lead'],
            mobile: ['Project Planner', 'Mobile Lead', 'UI/UX Designer'],
            data: ['Data Architect', 'ML Engineer', 'Data Engineer']
        };
        const expertNames = expertConfigs[teamTemplate] || expertConfigs.fullstack;
        // Build output directly
        const lines = [
            `📋 **EO Project Plan v${PLUGIN_VERSION}**`,
            ``,
            `**Task:** ${task}`,
            `**Priority:** ${priority}`,
            `**Team:** ${teamTemplate}`,
            ``,
            `---`,
            ``,
            `## Expert Team (${expertNames.length} experts)`,
            ``
        ];
        for (let i = 0; i < expertNames.length; i++) {
            const name = expertNames[i];
            const expert = EXPERTS[name];
            lines.push(`${i + 1}. **${name}**`);
            lines.push(`   - ${expert?.description || 'Expert description'}`);
            lines.push(``);
        }
        lines.push(`---`);
        lines.push(``);
        lines.push(`## Suggested Subagent Spawning`);
        lines.push(``);
        lines.push(`\`\`\``);
        for (const name of expertNames) {
            lines.push(`sessions_spawn({`);
            lines.push(`  task: "作为 ${name}，请为以下任务提供专业建议：${task}",`);
            lines.push(`  runtime: "subagent",`);
            lines.push(`  timeout: 120000`);
            lines.push(`})`);
        }
        lines.push(`\`\`\``);
        lines.push(``);
        lines.push(`⏱️ Duration: ${Date.now() - startTime}ms`);
        return textResult(lines.join('\n'), {
            success: true,
            expertCount: expertNames.length,
            durationMs: Date.now() - startTime,
            hasStructuredPlan: true
        });
    }
    catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err);
        console.error(`[eo_plan v5] Error: ${errorMsg}`);
        return textResult(`❌ **Plan Error:** ${errorMsg}`, {
            success: false,
            error: errorMsg
        });
    }
}
//# sourceMappingURL=plan.js.map