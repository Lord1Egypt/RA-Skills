import { z } from "zod";

export const domainResolveSchema = z.object({
  domain: z.string().min(3)
});

export const chatSchema = z.object({
  domain: z.string().min(3),
  modelId: z.string().min(1),
  channelId: z.string().min(1),
  messages: z.array(
    z.object({
      role: z.enum(["system", "user", "assistant"]),
      content: z.string().min(1)
    })
  )
});

export const modelSchema = z.object({
  id: z.string().min(1),
  modelId: z.string().min(1).optional(),
  providerId: z.string().min(1).optional(),
  platform: z.string().min(1).optional(),
  name: z.string().min(1),
  enabled: z.boolean(),
  maxTokens: z.number().int().positive(),
  apiKey: z.string().optional(),
  baseUrl: z.string().url().optional()
});

export const skillSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  enabled: z.boolean(),
  description: z.string().min(1),
  group: z.string().min(1)
});

export const channelSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  enabled: z.boolean(),
  weight: z.number().int().min(0),
  robotId: z.string().optional(),
  robotSecret: z.string().optional()
});

export const markdownUpdateSchema = z.object({
  fileName: z.string().endsWith(".md"),
  content: z.string()
});

export const openClawTargetUpdateSchema = z.object({
  domain: z.string().min(3),
  apiBaseUrl: z.string().url(),
  healthPath: z.string().min(1),
  chatPaths: z.array(z.string().min(1)).min(1),
  authHeaderName: z.string().optional(),
  authHeaderValue: z.string().optional(),
  extraHeaders: z.record(z.string(), z.string()).optional(),
  timeoutMs: z.number().int().min(500).max(20000).optional()
});

export const quickActionSchema = z.object({
  actionId: z.enum(["preset-openai-compatible", "enable-gateway-token", "setup-feishu-channel"]),
  domain: z.string().min(3).optional(),
  feishuRobotId: z.string().optional(),
  feishuRobotSecret: z.string().optional()
});

export const routingApplySchema = z.object({
  strategyId: z.string().min(1),
  scope: z.enum(["global", "domain"]).optional(),
  domain: z.string().min(3).optional()
});

export const routingPreviewSchema = z.object({
  taskType: z.string().min(1),
  domain: z.string().min(3).optional(),
  contentLength: z.number().int().min(0).optional(),
  priority: z.enum(["low", "normal", "high"]).optional()
});

export const healPolicySchema = z.object({
  enabled: z.boolean(),
  windowSec: z.number().int().min(30).max(1800),
  trigger: z.object({
    errorRate: z.number().min(0).max(1),
    timeoutRate: z.number().min(0).max(1)
  }),
  actions: z.array(z.enum(["retry", "switch-model", "switch-channel", "restart-gateway", "rollback"])).min(1)
});

export const healExecuteSchema = z.object({
  actionId: z.enum(["retry", "switch-model", "switch-channel", "restart-gateway", "rollback"]),
  domain: z.string().min(3).optional(),
  reason: z.string().min(1).optional()
});

export const healDrillSchema = z.object({
  drillType: z.enum(["model-timeout", "channel-down", "auth-failed"]),
  domain: z.string().min(3).optional()
});

export const appUpdatePolicySchema = z.object({
  platform: z.literal("android"),
  channel: z.literal("samsung"),
  latestVersionName: z.string().min(1),
  latestVersionCode: z.number().int().positive(),
  minSupportedVersionCode: z.number().int().positive(),
  forceUpdate: z.boolean(),
  downloadUrl: z.string().url(),
  releaseNotes: z.string().min(1)
});

export const appUpdateCheckSchema = z.object({
  platform: z.literal("android"),
  channel: z.literal("samsung"),
  currentVersionCode: z.number().int().positive()
});

export const gatewayServiceControlSchema = z.object({
  action: z.enum(["start", "stop", "restart"])
});

export const gatewayLogsQuerySchema = z.object({
  lines: z.coerce.number().int().min(20).max(500).optional()
});

export const securityConfigSchema = z.object({
  accessPassword: z.string().optional(),
  ignoreRisk: z.boolean()
});

export const panelSettingsSchema = z.object({
  networkProxyUrl: z.string().default(""),
  proxyModelRequests: z.boolean(),
  npmRegistry: z.string().url()
});

export const agentSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  workspace: z.string().min(1),
  enabled: z.boolean(),
  primaryModelId: z.string().min(1),
  fallbackModelIds: z.array(z.string().min(1)),
  updatedAt: z.string().optional()
});

export const communicationConfigSchema = z.object({
  messages: z.object({
    autoReplyEnabled: z.boolean(),
    autoReplyTemplate: z.string()
  }),
  broadcast: z.object({
    strategy: z.enum(["all", "priority"]),
    defaultChannelId: z.string().min(1)
  }),
  commands: z.object({
    enabled: z.boolean(),
    prefix: z.string().min(1)
  }),
  hooks: z.object({
    enabled: z.boolean(),
    webhookUrl: z.string()
  }),
  approvals: z.object({
    execEnabled: z.boolean(),
    requireConfirm: z.boolean()
  }),
  updatedAt: z.string().optional()
});

export const memoryQuerySchema = z.object({
  agentId: z.string().min(1),
  category: z.string().min(1)
});

export const memoryUpsertSchema = z.object({
  agentId: z.string().min(1),
  category: z.string().min(1),
  fileName: z.string().min(1),
  content: z.string()
});

export const memoryDeleteSchema = z.object({
  agentId: z.string().min(1),
  category: z.string().min(1),
  fileName: z.string().min(1)
});

export const usageSummaryQuerySchema = z.object({
  days: z.coerce.number().int().min(1).max(90).optional()
});

export const cronJobSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  cron: z.string().min(1),
  enabled: z.boolean(),
  taskType: z.string().min(1),
  payload: z.string(),
  updatedAt: z.string().optional()
});

export const cronRunSchema = z.object({
  id: z.string().min(1)
});

export const wsSendSchema = z.object({
  sessionId: z.string().min(1),
  domain: z.string().min(1),
  modelId: z.string().min(1),
  channelId: z.string().min(1),
  message: z.string().min(1)
});

export const assistantSessionCreateSchema = z.object({
  title: z.string().default("新会话")
});

export const assistantMessagesQuerySchema = z.object({
  sessionId: z.string().min(1)
});

export const assistantSendSchema = z.object({
  sessionId: z.string().min(1),
  domain: z.string().min(1),
  modelId: z.string().min(1),
  channelId: z.string().min(1),
  content: z.string().min(1)
});

export const skillSearchQuerySchema = z.object({
  keyword: z.string().optional()
});

export const skillDependencyQuerySchema = z.object({
  skillId: z.string().min(1)
});

export const skillInstallSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  description: z.string(),
  enabled: z.boolean().optional()
});

export const aboutUpgradeSchema = z.object({
  version: z.string().min(1)
});
