import { spawnSync } from "node:child_process";
import * as fs from "node:fs";
import * as os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";
import {
  OPENCLAW_DELIVERY_PATH,
  bindDeliveryFromPluginCommand,
  trySaveOpenclawDeliveryFromInboundClaim,
  trySaveOpenclawDeliveryFromMessageHook,
} from "./delivery.js";
import { startImageServerAtRoot } from "./start-image-server.js";
import { startLocalAutoAtRoot } from "./start-local-auto.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const FARM_IMAGE_PATH = path.join(os.homedir(), ".grinders-farm", "farm.png");
const OPENCLAW_MEDIA_DIR = path.join(os.homedir(), ".openclaw", "media", "grinders-farm");
const ONESHOT_RELATIVE_PATH = path.join("src", "adapters", "oneshot.ts");
const DEFAULT_START_INTERVAL_SEC = 20 * 60;

type RuntimeMode =
  | { kind: "repo-tsx"; gameRoot: string }
  | { kind: "cli-bin"; bin: string; binArgsPrefix: string[] };
const ONESHOT_TIMEOUT_MS = 15_000;

function resolveGameRoot(api: OpenClawPluginApi): string {
  const raw = api.pluginConfig as { gameRoot?: string } | undefined;
  const fromEnv = process.env.GRINDERS_FARM_ROOT?.trim();
  if (fromEnv) return path.resolve(fromEnv);
  if (raw?.gameRoot?.trim()) return path.resolve(raw.gameRoot.trim());
  return path.resolve(__dirname, "..");
}

function isValidGameRoot(candidate: string): boolean {
  return fs.existsSync(path.join(candidate, ONESHOT_RELATIVE_PATH));
}

function resolveClawFarmCliBin(): { bin: string; binArgsPrefix: string[] } | null {
  const fromEnv = process.env.GRINDERS_FARM_CLI_BIN?.trim();
  if (fromEnv) {
    if (fromEnv.endsWith("/dist/src/adapters/terminal.js")) {
      const oneshotJs = fromEnv.replace(/terminal\.js$/, "oneshot.js");
      if (fs.existsSync(oneshotJs)) {
        return { bin: process.execPath, binArgsPrefix: [oneshotJs] };
      }
      return null;
    }
    return fromEnv.endsWith(".js") ? { bin: process.execPath, binArgsPrefix: [fromEnv] } : { bin: fromEnv, binArgsPrefix: [] };
  }
  try {
    const oneshotWhich = spawnSync("sh", ["-lc", "command -v grinders-farm-oneshot"], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
    const oneshotOut = (oneshotWhich.stdout ?? "").trim();
    if (oneshotOut) return { bin: oneshotOut, binArgsPrefix: [] };

    const which = spawnSync("sh", ["-lc", "command -v grinders-farm"], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
    const out = (which.stdout ?? "").trim();
    if (out) {
      if (out.endsWith("/dist/src/adapters/terminal.js")) {
        const oneshotJs = out.replace(/terminal\.js$/, "oneshot.js");
        if (fs.existsSync(oneshotJs)) {
          return { bin: process.execPath, binArgsPrefix: [oneshotJs] };
        }
        return null;
      }
      if (out.endsWith(".js")) {
        return { bin: process.execPath, binArgsPrefix: [out] };
      }
      return { bin: out, binArgsPrefix: [] };
    }
  } catch {
    // ignore
  }
  return null;
}

function resolveRuntimeMode(api: OpenClawPluginApi): RuntimeMode | null {
  const gameRoot = resolveGameRoot(api);
  if (isValidGameRoot(gameRoot)) {
    return { kind: "repo-tsx", gameRoot };
  }
  const bin = resolveClawFarmCliBin();
  if (bin) {
    return { kind: "cli-bin", bin: bin.bin, binArgsPrefix: bin.binArgsPrefix };
  }
  return null;
}

function getPluginTiming(api: OpenClawPluginApi): { autoBoot: boolean; imageServerPort: number } {
  const c = api.pluginConfig as
    | {
        autoStartWorkerOnGatewayBoot?: boolean;
        imageServerPort?: number;
      }
    | undefined;
  const autoBoot = c?.autoStartWorkerOnGatewayBoot !== false;
  const imageServerPort = typeof c?.imageServerPort === "number" && c.imageServerPort >= 1 ? c.imageServerPort : 18931;
  return { autoBoot, imageServerPort };
}

function runOneshot(mode: RuntimeMode, argsLine: string): { text: string; exitCode: number } {
  const argv = argsLine.trim().length > 0 ? argsLine.trim().split(/\s+/) : ["farm"];
  const resolvedOpenclawBin = resolveOpenclawBin();
  const env = {
    ...process.env,
    OPENCLAW_BIN: process.env.OPENCLAW_BIN?.trim() || resolvedOpenclawBin,
  };
  const result =
    mode.kind === "repo-tsx"
      ? spawnSync("npx", ["tsx", path.join(mode.gameRoot, ONESHOT_RELATIVE_PATH), ...argv], {
          cwd: mode.gameRoot,
          encoding: "utf8",
          maxBuffer: 8 * 1024 * 1024,
          timeout: ONESHOT_TIMEOUT_MS,
          env,
        })
      : spawnSync(mode.bin, [...mode.binArgsPrefix, ...argv], {
          encoding: "utf8",
          maxBuffer: 8 * 1024 * 1024,
          timeout: ONESHOT_TIMEOUT_MS,
          env,
        });
  const finalResult =
    result.error && (result.error as NodeJS.ErrnoException).code === "ENOEXEC"
      ? spawnSync(
          process.execPath,
          [mode.kind === "cli-bin" ? mode.bin : "", ...(mode.kind === "cli-bin" ? mode.binArgsPrefix : []), ...argv].filter(
            Boolean,
          ),
          {
          encoding: "utf8",
          maxBuffer: 8 * 1024 * 1024,
          timeout: ONESHOT_TIMEOUT_MS,
          env,
          },
        )
      : result;
  const stderr = finalResult.stderr?.trim() ?? "";
  const stdout = finalResult.stdout?.trim() ?? "";
  const combined = [stdout, stderr].filter(Boolean).join("\n");
  const code = finalResult.status ?? (finalResult.error ? 1 : 0);
  if (finalResult.error && (finalResult.error as NodeJS.ErrnoException).code === "ETIMEDOUT") {
    return {
      text:
        "grinders-farm 命令执行超时。请确认你安装的是支持 oneshot 的新版 grinders-farm（含 grinders-farm-oneshot），或在插件 config 里设置 gameRoot 指向源码仓库。",
      exitCode: 1,
    };
  }
  return { text: combined || (finalResult.error ? String(finalResult.error.message) : "(no output)"), exitCode: code };
}

function isTelegramChannel(ctx: { channel?: string; channelId?: string }): boolean {
  const surface = (ctx.channel ?? ctx.channelId ?? "").toString().trim().toLowerCase();
  return surface === "tg" || surface.includes("telegram");
}

function canAttachFarmImage(): boolean {
  return fs.existsSync(FARM_IMAGE_PATH);
}

function shouldAttachFarmImageForReply(text: string): boolean {
  // Only attach image when oneshot output explicitly includes farm image link.
  // This avoids stale farm.png being sent for text-only commands like `shop`.
  return text.includes("🖼 查看高清像素图:");
}

function stageFarmImageForOpenclaw(): string | null {
  try {
    fs.mkdirSync(OPENCLAW_MEDIA_DIR, { recursive: true });
    const staged = path.join(OPENCLAW_MEDIA_DIR, `farm-${Date.now()}.png`);
    fs.copyFileSync(FARM_IMAGE_PATH, staged);
    return staged;
  } catch {
    return null;
  }
}

function resolveOpenclawBin(): string {
  const fromEnv = process.env.OPENCLAW_BIN?.trim();
  if (fromEnv && fromEnv.length > 0) return fromEnv;
  try {
    const which = spawnSync("sh", ["-lc", "command -v openclaw"], {
      encoding: "utf8",
      maxBuffer: 1024 * 1024,
    });
    const fromWhich = (which.stdout ?? "").trim();
    if (fromWhich) return fromWhich;
  } catch {
    // keep trying
  }
  const candidates = [
    process.env.OPENCLAW_PATH?.trim(),
    process.env.NVM_BIN ? path.join(process.env.NVM_BIN, "openclaw") : "",
    path.join(path.dirname(process.execPath), "openclaw"),
    "/opt/homebrew/bin/openclaw",
    "/usr/local/bin/openclaw",
  ]
    .map((p) => (p ?? "").trim())
    .filter(Boolean);
  for (const p of candidates) {
    try {
      fs.accessSync(p, fs.constants.X_OK);
      return p;
    } catch {
      // keep trying
    }
  }
  return "openclaw";
}

function resolveDeliveryFallback(): { target?: string; accountId?: string; channel?: string; threadId?: string | number } {
  try {
    if (!fs.existsSync(OPENCLAW_DELIVERY_PATH)) return {};
    const raw = JSON.parse(fs.readFileSync(OPENCLAW_DELIVERY_PATH, "utf8")) as {
      target?: unknown;
      accountId?: unknown;
      channel?: unknown;
      threadId?: unknown;
    };
    const target = typeof raw.target === "string" ? raw.target.trim() : "";
    const accountId = typeof raw.accountId === "string" ? raw.accountId.trim() : "";
    const channel = typeof raw.channel === "string" ? raw.channel.trim() : "";
    const threadId =
      typeof raw.threadId === "string" || typeof raw.threadId === "number" ? (raw.threadId as string | number) : undefined;
    return {
      ...(target ? { target } : {}),
      ...(accountId ? { accountId } : {}),
      ...(channel ? { channel } : {}),
      ...(threadId != null ? { threadId } : {}),
    };
  } catch {
    return {};
  }
}

function buildTelegramImageCaption(text: string): string {
  const lines = text
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
  const nonTableLines = lines.filter((line) => !line.startsWith("|"));
  const title = nonTableLines[0] ?? "🌾 Grinder's Farm";
  const orderDoneLine = nonTableLines.find((line) => line.startsWith("✅ 完成订单："));
  const orderLine = nonTableLines.find((line) => line.startsWith("📦 订单:"));
  const marketLine = nonTableLines.find((line) => line.startsWith("📉 市场反馈："));
  const parts = [title, orderDoneLine, orderLine, marketLine].filter(Boolean);
  return parts.join("\n");
}

function trySendTelegramFarmImage(
  api: OpenClawPluginApi,
  ctx: {
    accountId?: string;
    to?: string;
    from?: string;
    senderId?: string;
    messageThreadId?: string | number;
  },
  caption: string,
): boolean {
  const fallback = resolveDeliveryFallback();
  const target = ((ctx.to ?? ctx.from ?? ctx.senderId ?? fallback.target) as string | undefined)?.toString().trim();
  if (!target) {
    api.logger?.warn?.("grinders-farm: skip telegram image send: missing target.");
    return false;
  }
  if (!canAttachFarmImage()) {
    api.logger?.warn?.(`grinders-farm: skip telegram image send: image not found (${FARM_IMAGE_PATH}).`);
    return false;
  }
  const stagedImagePath = stageFarmImageForOpenclaw();
  if (!stagedImagePath) {
    api.logger?.warn?.("grinders-farm: skip telegram image send: failed to stage image into ~/.openclaw/media.");
    return false;
  }

  const args = ["message", "send", "--channel", "telegram", "--target", target, "--message", caption];
  const accountId = ctx.accountId?.trim() || fallback.accountId;
  if (accountId) args.push("--account", accountId);
  const threadId = ctx.messageThreadId ?? fallback.threadId;
  if (threadId != null) args.push("--thread-id", String(threadId));
  args.push("--media", stagedImagePath);

  const r = spawnSync(resolveOpenclawBin(), args, {
    encoding: "utf8",
    maxBuffer: 8 * 1024 * 1024,
    env: { ...process.env },
  });
  if (r.error) {
    api.logger?.warn?.(`grinders-farm: telegram image send error: ${String(r.error.message)}`);
    return false;
  }
  const code = r.status ?? 0;
  if (code !== 0) {
    const details = [r.stdout, r.stderr].filter(Boolean).join("\n").trim();
    api.logger?.warn?.(`grinders-farm: telegram image send failed (exit ${code}) ${details || "(no output)"}`);
    return false;
  }
  return true;
}

function createFarmTool(mode: RuntimeMode) {
  return {
    name: "grinders_farm",
    label: "Grinder's Farm",
    ownerOnly: false,
    description:
      "Run grinders-farm one-shot CLI. Used by SKILL command-dispatch; params include `command` (raw args after /grinders_farm).",
    parameters: {
      type: "object",
      additionalProperties: true,
      properties: {
        command: { type: "string", description: "Raw args after /grinders_farm, e.g. plant carrot A1" },
        commandName: { type: "string" },
        skillName: { type: "string" },
      },
    },
    execute: async (_toolCallId: string, params: Record<string, unknown>) => {
      const raw = typeof params.command === "string" ? params.command : "";
      const { text, exitCode } = runOneshot(mode, raw);
      return {
        content: [{ type: "text" as const, text }],
        details: { exitCode },
        isError: exitCode !== 0,
      };
    },
  };
}

const plugin = {
  id: "grinders-farm",
  name: "Grinder's Farm",
  description: "Local grinders-farm subprocess for farm commands and push.",
  register(api: OpenClawPluginApi) {
    const runtime = resolveRuntimeMode(api);
    if (!runtime) {
      api.logger?.error?.(
        "grinders-farm: 无法定位运行时。请任选其一：1) 在插件 config 里设置 gameRoot（含 src/adapters/oneshot.ts）；2) 安装 grinders-farm CLI 并加入 PATH；3) 设置 GRINDERS_FARM_ROOT / GRINDERS_FARM_CLI_BIN。",
      );
      return;
    }
    api.registerTool(createFarmTool(runtime));

    api.registerCommand({
      name: "farm",
      description: "Grinder's Farm — run a game command and bind this chat for farm push.",
      acceptsArgs: true,
      handler: async (ctx) => {
        const bound = await bindDeliveryFromPluginCommand(ctx);
        if (!bound) {
          api.logger?.warn?.(
            "grinders-farm: could not bind delivery (need channel + senderId/to/from, or conversation binding).",
          );
        } else {
          const surface = (ctx.channel ?? ctx.channelId)?.toString().toLowerCase() ?? "";
          if (surface === "webchat") {
            api.logger?.info?.(
              "grinders-farm: Web 控制端已绑定；自动推送使用 Gateway chat.inject（默认会话 agent:<agentId>:main）。",
            );
          }
        }
        const { text, exitCode } = runOneshot(runtime, ctx.args ?? "");
        const fallback = resolveDeliveryFallback();
        const telegramLikeChannel = isTelegramChannel(ctx) || (fallback.channel?.toLowerCase().includes("telegram") ?? false);
        if (exitCode === 0 && telegramLikeChannel && shouldAttachFarmImageForReply(text) && canAttachFarmImage()) {
          const stagedImagePath = stageFarmImageForOpenclaw();
          if (stagedImagePath) {
            // Prefer native command reply media to avoid fallback-to-table behavior
            // in newer OpenClaw versions when command replies are text-only.
            return {
              text: buildTelegramImageCaption(text),
              mediaUrls: [stagedImagePath],
              isError: false,
            };
          }
          api.logger?.warn?.("grinders-farm: skip telegram inline media reply: failed to stage image.");
        }
        return { text, isError: exitCode !== 0 };
      },
    });

    api.on("gateway_start", async () => {
      const { autoBoot, imageServerPort } = getPluginTiming(api);
      if (runtime.kind !== "repo-tsx") {
        if (!autoBoot) return;
        const autoStart = runOneshot(runtime, "start");
        if (autoStart.exitCode === 0) {
          api.logger?.info?.("grinders-farm: 已通过 CLI 模式启动自动推进（固定 20 分钟）");
        } else {
          api.logger?.warn?.(`grinders-farm: CLI 模式自动推进启动失败：${autoStart.text}`);
        }
        return;
      }
      try {
        const imageServer = await startImageServerAtRoot(runtime.gameRoot, imageServerPort);
        if (imageServer.success) {
          api.logger?.info?.(`grinders-farm: ${imageServer.message}`);
        } else {
          api.logger?.warn?.(`grinders-farm: gateway_start image-server: ${imageServer.message}`);
        }
      } catch (e) {
        api.logger?.warn?.(`grinders-farm: gateway_start image-server: ${String(e)}`);
      }
      if (!autoBoot) return;
      try {
        const r = await startLocalAutoAtRoot(runtime.gameRoot, DEFAULT_START_INTERVAL_SEC);
        if (r.success) {
          api.logger?.info?.(`grinders-farm: ${r.message}`);
        } else {
          api.logger?.warn?.(`grinders-farm: gateway_start worker: ${r.message}`);
        }
      } catch (e) {
        api.logger?.warn?.(`grinders-farm: gateway_start: ${String(e)}`);
      }
    });

    api.on("inbound_claim", async (event, ctx) => {
      const saved = trySaveOpenclawDeliveryFromInboundClaim({
        channel: event.channel,
        accountId: event.accountId ?? ctx.accountId,
        conversationId: event.conversationId ?? ctx.conversationId,
        senderId: event.senderId ?? ctx.senderId,
        threadId: event.threadId,
      });
      if (saved) {
        api.logger?.info?.("grinders-farm: wrote openclaw-delivery.json (inbound_claim)");
      }
      return { handled: false };
    });

    api.on("message_received", async (event, ctx) => {
      const saved = trySaveOpenclawDeliveryFromMessageHook(event, ctx);
      if (saved) {
        api.logger?.info?.("grinders-farm: wrote openclaw-delivery.json (message_received)");
      }
    });
  },
};

export default plugin;
