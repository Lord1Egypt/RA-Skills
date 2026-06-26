import { BotServer } from "./bot";
import { SessionManager } from "./session";
import { PluginConfig, GatewayAPI, InboundMessage, GatewayResponse } from "./types";
import WebSocket from "ws";

/**
 * OpenClaw Plugin API interface (as provided by the gateway).
 */
interface OpenClawPluginApi {
  id: string;
  logger: {
    info(msg: string, ...args: unknown[]): void;
    warn(msg: string, ...args: unknown[]): void;
    error(msg: string, ...args: unknown[]): void;
    debug(msg: string, ...args: unknown[]): void;
  };
  pluginConfig: unknown;
  registerService?: (service: { id: string; start(): Promise<void>; stop(): Promise<void> }) => void;
}

/**
 * Send a message to the OpenClaw Gateway via WebSocket and wait for the final response.
 * Supports text and image attachments (base64 data URLs) for Vision.
 */
async function sendViaWebSocket(
  text: string,
  sessionId: string,
  gatewayToken: string,
  logger: OpenClawPluginApi["logger"],
  timeoutMs = 180000,
): Promise<string> {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://127.0.0.1:18789", {
      headers: { Authorization: `Bearer ${gatewayToken}` },
    });

    const timer = setTimeout(() => {
      ws.close();
      reject(new Error("WebSocket agent timeout"));
    }, timeoutMs);

    let resolved = false;

    function done(result: string) {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);
      ws.close();
      resolve(result);
    }

    const msgId = `teams-msg-${Date.now()}`;

    ws.on("open", () => {
      // Authenticate first
      ws.send(JSON.stringify({
        id: `auth-${Date.now()}`,
        method: "auth.token",
        params: { token: gatewayToken },
      }));
    });

    ws.on("message", (raw: Buffer) => {
      try {
        const msg = JSON.parse(raw.toString());

        // After auth, send the agent run request
        if (msg.method === "auth.token" && msg.result?.ok) {
          ws.send(JSON.stringify({
            id: msgId,
            method: "agent.run",
            params: {
              sessionId,
              message: text,
              stream: false,
            },
          }));
          return;
        }

        // Wait for our request to complete
        if (msg.id === msgId) {
          const responseText = msg.result?.payloads?.[0]?.text
            ?? msg.result?.text
            ?? msg.error?.message
            ?? "No response received.";
          done(responseText);
        }

        // Also handle streaming/push events
        if (msg.method === "agent.message" && msg.params?.sessionId === sessionId) {
          const t = msg.params?.text;
          if (t && msg.params?.final) done(t);
        }
      } catch { /* ignore parse errors */ }
    });

    ws.on("error", (err) => {
      logger.warn(`[teams] WebSocket error: ${err.message}`);
      reject(err);
    });

    ws.on("close", () => {
      if (!resolved) reject(new Error("WebSocket closed before response"));
    });
  });
}

/**
 * Build a GatewayAPI implementation.
 */
function buildGateway(logger: OpenClawPluginApi["logger"], gatewayToken: string): GatewayAPI {
  const OPENCLAW_BIN = process.env.OPENCLAW_BIN || "/usr/local/bin/openclaw";

  async function sendToAgent(text: string, sessionId?: string, timeoutMs = 180000): Promise<string> {
    const safeId = sessionId ?? "teams-default";

    // Try WebSocket first (supports vision via data URLs in text)
    try {
      logger.debug(`[teams] Sending via WebSocket to session ${safeId}`);
      const result = await sendViaWebSocket(text, safeId, gatewayToken, logger, timeoutMs);
      logger.debug(`[teams] WebSocket response received (${result.length} chars)`);
      return result;
    } catch (wsErr: any) {
      logger.warn(`[teams] WebSocket failed: ${wsErr.message} - falling back to CLI`);
    }

    // Fallback: openclaw agent CLI (no vision support but reliable for text)
    try {
      const { execFile } = require("child_process");
      const { promisify } = require("util");
      const execFileAsync = promisify(execFile);

      const args = [
        "agent",
        "--message", text,
        "--json",
        "--timeout", String(Math.floor(timeoutMs / 1000)),
        "--session-id", safeId,
      ];

      logger.debug(`[teams] CLI fallback: openclaw agent`);

      let stdout = "";
      try {
        const r = await execFileAsync(OPENCLAW_BIN, args, {
          timeout: timeoutMs + 5000,
          env: { ...process.env, HOME: "/home/elvatis-agent" },
        });
        stdout = r.stdout;
      } catch (execErr: any) {
        stdout = execErr.stdout ?? "";
        if (!stdout.trim()) throw execErr;
      }

      try {
        const result = JSON.parse(stdout.trim());
        const t = result?.result?.payloads?.[0]?.text ?? result?.text;
        if (t) return t;
      } catch { /* not JSON */ }

      return stdout.trim() || "No response received.";
    } catch (err: any) {
      logger.error(`[teams] CLI fallback also failed: ${err.message}`);
      return "An error occurred. Please try again.";
    }
  }

  return {
    async hasSession(_sessionId: string): Promise<boolean> {
      return true;
    },
    async createSession(_params: any): Promise<void> {
      // auto-managed by gateway
    },
    async sendMessage(message: InboundMessage): Promise<GatewayResponse> {
      const context = message.sender
        ? `[Teams/${message.metadata?.channelName ?? "General"} from ${message.sender}]: ${message.text}`
        : message.text;

      const rawId = message.sessionId ?? "default";
      const safeId = "teams-" + rawId.replace(/[^a-zA-Z0-9]/g, "").slice(0, 40);

      const text = await sendToAgent(context, safeId);
      return { text, sessionId: message.sessionId };
    },
  };
}

export default {
  id: "openclaw-teams-elvatis",
  name: "OpenClaw Teams Connector (Elvatis)",
  version: "0.1.2",

  register(api: OpenClawPluginApi): void {
    const config = api.pluginConfig as PluginConfig;
    const logger = api.logger;

    if (config?.enabled === false) {
      logger.info("[teams] Plugin disabled - skipping startup");
      return;
    }

    if (!config?.appId || !config?.appPassword) {
      logger.error("[teams] Missing appId or appPassword in plugin config");
      return;
    }

    logger.info("[teams] Registering Teams connector service...");

    // Read gateway token from config file
    let gatewayToken = "";
    try {
      const fs = require("fs");
      const cfg = JSON.parse(fs.readFileSync("/home/elvatis-agent/.openclaw/openclaw.json", "utf8"));
      gatewayToken = cfg?.gateway?.auth?.token ?? "";
    } catch { /* fallback: no token */ }

    const gateway = buildGateway(logger, gatewayToken);
    let botServer: BotServer | null = null;
    let sessionManager: SessionManager | null = null;

    if (typeof api.registerService === "function") {
      api.registerService({
        id: "openclaw-teams-bot",
        async start() {
          sessionManager = new SessionManager(gateway, logger as any, config.channels ?? {});
          botServer = new BotServer(config, sessionManager, gateway, logger as any);
          await botServer.start();
          const channelCount = Object.keys(config.channels ?? {}).length;
          logger.info(`[teams] Teams bot ready - ${channelCount} channel(s) configured`);
        },
        async stop() {
          if (botServer) { await botServer.stop(); botServer = null; }
          if (sessionManager) { sessionManager.clear(); sessionManager = null; }
        },
      });
    } else {
      Promise.resolve().then(async () => {
        try {
          sessionManager = new SessionManager(gateway, logger as any, config.channels ?? {});
          botServer = new BotServer(config, sessionManager, gateway, logger as any);
          await botServer.start();
          logger.info(`[teams] Teams bot ready (fallback mode)`);
        } catch (err: any) {
          logger.error(`[teams] Failed to start: ${err.message}`);
        }
      });
    }
  },
};
