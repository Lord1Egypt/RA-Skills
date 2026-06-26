/**
 * grok-session.ts
 *
 * Manages a persistent grok.com browser session using Playwright.
 *
 * Auth flow:
 *  1. First run: open Chromium, navigate to grok.com → user logs in manually via X.com OAuth
 *  2. On success: save cookies + localStorage to SESSION_PATH
 *  3. Subsequent runs: restore session from file, verify still valid
 *  4. If session expired: repeat step 1
 *
 * The saved session file is stored at ~/.openclaw/grok-session.json
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, unlinkSync } from "node:fs";
import { homedir } from "node:os";
import { join, dirname } from "node:path";
import type { Browser, BrowserContext, Cookie } from "playwright";

export const DEFAULT_SESSION_PATH = join(
  homedir(),
  ".openclaw",
  "grok-session.json"
);

export const GROK_HOME = "https://grok.com";
export const GROK_API_BASE = "https://grok.com/api";

/** Stored session data */
export interface GrokSession {
  cookies: Cookie[];
  savedAt: number; // epoch ms
  userAgent?: string;
}

/** Result of a session check */
export interface SessionCheckResult {
  valid: boolean;
  reason?: string;
}

// ──────────────────────────────────────────────────────────────────────────────
// Persistence helpers
// ──────────────────────────────────────────────────────────────────────────────

export function loadSession(sessionPath: string): GrokSession | null {
  if (!existsSync(sessionPath)) return null;
  try {
    const raw = readFileSync(sessionPath, "utf-8");
    const parsed = JSON.parse(raw) as GrokSession;
    if (!parsed.cookies || !Array.isArray(parsed.cookies)) return null;
    return parsed;
  } catch {
    return null;
  }
}

export function saveSession(
  sessionPath: string,
  session: GrokSession
): void {
  mkdirSync(dirname(sessionPath), { recursive: true });
  writeFileSync(sessionPath, JSON.stringify(session, null, 2), "utf-8");
}

export function deleteSession(sessionPath: string): void {
  if (existsSync(sessionPath)) {
    unlinkSync(sessionPath);
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Session validation
// ──────────────────────────────────────────────────────────────────────────────

const SESSION_MAX_AGE_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

export function isSessionExpiredByAge(session: GrokSession): boolean {
  return Date.now() - session.savedAt > SESSION_MAX_AGE_MS;
}

/**
 * Verify the session is still valid by making a lightweight API call.
 * Returns {valid: true} if the session works, {valid: false, reason} otherwise.
 */
export async function verifySession(
  context: BrowserContext,
  log: (msg: string) => void
): Promise<SessionCheckResult> {
  log("verifying grok session...");

  // Prefer an existing grok.com page — don't open a new one (new pages can
  // trigger Cloudflare checks and displace the authenticated session page).
  const existingPages = context.pages().filter((p) => p.url().startsWith("https://grok.com"));
  if (existingPages.length > 0) {
    const page = existingPages[0];
    // Check for sign-in link on existing page
    const signIn = page.locator('a[href*="sign-in"], a[href*="/login"]');
    const signInVisible = await signIn.isVisible().catch(() => false);
    if (signInVisible) return { valid: false, reason: "sign-in link visible — session expired" };
    // Check for editor (logged in indicator)
    const editor = page.locator('.ProseMirror, [contenteditable="true"]');
    const editorVisible = await editor.isVisible().catch(() => false);
    if (editorVisible) {
      log("session valid ✅");
      return { valid: true };
    }
  }

  // No existing page — open one to check, then leave it open for reuse
  const page = await context.newPage();
  try {
    log("verifying grok session...");
    await page.goto(GROK_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });

    const signIn = page.locator('a[href*="sign-in"], a[href*="/login"]');
    if (await signIn.isVisible().catch(() => false)) {
      await page.close();
      return { valid: false, reason: "sign-in link visible — session expired" };
    }

    const editor = page.locator('.ProseMirror, [contenteditable="true"]');
    if (await editor.isVisible().catch(() => false)) {
      // Keep page open — grokComplete will reuse it
      log("session valid ✅");
      return { valid: true };
    }

    // Ambiguous — assume valid, keep page open
    log("session check ambiguous — assuming valid");
    return { valid: true };
  } catch (err) {
    await page.close().catch(() => {});
    return { valid: false, reason: (err as Error).message };
  }
}

// ──────────────────────────────────────────────────────────────────────────────
// Interactive login (opens visible browser window)
// ──────────────────────────────────────────────────────────────────────────────

export async function runInteractiveLogin(
  browser: Browser,
  sessionPath: string,
  log: (msg: string) => void,
  timeoutMs = 5 * 60 * 1000
): Promise<GrokSession> {
  log("opening browser for grok.com login — please sign in with your X account...");

  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
  });
  const page = await context.newPage();

  await page.goto(GROK_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });

  // Wait for sign-in to complete: look for chat textarea to appear
  log(`waiting for login (timeout: ${timeoutMs / 1000}s)...`);
  await page.waitForSelector(
    'textarea, [placeholder*="mind"], [aria-label*="message"]',
    { timeout: timeoutMs }
  );

  log("login detected — saving session...");
  const cookies = await context.cookies();
  const userAgent = await page.evaluate(() => navigator.userAgent);

  const session: GrokSession = {
    cookies,
    savedAt: Date.now(),
    userAgent,
  };

  saveSession(sessionPath, session);
  log(`session saved to ${sessionPath}`);

  await context.close();
  return session;
}

// ──────────────────────────────────────────────────────────────────────────────
// Context factory: create a BrowserContext with restored cookies
// ──────────────────────────────────────────────────────────────────────────────

export async function createContextFromSession(
  browser: Browser,
  session: GrokSession
): Promise<BrowserContext> {
  const context = await browser.newContext({
    userAgent: session.userAgent,
    viewport: { width: 1280, height: 800 },
  });
  await context.addCookies(session.cookies);
  return context;
}
