import type {
  AdapterHealth,
  MailFindRequest,
  MailFindResult,
  MailWaitRequest,
  MailWebhookEvent
} from "../../types/contracts";

export interface MailQueryAdapter {
  health(): Promise<AdapterHealth>;
  findLatest(req: MailFindRequest): Promise<MailFindResult>;
  waitForNew(req: MailWaitRequest): Promise<MailFindResult>;
  normalizeWebhook(payload: unknown): Promise<MailWebhookEvent>;
}

