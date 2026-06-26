export type JobMode = "findLatest" | "waitForNew";

export type JobStatus =
  | "CREATED"
  | "PARSED"
  | "REJECTED"
  | "QUERYING_HISTORY"
  | "WAITING_NEW_MAIL"
  | "MATCHED"
  | "NOT_FOUND"
  | "TIMEOUT"
  | "REPLY_QUEUED"
  | "REPLY_SENT"
  | "REPLY_FAILED"
  | "COMPLETED";

export interface AdapterHealth {
  ok: boolean;
  name: string;
  detail?: string;
}

export interface IncomingChatMessageEvent {
  eventId: string;
  source: string;
  sidecarId: string;
  platform: string;
  chatType: "group" | "private";
  chatId: string;
  chatName: string;
  senderDisplayName?: string;
  messageId: string;
  messageText: string;
  messageTime: string;
  observedAt: string;
}

export interface MailFindRequest {
  email: string;
  mode: "findLatest";
  sourceEventId: string;
}

export interface MailWaitRequest {
  email: string;
  mode: "waitForNew";
  timeoutSec: number;
  sourceEventId: string;
}

export interface MailFindResult {
  found: boolean;
  mode: JobMode;
  matchedEmail: string;
  mailId?: string;
  subject?: string;
  from?: string;
  receivedAt?: string;
  bodyPreview?: string;
  extractedFields?: Record<string, string>;
  rawProvider: string;
  reason?: string;
}

export interface MailWebhookEvent {
  matchedEmail: string;
  subject?: string;
  from?: string;
  receivedAt?: string;
  bodyPreview?: string;
  extractedFields?: Record<string, string>;
  rawProvider: string;
  targetChatId?: string;
  targetChatName?: string;
  replyToMessageId?: string;
}

export interface OutboundWeChatSendCommand {
  commandId: string;
  chatId: string;
  chatName?: string;
  replyToMessageId?: string;
  text: string;
  createdAt: string;
}

export interface MailQueryJob {
  jobId: string;
  sourceEventId: string;
  chatId: string;
  chatName: string;
  replyToMessageId?: string;
  email: string;
  mode: JobMode;
  status: JobStatus;
  createdAt: string;
  updatedAt: string;
  expiresAt: string;
  error?: string;
}

export interface IngestDecisionIgnored {
  status: "ignored";
  reason: string;
}

export interface IngestDecisionDuplicate {
  status: "duplicate";
}

export interface IngestDecisionQueued {
  status: "queued";
  jobId?: string;
  commandId: string;
}

export type IngestDecision =
  | IngestDecisionIgnored
  | IngestDecisionDuplicate
  | IngestDecisionQueued;

