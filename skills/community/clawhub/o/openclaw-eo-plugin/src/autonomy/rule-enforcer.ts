/**
 * Rule Enforcer - Applies mandatory rules to agent SOUL.md files
 * 
 * This is the CRITICAL piece that closes the loop:
 * Evolution generates rules → Enforcer writes them to SOUL.md → Agent MUST follow
 * 
 * Rules are not suggestions - they become part of the agent's identity
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { appendEvolutionLog } from './rule-persistence.js';
const OPENCLAW_CONFIG = '.openclaw/openclaw.json';
const SOUL_MARKER_START = '<!-- EO MANDATORY RULES START -->';
const SOUL_MARKER_END = '<!-- EO MANDATORY RULES END -->';
/**
 * Get home directory
 */
function getHomeDir(): string {
    return homedir();
}
/**
 * Load openclaw config to get agent list
 */
function loadOpenClawConfig(): any {
    const configPath = join(getHomeDir(), OPENCLAW_CONFIG);
    if (!existsSync(configPath)) {
        throw new Error(`OpenClaw config not found: ${configPath}`);
    }
    return JSON.parse(readFileSync(configPath, 'utf-8'));
}
/**
 * Get all agent workspaces
 */
function getAgentWorkspaces(): { id: string; name: string; workspace: string }[] {
    const config = loadOpenClawConfig();
    const agents = config.agents?.list || [];
    return agents.map((a: any) => ({
        id: a.id,
        name: a.name || a.id,
        workspace: a.workspace || join(getHomeDir(), '.openclaw/workspace', `workspace-${a.id}`),
    }));
}
/**
 * Check if workspace exists
 */
function workspaceExists(ws: string): boolean {
    try {
        return existsSync(ws);
    }
    catch {
        return false;
    }
}
/**
 * Read SOUL.md from workspace
 */
function readSoul(workspace: string): string | null {
    const soulPath = join(workspace, 'SOUL.md');
    if (!existsSync(soulPath)) {
        return null;
    }
    return readFileSync(soulPath, 'utf-8');
}
/**
 * Write SOUL.md to workspace
 */
function writeSoul(workspace: string, content: string): void {
    const soulPath = join(workspace, 'SOUL.md');
    writeFileSync(soulPath, content, 'utf-8');
}
/**
 * Generate mandatory rules section for SOUL.md
 */
function generateRulesSection(rules: any[], metadata: any): string {
    const ruleLines: string[] = [
        SOUL_MARKER_START,
        '',
        `**⚠️ 这些是强制规则，不可忽略**`,
        '',
    ];
    for (const rule of rules) {
        ruleLines.push(`### ${rule.name}`);
        ruleLines.push(`**类型**: ${rule.type}`);
        ruleLines.push(`**触发条件**: ${rule.condition}`);
        ruleLines.push(`**强制行为**: ${rule.action}`);
        if (rule.parameters) {
            ruleLines.push(`**参数**: \`${JSON.stringify(rule.parameters)}\``);
        }
        if (rule.examples) {
            ruleLines.push(`**示例**: ${rule.examples}`);
        }
        ruleLines.push('');
    }
    ruleLines.push(`*生成时间: ${new Date().toISOString()} | 规则数: ${rules.length}*`);
    ruleLines.push(SOUL_MARKER_END);
    return ruleLines.join('\n');
}
/**
 * Insert or update mandatory rules in SOUL.md
 */
function insertRulesIntoSoul(soul: string, rules: any[], metadata: any): string {
    const rulesSection = generateRulesSection(rules, metadata);
    // If already has rules, replace them
    if (soul.includes(SOUL_MARKER_START)) {
        const startIdx = soul.indexOf(SOUL_MARKER_START);
        const endIdx = soul.indexOf(SOUL_MARKER_END) + SOUL_MARKER_END.length;
        return soul.substring(0, startIdx) + rulesSection + soul.substring(endIdx);
    }
    // Otherwise append at the end
    return soul + '\n\n' + rulesSection;
}
/**
 * Apply rules to a specific agent's SOUL.md
 */
export function applyRulesToAgent(agentId: string, rules: any[], dryRun: boolean = false): any {
    const workspaces = getAgentWorkspaces();
    const workspace = workspaces.find((w) => w.id === agentId);
    if (!workspace) {
        return { success: false, error: `Agent ${agentId} not found` };
    }
    if (!workspaceExists(workspace.workspace)) {
        return { success: false, error: `Workspace not found: ${workspace.workspace}` };
    }
    const soul = readSoul(workspace.workspace);
    if (!soul) {
        return { success: false, error: 'SOUL.md not found' };
    }
    if (dryRun) {
        return {
            success: true,
            dryRun: true,
            agentId,
            workspace: workspace.workspace,
            newSoulPreview: insertRulesIntoSoul(soul, rules, {}).substring(0, 500) + '...',
        };
    }
    const newSoul = insertRulesIntoSoul(soul, rules, {});
    writeSoul(workspace.workspace, newSoul);
    return {
        success: true,
        agentId,
        workspace: workspace.workspace,
        rulesApplied: rules.length,
    };
}
/**
 * Apply rules to ALL agent workspaces
 */
export function applyRulesToAllAgents(rules: any[], options: any = {}): any {
    const { dryRun = false, agentIds } = options;
    const workspaces = getAgentWorkspaces();
    const filtered = agentIds ? workspaces.filter((w) => agentIds.includes(w.id)) : workspaces;
    const results = [];
    for (const ws of filtered) {
        if (!workspaceExists(ws.workspace)) {
            results.push({ agentId: ws.id, success: false, error: 'workspace not found' });
            continue;
        }
        const result = applyRulesToAgent(ws.id, rules, dryRun);
        results.push(result);
    }
    return {
        total: filtered.length,
        success: results.filter((r: any) => r.success && !r.dryRun).length,
        dryRun: results.filter((r: any) => r.dryRun).length,
        failed: results.filter((r: any) => !r.success).length,
        results,
    };
}
/**
 * Extract current mandatory rules from a SOUL.md
 */
export function extractRulesFromSoul(soul: string): any[] {
    if (!soul || !soul.includes(SOUL_MARKER_START)) {
        return [];
    }
    const startIdx = soul.indexOf(SOUL_MARKER_START);
    const endIdx = soul.indexOf(SOUL_MARKER_END);
    const rulesSection = soul.substring(startIdx + SOUL_MARKER_START.length, endIdx);
    // Parse rules from the section (simplified)
    const rules: any[] = [];
    const ruleBlocks = rulesSection.split('### ').filter((b) => b.trim());
    for (const block of ruleBlocks) {
        const lines = block.split('\n').filter((l) => l.trim());
        if (lines.length > 0) {
            const name = lines[0].trim();
            const typeMatch = block.match(/\*\*类型\*\*: (.+)/);
            const conditionMatch = block.match(/\*\*触发条件\*\*: (.+)/);
            const actionMatch = block.match(/\*\*强制行为\*\*: (.+)/);
            if (name && typeMatch && conditionMatch && actionMatch) {
                rules.push({
                    name,
                    type: typeMatch[1].trim(),
                    condition: conditionMatch[1].trim(),
                    action: actionMatch[1].trim(),
                });
            }
        }
    }
    return rules;
}
/**
 * Generate rules from evolution analysis
 */
export function generateRulesFromEvolution(evolutionResult: any, stats: any): any[] {
    const rules: any[] = [];
    // High performance rule
    if (evolutionResult.newRules.includes('high_performance_threshold:75')) {
        rules.push({
            name: 'high_performance_mode',
            type: 'performance',
            condition: '当 avgScore > 75 且 successRate > 0.7',
            action: '启用激进策略，减少确认步骤以提升效率',
            examples: 'multi_expert_collaboration → batch_size:6',
        });
    }
    // Conservative mode rule
    if (evolutionResult.retiredRules.includes('aggressive_default')) {
        rules.push({
            name: 'conservative_mode',
            type: 'safety',
            condition: '当 successRate < 0.6',
            action: '切换到保守策略，增加确认步骤',
            examples: '每步操作前要求用户确认',
        });
    }
    // Low score alert rule
    if (stats.avgScore < 50) {
        rules.push({
            name: 'low_score_alert',
            type: 'safety',
            condition: '当 avgScore < 50',
            action: '立即切换到保守模式，停止自动执行',
            examples: '暂停所有多专家协作，启动人工干预',
        });
    }
    // Success rate warning
    if (stats.successRate < 0.5) {
        rules.push({
            name: 'success_rate_warning',
            type: 'safety',
            condition: '当 successRate < 0.5',
            action: '降低batch size，增加验证步骤',
            examples: 'batch_size:2, verify_each:true',
        });
    }
    // Trend following
    if (stats.trend === 'declining') {
        rules.push({
            name: 'declining_trend_response',
            type: 'adaptive',
            condition: '当 trend === declining',
            action: '立即减少batch size，回退到保守配置',
            examples: 'batch_size:1, confirmation_required:true',
        });
    }
    return rules;
}
