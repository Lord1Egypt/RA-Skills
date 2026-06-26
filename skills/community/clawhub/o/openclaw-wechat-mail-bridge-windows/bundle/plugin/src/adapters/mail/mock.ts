import type {
  AdapterHealth,
  MailFindRequest,
  MailFindResult,
  MailWaitRequest,
  MailWebhookEvent
} from "../../types/contracts";
import type { MailQueryAdapter } from "./types";

function nowIso(): string {
  return new Date().toISOString();
}

export class MockMailAdapter implements MailQueryAdapter {
  async health(): Promise<AdapterHealth> {
    return {
      ok: true,
      name: "mock-mail",
      detail: "mock adapter active"
    };
  }

  async findLatest(req: MailFindRequest): Promise<MailFindResult> {
    return {
      found: true,
      mode: "findLatest",
      matchedEmail: req.email,
      mailId: "mock_latest_001",
      subject: "Mock mail result",
      from: "no-reply@example.com",
      receivedAt: nowIso(),
      bodyPreview: "This is a mock mail preview from the mock adapter.",
      extractedFields: { code: "123456" },
      rawProvider: "mock"
    };
  }

  async waitForNew(req: MailWaitRequest): Promise<MailFindResult> {
    const sleepMs = Math.min(1200, Math.max(0, req.timeoutSec * 10));
    if (sleepMs > 0) {
      await new Promise((resolve) => setTimeout(resolve, sleepMs));
    }

    return {
      found: true,
      mode: "waitForNew",
      matchedEmail: req.email,
      mailId: "mock_watch_001",
      subject: "Mock new mail",
      from: "alerts@example.com",
      receivedAt: nowIso(),
      bodyPreview: "A new mock mail arrived during watch mode.",
      extractedFields: { code: "654321" },
      rawProvider: "mock"
    };
  }

  async normalizeWebhook(payload: unknown): Promise<MailWebhookEvent> {
    const asRecord = payload && typeof payload === "object" ? (payload as Record<string, unknown>) : {};
    const matchedEmail = String(asRecord.matchedEmail ?? asRecord.email ?? "");
    return {
      matchedEmail,
      subject: asRecord.subject ? String(asRecord.subject) : undefined,
      from: asRecord.from ? String(asRecord.from) : undefined,
      receivedAt: asRecord.receivedAt ? String(asRecord.receivedAt) : undefined,
      bodyPreview: asRecord.bodyPreview ? String(asRecord.bodyPreview) : undefined,
      extractedFields:
        asRecord.extractedFields && typeof asRecord.extractedFields === "object"
          ? (asRecord.extractedFields as Record<string, string>)
          : undefined,
      rawProvider: "mock-webhook",
      targetChatId: asRecord.chatId ? String(asRecord.chatId) : undefined,
      targetChatName: asRecord.chatName ? String(asRecord.chatName) : undefined,
      replyToMessageId: asRecord.replyToMessageId ? String(asRecord.replyToMessageId) : undefined
    };
  }
}

