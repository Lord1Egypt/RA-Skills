/**
 * **动态 Agent 路由模块**
 *
 * 为每个用户/群组自动生成独立的 Agent ID + workspace + agentDir，实现会话隔离。
 * v2.9.0 ⭐ 补全 workspace/agentDir/bindings 持久化（之前只写 cfg.agents.list 的 {id}，
 * 不写 workspace/agentDir 也不写 cfg.bindings → OpenClaw 不知道把 inbound route 到哪个 agent，
 * 全部 fallback 回 main，所谓"动态 agent"形同虚设）。
 *
 * 参考：OpenClaw 自带 feishu 内置 channel 的 monitor.ts 派生逻辑
 * （node_modules/openclaw/dist/extensions/feishu/monitor-DDkD5r4p.js）。
 */

import os from "node:os";
import path from "node:path";

import type { OpenClawConfig } from "openclaw/plugin-sdk";

export interface DynamicAgentConfig {
    enabled: boolean;
    dmCreateAgent: boolean;
    groupEnabled: boolean;
    adminUsers: string[];
    /** 模板字符串，支持 {agentId} / {userId} / {accountId} / {peerId} / {chatType} 占位符。
     *  默认 ~/.openclaw/workspace-{agentId} —— 与 OpenClaw 核心 resolveAgentWorkspaceDir
     *  兜底分支一致。 */
    workspaceTemplate: string;
    /** 默认 ~/.openclaw/agents/{agentId}/agent —— 与 feishu 内置实现一致。 */
    agentDirTemplate: string;
    /** 防滥用上限。超过后新派生请求降级回 main 不再写入 cfg。默认 100。 */
    maxAgents: number;
    /** v2.9.2 ⭐ 派生新 workspace 时，从 main agent workspace 复制身份/约定文件
     *  （IDENTITY/SOUL/USER/AGENTS）。避免每个新派生 workspace 都触发 OpenClaw 核心
     *  的 BOOTSTRAP "我是谁/你是谁" 引导脚本——老用户已经配过主工作区，新派生应该继承。
     *  默认 true。 */
    seedFromMainWorkspace: boolean;
    /** 种子复制清单（相对 workspace 根的文件名）。默认 ['IDENTITY.md','SOUL.md','USER.md','AGENTS.md']。
     *  不复制 BOOTSTRAP.md（避免触发引导）/ MEMORY.md / HEARTBEAT.md（per-agent 应该独立）。 */
    seedFiles: string[];
    /** main agent workspace 路径，默认从 cfg.agents.defaults.workspace 读取。 */
    mainWorkspacePath?: string;
}

const DEFAULT_WORKSPACE_TEMPLATE = "~/.openclaw/workspace-{agentId}";
const DEFAULT_AGENT_DIR_TEMPLATE = "~/.openclaw/agents/{agentId}/agent";
const DEFAULT_MAX_AGENTS = 100;
const DEFAULT_SEED_FILES = ["IDENTITY.md", "SOUL.md", "USER.md", "AGENTS.md"];

/**
 * **getDynamicAgentConfig (读取动态 Agent 配置)**
 *
 * 从 channels.wecom.dynamicAgents 读取配置，提供合理默认值。v2.9.0 起 enabled 默认 true，
 * 让"开箱即用"——之前 false 导致 90% 用户压根没启用，所有群消息汇到 main。
 */
export function getDynamicAgentConfig(config: OpenClawConfig): DynamicAgentConfig {
    const dynamicAgents = (config as { channels?: { wecom?: { dynamicAgents?: Partial<DynamicAgentConfig> } } })?.channels?.wecom?.dynamicAgents;
    const mainWorkspaceFromAgents = (config as { agents?: { defaults?: { workspace?: string } } })?.agents?.defaults?.workspace;
    return {
        enabled: dynamicAgents?.enabled ?? true,
        dmCreateAgent: dynamicAgents?.dmCreateAgent ?? true,
        groupEnabled: dynamicAgents?.groupEnabled ?? true,
        adminUsers: dynamicAgents?.adminUsers ?? [],
        workspaceTemplate: dynamicAgents?.workspaceTemplate?.trim() || DEFAULT_WORKSPACE_TEMPLATE,
        agentDirTemplate: dynamicAgents?.agentDirTemplate?.trim() || DEFAULT_AGENT_DIR_TEMPLATE,
        maxAgents:
            typeof dynamicAgents?.maxAgents === "number" && dynamicAgents.maxAgents > 0
                ? Math.floor(dynamicAgents.maxAgents)
                : DEFAULT_MAX_AGENTS,
        seedFromMainWorkspace: dynamicAgents?.seedFromMainWorkspace ?? true,
        seedFiles:
            Array.isArray(dynamicAgents?.seedFiles) && dynamicAgents.seedFiles.length > 0
                ? dynamicAgents.seedFiles
                : DEFAULT_SEED_FILES,
        mainWorkspacePath: dynamicAgents?.mainWorkspacePath || mainWorkspaceFromAgents,
    };
}

function sanitizeDynamicIdPart(value: string): string {
    return String(value)
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9_-]/g, "_");
}

/**
 * **generateAgentId (生成动态 Agent ID)**
 *
 * 根据账号 + 聊天类型 + 对端 ID 生成确定性的 Agent ID，避免多账号串会话。
 * 格式: wecom-{accountId}-{type}-{sanitizedPeerId}
 */
export function generateAgentId(chatType: "dm" | "group", peerId: string, accountId?: string): string {
    const sanitizedPeer = sanitizeDynamicIdPart(peerId) || "unknown";
    const sanitizedAccountId = sanitizeDynamicIdPart(accountId ?? "default") || "default";
    return `wecom-${sanitizedAccountId}-${chatType}-${sanitizedPeer}`;
}

export function buildAgentSessionTarget(userId: string, accountId?: string): string {
    const normalizedUserId = String(userId).trim();
    const sanitizedAccountId = sanitizeDynamicIdPart(accountId ?? "default") || "default";
    return `wecom-agent:${sanitizedAccountId}:user:${normalizedUserId}`;
}

/**
 * **shouldUseDynamicAgent (检查是否使用动态 Agent)**
 */
export function shouldUseDynamicAgent(params: {
    chatType: "dm" | "group";
    senderId: string;
    config: OpenClawConfig;
}): boolean {
    const { chatType, senderId, config } = params;
    const dynamicConfig = getDynamicAgentConfig(config);

    if (!dynamicConfig.enabled) {
        return false;
    }

    const sender = String(senderId).trim().toLowerCase();
    const isAdmin = dynamicConfig.adminUsers.some(
        (admin) => admin.trim().toLowerCase() === sender
    );
    if (isAdmin) {
        return false;
    }

    if (chatType === "group") {
        return dynamicConfig.groupEnabled;
    }
    return dynamicConfig.dmCreateAgent;
}

function resolveUserPath(p: string): string {
    if (!p) return p;
    if (p === "~") return os.homedir();
    if (p.startsWith("~/")) return path.join(os.homedir(), p.slice(2));
    return p;
}

/**
 * **seedWorkspaceFromMain (v2.9.2)** — 把 main agent workspace 的身份/约定文件复制到新派生 workspace。
 *
 * Why: OpenClaw 核心 SessionStart 看到 fresh workspace 会自动写 BOOTSTRAP.md 触发"我是谁/你是谁"
 * 5 步引导。老用户在主工作区已经配过 IDENTITY/SOUL/USER，新派生 workspace 应该继承——否则每个
 * 群/DM 第一次对话都要重走引导。复制后 OpenClaw 核心检测到 IDENTITY 已存在 → 跳过 BOOTSTRAP。
 *
 * 复制策略：
 * - 只复制清单里的文件（默认 IDENTITY/SOUL/USER/AGENTS）
 * - **不复制 BOOTSTRAP**（避免引导触发）
 * - **不复制 MEMORY/HEARTBEAT**（每个 agent 独立记忆和心跳）
 * - main 缺某个文件 = skip 不报错（部分种子也比没种子强）
 * - 目标已存在 = skip（幂等，不覆盖用户后续在该 workspace 的修改）
 */
async function seedWorkspaceFromMain(params: {
    targetWorkspace: string;
    mainWorkspace: string | undefined;
    seedFiles: string[];
}): Promise<{ copied: string[]; skipped: string[] }> {
    const copied: string[] = [];
    const skipped: string[] = [];
    if (!params.mainWorkspace) {
        return { copied, skipped: params.seedFiles.map((f) => `${f}:no-main-ws`) };
    }
    const mainAbs = resolveUserPath(params.mainWorkspace);
    if (mainAbs === params.targetWorkspace) {
        // 派生 workspace 与 main 是同一目录（admin 用户 / 配置错），无需复制
        return { copied, skipped: params.seedFiles.map((f) => `${f}:same-dir`) };
    }
    const fs = await import("node:fs/promises");
    for (const filename of params.seedFiles) {
        const src = path.join(mainAbs, filename);
        const dst = path.join(params.targetWorkspace, filename);
        try {
            // 目标已存在 → 跳过（幂等 + 不覆盖）
            try {
                await fs.access(dst);
                skipped.push(`${filename}:dst-exists`);
                continue;
            } catch {
                // 目标不存在，继续复制
            }
            // 源不存在 → 跳过不报错
            try {
                await fs.access(src);
            } catch {
                skipped.push(`${filename}:src-missing`);
                continue;
            }
            await fs.copyFile(src, dst);
            copied.push(filename);
        } catch (err) {
            skipped.push(`${filename}:error:${(err as Error)?.message ?? "unknown"}`);
        }
    }
    return { copied, skipped };
}

function renderTemplate(template: string, vars: Record<string, string>): string {
    return template.replace(/\{(\w+)\}/g, (full, key: string) => vars[key] ?? full);
}

/**
 * 内存中已确保的 Agent ID（避免重复写入）
 */
const ensuredDynamicAgentIds = new Set<string>();

/**
 * 写入队列（避免并发冲突）
 */
let ensureDynamicAgentWriteQueue: Promise<void> = Promise.resolve();

interface AgentListEntry {
    id: string;
    workspace?: string;
    agentDir?: string;
}

interface AgentBindingEntry {
    type?: "route" | "acp";
    agentId: string;
    match: {
        channel: string;
        accountId?: string;
        peer?: { kind: "direct" | "group"; id: string };
    };
}

/**
 * 在 cfg.agents.list 找现有 entry（按 id 大小写不敏感）。返回 -1 = 没找到。
 */
function findAgentListIndex(list: AgentListEntry[], agentId: string): number {
    const norm = agentId.trim().toLowerCase();
    for (let i = 0; i < list.length; i++) {
        if ((list[i]?.id ?? "").trim().toLowerCase() === norm) return i;
    }
    return -1;
}

function findBindingIndex(
    bindings: AgentBindingEntry[],
    agentId: string,
    match: AgentBindingEntry["match"],
): number {
    const norm = agentId.trim().toLowerCase();
    for (let i = 0; i < bindings.length; i++) {
        const b = bindings[i];
        if (!b) continue;
        if ((b.agentId ?? "").trim().toLowerCase() !== norm) continue;
        const m = b.match;
        if (!m) continue;
        if (m.channel !== match.channel) continue;
        if ((m.accountId ?? "") !== (match.accountId ?? "")) continue;
        const pa = m.peer;
        const pb = match.peer;
        if (!pa && !pb) return i;
        if (!pa || !pb) continue;
        if (pa.kind !== pb.kind) continue;
        if ((pa.id ?? "") !== (pb.id ?? "")) continue;
        return i;
    }
    return -1;
}

/**
 * 升级 cfg：补全 agents.list[i].workspace/agentDir + 写 cfg.bindings 路由。
 * 返回 true = 改了任何字段需要 writeConfigFile。
 */
function upsertAgentEntryAndBinding(
    cfg: Record<string, unknown>,
    params: {
        agentId: string;
        chatType: "dm" | "group";
        peerId: string;
        accountId: string;
        workspace: string;
        agentDir: string;
        maxAgents: number;
    },
): { changed: boolean; rejectedOverLimit: boolean } {
    if (!cfg.agents || typeof cfg.agents !== "object") {
        cfg.agents = {};
    }
    const agentsObj = cfg.agents as Record<string, unknown>;
    const list: AgentListEntry[] = Array.isArray(agentsObj.list)
        ? (agentsObj.list as AgentListEntry[])
        : [];

    let changed = false;

    // 首次创建时保留 main 作为默认
    if (list.length === 0) {
        list.push({ id: "main" });
        changed = true;
    }

    const idx = findAgentListIndex(list, params.agentId);
    if (idx === -1) {
        // 派生新 agent 之前先看上限。注意：list 里包含的 main + 历史已有的 wecom- 派生 agent 都算，
        // 这是有意的——上限保护 cfg 不无限膨胀。
        const dynamicCount = list.filter((e) => e.id?.startsWith("wecom-")).length;
        if (dynamicCount >= params.maxAgents) {
            return { changed, rejectedOverLimit: true };
        }
        list.push({
            id: params.agentId,
            workspace: params.workspace,
            agentDir: params.agentDir,
        });
        changed = true;
    } else {
        // 已存在但缺 workspace/agentDir → 补上（v2.8.x 旧版本只写了 {id}，迁移补齐）
        const existing = list[idx]!;
        if (existing.workspace !== params.workspace || existing.agentDir !== params.agentDir) {
            list[idx] = {
                ...existing,
                workspace: params.workspace,
                agentDir: params.agentDir,
            };
            changed = true;
        }
    }

    if (changed) {
        agentsObj.list = list;
    }

    // 写 cfg.bindings —— 没这一条 OpenClaw 核心 routing 不会派去新 agent
    const bindingsList: AgentBindingEntry[] = Array.isArray(cfg.bindings)
        ? (cfg.bindings as AgentBindingEntry[])
        : [];
    const peerKind: "direct" | "group" = params.chatType === "group" ? "group" : "direct";
    const matchSpec: AgentBindingEntry["match"] = {
        channel: "wecom",
        accountId: params.accountId,
        peer: { kind: peerKind, id: params.peerId },
    };
    if (findBindingIndex(bindingsList, params.agentId, matchSpec) === -1) {
        bindingsList.push({
            type: "route",
            agentId: params.agentId,
            match: matchSpec,
        });
        cfg.bindings = bindingsList;
        changed = true;
    }

    return { changed, rejectedOverLimit: false };
}

/**
 * **ensureDynamicAgentListed (确保动态 Agent 已注册并能被 dispatch route 到)**
 *
 * v2.9.0 升级：除了把 agentId 写进 cfg.agents.list，还补：
 * 1. workspace + agentDir（按 dynamicAgents.workspaceTemplate / agentDirTemplate 渲染）
 * 2. mkdir -p workspace + agentDir
 * 3. cfg.bindings 加路由 entry { agentId, match: { channel, accountId, peer } }
 *
 * 这三条缺一不可——少 binding OpenClaw 核心不会 route 过去；少 workspace agent 落到错的 cwd。
 *
 * 接口幂等：内存 Set + 写入队列 + cfg snapshot 检查 = 重复调用不做无谓写入。
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export async function ensureDynamicAgentListed(params: {
    agentId: string;
    chatType: "dm" | "group";
    peerId: string;
    accountId: string;
    runtime: any;
}): Promise<void> {
    const normalizedId = String(params.agentId).trim().toLowerCase();
    if (!normalizedId) return;
    if (ensuredDynamicAgentIds.has(normalizedId)) return;

    const configRuntime = params.runtime?.config;
    if (!configRuntime?.loadConfig || !configRuntime?.writeConfigFile) return;

    ensureDynamicAgentWriteQueue = ensureDynamicAgentWriteQueue
        .then(async () => {
            if (ensuredDynamicAgentIds.has(normalizedId)) return;

            const baseConfig = configRuntime.loadConfig!() as OpenClawConfig | null | undefined;
            if (!baseConfig || typeof baseConfig !== "object") return;

            // v2.9.0 ⭐ 深拷贝再 mutate —— OpenClaw 核心 writeConfigFile 用
            // `createMergePatch(runtimeConfigSnapshot, cfg)` 算 diff 决定写什么。
            // 直接 mutate loadConfig() 返回的对象 = mutate runtime snapshot 本体 = patch 算出来空 = 文件没变。
            // 必须先 structuredClone 拿独立副本，让 mergePatch 看到差异。
            const cloned = typeof structuredClone === "function"
                ? structuredClone(baseConfig)
                : JSON.parse(JSON.stringify(baseConfig));

            const dynCfg = getDynamicAgentConfig(cloned);
            const templateVars: Record<string, string> = {
                agentId: params.agentId,
                userId: params.peerId,
                accountId: params.accountId,
                peerId: params.peerId,
                chatType: params.chatType,
            };
            const workspace = resolveUserPath(renderTemplate(dynCfg.workspaceTemplate, templateVars));
            const agentDir = resolveUserPath(renderTemplate(dynCfg.agentDirTemplate, templateVars));

            const result = upsertAgentEntryAndBinding(
                cloned as unknown as Record<string, unknown>,
                {
                    agentId: params.agentId,
                    chatType: params.chatType,
                    peerId: params.peerId,
                    accountId: params.accountId,
                    workspace,
                    agentDir,
                    maxAgents: dynCfg.maxAgents,
                },
            );

            if (result.rejectedOverLimit) {
                console.warn(
                    `[wecom] dynamic agent maxAgents=${dynCfg.maxAgents} reached; rejecting derive for ${params.agentId}; will fallback to main`,
                );
                ensuredDynamicAgentIds.add(normalizedId); // 缓存避免每条消息都尝试
                return;
            }

            if (result.changed) {
                // mkdir 失败不阻塞（大概率目录已存在；OpenClaw 核心也会按需创建）
                try {
                    const fs = await import("node:fs/promises");
                    await fs.mkdir(workspace, { recursive: true });
                    await fs.mkdir(agentDir, { recursive: true });
                } catch (err) {
                    console.warn(`[wecom] dynamic agent mkdir warn: ${(err as Error)?.message}`);
                }

                // v2.9.2 ⭐ 从 main workspace 种子复制身份文件，跳过 OpenClaw 核心 BOOTSTRAP 引导
                if (dynCfg.seedFromMainWorkspace) {
                    try {
                        const seedResult = await seedWorkspaceFromMain({
                            targetWorkspace: workspace,
                            mainWorkspace: dynCfg.mainWorkspacePath,
                            seedFiles: dynCfg.seedFiles,
                        });
                        if (seedResult.copied.length > 0) {
                            console.log(
                                `[wecom] seeded ${params.agentId} workspace from main: copied=${seedResult.copied.join(",")}${seedResult.skipped.length ? ` skipped=${seedResult.skipped.join(",")}` : ""}`,
                            );
                        }
                    } catch (err) {
                        console.warn(`[wecom] seed workspace warn: ${(err as Error)?.message}`);
                    }
                }

                await configRuntime.writeConfigFile!(cloned as unknown);
                console.log(
                    `[wecom] dynamic agent registered: ${params.agentId} workspace=${workspace} agentDir=${agentDir}`,
                );
            }

            ensuredDynamicAgentIds.add(normalizedId);
        })
        .catch((err) => {
            console.warn(`[wecom] 动态 Agent 注册失败: ${normalizedId}`, err);
        });

    await ensureDynamicAgentWriteQueue;
}

/**
 * **resetEnsuredCache (重置已确保缓存)**
 *
 * 主要用于测试场景，重置内存中的缓存状态。
 */
export function resetEnsuredCache(): void {
    ensuredDynamicAgentIds.clear();
}
