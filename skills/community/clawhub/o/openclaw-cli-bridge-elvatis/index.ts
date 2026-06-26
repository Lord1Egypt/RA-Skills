/**
 * openclaw-cli-bridge-elvatis — index.ts
 *
 * Phase 1 (auth bridge): registers openai-codex provider using tokens from
 *   ~/.codex/auth.json (Codex CLI is already logged in — no re-login needed).
 *
 * Phase 2 (request bridge): starts a local OpenAI-compatible HTTP proxy server
 *   and configures OpenClaw's vllm provider to route through it. Model calls
 *   are routed to CLI tools or browser-session providers.
 *
 * Phase 3 (slash commands): registers /cli-* commands for instant model switching.
 *   /cli-sonnet       → vllm/cli-claude/claude-sonnet-4-6      (Claude Code CLI proxy)
 *   /cli-opus         → vllm/cli-claude/claude-opus-4-6        (Claude Code CLI proxy)
 *   /cli-haiku        → vllm/cli-claude/claude-haiku-4-5       (Claude Code CLI proxy)
 *   /cli-gemini       → vllm/cli-gemini/gemini-2.5-pro         (Gemini CLI proxy)
 *   /cli-gemini-flash → vllm/cli-gemini/gemini-2.5-flash       (Gemini CLI proxy)
 *   /cli-gemini3      → vllm/cli-gemini/gemini-3-pro-preview   (Gemini CLI proxy)
 *   /cli-codex        → openai-codex/gpt-5.3-codex             (Codex CLI OAuth, direct API)
 *   /cli-codex54      → openai-codex/gpt-5.4                   (Codex CLI OAuth, direct API)
 *   /cli-opencode     → vllm/opencode/default                  (OpenCode CLI proxy)
 *   /cli-pi           → vllm/pi/default                        (Pi CLI proxy)
 *   /cli-back         → restore model that was active before last /cli-* switch
 *   /cli-test [model] → one-shot proxy health check (does NOT switch global model)
 *   /cli-list         → list all registered CLI bridge models with commands
 *
 * Provider / model naming:
 *   vllm/cli-gemini/gemini-2.5-pro  → `gemini -m gemini-2.5-pro @<tmpfile>`
 *   vllm/cli-claude/claude-opus-4-6 → `claude -p -m claude-opus-4-6 --output-format text` (stdin)
 */

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import http from "node:http";

// ── Auto-source version from package.json (eliminates hardcoded version sync) ──
const __dirname_local = dirname(fileURLToPath(import.meta.url));
const PACKAGE_VERSION: string = (() => {
  try {
    const pkg = JSON.parse(readFileSync(join(__dirname_local, "package.json"), "utf-8")) as { version: string };
    return pkg.version;
  } catch {
    // Second attempt: try openclaw.plugin.json (always co-located)
    try {
      const manifest = JSON.parse(readFileSync(join(__dirname_local, "openclaw.plugin.json"), "utf-8")) as { version: string };
      return manifest.version;
    } catch {
      return "unknown"; // should never happen — both files are always present
    }
  }
})();
import type {
  OpenClawPluginApi,
  ProviderAuthContext,
  ProviderAuthResult,
} from "openclaw/plugin-sdk";

// OpenClawPluginCommandDefinition is defined in the SDK types but not re-exported
// by the package — derive it from the registerCommand signature.
type OpenClawPluginCommandDefinition = Parameters<OpenClawPluginApi["registerCommand"]>[0];
import { buildOauthProviderAuthResult } from "openclaw/plugin-sdk";
import {
  DEFAULT_CODEX_AUTH_PATH,
  DEFAULT_MODEL as CODEX_DEFAULT_MODEL,
  readCodexCredentials,
} from "./src/codex-auth.js";
import { importCodexAuth } from "./src/codex-auth-import.js";
import { startProxyServer } from "./src/proxy-server.js";
import { patchOpencllawConfig } from "./src/config-patcher.js";
import {
  DEFAULT_PROXY_PORT,
  DEFAULT_PROXY_API_KEY,
  DEFAULT_PROXY_TIMEOUT_MS,
  DEFAULT_MODEL_TIMEOUTS,
  DEFAULT_MODEL_FALLBACKS,
  STATE_FILE as CONFIG_STATE_FILE,
  PENDING_FILE as CONFIG_PENDING_FILE,
  OPENCLAW_DIR,
  CLI_TEST_DEFAULT_MODEL as CONFIG_CLI_TEST_DEFAULT_MODEL,
  PROFILE_DIRS,
} from "./src/config.js";
import {
  loadSession,
  deleteSession,
  isSessionExpiredByAge,
  verifySession,
  runInteractiveLogin,
  createContextFromSession,
  DEFAULT_SESSION_PATH,
} from "./src/grok-session.js";
import {
  formatExpiryInfo,
  formatGeminiExpiry,
  formatClaudeExpiry,
  formatChatGPTExpiry,
} from "./src/expiry-helpers.js";
import type { BrowserContext, Browser } from "playwright";
import { checkSystemChrome } from "./src/chrome-check.js";
import { saveProviderExpiry, loadProviderExpiry, migrateLegacyFiles } from "./src/cookie-expiry-store.js";

// ──────────────────────────────────────────────────────────────────────────────
// Types derived from SDK (not re-exported by the package)
// ──────────────────────────────────────────────────────────────────────────────
type RegisterCommandParam = Parameters<OpenClawPluginApi["registerCommand"]>[0];
type PluginCommandContext = Parameters<RegisterCommandParam["handler"]>[0];
type PluginCommandResult = Awaited<ReturnType<RegisterCommandParam["handler"]>>;

// ──────────────────────────────────────────────────────────────────────────────
// Plugin config type
// ──────────────────────────────────────────────────────────────────────────────
interface CliPluginConfig {
  codexAuthPath?: string;
  enableCodex?: boolean;
  enableProxy?: boolean;
  proxyPort?: number;
  proxyApiKey?: string;
  proxyTimeoutMs?: number;
  modelTimeouts?: Record<string, number>;
  grokSessionPath?: string;
}

// ──────────────────────────────────────────────────────────────────────────────
// Grok web-session state (module-level, persists across commands)
// ──────────────────────────────────────────────────────────────────────────────

let grokBrowser: Browser | null = null;
let grokContext: BrowserContext | null = null;

// Persistent profile dirs — imported from config.ts
const GROK_PROFILE_DIR = PROFILE_DIRS.grok;
const GEMINI_PROFILE_DIR = PROFILE_DIRS.gemini;
const CLAUDE_PROFILE_DIR = PROFILE_DIRS.claude;
const CHATGPT_PROFILE_DIR = PROFILE_DIRS.chatgpt;

// Stealth launch options — prevent Cloudflare/bot detection from flagging the browser
const STEALTH_ARGS = [
  "--no-sandbox",
  "--disable-setuid-sandbox",
  "--disable-blink-features=AutomationControlled",
  "--disable-infobars",
];
const STEALTH_IGNORE_DEFAULTS = ["--enable-automation"] as const;

// ── Gemini web-session state ──────────────────────────────────────────────────
let geminiContext: BrowserContext | null = null;

// ── Claude web-session state ─────────────────────────────────────────────────
let claudeWebContext: BrowserContext | null = null;

// ── ChatGPT web-session state ────────────────────────────────────────────────
let chatgptContext: BrowserContext | null = null;

// ── Consolidated cookie expiry (delegates to cookie-expiry-store.ts) ─────────
// Legacy per-provider files are auto-migrated on first load.
interface GeminiExpiryInfo { expiresAt: number; loginAt: number; cookieName: string; }

function saveGeminiExpiry(info: GeminiExpiryInfo): void {
  saveProviderExpiry("gemini", info);
}
function loadGeminiExpiry(): GeminiExpiryInfo | null {
  return loadProviderExpiry("gemini");
}
// formatGeminiExpiry imported from ./src/expiry-helpers.js
async function scanGeminiCookieExpiry(ctx: BrowserContext): Promise<GeminiExpiryInfo | null> {
  try {
    const cookies = await ctx.cookies(["https://gemini.google.com", "https://accounts.google.com"]);
    const auth = cookies.filter(c => ["__Secure-1PSID", "__Secure-3PSID", "SID"].includes(c.name) && c.expires && c.expires > 0);
    if (!auth.length) return null;
    // Use the longest-lived auth cookie for expiry tracking
    auth.sort((a, b) => (b.expires ?? 0) - (a.expires ?? 0));
    const longest = auth[0];
    return { expiresAt: (longest.expires ?? 0) * 1000, loginAt: Date.now(), cookieName: longest.name };
  } catch { return null; }
}
// ── Claude cookie expiry helpers ─────────────────────────────────────────────
interface ClaudeExpiryInfo { expiresAt: number; loginAt: number; cookieName: string; }
function saveClaudeExpiry(info: ClaudeExpiryInfo): void {
  saveProviderExpiry("claude", info);
}
function loadClaudeExpiry(): ClaudeExpiryInfo | null {
  return loadProviderExpiry("claude");
}
// formatClaudeExpiry imported from ./src/expiry-helpers.js
async function scanClaudeCookieExpiry(ctx: BrowserContext): Promise<ClaudeExpiryInfo | null> {
  try {
    const cookies = await ctx.cookies(["https://claude.ai"]);
    const auth = cookies.filter(c => ["sessionKey", "lastActiveOrg"].includes(c.name) && c.expires && c.expires > 0);
    if (!auth.length) return null;
    // Use the LONGEST-lived auth cookie (sessionKey) for expiry tracking,
    // not short-lived Cloudflare cookies like __cf_bm (~30 min).
    auth.sort((a, b) => (b.expires ?? 0) - (a.expires ?? 0));
    const longest = auth[0];
    return { expiresAt: (longest.expires ?? 0) * 1000, loginAt: Date.now(), cookieName: longest.name };
  } catch { return null; }
}

// ── ChatGPT cookie expiry helpers ────────────────────────────────────────────
interface ChatGPTExpiryInfo { expiresAt: number; loginAt: number; cookieName: string; }
function saveChatGPTExpiry(info: ChatGPTExpiryInfo): void {
  saveProviderExpiry("chatgpt", info);
}
function loadChatGPTExpiry(): ChatGPTExpiryInfo | null {
  return loadProviderExpiry("chatgpt");
}
// formatChatGPTExpiry imported from ./src/expiry-helpers.js
async function scanChatGPTCookieExpiry(ctx: BrowserContext): Promise<ChatGPTExpiryInfo | null> {
  try {
    const cookies = await ctx.cookies(["https://chatgpt.com", "https://auth0.openai.com"]);
    const auth = cookies.filter(c => ["__Secure-next-auth.session-token", "_puid", "oai-did"].includes(c.name) && c.expires && c.expires > 0);
    if (!auth.length) return null;
    // Use the LONGEST-lived auth cookie for expiry tracking — _puid (~7d) is
    // much shorter than __Secure-next-auth.session-token and triggers false alerts.
    auth.sort((a, b) => (b.expires ?? 0) - (a.expires ?? 0));
    const longest = auth[0];
    return { expiresAt: (longest.expires ?? 0) * 1000, loginAt: Date.now(), cookieName: longest.name };
  } catch { return null; }
}

// ─────────────────────────────────────────────────────────────────────────────

interface GrokExpiryInfo {
  expiresAt: number;    // epoch ms — earliest auth cookie expiry
  loginAt: number;      // epoch ms — when /grok-login was last run
  cookieName: string;   // which cookie determines the expiry
}

function saveGrokExpiry(info: GrokExpiryInfo): void {
  saveProviderExpiry("grok", info);
}

function loadGrokExpiry(): GrokExpiryInfo | null {
  return loadProviderExpiry("grok");
}

// formatExpiryInfo imported from ./src/expiry-helpers.js

/** Scan context cookies and return earliest auth cookie expiry */
async function scanCookieExpiry(ctx: import("playwright").BrowserContext): Promise<GrokExpiryInfo | null> {
  try {
    const cookies = await ctx.cookies(["https://grok.com", "https://x.ai"]);
    const authCookies = cookies.filter((c) => ["sso", "sso-rw"].includes(c.name) && c.expires > 0);
    if (authCookies.length === 0) return null;
    // Use the longest-lived auth cookie for expiry tracking
    const earliest = authCookies.reduce((min, c) => (c.expires > min.expires ? c : min));
    return {
      expiresAt: earliest.expires * 1000,
      loginAt: Date.now(),
      cookieName: earliest.name,
    };
  } catch { return null; }
}

// Singleton CDP connection — one browser object shared across grok + claude
let _cdpBrowser: import("playwright").Browser | null = null;
let _cdpBrowserLaunchPromise: Promise<import("playwright").BrowserContext | null> | null = null;

// Startup restore guard — module-level so it survives hot-reloads (SIGUSR1).
// Set to true after first run; hot-reloads see true and skip the restore loop.
let _startupRestoreDone = false;

// ── Proxy guards ─────────────────────────────────────────────────────────────
// register() is called per-agent (~11×) AND on every hot-reload (~60s).
// All noisy info logs removed. Only warnings/errors remain. These simple
// module-level booleans are sufficient — probeExisting() handles the real
// deduplication for the proxy.
let _proxyStarted = false;
let _proxyOwnedByThisProcess = false;

// Session keep-alive interval — refreshes browser cookies every 20h
let _keepAliveInterval: ReturnType<typeof setInterval> | null = null;

/**
 * Connect to the OpenClaw managed browser (CDP port 18800).
 * Singleton: reuses the same connection. Falls back to persistent Chromium for Grok only.
 * NEVER launches a new browser for Claude — Claude requires the OpenClaw browser.
 */
async function connectToOpenClawBrowser(
  log: (msg: string) => void
): Promise<BrowserContext | null> {
  // Reuse existing CDP connection if still alive
  if (_cdpBrowser) {
    try {
      _cdpBrowser.contexts(); // ping
      return _cdpBrowser.contexts()[0] ?? null;
    } catch {
      _cdpBrowser = null;
    }
  }
  const { chromium } = await import("playwright");
  try {
    const browser = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 3000 });
    _cdpBrowser = browser;
    browser.on("disconnected", () => { _cdpBrowser = null; log("[cli-bridge] OpenClaw browser disconnected"); });
    log("[cli-bridge] connected to OpenClaw browser via CDP");
    return browser.contexts()[0] ?? null;
  } catch {
    log("[cli-bridge] OpenClaw browser not available (CDP 18800)");
    return null;
  }
}

/**
 * Launch (or reuse) a persistent headless Chromium context for grok.com.
 * ONLY used for Grok — Grok has a saved persistent profile with cookies.
 * Claude does NOT use this — it requires the OpenClaw browser.
 */
async function getOrLaunchGrokContext(
  log: (msg: string) => void
): Promise<BrowserContext | null> {
  // Already have a live context?
  if (grokContext) {
    try { grokContext.pages(); return grokContext; } catch { grokContext = null; }
  }

  // Try OpenClaw browser first (singleton CDP)
  const cdpCtx = await connectToOpenClawBrowser(log);
  if (cdpCtx) return cdpCtx;

  // Coalesce concurrent launch requests into one
  if (_cdpBrowserLaunchPromise) return _cdpBrowserLaunchPromise;

  _cdpBrowserLaunchPromise = (async () => {
    const { chromium } = await import("playwright");
    log("[cli-bridge:grok] launching persistent Chromium…");
    try {
      const ctx = await chromium.launchPersistentContext(GROK_PROFILE_DIR, {
        headless: true,
        channel: "chrome",
        args: STEALTH_ARGS,
        ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
      });
      grokContext = ctx;
      // Auto-cleanup on browser crash
      ctx.on("close", () => { grokContext = null; log("[cli-bridge:grok] persistent context closed"); });
      log("[cli-bridge:grok] persistent context ready");
      return ctx;
    } catch (err) {
      log(`[cli-bridge:grok] failed to launch browser: ${(err as Error).message}`);
      return null;
    } finally {
      _cdpBrowserLaunchPromise = null;
    }
  })();
  return _cdpBrowserLaunchPromise;
}

// ── Per-provider persistent context launch promises (coalesce concurrent calls) ──
let _geminiLaunchPromise: Promise<BrowserContext | null> | null = null;

async function getOrLaunchGeminiContext(
  log: (msg: string) => void
): Promise<BrowserContext | null> {
  if (geminiContext) {
    try { geminiContext.pages(); return geminiContext; } catch { geminiContext = null; }
  }
  const cdpCtx = await connectToOpenClawBrowser(log);
  if (cdpCtx) return cdpCtx;
  if (_geminiLaunchPromise) return _geminiLaunchPromise;
  _geminiLaunchPromise = (async () => {
    const { chromium } = await import("playwright");
    log("[cli-bridge:gemini] launching persistent Chromium…");
    try {
      mkdirSync(GEMINI_PROFILE_DIR, { recursive: true });
      const ctx = await chromium.launchPersistentContext(GEMINI_PROFILE_DIR, {
        headless: true,
        channel: "chrome",
        args: STEALTH_ARGS,
        ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
      });
      geminiContext = ctx;
      ctx.on("close", () => { geminiContext = null; log("[cli-bridge:gemini] persistent context closed"); });
      log("[cli-bridge:gemini] persistent context ready");
      return ctx;
    } catch (err) {
      log(`[cli-bridge:gemini] failed to launch browser: ${(err as Error).message}`);
      return null;
    } finally {
      _geminiLaunchPromise = null;
    }
  })();
  return _geminiLaunchPromise;
}

// ── Per-provider persistent context launch promises (Claude) ─────────────────
let _claudeLaunchPromise: Promise<BrowserContext | null> | null = null;

async function getOrLaunchClaudeContext(
  log: (msg: string) => void
): Promise<BrowserContext | null> {
  if (claudeWebContext) {
    try { claudeWebContext.pages(); return claudeWebContext; } catch { claudeWebContext = null; }
  }
  const cdpCtx = await connectToOpenClawBrowser(log);
  if (cdpCtx) return cdpCtx;
  if (_claudeLaunchPromise) return _claudeLaunchPromise;
  _claudeLaunchPromise = (async () => {
    const { chromium } = await import("playwright");
    log("[cli-bridge:claude-web] launching persistent Chromium…");
    try {
      mkdirSync(CLAUDE_PROFILE_DIR, { recursive: true });
      const ctx = await chromium.launchPersistentContext(CLAUDE_PROFILE_DIR, {
        headless: true,
        channel: "chrome",
        args: STEALTH_ARGS,
        ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
      });
      claudeWebContext = ctx;
      ctx.on("close", () => { claudeWebContext = null; log("[cli-bridge:claude-web] persistent context closed"); });
      log("[cli-bridge:claude-web] persistent context ready");
      return ctx;
    } catch (err) {
      log(`[cli-bridge:claude-web] failed to launch browser: ${(err as Error).message}`);
      return null;
    } finally {
      _claudeLaunchPromise = null;
    }
  })();
  return _claudeLaunchPromise;
}

// ── Per-provider persistent context launch promises (ChatGPT) ────────────────
let _chatgptLaunchPromise: Promise<BrowserContext | null> | null = null;

async function getOrLaunchChatGPTContext(
  log: (msg: string) => void
): Promise<BrowserContext | null> {
  if (chatgptContext) {
    try { chatgptContext.pages(); return chatgptContext; } catch { chatgptContext = null; }
  }
  const cdpCtx = await connectToOpenClawBrowser(log);
  if (cdpCtx) return cdpCtx;
  if (_chatgptLaunchPromise) return _chatgptLaunchPromise;
  _chatgptLaunchPromise = (async () => {
    const { chromium } = await import("playwright");
    log("[cli-bridge:chatgpt] launching persistent Chromium…");
    try {
      mkdirSync(CHATGPT_PROFILE_DIR, { recursive: true });
      const ctx = await chromium.launchPersistentContext(CHATGPT_PROFILE_DIR, {
        headless: true,
        channel: "chrome",
        args: STEALTH_ARGS,
        ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
      });
      chatgptContext = ctx;
      ctx.on("close", () => { chatgptContext = null; log("[cli-bridge:chatgpt] persistent context closed"); });
      log("[cli-bridge:chatgpt] persistent context ready");
      return ctx;
    } catch (err) {
      log(`[cli-bridge:chatgpt] failed to launch browser: ${(err as Error).message}`);
      return null;
    } finally {
      _chatgptLaunchPromise = null;
    }
  })();
  return _chatgptLaunchPromise;
}

/** Session keep-alive — navigate to provider home pages to refresh cookies.
 *  After each touch, verifies the session is still valid. If expired, attempts
 *  a full relogin. Returns provider login commands that need manual attention. */
async function sessionKeepAlive(log: (msg: string) => void): Promise<string[]> {
  const providers: Array<{
    name: string;
    homeUrl: string;
    verifySelector: string;
    loginCmd: string;
    getCtx: () => BrowserContext | null;
    setCtx: (c: BrowserContext | null) => void;
    scanExpiry: (ctx: BrowserContext) => Promise<{ expiresAt: number; loginAt: number; cookieName: string } | null>;
    saveExpiry: (info: { expiresAt: number; loginAt: number; cookieName: string }) => void;
  }> = [
    { name: "grok", homeUrl: "https://grok.com", verifySelector: "textarea", loginCmd: "/grok-login", getCtx: () => grokContext, setCtx: (c) => { grokContext = c; }, scanExpiry: scanCookieExpiry, saveExpiry: saveGrokExpiry },
    { name: "gemini", homeUrl: "https://gemini.google.com/app", verifySelector: ".ql-editor", loginCmd: "/gemini-login", getCtx: () => geminiContext, setCtx: (c) => { geminiContext = c; }, scanExpiry: scanGeminiCookieExpiry, saveExpiry: saveGeminiExpiry },
    { name: "claude-web", homeUrl: "https://claude.ai/new", verifySelector: ".ProseMirror", loginCmd: "/claude-login", getCtx: () => claudeWebContext, setCtx: (c) => { claudeWebContext = c; }, scanExpiry: scanClaudeCookieExpiry, saveExpiry: saveClaudeExpiry },
    { name: "chatgpt", homeUrl: "https://chatgpt.com", verifySelector: "#prompt-textarea", loginCmd: "/chatgpt-login", getCtx: () => chatgptContext, setCtx: (c) => { chatgptContext = c; }, scanExpiry: scanChatGPTCookieExpiry, saveExpiry: saveChatGPTExpiry },
  ];

  const needsLogin: string[] = [];

  for (const p of providers) {
    const ctx = p.getCtx();
    if (!ctx) continue;
    try {
      const page = await ctx.newPage();
      await page.goto(p.homeUrl, { waitUntil: "domcontentloaded", timeout: 15_000 });
      await new Promise(r => setTimeout(r, 4000));

      // Verify session is still valid after touch
      let valid = await page.locator(p.verifySelector).isVisible().catch(() => false);
      if (!valid) {
        // Retry once
        await new Promise(r => setTimeout(r, 3000));
        valid = await page.locator(p.verifySelector).isVisible().catch(() => false);
      }
      await page.close();

      if (valid) {
        const expiry = await p.scanExpiry(ctx);
        if (expiry) p.saveExpiry(expiry);
        log(`[cli-bridge:${p.name}] session keep-alive touch ✅`);
      } else {
        // Session expired — attempt relogin in same persistent context
        log(`[cli-bridge:${p.name}] session expired after keep-alive — attempting auto-relogin…`);
        const reloginPage = await ctx.newPage();
        await reloginPage.goto(p.homeUrl, { waitUntil: "domcontentloaded", timeout: 20_000 });
        await new Promise(r => setTimeout(r, 6000));
        let reloginOk = await reloginPage.locator(p.verifySelector).isVisible().catch(() => false);
        if (!reloginOk) {
          await new Promise(r => setTimeout(r, 3000));
          reloginOk = await reloginPage.locator(p.verifySelector).isVisible().catch(() => false);
        }
        await reloginPage.close().catch(() => {});
        if (reloginOk) {
          const expiry = await p.scanExpiry(ctx);
          if (expiry) p.saveExpiry(expiry);
          log(`[cli-bridge:${p.name}] auto-relogin successful ✅`);
        } else {
          log(`[cli-bridge:${p.name}] auto-relogin failed, needs manual ${p.loginCmd}`);
          needsLogin.push(p.loginCmd);
        }
      }
    } catch (err) {
      log(`[cli-bridge:${p.name}] session keep-alive failed: ${(err as Error).message}`);
    }
    // Sequential — avoid spawning multiple pages at once
    await new Promise(r => setTimeout(r, 2000));
  }

  return needsLogin;
}

/** Clean up all browser resources — call on plugin teardown */
async function cleanupBrowsers(log: (msg: string) => void): Promise<void> {
  if (_keepAliveInterval) {
    clearInterval(_keepAliveInterval);
    _keepAliveInterval = null;
  }
  // Close all browser contexts first, then the browser instances.
  // Closing contexts before browsers prevents orphaned Chromium processes.
  if (grokContext) {
    try { await grokContext.close(); } catch { /* ignore */ }
    grokContext = null;
  }
  if (grokBrowser) {
    try { await grokBrowser.close(); } catch { /* ignore */ }
    grokBrowser = null;
  }
  if (geminiContext) {
    try { await geminiContext.close(); } catch { /* ignore */ }
    geminiContext = null;
  }
  if (claudeWebContext) {
    try { await claudeWebContext.close(); } catch { /* ignore */ }
    claudeWebContext = null;
  }
  if (chatgptContext) {
    try { await chatgptContext.close(); } catch { /* ignore */ }
    chatgptContext = null;
  }
  if (_cdpBrowser) {
    try { await _cdpBrowser.close(); } catch { /* ignore */ }
    _cdpBrowser = null;
  }
  // Clear any pending launch promises to prevent stale references
  _cdpBrowserLaunchPromise = null;
  _geminiLaunchPromise = null;
  _claudeLaunchPromise = null;
  _chatgptLaunchPromise = null;
  log("[cli-bridge] browser resources cleaned up");
}

/**
 * Singleton guard for ensureAllProviderContexts — prevents concurrent spawns.
 * If a run is already in progress, callers await the same promise instead of
 * spawning a new Chromium each time.
 */
let _ensureAllRunning: Promise<void> | null = null;

/**
 * Ensure all browser provider contexts are connected.
 * 1. Try the shared OpenClaw browser (CDP 18800)
 * 2. Fallback: launch a persistent headless Chromium per provider (saved profile with cookies)
 *
 * SAFETY: Only one concurrent run allowed. Extra callers await the existing run.
 */
async function ensureAllProviderContexts(log: (msg: string) => void): Promise<void> {
  if (_ensureAllRunning) {
    log("[cli-bridge] ensureAllProviderContexts already running — awaiting existing run");
    return _ensureAllRunning;
  }
  _ensureAllRunning = _doEnsureAllProviderContexts(log).finally(() => {
    _ensureAllRunning = null;
  });
  return _ensureAllRunning;
}

async function _doEnsureAllProviderContexts(log: (msg: string) => void): Promise<void> {
  const { chromium } = await import("playwright");

  // Try CDP first (OpenClaw browser)
  let sharedCtx: BrowserContext | null = null;
  try {
    const b = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 2000 });
    sharedCtx = b.contexts()[0] ?? null;
    if (sharedCtx) log("[cli-bridge] using OpenClaw browser for all providers");
  } catch { /* not available */ }

  // For each provider: if no context yet, try shared ctx or launch own persistent context
  const providerConfigs = [
    {
      name: "gemini",
      profileDir: join(homedir(), ".openclaw", "gemini-profile"),
      getCtx: () => geminiContext,
      setCtx: (c: BrowserContext) => { geminiContext = c; },
      homeUrl: "https://gemini.google.com/app",
      verifySelector: ".ql-editor",
    },
  ];

  for (const cfg of providerConfigs) {
    if (cfg.getCtx()) continue; // already connected

    let ctx: BrowserContext | null = null;

    // 1. Try shared OpenClaw browser context
    if (sharedCtx) {
      try {
        const pages = sharedCtx.pages();
        const existing = pages.find(p => p.url().includes(new URL(cfg.homeUrl).hostname));
        const page = existing ?? await sharedCtx.newPage();
        if (!existing) {
          await page.goto(cfg.homeUrl, { waitUntil: "domcontentloaded", timeout: 10_000 });
          await new Promise(r => setTimeout(r, 2000));
        }
        const visible = await page.locator(cfg.verifySelector).isVisible().catch(() => false);
        if (visible) {
          ctx = sharedCtx;
          log(`[cli-bridge:${cfg.name}] connected via OpenClaw browser ✅`);
        }
      } catch { /* fall through */ }
    }

    // 2. Launch own persistent context (has saved cookies)
    if (!ctx) {
      try {
        mkdirSync(cfg.profileDir, { recursive: true });
        const pCtx = await chromium.launchPersistentContext(cfg.profileDir, {
          headless: true,
          channel: "chrome",
          args: STEALTH_ARGS,
          ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
        });
        const page = await pCtx.newPage();
        await page.goto(cfg.homeUrl, { waitUntil: "domcontentloaded", timeout: 15_000 });
        await new Promise(r => setTimeout(r, 4000));
        const visible = await page.locator(cfg.verifySelector).isVisible().catch(() => false);
        if (visible) {
          ctx = pCtx;
          log(`[cli-bridge:${cfg.name}] launched persistent context ✅`);
        } else {
          const title = await page.title().catch(() => "unknown");
          const bodySnippet = await page.evaluate(() => document.body?.innerText?.substring(0, 100) ?? "").catch(() => "");
          log(`[cli-bridge:${cfg.name}] persistent headless: editor not visible — title="${title}" body="${bodySnippet}"`);
          await pCtx.close().catch(() => {});
        }
      } catch (err) {
        log(`[cli-bridge:${cfg.name}] could not launch browser: ${(err as Error).message}`);
      }
    }

    if (ctx) cfg.setCtx(ctx);
  }
}

async function tryRestoreGrokSession(
  _sessionPath: string,
  log: (msg: string) => void
): Promise<boolean> {
  try {
    const ctx = await getOrLaunchGrokContext(log);
    if (!ctx) return false;

    const check = await verifySession(ctx, log);
    if (!check.valid) {
      log(`[cli-bridge:grok] session invalid: ${check.reason}`);
      return false;
    }
    grokContext = ctx;
    log("[cli-bridge:grok] session restored ✅");
    // Log cookie expiry status on startup
    const expiry = loadGrokExpiry();
    if (expiry) {
      log(`[cli-bridge:grok] cookie expiry: ${formatExpiryInfo(expiry)}`);
      // Re-scan to keep expiry file fresh (cookies may have been renewed)
      const freshExpiry = await scanCookieExpiry(ctx);
      if (freshExpiry) saveGrokExpiry(freshExpiry);
    }
    return true;
  } catch (err) {
    log(`[cli-bridge:grok] session restore error: ${(err as Error).message}`);
    return false;
  }
}

// DEFAULT_PROXY_PORT, DEFAULT_PROXY_API_KEY imported from config.ts

// ──────────────────────────────────────────────────────────────────────────────
// State file — persists the model that was active before the last /cli-* switch
// Located at ~/.openclaw/cli-bridge-state.json (survives gateway restarts)
// ──────────────────────────────────────────────────────────────────────────────
const STATE_FILE = CONFIG_STATE_FILE;

interface CliBridgeState {
  previousModel: string;
}

function readState(): CliBridgeState | null {
  try {
    return JSON.parse(readFileSync(STATE_FILE, "utf8")) as CliBridgeState;
  } catch {
    return null;
  }
}

function writeState(state: CliBridgeState): void {
  try {
    mkdirSync(OPENCLAW_DIR, { recursive: true });
    writeFileSync(STATE_FILE, JSON.stringify(state, null, 2) + "\n", "utf8");
  } catch {
    // non-fatal — /cli-back will just report no previous model
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Read the current primary model from openclaw.json
// ──────────────────────────────────────────────────────────────────────────────
function readCurrentModel(): string | null {
  try {
    const cfg = JSON.parse(
      readFileSync(join(homedir(), ".openclaw", "openclaw.json"), "utf8")
    );
    const m = cfg?.agents?.defaults?.model;
    if (typeof m === "string") return m;
    if (typeof m === "object" && m !== null && typeof m.primary === "string")
      return m.primary;
    return null;
  } catch {
    return null;
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// BitNet server health check
// ──────────────────────────────────────────────────────────────────────────────
async function checkBitNetServer(url = "http://127.0.0.1:8082"): Promise<boolean> {
  return new Promise((resolve) => {
    const target = new URL("/v1/models", url);
    const req = http.get(
      { hostname: target.hostname, port: parseInt(target.port), path: target.pathname, timeout: 3_000 },
      (res) => {
        let data = "";
        res.on("data", (c: Buffer) => (data += c));
        res.on("end", () => resolve(res.statusCode === 200));
      }
    );
    req.on("error", () => resolve(false));
    req.on("timeout", () => { req.destroy(); resolve(false); });
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// Phase 3: model command table
// ──────────────────────────────────────────────────────────────────────────────
const CLI_MODEL_COMMANDS = [
  // ── Claude Code CLI (via local proxy) ────────────────────────────────────────
  { name: "cli-sonnet",       model: "vllm/cli-claude/claude-sonnet-4-6",    description: "Claude Sonnet 4.6 (Claude Code CLI)",   label: "Claude Sonnet 4.6 (CLI)" },
  { name: "cli-opus",         model: "vllm/cli-claude/claude-opus-4-6",      description: "Claude Opus 4.6 (Claude Code CLI)",     label: "Claude Opus 4.6 (CLI)" },
  { name: "cli-haiku",        model: "vllm/cli-claude/claude-haiku-4-5",     description: "Claude Haiku 4.5 (Claude Code CLI)",    label: "Claude Haiku 4.5 (CLI)" },
  // ── Gemini CLI (via local proxy) ─────────────────────────────────────────────
  { name: "cli-gemini",       model: "vllm/cli-gemini/gemini-2.5-pro",       description: "Gemini 2.5 Pro (Gemini CLI)",           label: "Gemini 2.5 Pro (CLI)" },
  { name: "cli-gemini-flash", model: "vllm/cli-gemini/gemini-2.5-flash",     description: "Gemini 2.5 Flash (Gemini CLI)",         label: "Gemini 2.5 Flash (CLI)" },
  { name: "cli-gemini3",      model: "vllm/cli-gemini/gemini-3-pro-preview", description: "Gemini 3 Pro (Gemini CLI)",             label: "Gemini 3 Pro (CLI)" },
  { name: "cli-gemini3-flash", model: "vllm/cli-gemini/gemini-3-flash-preview", description: "Gemini 3 Flash (Gemini CLI)",       label: "Gemini 3 Flash (CLI)" },
  // ── Codex CLI (openai-codex provider, OAuth auth) ────────────────────────────
  { name: "cli-codex",        model: "openai-codex/gpt-5.3-codex",          description: "GPT-5.3 Codex (Codex CLI auth)",        label: "GPT-5.3 Codex" },
  { name: "cli-codex-spark",  model: "openai-codex/gpt-5.3-codex-spark",    description: "GPT-5.3 Codex Spark (Codex CLI auth)",  label: "GPT-5.3 Codex Spark" },
  { name: "cli-codex52",      model: "openai-codex/gpt-5.2-codex",          description: "GPT-5.2 Codex (Codex CLI auth)",        label: "GPT-5.2 Codex" },
  { name: "cli-codex54",      model: "openai-codex/gpt-5.4",                description: "GPT-5.4 (Codex CLI auth)",              label: "GPT-5.4" },
  { name: "cli-codex-mini",   model: "openai-codex/gpt-5.1-codex-mini",     description: "GPT-5.1 Codex Mini (Codex CLI auth)",   label: "GPT-5.1 Codex Mini" },
  // ── OpenCode CLI (via local proxy) ─────────────────────────────────────────
  { name: "cli-opencode",     model: "vllm/opencode/default",               description: "OpenCode (CLI)",                         label: "OpenCode (CLI)" },
  // ── Pi CLI (via local proxy) ─────────────────────────────────────────────────
  { name: "cli-pi",           model: "vllm/pi/default",                     description: "Pi (CLI)",                               label: "Pi (CLI)" },
  // ── BitNet local inference (via local proxy → llama-server) ─────────────────
  { name: "cli-bitnet",       model: "vllm/local-bitnet/bitnet-2b",         description: "BitNet b1.58 2B (local CPU, no API key)", label: "BitNet 2B (local)" },
] as const;

/** Default model used by /cli-test when no arg is given */
const CLI_TEST_DEFAULT_MODEL = CONFIG_CLI_TEST_DEFAULT_MODEL;

// ──────────────────────────────────────────────────────────────────────────────
// Staged-switch state file
// Stores a pending model switch that has not yet been applied.
// Written by /cli-* (default), applied by /cli-apply or /cli-* --now.
// Located at ~/.openclaw/cli-bridge-pending.json
// ──────────────────────────────────────────────────────────────────────────────
const PENDING_FILE = CONFIG_PENDING_FILE;

interface CliBridgePending {
  model: string;
  label: string;
  requestedAt: string;
}

function readPending(): CliBridgePending | null {
  try {
    return JSON.parse(readFileSync(PENDING_FILE, "utf8")) as CliBridgePending;
  } catch {
    return null;
  }
}

function writePending(pending: CliBridgePending): void {
  try {
    mkdirSync(OPENCLAW_DIR, { recursive: true });
    writeFileSync(PENDING_FILE, JSON.stringify(pending, null, 2) + "\n", "utf8");
  } catch {
    // non-fatal
  }
}

function clearPending(): void {
  try {
    const { unlinkSync } = require("node:fs");
    unlinkSync(PENDING_FILE);
  } catch {
    // non-fatal — file may not exist
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Helper: immediately apply the model switch (no safety checks)
// ──────────────────────────────────────────────────────────────────────────────
async function applyModelSwitch(
  api: OpenClawPluginApi,
  model: string,
  label: string,
): Promise<PluginCommandResult> {
  const current = readCurrentModel();
  if (current && current !== model) {
    writeState({ previousModel: current });
    api.logger.info(`[cli-bridge] saved previous model: ${current}`);
  }

  try {
    const result = await api.runtime.system.runCommandWithTimeout(
      ["openclaw", "models", "set", model],
      { timeoutMs: 8_000 }
    );

    if (result.code !== 0) {
      const err = (result.stderr || result.stdout || "unknown error").trim();
      api.logger.warn(`[cli-bridge] models set failed (code ${result.code}): ${err}`);
      return { text: `❌ Failed to switch to ${label}: ${err}` };
    }

    clearPending();
    api.logger.info(`[cli-bridge] switched model → ${model}`);
    return {
      text:
        `✅ Switched to **${label}**\n` +
        `\`${model}\`\n\n` +
        `Use \`/cli-back\` to restore previous model.`,
    };
  } catch (err) {
    const msg = (err as Error).message;
    api.logger.warn(`[cli-bridge] models set error: ${msg}`);
    return { text: `❌ Error switching model: ${msg}` };
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Helper: staged switch (default behavior)
//
// ⚠️  SAFETY: /cli-* mid-session bricht den aktiven Agenten.
//
// `openclaw models set` ist ein **sofortiger, globaler Switch**.
// Der laufende Agent verliert seinen Kontext — Tool-Calls werden nicht
// ausgeführt, Planfiles werden nicht geschrieben, keine Rückmeldung.
//
// Default: Switch wird nur gespeichert (nicht angewendet).
// Mit --now: sofortiger Switch (nur zwischen Sessions verwenden!).
// Mit /cli-apply: gespeicherten Switch anwenden (nach Session-Ende).
// ──────────────────────────────────────────────────────────────────────────────
async function switchModel(
  api: OpenClawPluginApi,
  model: string,
  label: string,
  forceNow: boolean,
): Promise<PluginCommandResult> {
  // --now: sofortiger Switch, volle Verantwortung beim User
  if (forceNow) {
    api.logger.warn(`[cli-bridge] --now switch to ${model} (immediate, session may break)`);
    return applyModelSwitch(api, model, label);
  }

  // Default: staged switch — speichern, warnen, nicht anwenden
  const current = readCurrentModel();

  if (current === model) {
    return { text: `ℹ️ Already on **${label}**\n\`${model}\`` };
  }

  writePending({ model, label, requestedAt: new Date().toISOString() });
  api.logger.info(`[cli-bridge] staged switch → ${model} (pending, not applied yet)`);

  return {
    text:
      `📋 **Model switch staged: ${label}**\n` +
      `\`${model}\`\n\n` +
      `⚠️ **NOT applied yet** — switching mid-session breaks the active agent:\n` +
      `tool calls fail silently, plan files don't get written, no feedback.\n\n` +
      `**To apply:**\n` +
      `• \`/cli-apply\` — apply after finishing your current task\n` +
      `• \`/cli-* --now\` — force immediate switch (only between sessions!)`,
  };
}

// ──────────────────────────────────────────────────────────────────────────────
// Helper: fire a one-shot test request directly at the proxy (no global switch)
// ──────────────────────────────────────────────────────────────────────────────
function proxyTestRequest(
  port: number,
  apiKey: string,
  model: string,
  timeoutMs: number
): Promise<string> {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model,
      messages: [{ role: "user", content: "Reply with exactly: CLI bridge OK" }],
      stream: false,
    });

    const req = http.request(
      {
        hostname: "127.0.0.1",
        port,
        path: "/v1/chat/completions",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`,
          "Content-Length": Buffer.byteLength(body),
        },
      },
      (res) => {
        let data = "";
        res.on("data", (chunk: Buffer) => { data += chunk.toString(); });
        res.on("end", () => {
          try {
            const parsed = JSON.parse(data) as {
              choices?: Array<{ message?: { content?: string } }>;
              error?: { message?: string };
            };
            if (parsed.error) {
              resolve(`Proxy error: ${parsed.error.message}`);
            } else {
              resolve(parsed.choices?.[0]?.message?.content?.trim() ?? "(empty response)");
            }
          } catch {
            resolve(`(non-JSON response: ${data.slice(0, 200)})`);
          }
        });
      }
    );

    req.setTimeout(timeoutMs, () => {
      req.destroy();
      reject(new Error(`Proxy test timed out after ${timeoutMs}ms`));
    });
    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// Plugin definition
// ──────────────────────────────────────────────────────────────────────────────
const plugin = {
  id: "openclaw-cli-bridge-elvatis",
  name: "OpenClaw CLI Bridge",
  version: PACKAGE_VERSION,
  description:
    "Phase 1: openai-codex auth bridge. " +
    "Phase 2: HTTP proxy for gemini/claude CLIs. " +
    "Phase 3: /cli-* model switching, /cli-back restore, /cli-test health check. " +
    "Phase 4: persistent browser profiles for Grok, Gemini, Claude.ai, ChatGPT.",

  register(api: OpenClawPluginApi) {
    const cfg = (api.pluginConfig ?? {}) as CliPluginConfig;
    const enableCodex = cfg.enableCodex ?? true;
    const enableProxy = cfg.enableProxy ?? true;
    const port = cfg.proxyPort ?? DEFAULT_PROXY_PORT;
    const apiKey = cfg.proxyApiKey ?? DEFAULT_PROXY_API_KEY;
    const timeoutMs = cfg.proxyTimeoutMs ?? DEFAULT_PROXY_TIMEOUT_MS;
    // Per-model timeout overrides — defaults from config.ts, can be extended via plugin config.
    const modelTimeouts = { ...DEFAULT_MODEL_TIMEOUTS, ...cfg.modelTimeouts };
    const codexAuthPath = cfg.codexAuthPath ?? DEFAULT_CODEX_AUTH_PATH;
    const grokSessionPath = cfg.grokSessionPath ?? DEFAULT_SESSION_PATH;

    // ── Model → slash command mapping for status page ──────────────────────────
    const modelCommands: Record<string, string> = {};
    for (const entry of CLI_MODEL_COMMANDS) {
      // Strip vllm/ prefix to match CLI_MODELS IDs
      const modelId = entry.model.replace(/^vllm\//, "");
      modelCommands[modelId] = `/${entry.name}`;
    }

    // ── Default model fallback chain (from config.ts) ──────────────────────────
    const modelFallbacks = { ...DEFAULT_MODEL_FALLBACKS };

    // ── Migrate legacy per-provider cookie expiry files to consolidated store ─
    const migration = migrateLegacyFiles();
    if (migration.migrated.length > 0) {
      api.logger.info(`[cli-bridge] migrated cookie expiry data: ${migration.migrated.join(", ")} → cookie-expiry.json`);
    }

    // ── Chrome availability check ────────────────────────────────────────────
    // Stealth mode uses channel: "chrome" (real system Chrome). If it's missing,
    // browser launches will fail or Cloudflare will block the bundled Chromium.
    const chromeCheck = checkSystemChrome();
    // Chrome warning only — success is silent (logged hundreds of times per minute otherwise)
    if (!chromeCheck.available) {
      api.logger.warn(
        `[cli-bridge] ⚠ system Chrome not found! Web browser providers (/grok-login, /gemini-login, etc.) ` +
        `require Google Chrome or Chromium installed system-wide. ` +
        `Install with: sudo apt install google-chrome-stable (or chromium-browser)`
      );
    }

    // ── Session restore: only on first plugin load (not on hot-reloads) ──────
    // The gateway polls every ~60s via openclaw status, which triggers a hot-reload
    // (SIGUSR1 + hybrid mode). Module-level contexts (grokContext etc.) survive
    // hot-reloads because Node keeps the module in memory — so we only need to
    // restore once, on the very first load (when all contexts are null).
    //
    // Guard: _startupRestoreDone is module-level and persists across hot-reloads.
    // IMPORTANT: Only restore sessions when the proxy is enabled (gateway mode).
    // Short-lived CLI commands (openclaw models status, openclaw doctor, etc.)
    // must NOT launch 4 Chromium instances — they block the process from exiting.
    // Only restore browser sessions when this process OWNS the proxy (gateway mode).
    // Short-lived CLI commands (openclaw models status) reuse an external proxy and
    // must not launch 4 Chromium instances that block the process from exiting.
    if (!_startupRestoreDone && _proxyOwnedByThisProcess) {
      _startupRestoreDone = true;
      void (async () => {
        await new Promise(r => setTimeout(r, 5000)); // wait for proxy + gateway to settle
        const { chromium } = await import("playwright");
        const { existsSync } = await import("node:fs");

        // Collect providers that need re-login — send one batched WhatsApp alert
        const needsLogin: string[] = [];

        const profileProviders: Array<{
          name: string;
          providerKey: import("./src/cookie-expiry-store.js").ProviderName;
          profileDir: string;
          verifySelector: string;
          homeUrl: string;
          loginCmd: string;
          setCtx: (c: BrowserContext) => void;
          getCtx: () => BrowserContext | null;
        }> = [
          {
            name: "grok",
            providerKey: "grok",
            profileDir: GROK_PROFILE_DIR,
            verifySelector: "textarea",
            homeUrl: "https://grok.com",
            loginCmd: "/grok-login",
            getCtx: () => grokContext,
            setCtx: (c) => { grokContext = c; },
          },
          {
            name: "gemini",
            providerKey: "gemini",
            profileDir: GEMINI_PROFILE_DIR,
            verifySelector: ".ql-editor",
            homeUrl: "https://gemini.google.com/app",
            loginCmd: "/gemini-login",
            getCtx: () => geminiContext,
            setCtx: (c) => { geminiContext = c; },
          },
          {
            name: "claude-web",
            providerKey: "claude",
            profileDir: CLAUDE_PROFILE_DIR,
            verifySelector: ".ProseMirror",
            homeUrl: "https://claude.ai/new",
            loginCmd: "/claude-login",
            getCtx: () => claudeWebContext,
            setCtx: (c) => { claudeWebContext = c; },
          },
          {
            name: "chatgpt",
            providerKey: "chatgpt",
            profileDir: CHATGPT_PROFILE_DIR,
            verifySelector: "#prompt-textarea",
            homeUrl: "https://chatgpt.com",
            loginCmd: "/chatgpt-login",
            getCtx: () => chatgptContext,
            setCtx: (c) => { chatgptContext = c; },
          },
        ];

        for (const p of profileProviders) {
          const storedExpiry = loadProviderExpiry(p.providerKey);
          if (!existsSync(p.profileDir) && !storedExpiry) {
            api.logger.info(`[cli-bridge:${p.name}] no saved profile — skipping startup restore`);
            continue;
          }
          if (p.getCtx()) continue; // already connected

          // ── Cookie-first check ────────────────────────────────────────────
          // If cookie expiry data exists and is still valid (>1h left),
          // launch the persistent context immediately without a browser-based
          // selector check. Selector checks are fragile (slow pages, DOM changes).
          // The keep-alive (20h) will verify the session properly later.
          let cookiesValid = false;
          if (storedExpiry) {
            try {
              const msLeft = storedExpiry.expiresAt - Date.now();
              if (msLeft > 3_600_000) { // >1h remaining
                cookiesValid = true;
                api.logger.info(`[cli-bridge:${p.name}] cookie valid (${Math.floor(msLeft / 86_400_000)}d left) — restoring context without browser check`);
              }
            } catch { /* ignore parse errors */ }
          }

          if (cookiesValid) {
            try {
              const ctx = await chromium.launchPersistentContext(p.profileDir, {
                headless: true,
                args: ["--no-sandbox", "--disable-setuid-sandbox"],
              });
              p.setCtx(ctx);
              ctx.on("close", () => { p.setCtx(null as unknown as BrowserContext); });
              api.logger.info(`[cli-bridge:${p.name}] session restored from profile ✅`);
            } catch (err) {
              api.logger.warn(`[cli-bridge:${p.name}] context launch failed: ${(err as Error).message}`);
              needsLogin.push(p.loginCmd);
            }
            // Sequential — never spawn all 4 Chromium instances at once
            await new Promise(r => setTimeout(r, 1000));
            continue;
          }

          // ── Fallback: cookies expired or missing — try browser check ─────
          try {
            api.logger.info(`[cli-bridge:${p.name}] cookies expired/missing — verifying via browser…`);
            const ctx = await chromium.launchPersistentContext(p.profileDir, {
              headless: true,
              args: ["--no-sandbox", "--disable-setuid-sandbox"],
            });
            const page = await ctx.newPage();
            await page.goto(p.homeUrl, { waitUntil: "domcontentloaded", timeout: 20_000 });
            await new Promise(r => setTimeout(r, 6000));
            const ok = await page.locator(p.verifySelector).isVisible().catch(() => false);
            await page.close().catch(() => {});
            if (ok) {
              p.setCtx(ctx);
              ctx.on("close", () => { p.setCtx(null as unknown as BrowserContext); });
              api.logger.info(`[cli-bridge:${p.name}] session restored from profile ✅`);
            } else {
              await ctx.close().catch(() => {});
              api.logger.info(`[cli-bridge:${p.name}] session expired — needs ${p.loginCmd}`);
              needsLogin.push(p.loginCmd);
            }
          } catch (err) {
            api.logger.warn(`[cli-bridge:${p.name}] startup restore failed: ${(err as Error).message}`);
          }

          // Sequential — never spawn all 4 Chromium instances at once
          await new Promise(r => setTimeout(r, 3000));

        }

        // Send one batched WhatsApp alert if any providers need re-login
        if (needsLogin.length > 0) {
          const cmds = needsLogin.map(cmd => `• ${cmd}`).join("\n");
          const msg = `🔐 *cli-bridge:* Session expired for ${needsLogin.length} provider(s). Run to re-login:\n\n${cmds}`;
          try {
            await api.runtime.system.runCommandWithTimeout(
              ["openclaw", "message", "send", "--channel", "whatsapp", "--to", "+4915170113694", "--message", msg],
              { timeoutMs: 10_000 }
            );
            api.logger.info(`[cli-bridge] sent re-login notification for: ${needsLogin.join(", ")}`);
          } catch (err) {
            api.logger.warn(`[cli-bridge] failed to send re-login notification: ${(err as Error).message}`);
          }
        }
      })();

      // Start session keep-alive interval (every 20h)
      if (!_keepAliveInterval) {
        _keepAliveInterval = setInterval(() => {
          void (async () => {
            const failed = await sessionKeepAlive((msg) => api.logger.info(msg));
            if (failed.length > 0) {
              const cmds = failed.map(cmd => `• ${cmd}`).join("\n");
              const msg = `🔐 *cli-bridge keep-alive:* Session expired for ${failed.length} provider(s). Run to re-login:\n\n${cmds}`;
              try {
                await api.runtime.system.runCommandWithTimeout(
                  ["openclaw", "message", "send", "--channel", "whatsapp", "--to", "+4915170113694", "--message", msg],
                  { timeoutMs: 10_000 }
                );
                api.logger.info(`[cli-bridge] keep-alive: sent re-login notification for: ${failed.join(", ")}`);
              } catch (err) {
                api.logger.warn(`[cli-bridge] keep-alive: failed to send notification: ${(err as Error).message}`);
              }
            }
          })();
        }, 72_000_000);
      }
    }

    // ── Phase 1: openai-codex auth bridge ─────────────────────────────────────
    if (enableCodex) {
      api.registerProvider({
        id: "openai-codex",
        label: "OpenAI Codex (CLI bridge)",
        docsPath: "/providers/openai",
        aliases: ["codex-cli"],

        auth: [
          {
            id: "codex-cli-oauth",
            label: "Codex CLI (existing login)",
            hint: "Reads OAuth tokens from ~/.codex/auth.json — no re-login needed",
            kind: "oauth",

            run: async (ctx: ProviderAuthContext): Promise<ProviderAuthResult> => {
              const spin = ctx.prompter.progress("Reading Codex CLI credentials…");
              try {
                const creds = await readCodexCredentials(codexAuthPath);
                spin.stop("Codex CLI credentials loaded");
                return buildOauthProviderAuthResult({
                  providerId: "openai-codex",
                  defaultModel: CODEX_DEFAULT_MODEL,
                  access: creds.accessToken,
                  refresh: creds.refreshToken,
                  expires: creds.expiresAt,
                  email: creds.email,
                  notes: [
                    `Auth read from: ${codexAuthPath}`,
                    "If calls fail, run 'codex login' to refresh, then re-run auth.",
                  ],
                });
              } catch (err) {
                spin.stop("Failed to read Codex credentials");
                throw err;
              }
            },
          },
        ],

        refreshOAuth: async (cred: ProviderAuthContext) => {
          try {
            const fresh = await readCodexCredentials(codexAuthPath);
            // Also update the agent auth store with refreshed tokens
            void importCodexAuth({
              codexAuthPath,
              log: (msg) => api.logger.info(`[cli-bridge:codex-refresh] ${msg}`),
            });
            return {
              ...cred,
              access: fresh.accessToken,
              refresh: fresh.refreshToken ?? cred.refresh,
              expires: fresh.expiresAt ?? cred.expires,
            };
          } catch {
            return cred;
          }
        },
      });

      // Provider registration is silent — logged hundreds of times otherwise

      // Auto-import Codex CLI credentials into the agent auth store (Issue #2).
      // This ensures `openai-codex/*` models work immediately without manual
      // `openclaw models auth login`. Runs async, non-blocking.
      // Codex auth import: silent log callback (suppress "already up-to-date" spam)
      // Only log on actual import or error — not on skip/already-current.
      void importCodexAuth({
        codexAuthPath,
        log: () => {}, // silent — internal "already up-to-date" spam suppressed
      }).then((result) => {
        if (result.imported) {
          api.logger.info("[cli-bridge] Codex auth auto-imported into agent auth store ✅");
        } else if (result.error) {
          api.logger.warn(`[cli-bridge] Codex auth import failed: ${result.error}`);
        }
      });
    }

    // ── Phase 2: CLI request proxy ─────────────────────────────────────────────
    let proxyServer: import("node:http").Server | null = null;

    if (enableProxy) {
      // Probe whether a healthy proxy is already listening on our port.
      // This handles hot-reloads where the previous plugin instance's server.close()
      // may not have completed yet — rather than killing anything (dangerous: fuser -k
      // can kill the gateway process itself during in-process hot-reloads), we just
      // check if the existing server still responds and reuse it if so.
      const probeExisting = (): Promise<boolean> => {
        return new Promise((resolve) => {
          const req = http.request(
            { hostname: "127.0.0.1", port, path: "/v1/models", method: "GET",
              headers: { Authorization: `Bearer ${apiKey}` } },
            (res) => { res.resume(); resolve(res.statusCode === 200); }
          );
          req.setTimeout(2000, () => { req.destroy(); resolve(false); });
          req.on("error", () => resolve(false));
          req.end();
        });
      };

      const startProxy = async (): Promise<void> => {
        // Guard: only the first register() call starts the proxy.
        // Subsequent per-agent calls AND hot-reloads skip entirely.
        if (_proxyStarted) return;
        _proxyStarted = true;

        // If a healthy proxy is already up, reuse it — no need to rebind.
        const alive = await probeExisting();
        if (alive) {
          // Silent — this fires on every hot-reload (~60s) and every register() call
          return;
        }

        try {
          const server = await startProxyServer({
            port,
            apiKey,
            timeoutMs,
            log: (msg) => api.logger.info(msg),
            warn: (msg) => api.logger.warn(msg),
            getGrokContext: () => grokContext,
            connectGrokContext: async () => {
              const ctx = await getOrLaunchGrokContext((msg) => api.logger.info(msg));
              if (ctx) {
                const check = await verifySession(ctx, (msg) => api.logger.info(msg));
                if (check.valid) { grokContext = ctx; return ctx; }
              }
              return null;
            },
            getGeminiContext: () => geminiContext,
            connectGeminiContext: async () => {
              const ctx = await getOrLaunchGeminiContext((msg) => api.logger.info(msg));
              if (ctx) {
                const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
                const { page } = await getOrCreateGeminiPage(ctx);
                const editor = await page.locator(".ql-editor").isVisible().catch(() => false);
                if (editor) { geminiContext = ctx; return ctx; }
              }
              return geminiContext;
            },
            getClaudeContext: () => claudeWebContext,
            connectClaudeContext: async () => {
              const ctx = await getOrLaunchClaudeContext((msg) => api.logger.info(msg));
              if (ctx) {
                const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
                const { page } = await getOrCreateClaudePage(ctx);
                const editor = await page.locator(".ProseMirror").isVisible().catch(() => false);
                if (editor) { claudeWebContext = ctx; return ctx; }
              }
              return claudeWebContext;
            },
            getChatGPTContext: () => chatgptContext,
            connectChatGPTContext: async () => {
              const ctx = await getOrLaunchChatGPTContext((msg) => api.logger.info(msg));
              if (ctx) {
                const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
                const { page } = await getOrCreateChatGPTPage(ctx);
                const editor = await page.locator("#prompt-textarea").isVisible().catch(() => false);
                if (editor) { chatgptContext = ctx; return ctx; }
              }
              return chatgptContext;
            },
            version: plugin.version,
            modelCommands,
            modelFallbacks,
            modelTimeouts,
            getExpiryInfo: () => ({
              grok:    (() => { const e = loadGrokExpiry();    return e ? formatExpiryInfo(e)    : null; })(),
              gemini:  (() => { const e = loadGeminiExpiry();  return e ? formatGeminiExpiry(e)  : null; })(),
              claude:  (() => { const e = loadClaudeExpiry();  return e ? formatClaudeExpiry(e)  : null; })(),
              chatgpt: (() => { const e = loadChatGPTExpiry(); return e ? formatChatGPTExpiry(e) : null; })(),
            }),
          });
          proxyServer = server;
          _proxyOwnedByThisProcess = true;
          api.logger.info(
            `[cli-bridge] proxy ready on :${port} — vllm/cli-gemini/* and vllm/cli-claude/* available`
          );

          // Warn if OpenClaw's LLM idle timeout is too low for CLI models.
          // CLI subprocesses (especially with large prompts) need time before producing
          // the first token. The default 60s causes premature 408 timeouts.
          const llmIdleTimeout = (api.pluginConfig as Record<string, unknown>)?._resolvedAgentDefaults?.llm?.idleTimeoutSeconds;
          if (llmIdleTimeout === undefined) {
            // Can't read the resolved config — check the raw file instead
            try {
              const ocConfig = JSON.parse(readFileSync(join(OPENCLAW_DIR, "openclaw.json"), "utf-8")) as Record<string, unknown>;
              const agentDefaults = (ocConfig?.agents as Record<string, unknown>)?.defaults as Record<string, unknown> | undefined;
              const llm = agentDefaults?.llm as Record<string, unknown> | undefined;
              const idle = llm?.idleTimeoutSeconds as number | undefined;
              if (idle === undefined || (idle > 0 && idle < 120)) {
                api.logger.warn(
                  `[cli-bridge] ⚠️  agents.defaults.llm.idleTimeoutSeconds is ${idle ?? "not set (default 60s)"} — ` +
                  `CLI models need at least 120–300s. Set to 300 in openclaw.json to prevent premature 408 timeouts.`
                );
              }
            } catch { /* non-fatal — just skip the check */ }
          }

          const result = patchOpencllawConfig(port);
          if (result.patched) {
            api.logger.info(
              `[cli-bridge] openclaw.json patched with vllm provider. Restart gateway to activate.`
            );
          }
        } catch (err: unknown) {
          const msg = (err as Error).message ?? String(err);
          if (msg.includes("EADDRINUSE")) {
            // Port is busy but probe didn't respond — maybe the old server is still shutting down.
            // Re-probe first: if it now responds, reuse it without rebinding.
            api.logger.warn(`[cli-bridge] port ${port} busy — re-probing before retry…`);
            await new Promise(r => setTimeout(r, 1500));
            const aliveNow = await probeExisting();
            if (aliveNow) {
              api.logger.info(`[cli-bridge] proxy now responding on :${port} — reusing`);
              return;
            }
            // Still not responding — wait for OS to release the port, then rebind
            api.logger.warn(`[cli-bridge] port ${port} still busy, waiting 1s for OS release…`);
            await new Promise((r) => setTimeout(r, 1000));
            // One final attempt
            try {
              const server = await startProxyServer({
                port, apiKey, timeoutMs, modelCommands, modelFallbacks, modelTimeouts,
                log: (msg) => api.logger.info(msg),
                warn: (msg) => api.logger.warn(msg),
                getGrokContext: () => grokContext,
                connectGrokContext: async () => {
                  const ctx = await connectToOpenClawBrowser((msg) => api.logger.info(msg));
                  if (ctx) {
                    const check = await verifySession(ctx, (msg) => api.logger.info(msg));
                    if (check.valid) { grokContext = ctx; return ctx; }
                  }
                  return null;
                },
                getGeminiContext: () => geminiContext,
                connectGeminiContext: async () => {
                  const ctx = await connectToOpenClawBrowser((msg) => api.logger.info(msg));
                  if (ctx) {
                    const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
                    const { page } = await getOrCreateGeminiPage(ctx);
                    const editor = await page.locator(".ql-editor").isVisible().catch(() => false);
                    if (editor) { geminiContext = ctx; return ctx; }
                  }
                  return geminiContext;
                },
                getClaudeContext: () => claudeWebContext,
                connectClaudeContext: async () => {
                  const ctx = await connectToOpenClawBrowser((msg) => api.logger.info(msg));
                  if (ctx) {
                    const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
                    const { page } = await getOrCreateClaudePage(ctx);
                    const editor = await page.locator(".ProseMirror").isVisible().catch(() => false);
                    if (editor) { claudeWebContext = ctx; return ctx; }
                  }
                  return claudeWebContext;
                },
                getChatGPTContext: () => chatgptContext,
                connectChatGPTContext: async () => {
                  const ctx = await connectToOpenClawBrowser((msg) => api.logger.info(msg));
                  if (ctx) {
                    const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
                    const { page } = await getOrCreateChatGPTPage(ctx);
                    const editor = await page.locator("#prompt-textarea").isVisible().catch(() => false);
                    if (editor) { chatgptContext = ctx; return ctx; }
                  }
                  return chatgptContext;
                },
              });
              proxyServer = server;
              api.logger.info(`[cli-bridge] proxy ready on :${port} (retry)`);
            } catch (e2: unknown) {
              api.logger.warn(`[cli-bridge] proxy unavailable after retry: ${(e2 as Error).message}`);
            }
          } else {
            api.logger.warn(`[cli-bridge] proxy failed to start on port ${port}: ${msg}`);
          }
        }
      };

      startProxy().catch(() => {});
    }

    // ── Cleanup: close proxy server on plugin stop (hot-reload / gateway restart) ──
    // Register a named service so OpenClaw can call stop() on plugin teardown.
    api.registerService({
      id: "cli-bridge-proxy",
      start: async () => { /* proxy already started above */ },
      stop: async () => {
        // Clean up browser resources first
        await cleanupBrowsers((msg) => api.logger.info(msg));

        if (proxyServer) {
          // closeAllConnections() forcefully terminates keep-alive connections
          // so that server.close() releases the port immediately rather than
          // waiting for them to drain. Without this, the port stays bound
          // during hot-reloads and the next start() call gets EADDRINUSE.
          if (typeof (proxyServer as any).closeAllConnections === "function") {
            (proxyServer as any).closeAllConnections();
          }
          await new Promise<void>((resolve) => {
            proxyServer!.close((err) => {
              if (err) api.logger.warn(`[cli-bridge] proxy close error: ${err.message}`);
              else api.logger.info(`[cli-bridge] proxy server closed on plugin stop`);
              resolve();
            });
          });
          proxyServer = null;
        }
      },
    });


    // ── Phase 3a: /cli-* model switch commands ─────────────────────────────────
    for (const entry of CLI_MODEL_COMMANDS) {
      const { name, model, description, label } = entry;
      api.registerCommand({
        name,
        description: `${description}. Pass --now to apply immediately (only between sessions!).`,
        acceptsArgs: true,
        requireAuth: false,
        handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
          const forceNow = (ctx.args ?? "").trim().toLowerCase().startsWith("--now");
          api.logger.info(`[cli-bridge] /${name} by ${ctx.senderId ?? "?"} forceNow=${forceNow}`);
          return switchModel(api, model, label, forceNow);
        },
      } satisfies OpenClawPluginCommandDefinition);
    }

    // ── Phase 3b: /cli-back — restore previous model ──────────────────────────
    api.registerCommand({
      name: "cli-back",
      description: "Restore the model active before the last /cli-* switch. Clears any pending staged switch.",
      requireAuth: false,
      handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
        api.logger.info(`[cli-bridge] /cli-back by ${ctx.senderId ?? "?"}`);

        // Clear any pending staged switch
        clearPending();

        const state = readState();
        if (!state?.previousModel) {
          return { text: "ℹ️ No previous model saved. Use `/cli-sonnet` etc. to switch first." };
        }

        const prev = state.previousModel;

        // Clear the saved state so a second /cli-back doesn't bounce back
        writeState({ previousModel: "" });

        try {
          const result = await api.runtime.system.runCommandWithTimeout(
            ["openclaw", "models", "set", prev],
            { timeoutMs: 8_000 }
          );

          if (result.code !== 0) {
            const err = (result.stderr || result.stdout || "unknown error").trim();
            return { text: `❌ Failed to restore \`${prev}\`: ${err}` };
          }

          api.logger.info(`[cli-bridge] /cli-back restored → ${prev}`);
          return { text: `✅ Restored previous model\n\`${prev}\`` };
        } catch (err) {
          return { text: `❌ Error: ${(err as Error).message}` };
        }
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 3b2: /cli-apply — apply staged model switch ─────────────────────
    api.registerCommand({
      name: "cli-apply",
      description: "Apply a staged /cli-* model switch. Use this AFTER finishing your current task.",
      requireAuth: false,
      handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
        api.logger.info(`[cli-bridge] /cli-apply by ${ctx.senderId ?? "?"}`);

        const pending = readPending();
        if (!pending) {
          const current = readCurrentModel();
          return {
            text:
              `ℹ️ No staged switch pending.\n` +
              `Current model: \`${current ?? "unknown"}\`\n\n` +
              `Use \`/cli-sonnet\`, \`/cli-opus\` etc. to stage a switch.`,
          };
        }

        api.logger.info(`[cli-bridge] applying staged switch → ${pending.model}`);
        return applyModelSwitch(api, pending.model, pending.label);
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 3b3: /cli-pending — show staged switch ───────────────────────────
    api.registerCommand({
      name: "cli-pending",
      description: "Show the currently staged model switch (if any).",
      requireAuth: false,
      handler: async (): Promise<PluginCommandResult> => {
        const pending = readPending();
        const current = readCurrentModel();
        if (!pending) {
          return {
            text:
              `✅ No pending switch.\n` +
              `Current model: \`${current ?? "unknown"}\``,
          };
        }
        return {
          text:
            `📋 **Staged switch pending:**\n` +
            `→ \`${pending.model}\` (${pending.label})\n` +
            `Requested: ${pending.requestedAt}\n\n` +
            `Current: \`${current ?? "unknown"}\`\n\n` +
            `Run \`/cli-apply\` to apply after finishing your current task.\n` +
            `Run \`/cli-sonnet --now\` etc. to discard and switch immediately.`,
        };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 3c: /cli-test — one-shot proxy ping, no global model switch ──────
    api.registerCommand({
      name: "cli-test",
      description: "Test the CLI bridge proxy without switching your active model. Usage: /cli-test [model]",
      acceptsArgs: true,
      requireAuth: false,
      handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
        const targetModel = ctx.args?.trim() || CLI_TEST_DEFAULT_MODEL;
        // Accept short names like "cli-sonnet" or full "vllm/cli-claude/claude-sonnet-4-6"
        const model = targetModel.startsWith("vllm/")
          ? targetModel
          : `vllm/${targetModel}`;

        api.logger.info(`[cli-bridge] /cli-test → ${model} by ${ctx.senderId ?? "?"}`);

        if (!enableProxy) {
          return { text: "❌ Proxy is disabled (enableProxy: false in config)." };
        }

        const current = readCurrentModel();
        const testTimeoutMs = Math.min(timeoutMs, 30_000);

        try {
          const start = Date.now();
          const response = await proxyTestRequest(port, apiKey, model, testTimeoutMs);
          const elapsed = Date.now() - start;

          return {
            text:
              `🧪 **CLI Bridge Test**\n` +
              `Model: \`${model}\`\n` +
              `Response: _${response}_\n` +
              `Latency: ${elapsed}ms\n\n` +
              `Active model unchanged: \`${current ?? "unknown"}\``,
          };
        } catch (err) {
          return {
            text:
              `❌ **CLI Bridge Test Failed**\n` +
              `Model: \`${model}\`\n` +
              `Error: ${(err as Error).message}\n\n` +
              `Active model unchanged: \`${current ?? "unknown"}\``,
          };
        }
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 3d: /cli-list — formatted model overview ────────────────────────
    api.registerCommand({
      name: "cli-list",
      description: "List all registered CLI bridge models and their commands.",
      requireAuth: false,
      handler: async (): Promise<PluginCommandResult> => {
        const groups: Record<string, { cmd: string; model: string }[]> = {
          "Claude Code CLI": [],
          "Gemini CLI": [],
          "Codex (OAuth)": [],
        };

        for (const c of CLI_MODEL_COMMANDS) {
          const entry = { cmd: `/${c.name}`, model: c.model };
          if (c.model.startsWith("vllm/cli-claude/")) groups["Claude Code CLI"].push(entry);
          else if (c.model.startsWith("vllm/cli-gemini/")) groups["Gemini CLI"].push(entry);
          else groups["Codex (OAuth)"].push(entry);
        }

        const lines: string[] = ["🤖 *CLI Bridge Models*", ""];
        for (const [group, entries] of Object.entries(groups)) {
          if (entries.length === 0) continue;
          lines.push(`*${group}*`);
          for (const { cmd, model } of entries) {
            const modelId = model.replace(/^vllm\/cli-(claude|gemini)\//, "").replace(/^openai-codex\//, "");
            lines.push(`  ${cmd.padEnd(20)} ${modelId}`);
          }
          lines.push("");
        }
        const pending = readPending();
        const pendingNote = pending ? ` ← pending: ${pending.label}` : "";

        lines.push("*Utility*");
        lines.push(`  /cli-apply           Apply staged switch${pendingNote}`);
        lines.push("  /cli-pending         Show staged switch (if any)");
        lines.push("  /cli-back            Restore previous model + clear staged");
        lines.push("  /cli-test [model]    Health check (no model switch)");
        lines.push("  /cli-list            This overview");
        lines.push("  /cli-help            Connected providers + examples + dashboard link");
        lines.push("");
        lines.push("*Switching safely:*");
        lines.push("  /cli-sonnet          → stages switch (safe, apply later)");
        lines.push("  /cli-sonnet --now    → immediate switch (only between sessions!)");
        lines.push("");
        lines.push(`Proxy: \`127.0.0.1:${port}\`  ·  Dashboard: http://127.0.0.1:${port}/status`);

        return { text: lines.join("\n") };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 3e: /cli-help — context-aware help with connected providers ─────
    api.registerCommand({
      name: "cli-help",
      description: "Show available models based on currently connected providers, with example commands and status page link.",
      requireAuth: false,
      handler: async (): Promise<PluginCommandResult> => {
        const lines: string[] = [`🌉 *CLI Bridge Help* — v${plugin.version}`, ""];

        // ── CLI models (always available — spawns local CLI) ────────────────
        lines.push("*CLI Models* (always available — uses locally installed CLIs)");
        lines.push("");
        const cliGroups: Record<string, typeof CLI_MODEL_COMMANDS[number][]> = {
          "Claude Code": [],
          "Gemini": [],
        };
        for (const c of CLI_MODEL_COMMANDS) {
          if (c.model.startsWith("vllm/cli-claude/")) cliGroups["Claude Code"].push(c);
          else if (c.model.startsWith("vllm/cli-gemini/")) cliGroups["Gemini"].push(c);
        }
        for (const [group, entries] of Object.entries(cliGroups)) {
          if (entries.length === 0) continue;
          lines.push(`  *${group}*`);
          for (const c of entries) {
            const modelShort = c.model.replace(/^vllm\/cli-(claude|gemini)\//, "");
            lines.push(`    \`/${c.name}\`  →  ${modelShort}`);
          }
        }
        lines.push("");

        // ── Codex models (OAuth — always registered) ────────────────────────
        const codexEntries = CLI_MODEL_COMMANDS.filter(c => c.model.startsWith("openai-codex/"));
        if (codexEntries.length > 0) {
          lines.push("*Codex* (OAuth — direct API, no proxy)");
          for (const c of codexEntries) {
            const modelShort = c.model.replace(/^openai-codex\//, "");
            lines.push(`    \`/${c.name}\`  →  ${modelShort}`);
          }
          lines.push("");
        }

        // ── Web session models (only if connected) ──────────────────────────
        const webProviders: Array<{
          name: string;
          ctx: BrowserContext | null;
          models: string[];
          cmds: string[];
          loginCmd: string;
          expiry: string | null;
        }> = [
          {
            name: "Grok",
            ctx: grokContext,
            models: ["web-grok/grok-3", "web-grok/grok-3-fast", "web-grok/grok-3-mini", "web-grok/grok-3-mini-fast"],
            cmds: ["openclaw models set vllm/web-grok/grok-3"],
            loginCmd: "/grok-login",
            expiry: (() => { const e = loadGrokExpiry(); return e ? formatExpiryInfo(e) : null; })(),
          },
          {
            name: "Gemini (web)",
            ctx: geminiContext,
            models: ["web-gemini/gemini-2-5-pro", "web-gemini/gemini-2-5-flash", "web-gemini/gemini-3-pro", "web-gemini/gemini-3-flash"],
            cmds: ["openclaw models set vllm/web-gemini/gemini-2-5-pro"],
            loginCmd: "/gemini-login",
            expiry: (() => { const e = loadGeminiExpiry(); return e ? formatGeminiExpiry(e) : null; })(),
          },
          {
            name: "Claude.ai (web)",
            ctx: claudeWebContext,
            models: ["web-claude/*"],
            cmds: [],
            loginCmd: "/claude-login",
            expiry: (() => { const e = loadClaudeExpiry(); return e ? formatClaudeExpiry(e) : null; })(),
          },
          {
            name: "ChatGPT (web)",
            ctx: chatgptContext,
            models: ["web-chatgpt/*"],
            cmds: [],
            loginCmd: "/chatgpt-login",
            expiry: (() => { const e = loadChatGPTExpiry(); return e ? formatChatGPTExpiry(e) : null; })(),
          },
        ];

        const connectedWeb = webProviders.filter(p => p.ctx !== null);
        const disconnectedWeb = webProviders.filter(p => p.ctx === null);

        if (connectedWeb.length > 0) {
          lines.push("*Web Session Models* (connected)");
          for (const p of connectedWeb) {
            const expiryNote = p.expiry ? ` — ${p.expiry}` : "";
            lines.push(`  🟢 *${p.name}*${expiryNote}`);
            lines.push(`    Models: ${p.models.join(", ")}`);
            if (p.cmds.length > 0) {
              lines.push(`    Example: \`${p.cmds[0]}\``);
            }
          }
          lines.push("");
        }

        if (disconnectedWeb.length > 0) {
          lines.push("*Web Session Models* (not connected)");
          for (const p of disconnectedWeb) {
            const expiryNote = p.expiry && !p.expiry.startsWith("⚠️ EXPIRED") ? " (cookies valid, auto-connects on use)" : "";
            lines.push(`  ⚪ *${p.name}*${expiryNote}  →  run \`${p.loginCmd}\``);
          }
          lines.push("");
        }

        // ── BitNet ──────────────────────────────────────────────────────────
        const bitnetOk = await checkBitNetServer();
        if (bitnetOk) {
          lines.push("*Local Inference*");
          lines.push("  🟢 *BitNet 2B* — running  →  \`/cli-bitnet\`");
        } else {
          lines.push("*Local Inference*");
          lines.push("  ⚪ *BitNet 2B* — not running  →  \`sudo systemctl start bitnet-server\`");
        }
        lines.push("");

        // ── Utility commands ────────────────────────────────────────────────
        lines.push("*Utility Commands*");
        lines.push("  \`/cli-help\`             This help");
        lines.push("  \`/cli-list\`             All models (no status check)");
        lines.push("  \`/cli-test [model]\`     Health check (no model switch)");
        lines.push("  \`/cli-back\`             Restore previous model");
        lines.push("  \`/cli-apply\`            Apply staged model switch");
        lines.push("  \`/bridge-status\`        Full provider diagnostics");
        lines.push("");

        // ── Quick examples ──────────────────────────────────────────────────
        lines.push("*Quick Examples*");
        lines.push("  \`/cli-sonnet\`           Switch to Claude Sonnet (staged)");
        lines.push("  \`/cli-sonnet --now\`     Switch immediately");
        lines.push("  \`/cli-gemini\`           Switch to Gemini 2.5 Pro");
        lines.push("  \`/cli-codex\`            Switch to GPT-5.3 Codex");
        lines.push("");

        // ── Status page link ────────────────────────────────────────────────
        lines.push(`📊 Dashboard: http://127.0.0.1:${port}/status`);
        lines.push(`🔍 Health JSON: http://127.0.0.1:${port}/healthz`);

        return { text: lines.join("\n") };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Phase 4: Grok web-session commands ────────────────────────────────────

    api.registerCommand({
      name: "grok-login",
      description: "Authenticate grok.com: imports cookies from OpenClaw browser into persistent profile",
      handler: async (): Promise<PluginCommandResult> => {
        if (grokContext) {
          const check = await verifySession(grokContext, (msg) => api.logger.info(msg));
          if (check.valid) {
            return { text: "✅ Already connected to grok.com. Use `/grok-logout` first to reset." };
          }
          grokContext = null;
        }
        api.logger.info("[cli-bridge:grok] /grok-login: importing session from OpenClaw browser…");
        const { chromium } = await import("playwright");

        // Step 1: try to grab cookies from the OpenClaw browser (user must have grok.com open)
        let importedCookies: unknown[] = [];
        try {
          const ocBrowser = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 3000 });
          const ocCtx = ocBrowser.contexts()[0];
          if (ocCtx) {
            importedCookies = await ocCtx.cookies(["https://grok.com", "https://x.ai", "https://accounts.x.ai"]);
            api.logger.info(`[cli-bridge:grok] imported ${importedCookies.length} cookies from OpenClaw browser`);
          }
          await ocBrowser.close().catch(() => {});
        } catch {
          api.logger.info("[cli-bridge:grok] OpenClaw browser not available — using saved profile");
        }

        // Step 2: launch/connect persistent context and inject cookies
        const ctx = await getOrLaunchGrokContext((msg) => api.logger.info(msg));
        if (!ctx) return { text: "❌ Could not launch browser. Check server logs." };

        if (importedCookies.length > 0) {
          await ctx.addCookies(importedCookies as Parameters<typeof ctx.addCookies>[0]);
          api.logger.info(`[cli-bridge:grok] cookies injected into persistent profile`);
        }

        // Step 3: navigate to grok.com and verify
        const pages = ctx.pages();
        const page = pages.find(p => p.url().includes("grok.com")) ?? await ctx.newPage();
        if (!page.url().includes("grok.com")) {
          await page.goto("https://grok.com", { waitUntil: "domcontentloaded", timeout: 15_000 });
        }

        const check = await verifySession(ctx, (msg) => api.logger.info(msg));
        if (!check.valid) {
          return { text: `❌ Session not valid: ${check.reason}\n\nMake sure grok.com is open in your browser and you're logged in, then run /grok-login again.` };
        }
        grokContext = ctx;

        // Scan cookie expiry and persist it
        const expiry = await scanCookieExpiry(ctx);
        if (expiry) {
          saveGrokExpiry(expiry);
          api.logger.info(`[cli-bridge:grok] cookie expiry: ${new Date(expiry.expiresAt).toISOString()}`);
        }
        const expiryLine = expiry ? `\n\n🕐 Cookie expiry: ${formatExpiryInfo(expiry)}` : "";

        return { text: `✅ Grok session ready!\n\nModels available:\n• \`vllm/web-grok/grok-3\`\n• \`vllm/web-grok/grok-3-fast\`\n• \`vllm/web-grok/grok-3-mini\`\n• \`vllm/web-grok/grok-3-mini-fast\`${expiryLine}` };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "grok-status",
      description: "Check grok.com session status",
      handler: async (): Promise<PluginCommandResult> => {
        if (!grokContext) {
          return { text: "❌ No active grok.com session\nRun `/grok-login` to authenticate." };
        }
        const check = await verifySession(grokContext, (msg) => api.logger.info(msg));
        if (check.valid) {
          const expiry = loadGrokExpiry();
          const expiryLine = expiry ? `\n🕐 ${formatExpiryInfo(expiry)}` : "";
          return { text: `✅ grok.com session active\nProxy: \`127.0.0.1:${port}\`\nModels: web-grok/grok-3, web-grok/grok-3-fast, web-grok/grok-3-mini, web-grok/grok-3-mini-fast${expiryLine}` };
        }
        grokContext = null;
        return { text: `❌ Session expired: ${check.reason}\nRun \`/grok-login\` to re-authenticate.` };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "grok-logout",
      description: "Disconnect from grok.com session (does not close the browser)",
      handler: async (): Promise<PluginCommandResult> => {
        grokContext = null;
        deleteSession(grokSessionPath);
        return { text: "✅ Disconnected from grok.com. Run `/grok-login` to reconnect." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Gemini web-session commands ───────────────────────────────────────────
    api.registerCommand({
      name: "gemini-login",
      description: "Authenticate gemini.google.com: imports session from OpenClaw browser",
      handler: async (): Promise<PluginCommandResult> => {
        if (geminiContext) {
          const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
          try {
            const { page } = await getOrCreateGeminiPage(geminiContext);
            const editor = await page.locator(".ql-editor").isVisible().catch(() => false);
            if (editor) return { text: "✅ Already connected to gemini.google.com. Use `/gemini-logout` first to reset." };
          } catch { /* fall through */ }
          geminiContext = null;
        }

        api.logger.info("[cli-bridge:gemini] /gemini-login: connecting…");

        // Step 1: try to grab cookies from OpenClaw browser (CDP) if available
        let importedCookies: unknown[] = [];
        try {
          const { chromium } = await import("playwright");
          const ocBrowser = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 3000 });
          const ocCtx = ocBrowser.contexts()[0];
          if (ocCtx) {
            importedCookies = await ocCtx.cookies(["https://gemini.google.com", "https://accounts.google.com", "https://google.com"]);
            api.logger.info(`[cli-bridge:gemini] imported ${importedCookies.length} cookies from OpenClaw browser`);
          }
          await ocBrowser.close().catch(() => {});
        } catch {
          api.logger.info("[cli-bridge:gemini] OpenClaw browser not available — using saved profile");
        }

        // Step 2: get or launch persistent context
        const ctx = await getOrLaunchGeminiContext((msg) => api.logger.info(msg));
        if (!ctx) return { text: "❌ Could not launch browser. Check server logs." };

        // Step 3: inject imported cookies if available
        if (importedCookies.length > 0) {
          await ctx.addCookies(importedCookies as Parameters<typeof ctx.addCookies>[0]);
          api.logger.info("[cli-bridge:gemini] cookies injected into persistent profile");
        }

        // Step 4: navigate and verify
        const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
        let page;
        try {
          ({ page } = await getOrCreateGeminiPage(ctx));
        } catch (err) {
          return { text: `❌ Failed to open gemini.google.com: ${(err as Error).message}` };
        }

        let editor = await page.locator(".ql-editor").isVisible().catch(() => false);
        if (!editor) {
          // Headless failed — launch headed browser for interactive login
          api.logger.info("[cli-bridge:gemini] headless login failed — launching headed browser for manual login…");
          try { await ctx.close(); } catch { /* ignore */ }
          geminiContext = null;

          const { chromium } = await import("playwright");
          const headedCtx = await chromium.launchPersistentContext(GEMINI_PROFILE_DIR, {
            headless: false,
            channel: "chrome",
            args: STEALTH_ARGS,
            ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
          });
          const loginPage = await headedCtx.newPage();
          await loginPage.goto("https://gemini.google.com/app", { waitUntil: "domcontentloaded", timeout: 15_000 });

          api.logger.info("[cli-bridge:gemini] waiting for manual login (5 min timeout)…");
          try {
            await loginPage.waitForSelector(".ql-editor", { timeout: 300_000 });
          } catch {
            await headedCtx.close().catch(() => {});
            return { text: "❌ Login timeout — Gemini editor did not appear within 5 minutes." };
          }

          geminiContext = headedCtx;
          headedCtx.on("close", () => { geminiContext = null; });
          editor = true;
          page = loginPage;
        } else {
          geminiContext = ctx;
        }

        const expiry = await scanGeminiCookieExpiry(geminiContext!);
        if (expiry) {
          saveGeminiExpiry(expiry);
          api.logger.info(`[cli-bridge:gemini] cookie expiry: ${new Date(expiry.expiresAt).toISOString()}`);
        }
        const expiryLine = expiry ? `\n\n🕐 Cookie expiry: ${formatGeminiExpiry(expiry)}` : "";

        return { text: `✅ Gemini session ready!\n\nModels available:\n• \`vllm/web-gemini/gemini-2-5-pro\`\n• \`vllm/web-gemini/gemini-2-5-flash\`\n• \`vllm/web-gemini/gemini-3-pro\`\n• \`vllm/web-gemini/gemini-3-flash\`${expiryLine}` };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "gemini-status",
      description: "Check gemini.google.com session status",
      handler: async (): Promise<PluginCommandResult> => {
        if (!geminiContext) {
          return { text: "❌ No active gemini.google.com session\nRun `/gemini-login` to authenticate." };
        }
        const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
        try {
          const { page } = await getOrCreateGeminiPage(geminiContext);
          const editor = await page.locator(".ql-editor").isVisible().catch(() => false);
          if (editor) {
            const expiry = loadGeminiExpiry();
            const expiryLine = expiry ? `\n🕐 ${formatGeminiExpiry(expiry)}` : "";
            return { text: `✅ gemini.google.com session active\nProxy: \`127.0.0.1:${port}\`\nModels: web-gemini/gemini-2-5-pro, gemini-2-5-flash, gemini-3-pro, gemini-3-flash${expiryLine}` };
          }
        } catch { /* fall through */ }
        geminiContext = null;
        return { text: "❌ Session lost — run `/gemini-login` to re-authenticate." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "gemini-logout",
      description: "Disconnect from gemini.google.com session",
      handler: async (): Promise<PluginCommandResult> => {
        geminiContext = null;
        return { text: "✅ Disconnected from gemini.google.com. Run `/gemini-login` to reconnect." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── Claude.ai web-session commands ─────────────────────────────────────────
    api.registerCommand({
      name: "claude-login",
      description: "Authenticate claude.ai: imports cookies from OpenClaw browser into persistent profile",
      handler: async (): Promise<PluginCommandResult> => {
        if (claudeWebContext) {
          const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
          try {
            const { page } = await getOrCreateClaudePage(claudeWebContext);
            const editor = await page.locator(".ProseMirror").isVisible().catch(() => false);
            if (editor) return { text: "✅ Already connected to claude.ai. Use `/claude-logout` first to reset." };
          } catch { /* fall through */ }
          claudeWebContext = null;
        }

        api.logger.info("[cli-bridge:claude-web] /claude-login: connecting…");

        // Step 1: try to grab cookies from OpenClaw browser (CDP)
        let importedCookies: unknown[] = [];
        try {
          const { chromium } = await import("playwright");
          const ocBrowser = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 3000 });
          const ocCtx = ocBrowser.contexts()[0];
          if (ocCtx) {
            importedCookies = await ocCtx.cookies(["https://claude.ai"]);
            api.logger.info(`[cli-bridge:claude-web] imported ${importedCookies.length} cookies from OpenClaw browser`);
          }
          await ocBrowser.close().catch(() => {});
        } catch {
          api.logger.info("[cli-bridge:claude-web] OpenClaw browser not available — using saved profile");
        }

        // Step 2: get or launch persistent context
        const ctx = await getOrLaunchClaudeContext((msg) => api.logger.info(msg));
        if (!ctx) return { text: "❌ Could not launch browser. Check server logs." };

        // Step 3: inject imported cookies
        if (importedCookies.length > 0) {
          await ctx.addCookies(importedCookies as Parameters<typeof ctx.addCookies>[0]);
          api.logger.info("[cli-bridge:claude-web] cookies injected into persistent profile");
        }

        // Step 4: navigate and verify
        const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
        let page;
        try {
          ({ page } = await getOrCreateClaudePage(ctx));
        } catch (err) {
          return { text: `❌ Failed to open claude.ai: ${(err as Error).message}` };
        }

        let editor = await page.locator(".ProseMirror").isVisible().catch(() => false);
        if (!editor) {
          // Headless failed — launch headed browser for interactive login
          api.logger.info("[cli-bridge:claude-web] headless login failed — launching headed browser for manual login…");
          try { await ctx.close(); } catch { /* ignore */ }
          claudeWebContext = null;

          const { chromium } = await import("playwright");
          const headedCtx = await chromium.launchPersistentContext(CLAUDE_PROFILE_DIR, {
            headless: false,
            channel: "chrome",
            args: STEALTH_ARGS,
            ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
          });
          const loginPage = await headedCtx.newPage();
          await loginPage.goto("https://claude.ai/new", { waitUntil: "domcontentloaded", timeout: 15_000 });

          api.logger.info("[cli-bridge:claude-web] waiting for manual login (5 min timeout)…");
          try {
            await loginPage.waitForSelector(".ProseMirror", { timeout: 300_000 });
          } catch {
            await headedCtx.close().catch(() => {});
            return { text: "❌ Login timeout — Claude editor did not appear within 5 minutes." };
          }

          claudeWebContext = headedCtx;
          headedCtx.on("close", () => { claudeWebContext = null; });
          editor = true;
          page = loginPage;
        } else {
          claudeWebContext = ctx;
        }

        const expiry = await scanClaudeCookieExpiry(claudeWebContext!);
        if (expiry) {
          saveClaudeExpiry(expiry);
          api.logger.info(`[cli-bridge:claude-web] cookie expiry: ${new Date(expiry.expiresAt).toISOString()}`);
        }
        const expiryLine = expiry ? `\n\n🕐 Cookie expiry: ${formatClaudeExpiry(expiry)}` : "";

        return { text: `✅ Claude.ai session ready!\n\nModels available:\n• \`vllm/web-claude/claude-sonnet\`\n• \`vllm/web-claude/claude-opus\`\n• \`vllm/web-claude/claude-haiku\`${expiryLine}` };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "claude-status",
      description: "Check claude.ai session status",
      handler: async (): Promise<PluginCommandResult> => {
        if (!claudeWebContext) {
          return { text: "❌ No active claude.ai session\nRun `/claude-login` to authenticate." };
        }
        const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
        try {
          const { page } = await getOrCreateClaudePage(claudeWebContext);
          const editor = await page.locator(".ProseMirror").isVisible().catch(() => false);
          if (editor) {
            const expiry = loadClaudeExpiry();
            const expiryLine = expiry ? `\n🕐 ${formatClaudeExpiry(expiry)}` : "";
            return { text: `✅ claude.ai session active\nProxy: \`127.0.0.1:${port}\`\nModels: web-claude/claude-sonnet, claude-opus, claude-haiku${expiryLine}` };
          }
        } catch { /* fall through */ }
        claudeWebContext = null;
        return { text: "❌ Session lost — run `/claude-login` to re-authenticate." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "claude-logout",
      description: "Disconnect from claude.ai session",
      handler: async (): Promise<PluginCommandResult> => {
        claudeWebContext = null;
        return { text: "✅ Disconnected from claude.ai. Run `/claude-login` to reconnect." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── ChatGPT web-session commands ─────────────────────────────────────────
    api.registerCommand({
      name: "chatgpt-login",
      description: "Authenticate chatgpt.com: imports cookies from OpenClaw browser into persistent profile",
      handler: async (): Promise<PluginCommandResult> => {
        if (chatgptContext) {
          const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
          try {
            const { page } = await getOrCreateChatGPTPage(chatgptContext);
            const editor = await page.locator("#prompt-textarea").isVisible().catch(() => false);
            if (editor) return { text: "✅ Already connected to chatgpt.com. Use `/chatgpt-logout` first to reset." };
          } catch { /* fall through */ }
          chatgptContext = null;
        }

        api.logger.info("[cli-bridge:chatgpt] /chatgpt-login: connecting…");

        // Step 1: try to grab cookies from OpenClaw browser (CDP)
        let importedCookies: unknown[] = [];
        try {
          const { chromium } = await import("playwright");
          const ocBrowser = await chromium.connectOverCDP("http://127.0.0.1:18800", { timeout: 3000 });
          const ocCtx = ocBrowser.contexts()[0];
          if (ocCtx) {
            importedCookies = await ocCtx.cookies(["https://chatgpt.com", "https://auth0.openai.com", "https://openai.com"]);
            api.logger.info(`[cli-bridge:chatgpt] imported ${importedCookies.length} cookies from OpenClaw browser`);
          }
          await ocBrowser.close().catch(() => {});
        } catch {
          api.logger.info("[cli-bridge:chatgpt] OpenClaw browser not available — using saved profile");
        }

        // Step 2: get or launch persistent context
        const ctx = await getOrLaunchChatGPTContext((msg) => api.logger.info(msg));
        if (!ctx) return { text: "❌ Could not launch browser. Check server logs." };

        // Step 3: inject imported cookies
        if (importedCookies.length > 0) {
          await ctx.addCookies(importedCookies as Parameters<typeof ctx.addCookies>[0]);
          api.logger.info("[cli-bridge:chatgpt] cookies injected into persistent profile");
        }

        // Step 4: navigate and verify
        const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
        let page;
        try {
          ({ page } = await getOrCreateChatGPTPage(ctx));
        } catch (err) {
          return { text: `❌ Failed to open chatgpt.com: ${(err as Error).message}` };
        }

        let editor = await page.locator("#prompt-textarea").isVisible().catch(() => false);
        if (!editor) {
          // Headless failed — launch headed browser for interactive login
          api.logger.info("[cli-bridge:chatgpt] headless login failed — launching headed browser for manual login…");
          try { await ctx.close(); } catch { /* ignore */ }
          chatgptContext = null;

          const { chromium } = await import("playwright");
          const headedCtx = await chromium.launchPersistentContext(CHATGPT_PROFILE_DIR, {
            headless: false,
            channel: "chrome",
            args: STEALTH_ARGS,
            ignoreDefaultArgs: [...STEALTH_IGNORE_DEFAULTS],
          });
          const loginPage = await headedCtx.newPage();
          await loginPage.goto("https://chatgpt.com", { waitUntil: "domcontentloaded", timeout: 15_000 });

          api.logger.info("[cli-bridge:chatgpt] waiting for manual login (5 min timeout)…");
          try {
            await loginPage.waitForSelector("#prompt-textarea", { timeout: 300_000 });
          } catch {
            await headedCtx.close().catch(() => {});
            return { text: "❌ Login timeout — ChatGPT editor did not appear within 5 minutes." };
          }

          chatgptContext = headedCtx;
          headedCtx.on("close", () => { chatgptContext = null; });
          editor = true;
          page = loginPage;
        } else {
          chatgptContext = ctx;
        }

        const expiry = await scanChatGPTCookieExpiry(chatgptContext!);
        if (expiry) {
          saveChatGPTExpiry(expiry);
          api.logger.info(`[cli-bridge:chatgpt] cookie expiry: ${new Date(expiry.expiresAt).toISOString()}`);
        }
        const expiryLine = expiry ? `\n\n🕐 Cookie expiry: ${formatChatGPTExpiry(expiry)}` : "";

        return { text: `✅ ChatGPT session ready!\n\nModels available:\n• \`vllm/web-chatgpt/gpt-4o\`\n• \`vllm/web-chatgpt/gpt-4o-mini\`\n• \`vllm/web-chatgpt/gpt-4.1\`\n• \`vllm/web-chatgpt/gpt-4.1-mini\`\n• \`vllm/web-chatgpt/o3\`\n• \`vllm/web-chatgpt/o4-mini\`\n• \`vllm/web-chatgpt/gpt-5\`\n• \`vllm/web-chatgpt/gpt-5-mini\`${expiryLine}` };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "chatgpt-status",
      description: "Check chatgpt.com session status",
      handler: async (): Promise<PluginCommandResult> => {
        if (!chatgptContext) {
          return { text: "❌ No active chatgpt.com session\nRun `/chatgpt-login` to authenticate." };
        }
        const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
        try {
          const { page } = await getOrCreateChatGPTPage(chatgptContext);
          const editor = await page.locator("#prompt-textarea").isVisible().catch(() => false);
          if (editor) {
            const expiry = loadChatGPTExpiry();
            const expiryLine = expiry ? `\n🕐 ${formatChatGPTExpiry(expiry)}` : "";
            return { text: `✅ chatgpt.com session active\nProxy: \`127.0.0.1:${port}\`\nModels: web-chatgpt/gpt-4o, gpt-4o-mini, gpt-4.1, gpt-4.1-mini, o3, o4-mini, gpt-5, gpt-5-mini${expiryLine}` };
          }
        } catch { /* fall through */ }
        chatgptContext = null;
        return { text: "❌ Session lost — run `/chatgpt-login` to re-authenticate." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    api.registerCommand({
      name: "chatgpt-logout",
      description: "Disconnect from chatgpt.com session",
      handler: async (): Promise<PluginCommandResult> => {
        chatgptContext = null;
        return { text: "✅ Disconnected from chatgpt.com. Run `/chatgpt-login` to reconnect." };
      },
    } satisfies OpenClawPluginCommandDefinition);

    // ── /bridge-status — all providers at a glance ───────────────────────────
    api.registerCommand({
      name: "bridge-status",
      description: "Show status of all headless browser providers (Grok, Gemini, Claude, ChatGPT)",
      handler: async (): Promise<PluginCommandResult> => {
        const lines: string[] = [`🌉 *CLI Bridge v${plugin.version} — Provider Status*\n`];

        const checks = [
          {
            name: "Grok",
            ctx: grokContext,
            check: async () => {
              if (!grokContext) return false;
              const r = await verifySession(grokContext, () => {});
              if (!r.valid) { grokContext = null; }
              return r.valid;
            },
            models: "web-grok/grok-3, grok-3-fast, grok-3-mini",
            loginCmd: "/grok-login",
            expiry: () => { const e = loadGrokExpiry(); return e ? formatExpiryInfo(e) : null; },
          },
          {
            name: "Gemini",
            ctx: geminiContext,
            check: async () => {
              if (!geminiContext) return false;
              try {
                const { getOrCreateGeminiPage } = await import("./src/gemini-browser.js");
                const { page } = await getOrCreateGeminiPage(geminiContext);
                return page.locator(".ql-editor").isVisible().catch(() => false);
              } catch { geminiContext = null; return false; }
            },
            models: "web-gemini/gemini-2-5-pro, gemini-2-5-flash, gemini-3-pro, gemini-3-flash",
            loginCmd: "/gemini-login",
            expiry: () => { const e = loadGeminiExpiry(); return e ? formatGeminiExpiry(e) : null; },
          },
          {
            name: "Claude.ai",
            ctx: claudeWebContext,
            check: async () => {
              if (!claudeWebContext) return false;
              try {
                const { getOrCreateClaudePage } = await import("./src/claude-browser.js");
                const { page } = await getOrCreateClaudePage(claudeWebContext);
                return page.locator(".ProseMirror").isVisible().catch(() => false);
              } catch { claudeWebContext = null; return false; }
            },
            models: "web-claude/claude-sonnet, claude-opus, claude-haiku",
            loginCmd: "/claude-login",
            expiry: () => { const e = loadClaudeExpiry(); return e ? formatClaudeExpiry(e) : null; },
          },
          {
            name: "ChatGPT",
            ctx: chatgptContext,
            check: async () => {
              if (!chatgptContext) return false;
              try {
                const { getOrCreateChatGPTPage } = await import("./src/chatgpt-browser.js");
                const { page } = await getOrCreateChatGPTPage(chatgptContext);
                return page.locator("#prompt-textarea").isVisible().catch(() => false);
              } catch { chatgptContext = null; return false; }
            },
            models: "web-chatgpt/gpt-4o, gpt-4o-mini, gpt-4.1, gpt-4.1-mini, o3, o4-mini, gpt-5, gpt-5-mini",
            loginCmd: "/chatgpt-login",
            expiry: () => { const e = loadChatGPTExpiry(); return e ? formatChatGPTExpiry(e) : null; },
          },
        ];

        for (const c of checks) {
          const expiry = c.expiry();
          const inMemory = c.ctx !== null;
          const liveOk = inMemory ? await c.check() : false;

          // Cookie-based status: treat as "logged in" if expiry file exists and not expired
          // ⚠️ EXPIRED = truly expired, 🚨 = expiring soon (still valid), ✅ = fine
          // This reflects actual login state independent of in-memory context
          const cookieExpired = expiry !== null && expiry.startsWith("⚠️ EXPIRED");
          const cookieValid = expiry !== null && !cookieExpired;

          if (liveOk) {
            // In-memory context active and verified
            lines.push(`✅ *${c.name}* — active (browser connected)`);
            if (expiry) lines.push(`   🕐 ${expiry}`);
            lines.push(`   Models: ${c.models}`);
          } else if (cookieValid) {
            // Not in memory yet, but cookies are valid — will auto-connect on next request
            lines.push(`🟡 *${c.name}* — logged in, browser not loaded`);
            lines.push(`   🕐 ${expiry}`);
            lines.push(`   Models: ${c.models}`);
            lines.push(`   ℹ️ Browser launches on first request`);
          } else if (cookieExpired) {
            // Cookies expired — needs re-login
            lines.push(`🔴 *${c.name}* — session expired (run \`${c.loginCmd}\`)`);
            if (expiry) lines.push(`   🕐 ${expiry}`);
          } else {
            // No cookie file at all — never logged in
            lines.push(`⚪ *${c.name}* — never logged in (run \`${c.loginCmd}\`)`);
          }
          lines.push("");
        }

        // ── BitNet local inference ──────────────────────────────────────────────
        const bitnetOk = await checkBitNetServer();
        if (bitnetOk) {
          lines.push(`✅ *BitNet (local)* — running at 127.0.0.1:8082`);
          lines.push(`   Models: local-bitnet/bitnet-2b`);
        } else {
          lines.push(`❌ *BitNet (local)* — not running (\`sudo systemctl start bitnet-server\`)`);
        }
        lines.push("");

        lines.push(`🔌 Proxy: \`127.0.0.1:${port}\``);
        return { text: lines.join("\n") };
      },
    } satisfies OpenClawPluginCommandDefinition);
    // ─────────────────────────────────────────────────────────────────────────

    const allCommands = [
      ...CLI_MODEL_COMMANDS.map((c) => `/${c.name}`),
      "/cli-back",
      "/cli-test",
      "/cli-list",
      "/grok-login",
      "/grok-status",
      "/grok-logout",
      "/gemini-login",
      "/gemini-status",
      "/gemini-logout",
      "/claude-login",
      "/claude-status",
      "/claude-logout",
      "/chatgpt-login",
      "/chatgpt-status",
      "/chatgpt-logout",
      "/bridge-status",
      "/cli-help",
    ];
    // Command registration is silent — fires on every register() call
  },
};

export default plugin;
