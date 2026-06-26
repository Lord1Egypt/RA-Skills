import type { RawFrameReference, WecomAuditCategory, WecomTransportKind } from "../types/index.js";

export type AuditEntry = {
  accountId: string;
  transport: WecomTransportKind;
  category: WecomAuditCategory;
  messageId?: string;
  summary: string;
  raw?: RawFrameReference;
  createdAt: number;
  error?: string;
};

export class WecomAuditLog {
  private readonly entries: AuditEntry[] = [];

  append(entry: AuditEntry): void {
    this.entries.push(entry);
    if (this.entries.length > 200) {
      this.entries.shift();
    }
  }

  list(): AuditEntry[] {
    return [...this.entries];
  }

  appendInbound(entry: Omit<AuditEntry, "category" | "createdAt">): void {
    this.append({
      ...entry,
      category: "inbound",
      createdAt: Date.now(),
    });
  }

  appendOperational(entry: Omit<AuditEntry, "createdAt">): void {
    this.append({
      ...entry,
      createdAt: Date.now(),
    });
  }

  latestOperationalIssue(): AuditEntry | undefined {
    return [...this.entries]
      .reverse()
      .find((entry) => entry.category !== "inbound");
  }
}
