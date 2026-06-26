import type {
  AdapterHealth,
  MailFindRequest,
  MailFindResult,
  MailWaitRequest,
  MailWebhookEvent
} from "../../types/contracts";
import type { MailQueryAdapter } from "./types";

interface BhmailerHttpAdapterConfig {
  baseUrl: string;
  uid: string;
  sign: string;
  defaultTimeoutSec: number;
  extractionProfile: string;
  maxRetries?: number;
}

function asRecord(input: unknown): Record<string, unknown> | null {
  if (!input || typeof input !== "object") {
    return null;
  }
  return input as Record<string, unknown>;
}

function pickString(...values: unknown[]): string | undefined {
  for (const value of values) {
    if (typeof value === "string" && value.trim().length > 0) {
      return value.trim();
    }
  }
  return undefined;
}

function pickObject(...values: unknown[]): Record<string, unknown> | undefined {
  for (const value of values) {
    if (value && typeof value === "object" && !Array.isArray(value)) {
      return value as Record<string, unknown>;
    }
  }
  return undefined;
}

function pickBoolean(...values: unknown[]): boolean | undefined {
  for (const value of values) {
    if (typeof value === "boolean") {
      return value;
    }
    if (typeof value === "number") {
      return value !== 0;
    }
  }
  return undefined;
}

function truncate(text: string | undefined, max: number): string | undefined {
  if (!text) {
    return undefined;
  }
  if (text.length <= max) {
    return text;
  }
  return `${text.slice(0, Math.max(0, max - 1))}...`;
}

function previewLimitByProfile(profile: string): number {
  if (profile === "full-preview") {
    return 4000;
  }
  if (profile === "otp") {
    return 300;
  }
  return 1000;
}

function extractOtpCode(input: string | undefined): string | undefined {
  if (!input) {
    return undefined;
  }
  const match = input.match(/\b(\d{4,8})\b/);
  return match ? match[1] : undefined;
}

export class BhmailerHttpAdapter implements MailQueryAdapter {
  constructor(private readonly config: BhmailerHttpAdapterConfig) {}

  async health(): Promise<AdapterHealth> {
    if (!this.config.baseUrl || !this.config.uid || !this.config.sign) {
      return {
        ok: false,
        name: "bhmailer-http",
        detail: "BHMailer config incomplete"
      };
    }
    return {
      ok: true,
      name: "bhmailer-http",
      detail: "configured"
    };
  }

  async findLatest(req: MailFindRequest): Promise<MailFindResult> {
    const payload = {
      uid: this.config.uid,
      sign: this.config.sign,
      email: req.email,
      extractionProfile: this.config.extractionProfile
    };

    const raw = await this.postFirstSuccess(["/mailFind", "/api/mailFind", "/checkMail", "/api/checkMail"], payload);
    let normalized = this.normalizeQueryResult(raw, req.email, "findLatest");
    normalized = await this.maybeEnrichByExtraction(normalized, req.email);
    return normalized;
  }

  async waitForNew(req: MailWaitRequest): Promise<MailFindResult> {
    const payload = {
      uid: this.config.uid,
      sign: this.config.sign,
      email: req.email,
      timeoutSec: req.timeoutSec,
      extractionProfile: this.config.extractionProfile
    };

    const raw = await this.postFirstSuccess(
      ["/mailReceive", "/api/mailReceive", "/checkMail", "/api/checkMail"],
      payload
    );
    let normalized = this.normalizeQueryResult(raw, req.email, "waitForNew");
    normalized = await this.maybeEnrichByExtraction(normalized, req.email);
    return normalized;
  }

  async normalizeWebhook(payload: unknown): Promise<MailWebhookEvent> {
    const record = asRecord(payload) ?? {};
    const data = pickObject(record.data, record.result) ?? record;
    const extractedFields = pickObject(data.extractedFields, data.fields);

    return {
      matchedEmail: pickString(data.matchedEmail, data.email) ?? "",
      subject: pickString(data.subject, data.title),
      from: pickString(data.from, data.sender),
      receivedAt: pickString(data.receivedAt, data.time, data.received_time),
      bodyPreview: truncate(pickString(data.bodyPreview, data.preview, data.body), 400),
      extractedFields: extractedFields as Record<string, string> | undefined,
      rawProvider: "bhmailer-http",
      targetChatId: pickString(data.chatId, data.targetChatId),
      targetChatName: pickString(data.chatName, data.targetChatName),
      replyToMessageId: pickString(data.replyToMessageId)
    };
  }

  private normalizeQueryResult(raw: unknown, email: string, mode: "findLatest" | "waitForNew"): MailFindResult {
    const top = asRecord(raw) ?? {};
    const data = pickObject(top.data, top.result, top.mail) ?? top;

    const found =
      pickBoolean(data.found, data.ok, top.found, top.ok) ??
      Boolean(
        pickString(
          data.mailId,
          data.id,
          pickObject(data.mail)?.id,
          pickObject(data.mail)?.mailId,
          data.subject,
          pickObject(data.mail)?.subject
        )
      );

    const nestedMail = pickObject(data.mail);
    const extractedFields =
      pickObject(data.extractedFields, data.fields, nestedMail?.extractedFields) ??
      ({} as Record<string, string>);

    if (!found) {
      return {
        found: false,
        mode,
        matchedEmail: email,
        rawProvider: "bhmailer-http",
        reason: mode === "waitForNew" ? "timeout" : "not_found"
      };
    }

    const preview = truncate(
      pickString(data.bodyPreview, data.preview, nestedMail?.preview, data.body),
      previewLimitByProfile(this.config.extractionProfile)
    );
    const mergedFields: Record<string, string> = { ...(extractedFields as Record<string, string>) };
    if (this.config.extractionProfile === "otp" && !mergedFields.code) {
      const code = extractOtpCode(preview ?? pickString(data.body, nestedMail?.body));
      if (code) {
        mergedFields.code = code;
      }
    }

    return {
      found: true,
      mode,
      matchedEmail: pickString(data.matchedEmail, data.email) ?? email,
      mailId: pickString(data.mailId, data.id, nestedMail?.mailId, nestedMail?.id),
      subject: pickString(data.subject, nestedMail?.subject, data.title),
      from: pickString(data.from, nestedMail?.from, data.sender),
      receivedAt: pickString(data.receivedAt, nestedMail?.receivedAt, data.time, data.received_time),
      bodyPreview: preview,
      extractedFields: mergedFields,
      rawProvider: "bhmailer-http"
    };
  }

  private async postFirstSuccess(paths: string[], payload: Record<string, unknown>): Promise<unknown> {
    let lastError: unknown = new Error("no_request_attempted");
    for (const path of paths) {
      try {
        return await this.postJson(path, payload);
      } catch (error) {
        lastError = error;
      }
    }
    throw lastError;
  }

  private async postJson(pathname: string, payload: Record<string, unknown>): Promise<unknown> {
    const base = this.config.baseUrl.replace(/\/+$/, "");
    const path = pathname.startsWith("/") ? pathname : `/${pathname}`;
    const url = `${base}${path}`;

    const controller = new AbortController();
    const timeoutMs = Math.max(1000, this.config.defaultTimeoutSec * 1000);
    const timeout = setTimeout(() => controller.abort(), timeoutMs);

    try {
      const retries = Math.max(0, this.config.maxRetries ?? 2);
      let attempt = 0;
      while (true) {
        attempt += 1;
        try {
          const response = await fetch(url, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify(payload),
            signal: controller.signal
          });

          if (!response.ok) {
            if (response.status >= 500 && attempt <= retries) {
              await this.sleep(attempt * 200);
              continue;
            }
            throw new Error(`bhmailer_http_${response.status}`);
          }

          return await response.json();
        } catch (error) {
          if (attempt > retries) {
            throw error;
          }
          await this.sleep(attempt * 200);
        }
      }
    } finally {
      clearTimeout(timeout);
    }
  }

  private async sleep(ms: number): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, ms));
  }

  private async maybeEnrichByExtraction(base: MailFindResult, email: string): Promise<MailFindResult> {
    if (!base.found) {
      return base;
    }
    if (this.config.extractionProfile === "default") {
      return base;
    }
    if (!base.mailId) {
      return base;
    }

    try {
      const payload = {
        uid: this.config.uid,
        sign: this.config.sign,
        mailId: base.mailId,
        email,
        extractionProfile: this.config.extractionProfile
      };
      const raw = await this.postFirstSuccess(["/mailExtract", "/api/mailExtract"], payload);
      const extract = this.normalizeExtractResult(raw);

      return {
        ...base,
        subject: extract.subject ?? base.subject,
        from: extract.from ?? base.from,
        receivedAt: extract.receivedAt ?? base.receivedAt,
        bodyPreview: extract.bodyPreview ?? base.bodyPreview,
        extractedFields: {
          ...(base.extractedFields ?? {}),
          ...(extract.extractedFields ?? {})
        }
      };
    } catch (error) {
      return base;
    }
  }

  private normalizeExtractResult(raw: unknown): {
    subject?: string;
    from?: string;
    receivedAt?: string;
    bodyPreview?: string;
    extractedFields?: Record<string, string>;
  } {
    const top = asRecord(raw) ?? {};
    const data = pickObject(top.data, top.result) ?? top;
    const fields = pickObject(data.extractedFields, data.fields, data.extract);
    return {
      subject: pickString(data.subject, data.title),
      from: pickString(data.from, data.sender),
      receivedAt: pickString(data.receivedAt, data.time),
      bodyPreview: truncate(
        pickString(data.bodyPreview, data.preview, data.body),
        previewLimitByProfile(this.config.extractionProfile)
      ),
      extractedFields: fields as Record<string, string> | undefined
    };
  }
}
