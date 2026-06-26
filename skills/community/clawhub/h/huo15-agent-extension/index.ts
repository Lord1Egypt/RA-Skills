/**
 * huo15-agent-extension
 *
 * 动态Agent配置同步技能
 * 将主Agent的工作区配置同步到动态Agent工作区
 */

import * as fs from "fs";
import * as path from "path";
import * as os from "os";

/**
 * 获取主Agent工作目录
 */
function getMainAgentWorkspaceDir(): string {
    const homeDir = os.homedir();
    return path.join(homeDir, ".openclaw", "workspace");
}

/**
 * 获取动态Agent工作目录
 * 格式: ~/.openclaw/workspace-{agentId}
 */
function getDynamicAgentWorkspaceDir(agentId: string): string {
    const homeDir = os.homedir();
    return path.join(homeDir, ".openclaw", `workspace-${agentId}`);
}

/**
 * 需要同步的配置文件
 */
const CONFIG_FILES_TO_SYNC = [
    "AGENTS.md",
    "SOUL.md",
    "TOOLS.md",
    "IDENTITY.md",
    "USER.md",
    "HEARTBEAT.md",
    "MEMORY.md"
];

/**
 * 需要同步的目录
 */
const DIRS_TO_SYNC = [
    "skills",
    "memory"
];

/**
 * 同步单个配置文件
 * 配置文件始终以主Agent为准（覆盖目标文件）
 */
function syncConfigFile(sourcePath: string, targetPath: string): boolean {
    try {
        if (fs.existsSync(sourcePath)) {
            const targetDir = path.dirname(targetPath);
            if (!fs.existsSync(targetDir)) {
                fs.mkdirSync(targetDir, { recursive: true });
            }
            fs.copyFileSync(sourcePath, targetPath);
            return true;
        }
    } catch (err) {
        console.warn(`[huo15-agent-extension] 同步配置文件失败: ${sourcePath} -> ${targetPath}`, err);
    }
    return false;
}

/**
 * 同步目录（递归复制）
 * 目录始终以主Agent为准（有冲突就覆盖）
 */
function syncDir(sourceDir: string, targetDir: string): boolean {
    try {
        if (!fs.existsSync(sourceDir)) {
            return false;
        }

        if (!fs.existsSync(targetDir)) {
            fs.mkdirSync(targetDir, { recursive: true });
        }

        const entries = fs.readdirSync(sourceDir, { withFileTypes: true });
        for (const entry of entries) {
            const sourcePath = path.join(sourceDir, entry.name);
            const targetPath = path.join(targetDir, entry.name);

            if (entry.isDirectory()) {
                syncDir(sourcePath, targetPath);
            } else if (entry.isFile()) {
                // 始终以主Agent为准，覆盖目标文件
                fs.copyFileSync(sourcePath, targetPath);
            }
        }
        return true;
    } catch (err) {
        console.warn(`[huo15-agent-extension] 同步目录失败: ${sourceDir} -> ${targetDir}`, err);
    }
    return false;
}

/**
 * 同步主Agent配置到动态Agent
 *
 * @param agentId 动态Agent ID
 * @returns 同步结果
 */
export function syncMainAgentToDynamicAgent(agentId: string): {
    success: boolean;
    message: string;
    details: string[];
} {
    const mainWorkspace = getMainAgentWorkspaceDir();
    const dynamicWorkspace = getDynamicAgentWorkspaceDir(agentId);
    const details: string[] = [];

    if (!fs.existsSync(mainWorkspace)) {
        return {
            success: false,
            message: `主Agent工作目录不存在: ${mainWorkspace}`,
            details
        };
    }

    console.log(`[huo15-agent-extension] 同步主Agent配置到动态Agent: ${agentId}`);

    // 1. 同步配置文件（始终以主Agent为准）
    for (const file of CONFIG_FILES_TO_SYNC) {
        const sourcePath = path.join(mainWorkspace, file);
        const targetPath = path.join(dynamicWorkspace, file);
        if (syncConfigFile(sourcePath, targetPath)) {
            details.push(`✓ 同步配置文件: ${file}`);
        }
    }

    // 2. 同步目录（只复制不存在的文件）
    for (const dir of DIRS_TO_SYNC) {
        const sourcePath = path.join(mainWorkspace, dir);
        const targetPath = path.join(dynamicWorkspace, dir);
        if (syncDir(sourcePath, targetPath)) {
            details.push(`✓ 同步目录: ${dir}/`);
        }
    }

    return {
        success: true,
        message: `配置同步完成 for ${agentId}`,
        details
    };
}

/**
 * 获取所有动态Agent列表
 */
export function listDynamicAgents(): string[] {
    const workspaceDir = path.join(os.homedir(), ".openclaw");
    try {
        const entries = fs.readdirSync(workspaceDir);
        return entries
            .filter(name => name.startsWith("workspace-wecom-") || name.startsWith("workspace-"))
            .filter(name => !name.includes("memory") && !name.includes("skills"))
            .filter(name => fs.statSync(path.join(workspaceDir, name)).isDirectory());
    } catch {
        return [];
    }
}

export default {
    syncMainAgentToDynamicAgent,
    listDynamicAgents
};
