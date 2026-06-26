import crypto from "node:crypto";
import type { BridgeConfig } from "../config/schema";
import { formatClarificationMessage, formatMailReply } from "../formatters/reply";
import { extractEmails } from "../parsers/email";
import { parseTrigger } from "../parsers/trigger";
import type { MailQueryAdapter } from "../adapters/mail/types";
import { SQLiteStore } from "../state/sqlite";
import type {
  IngestDecision,
  IncomingChatMessageEvent,
  MailFindResult,
  MailWebhookEvent,
  OutboundWeChatSendCommand
} from "../types/contracts";

function prefixedId(prefix: string): string {
  return `${prefix}_${crypto.randomUUID().replace(/-/g, "")}`;
}

function nowIso(): string {
  return new Date().toISOString();
}

function plusSecondsIso(seconds: number): string {
  return new Date(Date.now() + seconds * 1000).toISOString();
}

function isAdminCommand(text: string): boolean {
  const normalized = text.trim().toLowerCase();
  return (
    normalized === "/mail-health" ||
    normalized === "邮箱桥状态" ||
    normalized === "/mail-bind list" ||
    normalized.startsWith("/mail-bind set ") ||
    normalized.startsWith("/mail-bind del ") ||
    normalized.startsWith("/mail-bind get ") ||
    normalized === "/mail-pause" ||
    normalized === "/mail-resume" ||
    normalized === "/mail-flush" ||
    normalized.startsWith("/mail-last ")
  );
}

export class JobCoordinator {
  constructor(
    private readonly store: SQLiteStore,
    private readonly config: BridgeConfig,
    private readonly mailAdapter: MailQueryAdapter
  ) {}

  async ingestEvent(event: IncomingChatMessageEvent): Promise<IngestDecision> {
    const normalizedMessageId =
      event.messageId && event.messageId.trim().length > 0
        ? event.messageId
        : this.synthesizeMessageId(event);
    const normalizedEvent = {
      ...event,
      messageId: normalizedMessageId
    };

    const dedupeKey = `${normalizedEvent.sidecarId}:${normalizedEvent.messageId}`;
    const accepted = this.store.addInboundDedupeKey(dedupeKey);
    if (!accepted) {
      return { status: "duplicate" };
    }

    this.store.saveIncomingEvent(
      this.config.privacy.storeRawWechatText
        ? normalizedEvent
        : {
            ...normalizedEvent,
            messageText: "[redacted]"
          }
    );

    if (!this.isGroupAllowed(normalizedEvent.chatId, normalizedEvent.chatName)) {
      return { status: "ignored", reason: "group_not_allowlisted" };
    }

    const incomingText = normalizedEvent.messageText.trim();
    if (isAdminCommand(incomingText)) {
      return this.handleAdminCommand(normalizedEvent);
    }

    if (this.store.isMonitoringPaused()) {
      return { status: "ignored", reason: "monitoring_paused" };
    }

    const decision = parseTrigger(normalizedEvent.messageText, {
      triggerPrefixes: this.config.wechat.triggerPrefixes,
      passiveSingleEmailMode: this.config.wechat.passiveSingleEmailMode,
      defaultWaitTimeoutSec: this.config.wechat.defaultWaitTimeoutSec
    });

    if (decision.kind === "ignore") {
      return { status: "ignored", reason: decision.reason };
    }

    if (decision.kind === "clarify") {
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: normalizedEvent.messageId,
        text: formatClarificationMessage(decision)
      });
      return { status: "queued", commandId };
    }

    const jobId = prefixedId("job");
    const baseCreated = nowIso();
    this.store.createJob({
      jobId,
      sourceEventId: event.eventId,
      chatId: normalizedEvent.chatId,
      chatName: normalizedEvent.chatName,
      replyToMessageId: normalizedEvent.messageId,
      email: decision.email,
      mode: decision.kind === "waitForNew" ? "waitForNew" : "findLatest",
      status: "CREATED",
      createdAt: baseCreated,
      updatedAt: baseCreated,
      expiresAt:
        decision.kind === "waitForNew"
          ? plusSecondsIso(decision.timeoutSec)
          : plusSecondsIso(this.config.wechat.defaultWaitTimeoutSec)
    });

    this.store.updateJobStatus(jobId, "PARSED");

    if (
      decision.kind === "waitForNew" &&
      (this.config.mail.queryMode === "push-webhook" || this.config.mail.preferPushWebhook)
    ) {
      this.store.updateJobStatus(jobId, "WAITING_NEW_MAIL");
      this.store.createWatchSubscription({
        jobId,
        email: decision.email,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        expiresAt: plusSecondsIso(decision.timeoutSec),
        status: "active",
        createdAt: baseCreated,
        updatedAt: baseCreated
      });

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: normalizedEvent.messageId,
        text: `已开始监控 ${decision.email}，等待 ${decision.timeoutSec} 秒内的新邮件。`
      });
      this.store.updateJobStatus(jobId, "REPLY_QUEUED");
      return { status: "queued", jobId, commandId };
    }

    try {
      let result: MailFindResult;
      if (decision.kind === "findLatest") {
        this.store.updateJobStatus(jobId, "QUERYING_HISTORY");
        result = await this.mailAdapter.findLatest({
          email: decision.email,
          mode: "findLatest",
          sourceEventId: event.eventId
        });
      } else {
        this.store.updateJobStatus(jobId, "WAITING_NEW_MAIL");
        result = await this.mailAdapter.waitForNew({
          email: decision.email,
          mode: "waitForNew",
          timeoutSec: decision.timeoutSec,
          sourceEventId: event.eventId
        });
      }

      if (result.found) {
        this.store.updateJobStatus(jobId, "MATCHED");
      } else if (result.reason === "timeout") {
        this.store.updateJobStatus(jobId, "TIMEOUT");
      } else {
        this.store.updateJobStatus(jobId, "NOT_FOUND");
      }

      if (!this.config.privacy.storeRawMailBody) {
        result = {
          ...result,
          bodyPreview: undefined
        };
      }

      const reply = formatMailReply(decision.email, result, {
        maxBodyPreviewChars: this.config.reply.maxBodyPreviewChars,
        includeSubject: this.config.reply.includeSubject,
        includeFrom: this.config.reply.includeFrom,
        includeReceivedAt: this.config.reply.includeReceivedAt
      });

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId,
        chatId: normalizedEvent.chatId,
        chatName: normalizedEvent.chatName,
        replyToMessageId: normalizedEvent.messageId,
        text: reply
      });
      this.store.updateJobStatus(jobId, "REPLY_QUEUED");

      return { status: "queued", jobId, commandId };
    } catch (error) {
      const message = error instanceof Error ? error.message : "mail_query_failed";
      this.store.updateJobStatus(jobId, "REPLY_FAILED", message);

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId,
        chatId: normalizedEvent.chatId,
        chatName: normalizedEvent.chatName,
        replyToMessageId: normalizedEvent.messageId,
        text: `查询失败：${message}`
      });
      return { status: "queued", jobId, commandId };
    }
  }

  async ingestWebhook(payload: unknown): Promise<{
    accepted: boolean;
    reason?: string;
    commandId?: string;
    commandIds?: string[];
    normalized?: MailWebhookEvent;
  }> {
    const normalized = await this.mailAdapter.normalizeWebhook(payload);
    const directTarget =
      normalized.targetChatId && normalized.targetChatId.trim().length > 0
        ? { chatId: normalized.targetChatId, chatName: normalized.targetChatName }
        : normalized.targetChatName && normalized.targetChatName.trim().length > 0
          ? this.store.resolveGroupBinding(normalized.targetChatName.trim())
          : null;
    const mailDedupeKey = this.getWebhookDedupeKey(normalized);
    if (!this.store.addWebhookDedupeKey(mailDedupeKey)) {
      return {
        accepted: false,
        reason: "duplicate_webhook",
        normalized
      };
    }

    const result: MailFindResult = {
      found: true,
      mode: "waitForNew",
      matchedEmail: normalized.matchedEmail,
      subject: normalized.subject,
      from: normalized.from,
      receivedAt: normalized.receivedAt,
      bodyPreview: normalized.bodyPreview,
      extractedFields: normalized.extractedFields,
      rawProvider: normalized.rawProvider
    };

    const normalizedResult = this.config.privacy.storeRawMailBody
      ? result
      : {
          ...result,
          bodyPreview: undefined
        };

    if (!directTarget) {
      const watches = this.store.listActiveWatchSubscriptionsByEmail(normalized.matchedEmail);
      if (watches.length === 0) {
        return {
          accepted: false,
          reason: "missing_target_chat_and_no_watch_subscription",
          normalized
        };
      }

      const commandIds: string[] = [];
      for (const watch of watches) {
        const reply = formatMailReply(normalized.matchedEmail, normalizedResult, {
          maxBodyPreviewChars: this.config.reply.maxBodyPreviewChars,
          includeSubject: this.config.reply.includeSubject,
          includeFrom: this.config.reply.includeFrom,
          includeReceivedAt: this.config.reply.includeReceivedAt
        });

        this.store.updateJobStatus(watch.jobId, "MATCHED");
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          jobId: watch.jobId,
          chatId: watch.chatId,
          chatName: watch.chatName,
          replyToMessageId: watch.replyToMessageId,
          text: reply
        });
        this.store.updateJobStatus(watch.jobId, "REPLY_QUEUED");
        this.store.markWatchSubscriptionStatus(watch.jobId, "matched", mailDedupeKey);
        commandIds.push(commandId);
      }

      return {
        accepted: true,
        commandIds,
        normalized
      };
    } else {
      const reply = formatMailReply(normalized.matchedEmail, normalizedResult, {
          maxBodyPreviewChars: this.config.reply.maxBodyPreviewChars,
          includeSubject: this.config.reply.includeSubject,
          includeFrom: this.config.reply.includeFrom,
          includeReceivedAt: this.config.reply.includeReceivedAt
        });

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: directTarget.chatId,
        chatName: directTarget.chatName,
        replyToMessageId: normalized.replyToMessageId,
        text: reply
      });

      return {
        accepted: true,
        commandId,
        normalized
      };
    }
  }

  async sweepExpiredWatches(): Promise<number> {
    const expired = this.store.sweepExpiredWatchSubscriptions();
    if (expired.length === 0) {
      return 0;
    }

    for (const watch of expired) {
      this.store.updateJobStatus(watch.jobId, "TIMEOUT");
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId: watch.jobId,
        chatId: watch.chatId,
        chatName: watch.chatName,
        replyToMessageId: watch.replyToMessageId,
        text: `监控超时，邮箱 ${watch.email} 在等待窗口内没有匹配的新邮件。`
      });
      this.store.updateJobStatus(watch.jobId, "REPLY_QUEUED");
    }

    return expired.length;
  }

  async runMaintenance(): Promise<{
    sweptWatches: number;
    requeuedClaims: number;
    inboundDedupePruned: number;
    webhookDedupePruned: number;
    jobsDeleted: number;
    inboundEventsDeleted: number;
    receiptsDeleted: number;
    commandsDeleted: number;
    heartbeatsDeleted: number;
  }> {
    const sweptWatches = await this.sweepExpiredWatches();
    const now = Date.now();
    const staleBeforeIso = new Date(now - this.config.bridge.staleClaimSec * 1000).toISOString();
    const dedupeBeforeIso = new Date(
      now - this.config.bridge.dedupeRetentionHours * 60 * 60 * 1000
    ).toISOString();
    const operationalBeforeIso = new Date(
      now - this.config.bridge.jobRetentionHours * 60 * 60 * 1000
    ).toISOString();

    const requeuedClaims = this.store.requeueStaleClaimedCommands(staleBeforeIso);
    const dedupePruned = this.store.pruneDedupeOlderThan(dedupeBeforeIso);
    const operationalPruned = this.store.pruneOperationalData(operationalBeforeIso);

    return {
      sweptWatches,
      requeuedClaims,
      inboundDedupePruned: dedupePruned.inboundDeleted,
      webhookDedupePruned: dedupePruned.webhookDeleted,
      jobsDeleted: operationalPruned.jobsDeleted,
      inboundEventsDeleted: operationalPruned.inboundEventsDeleted,
      receiptsDeleted: operationalPruned.receiptsDeleted,
      commandsDeleted: operationalPruned.commandsDeleted,
      heartbeatsDeleted: operationalPruned.heartbeatsDeleted
    };
  }

  claimCommands(sidecarId: string, limit: number): OutboundWeChatSendCommand[] {
    return this.store.claimCommands(sidecarId, limit);
  }

  ackCommand(
    commandId: string,
    sidecarId: string,
    status: "sent" | "failed",
    errorCode?: string,
    errorMessage?: string
  ): boolean {
    return this.store.ackCommand(commandId, sidecarId, status, errorCode, errorMessage);
  }

  listActiveWatches(limit = 100) {
    return this.store.listActiveWatchSubscriptions(limit);
  }

  closeWatch(jobId: string): boolean {
    const closed = this.store.closeWatchSubscription(jobId);
    if (closed) {
      this.store.updateJobStatus(jobId, "COMPLETED", "watch_closed_by_operator");
    }
    return closed;
  }

  isMonitoringPaused(): boolean {
    return this.store.isMonitoringPaused();
  }

  setMonitoringPaused(paused: boolean): void {
    this.store.setMonitoringPaused(paused);
  }

  async rerunLastQuery(
    email: string,
    replyTarget?: { chatId: string; chatName?: string; replyToMessageId?: string }
  ): Promise<{ ok: boolean; reason?: string; jobId?: string; commandId?: string }> {
    const base = this.store.getLatestJobByEmail(email);
    if (!base && !replyTarget) {
      return { ok: false, reason: "no_previous_job_for_email" };
    }

    const target = {
      chatId: replyTarget?.chatId ?? base!.chatId,
      chatName: replyTarget?.chatName ?? base?.chatName ?? "Manual Rerun",
      replyToMessageId: replyTarget?.replyToMessageId ?? base?.replyToMessageId
    };

    const jobId = prefixedId("job");
    const createdAt = nowIso();
    this.store.createJob({
      jobId,
      sourceEventId: prefixedId("evt_rerun"),
      chatId: target.chatId,
      chatName: target.chatName,
      replyToMessageId: target.replyToMessageId,
      email,
      mode: "findLatest",
      status: "CREATED",
      createdAt,
      updatedAt: createdAt,
      expiresAt: plusSecondsIso(this.config.wechat.defaultWaitTimeoutSec)
    });
    this.store.updateJobStatus(jobId, "QUERYING_HISTORY");

    try {
      let result = await this.mailAdapter.findLatest({
        email,
        mode: "findLatest",
        sourceEventId: prefixedId("evt_rerun_source")
      });
      if (!this.config.privacy.storeRawMailBody) {
        result = {
          ...result,
          bodyPreview: undefined
        };
      }

      if (result.found) {
        this.store.updateJobStatus(jobId, "MATCHED");
      } else {
        this.store.updateJobStatus(jobId, "NOT_FOUND");
      }

      const reply = formatMailReply(email, result, {
        maxBodyPreviewChars: this.config.reply.maxBodyPreviewChars,
        includeSubject: this.config.reply.includeSubject,
        includeFrom: this.config.reply.includeFrom,
        includeReceivedAt: this.config.reply.includeReceivedAt
      });

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId,
        chatId: target.chatId,
        chatName: target.chatName,
        replyToMessageId: target.replyToMessageId,
        text: reply
      });
      this.store.updateJobStatus(jobId, "REPLY_QUEUED");
      return { ok: true, jobId, commandId };
    } catch (error) {
      const message = error instanceof Error ? error.message : "rerun_failed";
      this.store.updateJobStatus(jobId, "REPLY_FAILED", message);
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        jobId,
        chatId: target.chatId,
        chatName: target.chatName,
        replyToMessageId: target.replyToMessageId,
        text: `查询失败：${message}`
      });
      return { ok: true, jobId, commandId };
    }
  }

  flushPendingCommands(reason?: string): number {
    return this.store.flushPendingCommands(reason);
  }

  listRecentReceipts(limit = 100) {
    return this.store.listRecentReceipts(limit);
  }

  ingestSidecarHeartbeat(input: {
    sidecarId: string;
    adapterName: string;
    adapterOk: boolean;
    detail?: string;
    groups?: unknown[];
  }): void {
    this.store.upsertSidecarHeartbeat({
      sidecarId: input.sidecarId,
      adapterName: input.adapterName,
      adapterOk: input.adapterOk,
      detail: input.detail,
      groupsJson: JSON.stringify(input.groups ?? []),
      lastSeenAt: nowIso()
    });
  }

  listSidecarHeartbeats(limit = 100) {
    const staleBefore = new Date(Date.now() - this.config.bridge.sidecarStaleSec * 1000).toISOString();
    return this.store.listSidecarHeartbeats(limit).map((item) => ({
      ...item,
      stale: item.lastSeenAt < staleBefore
    }));
  }

  listJobs(limit = 100, status?: string) {
    return this.store.listJobs(limit, status);
  }

  getJobStatusCounts() {
    return this.store.getJobStatusCounts();
  }

  listCommands(limit = 100, status?: string) {
    return this.store.listCommands(limit, status);
  }

  setGroupBinding(alias: string, chatId: string, chatName?: string): void {
    this.store.upsertGroupBinding(alias, chatId, chatName);
  }

  listGroupBindings(limit = 100) {
    return this.store.listGroupBindings(limit);
  }

  deleteGroupBinding(alias: string): boolean {
    return this.store.deleteGroupBinding(alias);
  }

  getGroupBinding(alias: string) {
    return this.store.getGroupBinding(alias);
  }

  resolveGroupTarget(aliasOrChatId: string): { chatId: string; chatName?: string } {
    return this.store.resolveGroupBinding(aliasOrChatId);
  }

  private isGroupAllowed(chatId: string, chatName: string): boolean {
    if (this.config.wechat.allowGroups.length === 0) {
      return true;
    }
    return this.config.wechat.allowGroups.includes(chatId) || this.config.wechat.allowGroups.includes(chatName);
  }

  private getWebhookDedupeKey(event: MailWebhookEvent): string {
    const keyPart = event.extractedFields?.code ?? event.receivedAt ?? event.subject ?? event.bodyPreview ?? "";
    return `${event.rawProvider}:${event.matchedEmail}:${keyPart}`;
  }

  private synthesizeMessageId(event: IncomingChatMessageEvent): string {
    const coarseTs = event.messageTime ? String(event.messageTime).slice(0, 16) : "";
    const base = `${event.sidecarId}|${event.chatId}|${event.senderDisplayName ?? ""}|${coarseTs}|${event.messageText}`;
    const hash = crypto.createHash("sha256").update(base).digest("hex").slice(0, 20);
    return `synthetic_${hash}`;
  }

  private async handleAdminCommand(event: IncomingChatMessageEvent): Promise<IngestDecision> {
    const normalized = event.messageText.trim().toLowerCase();

    if (normalized === "/mail-health" || normalized === "邮箱桥状态") {
      const mailHealth = await this.mailAdapter.health();
      const state = this.store.getHealthSnapshot();
      const lines: string[] = [];
      lines.push("邮箱桥状态");
      lines.push(`mailAdapter: ${mailHealth.name}`);
      lines.push(`mailOk: ${mailHealth.ok ? "yes" : "no"}`);
      if (mailHealth.detail) {
        lines.push(`mailDetail: ${mailHealth.detail}`);
      }
      lines.push(`queued: ${state.queuedCommands}`);
      lines.push(`claimed: ${state.claimedCommands}`);
      lines.push(`activeJobs: ${state.activeJobs}`);
      lines.push(`activeWatches: ${state.activeWatchSubscriptions}`);
      lines.push(`monitoringPaused: ${state.monitoringPaused ? "yes" : "no"}`);
      lines.push(`sidecars: ${state.sidecarHeartbeatCount}`);

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: lines.join("\n")
      });
      return { status: "queued", commandId };
    }

    if (normalized === "/mail-bind list") {
      const bindings = this.store.listGroupBindings(50);
      const lines: string[] = [];
      lines.push("当前群绑定");
      if (bindings.length === 0) {
        lines.push("（空）");
      } else {
        for (const binding of bindings) {
          lines.push(`${binding.alias} => ${binding.chatId}${binding.chatName ? ` (${binding.chatName})` : ""}`);
        }
      }

      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: lines.join("\n")
      });
      return { status: "queued", commandId };
    }

    if (normalized.startsWith("/mail-bind set ")) {
      const parts = event.messageText.trim().split(/\s+/).filter((item) => item.length > 0);
      const alias = parts[2] ?? "";
      const targetRef = parts.length > 3 ? parts.slice(3).join(" ").trim() : "";
      if (!alias) {
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          chatId: event.chatId,
          chatName: event.chatName,
          replyToMessageId: event.messageId,
          text: "用法：/mail-bind set <别名>"
        });
        return { status: "queued", commandId };
      }

      if (!targetRef) {
        this.store.upsertGroupBinding(alias, event.chatId, event.chatName);
      } else {
        const resolved = this.store.resolveGroupBinding(targetRef);
        this.store.upsertGroupBinding(alias, resolved.chatId, resolved.chatName ?? targetRef);
      }

      const commandId = prefixedId("cmd");
      const finalBinding = this.store.getGroupBinding(alias);
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: `已绑定：${alias} => ${finalBinding?.chatId ?? event.chatId}`
      });
      return { status: "queued", commandId };
    }

    if (normalized.startsWith("/mail-bind del ")) {
      const parts = event.messageText.trim().split(/\s+/).filter((item) => item.length > 0);
      const alias = parts[2] ?? "";
      if (!alias) {
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          chatId: event.chatId,
          chatName: event.chatName,
          replyToMessageId: event.messageId,
          text: "用法：/mail-bind del <别名>"
        });
        return { status: "queued", commandId };
      }

      const deleted = this.store.deleteGroupBinding(alias);
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: deleted ? `已删除绑定：${alias}` : `未找到绑定：${alias}`
      });
      return { status: "queued", commandId };
    }

    if (normalized.startsWith("/mail-bind get ")) {
      const parts = event.messageText.trim().split(/\s+/).filter((item) => item.length > 0);
      const alias = parts[2] ?? "";
      if (!alias) {
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          chatId: event.chatId,
          chatName: event.chatName,
          replyToMessageId: event.messageId,
          text: "用法：/mail-bind get <别名>"
        });
        return { status: "queued", commandId };
      }
      const binding = this.store.getGroupBinding(alias);
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: binding
          ? `${binding.alias} => ${binding.chatId}${binding.chatName ? ` (${binding.chatName})` : ""}`
          : `未找到绑定：${alias}`
      });
      return { status: "queued", commandId };
    }

    if (normalized === "/mail-pause") {
      this.store.setMonitoringPaused(true);
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: "已暂停自动处理新消息。"
      });
      return { status: "queued", commandId };
    }

    if (normalized === "/mail-resume") {
      this.store.setMonitoringPaused(false);
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: "已恢复自动处理新消息。"
      });
      return { status: "queued", commandId };
    }

    if (normalized === "/mail-flush") {
      const flushed = this.store.flushPendingCommands("flushed_by_chat_command");
      const commandId = prefixedId("cmd");
      this.store.queueReply({
        commandId,
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId,
        text: `已清空待发送队列，处理 ${flushed} 条命令。`
      });
      return { status: "queued", commandId };
    }

    if (normalized.startsWith("/mail-last ")) {
      const emails = extractEmails(event.messageText);
      if (emails.length !== 1) {
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          chatId: event.chatId,
          chatName: event.chatName,
          replyToMessageId: event.messageId,
          text: "请只提供一个邮箱，例如：/mail-last someone@example.com"
        });
        return { status: "queued", commandId };
      }

      const outcome = await this.rerunLastQuery(emails[0], {
        chatId: event.chatId,
        chatName: event.chatName,
        replyToMessageId: event.messageId
      });
      if (!outcome.ok) {
        const commandId = prefixedId("cmd");
        this.store.queueReply({
          commandId,
          chatId: event.chatId,
          chatName: event.chatName,
          replyToMessageId: event.messageId,
          text: "没有可重跑的历史查询。"
        });
        return { status: "queued", commandId };
      }
      return { status: "queued", jobId: outcome.jobId, commandId: outcome.commandId! };
    }

    return { status: "ignored", reason: "unsupported_admin_command" };
  }
}
