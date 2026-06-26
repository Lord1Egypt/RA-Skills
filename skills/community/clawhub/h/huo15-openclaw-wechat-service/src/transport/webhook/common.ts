import type { IncomingMessage, ServerResponse } from "node:http";
import { URL } from "node:url";

export const MAX_REQUEST_BODY_SIZE = 2 * 1024 * 1024;

export function resolvePath(req: IncomingMessage): string {
  const rawUrl = req.url ?? "/";
  const withHost = rawUrl.startsWith("http") ? rawUrl : `http://placeholder${rawUrl}`;
  try {
    return new URL(withHost).pathname || "/";
  } catch {
    return rawUrl.split("?")[0] ?? "/";
  }
}

export function resolveQueryParams(req: IncomingMessage): URLSearchParams {
  const rawUrl = req.url ?? "/";
  const withHost = rawUrl.startsWith("http") ? rawUrl : `http://placeholder${rawUrl}`;
  try {
    return new URL(withHost).searchParams;
  } catch {
    return new URLSearchParams();
  }
}

export function resolveSignatureParam(q: URLSearchParams): string {
  return q.get("msg_signature") ?? q.get("signature") ?? "";
}

export type RouteFailureReason =
  | "wechat_service_account_not_found"
  | "wechat_service_account_conflict"
  | "wechat_service_signature_invalid"
  | "wechat_service_decrypt_failed"
  | "wechat_service_invalid_xml"
  | "wechat_service_payload_too_large"
  | "wechat_service_method_not_allowed";

export function writeRouteFailure(
  res: ServerResponse,
  reason: RouteFailureReason,
  message: string,
): void {
  const status =
    reason === "wechat_service_method_not_allowed"
      ? 405
      : reason === "wechat_service_payload_too_large"
        ? 413
        : reason === "wechat_service_signature_invalid"
          ? 401
          : reason === "wechat_service_account_conflict"
            ? 409
            : 404;
  res.statusCode = status;
  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.end(`${reason}: ${message}`);
}

export function logRouteFailure(params: {
  reqId: string;
  path: string;
  method: string;
  reason: RouteFailureReason;
  candidateAccountIds: string[];
}): void {
  console.error(
    `[wechat-service] route-failure reqId=${params.reqId} path=${params.path} method=${params.method} reason=${params.reason} candidates=[${params.candidateAccountIds.join(",")}]`,
  );
}

export async function readTextBody(
  req: IncomingMessage,
  maxBytes: number,
): Promise<{ ok: true; value: string } | { ok: false; error: string }> {
  return new Promise((resolve) => {
    const chunks: Buffer[] = [];
    let total = 0;
    req.on("data", (chunk: Buffer) => {
      total += chunk.length;
      if (total > maxBytes) {
        req.removeAllListeners("data");
        req.removeAllListeners("end");
        resolve({ ok: false, error: `payload too large (>${maxBytes} bytes)` });
        return;
      }
      chunks.push(chunk);
    });
    req.on("end", () => {
      const value = Buffer.concat(chunks).toString("utf8");
      resolve({ ok: true, value });
    });
    req.on("error", (err: Error) => {
      resolve({ ok: false, error: err.message });
    });
  });
}

export function generateReqId(): string {
  return Math.random().toString(36).slice(2, 10);
}
