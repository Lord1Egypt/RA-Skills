import {
  ActivityHandler,
  BotFrameworkAdapter,
  ConversationReference,
  TurnContext,
  TeamsInfo,
  ActivityTypes,
} from "botbuilder";
import express from "express";
import bodyParser from "body-parser";
import http from "http";
import { SessionManager } from "./session";
import { GatewayAPI, Logger, PluginConfig } from "./types";

// Cache Graph token to avoid fetching on every message
let graphTokenCache: { token: string; expiresAt: number } | null = null;

async function getGraphToken(appId: string, appPassword: string, tenantId: string): Promise<string | null> {
  const now = Date.now();
  if (graphTokenCache && graphTokenCache.expiresAt > now + 60000) {
    return graphTokenCache.token;
  }
  try {
    const fetch = require("node-fetch");
    const resp = await fetch(
      `https://login.microsoftonline.com/${tenantId}/oauth2/v2.0/token`,
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: appId,
          client_secret: appPassword,
          scope: "https://graph.microsoft.com/.default",
          grant_type: "client_credentials",
        }).toString(),
      }
    );
    if (!resp.ok) return null;
    const data = await resp.json();
    graphTokenCache = {
      token: data.access_token,
      expiresAt: now + (data.expires_in ?? 3600) * 1000,
    };
    return graphTokenCache.token;
  } catch {
    return null;
  }
}

async function fetchWithGraphToken(
  url: string,
  appId: string,
  appPassword: string,
  tenantId: string
): Promise<Buffer | null> {
  const fetch = require("node-fetch");
  // First try without auth (works for some public CDN URLs)
  try {
    const resp = await fetch(url);
    if (resp.ok) return await resp.buffer();
  } catch { /* fall through */ }

  // Try with Graph token
  const token = await getGraphToken(appId, appPassword, tenantId);
  if (!token) return null;
  try {
    const resp = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (resp.ok) return await resp.buffer();
  } catch { /* fall through */ }

  return null;
}

/**
 * Express HTTP server that exposes the Bot Framework messaging endpoint.
 */
export class BotServer {
  private app: express.Application;
  private server: http.Server | null = null;
  private adapter: BotFrameworkAdapter;
  private bot: OpenClawTeamsBot;

  constructor(
    private config: PluginConfig,
    private sessionManager: SessionManager,
    private gateway: GatewayAPI,
    private logger: Logger,
  ) {
    this.adapter = new BotFrameworkAdapter({
      appId: config.appId,
      appPassword: config.appPassword,
      channelAuthTenant: config.appTenantId,
    });

    // Global error handler - log and notify the user when something breaks.
    this.adapter.onTurnError = async (context: TurnContext, error: Error) => {
      this.logger.error(`Bot turn error: ${error.message}`, error);
      try {
        await context.sendActivity(
          "An error occurred. Please try again.",
        );
      } catch (sendErr) {
        this.logger.error(
          `Failed to send error message to Teams: ${(sendErr as Error).message}`,
        );
      }
    };

    this.bot = new OpenClawTeamsBot(
      this.sessionManager,
      this.gateway,
      this.adapter,
      this.logger,
      this.config,
    );

    this.app = express();
    this.app.use(bodyParser.json());

    // Bot Framework webhook endpoint
    this.app.post("/api/messages", (req, res) => {
      this.adapter.processActivity(req, res, async (context) => {
        await this.bot.run(context);
      });
    });

    // Health-check endpoint
    this.app.get("/health", (_req, res) => {
      res.json({ status: "ok", plugin: "openclaw-teams-elvatis" });
    });
  }

  /**
   * Start listening for incoming Bot Framework requests.
   */
  async start(): Promise<void> {
    const port = this.config.port ?? 3978;
    return new Promise((resolve, reject) => {
      this.server = this.app
        .listen(port, () => {
          this.logger.info(
            `Teams bot server listening on port ${port}`,
          );
          resolve();
        })
        .on("error", (err) => {
          this.logger.error(`Failed to start bot server: ${err.message}`);
          reject(err);
        });
    });
  }

  /**
   * Gracefully shut down the HTTP server.
   */
  async stop(): Promise<void> {
    if (!this.server) return;
    return new Promise((resolve, reject) => {
      this.server!.close((err) => {
        if (err) {
          this.logger.error(`Error stopping bot server: ${err.message}`);
          reject(err);
        } else {
          this.logger.info("Teams bot server stopped");
          resolve();
        }
      });
    });
  }
}

/**
 * Core Teams bot that bridges messages between Teams and OpenClaw Gateway.
 */
class OpenClawTeamsBot extends ActivityHandler {
  constructor(
    private sessionManager: SessionManager,
    private gateway: GatewayAPI,
    private adapter: BotFrameworkAdapter,
    private logger: Logger,
    private config: PluginConfig,
  ) {
    super();

    // Handle incoming messages
    this.onMessage(async (context: TurnContext, next) => {
      await this.handleIncomingMessage(context);
      await next();
    });

    // Handle new members joining the conversation (welcome message)
    this.onMembersAdded(async (context: TurnContext, next) => {
      const membersAdded = context.activity.membersAdded ?? [];
      for (const member of membersAdded) {
        if (member.id !== context.activity.recipient.id) {
          await context.sendActivity(
            "Hello! I am the Elvatis AI assistant. Send me a message to get started.",
          );
        }
      }
      await next();
    });
  }

  /**
   * Process an incoming Teams message:
   * 1. Resolve the channel and session
   * 2. Forward the message text to OpenClaw
   * 3. Send the gateway response back to Teams
   */
  private async handleIncomingMessage(context: TurnContext): Promise<void> {
    const text = context.activity.text?.trim() ?? "";
    const attachments = context.activity.attachments ?? [];

    // Collect and describe all attachments
    const attachmentParts: string[] = [];
    const appId = this.config.appId ?? "";
    const appPassword = this.config.appPassword ?? "";
    const tenantId = this.config.appTenantId ?? "";

    // DEBUG: log full attachment structure
    if (attachments.length > 0) {
      this.logger.info(`[teams:debug] ${attachments.length} attachment(s):`);
      for (const a of attachments) {
        this.logger.info(`[teams:debug]  type=${a.contentType} name=${a.name} url=${a.contentUrl ?? "(none)"}`);
        if (a.content) {
          const raw = typeof a.content === "string" ? a.content : JSON.stringify(a.content);
          this.logger.info(`[teams:debug]  content(500)=${raw.slice(0, 500)}`);
        }
      }
    }

    for (const att of attachments) {
      const contentType = att.contentType ?? "";
      const name = att.name ?? "unnamed";

      // Helper: fetch URL with Graph token fallback
      const fetchBuffer = (url: string) =>
        fetchWithGraphToken(url, appId, appPassword, tenantId);

      // Images -  Teams inline images need the Bot's own OAuth token
      if (contentType.startsWith("image/") && att.contentUrl) {
        let buffer: Buffer | null = null;

        // Get Bot Framework connector token via MicrosoftAppCredentials
        try {
          const fetch = require("node-fetch");
          const { MicrosoftAppCredentials } = require("botframework-connector");
          const creds = new MicrosoftAppCredentials(appId, appPassword, tenantId);
          const botToken = await creds.getToken();

          if (botToken) {
            const resp = await fetch(att.contentUrl, {
              headers: { Authorization: `Bearer ${botToken}` },
            });
            if (resp.ok) {
              buffer = await resp.buffer();
              this.logger.debug(`Fetched inline image via Bot token: ${name}`);
            } else {
              this.logger.warn(`Bot token fetch failed (${resp.status}) for: ${name}`);
            }
          }
        } catch (err: any) {
          this.logger.warn(`Bot token fetch error: ${err.message}`);
        }

        // Fall back to Graph API token
        if (!buffer) buffer = await fetchBuffer(att.contentUrl);

        if (buffer) {
          // Save to plugin-local tmp/ folder and clean up after use
          try {
            const path = require("path");
            const fs = require("fs");
            // Use __dirname which resolves to the plugin root directory at runtime
            const pluginDir = __dirname;
            const tmpDir = path.join(pluginDir, "tmp");
            if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir, { recursive: true });
            const ext = contentType.split("/")[1]?.split(";")[0] ?? "png";
            const tmpPath = path.join(tmpDir, `img-${Date.now()}.${ext}`);
            fs.writeFileSync(tmpPath, buffer);
            const sizeKb = Math.round(buffer.length / 1024);
            // Inline small images as base64 for vision; large ones as file path
            const base64 = buffer.toString("base64");
            const mimeInline = contentType.startsWith("image/") ? contentType : "image/png";
            if (buffer.length < 900 * 1024) {
              attachmentParts.push(`[Image: ${name} (${sizeKb}KB)]\ndata:${mimeInline};base64,${base64}`);
            } else {
              attachmentParts.push(`[Image: ${name} (${sizeKb}KB) saved to ${tmpPath} -  please read and analyse this image file using the read tool, then delete it]`);
            }
            this.logger.debug(`Image saved: ${tmpPath} (${sizeKb}KB)`);
            // Schedule cleanup after 5 minutes
            setTimeout(() => {
              try { fs.unlinkSync(tmpPath); } catch { /* already gone */ }
            }, 5 * 60 * 1000);
          } catch (err: any) {
            // Fallback to inline base64
            const base64 = buffer.toString("base64");
            const sizeKb = Math.round(buffer.length / 1024);
            attachmentParts.push(`[Image: ${name} (${contentType}, ${sizeKb}KB)]\ndata:${contentType};base64,${base64}`);
          }
        } else {
          // Inline screenshots cannot be fetched due to Teams CDN auth restrictions
          // Prompt user to attach as file instead
          attachmentParts.push(`[Note: The inline image "${name}" could not be loaded (Teams CDN authentication required). Please attach it as a file using the paperclip icon instead of pasting -  file attachments work perfectly.]`);
        }
      }

      // Audio files
      else if (contentType.startsWith("audio/") && att.contentUrl) {
        attachmentParts.push(`[Audio file: ${name} (${contentType})]`);
      }

      // Video files
      else if (contentType.startsWith("video/") && att.contentUrl) {
        attachmentParts.push(`[Video file: ${name} (${contentType})]`);
      }

      // Text and PDF documents
      else if ((contentType === "application/pdf" || contentType.startsWith("text/")) && att.contentUrl) {
        const buffer = await fetchBuffer(att.contentUrl);
        if (buffer) {
          const sizeKb = Math.round(buffer.length / 1024);
          if (contentType.startsWith("text/")) {
            const content = buffer.toString("utf8").slice(0, 8000);
            attachmentParts.push(`[Text file: ${name} (${sizeKb}KB)]\n${content}`);
          } else {
            attachmentParts.push(`[PDF: ${name} (${sizeKb}KB)]`);
          }
        }
      }

      // Teams SharePoint/OneDrive file
      else if (contentType === "application/vnd.microsoft.teams.file.download.info") {
        const fileInfo = att.content as Record<string, string> | undefined;
        const downloadUrl = fileInfo?.["downloadUrl"];
        const url = downloadUrl ?? att.contentUrl;
        if (url) {
          // downloadUrl contains tempauth token -  fetch directly without extra auth
          let buffer: Buffer | null = null;
          try {
            const fetch = require("node-fetch");
            const resp = await fetch(url); // no auth header needed, tempauth is in URL
            if (resp.ok) {
              buffer = await resp.buffer();
              this.logger.debug(`[teams] Direct fetch OK: ${name} (${buffer?.length} bytes)`);
            } else {
              this.logger.warn(`[teams] Direct fetch failed (${resp.status}), trying Graph token`);
              buffer = await fetchBuffer(url);
            }
          } catch (err: any) {
            this.logger.warn(`[teams] Direct fetch error: ${err.message}`);
            buffer = await fetchBuffer(url);
          }
          if (buffer) {
            const sizeKb = Math.round(buffer.length / 1024);
            const isText = name.match(/\.(txt|md|csv|json|xml|yaml|yml|log|ts|js|py|sh)$/i);
            const isImg = name.match(/\.(png|jpg|jpeg|gif|webp|bmp)$/i);
            if (isText) {
              const content = buffer.toString("utf8").slice(0, 8000);
              attachmentParts.push(`[File: ${name} (${sizeKb}KB)]\n${content}`);
            } else if (isImg) {
              const _path = require("path");
              const _fs = require("fs");
              const pluginDir2 = __dirname;
              const tmpDir2 = _path.join(pluginDir2, "tmp");
              if (!_fs.existsSync(tmpDir2)) _fs.mkdirSync(tmpDir2, { recursive: true });
              const ext2 = name.split(".").pop() ?? "png";
              const tmpPath2 = _path.join(tmpDir2, `img-${Date.now()}.${ext2}`);
              _fs.writeFileSync(tmpPath2, buffer);
              const base64_2 = buffer.toString("base64");
              const mimeInline2 = "image/" + (ext2 === "jpg" ? "jpeg" : ext2);
              if (buffer.length < 900 * 1024) {
                attachmentParts.push(`[Image: ${name} (${sizeKb}KB)]\ndata:${mimeInline2};base64,${base64_2}`);
              } else {
                attachmentParts.push(`[Image: ${name} (${sizeKb}KB) saved to ${tmpPath2} -  please read and analyse this image file using the read tool, then delete it]`);
              }
              setTimeout(() => { try { _fs.unlinkSync(tmpPath2); } catch { /* gone */ } }, 5 * 60 * 1000);
            } else {
              attachmentParts.push(`[File: ${name} (${sizeKb}KB)]`);
            }
          } else {
            attachmentParts.push(`[File: ${name} -  could not fetch]`);
          }
        }
      }

      // text/html attachments -  Teams sends channel images in this format
      // The HTML contains an <img> tag with a URL that requires Bot Connector auth
      else if (contentType === "text/html" && att.content) {
        const html = typeof att.content === "string" ? att.content : JSON.stringify(att.content);
        this.logger.debug(`[teams] HTML attachment content: ${html.slice(0, 500)}`);

        // Extract all image src URLs
        const srcRegex = /src=["']([^"']+)["']/gi;
        const urls: string[] = [];
        let m: RegExpExecArray | null;
        while ((m = srcRegex.exec(html)) !== null) {
          if (m[1].startsWith("http")) urls.push(m[1]);
        }

        let handled = false;
        for (const url of urls) {
          // Try Bot Connector token first
          let buffer: Buffer | null = null;
          try {
            const fetch = require("node-fetch");
            const { MicrosoftAppCredentials } = require("botframework-connector");
            const creds = new MicrosoftAppCredentials(appId, appPassword, tenantId);
            const botToken = await creds.getToken();
            if (botToken) {
              const resp = await fetch(url, { headers: { Authorization: `Bearer ${botToken}` } });
              if (resp.ok) buffer = await resp.buffer();
            }
          } catch { /* fall through */ }

          // Fall back to Graph token
          if (!buffer) buffer = await fetchWithGraphToken(url, appId, appPassword, tenantId);

          if (buffer && buffer.length > 1000) { // skip tiny/empty responses
            const _path = require("path");
            const _fs = require("fs");
            const tmpDir3 = _path.join(__dirname, "tmp");
            if (!_fs.existsSync(tmpDir3)) _fs.mkdirSync(tmpDir3, { recursive: true });
            const tmpPath3 = _path.join(tmpDir3, `img-${Date.now()}.png`);
            _fs.writeFileSync(tmpPath3, buffer);
            const sizeKb = Math.round(buffer.length / 1024);
            const base64_3 = buffer.toString("base64");
            if (buffer.length < 900 * 1024) {
              attachmentParts.push(`[Image: ${name} (${sizeKb}KB)]\ndata:image/png;base64,${base64_3}`);
            } else {
              attachmentParts.push(`[Image: ${name} (${sizeKb}KB) saved to ${tmpPath3} -  please read and analyse this image file using the read tool, then delete it]`);
            }
            setTimeout(() => { try { _fs.unlinkSync(tmpPath3); } catch { /* gone */ } }, 5 * 60 * 1000);
            handled = true;
            this.logger.info(`[teams] Fetched HTML-embedded image: ${tmpPath3} (${sizeKb}KB)`);
            break;
          }
        }
        if (!handled) {
          // Log the URLs we tried so we can debug
          this.logger.warn(`[teams] Could not fetch image from HTML attachment. URLs tried: ${urls.join(", ").slice(0, 200)}`);
          attachmentParts.push(`[Image attachment received but could not be loaded (Teams CDN auth). Please share as a direct file attachment via the paperclip icon, or drag the image file directly into the chat.]`);
        }
      }

      // Everything else
      else if (att.contentUrl || att.content) {
        attachmentParts.push(`[Attachment: ${name} (${contentType || "unknown type"})]`);
      }
    }

    // Combine text + attachments
    const fullText = [text, ...attachmentParts].filter(Boolean).join("\n");
    if (!fullText) return;

    const channelId = this.resolveChannelId(context);
    const channelName = await this.resolveChannelName(context, channelId);
    const senderName = this.resolveSenderName(context);

    this.logger.debug(
      `Received message from "${senderName}" in channel "${channelName}": ${fullText.substring(0, 100)}`,
    );

    // Build a conversation reference so we can reply proactively later
    const conversationReference = TurnContext.getConversationReference(
      context.activity,
    ) as Partial<ConversationReference>;

    try {
      // Ensure we have a session for this channel
      const session = await this.sessionManager.ensureSession(
        channelId,
        channelName,
        conversationReference,
      );

      // Show typing indicator while waiting for the gateway response
      await context.sendActivity({ type: ActivityTypes.Typing });

      // Forward to OpenClaw Gateway
      const response = await this.gateway.sendMessage({
        sessionId: session.sessionId,
        text: fullText,
        sender: senderName,
        metadata: {
          source: "teams",
          channelId,
          channelName,
          senderName,
        },
      });

      // Send the response back to Teams
      // Teams has a ~28KB message limit -  split long responses into chunks
      if (response.text) {
        const MAX_CHARS = 20000;
        const text = response.text;
        if (text.length <= MAX_CHARS) {
          await context.sendActivity(text);
        } else {
          // Split at paragraph boundaries
          const chunks: string[] = [];
          let remaining = text;
          while (remaining.length > 0) {
            if (remaining.length <= MAX_CHARS) {
              chunks.push(remaining);
              break;
            }
            // Find last newline before limit
            let cutAt = remaining.lastIndexOf("\n", MAX_CHARS);
            if (cutAt < MAX_CHARS / 2) cutAt = MAX_CHARS; // fallback to hard cut
            chunks.push(remaining.slice(0, cutAt));
            remaining = remaining.slice(cutAt).trimStart();
          }
          for (let i = 0; i < chunks.length; i++) {
            const part = chunks.length > 1 ? `*(${i + 1}/${chunks.length})*\n${chunks[i]}` : chunks[i];
            await context.sendActivity(part);
            if (i < chunks.length - 1) await new Promise(r => setTimeout(r, 500));
          }
        }
      }
    } catch (err) {
      const error = err as Error;
      this.logger.error(
        `Error processing message in channel "${channelName}": ${error.message}`,
        error,
      );
      await context.sendActivity(
        "Sorry, I could not process your message. Please try again.",
      );
    }
  }

  /**
   * Extract the channel ID from the turn context.
   * Falls back to conversation ID for 1:1 chats.
   */
  private resolveChannelId(context: TurnContext): string {
    const channelData = context.activity.channelData as
      | Record<string, unknown>
      | undefined;

    // Teams channel conversations include teamsChannelId in channelData
    if (channelData?.channel && typeof channelData.channel === "object") {
      const channel = channelData.channel as Record<string, string>;
      if (channel.id) return channel.id;
    }

    // Fallback: use the conversation ID (covers 1:1 and group chats)
    return context.activity.conversation?.id ?? "unknown";
  }

  /**
   * Resolve a human-readable channel name.
   * Attempts to fetch via TeamsInfo; falls back to channelData or a default.
   */
  private async resolveChannelName(
    context: TurnContext,
    channelId: string,
  ): Promise<string> {
    // Try to get channel name from channelData first (faster, no API call)
    const channelData = context.activity.channelData as
      | Record<string, unknown>
      | undefined;

    if (channelData?.channel && typeof channelData.channel === "object") {
      const channel = channelData.channel as Record<string, string>;
      if (channel.name) return channel.name;
    }

    // Attempt to resolve via Teams API
    try {
      const channels = await TeamsInfo.getTeamChannels(context);
      const match = channels.find((ch) => ch.id === channelId);
      if (match?.name) return match.name;
    } catch {
      // TeamsInfo calls can fail in 1:1 chats - that's expected
    }

    // For 1:1 chats, use "Direct" as the channel name
    if (context.activity.conversation?.conversationType === "personal") {
      return "Direct";
    }

    return "General";
  }

  /**
   * Get the display name of the message sender.
   */
  private resolveSenderName(context: TurnContext): string {
    return context.activity.from?.name ?? "Unknown";
  }
}
