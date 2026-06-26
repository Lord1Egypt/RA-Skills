import type { FastifyInstance } from "fastify";
import { z } from "zod";
import type { BridgeConfig } from "../config/schema";
import { assertAuthenticated } from "../security/auth";
import type { MailQueryAdapter } from "../adapters/mail/types";
import { JobCoordinator } from "../services/coordinator";
import { SQLiteStore } from "../state/sqlite";

const incomingEventSchema = z.object({
  eventId: z.string().min(1),
  source: z.string().min(1),
  sidecarId: z.string().min(1),
  platform: z.string().min(1),
  chatType: z.enum(["group", "private"]),
  chatId: z.string().min(1),
  chatName: z.string().min(1),
  senderDisplayName: z.string().optional(),
  messageId: z.string().optional().default(""),
  messageText: z.string().min(1),
  messageTime: z.string().min(1),
  observedAt: z.string().min(1)
});

const sidecarHeartbeatSchema = z.object({
  sidecarId: z.string().min(1),
  adapterName: z.string().min(1),
  adapterOk: z.boolean(),
  detail: z.string().optional(),
  groups: z.array(z.unknown()).optional()
});

const claimSchema = z.object({
  sidecarId: z.string().min(1),
  limit: z.number().int().min(1).max(100).optional()
});

const ackSchema = z.object({
  sidecarId: z.string().min(1),
  status: z.enum(["sent", "failed"]),
  errorCode: z.string().optional(),
  errorMessage: z.string().optional()
});

const toolQuerySchema = z.object({
  email: z.string().email(),
  mode: z.enum(["findLatest", "waitForNew"]).default("findLatest"),
  timeoutSec: z.number().int().min(5).max(3600).optional(),
  replyTarget: z
    .object({
      chatId: z.string().min(1),
      chatName: z.string().optional(),
      replyToMessageId: z.string().optional()
    })
    .optional()
});

const listWatchSchema = z.object({
  limit: z.number().int().min(1).max(500).optional()
});

const flushCommandsSchema = z.object({
  reason: z.string().min(1).max(200).optional()
});

const closeWatchSchema = z.object({
  jobId: z.string().min(1)
});

const monitoringStateSchema = z.object({
  paused: z.boolean()
});

const rerunLastSchema = z.object({
  email: z.string().email(),
  replyTarget: z
    .object({
      chatId: z.string().min(1),
      chatName: z.string().optional(),
      replyToMessageId: z.string().optional()
    })
    .optional()
});

const listReceiptsSchema = z.object({
  limit: z.number().int().min(1).max(500).optional()
});

const listSidecarsSchema = z.object({
  limit: z.number().int().min(1).max(500).optional()
});

const listJobsSchema = z.object({
  limit: z.number().int().min(1).max(500).optional(),
  status: z.string().min(1).optional()
});
const listCommandsSchema = z.object({
  limit: z.number().int().min(1).max(500).optional(),
  status: z.string().min(1).optional()
});
const emptyBodySchema = z.object({}).passthrough();

const setBindingSchema = z.object({
  alias: z.string().min(1),
  chatId: z.string().min(1),
  chatName: z.string().optional()
});

const deleteBindingSchema = z.object({
  alias: z.string().min(1)
});

const resolveBindingSchema = z.object({
  target: z.string().min(1)
});

const listBindingsSchema = z.object({
  limit: z.number().int().min(1).max(500).optional()
});

interface RegisterRoutesDependencies {
  config: BridgeConfig;
  store: SQLiteStore;
  coordinator: JobCoordinator;
  mailAdapter: MailQueryAdapter;
}

function sendBadRequest(reply: { code: (value: number) => { send: (body: unknown) => unknown } }, error: unknown) {
  const message = error instanceof Error ? error.message : "bad_request";
  return reply.code(400).send({ ok: false, error: message });
}

function sendUnauthorized(
  reply: { code: (value: number) => { send: (body: unknown) => unknown } },
  error: unknown
) {
  const message = error instanceof Error ? error.message : "unauthorized";
  return reply.code(401).send({ ok: false, error: message });
}

export async function registerRoutes(app: FastifyInstance, deps: RegisterRoutesDependencies): Promise<void> {
  app.get("/health", async () => {
    const mailHealth = await deps.mailAdapter.health();
    const state = deps.store.getHealthSnapshot();
    return {
      ok: true,
      time: new Date().toISOString(),
      mailAdapter: mailHealth,
      state
    };
  });

  app.get("/api/v1/admin/health/detail", async (request, reply) => {
    try {
      assertAuthenticated(request.headers, deps.config.bridge.sharedSecret, deps.config.bridge.authWindowSec);
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    const mailHealth = await deps.mailAdapter.health();
    const state = deps.store.getHealthSnapshot();
    const sidecars = deps.coordinator.listSidecarHeartbeats(20);
    const jobStatusCounts = deps.coordinator.getJobStatusCounts();
    return {
      ok: true,
      time: new Date().toISOString(),
      mailAdapter: mailHealth,
      state,
      sidecars,
      jobStatusCounts
    };
  });

  app.post("/api/v1/sidecar/events", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = incomingEventSchema.parse(request.body);
      const result = await deps.coordinator.ingestEvent(body);
      return { ok: true, result };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/sidecar/heartbeat", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = sidecarHeartbeatSchema.parse(request.body);
      deps.coordinator.ingestSidecarHeartbeat(body);
      return { ok: true };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/sidecar/commands/claim", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = claimSchema.parse(request.body);
      const commands = deps.coordinator.claimCommands(body.sidecarId, body.limit ?? 10);
      return { ok: true, commands };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/sidecar/commands/:commandId/ack", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const params = z.object({ commandId: z.string().min(1) }).parse(request.params);
      const body = ackSchema.parse(request.body);
      const ok = deps.coordinator.ackCommand(
        params.commandId,
        body.sidecarId,
        body.status,
        body.errorCode,
        body.errorMessage
      );
      if (!ok) {
        return reply.code(404).send({ ok: false, error: "command_not_found_or_not_claimed" });
      }
      return { ok: true };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/bhmailer/webhook", async (request, reply) => {
    const webhookSecret = deps.config.mail.webhookSecret ?? deps.config.bridge.sharedSecret;
    try {
      assertAuthenticated(request.headers, webhookSecret, deps.config.bridge.authWindowSec, request.body);
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const outcome = await deps.coordinator.ingestWebhook(request.body);
      if (!outcome.accepted) {
        return reply.code(202).send({ ok: true, accepted: false, reason: outcome.reason });
      }
      return {
        ok: true,
        accepted: true,
        commandId: outcome.commandId,
        commandIds: outcome.commandIds
      };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/watch/sweep", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const swept = await deps.coordinator.sweepExpiredWatches();
      return { ok: true, swept };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/watch/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listWatchSchema.parse(request.body ?? {});
      const watches = deps.coordinator.listActiveWatches(body.limit ?? 100);
      return { ok: true, watches };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/commands/flush", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = flushCommandsSchema.parse(request.body ?? {});
      const flushed = deps.coordinator.flushPendingCommands(body.reason);
      return { ok: true, flushed };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/watch/close", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = closeWatchSchema.parse(request.body ?? {});
      const closed = deps.coordinator.closeWatch(body.jobId);
      if (!closed) {
        return reply.code(404).send({ ok: false, error: "watch_not_found_or_not_active" });
      }
      return { ok: true, closed: true };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/maintenance/run", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const result = await deps.coordinator.runMaintenance();
      return { ok: true, result };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/monitoring/set", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = monitoringStateSchema.parse(request.body ?? {});
      deps.coordinator.setMonitoringPaused(body.paused);
      return { ok: true, paused: deps.coordinator.isMonitoringPaused() };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.get("/api/v1/admin/monitoring/status", async (request, reply) => {
    try {
      assertAuthenticated(request.headers, deps.config.bridge.sharedSecret, deps.config.bridge.authWindowSec);
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    return { ok: true, paused: deps.coordinator.isMonitoringPaused() };
  });

  app.post("/api/v1/admin/query/rerun-last", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = rerunLastSchema.parse(request.body ?? {});
      const resolvedTarget = body.replyTarget?.chatId
        ? deps.coordinator.resolveGroupTarget(body.replyTarget.chatId)
        : undefined;
      const outcome = await deps.coordinator.rerunLastQuery(
        body.email,
        body.replyTarget
          ? {
              chatId: resolvedTarget?.chatId ?? body.replyTarget.chatId,
              chatName: body.replyTarget.chatName ?? resolvedTarget?.chatName,
              replyToMessageId: body.replyTarget.replyToMessageId
            }
          : undefined
      );
      if (!outcome.ok) {
        return reply.code(404).send({ ok: false, error: outcome.reason });
      }
      return { ok: true, outcome };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/receipts/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listReceiptsSchema.parse(request.body ?? {});
      const receipts = deps.coordinator.listRecentReceipts(body.limit ?? 100);
      return { ok: true, receipts };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/sidecars/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listSidecarsSchema.parse(request.body ?? {});
      const sidecars = deps.coordinator.listSidecarHeartbeats(body.limit ?? 100);
      return { ok: true, sidecars };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/jobs/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listJobsSchema.parse(request.body ?? {});
      const jobs = deps.coordinator.listJobs(body.limit ?? 100, body.status);
      return { ok: true, jobs };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/jobs/status-counts", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      emptyBodySchema.parse(request.body ?? {});
      const counts = deps.coordinator.getJobStatusCounts();
      return { ok: true, counts };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/commands/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listCommandsSchema.parse(request.body ?? {});
      const commands = deps.coordinator.listCommands(body.limit ?? 100, body.status);
      return { ok: true, commands };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/bindings/list", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = listBindingsSchema.parse(request.body ?? {});
      const bindings = deps.coordinator.listGroupBindings(body.limit ?? 100);
      return { ok: true, bindings };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/bindings/set", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = setBindingSchema.parse(request.body ?? {});
      deps.coordinator.setGroupBinding(body.alias, body.chatId, body.chatName);
      return { ok: true };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/bindings/delete", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = deleteBindingSchema.parse(request.body ?? {});
      const deleted = deps.coordinator.deleteGroupBinding(body.alias);
      if (!deleted) {
        return reply.code(404).send({ ok: false, error: "binding_not_found" });
      }
      return { ok: true };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/admin/bindings/resolve", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = resolveBindingSchema.parse(request.body ?? {});
      const resolved = deps.coordinator.resolveGroupTarget(body.target);
      return { ok: true, resolved };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });

  app.post("/api/v1/tools/wechat_mail_bridge_query", async (request, reply) => {
    try {
      assertAuthenticated(
        request.headers,
        deps.config.bridge.sharedSecret,
        deps.config.bridge.authWindowSec,
        request.body
      );
    } catch (error) {
      return sendUnauthorized(reply, error);
    }

    try {
      const body = toolQuerySchema.parse(request.body);
      const now = new Date().toISOString();
      const eventId = `evt_tool_${Date.now()}`;
      const messageId = `tool_msg_${Date.now()}`;
      const modePrefix = body.mode === "waitForNew" ? "/watch" : "/mail";
      const suffix = body.mode === "waitForNew" ? ` ${body.timeoutSec ?? deps.config.wechat.defaultWaitTimeoutSec}` : "";
      const text = `${modePrefix} ${body.email}${suffix}`;
      const resolvedTarget = body.replyTarget?.chatId
        ? deps.coordinator.resolveGroupTarget(body.replyTarget.chatId)
        : { chatId: "manual-tool-chat", chatName: "Manual Tool" };
      const result = await deps.coordinator.ingestEvent({
        eventId,
        source: "manual-tool",
        sidecarId: "manual-tool",
        platform: "tool",
        chatType: "group",
        chatId: resolvedTarget.chatId,
        chatName: body.replyTarget?.chatName ?? resolvedTarget.chatName ?? "Manual Tool",
        messageId: body.replyTarget?.replyToMessageId ?? messageId,
        messageText: text,
        messageTime: now,
        observedAt: now
      });
      return { ok: true, result };
    } catch (error) {
      return sendBadRequest(reply, error);
    }
  });
}
