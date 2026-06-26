import path from "path";
import { AgentProfile, AppUpdatePolicy, AssistantMessage, AssistantSession, ChannelConfig, ChatWsSession, CommunicationConfig, CronJob, HealEvent, HealPolicy, ModelConfig, OpenClawTarget, PanelSettings, RoutingStrategy, SecurityConfig, SkillConfig, TokenUsageRecord } from "./types";
import { createId } from "./utils";

export const markdownDir = path.resolve(process.cwd(), "../../data/markdown");
export const memoryDir = path.resolve(process.cwd(), "../../data/memory");

export const openClawTargets: OpenClawTarget[] = [
  {
    domain: "alpha.openclaw.local",
    version: "v1",
    apiBaseUrl: "https://alpha.openclaw.local/api",
    healthPath: "/health",
    chatPaths: ["/chat/send"],
    timeoutMs: 2500
  },
  {
    domain: "beta.openclaw.local",
    version: "v2",
    apiBaseUrl: "https://beta.openclaw.local/api",
    healthPath: "/health",
    chatPaths: ["/chat/send"],
    timeoutMs: 2500
  },
  {
    domain: "prod.openclaw.local",
    version: "v3",
    apiBaseUrl: "https://prod.openclaw.local/api",
    healthPath: "/health",
    chatPaths: ["/chat/send"],
    timeoutMs: 2500
  },
  {
    domain: "openclaws.gdcp.edu.cn",
    version: "v3",
    apiBaseUrl: "https://openclaws.gdcp.edu.cn",
    healthPath: "/health",
    chatPaths: ["/v1/chat/completions"],
    authHeaderName: "Authorization",
    authHeaderValue: "",
    timeoutMs: 6000
  }
];

export const models: ModelConfig[] = [
  { id: "gpt-4.1", modelId: "gpt-4.1", providerId: "openai", platform: "openai", name: "GPT-4.1", enabled: true, maxTokens: 8192 },
  { id: "claude-3.7", modelId: "claude-3.7", providerId: "anthropic", platform: "anthropic", name: "Claude 3.7", enabled: true, maxTokens: 8192 },
  { id: "qwen-max", modelId: "qwen-max", providerId: "qwen", platform: "qwen", name: "Qwen Max", enabled: false, maxTokens: 4096 }
];

export const skills: SkillConfig[] = [
  { id: "knowledge", name: "知识检索", enabled: true, description: "从知识库检索背景信息", group: "内置技能" },
  { id: "workflow", name: "工作流执行", enabled: true, description: "执行预定义流程任务", group: "内置技能" }
];

export const channels: ChannelConfig[] = [
  { id: "default", name: "默认渠道", enabled: true, weight: 100 },
  { id: "vip", name: "VIP渠道", enabled: true, weight: 200 }
];

export const tokenUsages: TokenUsageRecord[] = [];

export const runtimeState = {
  gatewayLastRestartAt: "",
  openclawLastUpdateAt: ""
};

export const routingStrategies: RoutingStrategy[] = [
  {
    id: "code-first",
    name: "代码任务优先",
    description: "代码任务优先使用编码模型，失败自动回退",
    enabled: false,
    scope: "global",
    rules: [
      {
        taskTypes: ["code", "debug", "review"],
        primaryModelId: "qwen3-coder-plus",
        fallbackModelIds: ["qwen3.5-plus", "gpt-4.1"],
        channelPriority: ["vip", "default"]
      }
    ],
    hitCount: 0,
    updatedAt: new Date().toISOString()
  },
  {
    id: "cost-first",
    name: "低成本优先",
    description: "总结问答优先使用低成本模型并限制单次预算",
    enabled: false,
    scope: "global",
    rules: [
      {
        taskTypes: ["summary", "qa", "translate"],
        primaryModelId: "qwen3.5-plus",
        fallbackModelIds: ["kimi-k2.5", "gpt-4.1"],
        channelPriority: ["default", "vip"],
        maxBudgetPerRequest: 0.02
      }
    ],
    hitCount: 0,
    updatedAt: new Date().toISOString()
  },
  {
    id: "stability-first",
    name: "高稳定优先",
    description: "高峰期优先稳定链路并启用多级回退",
    enabled: false,
    scope: "global",
    rules: [
      {
        taskTypes: ["general", "ops"],
        primaryModelId: "gpt-4.1",
        fallbackModelIds: ["qwen3.5-plus", "kimi-k2.5"],
        channelPriority: ["vip", "default"]
      }
    ],
    hitCount: 0,
    updatedAt: new Date().toISOString()
  }
];

export const healPolicy: HealPolicy = {
  enabled: true,
  windowSec: 120,
  trigger: {
    errorRate: 0.2,
    timeoutRate: 0.15
  },
  actions: ["retry", "switch-model", "restart-gateway"],
  updatedAt: new Date().toISOString()
};

export const healEvents: HealEvent[] = [];

export const appUpdatePolicy: AppUpdatePolicy = {
  platform: "android",
  channel: "samsung",
  latestVersionName: "1.0.0",
  latestVersionCode: 10016,
  minSupportedVersionCode: 10010,
  forceUpdate: false,
  downloadUrl: "",
  releaseNotes: "修复已知问题并优化体验",
  updatedAt: new Date().toISOString()
};

export const securityConfig: SecurityConfig = {
  accessPasswordSet: false,
  ignoreRisk: false,
  updatedAt: new Date().toISOString()
};

export const panelSettings: PanelSettings = {
  networkProxyUrl: "",
  proxyModelRequests: false,
  npmRegistry: "https://registry.npmjs.org",
  updatedAt: new Date().toISOString()
};

export const agents: AgentProfile[] = [
  {
    id: "default-agent",
    name: "默认助手",
    workspace: process.cwd(),
    enabled: true,
    primaryModelId: "gpt-4.1",
    fallbackModelIds: ["claude-3.7"],
    updatedAt: new Date().toISOString()
  }
];

export const communicationConfig: CommunicationConfig = {
  messages: {
    autoReplyEnabled: true,
    autoReplyTemplate: "已收到消息，正在处理。"
  },
  broadcast: {
    strategy: "priority",
    defaultChannelId: "feishu"
  },
  commands: {
    enabled: true,
    prefix: "/"
  },
  hooks: {
    enabled: false,
    webhookUrl: ""
  },
  approvals: {
    execEnabled: true,
    requireConfirm: true
  },
  updatedAt: new Date().toISOString()
};

export const cronJobs: CronJob[] = [];

export const chatWsSessions: ChatWsSession[] = [];

export const assistantSessions: AssistantSession[] = [];

export const assistantMessages: AssistantMessage[] = [];

export function seedTokenUsage(): void {
  if (process.env.OPENCLAW_SEED_TOKEN_USAGE !== "1") {
    return;
  }
  if (tokenUsages.length > 0) {
    return;
  }

  tokenUsages.push(
    {
      id: createId("tok"),
      modelId: "gpt-4.1",
      channelId: "default",
      promptTokens: 140,
      completionTokens: 230,
      createdAt: new Date().toISOString()
    },
    {
      id: createId("tok"),
      modelId: "claude-3.7",
      channelId: "vip",
      promptTokens: 420,
      completionTokens: 600,
      createdAt: new Date().toISOString()
    }
  );
}
