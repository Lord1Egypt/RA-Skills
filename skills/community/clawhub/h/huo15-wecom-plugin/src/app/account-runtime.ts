import type { OpenClawConfig, PluginRuntime } from "openclaw/plugin-sdk";
import { formatErrorMessage } from "openclaw/plugin-sdk/infra-runtime";
import type { ResolvedRuntimeAccount } from "../config/runtime-config.js";
import { WecomAuditLog } from "../observability/audit-log.js";
import { WecomStatusRegistry } from "../observability/status-registry.js";
import { summarizeTransportSessions } from "../observability/transport-session-view.js";
import { dispatchInboundEvent } from "../runtime/dispatcher.js";
import { WecomMediaService } from "../shared/media-service.js";
import { InMemoryRuntimeStore } from "../store/memory-store.js";
import type {
  AccountRuntimeStatusSnapshot,
  ReplyHandle,
  ReplyPayload,
  TransportSessionPatch,
  TransportSessionSnapshot,
  UnifiedInboundEvent,
  WecomAuditCategory,
  WecomRuntimeHealth,
  WecomTransportKind,
} from "../types/index.js";

export class WecomAccountRuntime {
  readonly store = new InMemoryRuntimeStore();
  readonly mediaService: WecomMediaService;
  readonly auditLog = new WecomAuditLog();
  readonly statusRegistry = new WecomStatusRegistry();
  private readonly runtimeStatus: AccountRuntimeStatusSnapshot;

  constructor(
    readonly core: PluginRuntime,
    readonly cfg: OpenClawConfig,
    readonly resolved: ResolvedRuntimeAccount,
    readonly log: {
      info?: (message: string) => void;
      warn?: (message: string) => void;
      error?: (message: string) => void;
    } = {},
    private readonly statusSink?: (snapshot: Record<string, unknown>) => void,
  ) {
    this.mediaService = new WecomMediaService(core, cfg);
    this.runtimeStatus = {
      accountId: resolved.account.accountId,
      health: "idle",
      ownerId: null,
      ownerDriftAt: null,
      lastError: null,
      lastErrorAt: null,
      lastInboundAt: null,
      lastOutboundAt: null,
      recentInboundSummary: null,
      recentOutboundSummary: null,
      recentIssueCategory: null,
      recentIssueSummary: null,
      transportSessions: [],
    };
  }

  get account() {
    return this.resolved.account;
  }

  async handleEvent(event: UnifiedInboundEvent, replyHandle: ReplyHandle): Promise<void> {
    const dispatchStartedAt = Date.now();
    this.runtimeStatus.lastInboundAt = Date.now();
    this.runtimeStatus.recentInboundSummary = `${event.transport} ${event.inboundKind} ${event.messageId}`;
    this.log.info?.(
      `[wecom-runtime] inbound account=${event.accountId} transport=${event.transport} kind=${event.inboundKind} messageId=${event.messageId} peer=${event.conversation.peerKind}:${event.conversation.peerId}`,
    );
    this.log.info?.(
      `[wecom-runtime] dispatch-start account=${event.accountId} transport=${event.transport} kind=${event.inboundKind} messageId=${event.messageId}`,
    );
    this.emitStatus();

    const trackedReplyHandle: ReplyHandle = {
      context: replyHandle.context,
      deliver: async (payload: ReplyPayload, info) => {
        const deliverStartedAt = Date.now();
        const textLen = payload.text?.trim().length ?? 0;
        const mediaCount = (payload.mediaUrls?.length ?? 0) + (payload.mediaUrl ? 1 : 0);
        this.log.info?.(
          `[wecom-runtime] deliver-start account=${event.accountId} transport=${replyHandle.context.transport} kind=${info.kind} messageId=${event.messageId} textLen=${textLen} mediaCount=${mediaCount} reasoning=${String(payload.isReasoning === true)}`,
        );
        await replyHandle.deliver(payload, info);
        this.runtimeStatus.lastOutboundAt = Date.now();
        const outboundSummary =
          payload.text?.trim() || payload.mediaUrl || payload.mediaUrls?.[0] || info.kind;
        this.runtimeStatus.recentOutboundSummary = `${replyHandle.context.transport} ${outboundSummary.slice(0, 120)}`;
        this.log.info?.(
          `[wecom-runtime] outbound account=${event.accountId} transport=${replyHandle.context.transport} kind=${info.kind} messageId=${event.messageId} summary=${JSON.stringify(this.runtimeStatus.recentOutboundSummary)}`,
        );
        this.log.info?.(
          `[wecom-runtime] deliver-done account=${event.accountId} transport=${replyHandle.context.transport} kind=${info.kind} messageId=${event.messageId} durationMs=${Date.now() - deliverStartedAt}`,
        );
        this.emitStatus();
      },
      fail: async (error: unknown) => {
        const formattedError = formatErrorMessage(error);
        this.recordOperationalIssue({
          transport: replyHandle.context.transport,
          category: "runtime-error",
          messageId: event.messageId,
          raw: replyHandle.context.raw,
          summary: `reply-fail ${formattedError}`,
          error: formattedError,
        });
        this.log.error?.(
          `[wecom-runtime] reply-fail account=${event.accountId} transport=${replyHandle.context.transport} messageId=${event.messageId} error=${formattedError}`,
        );
        await replyHandle.fail?.(error);
      },
      markExternalActivity: () => {
        replyHandle.markExternalActivity?.();
      },
    };

    try {
      await dispatchInboundEvent({
        core: this.core,
        cfg: this.cfg,
        store: this.store,
        auditLog: this.auditLog,
        mediaService: this.mediaService,
        event,
        replyHandle: trackedReplyHandle,
      });
      this.log.info?.(
        `[wecom-runtime] dispatch-done account=${event.accountId} transport=${event.transport} kind=${event.inboundKind} messageId=${event.messageId} durationMs=${Date.now() - dispatchStartedAt}`,
      );
    } catch (error) {
      this.log.error?.(
        `[wecom-runtime] dispatch-fail account=${event.accountId} transport=${event.transport} kind=${event.inboundKind} messageId=${event.messageId} durationMs=${Date.now() - dispatchStartedAt} error=${formatErrorMessage(error)}`,
      );
      throw error;
    }
  }

  updateTransportSession(snapshot: TransportSessionSnapshot): void {
    const previous = this.store.readTransportSession(snapshot.accountId, snapshot.transport);
    this.store.writeTransportSession(snapshot);
    this.statusRegistry.write(snapshot);
    this.log.info?.(
      `[wecom-runtime] session account=${snapshot.accountId} transport=${snapshot.transport} running=${snapshot.running} owner=${snapshot.ownerId ?? "none"} connected=${String(snapshot.connected ?? false)} authenticated=${String(snapshot.authenticated ?? false)} error=${snapshot.lastError ?? "none"}`,
    );
    if (
      previous?.ownerId &&
      snapshot.ownerId &&
      previous.ownerId !== snapshot.ownerId &&
      previous.running
    ) {
      this.recordOperationalIssue({
        transport: snapshot.transport,
        category: "owner-drift",
        summary: `owner drift ${previous.ownerId} -> ${snapshot.ownerId}`,
      });
    }
    if (snapshot.lastError) {
      this.runtimeStatus.lastError = snapshot.lastError;
      this.runtimeStatus.lastErrorAt = Date.now();
    } else if (snapshot.running) {
      this.runtimeStatus.lastError = null;
    }
    this.emitStatus();
  }

  touchTransportSession(transport: WecomTransportKind, patch: TransportSessionPatch): void {
    const current = this.store.readTransportSession(this.account.accountId, transport);
    const next: TransportSessionSnapshot = {
      accountId: this.account.accountId,
      transport,
      running: patch.running ?? current?.running ?? true,
      ownerId: patch.ownerId ?? current?.ownerId,
      connected: patch.connected ?? current?.connected,
      authenticated: patch.authenticated ?? current?.authenticated,
      lastConnectedAt: patch.lastConnectedAt ?? current?.lastConnectedAt,
      lastDisconnectedAt: patch.lastDisconnectedAt ?? current?.lastDisconnectedAt,
      lastInboundAt: patch.lastInboundAt ?? current?.lastInboundAt,
      lastOutboundAt: patch.lastOutboundAt ?? current?.lastOutboundAt,
      lastError: "lastError" in patch ? (patch.lastError ?? undefined) : current?.lastError,
    };
    this.updateTransportSession(next);
  }

  listTransportSessions() {
    return this.statusRegistry.read(this.account.accountId);
  }

  listAuditEntries() {
    return this.auditLog.list();
  }

  buildRuntimeStatus(): AccountRuntimeStatusSnapshot {
    const sessions = this.listTransportSessions();
    const primarySession = this.resolvePrimarySession(sessions);
    return {
      ...this.runtimeStatus,
      health: this.computeHealth(sessions),
      transport: primarySession?.transport,
      ownerId: primarySession?.ownerId ?? this.runtimeStatus.ownerId ?? null,
      connected: primarySession?.connected,
      authenticated: primarySession?.authenticated,
      lastError:
        primarySession?.lastError ??
        (primarySession?.running ? null : (this.runtimeStatus.lastError ?? null)),
      transportSessions: summarizeTransportSessions(sessions),
    };
  }

  recordOperationalIssue(params: {
    transport: WecomTransportKind;
    category: WecomAuditCategory;
    summary: string;
    messageId?: string;
    raw?: ReplyHandle["context"]["raw"];
    error?: string;
  }): void {
    this.auditLog.appendOperational({
      accountId: this.account.accountId,
      transport: params.transport,
      category: params.category,
      messageId: params.messageId,
      summary: params.summary,
      raw: params.raw,
      error: params.error,
    });
    if (params.category === "owner-drift" || params.category === "ws-kicked") {
      this.runtimeStatus.ownerDriftAt = Date.now();
    }
    this.runtimeStatus.lastError = params.error ?? params.summary;
    this.runtimeStatus.lastErrorAt = Date.now();
    this.runtimeStatus.recentIssueCategory = params.category;
    this.runtimeStatus.recentIssueSummary = params.summary;
    const sink =
      params.category === "runtime-error" || params.category === "fallback-delivery-failed"
        ? this.log.error
        : this.log.warn;
    sink?.(
      `[wecom-runtime] issue account=${this.account.accountId} transport=${params.transport} category=${params.category} messageId=${params.messageId ?? "n/a"} summary=${params.summary}`,
    );
    this.emitStatus();
  }

  private emitStatus(): void {
    this.statusSink?.(this.buildRuntimeStatus() as unknown as Record<string, unknown>);
  }

  private resolvePrimarySession(
    sessions: TransportSessionSnapshot[],
  ): TransportSessionSnapshot | undefined {
    const primaryTransport = this.account.bot?.configured
      ? this.account.bot.primaryTransport === "ws"
        ? "bot-ws"
        : "bot-webhook"
      : this.account.agent?.callbackConfigured
        ? "agent-callback"
        : undefined;
    if (!primaryTransport) {
      return sessions[0];
    }
    return sessions.find((session) => session.transport === primaryTransport) ?? sessions[0];
  }

  private computeHealth(sessions: TransportSessionSnapshot[]): WecomRuntimeHealth {
    if (sessions.length === 0) {
      return this.runtimeStatus.lastError ? "down" : "idle";
    }
    const hasRunning = sessions.some((session) => session.running);
    const hasError = sessions.some((session) => Boolean(session.lastError));
    if (hasRunning && !hasError) {
      return "healthy";
    }
    if (hasRunning) {
      return "degraded";
    }
    return hasError ? "down" : "idle";
  }
}
