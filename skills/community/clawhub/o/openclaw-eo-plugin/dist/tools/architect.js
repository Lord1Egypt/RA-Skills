/**
 * EO Architect Tool Handler v3
 */
import { textResult } from '../formatters/index.js';
import { EXPERTS } from '../experts/data.js';
import { PLUGIN_VERSION } from '../config.js';
import { toolLogger } from '../utils/logger.js';
export async function handleArchitect(params) {
    const { task = 'System Design', style = 'layered', language = 'typescript', cloud = 'multi-cloud' } = params;
    const startTime = Date.now();
    toolLogger.log(`Architecture design for: ${task.slice(0, 50)}...`);
    try {
        // Architecture experts
        const expertNames = ['System Architect', 'Frontend Architect', 'Backend Architect', 'DevOps Engineer'];
        const experts = expertNames.map(name => {
            const expert = EXPERTS[name];
            return {
                name,
                description: expert?.description || 'Expert description'
            };
        });
        // Build output
        const lines = [
            `🏗️ **System Architecture Design v${PLUGIN_VERSION}**`,
            ``,
            `**Task:** ${task}`,
            `**Style:** ${style} | **Language:** ${language} | **Cloud:** ${cloud}`,
            ``,
            `**Expert Contributions:** ${experts.length}`,
            ``
        ];
        for (const expert of experts) {
            lines.push(`### ${expert.name}`);
            lines.push(expert.description);
            lines.push(``);
        }
        lines.push(`---`);
        lines.push(`**Suggested Subagent Spawning:**`);
        lines.push(``);
        lines.push(`\`\`\``);
        for (const expert of experts) {
            lines.push(`sessions_spawn({`);
            lines.push(`  task: "作为 ${expert.name}，请为以下系统提供架构设计：${task}",`);
            lines.push(`  runtime: "subagent",`);
            lines.push(`  timeout: 180000`);
            lines.push(`})`);
        }
        lines.push(`\`\`\``);
        lines.push(``);
        lines.push(`⏱️ Duration: ${Date.now() - startTime}ms`);
        return textResult(lines.join('\n'), {
            success: true,
            expertCount: experts.length,
            durationMs: Date.now() - startTime
        });
    }
    catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err);
        console.error(`[eo_architect v3] Error: ${errorMsg}`);
        return textResult(`🏗️ **System Architecture Error:** ${errorMsg}`, {
            success: false,
            error: errorMsg
        });
    }
}
//# sourceMappingURL=architect.js.map