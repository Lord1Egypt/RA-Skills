import type { TransportSessionSnapshot } from "../types/index.js";

export function summarizeTransportSessions(sessions: TransportSessionSnapshot[]): string[] {
  return sessions.map((session) => {
    const parts = [
      session.transport,
      session.running ? "running" : "stopped",
      session.ownerId ? `owner=${session.ownerId}` : "owner=none",
    ];
    if (session.connected != null) parts.push(`connected=${String(session.connected)}`);
    if (session.authenticated != null) parts.push(`authenticated=${String(session.authenticated)}`);
    return parts.join(" ");
  });
}
