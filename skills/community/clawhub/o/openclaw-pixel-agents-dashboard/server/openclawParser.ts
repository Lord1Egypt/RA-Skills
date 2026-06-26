/**
 * OpenClaw JSONL Parser
 *
 * Parses OpenClaw session JSONL format and emits dashboard events.
 * Key differences from Claude Code format:
 * - Uses 'toolCall' / 'toolResult' instead of 'tool_use' / 'tool_result'
 * - Wraps in message.message.content[] structure
 * - type field at top level: 'message', 'session', 'custom', 'model_change', etc.
 * - message.message.role: 'user', 'assistant', 'toolResult'
 */

import * as path from 'path';

// Dashboard event types sent to the browser
export interface DashboardEvent {
  type: string;
  [key: string]: unknown;
}

/** Format a tool call into a human-readable status string */
function formatToolStatus(toolName: string, args: Record<string, unknown>): string {
  const base = (p: unknown) => (typeof p === 'string' ? path.basename(p) : '');
  switch (toolName) {
    case 'Read':
    case 'read':
      return `Reading ${base(args.file_path || args.path)}`;
    case 'Edit':
    case 'edit':
      return `Editing ${base(args.file_path || args.path)}`;
    case 'Write':
    case 'write':
      return `Writing ${base(args.file_path || args.path)}`;
    case 'exec':
      return `Running command`;
    case 'web_fetch':
      return `Fetching ${typeof args.url === 'string' ? args.url.slice(0, 60) : 'URL'}`;
    case 'browser':
      return `Using browser`;
    case 'sessions_spawn':
      return `Spawning sub-agent`;
    case 'memory_search':
      return `Searching memory`;
    case 'memory_get':
      return `Reading memory`;
    case 'message':
      return `Sending message`;
    case 'image':
      return `Analyzing image`;
    case 'pdf':
      return `Analyzing PDF`;
    case 'tts':
      return `Speaking`;
    default:
      return `Using ${toolName}`;
  }
}

/**
 * Extract a meaningful task description from a user message.
 * OpenClaw wraps user messages in metadata — we strip that to find the actual content.
 */
function extractTaskFromUserMessage(content: unknown): string {
  let text = '';
  if (typeof content === 'string') {
    text = content;
  } else if (Array.isArray(content)) {
    for (const block of content) {
      if (block?.type === 'text' && typeof block.text === 'string') {
        text = block.text;
        break;
      }
    }
  }
  if (!text) return '';

  // Strip OpenClaw conversation metadata wrapper
  // These messages start with "Conversation info (untrusted metadata):" followed by JSON
  // The actual user content is after all the metadata blocks
  let cleaned = text;

  // Strip inter-session message headers
  const interSessionMatch = cleaned.match(/\[Inter-session message\].*?\n.*?\n([\s\S]*)/);
  if (interSessionMatch) {
    cleaned = interSessionMatch[1].trim();
  }

  // Strip "Conversation info" metadata block
  const convMatch = cleaned.match(/Conversation info \(untrusted.*?\n```json\n[\s\S]*?```\n([\s\S]*)/);
  if (convMatch) {
    cleaned = convMatch[1].trim();
  }

  // Strip "Sender" metadata block
  const senderMatch = cleaned.match(/Sender \(untrusted.*?\n```json\n[\s\S]*?```\n([\s\S]*)/);
  if (senderMatch) {
    cleaned = senderMatch[1].trim();
  }

  // Strip chat history block
  const histMatch = cleaned.match(/Chat history.*?\n```json\n[\s\S]*?```\n([\s\S]*)/);
  if (histMatch) {
    cleaned = histMatch[1].trim();
  }

  // Strip @mentions at the start
  cleaned = cleaned.replace(/^@\S+\s*/g, '').trim();

  // Strip untrusted context blocks (both the wrapper line and the content)
  cleaned = cleaned.replace(/Untrusted context \(metadata[^)]*\):\s*/g, '').trim();
  cleaned = cleaned.replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[\s\S]*?<<<END_EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>/g, '').trim();

  // If it's a sessions_send payload, try to get the message body
  try {
    const parsed = JSON.parse(cleaned);
    if (parsed?.messages || parsed?.message) {
      cleaned = parsed.message || '';
    }
  } catch {
    // Not JSON, that's fine
  }

  // Truncate to something reasonable
  if (cleaned.length > 150) {
    cleaned = cleaned.slice(0, 147) + '...';
  }

  return cleaned || '';
}

/** Extract the short tool name for character animation decisions */
export function extractToolName(status: string): string {
  // Reading tools → character reads (looks at screen)
  if (status.startsWith('Reading') || status.startsWith('Searching memory')) {
    return 'read';
  }
  // Everything else → character types
  return 'write';
}

export interface AgentState {
  activeToolIds: Set<string>;
  activeToolStatuses: Map<string, string>;
  activeToolNames: Map<string, string>;
  /** Timestamp when each tool call started */
  activeToolStartMs: Map<string, number>;
  /** Track which tool IDs are sessions_spawn calls (for sub-agent despawn) */
  spawnToolIds: Set<string>;
  isIdle: boolean;
  isStalled: boolean;
  lastActivityMs: number;
  /** Timestamp of last inbound user message */
  lastUserMessageMs: number;
  /** Current task context — extracted from last user message or sessions_spawn task */
  currentTask: string;
  /** Last assistant text message (for chat preview) */
  lastChatMessage: string;
}

/**
 * Parse a single JSONL line from an OpenClaw session file.
 * Returns an array of dashboard events to broadcast (may be empty).
 */
export function parseOpenClawLine(
  agentId: number,
  line: string,
  state: AgentState,
): DashboardEvent[] {
  const events: DashboardEvent[] = [];

  try {
    const record = JSON.parse(line);

    if (record.type === 'message') {
      const msg = record.message;
      if (!msg) return events;

      if (msg.role === 'assistant' && Array.isArray(msg.content)) {
        const blocks = msg.content as Array<{
          type: string;
          id?: string;
          name?: string;
          arguments?: Record<string, unknown>;
        }>;

        const hasToolCall = blocks.some((b) => b.type === 'toolCall');

        // Extract chat text from any assistant message (even ones with tool calls)
        for (const block of blocks) {
          if (block.type === 'text' && typeof (block as Record<string, unknown>).text === 'string') {
            let chatText = ((block as Record<string, unknown>).text as string).trim();
            chatText = chatText.replace(/^\[\[reply_to[^\]]*\]\]\s*/i, '').trim();
            if (chatText.length > 0 && chatText !== 'NO_REPLY' && chatText !== 'HEARTBEAT_OK' && chatText !== 'ANNOUNCE_SKIP' && chatText !== 'REPLY_SKIP') {
              state.lastChatMessage = chatText.length > 2000 ? chatText.slice(0, 1997) + '...' : chatText;
              events.push({ type: 'agentChat', id: agentId, message: state.lastChatMessage });
              break;
            }
          }
        }

        if (hasToolCall) {
          // Agent is active — clear idle state
          if (state.isIdle) {
            state.isIdle = false;
            events.push({ type: 'agentStatus', id: agentId, status: 'active' });
          }

          for (const block of blocks) {
            if (block.type === 'toolCall' && block.id) {
              const toolName = block.name || 'unknown';
              const status = formatToolStatus(toolName, block.arguments || {});

              state.activeToolIds.add(block.id);
              state.activeToolStatuses.set(block.id, status);
              state.activeToolNames.set(block.id, toolName);
              state.activeToolStartMs.set(block.id, Date.now());
              state.lastActivityMs = Date.now();
              state.isStalled = false;

              events.push({
                type: 'agentToolStart',
                id: agentId,
                toolId: block.id,
                status,
              });

              // Detect sub-agent spawns
              if (toolName === 'sessions_spawn') {
                const args = block.arguments || {};
                const label = (args.label as string) || (args.agentId as string) || 'sub-agent';
                const task = (args.task as string) || '';
                state.spawnToolIds.add(block.id);
                events.push({
                  type: 'subagentSpawned',
                  id: agentId,
                  toolId: block.id,
                  label,
                  task: task.slice(0, 200),
                });
              }
            }
          }
        } else if (blocks.some((b) => b.type === 'text')) {
          // Text-only response — agent is thinking/responding
          state.lastActivityMs = Date.now();
          if (state.isIdle) {
            state.isIdle = false;
            events.push({ type: 'agentStatus', id: agentId, status: 'active' });
          }

        }
      } else if (msg.role === 'toolResult') {
        // Tool completed
        const toolCallId = msg.toolCallId;
        if (toolCallId && state.activeToolIds.has(toolCallId)) {
          // Check if this was a sessions_spawn — emit sub-agent despawn
          if (state.spawnToolIds.has(toolCallId)) {
            state.spawnToolIds.delete(toolCallId);
            events.push({
              type: 'subagentDespawned',
              id: agentId,
              toolId: toolCallId,
            });
          }

          state.activeToolIds.delete(toolCallId);
          state.activeToolStatuses.delete(toolCallId);
          state.activeToolNames.delete(toolCallId);
          state.activeToolStartMs.delete(toolCallId);
          state.lastActivityMs = Date.now();
          state.isStalled = false;

          events.push({
            type: 'agentToolDone',
            id: agentId,
            toolId: toolCallId,
          });

          // If all tools done, clear tools
          if (state.activeToolIds.size === 0) {
            events.push({ type: 'agentToolsClear', id: agentId });
          }
        }
      } else if (msg.role === 'user') {
        // New user message — new turn starting
        state.activeToolIds.clear();
        state.activeToolStatuses.clear();
        state.activeToolNames.clear();
        state.activeToolStartMs.clear();
        state.lastActivityMs = Date.now();
        state.isIdle = false;

        // Extract task context from user message
        state.lastUserMessageMs = Date.now();
        const taskText = extractTaskFromUserMessage(msg.content);
        if (taskText) {
          state.currentTask = taskText;
          events.push({ type: 'agentTask', id: agentId, task: taskText });
        }
        events.push({ type: 'userMessage', id: agentId, timestamp: Date.now() });

        events.push({ type: 'agentToolsClear', id: agentId });
        events.push({ type: 'agentStatus', id: agentId, status: 'active' });
      }
    } else if (record.type === 'session') {
      // Session start record
      state.lastActivityMs = Date.now();
      state.isIdle = false;
      events.push({ type: 'agentSessionStart', id: agentId });
      events.push({ type: 'agentStatus', id: agentId, status: 'active' });
    }
  } catch {
    // Ignore malformed lines
  }

  return events;
}
