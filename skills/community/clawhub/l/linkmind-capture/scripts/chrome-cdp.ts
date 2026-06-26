/**
 * Chrome DevTools Protocol (CDP) client for LinkMind.
 *
 * Replaces Playwright by connecting to the user's system Chrome via
 * --remote-debugging-port. Zero extra download (~200MB Chromium eliminated).
 */

import { spawn, type ChildProcess } from "node:child_process";
import { existsSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { createConnection, type Socket } from "node:net";

// ---------------------------------------------------------------------------
// Chrome path discovery
// ---------------------------------------------------------------------------

const CHROME_PATHS: Record<string, string[]> = {
  darwin: [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ],
  win32: [
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
    `${process.env.LOCALAPPDATA ?? ""}\\Google\\Chrome\\Application\\chrome.exe`,
  ],
  linux: [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
    "/snap/bin/chromium",
  ],
};

export function findChrome(): string {
  const candidates = CHROME_PATHS[process.platform] ?? CHROME_PATHS.linux;
  for (const p of candidates) {
    if (p && existsSync(p)) return p;
  }
  throw new Error(
    `未找到 Chrome 浏览器。请安装 Google Chrome 或设置 CHROME_PATH 环境变量。\n` +
      `已搜索路径：${candidates.join(", ")}`,
  );
}

// ---------------------------------------------------------------------------
// CDP WebSocket connection
// ---------------------------------------------------------------------------

interface CDPResponse {
  id?: number;
  result?: any;
  error?: { code: number; message: string };
  method?: string;
  params?: any;
}

export class CDPSession {
  private ws!: WebSocket;
  private reqId = 0;
  private pending = new Map<number, { resolve: (v: any) => void; reject: (e: Error) => void }>();
  private eventHandlers = new Map<string, Array<(params: any) => void>>();
  private connected = false;

  private constructor() {}

  static async connect(wsUrl: string): Promise<CDPSession> {
    const session = new CDPSession();
    await session.init(wsUrl);
    return session;
  }

  private init(wsUrl: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(wsUrl);
      this.ws.onopen = () => {
        this.connected = true;
        resolve();
      };
      this.ws.onerror = (e) => {
        if (!this.connected) reject(new Error(`CDP WebSocket 连接失败: ${e}`));
      };
      this.ws.onclose = () => {
        this.connected = false;
        for (const [, p] of this.pending) {
          p.reject(new Error("CDP connection closed"));
        }
        this.pending.clear();
      };
      this.ws.onmessage = (event) => {
        const msg: CDPResponse = JSON.parse(String(event.data));
        if (msg.id !== undefined && this.pending.has(msg.id)) {
          const p = this.pending.get(msg.id)!;
          this.pending.delete(msg.id);
          if (msg.error) {
            p.reject(new Error(`CDP error: ${msg.error.message}`));
          } else {
            p.resolve(msg.result);
          }
        }
        if (msg.method && this.eventHandlers.has(msg.method)) {
          for (const fn of this.eventHandlers.get(msg.method)!) {
            fn(msg.params);
          }
        }
      };
    });
  }

  async send(method: string, params?: Record<string, unknown>): Promise<any> {
    if (!this.connected) throw new Error("CDP session not connected");
    const id = ++this.reqId;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  on(event: string, handler: (params: any) => void): void {
    if (!this.eventHandlers.has(event)) {
      this.eventHandlers.set(event, []);
    }
    this.eventHandlers.get(event)!.push(handler);
  }

  close(): void {
    if (this.connected) {
      this.ws.close();
      this.connected = false;
    }
  }
}

// ---------------------------------------------------------------------------
// Chrome launcher
// ---------------------------------------------------------------------------

async function waitForPort(port: number, timeoutMs = 15_000): Promise<void> {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    const ok = await new Promise<boolean>((resolve) => {
      const sock: Socket = createConnection({ port, host: "127.0.0.1" }, () => {
        sock.destroy();
        resolve(true);
      });
      sock.on("error", () => {
        sock.destroy();
        resolve(false);
      });
    });
    if (ok) return;
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new Error(`Chrome debug port ${port} 未在 ${timeoutMs}ms 内就绪`);
}

async function getWsEndpoint(port: number): Promise<string> {
  const resp = await fetch(`http://127.0.0.1:${port}/json/version`);
  const data = (await resp.json()) as { webSocketDebuggerUrl: string };
  return data.webSocketDebuggerUrl;
}

export interface ChromeInstance {
  process: ChildProcess;
  wsEndpoint: string;
  port: number;
  kill: () => void;
}

export async function launchChrome(opts?: {
  headless?: boolean;
  port?: number;
  chromePath?: string;
  userDataDir?: string;
}): Promise<ChromeInstance> {
  const port = opts?.port ?? 9222 + Math.floor(Math.random() * 1000);
  const chromePath = opts?.chromePath ?? process.env.CHROME_PATH ?? findChrome();

  const args = [
    `--remote-debugging-port=${port}`,
    "--disable-background-networking",
    "--disable-client-side-phishing-detection",
    "--disable-default-apps",
    "--disable-extensions",
    "--disable-hang-monitor",
    "--disable-popup-blocking",
    "--disable-prompt-on-repost",
    "--disable-sync",
    "--disable-translate",
    "--metrics-recording-only",
    "--no-first-run",
    "--safebrowsing-disable-auto-update",
    "--disable-blink-features=AutomationControlled",
  ];

  if (opts?.headless !== false) {
    args.push("--headless=new");
  }

  const userDataDir = opts?.userDataDir ?? mkdtempSync(join(tmpdir(), "linkmind-chrome-"));
  args.push(`--user-data-dir=${userDataDir}`);

  const child = spawn(chromePath, args, {
    stdio: "ignore",
    detached: process.platform !== "win32",
  });

  child.on("error", (err) => {
    throw new Error(`Chrome 启动失败: ${err.message}`);
  });

  await waitForPort(port);
  const wsEndpoint = await getWsEndpoint(port);

  return {
    process: child,
    wsEndpoint,
    port,
    kill() {
      try {
        child.kill();
      } catch {}
    },
  };
}

// ---------------------------------------------------------------------------
// High-level page abstraction
// ---------------------------------------------------------------------------

export class CDPPage {
  constructor(
    private session: CDPSession,
    private targetId: string,
  ) {}

  static async create(browserWsUrl: string): Promise<{ page: CDPPage; session: CDPSession; targetId: string }> {
    const browserSession = await CDPSession.connect(browserWsUrl);
    const { targetId } = await browserSession.send("Target.createTarget", {
      url: "about:blank",
    });
    const { sessionId } = await browserSession.send("Target.attachToTarget", {
      targetId,
      flatten: true,
    }) as { sessionId: string };

    // Create a page session from the target's sessionId
    const pageWsUrl = browserWsUrl.replace(/\/devtools\/browser\/.*/, `/devtools/page/${targetId}`);
    const pageSession = await CDPSession.connect(pageWsUrl);

    await pageSession.send("Page.enable");
    await pageSession.send("Runtime.enable");
    await pageSession.send("Network.enable");

    browserSession.close();
    return { page: new CDPPage(pageSession, targetId), session: pageSession, targetId };
  }

  async addScriptOnNewDocument(source: string): Promise<void> {
    await this.session.send("Page.addScriptToEvaluateOnNewDocument", { source });
  }

  async navigate(url: string, opts?: { timeout?: number }): Promise<void> {
    const timeout = opts?.timeout ?? 30_000;
    const navPromise = new Promise<void>((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`Navigation timeout: ${url}`)), timeout);
      let resolved = false;
      const handler = () => {
        if (resolved) return;
        resolved = true;
        clearTimeout(timer);
        resolve();
      };
      this.session.on("Page.loadEventFired", handler);
    });
    await this.session.send("Page.navigate", { url });
    await navPromise;
  }

  async evaluate<T = any>(expression: string): Promise<T> {
    const result = await this.session.send("Runtime.evaluate", {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (result.exceptionDetails) {
      throw new Error(
        `JS evaluation error: ${result.exceptionDetails.exception?.description ?? result.exceptionDetails.text}`,
      );
    }
    return result.result.value as T;
  }

  async setCookies(
    cookies: Array<{ name: string; value: string; domain: string; path?: string }>,
  ): Promise<void> {
    await this.session.send("Network.setCookies", {
      cookies: cookies.map((c) => ({
        name: c.name,
        value: c.value,
        domain: c.domain,
        path: c.path ?? "/",
      })),
    });
  }

  async mouseMove(x: number, y: number): Promise<void> {
    await this.session.send("Input.dispatchMouseEvent", {
      type: "mouseMoved",
      x,
      y,
    });
  }

  url(): Promise<string> {
    return this.evaluate<string>("window.location.href");
  }

  async waitForSelector(selector: string, timeout = 15_000): Promise<boolean> {
    const start = Date.now();
    while (Date.now() - start < timeout) {
      const found = await this.evaluate<boolean>(
        `!!document.querySelector(${JSON.stringify(selector)})`,
      );
      if (found) return true;
      await new Promise((r) => setTimeout(r, 500));
    }
    return false;
  }

  async close(): Promise<void> {
    this.session.close();
  }
}

// ---------------------------------------------------------------------------
// Convenience: launch Chrome + open a page
// ---------------------------------------------------------------------------

export interface CDPBrowser {
  chrome: ChromeInstance;
  page: CDPPage;
  session: CDPSession;
  close: () => Promise<void>;
}

export async function launchWithPage(opts?: {
  headless?: boolean;
  chromePath?: string;
}): Promise<CDPBrowser> {
  const chrome = await launchChrome(opts);
  const { page, session } = await CDPPage.create(chrome.wsEndpoint);

  return {
    chrome,
    page,
    session,
    async close() {
      page.close();
      chrome.kill();
    },
  };
}
