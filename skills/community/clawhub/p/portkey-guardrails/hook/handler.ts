import * as path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const hookDir = path.dirname(fileURLToPath(import.meta.url));
const workspaceRoot = path.resolve(hookDir, "../..");

// The Portkey implementation resolves audit/config paths from this env var.
process.env.OPENCLAW_WORKSPACE_ROOT ??= workspaceRoot;

const guardrailsModulePath = pathToFileURL(
  path.resolve(
    workspaceRoot,
    "projects/portkey-gateway-integration/implementation/guardrails/index.ts"
  )
).href;

let guardrailsModulePromise:
  | Promise<{
      runPreDispatchGuards: (
        agentId: string,
        message: string,
        agentGuardrails?: unknown
      ) => Promise<any>;
      runPostDispatchGuards: (
        agentId: string,
        response: string,
        agentGuardrails?: unknown
      ) => Promise<any>;
    }>
  | null = null;

function loadGuardrailsModule() {
  guardrailsModulePromise ??= import(guardrailsModulePath);
  return guardrailsModulePromise;
}

type HookEvent = {
  type?: string;
  action?: string;
  context?: Record<string, unknown>;
  messages?: string[];
};

function getContext(event: HookEvent): Record<string, unknown> {
  return (event.context ?? {}) as Record<string, unknown>;
}

function getString(value: unknown): string {
  return typeof value === "string" ? value : "";
}

function extractMessageContent(event: HookEvent): string {
  const context = getContext(event);

  return (
    getString(context.bodyForAgent) ||
    getString(context.content) ||
    getString(context.body) ||
    getString(context.transcript) ||
    getString(context.message)
  );
}

function resolveAgentId(event: HookEvent): string {
  const context = getContext(event);
  return (
    getString(context.agentId) ||
    getString(context.agent) ||
    getString(context.sessionAgentId) ||
    getString(context.sessionKey) ||
    "main"
  );
}

function note(event: HookEvent, message: string) {
  if (Array.isArray(event.messages)) {
    event.messages.push(message);
  }
}

function markBlocked(event: HookEvent, reason: string) {
  const context = getContext(event);
  context.blocked = true;
  context.blockReason = reason;
  context.blockedReason = reason;
  context.cancel = true;
  event.context = context;
}

function markRedacted(event: HookEvent, redacted: string) {
  const context = getContext(event);
  context.content = redacted;
  context.bodyForAgent = redacted;
  context.redactedContent = redacted;
  event.context = context;
}

async function handleInboundGuardrails(event: HookEvent) {
  const content = extractMessageContent(event);
  if (!content) return;

  const agentId = resolveAgentId(event);
  const { runPreDispatchGuards } = await loadGuardrailsModule();
  const result = await runPreDispatchGuards(agentId, content);

  if (result.action === "pass") return;

  const reason = result.detail ?? `${result.rule ?? "guardrail"} triggered`;

  if (result.action === "block") {
    markBlocked(event, reason);
    note(event, `🛡️ Guardrails blocked this message: ${reason}`);
    return { cancel: true, reason, blocked: true };
  }

  if (result.action === "flag" || result.action === "warn") {
    note(event, `⚠️ Guardrails ${result.action}: ${reason}`);
    return { cancel: false, reason, flagged: true };
  }

  return { cancel: false, reason };
}

async function handleOutboundGuardrails(event: HookEvent) {
  const content = extractMessageContent(event);
  if (!content) return;

  const agentId = resolveAgentId(event);
  const { runPostDispatchGuards } = await loadGuardrailsModule();
  const result = await runPostDispatchGuards(agentId, content);

  if (result.action === "pass") return;

  const reason = result.detail ?? `${result.rule ?? "guardrail"} triggered`;

  if (result.action === "redact" && result.redacted) {
    markRedacted(event, result.redacted);
    note(event, `🛡️ Guardrails redacted outbound content: ${reason}`);
    return { cancel: false, reason, redacted: true, content: result.redacted };
  }

  if (result.action === "block") {
    markBlocked(event, reason);
    note(event, `🛡️ Guardrails blocked outbound content: ${reason}`);
    return { cancel: true, reason, blocked: true };
  }

  if (result.action === "flag" || result.action === "warn") {
    note(event, `⚠️ Guardrails ${result.action}: ${reason}`);
    return { cancel: false, reason, flagged: true };
  }

  return { cancel: false, reason };
}

const handler = async (event: HookEvent): Promise<unknown> => {
  const type = event.type;
  const action = event.action;

  if (type !== "message") return;

  if (action === "received" || action === "preprocessed") {
    return handleInboundGuardrails(event);
  }

  if (action === "sending" || action === "sent") {
    return handleOutboundGuardrails(event);
  }
};

export default handler;
