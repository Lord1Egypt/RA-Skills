import type { IncomingMessage, ServerResponse } from "node:http";

import { WEBHOOK_PATHS } from "../../types/constants.js";

export type RouteFailureReason =
  | "wecom_account_not_found"
  | "wecom_account_conflict"
  | "wecom_identity_mismatch"
  | "wecom_matrix_path_required";

export function normalizeWecomWebhookPath(raw: string): string {
  const trimmed = raw.trim();
  if (!trimmed) return "/";
  const withSlash = trimmed.startsWith("/") ? trimmed : `/${trimmed}`;
  if (withSlash.length > 1 && withSlash.endsWith("/")) return withSlash.slice(0, -1);
  return withSlash;
}

export function resolveQueryParams(req: IncomingMessage): URLSearchParams {
  const url = new URL(req.url ?? "/", "http://localhost");
  return url.searchParams;
}

export function resolvePath(req: IncomingMessage): string {
  const url = new URL(req.url ?? "/", "http://localhost");
  return normalizeWecomWebhookPath(url.pathname || "/");
}

export function resolveSignatureParam(params: URLSearchParams): string {
  return params.get("msg_signature") ?? params.get("msgsignature") ?? params.get("signature") ?? "";
}

export function isAgentCallbackPathCandidate(path: string): boolean {
  return (
    path === WEBHOOK_PATHS.AGENT ||
    path === WEBHOOK_PATHS.AGENT_PLUGIN ||
    path.startsWith(`${WEBHOOK_PATHS.AGENT}/`) ||
    path.startsWith(`${WEBHOOK_PATHS.AGENT_PLUGIN}/`)
  );
}

export function isKefuCallbackPathCandidate(path: string): boolean {
  return (
    path === WEBHOOK_PATHS.KEFU ||
    path === WEBHOOK_PATHS.KEFU_PLUGIN ||
    path.startsWith(`${WEBHOOK_PATHS.KEFU}/`) ||
    path.startsWith(`${WEBHOOK_PATHS.KEFU_PLUGIN}/`)
  );
}

export function isNonMatrixWecomBasePath(path: string): boolean {
  return (
    path === WEBHOOK_PATHS.BOT ||
    path === WEBHOOK_PATHS.BOT_ALT ||
    path === WEBHOOK_PATHS.AGENT ||
    path === WEBHOOK_PATHS.KEFU ||
    path === WEBHOOK_PATHS.BOT_PLUGIN ||
    path === WEBHOOK_PATHS.AGENT_PLUGIN ||
    path === WEBHOOK_PATHS.KEFU_PLUGIN
  );
}

function maskAccountId(accountId: string): string {
  const normalized = accountId.trim();
  if (!normalized) return "***";
  if (normalized.length <= 4) return `${normalized[0] ?? "*"}***`;
  return `${normalized.slice(0, 2)}***${normalized.slice(-2)}`;
}

export function logRouteFailure(params: {
  reqId: string;
  path: string;
  method: string;
  reason: RouteFailureReason;
  candidateAccountIds: string[];
}): void {
  const payload = {
    reqId: params.reqId,
    path: params.path,
    method: params.method,
    reason: params.reason,
    candidateAccountIds: params.candidateAccountIds.map(maskAccountId),
  };
  console.error(`[wecom] route-error ${JSON.stringify(payload)}`);
}

export function writeRouteFailure(
  res: ServerResponse,
  reason: RouteFailureReason,
  message: string,
): void {
  res.statusCode = 401;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify({ error: reason, message }));
}

export async function readTextBody(
  req: IncomingMessage,
  maxBytes: number,
): Promise<{ ok: true; value: string } | { ok: false; error: string }> {
  const chunks: Buffer[] = [];
  let total = 0;
  return await new Promise((resolve) => {
    req.on("data", (chunk: Buffer) => {
      total += chunk.length;
      if (total > maxBytes) {
        resolve({ ok: false as const, error: "payload too large" });
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      resolve({ ok: true as const, value: Buffer.concat(chunks).toString("utf8") });
    });
    req.on("error", (err) => {
      resolve({ ok: false as const, error: String(err) });
    });
  });
}
