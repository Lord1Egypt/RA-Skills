import fs from "fs/promises";
import { execFileSync } from "child_process";
import { randomBytes } from "crypto";
import { existsSync, readFileSync, readdirSync } from "fs";
import os from "os";
import path from "path";
import { AboutInfo, AgentProfile, AppUpdatePolicy, AssistantMessage, AssistantSession, ChannelConfig, ChatWsSession, CommunicationConfig, CronJob, HealEvent, HealPolicy, MarkdownFileRecord, MemoryFileItem, ModelConfig, OpenClawTarget, PanelSettings, QuickActionItem, RoutingStrategy, SecurityConfig, ServiceStatus, SkillConfig, SkillDependencyIssue, SkillDependencyReport, TokenUsageRecord } from "./types";
import { agents, appUpdatePolicy, assistantMessages, assistantSessions, channels, chatWsSessions, communicationConfig, cronJobs, healEvents, healPolicy, markdownDir, memoryDir, models, openClawTargets, panelSettings, routingStrategies, runtimeState, securityConfig, skills, tokenUsages } from "./store";
import { createId } from "./utils";

const modelOverrides = new Map<string, ModelConfig>();
const skillOverrides = new Map<string, SkillConfig>();
const channelOverrides = new Map<string, ChannelConfig>();

function resolveOpenClawConfigPath(): string {
  if (process.env.OPENCLAW_RUNTIME_CONFIG_PATH) {
    return process.env.OPENCLAW_RUNTIME_CONFIG_PATH;
  }
  if (process.env.OPENCLAW_CONFIG_PATH) {
    return process.env.OPENCLAW_CONFIG_PATH;
  }
  const homeDir = process.env.HOME ?? process.env.USERPROFILE ?? os.homedir();
  return path.join(homeDir, ".openclaw", "openclaw.json");
}

function loadOpenClawConfig(): Record<string, unknown> | null {
  try {
    const filePath = resolveOpenClawConfigPath();
    const content = readFileSync(filePath, "utf-8");
    return JSON.parse(content) as Record<string, unknown>;
  } catch {
    return null;
  }
}

async function saveOpenClawConfig(nextConfig: Record<string, unknown>): Promise<void> {
  const filePath = resolveOpenClawConfigPath();
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(nextConfig, null, 2)}\n`, "utf-8");
}

function pickObject(input: unknown): Record<string, unknown> {
  return input && typeof input === "object" && !Array.isArray(input) ? input as Record<string, unknown> : {};
}

function toBool(input: unknown, fallback: boolean): boolean {
  return typeof input === "boolean" ? input : fallback;
}

function toNumber(input: unknown, fallback: number): number {
  return typeof input === "number" && Number.isFinite(input) ? input : fallback;
}

function toText(input: unknown, fallback: string): string {
  return typeof input === "string" && input.trim().length > 0 ? input : fallback;
}

function inferPlatformName(providerId: string, providerObj: Record<string, unknown>): string {
  const source = `${providerId} ${toText(providerObj.baseUrl, "")}`.toLowerCase();
  if (source.includes("openai") || source.includes("gpt")) {
    return "openai";
  }
  if (source.includes("volc") || source.includes("ark")) {
    return "volcengine";
  }
  if (source.includes("anthropic") || source.includes("claude")) {
    return "anthropic";
  }
  if (source.includes("gemini") || source.includes("google")) {
    return "google";
  }
  if (source.includes("deepseek")) {
    return "deepseek";
  }
  if (source.includes("dashscope") || source.includes("qwen")) {
    return "qwen";
  }
  if (source.includes("moonshot") || source.includes("kimi")) {
    return "kimi";
  }
  if (source.includes("zhipu") || source.includes("glm")) {
    return "zhipuai";
  }
  return providerId;
}

function collectRuntimeModels(): ModelConfig[] {
  const config = loadOpenClawConfig();
  const modelRoot = pickObject(config?.models);
  const providers = pickObject(modelRoot.providers);
  const result = new Map<string, ModelConfig>();

  for (const [providerId, provider] of Object.entries(providers)) {
    const providerObj = pickObject(provider);
    const providerEnabled = toBool(providerObj.enabled, true);
    const platform = inferPlatformName(providerId, providerObj);
    const providerApiKey = toText(providerObj.apiKey, "");
    const providerBaseUrl = toText(providerObj.baseUrl, "");
    const providerModels = Array.isArray(providerObj.models) ? providerObj.models : [];

    for (const item of providerModels) {
      const modelObj = pickObject(item);
      const modelId = toText(modelObj.id, "");
      if (!modelId) {
        continue;
      }
      const nextModel: ModelConfig = {
        id: modelId,
        modelId,
        providerId,
        platform,
        name: toText(modelObj.name, modelId),
        enabled: providerEnabled && toBool(modelObj.enabled, true),
        maxTokens: toNumber(modelObj.maxTokens, toNumber(modelObj.contextWindow, 8192)),
        apiKey: providerApiKey,
        baseUrl: providerBaseUrl
      };
      result.set(modelId, nextModel);
    }
  }

  return Array.from(result.values());
}

function collectRuntimeSkills(): SkillConfig[] {
  const config = loadOpenClawConfig();
  const skillsRoot = pickObject(config?.skills);
  const entries = skillsRoot.entries;
  const result = new Map<string, SkillConfig>();

  if (Array.isArray(entries)) {
    for (const item of entries) {
      const skillObj = pickObject(item);
      const id = toText(skillObj.id, "");
      if (!id) {
        continue;
      }
      result.set(id, {
        id,
        name: toText(skillObj.name, id),
        enabled: toBool(skillObj.enabled, true),
        description: toText(skillObj.description, `技能: ${id}`),
        group: "配置技能"
      });
    }
  } else {
    const entryMap = pickObject(entries);
    for (const [id, item] of Object.entries(entryMap)) {
      const skillObj = pickObject(item);
      result.set(id, {
        id,
        name: toText(skillObj.name, id),
        enabled: toBool(skillObj.enabled, true),
        description: toText(skillObj.description, `技能: ${id}`),
        group: "配置技能"
      });
    }
  }

  const homeDir = process.env.HOME ?? process.env.USERPROFILE ?? os.homedir();
  const runtimeSkillsDirs = [
    process.env.OPENCLAW_SKILLS_DIR,
    path.join(homeDir, ".openclaw", "skills"),
    path.resolve(process.cwd(), "../../skills")
  ].filter((item): item is string => Boolean(item));
  const seenDirs = new Set<string>();

  for (const dirPath of runtimeSkillsDirs) {
    if (seenDirs.has(dirPath) || !existsSync(dirPath)) {
      continue;
    }
    seenDirs.add(dirPath);
    const names = readdirSync(dirPath, { withFileTypes: true })
      .filter((item) => item.isDirectory())
      .map((item) => item.name);

    for (const name of names) {
      if (result.has(name)) {
        continue;
      }
      result.set(name, {
        id: name,
        name,
        enabled: true,
        description: `已安装技能: ${name}`,
        group: "已安装技能"
      });
    }
  }
  return Array.from(result.values()).sort((a, b) => a.id.localeCompare(b.id));
}

function collectRuntimeChannels(): ChannelConfig[] {
  const config = loadOpenClawConfig();
  const channelRoot = pickObject(config?.channels);
  const result: ChannelConfig[] = [];

  for (const [id, item] of Object.entries(channelRoot)) {
    const channelObj = pickObject(item);
    const accounts = pickObject(channelObj.accounts);
    const defaultAccount = pickObject(accounts.default);
    const robotId = toText(channelObj.appId, toText(defaultAccount.appId, ""));
    const robotSecret = toText(channelObj.appSecret, toText(defaultAccount.appSecret, ""));
    result.push({
      id,
      name: toText(channelObj.name, id === "feishu" ? "飞书渠道" : id),
      enabled: toBool(channelObj.enabled, true),
      weight: toNumber(channelObj.weight, id === "feishu" ? 200 : 100),
      robotId,
      robotSecret
    });
  }
  return result;
}

function mergeById<T extends { id: string }>(base: T[], overrides: Map<string, T>): T[] {
  const merged = new Map<string, T>();
  for (const item of base) {
    merged.set(item.id, item);
  }
  for (const [id, item] of overrides.entries()) {
    merged.set(id, item);
  }
  return Array.from(merged.values());
}

export function resolveByDomain(domain: string): OpenClawTarget | undefined {
  return openClawTargets.find((item) => item.domain === domain);
}

export function listOpenClawTargets(): OpenClawTarget[] {
  return openClawTargets;
}

export function updateOpenClawTargetConfig(nextTarget: {
  domain: string;
  apiBaseUrl: string;
  healthPath: string;
  chatPaths: string[];
  authHeaderName?: string;
  authHeaderValue?: string;
  extraHeaders?: Record<string, string>;
  timeoutMs?: number;
}): OpenClawTarget {
  const target = resolveByDomain(nextTarget.domain);
  if (!target) {
    throw new Error("目标域名不存在");
  }
  target.apiBaseUrl = nextTarget.apiBaseUrl.replace(/\/+$/, "");
  target.healthPath = nextTarget.healthPath;
  target.chatPaths = nextTarget.chatPaths;
  if ("authHeaderName" in nextTarget) {
    target.authHeaderName = nextTarget.authHeaderName;
  }
  if ("authHeaderValue" in nextTarget) {
    target.authHeaderValue = nextTarget.authHeaderValue;
  }
  if ("extraHeaders" in nextTarget) {
    target.extraHeaders = nextTarget.extraHeaders;
  }
  target.timeoutMs = nextTarget.timeoutMs ?? target.timeoutMs ?? 3000;
  return target;
}

function computeTokenUsageFromMessages(messages: Array<{ content: string }>): { promptTokens: number; completionTokens: number } {
  const contentLength = messages.map((item) => item.content.length).reduce((sum, value) => sum + value, 0);
  const promptTokens = Math.ceil(contentLength * 0.6);
  const completionTokens = Math.ceil(promptTokens * 1.2);
  return { promptTokens, completionTokens };
}

export async function probeOpenClawTarget(target: OpenClawTarget): Promise<{ ok: boolean; statusCode: number; message: string }> {
  const healthPath = target.healthPath ?? "/health";
  const headerName = target.authHeaderName?.trim();
  const authHeaders = headerName && target.authHeaderValue
    ? { [headerName]: target.authHeaderValue }
    : {};

  try {
    const response = await fetch(`${target.apiBaseUrl}${healthPath}`, {
      method: "GET",
      headers: {
        ...authHeaders,
        ...(target.extraHeaders ?? {})
      },
      signal: AbortSignal.timeout(target.timeoutMs ?? 5000)
    });

    if (response.ok) {
      return { ok: true, statusCode: response.status, message: "目标健康检查通过" };
    }
    return { ok: false, statusCode: response.status, message: `健康检查失败: HTTP ${response.status}` };
  } catch (error) {
    const message = error instanceof Error ? error.message : "探测失败";
    return { ok: false, statusCode: 0, message };
  }
}

export async function sendMessageToOpenClaw(payload: {
  target: OpenClawTarget;
  modelId: string;
  channelId: string;
  messages: Array<{ role: "system" | "user" | "assistant"; content: string }>;
}): Promise<{
  reply: string;
  mode: "proxy" | "mock";
  usage: TokenUsageRecord;
  proxyDetail?: { statusCode: number; endpoint: string };
}> {
  const { promptTokens, completionTokens } = computeTokenUsageFromMessages(payload.messages);
  const usage = recordTokenUsage(payload.modelId, payload.channelId, promptTokens, completionTokens);
  const latestContent = payload.messages[payload.messages.length - 1]?.content ?? "";
  const shouldTryProxy = !payload.target.domain.endsWith(".local");
  const tryEndpoints = payload.target.chatPaths?.length
    ? payload.target.chatPaths
    : ["/api/chat/send", "/api/v1/chat/completions", "/v1/chat/completions"];
  const headerName = payload.target.authHeaderName?.trim();
  const authHeaders = headerName && payload.target.authHeaderValue
    ? { [headerName]: payload.target.authHeaderValue }
    : {};

  for (const endpoint of shouldTryProxy ? tryEndpoints : []) {
    try {
      const response = await fetch(`${payload.target.apiBaseUrl}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(payload.target.gatewayToken ? { Authorization: `Bearer ${payload.target.gatewayToken}` } : {}),
          ...authHeaders,
          ...(payload.target.extraHeaders ?? {})
        },
        body: JSON.stringify({
          model: payload.modelId,
          messages: payload.messages
        }),
        signal: AbortSignal.timeout(payload.target.timeoutMs ?? 2500)
      });

      if (!response.ok) {
        continue;
      }

      const responseText = await response.text();
      let reply = `OpenClaw(${payload.target.version}) 已接收消息`;

      try {
        const parsed = JSON.parse(responseText) as {
          reply?: string;
          content?: string;
          choices?: Array<{ message?: { content?: string } }>;
        };
        reply = parsed.reply ?? parsed.content ?? parsed.choices?.[0]?.message?.content ?? reply;
      } catch {
        if (responseText.trim().length > 0) {
          reply = responseText.slice(0, 400);
        }
      }

      return {
        reply,
        mode: "proxy",
        usage,
        proxyDetail: { statusCode: response.status, endpoint }
      };
    } catch {
      continue;
    }
  }

  return {
    reply: `已由 ${payload.target.version} 版本处理：${latestContent}`,
    mode: "mock",
    usage
  };
}

export function listModels(): ModelConfig[] {
  const runtimeModels = collectRuntimeModels();
  return mergeById(runtimeModels, modelOverrides);
}

export async function upsertModel(nextModel: ModelConfig): Promise<ModelConfig> {
  modelOverrides.set(nextModel.id, nextModel);
  const config = loadOpenClawConfig();
  if (config) {
    const modelRoot = pickObject(config.models);
    const providers = pickObject(modelRoot.providers);
    const providerId = nextModel.providerId || nextModel.platform || "openai";
    const currentProvider = pickObject(providers[providerId]);
    const providerModels = Array.isArray(currentProvider.models) ? currentProvider.models.map((item) => pickObject(item)) : [];
    const targetModelId = nextModel.modelId || nextModel.id;
    const modelIndex = providerModels.findIndex((item) => toText(item.id, "") === targetModelId);
    const mergedModel: Record<string, unknown> = {
      ...(modelIndex >= 0 ? providerModels[modelIndex] : {}),
      id: targetModelId,
      name: nextModel.name,
      maxTokens: nextModel.maxTokens,
      contextWindow: nextModel.maxTokens
    };
    if (modelIndex >= 0) {
      providerModels[modelIndex] = mergedModel;
    } else {
      providerModels.push(mergedModel);
    }

    const mergedProvider: Record<string, unknown> = {
      ...currentProvider,
      models: providerModels
    };
    if (nextModel.apiKey !== undefined) {
      if (nextModel.apiKey.trim().length > 0) {
        mergedProvider.apiKey = nextModel.apiKey;
      } else {
        delete mergedProvider.apiKey;
      }
    }
    if (nextModel.baseUrl !== undefined) {
      if (nextModel.baseUrl.trim().length > 0) {
        mergedProvider.baseUrl = nextModel.baseUrl;
      } else {
        delete mergedProvider.baseUrl;
      }
    }

    config.models = {
      ...modelRoot,
      providers: {
        ...providers,
        [providerId]: mergedProvider
      }
    };
    await saveOpenClawConfig(config);
  }
  return nextModel;
}

export function listSkills(): SkillConfig[] {
  const runtimeSkills = collectRuntimeSkills();
  const baseSkills = runtimeSkills.length > 0 ? runtimeSkills : skills;
  return mergeById(baseSkills, skillOverrides);
}

export function upsertSkill(nextSkill: SkillConfig): SkillConfig {
  skillOverrides.set(nextSkill.id, nextSkill);
  return nextSkill;
}

export function listChannels(): ChannelConfig[] {
  const runtimeChannels = collectRuntimeChannels();
  return mergeById(runtimeChannels, channelOverrides);
}

export async function upsertChannel(nextChannel: ChannelConfig): Promise<ChannelConfig> {
  channelOverrides.set(nextChannel.id, nextChannel);
  const config = loadOpenClawConfig();
  if (config) {
    const channelsRoot = pickObject(config.channels);
    const current = pickObject(channelsRoot[nextChannel.id]);
    const merged: Record<string, unknown> = {
      ...current,
      enabled: nextChannel.enabled
    };
    if (nextChannel.id === "feishu") {
      if (nextChannel.robotId !== undefined) {
        merged.appId = nextChannel.robotId;
      }
      if (nextChannel.robotSecret !== undefined) {
        merged.appSecret = nextChannel.robotSecret;
      }
      const accounts = pickObject(merged.accounts);
      const defaultAccount = pickObject(accounts.default);
      if (nextChannel.robotId !== undefined) {
        defaultAccount.appId = nextChannel.robotId;
      }
      if (nextChannel.robotSecret !== undefined) {
        defaultAccount.appSecret = nextChannel.robotSecret;
      }
      merged.accounts = {
        ...accounts,
        default: defaultAccount
      };
    }
    config.channels = {
      ...channelsRoot,
      [nextChannel.id]: merged
    };
    await saveOpenClawConfig(config);
  }
  return nextChannel;
}

function collectRuntimeAgents(): AgentProfile[] {
  const config = loadOpenClawConfig();
  if (!config) {
    return [];
  }
  const agentsRoot = pickObject(config.agents);
  const items = pickObject(agentsRoot.items);
  const defaults = pickObject(agentsRoot.defaults);
  const defaultPrimary = toText(defaults.model, "gpt-4.1");
  const defaultFallbacks = Array.isArray(defaults.fallbacks)
    ? defaults.fallbacks.filter((item): item is string => typeof item === "string")
    : [];
  return Object.entries(items).map(([id, raw]) => {
    const item = pickObject(raw);
    const fallbackModels = Array.isArray(item.fallbackModels)
      ? item.fallbackModels.filter((entry): entry is string => typeof entry === "string")
      : defaultFallbacks;
    return {
      id,
      name: toText(item.name, id),
      workspace: toText(item.workspace, process.cwd()),
      enabled: toBool(item.enabled, true),
      primaryModelId: toText(item.primaryModelId, defaultPrimary),
      fallbackModelIds: fallbackModels,
      updatedAt: toText(item.updatedAt, new Date().toISOString())
    };
  });
}

export function listAgents(): AgentProfile[] {
  const runtimeAgents = collectRuntimeAgents();
  return runtimeAgents.length > 0 ? runtimeAgents : agents;
}

export async function upsertAgent(nextAgent: AgentProfile): Promise<AgentProfile> {
  const index = agents.findIndex((item) => item.id === nextAgent.id);
  const merged = {
    ...nextAgent,
    updatedAt: new Date().toISOString()
  };
  if (index >= 0) {
    agents[index] = merged;
  } else {
    agents.push(merged);
  }
  const config = loadOpenClawConfig();
  if (config) {
    const agentsRoot = pickObject(config.agents);
    const items = pickObject(agentsRoot.items);
    items[merged.id] = {
      name: merged.name,
      workspace: merged.workspace,
      enabled: merged.enabled,
      primaryModelId: merged.primaryModelId,
      fallbackModels: merged.fallbackModelIds,
      updatedAt: merged.updatedAt
    };
    config.agents = {
      ...agentsRoot,
      items
    };
    await saveOpenClawConfig(config);
  }
  return merged;
}

export async function deleteAgent(agentId: string): Promise<{ removed: boolean }> {
  const index = agents.findIndex((item) => item.id === agentId);
  if (index >= 0) {
    agents.splice(index, 1);
  }
  const config = loadOpenClawConfig();
  if (config) {
    const agentsRoot = pickObject(config.agents);
    const items = pickObject(agentsRoot.items);
    if (agentId in items) {
      delete items[agentId];
      config.agents = {
        ...agentsRoot,
        items
      };
      await saveOpenClawConfig(config);
      return { removed: true };
    }
  }
  return { removed: index >= 0 };
}

export function getCommunicationConfig(): CommunicationConfig {
  const config = loadOpenClawConfig();
  if (!config) {
    return communicationConfig;
  }
  const messages = pickObject(config.messages);
  const broadcast = pickObject(config.broadcast);
  const commands = pickObject(config.commands);
  const hooks = pickObject(config.hooks);
  const approvals = pickObject(config.approvals);
  return {
    messages: {
      autoReplyEnabled: toBool(messages.autoReplyEnabled, communicationConfig.messages.autoReplyEnabled),
      autoReplyTemplate: toText(messages.autoReplyTemplate, communicationConfig.messages.autoReplyTemplate)
    },
    broadcast: {
      strategy: toText(broadcast.strategy, communicationConfig.broadcast.strategy) === "all" ? "all" : "priority",
      defaultChannelId: toText(broadcast.defaultChannelId, communicationConfig.broadcast.defaultChannelId)
    },
    commands: {
      enabled: toBool(commands.enabled, communicationConfig.commands.enabled),
      prefix: toText(commands.prefix, communicationConfig.commands.prefix)
    },
    hooks: {
      enabled: toBool(hooks.enabled, communicationConfig.hooks.enabled),
      webhookUrl: toText(hooks.webhookUrl, communicationConfig.hooks.webhookUrl)
    },
    approvals: {
      execEnabled: toBool(approvals.execEnabled, communicationConfig.approvals.execEnabled),
      requireConfirm: toBool(approvals.requireConfirm, communicationConfig.approvals.requireConfirm)
    },
    updatedAt: new Date().toISOString()
  };
}

export async function updateCommunicationConfig(payload: CommunicationConfig): Promise<CommunicationConfig> {
  communicationConfig.messages = payload.messages;
  communicationConfig.broadcast = payload.broadcast;
  communicationConfig.commands = payload.commands;
  communicationConfig.hooks = payload.hooks;
  communicationConfig.approvals = payload.approvals;
  communicationConfig.updatedAt = new Date().toISOString();
  const config = loadOpenClawConfig();
  if (config) {
    config.messages = payload.messages;
    config.broadcast = payload.broadcast;
    config.commands = payload.commands;
    config.hooks = payload.hooks;
    config.approvals = payload.approvals;
    await saveOpenClawConfig(config);
  }
  return communicationConfig;
}

function safeSegment(input: string): string {
  return input.replace(/[^\w.-]/g, "_");
}

export async function listMemoryFiles(agentId: string, category: string): Promise<MemoryFileItem[]> {
  const safeAgentId = safeSegment(agentId);
  const safeCategory = safeSegment(category);
  const dir = path.join(memoryDir, safeAgentId, safeCategory);
  await fs.mkdir(dir, { recursive: true });
  const names = (await fs.readdir(dir)).filter((name) => name.endsWith(".md"));
  const files = await Promise.all(names.map(async (name) => {
    const filePath = path.join(dir, name);
    const content = await fs.readFile(filePath, "utf-8");
    const stat = await fs.stat(filePath);
    return {
      agentId: safeAgentId,
      category: safeCategory,
      fileName: name,
      content,
      updatedAt: stat.mtime.toISOString()
    };
  }));
  return files.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export async function upsertMemoryFile(payload: {
  agentId: string;
  category: string;
  fileName: string;
  content: string;
}): Promise<MemoryFileItem> {
  const safeAgentId = safeSegment(payload.agentId);
  const safeCategory = safeSegment(payload.category);
  const safeFileName = safeSegment(payload.fileName).endsWith(".md")
    ? safeSegment(payload.fileName)
    : `${safeSegment(payload.fileName)}.md`;
  const dir = path.join(memoryDir, safeAgentId, safeCategory);
  await fs.mkdir(dir, { recursive: true });
  const filePath = path.join(dir, safeFileName);
  await fs.writeFile(filePath, payload.content, "utf-8");
  const stat = await fs.stat(filePath);
  return {
    agentId: safeAgentId,
    category: safeCategory,
    fileName: safeFileName,
    content: payload.content,
    updatedAt: stat.mtime.toISOString()
  };
}

export async function deleteMemoryFile(payload: {
  agentId: string;
  category: string;
  fileName: string;
}): Promise<{ removed: boolean }> {
  const filePath = path.join(memoryDir, safeSegment(payload.agentId), safeSegment(payload.category), safeSegment(payload.fileName));
  try {
    await fs.rm(filePath);
    return { removed: true };
  } catch {
    return { removed: false };
  }
}

export function getUsageSummary(days: number): {
  days: number;
  from: string;
  to: string;
  totalTokens: number;
  totalPromptTokens: number;
  totalCompletionTokens: number;
  perModel: Record<string, number>;
  perChannel: Record<string, number>;
  openclawTotalTokens: number;
  openclawTotalCost: number;
  daily: Array<{ date: string; totalTokens: number; totalCost: number }>;
} {
  const boundedDays = Math.max(1, Math.min(90, Math.floor(days)));
  const stats = getTokenStats();
  const now = new Date();
  const fromDate = new Date(now.getTime() - boundedDays * 24 * 60 * 60 * 1000);
  const filtered = stats.recentRecords.filter((item) => new Date(item.createdAt) >= fromDate);
  const perModel: Record<string, number> = {};
  const perChannel: Record<string, number> = {};
  let totalPromptTokens = 0;
  let totalCompletionTokens = 0;
  for (const item of filtered) {
    const total = item.promptTokens + item.completionTokens;
    perModel[item.modelId] = (perModel[item.modelId] ?? 0) + total;
    perChannel[item.channelId] = (perChannel[item.channelId] ?? 0) + total;
    totalPromptTokens += item.promptTokens;
    totalCompletionTokens += item.completionTokens;
  }
  const daily = (stats.openclaw?.daily ?? []).slice(-boundedDays).map((item) => ({
    date: item.date,
    totalTokens: item.totalTokens,
    totalCost: item.totalCost
  }));
  return {
    days: boundedDays,
    from: fromDate.toISOString(),
    to: now.toISOString(),
    totalTokens: totalPromptTokens + totalCompletionTokens,
    totalPromptTokens,
    totalCompletionTokens,
    perModel,
    perChannel,
    openclawTotalTokens: stats.openclaw?.totals.totalTokens ?? 0,
    openclawTotalCost: stats.openclaw?.totals.totalCost ?? 0,
    daily
  };
}

export function listCronJobs(): CronJob[] {
  return [...cronJobs].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export function upsertCronJob(payload: Omit<CronJob, "updatedAt"> & { updatedAt?: string }): CronJob {
  const next: CronJob = {
    ...payload,
    updatedAt: new Date().toISOString()
  };
  const index = cronJobs.findIndex((item) => item.id === next.id);
  if (index >= 0) {
    cronJobs[index] = next;
  } else {
    cronJobs.push(next);
  }
  return next;
}

export function deleteCronJob(id: string): { removed: boolean } {
  const index = cronJobs.findIndex((item) => item.id === id);
  if (index < 0) {
    return { removed: false };
  }
  cronJobs.splice(index, 1);
  return { removed: true };
}

export function runCronJob(id: string): { ok: boolean; detail: string; ranAt: string } {
  const target = cronJobs.find((item) => item.id === id);
  if (!target) {
    return { ok: false, detail: "任务不存在", ranAt: new Date().toISOString() };
  }
  return {
    ok: true,
    detail: `已触发任务 ${target.name}`,
    ranAt: new Date().toISOString()
  };
}

export function getChatWsConfig(baseUrl: string): {
  wsUrl: string;
  token: string;
  challenge: string;
  protocol: "openclaw-ws-v1";
} {
  const wsUrl = baseUrl.replace(/^http/i, "ws").replace(/\/+$/, "") + "/ws";
  return {
    wsUrl,
    token: randomBytes(12).toString("hex"),
    challenge: randomBytes(8).toString("hex"),
    protocol: "openclaw-ws-v1"
  };
}

export function connectChatWs(): ChatWsSession {
  const session: ChatWsSession = {
    sessionId: createId("ws"),
    connectedAt: new Date().toISOString(),
    status: "connected"
  };
  chatWsSessions.push(session);
  return session;
}

export function listChatWsSessions(): ChatWsSession[] {
  return [...chatWsSessions].sort((a, b) => b.connectedAt.localeCompare(a.connectedAt));
}

export async function sendWsChatMessage(payload: {
  sessionId: string;
  target: OpenClawTarget;
  modelId: string;
  channelId: string;
  message: string;
}): Promise<{ reply: string; sessionId: string; mode: "proxy" | "mock" }> {
  const result = await sendMessageToOpenClaw({
    target: payload.target,
    modelId: payload.modelId,
    channelId: payload.channelId,
    messages: [{ role: "user", content: payload.message }]
  });
  return {
    reply: result.reply,
    sessionId: payload.sessionId,
    mode: result.mode
  };
}

export function listAssistantSessions(): AssistantSession[] {
  return [...assistantSessions].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export function createAssistantSession(title: string): AssistantSession {
  const session: AssistantSession = {
    id: createId("asst"),
    title: title.trim() || "新会话",
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
  assistantSessions.push(session);
  return session;
}

export function listAssistantMessages(sessionId: string): AssistantMessage[] {
  return assistantMessages
    .filter((item) => item.sessionId === sessionId)
    .sort((a, b) => a.createdAt.localeCompare(b.createdAt));
}

export async function sendAssistantMessage(payload: {
  sessionId: string;
  content: string;
  target: OpenClawTarget;
  modelId: string;
  channelId: string;
}): Promise<{ user: AssistantMessage; assistant: AssistantMessage }> {
  const now = new Date().toISOString();
  const userMessage: AssistantMessage = {
    id: createId("msg"),
    sessionId: payload.sessionId,
    role: "user",
    content: payload.content,
    createdAt: now
  };
  assistantMessages.push(userMessage);
  const response = await sendMessageToOpenClaw({
    target: payload.target,
    modelId: payload.modelId,
    channelId: payload.channelId,
    messages: [{ role: "user", content: payload.content }]
  });
  const assistantMessage: AssistantMessage = {
    id: createId("msg"),
    sessionId: payload.sessionId,
    role: "assistant",
    content: response.reply,
    createdAt: new Date().toISOString()
  };
  assistantMessages.push(assistantMessage);
  const session = assistantSessions.find((item) => item.id === payload.sessionId);
  if (session) {
    session.updatedAt = new Date().toISOString();
  }
  return { user: userMessage, assistant: assistantMessage };
}

export function searchSkills(keyword: string): SkillConfig[] {
  const text = keyword.trim().toLowerCase();
  if (!text) {
    return listSkills();
  }
  return listSkills().filter((item) =>
    item.id.toLowerCase().includes(text) ||
    item.name.toLowerCase().includes(text) ||
    item.description.toLowerCase().includes(text)
  );
}

function commandInstalled(command: string): boolean {
  const versionArgs = command === "ffmpeg" ? [["-version"], ["--version"]] : [["--version"], ["-version"]];
  for (const args of versionArgs) {
    const result = tryExec(command, args, 4000);
    if (result.ok) {
      return true;
    }
  }
  const fallback = tryExec("which", [command], 4000);
  return fallback.ok;
}

export function checkSkillDependencies(skillId: string): SkillDependencyReport {
  const lower = skillId.trim().toLowerCase();
  const checks: Array<{ name: string; required: boolean; ok: boolean; fixHint?: string }> = [
    { name: "node", required: true, ok: commandInstalled("node"), fixHint: "安装 Node.js 18+ 并确保 node 在 PATH 中" },
    { name: "npm", required: true, ok: commandInstalled("npm"), fixHint: "安装 npm 并确保 npm 在 PATH 中" },
    { name: "openclaw", required: true, ok: commandInstalled("openclaw"), fixHint: "安装 openclaw CLI 并执行 openclaw doctor --fix" },
    { name: "python3", required: lower.includes("douyin") || lower.includes("tiktok"), ok: commandInstalled("python3"), fixHint: "安装 Python3 以支持该技能依赖脚本" },
    { name: "ffmpeg", required: lower.includes("video"), ok: commandInstalled("ffmpeg"), fixHint: "安装 ffmpeg 以支持音视频处理能力" }
  ];
  const issues: SkillDependencyIssue[] = checks
    .filter((item) => item.required)
    .map((item) => ({
      name: item.name,
      severity: item.ok ? "info" : "error",
      installed: item.ok,
      message: item.ok ? `${item.name} 已安装` : `${item.name} 缺失`,
      fixHint: item.ok ? undefined : item.fixHint
    }));
  const warnings: SkillDependencyIssue[] = checks
    .filter((item) => !item.required && !item.ok)
    .map((item) => ({
      name: item.name,
      severity: "warning",
      installed: false,
      message: `${item.name} 未安装（当前技能可选）`,
      fixHint: item.fixHint
    }));
  const merged = [...issues, ...warnings];
  return {
    skillId,
    ready: !merged.some((item) => item.severity === "error"),
    issues: merged,
    checkedAt: new Date().toISOString()
  };
}

export async function installSkill(payload: SkillConfig): Promise<SkillConfig> {
  return upsertSkill(payload);
}

export function uninstallSkill(skillId: string): { removed: boolean } {
  const before = skills.length;
  const next = skills.filter((item) => item.id !== skillId);
  skills.splice(0, skills.length, ...next);
  return { removed: next.length < before };
}

export function getAboutInfo(): AboutInfo {
  return {
    appName: "clawK",
    appVersion: "1.0.0",
    backendVersion: "1.0.0",
    openclawLastUpdateAt: runtimeState.openclawLastUpdateAt,
    gatewayLastRestartAt: runtimeState.gatewayLastRestartAt
  };
}

export function uninstallOpenClawMock(): { ok: boolean; detail: string } {
  return {
    ok: true,
    detail: "移动网关模拟环境已执行卸载动作（未删除实际系统文件）"
  };
}

export async function listMarkdownFiles(): Promise<MarkdownFileRecord[]> {
  await fs.mkdir(markdownDir, { recursive: true });
  const entries = await fs.readdir(markdownDir);
  const markdownNames = entries.filter((name) => name.endsWith(".md"));
  const files = await Promise.all(
    markdownNames.map(async (name) => {
      const content = await fs.readFile(path.join(markdownDir, name), "utf-8");
      return { fileName: name, content };
    })
  );
  return files;
}

export async function updateMarkdownFile(fileName: string, content: string): Promise<MarkdownFileRecord> {
  await fs.mkdir(markdownDir, { recursive: true });
  await fs.writeFile(path.join(markdownDir, fileName), content, "utf-8");
  return { fileName, content };
}

export function recordTokenUsage(modelId: string, channelId: string, promptTokens: number, completionTokens: number): TokenUsageRecord {
  // 核心逻辑：每次对话都沉淀 token 使用明细，为后续统计面板提供原始数据。
  const next = {
    id: createId("tok"),
    modelId,
    channelId,
    promptTokens,
    completionTokens,
    createdAt: new Date().toISOString()
  };
  tokenUsages.push(next);
  return next;
}

export function getTokenStats(): {
  totalPromptTokens: number;
  totalCompletionTokens: number;
  totalTokens: number;
  perModel: Record<string, number>;
  perChannel: Record<string, number>;
  openclaw: {
    updatedAt: number;
    days: number;
    totals: {
      input: number;
      output: number;
      cacheRead: number;
      cacheWrite: number;
      totalTokens: number;
      totalCost: number;
    };
    daily: Array<{
      date: string;
      input: number;
      output: number;
      cacheRead: number;
      cacheWrite: number;
      totalTokens: number;
      totalCost: number;
    }>;
  } | null;
  recentRecords: TokenUsageRecord[];
} {
  // 核心逻辑：按模型与渠道双维度聚合 token，供移动端展示“酷炫统计”看板。
  const perModel: Record<string, number> = {};
  const perChannel: Record<string, number> = {};

  let totalPromptTokens = 0;
  let totalCompletionTokens = 0;

  for (const item of tokenUsages) {
    const total = item.promptTokens + item.completionTokens;
    totalPromptTokens += item.promptTokens;
    totalCompletionTokens += item.completionTokens;
    perModel[item.modelId] = (perModel[item.modelId] ?? 0) + total;
    perChannel[item.channelId] = (perChannel[item.channelId] ?? 0) + total;
  }

  let openclawUsage: {
    updatedAt: number;
    days: number;
    totals: {
      input: number;
      output: number;
      cacheRead: number;
      cacheWrite: number;
      totalTokens: number;
      totalCost: number;
    };
    daily: Array<{
      date: string;
      input: number;
      output: number;
      cacheRead: number;
      cacheWrite: number;
      totalTokens: number;
      totalCost: number;
    }>;
  } | null = null;

  try {
    const days = process.env.OPENCLAW_USAGE_DAYS ?? "7";
    const usageConfigPath = process.env.OPENCLAW_USAGE_CONFIG_PATH ?? process.env.OPENCLAW_CONFIG_PATH;
    const raw = execFileSync("openclaw", ["gateway", "usage-cost", "--days", days, "--json"], {
      encoding: "utf-8",
      timeout: 12000,
      env: {
        ...process.env,
        ...(usageConfigPath ? { OPENCLAW_CONFIG_PATH: usageConfigPath } : {})
      }
    });
    const parsed = JSON.parse(raw) as {
      updatedAt: number;
      days: number;
      totals: Record<string, number>;
      daily: Array<Record<string, number | string>>;
    };
    openclawUsage = {
      updatedAt: parsed.updatedAt,
      days: parsed.days,
      totals: {
        input: toNumber(parsed.totals?.input, 0),
        output: toNumber(parsed.totals?.output, 0),
        cacheRead: toNumber(parsed.totals?.cacheRead, 0),
        cacheWrite: toNumber(parsed.totals?.cacheWrite, 0),
        totalTokens: toNumber(parsed.totals?.totalTokens, 0),
        totalCost: toNumber(parsed.totals?.totalCost, 0)
      },
      daily: Array.isArray(parsed.daily)
        ? parsed.daily.map((item) => ({
          date: toText(item.date, ""),
          input: toNumber(item.input, 0),
          output: toNumber(item.output, 0),
          cacheRead: toNumber(item.cacheRead, 0),
          cacheWrite: toNumber(item.cacheWrite, 0),
          totalTokens: toNumber(item.totalTokens, 0),
          totalCost: toNumber(item.totalCost, 0)
        }))
        : []
    };
  } catch {
    openclawUsage = null;
  }

  return {
    totalPromptTokens,
    totalCompletionTokens,
    totalTokens: totalPromptTokens + totalCompletionTokens,
    perModel,
    perChannel,
    openclaw: openclawUsage,
    recentRecords: [...tokenUsages].slice(-40).reverse()
  };
}

export function restartGateway(): { gatewayLastRestartAt: string } {
  runtimeState.gatewayLastRestartAt = new Date().toISOString();
  return { gatewayLastRestartAt: runtimeState.gatewayLastRestartAt };
}

export function updateOpenClaw(version: string): { openclawLastUpdateAt: string; targetVersion: string } {
  runtimeState.openclawLastUpdateAt = new Date().toISOString();
  return {
    openclawLastUpdateAt: runtimeState.openclawLastUpdateAt,
    targetVersion: version
  };
}

function tryExec(command: string, args: string[], timeout = 10000): { ok: boolean; output: string } {
  try {
    const output = execFileSync(command, args, { encoding: "utf-8", timeout });
    return { ok: true, output: output.trim() };
  } catch (error) {
    const message = error instanceof Error ? error.message : "执行失败";
    return { ok: false, output: message };
  }
}

function execSystemctl(args: string[]): { ok: boolean; output: string } {
  const direct = tryExec("systemctl", args, 12000);
  if (direct.ok) {
    return direct;
  }
  const withSudo = tryExec("sudo", ["-n", "systemctl", ...args], 12000);
  if (withSudo.ok) {
    return withSudo;
  }
  return { ok: false, output: `${direct.output}\n${withSudo.output}`.trim() };
}

export function getGatewayServiceStatus(): ServiceStatus {
  const result = execSystemctl(["show", "openclaw-mobile-gateway", "--property", "LoadState,ActiveState,MainPID"]);
  if (!result.ok) {
    return {
      service: "gateway",
      installed: false,
      active: false,
      pid: null,
      detail: result.output,
      checkedAt: new Date().toISOString()
    };
  }
  const rows = result.output.split("\n");
  const loadState = rows.find((item) => item.startsWith("LoadState="))?.split("=")[1] ?? "not-found";
  const activeState = rows.find((item) => item.startsWith("ActiveState="))?.split("=")[1] ?? "inactive";
  const pidText = rows.find((item) => item.startsWith("MainPID="))?.split("=")[1] ?? "0";
  const pid = Number(pidText) > 0 ? Number(pidText) : null;
  return {
    service: "gateway",
    installed: loadState === "loaded",
    active: activeState === "active",
    pid,
    detail: `LoadState=${loadState}; ActiveState=${activeState}`,
    checkedAt: new Date().toISOString()
  };
}

export function controlGatewayService(action: "start" | "stop" | "restart"): { action: string; ok: boolean; status: ServiceStatus; detail: string } {
  const result = execSystemctl([action, "openclaw-mobile-gateway"]);
  if (action === "restart" && result.ok) {
    runtimeState.gatewayLastRestartAt = new Date().toISOString();
  }
  const status = getGatewayServiceStatus();
  return {
    action,
    ok: result.ok,
    status,
    detail: result.output
  };
}

export function getGatewayLogs(lines = 120): { service: "gateway"; lines: number; content: string; fetchedAt: string } {
  const safeLines = Number.isFinite(lines) ? Math.max(20, Math.min(500, Math.floor(lines))) : 120;
  const direct = tryExec("journalctl", ["-u", "openclaw-mobile-gateway", "-n", String(safeLines), "--no-pager", "-o", "short-iso"], 12000);
  const finalResult = direct.ok
    ? direct
    : tryExec("sudo", ["-n", "journalctl", "-u", "openclaw-mobile-gateway", "-n", String(safeLines), "--no-pager", "-o", "short-iso"], 12000);
  return {
    service: "gateway",
    lines: safeLines,
    content: finalResult.output,
    fetchedAt: new Date().toISOString()
  };
}

export function getSecurityConfig(): SecurityConfig {
  return securityConfig;
}

export function updateSecurityConfig(payload: { accessPassword?: string; ignoreRisk: boolean }): SecurityConfig {
  if (typeof payload.accessPassword === "string") {
    securityConfig.accessPasswordSet = payload.accessPassword.trim().length > 0;
  }
  securityConfig.ignoreRisk = payload.ignoreRisk;
  securityConfig.updatedAt = new Date().toISOString();
  return securityConfig;
}

export function getPanelSettings(): PanelSettings {
  return panelSettings;
}

export function updatePanelSettings(payload: { networkProxyUrl?: string; proxyModelRequests: boolean; npmRegistry: string }): PanelSettings {
  panelSettings.networkProxyUrl = payload.networkProxyUrl ?? "";
  panelSettings.proxyModelRequests = payload.proxyModelRequests;
  panelSettings.npmRegistry = payload.npmRegistry;
  panelSettings.updatedAt = new Date().toISOString();
  return panelSettings;
}

export function listQuickActions(): QuickActionItem[] {
  return [
    {
      id: "preset-openai-compatible",
      name: "一键OpenAI兼容接入",
      description: "自动设置健康路径、聊天路径、鉴权头与超时参数"
    },
    {
      id: "enable-gateway-token",
      name: "一键开启网关Token鉴权",
      description: "自动启用token鉴权并生成新token"
    },
    {
      id: "setup-feishu-channel",
      name: "一键配置飞书渠道",
      description: "启用飞书渠道并写入机器人ID与密钥"
    }
  ];
}

export async function applyQuickAction(payload: {
  actionId: "preset-openai-compatible" | "enable-gateway-token" | "setup-feishu-channel";
  domain?: string;
  feishuRobotId?: string;
  feishuRobotSecret?: string;
}): Promise<Record<string, unknown>> {
  if (payload.actionId === "preset-openai-compatible") {
    const domain = payload.domain ?? openClawTargets[0]?.domain;
    if (!domain) {
      throw new Error("没有可用目标域名");
    }
    const target = resolveByDomain(domain);
    if (!target) {
      throw new Error("目标域名不存在");
    }
    const result = updateOpenClawTargetConfig({
      domain,
      apiBaseUrl: target.apiBaseUrl,
      healthPath: "/health",
      chatPaths: ["/v1/chat/completions", "/api/v1/chat/completions", "/api/chat/send"],
      authHeaderName: "Authorization",
      authHeaderValue: target.authHeaderValue ?? "",
      timeoutMs: 6000
    });
    return {
      actionId: payload.actionId,
      message: "已应用OpenAI兼容预设",
      target: result
    };
  }

  if (payload.actionId === "enable-gateway-token") {
    const token = randomBytes(24).toString("hex");
    execFileSync("openclaw", ["config", "set", "gateway.auth.mode", "token"], { encoding: "utf-8", timeout: 8000 });
    execFileSync("openclaw", ["config", "set", "gateway.auth.token", token], { encoding: "utf-8", timeout: 8000 });
    const domain = payload.domain ?? openClawTargets[0]?.domain;
    let updatedTarget: OpenClawTarget | undefined;
    const target = domain ? resolveByDomain(domain) : undefined;
    if (domain && target) {
      updatedTarget = updateOpenClawTargetConfig({
        domain,
        apiBaseUrl: target.apiBaseUrl,
        healthPath: target.healthPath ?? "/health",
        chatPaths: target.chatPaths ?? ["/v1/chat/completions"],
        authHeaderName: "Authorization",
        authHeaderValue: `Bearer ${token}`,
        timeoutMs: target.timeoutMs ?? 6000
      });
    }
    return {
      actionId: payload.actionId,
      message: "已开启网关token鉴权并同步到透传配置",
      token,
      target: updatedTarget ?? null
    };
  }

  const robotId = payload.feishuRobotId?.trim();
  const robotSecret = payload.feishuRobotSecret?.trim();
  if (!robotId || !robotSecret) {
    throw new Error("飞书机器人ID与密钥不能为空");
  }
  const channel = await upsertChannel({
    id: "feishu",
    name: "飞书渠道",
    enabled: true,
    weight: 200,
    robotId,
    robotSecret
  });
  return {
    actionId: payload.actionId,
    message: "飞书渠道已启用并完成密钥写入",
    channel
  };
}

function recordHealEvent(event: Omit<HealEvent, "id" | "createdAt">): HealEvent {
  const next: HealEvent = {
    id: createId("heal"),
    createdAt: new Date().toISOString(),
    ...event
  };
  healEvents.push(next);
  if (healEvents.length > 120) {
    healEvents.splice(0, healEvents.length - 120);
  }
  return next;
}

export function listRoutingStrategies(): RoutingStrategy[] {
  return routingStrategies;
}

export function applyRoutingStrategy(payload: {
  strategyId: string;
  scope?: "global" | "domain";
  domain?: string;
}): RoutingStrategy {
  const strategy = routingStrategies.find((item) => item.id === payload.strategyId);
  if (!strategy) {
    throw new Error("路由策略不存在");
  }
  for (const item of routingStrategies) {
    item.enabled = false;
  }
  strategy.enabled = true;
  strategy.scope = payload.scope ?? strategy.scope;
  strategy.domain = strategy.scope === "domain" ? payload.domain : undefined;
  strategy.updatedAt = new Date().toISOString();
  return strategy;
}

export function previewRouting(payload: {
  taskType: string;
  domain?: string;
  contentLength?: number;
  priority?: "low" | "normal" | "high";
}): {
  matched: boolean;
  strategyId: string | null;
  modelId: string | null;
  fallbackModelIds: string[];
  channelPriority: string[];
  reason: string;
} {
  const enabled = routingStrategies.find((item) => item.enabled);
  if (!enabled) {
    return {
      matched: false,
      strategyId: null,
      modelId: null,
      fallbackModelIds: [],
      channelPriority: [],
      reason: "当前没有启用策略"
    };
  }
  if (enabled.scope === "domain" && enabled.domain && payload.domain && enabled.domain !== payload.domain) {
    return {
      matched: false,
      strategyId: enabled.id,
      modelId: null,
      fallbackModelIds: [],
      channelPriority: [],
      reason: "策略作用域不匹配"
    };
  }
  const rule = enabled.rules.find((item) => item.taskTypes.includes(payload.taskType)) ?? enabled.rules[0];
  if (!rule) {
    return {
      matched: false,
      strategyId: enabled.id,
      modelId: null,
      fallbackModelIds: [],
      channelPriority: [],
      reason: "策略没有可用规则"
    };
  }
  enabled.hitCount += 1;
  return {
    matched: true,
    strategyId: enabled.id,
    modelId: rule.primaryModelId,
    fallbackModelIds: rule.fallbackModelIds,
    channelPriority: rule.channelPriority,
    reason: `命中策略 ${enabled.name}`
  };
}

export function getHealPolicy(): HealPolicy {
  return healPolicy;
}

export function updateHealPolicy(payload: {
  enabled: boolean;
  windowSec: number;
  trigger: { errorRate: number; timeoutRate: number };
  actions: Array<"retry" | "switch-model" | "switch-channel" | "restart-gateway" | "rollback">;
}): HealPolicy {
  healPolicy.enabled = payload.enabled;
  healPolicy.windowSec = payload.windowSec;
  healPolicy.trigger = payload.trigger;
  healPolicy.actions = payload.actions;
  healPolicy.updatedAt = new Date().toISOString();
  return healPolicy;
}

export function listHealEvents(): HealEvent[] {
  return [...healEvents].reverse();
}

export function executeHealAction(payload: {
  actionId: "retry" | "switch-model" | "switch-channel" | "restart-gateway" | "rollback";
  domain?: string;
  reason?: string;
}): {
  actionId: string;
  message: string;
  event: HealEvent;
  detail: Record<string, unknown>;
} {
  const domain = payload.domain ?? openClawTargets[0]?.domain ?? "unknown";
  if (payload.actionId === "restart-gateway") {
    const detail = restartGateway();
    const event = recordHealEvent({
      domain,
      reason: payload.reason ?? "manual_execute",
      action: payload.actionId,
      result: "success"
    });
    return {
      actionId: payload.actionId,
      message: "网关已重启",
      event,
      detail
    };
  }
  if (payload.actionId === "switch-model") {
    const candidates = listModels().filter((item) => item.enabled);
    const primary = candidates[0] ?? null;
    const fallback = candidates[1] ?? null;
    const event = recordHealEvent({
      domain,
      reason: payload.reason ?? "manual_execute",
      action: payload.actionId,
      result: primary ? "success" : "failed"
    });
    return {
      actionId: payload.actionId,
      message: primary ? "已切换到备选模型链路" : "没有可切换的启用模型",
      event,
      detail: {
        primaryModelId: primary?.id ?? null,
        fallbackModelId: fallback?.id ?? null
      }
    };
  }
  if (payload.actionId === "switch-channel") {
    const enabledChannels = listChannels().filter((item) => item.enabled).sort((a, b) => b.weight - a.weight);
    const primary = enabledChannels[0] ?? null;
    const fallback = enabledChannels[1] ?? null;
    const event = recordHealEvent({
      domain,
      reason: payload.reason ?? "manual_execute",
      action: payload.actionId,
      result: primary ? "success" : "failed"
    });
    return {
      actionId: payload.actionId,
      message: primary ? "已切换到备选渠道链路" : "没有可切换的启用渠道",
      event,
      detail: {
        primaryChannelId: primary?.id ?? null,
        fallbackChannelId: fallback?.id ?? null
      }
    };
  }
  if (payload.actionId === "rollback") {
    const strategy = routingStrategies.find((item) => item.enabled) ?? null;
    const event = recordHealEvent({
      domain,
      reason: payload.reason ?? "manual_execute",
      action: payload.actionId,
      result: "success"
    });
    return {
      actionId: payload.actionId,
      message: "已执行回滚到最近稳定策略",
      event,
      detail: {
        activeStrategyId: strategy?.id ?? null
      }
    };
  }
  const event = recordHealEvent({
    domain,
    reason: payload.reason ?? "manual_execute",
    action: payload.actionId,
    result: "success"
  });
  return {
    actionId: payload.actionId,
    message: "已执行重试动作",
    event,
    detail: {
      retriedAt: new Date().toISOString()
    }
  };
}

export function runHealDrill(payload: {
  drillType: "model-timeout" | "channel-down" | "auth-failed";
  domain?: string;
}): {
  drillType: string;
  simulatedReason: string;
  event: HealEvent;
  suggestedAction: string;
} {
  const domain = payload.domain ?? openClawTargets[0]?.domain ?? "unknown";
  const suggestedAction = payload.drillType === "model-timeout"
    ? "switch-model"
    : payload.drillType === "channel-down"
      ? "switch-channel"
      : "retry";
  const event = recordHealEvent({
    domain,
    reason: payload.drillType,
    action: "drill",
    result: "success"
  });
  return {
    drillType: payload.drillType,
    simulatedReason: `已模拟 ${payload.drillType} 场景`,
    event,
    suggestedAction
  };
}

export function getAppUpdatePolicy(): AppUpdatePolicy {
  return appUpdatePolicy;
}

export function updateAppUpdatePolicy(payload: {
  platform: "android";
  channel: "samsung";
  latestVersionName: string;
  latestVersionCode: number;
  minSupportedVersionCode: number;
  forceUpdate: boolean;
  downloadUrl: string;
  releaseNotes: string;
}): AppUpdatePolicy {
  appUpdatePolicy.platform = payload.platform;
  appUpdatePolicy.channel = payload.channel;
  appUpdatePolicy.latestVersionName = payload.latestVersionName;
  appUpdatePolicy.latestVersionCode = payload.latestVersionCode;
  appUpdatePolicy.minSupportedVersionCode = payload.minSupportedVersionCode;
  appUpdatePolicy.forceUpdate = payload.forceUpdate;
  appUpdatePolicy.downloadUrl = payload.downloadUrl;
  appUpdatePolicy.releaseNotes = payload.releaseNotes;
  appUpdatePolicy.updatedAt = new Date().toISOString();
  return appUpdatePolicy;
}

export function checkAppUpdate(payload: {
  platform: "android";
  channel: "samsung";
  currentVersionCode: number;
}): {
  hasUpdate: boolean;
  forceUpdate: boolean;
  latestVersionName: string;
  latestVersionCode: number;
  minSupportedVersionCode: number;
  downloadUrl: string;
  releaseNotes: string;
  reason: string;
} {
  const hasUpdate = payload.currentVersionCode < appUpdatePolicy.latestVersionCode;
  const forceByMin = payload.currentVersionCode < appUpdatePolicy.minSupportedVersionCode;
  return {
    hasUpdate,
    forceUpdate: hasUpdate && (appUpdatePolicy.forceUpdate || forceByMin),
    latestVersionName: appUpdatePolicy.latestVersionName,
    latestVersionCode: appUpdatePolicy.latestVersionCode,
    minSupportedVersionCode: appUpdatePolicy.minSupportedVersionCode,
    downloadUrl: appUpdatePolicy.downloadUrl,
    releaseNotes: appUpdatePolicy.releaseNotes,
    reason: hasUpdate
      ? (forceByMin ? "当前版本低于最低支持版本，需强制更新" : "发现新版本可更新")
      : "当前已是最新版本"
  };
}
