#!/usr/bin/env node

import { createServer, HclServer } from "./server.js";
import { networkInterfaces } from "node:os";
import { discoverCdpTarget } from "./cdp.js";
import { Socket } from "node:net";
import { parseMaskRegions } from "./mask.js";

type ParsedArgs = Record<string, string | number | boolean>;

type ModeSelection =
  | { mode: "vnc"; vncHost: string; vncPort: number }
  | { mode: "cdp"; cdpHost: string; cdpPort: number };

type DetectResult = {
  selection: ModeSelection;
  reason: "explicit-cdp" | "explicit-vnc" | "auto-cdp" | "auto-vnc";
};

function getLocalIP(): string {
  const interfaces = networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    const iface = interfaces[name];
    if (!iface) continue;
    for (const addr of iface) {
      if (addr.family === "IPv4" && !addr.internal) {
        return addr.address;
      }
    }
  }
  return "127.0.0.1";
}

function parseArgs(args: string[]): ParsedArgs {
  const parsed: ParsedArgs = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        parsed[key] = isNaN(Number(next)) ? next : Number(next);
        i++;
      } else {
        parsed[key] = true;
      }
    } else {
      parsed._command = arg;
    }
  }
  return parsed;
}

function printUsage() {
  console.log(`HumanCanHelp (hcl) - Start a short-lived human help session for blocked AI workflows
HumanCanHelp (hcl) - 为受阻的 AI 工作流启动一个短时人工接手机制

Usage:
  hcl start [--port 6080] [--cdp localhost:9222] [--vnc localhost:5900] [--timeout 600] [--public] [--password secret]
  hcl stop
  hcl status

用法:
  hcl start [--port 6080] [--cdp localhost:9222] [--vnc localhost:5900] [--timeout 600] [--public] [--password secret]
  hcl stop
  hcl status

Commands:
  start    Start the help server and print helper URL(s)
  stop     Stop the running help server
  status   Check if a help server is running

命令:
  start    启动帮助会话并打印可分享的 URL
  stop     停止当前运行中的帮助服务
  status   检查当前是否已有帮助服务在运行

Options:
  --port <number>      HTTP server port (default: 6080)
  --cdp <host:port>    Use CDP mode (Chrome DevTools Protocol), e.g. --cdp localhost:9222
  --vnc <host:port>    VNC server address (default: localhost:5900)
  --timeout <seconds>  Session expiry in seconds; HCL immediately starts a fresh session after timeout (default: 600)
  --public             Create a public tunnel URL (for remote helpers)
  --password <string>  Optional password to protect the help URL
  --mask <regions>     Optional helper-side black mask regions that also block pointer input: "x,y,w,h;x,y,w,h"

参数:
  --port <number>      帮助页 HTTP 端口（默认：6080）
  --cdp <host:port>    使用 CDP 模式（Chrome DevTools Protocol），例如 --cdp localhost:9222
  --vnc <host:port>    VNC 服务地址（默认：localhost:5900）
  --timeout <seconds>  会话过期时间，单位秒；超时后 HCL 会立即启动一个新会话（默认：600）
  --public             为远程协助者创建公共访问地址
  --password <string>  为帮助地址添加访问密码
  --mask <regions>     可选协助者侧黑色遮罩，并阻止指针输入："x,y,w,h;x,y,w,h"
`);
}

function parseHostPort(value: string, defaultPort: number): { host: string; port: number } {
  const [host, portValue] = value.split(":");
  return {
    host: host || "localhost",
    port: parseInt(portValue || String(defaultPort), 10),
  };
}

async function fetchJson(url: string): Promise<Response> {
  try {
    return await fetch(url);
  } catch {
    throw new Error(`Unable to reach ${url}. / 无法连接到 ${url}。`);
  }
}

async function ensureCdpReady(host: string, port: number): Promise<void> {
  const versionResponse = await fetchJson(`http://${host}:${port}/json/version`);
  if (!versionResponse.ok) {
    throw new Error(
      `Chrome remote debugging is not available at ${host}:${port}. Start Chrome with --remote-debugging-port=${port}. / ${host}:${port} 上未发现 Chrome 远程调试端口，请先使用 --remote-debugging-port=${port} 启动 Chrome。`,
    );
  }

  const targetResponse = await fetchJson(`http://${host}:${port}/json/list`);
  if (!targetResponse.ok) {
    throw new Error(`CDP is reachable at ${host}:${port}, but the target list could not be loaded. / 已连通 ${host}:${port} 的 CDP，但无法读取目标页列表。`);
  }

  const targets = await targetResponse.json() as Array<{ type?: string; webSocketDebuggerUrl?: string }>;
  const hasPageTarget = targets.some((target) => target.type === "page" && typeof target.webSocketDebuggerUrl === "string");
  if (!hasPageTarget) {
    throw new Error(
      `CDP is reachable at ${host}:${port}, but no browser page target is open. Open the page you want to share and try again. / 已连通 ${host}:${port} 的 CDP，但当前没有可共享的页面，请先打开目标页面再重试。`,
    );
  }
}

async function ensureVncReady(host: string, port: number): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const socket = new Socket();
    let settled = false;

    const finish = (callback: () => void) => {
      if (settled) {
        return;
      }
      settled = true;
      socket.destroy();
      callback();
    };

    socket.setTimeout(1500);
    socket.once("connect", () => finish(resolve));
    socket.once("timeout", () => finish(() => reject(new Error(`Timed out connecting to VNC at ${host}:${port}. / 连接 ${host}:${port} 的 VNC 超时。`))));
    socket.once("error", () => finish(() => reject(new Error(`No VNC server is reachable at ${host}:${port}. / ${host}:${port} 没有可用的 VNC 服务。`))));
    socket.connect(port, host);
  });
}

async function chooseMode(parsed: ParsedArgs): Promise<DetectResult> {
  if (parsed.cdp) {
    const { host, port } = parseHostPort(String(parsed.cdp), 9222);
    return { selection: { mode: "cdp", cdpHost: host, cdpPort: port }, reason: "explicit-cdp" };
  }

  if (parsed.vnc) {
    const { host, port } = parseHostPort(String(parsed.vnc), 5900);
    return { selection: { mode: "vnc", vncHost: host, vncPort: port }, reason: "explicit-vnc" };
  }

  try {
    await ensureCdpReady("localhost", 9222);
    return { selection: { mode: "cdp", cdpHost: "localhost", cdpPort: 9222 }, reason: "auto-cdp" };
  } catch {
  }

  try {
    await ensureVncReady("localhost", 5900);
    return { selection: { mode: "vnc", vncHost: "localhost", vncPort: 5900 }, reason: "auto-vnc" };
  } catch {
  }

  throw new Error(
    "No usable local session source was found. Start Chrome with --remote-debugging-port=9222 or start a VNC server on localhost:5900 before running hcl start. / 未发现可用的本地会话来源。请先启动带 --remote-debugging-port=9222 的 Chrome，或先在 localhost:5900 启动 VNC 服务，然后再运行 hcl start。",
  );
}

async function verifySelectedMode(modeSelection: ModeSelection): Promise<void> {
  if (modeSelection.mode === "cdp") {
    await ensureCdpReady(modeSelection.cdpHost, modeSelection.cdpPort);
    return;
  }

  await ensureVncReady(modeSelection.vncHost, modeSelection.vncPort);
}

function printModeSelectionHint(reason: DetectResult["reason"]): void {
  if (reason === "auto-cdp") {
    console.log("  Source:  auto-detected CDP at localhost:9222 / 自动检测到 localhost:9222 上的 CDP");
    return;
  }

  if (reason === "auto-vnc") {
    console.log("  Source:  auto-detected VNC at localhost:5900 / 自动检测到 localhost:5900 上的 VNC");
  }
}

async function createPublicTunnel(port: number): Promise<string> {
  try {
    const localtunnel = await import("localtunnel");
    const tunnel = await localtunnel.default({ port });
    return tunnel.url;
  } catch {
    console.error("  Failed to create public tunnel. Install the optional dependency first: npm install localtunnel / 创建公共隧道失败。请先安装可选依赖：npm install localtunnel");
    return "";
  }
}

async function wait(ms: number): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    printUsage();
    process.exit(0);
  }

  const parsed = parseArgs(args);
  const command = parsed._command;

  if (command === "stop") {
    try {
      const resp = await fetch(`http://127.0.0.1:${parsed.port || 6080}/api/stop`, { method: "POST" });
      if (resp.ok) {
        await wait(200);
        console.log("Server stopped.");
      } else {
        console.log("No running server found.");
      }
    } catch {
      console.log("No running server found.");
    }
    process.exit(0);
  }

  if (command === "status") {
    try {
      const port = parsed.port || 6080;
      const resp = await fetch(`http://127.0.0.1:${port}/api/status`);
      if (resp.ok) {
        const data = await resp.json() as { status: string; publicUrl?: string; mode?: "vnc" | "cdp" };
        console.log(`Server running on port ${port}`);
        console.log(`Status: ${data.status}`);
        console.log(`Mode: ${data.mode || "vnc"}`);
        console.log(`Local: http://${getLocalIP()}:${port}`);
        if (data.publicUrl) console.log(`Public: ${data.publicUrl}`);
      } else {
        console.log("No server running.");
      }
    } catch {
      console.log("No server running.");
    }
    process.exit(0);
  }

  if (command === "start") {
    const port = Number(parsed.port) || 6080;
    const timeout = Number(parsed.timeout) || 600;
    const isPublic = !!parsed.public;
    const password = parsed.password ? String(parsed.password) : undefined;
    const mask = parsed.mask ? String(parsed.mask) : undefined;
    const detectResult = await chooseMode(parsed);
    const modeSelection = detectResult.selection;
      const maskRegions = mask ? parseMaskRegions(mask) : undefined;

    const localIP = getLocalIP();
    const localUrl = `http://${localIP}:${port}`;

    let currentServer: HclServer | null = null;
    let stopping = false;
    let publicUrl = "";

    process.on("SIGINT", () => {
      stopping = true;
      if (!currentServer) {
        console.log(`\n  Stopped.`);
        process.exit(0);
        return;
      }
      void currentServer?.stop().finally(() => {
        console.log(`\n  Stopped.`);
        process.exit(0);
      });
    });

    async function startSession(restarting = false): Promise<void> {
      let cdpTarget: string | null = null;
      try {
        await verifySelectedMode(modeSelection);
        if (modeSelection.mode === "cdp") {
          cdpTarget = await discoverCdpTarget({ host: modeSelection.cdpHost, port: modeSelection.cdpPort });
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        console.error(`Failed to start: ${message}`);
        process.exit(1);
        return;
      }

      let server: HclServer;
      try {
        server = await createServer({
          port,
          timeout,
          password,
          maskRegions,
          ...(modeSelection.mode === "cdp"
            ? {
                mode: "cdp",
                cdpHost: modeSelection.cdpHost,
                cdpPort: modeSelection.cdpPort,
              }
            : {
                mode: "vnc",
                vncHost: modeSelection.vncHost,
                vncPort: modeSelection.vncPort,
              }),
        });
      } catch (err) {
        const message = err instanceof Error ? err.message : String(err);
        console.error(`Failed to start: ${message}`);
        process.exit(1);
        return;
      }

      currentServer = server;

      console.log(restarting ? `\n  HumanCanHelp restarted\n` : `\n  HumanCanHelp started\n`);
      console.log(`  Local:   ${localUrl}`);
      if (!restarting) {
        printModeSelectionHint(detectResult.reason);
      }

      if (isPublic) {
        if (!publicUrl) {
          process.stdout.write(`  Public:  creating tunnel...`);
          publicUrl = await createPublicTunnel(port);
          if (publicUrl) {
            process.stdout.write(`\r  Public:  ${publicUrl}      \n`);
          } else {
            process.stdout.write(`\r  Public:  unavailable         \n`);
          }
        } else {
          console.log(`  Public:  ${publicUrl}`);
        }

        if (publicUrl) {
          server.setPublicUrl(publicUrl);
        }
      }

      if (modeSelection.mode === "cdp") {
        console.log(`  Mode:    CDP (Chrome DevTools Protocol)`);
        console.log(`  Target:  ${cdpTarget || server.getTarget() || `ws://${modeSelection.cdpHost}:${modeSelection.cdpPort}`}`);
      } else {
        console.log(`  Mode:    VNC`);
        console.log(`  VNC:     ${modeSelection.vncHost}:${modeSelection.vncPort}`);
      }
      console.log(`  Timeout: ${timeout}s`);
      if (password) console.log(`  Password: yes`);
      if (maskRegions) console.log(`  Masking:  ${maskRegions.length} region(s)`);
      console.log("");

      server.onDone(() => {
        currentServer = null;
        console.log(`\n  Helper marked as DONE.`);
        process.exit(0);
      });

      server.onFail((reason) => {
        currentServer = null;
        console.log(`\n  Helper marked as FAILED: ${reason}`);
        process.exit(1);
      });

      server.onLoginRequired((reason) => {
        currentServer = null;
        console.log(`\n  Helper marked as OWNER ACTION REQUIRED: ${reason}`);
        process.exit(2);
      });

      server.onTimeout((closed) => {
        currentServer = null;
        console.log(`\n  Timed out after ${timeout}s.`);
        if (stopping) {
          return;
        }
        void closed.then(() => startSession(true)).catch((err) => {
          const message = err instanceof Error ? err.message : String(err);
          console.error(`Failed to restart: ${message}`);
          process.exit(1);
        });
      });
    }

    await startSession();

    return;
  }

  printUsage();
  process.exit(1);
}

void main().catch((err) => {
  const message = err instanceof Error ? err.message : String(err);
  console.error(`Failed to start: ${message}`);
  process.exit(1);
});
