import type { TransportSessionSnapshot } from "../types/index.js";

export class WecomStatusRegistry {
  private readonly sessions = new Map<string, TransportSessionSnapshot>();

  write(snapshot: TransportSessionSnapshot): void {
    this.sessions.set(`${snapshot.accountId}:${snapshot.transport}`, snapshot);
  }

  read(accountId: string): TransportSessionSnapshot[] {
    return Array.from(this.sessions.values()).filter((entry) => entry.accountId === accountId);
  }
}
