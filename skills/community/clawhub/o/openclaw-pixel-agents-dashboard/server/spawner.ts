/**
 * TaskSpawner — Spawns agent sessions via the gateway tools API.
 * Uses sessions_spawn for initial spawn, sessions_send for follow-ups.
 * Polls sessions_history for responses. Gateway token from env, never exposed to browser.
 */

import { randomUUID } from 'crypto';

// ── Types ──────────────────────────────────────────────────

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: number;
}

export interface SpawnedSession {
  id: string;
  agent: string;
  sessionKey: string;
  status: 'running' | 'idle' | 'error';
  messages: ChatMessage[];
  startedAt: number;
  lastActivityAt: number;
  error?: string;
}

interface SpawnerCallbacks {
  onChunk: (sessionId: string, text: string) => void;
  onMessage: (sessionId: string, msg: ChatMessage) => void;
  onStatusChange: (sessionId: string, status: SpawnedSession['status']) => void;
  onError: (sessionId: string, error: string) => void;
}

// ── Configuration ──────────────────────────────────────────

import {
  SPAWNABLE_AGENTS,
  GATEWAY_URL as CONFIG_GATEWAY_URL,
  GATEWAY_TOKEN as CONFIG_GATEWAY_TOKEN,
} from './config.js';

const DEFAULT_ALLOWED_AGENTS = SPAWNABLE_AGENTS.length > 0 ? SPAWNABLE_AGENTS : ['rita', 'rivet'];
const MAX_MESSAGE_LENGTH = 2000;
const GATEWAY_URL = CONFIG_GATEWAY_URL;
const GATEWAY_TOKEN = CONFIG_GATEWAY_TOKEN;
const POLL_INTERVAL_MS = 1500;
const POLL_TIMEOUT_MS = 300_000; // 5 min — Gemini spawns can be slow

// ── Spawner ────────────────────────────────────────────────

export class TaskSpawner {
  private sessions = new Map<string, SpawnedSession>();
  private callbacks: SpawnerCallbacks;
  private allowedAgents: string[];
  maxConcurrent: number;

  constructor(callbacks: SpawnerCallbacks, maxConcurrent = 3, allowedAgents?: string[]) {
    this.callbacks = callbacks;
    this.maxConcurrent = maxConcurrent;
    this.allowedAgents = allowedAgents ?? DEFAULT_ALLOWED_AGENTS;
  }

  /** Spawn a new agent session with an initial task */
  async spawn(agent: string, task: string): Promise<SpawnedSession> {
    if (!this.allowedAgents.includes(agent)) {
      throw new Error(`Agent '${agent}' is not allowed. Only: ${this.allowedAgents.join(', ')}`);
    }

    if (!task || task.trim().length === 0) {
      throw new Error('Task cannot be empty');
    }
    if (task.length > MAX_MESSAGE_LENGTH) {
      throw new Error(`Task exceeds ${MAX_MESSAGE_LENGTH} character limit`);
    }

    const activeCount = this.getActiveSessions().length;
    if (activeCount >= this.maxConcurrent) {
      throw new Error(`Max concurrent sessions (${this.maxConcurrent}) reached`);
    }

    const id = randomUUID();

    const session: SpawnedSession = {
      id,
      agent,
      sessionKey: '', // set after gateway responds
      status: 'running',
      messages: [{ role: 'user', content: task.trim(), timestamp: Date.now() }],
      startedAt: Date.now(),
      lastActivityAt: Date.now(),
    };

    this.sessions.set(id, session);
    this.callbacks.onStatusChange(id, 'running');

    // Spawn via gateway tools API
    this.doSpawn(session, task.trim()).catch(err => {
      console.error(`[Spawner] Spawn error for ${id}:`, err);
    });

    return session;
  }

  /** Send a follow-up message to an existing session */
  async sendMessage(sessionId: string, message: string): Promise<void> {
    const session = this.sessions.get(sessionId);
    if (!session) throw new Error('Session not found');
    if (session.status === 'running') throw new Error('Session is busy — wait for current response');
    if (!session.sessionKey) throw new Error('Session not yet initialized');

    if (!message || message.trim().length === 0) {
      throw new Error('Message cannot be empty');
    }
    if (message.length > MAX_MESSAGE_LENGTH) {
      throw new Error(`Message exceeds ${MAX_MESSAGE_LENGTH} character limit`);
    }

    const userMsg: ChatMessage = { role: 'user', content: message.trim(), timestamp: Date.now() };
    session.messages.push(userMsg);
    session.status = 'running';
    session.lastActivityAt = Date.now();

    this.callbacks.onMessage(sessionId, userMsg);
    this.callbacks.onStatusChange(sessionId, 'running');

    this.doSend(session, message.trim()).catch(err => {
      console.error(`[Spawner] Send error for ${sessionId}:`, err);
    });
  }

  /** Close/end a spawned session */
  closeSession(sessionId: string): boolean {
    const session = this.sessions.get(sessionId);
    if (!session) return false;
    this.sessions.delete(sessionId);
    return true;
  }

  getSession(id: string): SpawnedSession | undefined {
    return this.sessions.get(id);
  }

  listSessions(): SpawnedSession[] {
    return Array.from(this.sessions.values());
  }

  getActiveSessions(): SpawnedSession[] {
    return this.listSessions().filter(s => s.status === 'running' || s.status === 'idle');
  }

  getAllowedAgents(): string[] {
    return [...this.allowedAgents];
  }

  // ── Gateway Communication ──────────────────────────────

  /** Invoke a gateway tool via /tools/invoke */
  private async invokeGatewayTool(tool: string, args: Record<string, unknown>): Promise<{
    ok: boolean;
    content?: string;
    error?: string;
  }> {
    const response = await fetch(`${GATEWAY_URL}/tools/invoke`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${GATEWAY_TOKEN}`,
      },
      body: JSON.stringify({ tool, args }),
    });

    if (!response.ok) {
      let body = '';
      try { body = await response.text(); } catch { /* ignore */ }
      return { ok: false, error: `Gateway returned ${response.status}: ${body || response.statusText}` };
    }

    const data = await response.json() as {
      ok: boolean;
      result?: { content?: Array<{ text?: string }> };
      error?: { message?: string };
    };

    if (!data.ok) {
      return { ok: false, error: data.error?.message || 'Unknown gateway error' };
    }

    const text = data.result?.content?.[0]?.text;
    return { ok: true, content: text };
  }

  /** Spawn via sessions_spawn, then poll for response */
  private async doSpawn(session: SpawnedSession, task: string): Promise<void> {
    try {
      const result = await this.invokeGatewayTool('sessions_spawn', {
        task,
        agentId: session.agent,
        runtime: 'subagent',
        mode: 'run', // one-shot; follow-ups spawn new runs with context
      });

      if (!result.ok || !result.content) {
        const errorMsg = result.error || 'Spawn returned no content';
        this.setError(session, errorMsg);
        return;
      }

      // Parse spawn response to get session key
      const spawnData = JSON.parse(result.content) as {
        status?: string;
        childSessionKey?: string;
        error?: string;
      };

      if (spawnData.status === 'error' || !spawnData.childSessionKey) {
        this.setError(session, spawnData.error || 'Spawn failed — no session key returned');
        return;
      }

      session.sessionKey = spawnData.childSessionKey;
      console.log(`[Spawner] Spawned ${session.agent} → ${session.sessionKey}`);

      // Poll for the assistant response
      await this.pollForResponse(session);
    } catch (err) {
      this.setError(session, `Spawn error: ${(err as Error).message}`);
    }
  }

  /** Send follow-up by spawning a new run with conversation context */
  private async doSend(session: SpawnedSession, message: string): Promise<void> {
    // Build context from conversation history
    const contextLines = session.messages
      .slice(0, -1) // exclude the message we just added (it becomes the new task)
      .map(m => `[${m.role}]: ${m.content}`)
      .join('\n');

    const taskWithContext = contextLines.length > 0
      ? `Previous conversation:\n${contextLines}\n\n---\nContinuing the conversation. New message: ${message}`
      : message;

    try {
      const result = await this.invokeGatewayTool('sessions_spawn', {
        task: taskWithContext,
        agentId: session.agent,
        runtime: 'subagent',
        mode: 'run',
      });

      if (!result.ok || !result.content) {
        this.setError(session, result.error || 'Follow-up spawn returned no content');
        return;
      }

      const spawnData = JSON.parse(result.content) as {
        status?: string;
        childSessionKey?: string;
        error?: string;
      };

      if (spawnData.status === 'error' || !spawnData.childSessionKey) {
        this.setError(session, spawnData.error || 'Follow-up spawn failed');
        return;
      }

      // Update session key to the new child session for polling
      const prevKey = session.sessionKey;
      session.sessionKey = spawnData.childSessionKey;
      console.log(`[Spawner] Follow-up ${session.agent}: ${prevKey} → ${session.sessionKey}`);

      await this.pollForResponse(session);
    } catch (err) {
      this.setError(session, `Follow-up error: ${(err as Error).message}`);
    }
  }

  /** Poll sessions_history until we see an assistant message in the current child session */
  private async pollForResponse(session: SpawnedSession): Promise<void> {
    const startedAt = Date.now();
    // Each spawn is a fresh session — we just need 1 assistant message
    const expectedAssistantCount = 1;

    while (Date.now() - startedAt < POLL_TIMEOUT_MS) {
      await sleep(POLL_INTERVAL_MS);

      // Session might have been closed while we were polling
      if (!this.sessions.has(session.id)) return;

      try {
        const result = await this.invokeGatewayTool('sessions_history', {
          sessionKey: session.sessionKey,
          limit: 20,
        });

        if (!result.ok || !result.content) continue;

        let history: { messages?: Array<{ role: string; content: string | Array<{ type: string; text?: string }> }> };
        try {
          history = JSON.parse(result.content);
        } catch {
          continue;
        }

        if (!history.messages) continue;

        const assistantMsgs = history.messages.filter(m => m.role === 'assistant');
        if (assistantMsgs.length >= expectedAssistantCount) {
          // Extract the latest assistant message content
          const latest = assistantMsgs[assistantMsgs.length - 1];
          let content = '';

          if (typeof latest.content === 'string') {
            content = latest.content;
          } else if (Array.isArray(latest.content)) {
            // Content blocks — extract text parts, skip thinking
            content = latest.content
              .filter(b => b.type === 'text' && b.text)
              .map(b => b.text!)
              .join('\n');
          }

          content = cleanAgentResponse(content);

          if (content.length > 0) {
            const assistantMsg: ChatMessage = {
              role: 'assistant',
              content,
              timestamp: Date.now(),
            };
            session.messages.push(assistantMsg);
            session.lastActivityAt = Date.now();
            this.callbacks.onMessage(session.id, assistantMsg);
          }

          session.status = 'idle';
          session.lastActivityAt = Date.now();
          this.callbacks.onStatusChange(session.id, 'idle');
          return;
        }
      } catch (err) {
        console.error(`[Spawner] Poll error for ${session.id}:`, (err as Error).message);
        // Keep polling — transient errors happen
      }
    }

    // Timeout
    this.setError(session, 'Response timeout — agent may still be working');
  }

  private setError(session: SpawnedSession, errorMsg: string): void {
    session.status = 'error';
    session.error = errorMsg;
    session.lastActivityAt = Date.now();
    this.callbacks.onError(session.id, errorMsg);
    this.callbacks.onStatusChange(session.id, 'error');
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/** Strip model-specific formatting artifacts from responses */
function cleanAgentResponse(content: string): string {
  return content
    // Strip Gemini <think>...</think> blocks
    .replace(/<think>[\s\S]*?<\/think>/gi, '')
    // Strip Gemini <final>...</final> wrappers (keep content)
    .replace(/<final>([\s\S]*?)<\/final>/gi, '$1')
    // Strip [Subagent Context] preambles that leak through
    .replace(/^\[Subagent Context\].*$/m, '')
    .trim();
}
