/**
 * grok-client.ts
 *
 * Grok.com integration via Playwright DOM automation.
 *
 * Strategy: inject messages via the ProseMirror editor, poll `.message-bubble`
 * DOM elements for the response. This bypasses Cloudflare anti-bot checks
 * on direct API calls (which require signed x-statsig-id headers generated
 * inside the page's own bundle — not accessible externally).
 *
 * Works by connecting to the running OpenClaw browser (CDP port 18800) which
 * already has an authenticated grok.com session open.
 */

import type { BrowserContext, Page } from "playwright";

// ──────────────────────────────────────────────────────────────────────────────
// Types
// ──────────────────────────────────────────────────────────────────────────────

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface GrokCompleteOptions {
  messages: ChatMessage[];
  model?: string;
  timeoutMs?: number;
}

export interface GrokCompleteResult {
  content: string;
  model: string;
  finishReason: string;
  promptTokens?: number;
  completionTokens?: number;
}

// ──────────────────────────────────────────────────────────────────────────────
// Constants
// ──────────────────────────────────────────────────────────────────────────────

const DEFAULT_TIMEOUT_MS = 120_000;
const STABLE_CHECKS = 3;       // consecutive identical reads to consider "done"
const STABLE_INTERVAL_MS = 500; // ms between stability checks

// ──────────────────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────────────────

function resolveModel(m?: string): string {
  const clean = (m ?? "grok-3").replace("web-grok/", "");
  const allowed = ["grok-4", "grok-3", "grok-3-fast", "grok-3-mini", "grok-3-mini-fast"];
  return allowed.includes(clean) ? clean : "grok-3";
}

/**
 * Flatten a multi-turn message array into a single string for the Grok UI.
 */
function flattenMessages(messages: ChatMessage[]): string {
  if (messages.length === 1) return messages[0].content;
  return messages
    .map((m) => {
      if (m.role === "system") return `[System]: ${m.content}`;
      if (m.role === "assistant") return `[Assistant]: ${m.content}`;
      return m.content;
    })
    .join("\n\n");
}

/**
 * Get an existing grok.com page from the context, or navigate to grok.com.
 */
export async function getOrCreateGrokPage(
  context: BrowserContext
): Promise<{ page: Page; owned: boolean }> {
  const existing = context.pages().filter((p) => p.url().startsWith("https://grok.com"));
  if (existing.length > 0) return { page: existing[0], owned: false };
  const page = await context.newPage();
  await page.goto("https://grok.com", { waitUntil: "domcontentloaded", timeout: 15_000 });
  return { page, owned: true };
}

// ──────────────────────────────────────────────────────────────────────────────
// Core DOM automation
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Send a message via the grok.com UI and wait for a stable response.
 * Returns the final text content of the last `.message-bubble` element.
 */
async function sendAndWait(
  page: Page,
  message: string,
  timeoutMs: number,
  log: (msg: string) => void
): Promise<string> {
  // Count current message bubbles
  const countBefore = await page.evaluate(
    () => document.querySelectorAll(".message-bubble").length
  );

  // Type the message into the ProseMirror editor
  await page.evaluate((msg: string) => {
    const ed =
      document.querySelector(".ProseMirror") ||
      document.querySelector('[contenteditable="true"]');
    if (!ed) throw new Error("Grok editor not found");
    (ed as HTMLElement).focus();
    document.execCommand("insertText", false, msg);
  }, message);

  await new Promise((r) => setTimeout(r, 300));
  await page.keyboard.press("Enter");

  log(`grok-client: message sent (${message.length} chars), waiting for response…`);

  // Poll for a stable response
  const deadline = Date.now() + timeoutMs;
  let lastText = "";
  let stableCount = 0;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

    const text = await page.evaluate(
      (before: number) => {
        const bubbles = [...document.querySelectorAll(".message-bubble")];
        if (bubbles.length <= before) return "";
        return bubbles[bubbles.length - 1].textContent?.trim() ?? "";
      },
      countBefore
    );

    if (text && text === lastText) {
      stableCount++;
      if (stableCount >= STABLE_CHECKS) {
        log(`grok-client: response stable (${text.length} chars)`);
        return text;
      }
    } else {
      stableCount = 0;
      lastText = text;
    }
  }

  throw new Error(`grok.com response timeout after ${timeoutMs}ms`);
}

// ──────────────────────────────────────────────────────────────────────────────
// Public API
// ──────────────────────────────────────────────────────────────────────────────

/**
 * Non-streaming completion.
 */
export async function grokComplete(
  context: BrowserContext,
  opts: GrokCompleteOptions,
  log: (msg: string) => void
): Promise<GrokCompleteResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`grok-client: complete model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto("https://grok.com", { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));
    const content = await sendAndWait(page, prompt, timeoutMs, log);
    return { content, model, finishReason: "stop" };
  } finally {
    await page.close().catch(() => {});
  }
}

/**
 * Streaming completion — polls the DOM and calls onToken when new text arrives.
 */
export async function grokCompleteStream(
  context: BrowserContext,
  opts: GrokCompleteOptions,
  onToken: (token: string) => void,
  log: (msg: string) => void
): Promise<GrokCompleteResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`grok-client: stream model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto("https://grok.com", { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));

    const countBefore = await page.evaluate(
      () => document.querySelectorAll(".message-bubble").length
    );

    // Send message
    await page.evaluate((msg: string) => {
      const ed =
        document.querySelector(".ProseMirror") ||
        document.querySelector('[contenteditable="true"]');
      if (!ed) throw new Error("Grok editor not found");
      (ed as HTMLElement).focus();
      document.execCommand("insertText", false, msg);
    }, prompt);
    await new Promise((r) => setTimeout(r, 300));
    await page.keyboard.press("Enter");

    log(`grok-client: message sent, streaming…`);

    // Stream: poll DOM, emit new chars as tokens
    const deadline = Date.now() + timeoutMs;
    let emittedLength = 0;
    let lastText = "";
    let stableCount = 0;

    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

      const text = await page.evaluate(
        (before: number) => {
          const bubbles = [...document.querySelectorAll(".message-bubble")];
          if (bubbles.length <= before) return "";
          return bubbles[bubbles.length - 1].textContent?.trim() ?? "";
        },
        countBefore
      );

      if (text && text.length > emittedLength) {
        const newChars = text.slice(emittedLength);
        onToken(newChars);
        emittedLength = text.length;
      }

      if (text && text === lastText) {
        stableCount++;
        if (stableCount >= STABLE_CHECKS) {
          log(`grok-client: stream done (${text.length} chars)`);
          return { content: text, model, finishReason: "stop" };
        }
      } else {
        stableCount = 0;
        lastText = text;
      }
    }

    throw new Error(`grok.com stream timeout after ${timeoutMs}ms`);
  } finally {
    await page.close().catch(() => {});
  }
}
