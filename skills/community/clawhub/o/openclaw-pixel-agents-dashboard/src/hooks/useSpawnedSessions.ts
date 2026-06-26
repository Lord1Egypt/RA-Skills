/**
 * useSpawnedSessions — Manages spawned Rita/Rivet sessions via the dashboard API.
 * Tracks conversations, handles WebSocket events for real-time updates.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { getApiBase } from '../apiBase.js';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface SpawnedSession {
  id: string;
  agent: 'rita' | 'rivet';
  sessionKey: string;
  status: 'running' | 'idle' | 'error';
  messages: ChatMessage[];
  error?: string;
}

type SpawnAgent = 'rita' | 'rivet';

export function useSpawnedSessions() {
  const [sessions, setSessions] = useState<Map<string, SpawnedSession>>(new Map());
  const [isSpawning, setIsSpawning] = useState(false);
  const sessionsRef = useRef(sessions);
  sessionsRef.current = sessions;

  // Handle incoming WebSocket events for spawn updates
  const handleSpawnEvent = useCallback((msg: Record<string, unknown>) => {
    const sessionId = msg.sessionId as string;
    if (!sessionId) return;

    switch (msg.type) {
      case 'spawnMessage': {
        const role = msg.role as 'user' | 'assistant';
        const content = msg.content as string;
        const timestamp = (msg.timestamp as number) || Date.now();
        setSessions(prev => {
          const next = new Map(prev);
          const session = next.get(sessionId);
          if (session) {
            // Avoid duplicate messages
            const lastMsg = session.messages[session.messages.length - 1];
            if (!(lastMsg && lastMsg.role === role && lastMsg.content === content)) {
              next.set(sessionId, {
                ...session,
                messages: [...session.messages, { role, content, timestamp }],
              });
            }
          }
          return next;
        });
        break;
      }
      case 'spawnStatus': {
        const status = msg.status as SpawnedSession['status'];
        setSessions(prev => {
          const next = new Map(prev);
          const session = next.get(sessionId);
          if (session) {
            next.set(sessionId, { ...session, status });
          }
          return next;
        });
        break;
      }
      case 'spawnError': {
        const error = msg.error as string;
        setSessions(prev => {
          const next = new Map(prev);
          const session = next.get(sessionId);
          if (session) {
            next.set(sessionId, { ...session, status: 'error', error });
          }
          return next;
        });
        break;
      }
      case 'spawnClosed': {
        setSessions(prev => {
          const next = new Map(prev);
          next.delete(sessionId);
          return next;
        });
        break;
      }
    }
  }, []);

  // Spawn a new agent session
  const spawn = useCallback(async (agent: SpawnAgent, task: string): Promise<string | null> => {
    setIsSpawning(true);
    try {
      const res = await fetch(`${getApiBase()}/api/spawn`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ agent, task }),
      });
      const data = await res.json();
      if (!data.ok) {
        console.error('[Spawn] Failed:', data.error);
        return null;
      }

      // Add to local state immediately
      const session: SpawnedSession = {
        id: data.id,
        agent: data.agent,
        sessionKey: data.sessionKey,
        status: 'running',
        messages: [{ role: 'user', content: task, timestamp: Date.now() }],
      };
      setSessions(prev => {
        const next = new Map(prev);
        next.set(data.id, session);
        return next;
      });

      return data.id;
    } catch (err) {
      console.error('[Spawn] Error:', err);
      return null;
    } finally {
      setIsSpawning(false);
    }
  }, []);

  // Send a follow-up message
  const sendMessage = useCallback(async (sessionId: string, message: string): Promise<boolean> => {
    // Add user message to local state immediately
    setSessions(prev => {
      const next = new Map(prev);
      const session = next.get(sessionId);
      if (session) {
        next.set(sessionId, {
          ...session,
          status: 'running',
          messages: [...session.messages, { role: 'user', content: message, timestamp: Date.now() }],
        });
      }
      return next;
    });

    try {
      const res = await fetch(`${getApiBase()}/api/spawn/${sessionId}/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      return data.ok;
    } catch {
      return false;
    }
  }, []);

  // Close a session
  const closeSession = useCallback(async (sessionId: string): Promise<void> => {
    try {
      await fetch(`${getApiBase()}/api/spawn/${sessionId}`, { method: 'DELETE' });
    } catch { /* ignore */ }
    setSessions(prev => {
      const next = new Map(prev);
      next.delete(sessionId);
      return next;
    });
  }, []);

  // Load existing sessions on mount (in case of page refresh during active sessions)
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${getApiBase()}/api/spawn`);
        if (res.ok) {
          const data = await res.json();
          if (data.sessions?.length > 0) {
            setSessions(new Map(data.sessions.map((s: SpawnedSession) => [s.id, s])));
          }
        }
      } catch { /* ignore */ }
    })();
  }, []);

  const activeCount = Array.from(sessions.values()).filter(
    s => s.status === 'running' || s.status === 'idle',
  ).length;

  return {
    sessions,
    activeCount,
    isSpawning,
    spawn,
    sendMessage,
    closeSession,
    handleSpawnEvent,
  };
}
