import cors from "cors";
import express from "express";
import { z } from "zod";
import {
  appUpdateCheckSchema,
  appUpdatePolicySchema,
  agentSchema,
  assistantMessagesQuerySchema,
  assistantSendSchema,
  assistantSessionCreateSchema,
  aboutUpgradeSchema,
  channelSchema,
  chatSchema,
  communicationConfigSchema,
  cronJobSchema,
  cronRunSchema,
  domainResolveSchema,
  gatewayLogsQuerySchema,
  gatewayServiceControlSchema,
  healDrillSchema,
  healExecuteSchema,
  healPolicySchema,
  markdownUpdateSchema,
  memoryDeleteSchema,
  memoryQuerySchema,
  memoryUpsertSchema,
  modelSchema,
  openClawTargetUpdateSchema,
  panelSettingsSchema,
  quickActionSchema,
  routingApplySchema,
  routingPreviewSchema,
  securityConfigSchema,
  skillDependencyQuerySchema,
  skillInstallSchema,
  skillSearchQuerySchema,
  skillSchema,
  usageSummaryQuerySchema,
  wsSendSchema
} from "./schemas";
import { seedTokenUsage } from "./store";
import {
  applyQuickAction,
  applyRoutingStrategy,
  checkAppUpdate,
  connectChatWs,
  controlGatewayService,
  createAssistantSession,
  deleteAgent,
  deleteCronJob,
  deleteMemoryFile,
  executeHealAction,
  getAboutInfo,
  getChatWsConfig,
  getCommunicationConfig,
  getGatewayLogs,
  getGatewayServiceStatus,
  getAppUpdatePolicy,
  getHealPolicy,
  getPanelSettings,
  getSecurityConfig,
  getTokenStats,
  getUsageSummary,
  installSkill,
  listAgents,
  listAssistantMessages,
  listAssistantSessions,
  listChatWsSessions,
  listCronJobs,
  listHealEvents,
  listMemoryFiles,
  listOpenClawTargets,
  listChannels,
  listRoutingStrategies,
  listQuickActions,
  listMarkdownFiles,
  listModels,
  listSkills,
  probeOpenClawTarget,
  previewRouting,
  resolveByDomain,
  restartGateway,
  runCronJob,
  runHealDrill,
  checkSkillDependencies,
  searchSkills,
  sendAssistantMessage,
  sendWsChatMessage,
  sendMessageToOpenClaw,
  uninstallOpenClawMock,
  uninstallSkill,
  updatePanelSettings,
  updateAppUpdatePolicy,
  updateCommunicationConfig,
  updateSecurityConfig,
  updateHealPolicy,
  updateOpenClawTargetConfig,
  updateMarkdownFile,
  updateOpenClaw,
  upsertChannel,
  upsertCronJob,
  upsertAgent,
  upsertMemoryFile,
  upsertModel,
  upsertSkill
} from "./services";

function parseRequest<T>(schema: z.ZodSchema<T>, input: unknown): T {
  // 核心逻辑：统一参数校验入口，保证每个管理接口的输入结构安全可控。
  return schema.parse(input);
}

export function createApp() {
  const app = express();
  seedTokenUsage();

  app.use(cors());
  app.use(express.json({ limit: "2mb" }));

  app.get("/health", (_req, res) => {
    res.json({ ok: true, service: "openclaw-mobile-admin-gateway" });
  });

  app.get("/api/openclaw/resolve", (req, res) => {
    const query = parseRequest(domainResolveSchema, req.query);
    const target = resolveByDomain(query.domain);
    if (!target) {
      return res.status(404).json({ message: "未找到对应域名的 OpenClaw 目标" });
    }
    return res.json(target);
  });

  app.get("/api/openclaw/targets", (_req, res) => {
    return res.json(listOpenClawTargets());
  });

  app.put("/api/openclaw/targets", (req, res) => {
    const payload = parseRequest(openClawTargetUpdateSchema, req.body);
    const result = updateOpenClawTargetConfig(payload);
    return res.json(result);
  });

  app.get("/api/openclaw/probe", async (req, res) => {
    const query = parseRequest(domainResolveSchema, req.query);
    const target = resolveByDomain(query.domain);
    if (!target) {
      return res.status(404).json({ message: "未找到对应域名的 OpenClaw 目标" });
    }
    const result = await probeOpenClawTarget(target);
    return res.json({
      domain: query.domain,
      openclawVersion: target.version,
      apiBaseUrl: target.apiBaseUrl,
      ...result
    });
  });

  app.post("/api/chat/send", async (req, res) => {
    const payload = parseRequest(chatSchema, req.body);
    const target = resolveByDomain(payload.domain);
    if (!target) {
      return res.status(404).json({ message: "域名未接入网关" });
    }

    // 核心逻辑：优先尝试透传调用真实 OpenClaw，失败时自动回退到本地模拟，保证后台管理可连续使用。
    const result = await sendMessageToOpenClaw({
      target,
      modelId: payload.modelId,
      channelId: payload.channelId,
      messages: payload.messages
    });

    return res.json({
      domain: payload.domain,
      openclawVersion: target.version,
      mode: result.mode,
      reply: result.reply,
      usage: result.usage,
      proxyDetail: result.proxyDetail ?? null
    });
  });

  app.get("/api/models", (_req, res) => {
    res.json(listModels());
  });

  app.put("/api/models", async (req, res, next) => {
    try {
      const payload = parseRequest(modelSchema, req.body);
      const modelId = payload.modelId ?? payload.id;
      const nextModel = {
        ...payload,
        modelId,
        providerId: payload.providerId ?? payload.platform ?? "openai",
        platform: payload.platform ?? payload.providerId ?? "openai"
      };
      res.json(await upsertModel(nextModel));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/skills", (_req, res) => {
    res.json(listSkills());
  });

  app.put("/api/skills", (req, res) => {
    const payload = parseRequest(skillSchema, req.body);
    res.json(upsertSkill(payload));
  });

  app.get("/api/channels", (_req, res) => {
    res.json(listChannels());
  });

  app.put("/api/channels", async (req, res, next) => {
    try {
      const payload = parseRequest(channelSchema, req.body);
      res.json(await upsertChannel(payload));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/agents", (_req, res) => {
    res.json(listAgents());
  });

  app.put("/api/agents", async (req, res, next) => {
    try {
      const payload = parseRequest(agentSchema, req.body);
      res.json(await upsertAgent({
        ...payload,
        updatedAt: new Date().toISOString()
      }));
    } catch (error) {
      next(error);
    }
  });

  app.delete("/api/agents", async (req, res, next) => {
    try {
      const query = parseRequest(z.object({ id: z.string().min(1) }), req.query);
      res.json(await deleteAgent(query.id));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/communication/config", (_req, res) => {
    res.json(getCommunicationConfig());
  });

  app.put("/api/communication/config", async (req, res, next) => {
    try {
      const payload = parseRequest(communicationConfigSchema, req.body);
      res.json(await updateCommunicationConfig({
        ...payload,
        updatedAt: new Date().toISOString()
      }));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/memory/files", async (req, res, next) => {
    try {
      const query = parseRequest(memoryQuerySchema, req.query);
      res.json(await listMemoryFiles(query.agentId, query.category));
    } catch (error) {
      next(error);
    }
  });

  app.put("/api/memory/files", async (req, res, next) => {
    try {
      const payload = parseRequest(memoryUpsertSchema, req.body);
      res.json(await upsertMemoryFile(payload));
    } catch (error) {
      next(error);
    }
  });

  app.delete("/api/memory/files", async (req, res, next) => {
    try {
      const query = parseRequest(memoryDeleteSchema, req.query);
      res.json(await deleteMemoryFile(query));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/usage/summary", (req, res) => {
    const query = parseRequest(usageSummaryQuerySchema, req.query);
    res.json(getUsageSummary(query.days ?? 7));
  });

  app.get("/api/cron/jobs", (_req, res) => {
    res.json(listCronJobs());
  });

  app.put("/api/cron/jobs", (req, res) => {
    const payload = parseRequest(cronJobSchema, req.body);
    res.json(upsertCronJob({
      ...payload,
      updatedAt: new Date().toISOString()
    }));
  });

  app.delete("/api/cron/jobs", (req, res) => {
    const query = parseRequest(cronRunSchema, req.query);
    res.json(deleteCronJob(query.id));
  });

  app.post("/api/cron/jobs/run", (req, res) => {
    const payload = parseRequest(cronRunSchema, req.body);
    res.json(runCronJob(payload.id));
  });

  app.get("/api/chat/ws/config", (req, res) => {
    const baseUrl = `${req.protocol}://${req.get("host")}`;
    res.json(getChatWsConfig(baseUrl));
  });

  app.post("/api/chat/ws/connect", (_req, res) => {
    res.json(connectChatWs());
  });

  app.get("/api/chat/ws/sessions", (_req, res) => {
    res.json(listChatWsSessions());
  });

  app.post("/api/chat/ws/send", async (req, res, next) => {
    try {
      const payload = parseRequest(wsSendSchema, req.body);
      const target = resolveByDomain(payload.domain);
      if (!target) {
        return res.status(404).json({ message: "未找到对应域名的 OpenClaw 目标" });
      }
      const result = await sendWsChatMessage({
        sessionId: payload.sessionId,
        target,
        modelId: payload.modelId,
        channelId: payload.channelId,
        message: payload.message
      });
      return res.json(result);
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/assistant/sessions", (_req, res) => {
    res.json(listAssistantSessions());
  });

  app.post("/api/assistant/sessions", (req, res) => {
    const payload = parseRequest(assistantSessionCreateSchema, req.body);
    res.json(createAssistantSession(payload.title ?? "新会话"));
  });

  app.get("/api/assistant/messages", (req, res) => {
    const query = parseRequest(assistantMessagesQuerySchema, req.query);
    res.json(listAssistantMessages(query.sessionId));
  });

  app.post("/api/assistant/messages", async (req, res, next) => {
    try {
      const payload = parseRequest(assistantSendSchema, req.body);
      const target = resolveByDomain(payload.domain);
      if (!target) {
        return res.status(404).json({ message: "未找到对应域名的 OpenClaw 目标" });
      }
      const result = await sendAssistantMessage({
        sessionId: payload.sessionId,
        content: payload.content,
        target,
        modelId: payload.modelId,
        channelId: payload.channelId
      });
      return res.json(result);
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/skills/search", (req, res) => {
    const query = parseRequest(skillSearchQuerySchema, req.query);
    res.json(searchSkills(query.keyword ?? ""));
  });

  app.get("/api/skills/dependencies/check", (req, res) => {
    const query = parseRequest(skillDependencyQuerySchema, req.query);
    res.json(checkSkillDependencies(query.skillId));
  });

  app.post("/api/skills/install", async (req, res, next) => {
    try {
      const payload = parseRequest(skillInstallSchema, req.body);
      const dependency = checkSkillDependencies(payload.id);
      if (!dependency.ready) {
        return res.status(400).json({
          message: "依赖检查未通过",
          dependency
        });
      }
      res.json(await installSkill({
        id: payload.id,
        name: payload.name,
        description: payload.description,
        enabled: payload.enabled ?? true,
        group: "custom"
      }));
    } catch (error) {
      next(error);
    }
  });

  app.delete("/api/skills/uninstall", (req, res) => {
    const query = parseRequest(z.object({ id: z.string().min(1) }), req.query);
    res.json(uninstallSkill(query.id));
  });

  app.get("/api/about/info", (_req, res) => {
    res.json(getAboutInfo());
  });

  app.post("/api/about/upgrade", (req, res) => {
    const payload = parseRequest(aboutUpgradeSchema, req.body);
    res.json(updateOpenClaw(payload.version));
  });

  app.post("/api/about/uninstall", (_req, res) => {
    res.json(uninstallOpenClawMock());
  });

  app.get("/api/md-files", async (_req, res, next) => {
    try {
      const files = await listMarkdownFiles();
      res.json(files);
    } catch (error) {
      next(error);
    }
  });

  app.put("/api/md-files", async (req, res, next) => {
    try {
      const payload = parseRequest(markdownUpdateSchema, req.body);
      const result = await updateMarkdownFile(payload.fileName, payload.content);
      res.json(result);
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/token-stats", (_req, res) => {
    res.json(getTokenStats());
  });

  app.get("/api/quick-actions", (_req, res) => {
    res.json(listQuickActions());
  });

  app.post("/api/quick-actions/apply", async (req, res, next) => {
    try {
      const payload = parseRequest(quickActionSchema, req.body);
      res.json(await applyQuickAction(payload));
    } catch (error) {
      next(error);
    }
  });

  app.get("/api/routing/strategies", (_req, res) => {
    res.json(listRoutingStrategies());
  });

  app.post("/api/routing/strategies/apply", (req, res) => {
    const payload = parseRequest(routingApplySchema, req.body);
    res.json(applyRoutingStrategy(payload));
  });

  app.post("/api/routing/preview", (req, res) => {
    const payload = parseRequest(routingPreviewSchema, req.body);
    res.json(previewRouting(payload));
  });

  app.get("/api/heal/policies", (_req, res) => {
    res.json(getHealPolicy());
  });

  app.put("/api/heal/policies", (req, res) => {
    const payload = parseRequest(healPolicySchema, req.body);
    res.json(updateHealPolicy(payload));
  });

  app.post("/api/heal/execute", (req, res) => {
    const payload = parseRequest(healExecuteSchema, req.body);
    res.json(executeHealAction(payload));
  });

  app.post("/api/heal/drill", (req, res) => {
    const payload = parseRequest(healDrillSchema, req.body);
    res.json(runHealDrill(payload));
  });

  app.get("/api/heal/events", (_req, res) => {
    res.json(listHealEvents());
  });

  app.get("/api/services/status", (_req, res) => {
    res.json(getGatewayServiceStatus());
  });

  app.post("/api/services/control", (req, res) => {
    const payload = parseRequest(gatewayServiceControlSchema, req.body);
    res.json(controlGatewayService(payload.action));
  });

  app.get("/api/logs/tail", (req, res) => {
    const query = parseRequest(gatewayLogsQuerySchema, req.query);
    res.json(getGatewayLogs(query.lines ?? 120));
  });

  app.get("/api/security/config", (_req, res) => {
    res.json(getSecurityConfig());
  });

  app.put("/api/security/config", (req, res) => {
    const payload = parseRequest(securityConfigSchema, req.body);
    res.json(updateSecurityConfig(payload));
  });

  app.get("/api/settings/panel", (_req, res) => {
    res.json(getPanelSettings());
  });

  app.put("/api/settings/panel", (req, res) => {
    const payload = parseRequest(panelSettingsSchema, req.body);
    res.json(updatePanelSettings(payload));
  });

  app.get("/api/app-update/policy", (_req, res) => {
    res.json(getAppUpdatePolicy());
  });

  app.put("/api/app-update/policy", (req, res) => {
    const payload = parseRequest(appUpdatePolicySchema, req.body);
    res.json(updateAppUpdatePolicy(payload));
  });

  app.post("/api/app-update/check", (req, res) => {
    const payload = parseRequest(appUpdateCheckSchema, req.body);
    res.json(checkAppUpdate(payload));
  });

  app.post("/api/system/restart-gateway", (_req, res) => {
    res.json(restartGateway());
  });

  app.post("/api/system/update-openclaw", (req, res) => {
    const payload = z.object({ version: z.string().min(1) }).parse(req.body);
    res.json(updateOpenClaw(payload.version));
  });

  app.use((error: unknown, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
    // 核心逻辑：把参数错误和运行时错误分层返回，方便移动端展示可读提示。
    if (error instanceof z.ZodError) {
      return res.status(400).json({ message: "请求参数不合法", issues: error.issues });
    }

    const message = error instanceof Error ? error.message : "未知错误";
    return res.status(500).json({ message });
  });

  return app;
}
