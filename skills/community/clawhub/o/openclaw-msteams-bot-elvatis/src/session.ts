import { ConversationReference } from "botbuilder";
import {
  SessionEntry,
  TeamsChannelConfig,
  GatewayAPI,
  Logger,
} from "./types";

/**
 * Manages the mapping between Teams channels and OpenClaw sessions.
 * Each Teams channel gets its own OpenClaw session with optional
 * per-channel system prompts and model overrides.
 */
export class SessionManager {
  private sessions: Map<string, SessionEntry> = new Map();

  constructor(
    private gateway: GatewayAPI,
    private logger: Logger,
    private channelConfigs: Record<string, TeamsChannelConfig>,
  ) {}

  /**
   * Derive a stable session ID from the Teams channel identifier.
   */
  private buildSessionId(channelId: string): string {
    return `teams-${channelId}`;
  }

  /**
   * Look up channel config by channel name first, then by channel ID.
   * This allows users to configure by human-readable name or raw ID.
   */
  private resolveChannelConfig(
    channelId: string,
    channelName: string,
  ): TeamsChannelConfig | undefined {
    return this.channelConfigs[channelName] ?? this.channelConfigs[channelId];
  }

  /**
   * Ensure a session exists for the given Teams channel.
   * Creates a new OpenClaw session on first contact; updates the
   * conversation reference on subsequent messages so replies always
   * target the latest context.
   */
  async ensureSession(
    channelId: string,
    channelName: string,
    conversationReference: Partial<ConversationReference>,
  ): Promise<SessionEntry> {
    const existing = this.sessions.get(channelId);

    if (existing) {
      // Always keep the conversation reference up-to-date so the bot
      // can reply even after Teams recycles infrastructure.
      existing.conversationReference = conversationReference;
      return existing;
    }

    const config = this.resolveChannelConfig(channelId, channelName);
    const sessionId = this.buildSessionId(channelId);
    const label = config?.label ?? `teams-${channelName}`;

    // Register the session with the OpenClaw gateway
    const hasSession = await this.gateway.hasSession(sessionId);
    if (!hasSession) {
      await this.gateway.createSession({
        id: sessionId,
        label,
        systemPrompt: config?.systemPrompt,
        model: config?.model,
        metadata: {
          source: "teams",
          channelId,
          channelName,
        },
      });
      this.logger.info(
        `Created OpenClaw session "${sessionId}" for Teams channel "${channelName}"`,
      );
    }

    const entry: SessionEntry = {
      sessionId,
      channelId,
      channelName,
      label,
      model: config?.model,
      systemPrompt: config?.systemPrompt,
      conversationReference,
    };

    this.sessions.set(channelId, entry);
    return entry;
  }

  /**
   * Retrieve a session by channel ID (if it exists).
   */
  getSession(channelId: string): SessionEntry | undefined {
    return this.sessions.get(channelId);
  }

  /**
   * Remove all tracked sessions (used during plugin shutdown).
   */
  clear(): void {
    this.sessions.clear();
  }
}
