/**
 * Session Watcher
 *
 * Watches OpenClaw agent session directories for active JSONL files.
 * Tails new lines and feeds them to the parser.
 * Detects new sessions and cleans up completed ones.
 */

import * as fs from 'fs';
import * as path from 'path';

import { type AgentConfig, AGENT_DESPAWN_TIMEOUT_MS, IDLE_TIMEOUT_MS, OPENCLAW_AGENTS_DIR, SESSION_SCAN_INTERVAL_MS, STALLED_TOOL_TIMEOUT_MS, STALLED_AGENT_TIMEOUT_MS } from './config.js';
import { type AgentState, type DashboardEvent, parseOpenClawLine } from './openclawParser.js';

interface WatchedSession {
  agentId: number;
  agentConfig: AgentConfig;
  filePath: string;
  fileOffset: number;
  lineBuffer: string;
  state: AgentState;
  channel: string; // telegram, discord, cron, etc.
  watcher: fs.FSWatcher | null;
  pollTimer: ReturnType<typeof setInterval> | null;
}

export class SessionWatcher {
  private sessions: Map<string, WatchedSession> = new Map();
  private scanTimer: ReturnType<typeof setInterval> | null = null;
  private agents: AgentConfig[];
  private nextAgentId = 0;
  private agentIdMap: Map<string, number> = new Map(); // agentDir → numeric ID
  private despawnedAgents: Set<string> = new Set(); // agentDir of agents that have been despawned
  private onEvent: (event: DashboardEvent) => void;

  constructor(agents: AgentConfig[], onEvent: (event: DashboardEvent) => void) {
    this.agents = agents;
    this.onEvent = onEvent;

    // Pre-assign numeric IDs to known agents
    for (const agent of agents) {
      const id = this.nextAgentId++;
      this.agentIdMap.set(agent.agentDir, id);
    }
  }

  /** Look up the channel for a session JSONL file from sessions.json */
  private getSessionChannel(agent: AgentConfig, sessionId: string): string {
    try {
      const sessionsJsonPath = path.join(OPENCLAW_AGENTS_DIR, agent.agentDir, 'sessions', 'sessions.json');
      if (!fs.existsSync(sessionsJsonPath)) return '';
      const data = JSON.parse(fs.readFileSync(sessionsJsonPath, 'utf-8'));
      for (const [sessionKey, value] of Object.entries(data)) {
        if (typeof value === 'object' && value !== null && (value as Record<string, unknown>).sessionId === sessionId) {
          // Session key format: agent:<name>:<channel>:<type>:<id>
          const parts = sessionKey.split(':');
          return parts.length > 2 ? parts[2] : '';
        }
      }
    } catch {
      // Ignore read errors
    }
    return '';
  }

  /** Start watching all agent session directories */
  start(): void {
    console.log('[SessionWatcher] Starting...');

    // Initial scan
    this.scanAllAgents();

    // Periodic scan for new sessions
    this.scanTimer = setInterval(() => {
      this.scanAllAgents();
      this.checkIdleAgents();
    }, SESSION_SCAN_INTERVAL_MS);
  }

  /** Stop watching everything */
  stop(): void {
    if (this.scanTimer) {
      clearInterval(this.scanTimer);
      this.scanTimer = null;
    }
    for (const session of this.sessions.values()) {
      this.stopWatching(session);
    }
    this.sessions.clear();
  }

  /** Get current state of all agents for initial sync */
  getAgentStates(): Array<{ id: number; config: AgentConfig; isActive: boolean; isStalled: boolean; currentTask: string; channel: string; lastChatMessage: string; tools: Array<{ toolId: string; status: string }> }> {
    const now = Date.now();
    const states: Array<{ id: number; config: AgentConfig; isActive: boolean; isStalled: boolean; currentTask: string; channel: string; lastChatMessage: string; tools: Array<{ toolId: string; status: string }> }> = [];

    for (const agent of this.agents) {
      const id = this.agentIdMap.get(agent.agentDir)!;
      let isActive = false;
      let isStalled = false;
      let currentTask = '';
      let channel = '';
      let lastChatMessage = '';
      const tools: Array<{ toolId: string; status: string }> = [];

      // Find the most recent active session for this agent
      let latestActivity = 0;
      let hasAnySessions = false;
      for (const session of this.sessions.values()) {
        if (session.agentConfig.agentDir === agent.agentDir) {
          hasAnySessions = true;
          // Always prefer a session with a known channel
          if (session.channel && !channel) {
            channel = session.channel;
          }
          if (session.state.lastActivityMs > latestActivity) {
            latestActivity = session.state.lastActivityMs;
            if (session.state.currentTask) {
              currentTask = session.state.currentTask;
            }
            if (session.state.lastChatMessage) {
              lastChatMessage = session.state.lastChatMessage;
            }
            // Prefer channel from the most active session
            if (session.channel) {
              channel = session.channel;
            }
          }
          if (!session.state.isIdle) {
            isActive = true;
            for (const [toolId, status] of session.state.activeToolStatuses) {
              tools.push({ toolId, status });
            }
          }
          if (session.state.isStalled) {
            isStalled = true;
          }
        }
      }

      // Always-present agents with no recent activity are stalled
      if (agent.alwaysPresent && !isActive) {
        if (!hasAnySessions || (latestActivity > 0 && now - latestActivity > STALLED_AGENT_TIMEOUT_MS)) {
          isStalled = true;
        }
      }

      states.push({ id, config: agent, isActive, isStalled, currentTask, channel, lastChatMessage, tools });
    }

    return states;
  }

  private scanAllAgents(): void {
    for (const agent of this.agents) {
      this.scanAgentSessions(agent);
    }
  }

  private scanAgentSessions(agent: AgentConfig): void {
    const sessionsDir = path.join(OPENCLAW_AGENTS_DIR, agent.agentDir, 'sessions');

    try {
      if (!fs.existsSync(sessionsDir)) return;

      const files = fs.readdirSync(sessionsDir)
        .filter(f => f.endsWith('.jsonl') && !f.includes('.deleted.'));

      // Only watch recently modified files (last 5 minutes) to avoid
      // opening watchers on hundreds of old session files
      const recentThreshold = Date.now() - 5 * 60_000;
      const recentFiles: Array<{ file: string; mtime: number }> = [];

      for (const file of files) {
        const filePath = path.join(sessionsDir, file);
        try {
          const stat = fs.statSync(filePath);
          if (stat.mtimeMs > recentThreshold) {
            recentFiles.push({ file: filePath, mtime: stat.mtimeMs });
          }
        } catch {
          // Skip files we can't stat
        }
      }

      // Sort by mtime descending, only watch the most recent few per agent
      recentFiles.sort((a, b) => b.mtime - a.mtime);
      const toWatch = recentFiles.slice(0, 3); // At most 3 recent sessions per agent

      for (const { file } of toWatch) {
        if (!this.sessions.has(file)) {
          this.startWatchingSession(agent, file);
        }
      }

      // Clean up sessions whose files were deleted or are no longer recent
      const activeFiles = new Set(toWatch.map(f => f.file));
      for (const [key, session] of this.sessions) {
        if (session.agentConfig.agentDir === agent.agentDir) {
          if (!fs.existsSync(session.filePath) || !activeFiles.has(key)) {
            // Only remove if the session is idle (don't kill active watchers)
            if (session.state.isIdle || !activeFiles.has(key)) {
              this.stopWatching(session);
              this.sessions.delete(key);
            }
          }
        }
      }
    } catch {
      // Directory may not exist yet — that's fine
    }
  }

  private startWatchingSession(agent: AgentConfig, filePath: string): void {
    const agentId = this.agentIdMap.get(agent.agentDir)!;
    const key = filePath;

    // Extract session ID from filename (UUID.jsonl)
    const sessionId = path.basename(filePath, '.jsonl');
    const channel = this.getSessionChannel(agent, sessionId);
    console.log(`[SessionWatcher] Watching ${agent.displayName}: ${path.basename(filePath)}${channel ? ` (${channel})` : ''}`);

    const session: WatchedSession = {
      agentId,
      agentConfig: agent,
      filePath,
      fileOffset: 0,
      lineBuffer: '',
      channel,
      state: {
        activeToolIds: new Set(),
        activeToolStatuses: new Map(),
        activeToolNames: new Map(),
        activeToolStartMs: new Map(),
        spawnToolIds: new Set(),
        isIdle: true,
        isStalled: false,
        lastActivityMs: 0,
        lastUserMessageMs: 0,
        currentTask: '',
        lastChatMessage: '',
      },
      watcher: null,
      pollTimer: null,
    };

    // Skip to end of file for existing sessions (only process new lines)
    try {
      const stat = fs.statSync(filePath);
      // If file was modified in the last 60 seconds, read from the beginning
      // to catch recent activity. Otherwise skip to end.
      const recentThreshold = Date.now() - 60_000;
      if (stat.mtimeMs > recentThreshold) {
        // Read recent file from beginning to reconstruct state
        session.fileOffset = 0;
      } else {
        session.fileOffset = stat.size;
      }
    } catch {
      // File may have been just created
    }

    // Set up file watching
    try {
      session.watcher = fs.watch(filePath, () => {
        this.readNewLines(session);
      });
    } catch (err) {
      console.log(`[SessionWatcher] fs.watch failed for ${path.basename(filePath)}: ${err}`);
    }

    // Polling fallback (more reliable on some systems)
    session.pollTimer = setInterval(() => {
      this.readNewLines(session);
    }, 1000);

    this.sessions.set(key, session);

    // Do initial read
    this.readNewLines(session);

    // If the agent is "always present", emit creation event
    if (agent.alwaysPresent) {
      this.onEvent({ type: 'agentCreated', id: agentId, name: agent.displayName, emoji: agent.emoji });
    }
  }

  private readNewLines(session: WatchedSession): void {
    try {
      const stat = fs.statSync(session.filePath);
      if (stat.size <= session.fileOffset) return;

      const buf = Buffer.alloc(stat.size - session.fileOffset);
      const fd = fs.openSync(session.filePath, 'r');
      fs.readSync(fd, buf, 0, buf.length, session.fileOffset);
      fs.closeSync(fd);
      session.fileOffset = stat.size;

      const text = session.lineBuffer + buf.toString('utf-8');
      const lines = text.split('\n');
      session.lineBuffer = lines.pop() || '';

      for (const line of lines) {
        if (!line.trim()) continue;
        const events = parseOpenClawLine(session.agentId, line, session.state);
        for (const event of events) {
          this.onEvent(event);
        }
      }
    } catch {
      // File may be in the process of being written
    }
  }

  private checkIdleAgents(): void {
    const now = Date.now();
    for (const session of this.sessions.values()) {
      // Check for idle (no activity for 30s)
      if (
        !session.state.isIdle &&
        session.state.lastActivityMs > 0 &&
        now - session.state.lastActivityMs > IDLE_TIMEOUT_MS
      ) {
        session.state.isIdle = true;

        // Despawn any remaining sub-agents
        for (const toolId of session.state.spawnToolIds) {
          this.onEvent({ type: 'subagentDespawned', id: session.agentId, toolId });
        }
        session.state.spawnToolIds.clear();

        session.state.activeToolIds.clear();
        session.state.activeToolStatuses.clear();
        session.state.activeToolNames.clear();
        session.state.activeToolStartMs.clear();
        this.onEvent({ type: 'agentToolsClear', id: session.agentId });
        this.onEvent({ type: 'agentStatus', id: session.agentId, status: 'waiting' });
      }

      // Check for stalled tool calls (running > 5 min without completing)
      if (!session.state.isStalled) {
        for (const [toolId, startMs] of session.state.activeToolStartMs) {
          if (now - startMs > STALLED_TOOL_TIMEOUT_MS) {
            session.state.isStalled = true;
            this.onEvent({ type: 'agentStatus', id: session.agentId, status: 'stalled' });
            break;
          }
        }
      }
    }

    // Check for stalled always-present agents (no recent session activity at all)
    for (const agent of this.agents) {
      if (!agent.alwaysPresent) continue;
      const agentId = this.agentIdMap.get(agent.agentDir)!;

      // Find the most recent activity across all sessions for this agent
      let latestActivity = 0;
      let hasAnySessions = false;
      for (const session of this.sessions.values()) {
        if (session.agentConfig.agentDir === agent.agentDir) {
          hasAnySessions = true;
          if (session.state.lastActivityMs > latestActivity) {
            latestActivity = session.state.lastActivityMs;
          }
        }
      }

      // If no sessions at all, or last activity was > 10 min ago → stalled
      if (!hasAnySessions || (latestActivity > 0 && now - latestActivity > STALLED_AGENT_TIMEOUT_MS)) {
        // Only emit if not already known as stalled
        const alreadyStalled = Array.from(this.sessions.values()).some(
          s => s.agentConfig.agentDir === agent.agentDir && s.state.isStalled
        );
        if (!alreadyStalled) {
          this.onEvent({ type: 'agentStatus', id: agentId, status: 'stalled' });
        }
      }
    }

    // Despawn non-always-present agents that have been idle too long
    for (const agent of this.agents) {
      if (agent.alwaysPresent) continue;
      const agentId = this.agentIdMap.get(agent.agentDir)!;

      // Check if all sessions for this agent are idle and beyond despawn threshold
      let allIdle = true;
      let latestActivity = 0;
      let hasAnySessions = false;
      for (const session of this.sessions.values()) {
        if (session.agentConfig.agentDir === agent.agentDir) {
          hasAnySessions = true;
          if (!session.state.isIdle) {
            allIdle = false;
            // Agent is active — clear despawned flag
            this.despawnedAgents.delete(agent.agentDir);
            break;
          }
          if (session.state.lastActivityMs > latestActivity) {
            latestActivity = session.state.lastActivityMs;
          }
        }
      }

      if (allIdle && hasAnySessions && latestActivity > 0 &&
          now - latestActivity > AGENT_DESPAWN_TIMEOUT_MS &&
          !this.despawnedAgents.has(agent.agentDir)) {
        this.despawnedAgents.add(agent.agentDir);
        this.onEvent({ type: 'agentDespawn', id: agentId });
      }
    }
  }

  private stopWatching(session: WatchedSession): void {
    if (session.watcher) {
      session.watcher.close();
      session.watcher = null;
    }
    if (session.pollTimer) {
      clearInterval(session.pollTimer);
      session.pollTimer = null;
    }
    try {
      fs.unwatchFile(session.filePath);
    } catch {
      // ignore
    }
  }
}
