/**
 * EO Closed-Loop Evolve Tool
 * Triggers the complete self-evolution cycle with automatic rule enforcement
 * 
 * This is the KEY tool that closes the loop:
 * Track → Analyze → Generate Rules → Persist → Enforce → Verify
 * 
 * Unlike eo_dream (which just analyzes), eo_evolve ENFORCES rules
 */
import { closedLoopEvolver, effectTracker, selfOptimizer } from '../autonomy/index.js';
import { textResult } from '../formatters/index.js';
interface EvolveParams {
    force?: boolean;
    dryRun?: boolean;
    status?: boolean;
}
export function handleEvolve(params: EvolveParams, api: any): any {
    const { force = false, dryRun = false, status = false } = params;
    // Status check
    if (status) {
        const s = closedLoopEvolver.getStatus();
        const lines: string[] = [
            '## 🔄 Closed-Loop Evolution Status',
            '',
            `**Enabled:** ${s.enabled ? '✅ Yes' : '❌ No'}`,
            `**Auto-Enforce:** ${s.autoEnforce ? '✅ Yes (rules auto-applied)' : '⚠️ No (manual enforcement only)'}`,
            `**Evolution Count:** ${s.evolutionCount}`,
            `**Cooldown:** ${s.cooldownHours}h`,
            `**Time Until Next:** ${s.timeUntilNextEvolution > 0 ? `${(s.timeUntilNextEvolution / 3600000).toFixed(1)}h` : 'Ready now'}`,
            '',
            `**Data:** ${s.currentDecisions}/${s.minDecisionsRequired} decisions (${s.hasEnoughData ? '✅ Enough' : '⏳ Need more'})`,
            '',
        ];
        // Add current rules
        const currentRules = closedLoopEvolver.getCurrentRules();
        if (currentRules.length > 0) {
            lines.push(`**Active Rules:** ${currentRules.length}`);
            for (const rule of currentRules) {
                lines.push(`- ${rule.name} (${rule.type}): ${rule.condition}`);
            }
        }
        else {
            lines.push('**Active Rules:** None');
        }
        // Add evolution history
        const history = closedLoopEvolver.getEvolutionHistory(5);
        if (history.length > 0) {
            lines.push('');
            lines.push('**Recent Evolutions:**');
            for (const h of history.reverse()) {
                lines.push(`- ${h.date?.split('T')[0]}: ${h.rulesGenerated || 0} rules, ${h.rulesEnforced || 0} enforced`);
            }
        }
        return textResult(lines.join('\n'));
    }
    // Force evolution
    if (force) {
        const result = closedLoopEvolver.forceEvolve(api);
        return formatEvolveResult(result);
    }
    // Dry run
    if (dryRun) {
        closedLoopEvolver.setAutoEnforce(false);
        const result = closedLoopEvolver.evolve(api);
        closedLoopEvolver.setAutoEnforce(true);
        return formatEvolveResult(result, true);
    }
    // Normal evolution
    const result = closedLoopEvolver.evolve(api);
    return formatEvolveResult(result);
}
function formatEvolveResult(result: any, isDryRun: boolean = false): any {
    if (!result.success) {
        const reasons: Record<string, string> = {
            disabled: '❌ Closed-loop evolution is disabled',
            cooldown: `⏳ Cooldown active: ${result.remainingHours}h remaining`,
            insufficient_data: `📊 Insufficient data: ${result.decisions}/${result.required} decisions`,
        };
        return textResult(`## 🔄 Evolution Result\n\n${reasons[result.reason] || 'Unknown reason'}`);
    }
    const lines: string[] = [
        '## 🔄 Closed-Loop Evolution Complete',
        '',
    ];
    if (isDryRun) {
        lines.push('⚠️ **DRY RUN** - Rules not actually applied');
    }
    lines.push(`**Rules Generated:** ${result.rulesGenerated}`);
    lines.push(`**Rules Enforced:** ${result.rulesEnforced}`);
    lines.push(`**Evolution Count:** #${result.evolutionCount}`);
    lines.push('');
    lines.push('### 📋 Generated Rules:');
    const rules = closedLoopEvolver.getCurrentRules();
    for (const rule of rules.slice(-5)) { // Show last 5
        lines.push(`- **${rule.name}** (${rule.type})`);
        lines.push(`  - Condition: ${rule.condition}`);
        lines.push(`  - Action: ${rule.action}`);
    }
    if (result.enforcementDetails?.results) {
        lines.push('');
        lines.push('### ✅ Enforcement Results:');
        for (const r of result.enforcementDetails.results) {
            const icon = r.success ? '✅' : '❌';
            lines.push(`${icon} ${r.agentId}: ${r.success ? 'Applied' : r.error}`);
        }
    }
    lines.push('');
    lines.push('**Note:** These rules are MANDATORY and have been written to agent SOUL.md files.');
    lines.push('Agents cannot ignore them - they are part of the agent identity.');
    return textResult(lines.join('\n'));
}
