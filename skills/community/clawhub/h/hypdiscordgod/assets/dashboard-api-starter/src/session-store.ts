type Session = {
  discordUserId: string;
  accessToken: string;
  refreshToken?: string;
  createdAt: string;
  expiresAt: string;
};

const sessions = new Map<string, Session>();
const SESSION_TTL_MS = 1000 * 60 * 60 * 12;

export function createSession(sessionId: string, discordUserId: string, accessToken: string, refreshToken?: string) {
  const now = Date.now();
  sessions.set(sessionId, {
    discordUserId,
    accessToken,
    refreshToken,
    createdAt: new Date(now).toISOString(),
    expiresAt: new Date(now + SESSION_TTL_MS).toISOString()
  });
}

export function getSession(sessionId: string) {
  const session = sessions.get(sessionId) || null;
  if (!session) return null;
  if (Date.parse(session.expiresAt) < Date.now()) {
    sessions.delete(sessionId);
    return null;
  }
  return session;
}

export function deleteSession(sessionId: string) {
  sessions.delete(sessionId);
}
