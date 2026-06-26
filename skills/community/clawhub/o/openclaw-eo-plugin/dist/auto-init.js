/**
 * EO Auto-Init Module
 *
 * Automatically configures all agent workspaces with EO-Enhanced SOUL.md
 * Runs on plugin installation/load to enable full EO capabilities
 */
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
// ============================================================================
// Constants
// ============================================================================
const PLUGIN_NAME = 'eo-collaboration';
const OPENCLAW_CONFIG = '.openclaw/openclaw.json';
const SOUL_EO_ADDON = `---

## 🚀 EO-Enhanced 能力（自动配置）

### 可用工具

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| \`eo_collab\` | 多专家协作 | 复杂任务需要多方专家 |
| \`eo_plan\` | 项目规划 | WBS生成、里程碑设定 |
| \`eo_architect\` | 架构设计 | 系统设计、技术选型 |
| \`eo_verify\` | 检查点验证 | 阶段交付物验证 |
| \`eo_code_review\` | 代码审查 | 安全、性能、风格 |
| \`eo_list_experts\` | 专家列表 | 查看141专家库 |

### 141专家军团

当遇到问题时，"召唤"对应领域专家：

| 问题类型 | 召唤专家分类 |
|---------|------------|
| 项目规划 | \`marketing\`, \`sales\`, \`product\` |
| 技术架构 | \`engineering\`, \`specialized\` |
| 营销文案 | \`marketing\` |
| 视觉设计 | \`design\` |
| 代码开发 | \`engineering\` |
| 安全审计 | \`specialized\` (security) |
| 部署运维 | \`engineering\` (DevOps) |
| 学术写作 | \`academic\` |
| 测试验证 | \`testing\` |

### 多专家协作流程

\`\`\`
接到任务
    ↓
Planner 规划 → 确定方案
    ↓
多专家并行执行（2-4个同时）
    ↓
Checkpoint 验证
    ↓
输出结果 → 自动记录
\`\`\`

### 主动感知规则

| 条件 | 自动执行 |
|------|---------|
| 复杂任务（多领域） | 触发\`eo_collab\` |
| 项目规划需求 | 触发\`eo_plan\` |
| 架构设计需求 | 触发\`eo_architect\` |
| 代码审查需求 | 触发\`eo_code_review\` |
| 验证检查点 | 触发\`eo_verify\` |
| 上下文>70% | 触发ContextSummarizer |
| 会话结束 | 触发GlobalMemory同步 |
| 30分钟空闲 | 触发Dream Module |

_🦞⚙️ EO-Enhanced Mode - Auto-configured by EO Plugin_
`;
// ============================================================================
// Helper Functions
// ============================================================================
function getHomeDir() {
    return homedir();
}
function loadOpenClawConfig() {
    const configPath = join(getHomeDir(), OPENCLAW_CONFIG);
    if (!existsSync(configPath)) {
        throw new Error(`OpenClaw config not found: ${configPath}`);
    }
    const content = readFileSync(configPath, 'utf-8');
    return JSON.parse(content);
}
function getAgentList(config) {
    const agents = config.agents?.list || [];
    return agents.map((a) => ({
        id: a.id,
        name: a.name || a.id,
        workspace: a.workspace || join(getHomeDir(), '.openclaw/workspace', `workspace-${a.id}`),
    }));
}
function workspaceExists(workspace) {
    try {
        return existsSync(workspace);
    }
    catch {
        return false;
    }
}
function readSoul(workspace) {
    const soulPath = join(workspace, 'SOUL.md');
    if (existsSync(soulPath)) {
        return readFileSync(soulPath, 'utf-8');
    }
    return null;
}
function isEOEnhanced(soul) {
    return soul !== null && soul.includes('EO-Enhanced');
}
function writeSoul(workspace, content) {
    const soulPath = join(workspace, 'SOUL.md');
    writeFileSync(soulPath, content, 'utf-8');
}
function generateEOSoul(existingSoul, agentId) {
    if (!existingSoul) {
        // Create new SOUL.md
        return `# SOUL.md - ${agentId}

_EO-Enhanced Agent - Auto-configured by EO Plugin_

${SOUL_EO_ADDON}
`;
    }
    if (isEOEnhanced(existingSoul)) {
        return null; // Already EO version
    }
    // Append EO addon to existing SOUL
    return `${existingSoul}\n${SOUL_EO_ADDON}\n`;
}
// ============================================================================
// Main Functions
// ============================================================================
/**
 * Run auto-initialization for all agent workspaces
 */
export async function runAutoInit(api, options = {}) {
    const { force = false, dryRun = false, agentIds } = options;
    api.logger.info('[EO Auto-Init] Starting EO agent auto-configuration...');
    // Load config and get agent list
    let config;
    try {
        config = loadOpenClawConfig();
    }
    catch (e) {
        api.logger.error(`[EO Auto-Init] Failed to load config: ${e.message}`);
        return { total: 0, success: 0, skipped: 0, failed: 1, results: [] };
    }
    let agents = getAgentList(config);
    // Filter by agentIds if specified
    if (agentIds && agentIds.length > 0) {
        agents = agents.filter(a => agentIds.includes(a.id));
    }
    api.logger.info(`[EO Auto-Init] Found ${agents.length} agent workspaces`);
    const results = [];
    let success = 0;
    let skipped = 0;
    let failed = 0;
    for (const agent of agents) {
        const result = {
            agentId: agent.id,
            workspace: agent.workspace,
            status: 'skipped',
        };
        // Check workspace exists
        if (!workspaceExists(agent.workspace)) {
            result.status = 'failed';
            result.reason = 'workspace not found';
            failed++;
            results.push(result);
            api.logger.debug(`[EO Auto-Init] ${agent.id}: workspace not found`);
            continue;
        }
        // Read existing SOUL
        const existingSoul = readSoul(agent.workspace);
        // Check if already EO
        if (existingSoul && isEOEnhanced(existingSoul) && !force) {
            result.status = 'skipped';
            result.reason = 'already EO-Enhanced';
            skipped++;
            results.push(result);
            api.logger.debug(`[EO Auto-Init] ${agent.id}: already EO-Enhanced`);
            continue;
        }
        // Generate new SOUL
        const newSoul = generateEOSoul(existingSoul, agent.id);
        if (!newSoul) {
            result.status = 'skipped';
            result.reason = 'already EO-Enhanced';
            skipped++;
            results.push(result);
            continue;
        }
        if (dryRun) {
            result.status = 'skipped';
            result.reason = 'dry-run mode';
            skipped++;
            api.logger.info(`[EO Auto-Init] ${agent.id}: [DRY-RUN] would configure`);
        }
        else {
            try {
                writeSoul(agent.workspace, newSoul);
                result.status = 'success';
                success++;
                api.logger.info(`[EO Auto-Init] ${agent.id}: ✅ configured`);
            }
            catch (e) {
                result.status = 'failed';
                result.error = e.message;
                failed++;
                api.logger.error(`[EO Auto-Init] ${agent.id}: failed - ${e.message}`);
            }
        }
        results.push(result);
    }
    const summary = { total: agents.length, success, skipped, failed, results };
    api.logger.info(`[EO Auto-Init] Complete: ${success} success, ${skipped} skipped, ${failed} failed`);
    return summary;
}
/**
 * Check if auto-init has been run before
 */
export function isAutoInitDone() {
    // In a full implementation, this would check a flag in openclaw.json
    // For now, we just check if the function exists
    return true;
}
//# sourceMappingURL=auto-init.js.map