/**
 * gemini-browser.ts
 *
 * Gemini web automation via Playwright DOM-polling.
 * Strategy identical to grok-client.ts / claude-browser.ts.
 *
 * DOM structure (confirmed 2026-03-11):
 *   Editor:   .ql-editor (Quill — use page.type(), NOT execCommand)
 *   Response: message-content (custom element, innerText = clean response)
 *   Also:     .markdown (same content, markdown-rendered)
 */

import type { BrowserContext, Page } from "playwright";

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface GeminiBrowserOptions {
  messages: ChatMessage[];
  model?: string;
  timeoutMs?: number;
}

export interface GeminiBrowserResult {
  content: string;
  model: string;
  finishReason: string;
}

const DEFAULT_TIMEOUT_MS = 120_000;
const STABLE_CHECKS = 3;
const STABLE_INTERVAL_MS = 600; // slightly longer — Gemini streams slower
const GEMINI_HOME = "https://gemini.google.com/app";

const MODEL_MAP: Record<string, string> = {
  "gemini-2-5-pro":        "gemini-2.5-pro",
  "gemini-2-5-flash":      "gemini-2.5-flash",
  "gemini-flash":          "gemini-flash",
  "gemini-pro":            "gemini-pro",
  "gemini-3-pro":          "gemini-3-pro",
  "gemini-3-flash":        "gemini-3-flash",
};

function resolveModel(m?: string): string {
  const clean = (m ?? "gemini-2-5-pro").replace("web-gemini/", "").replace(/\./g, "-");
  return MODEL_MAP[clean] ?? "gemini-2.5-pro";
}

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
 * Get or create a Gemini page in the given context.
 */
export async function getOrCreateGeminiPage(
  context: BrowserContext
): Promise<{ page: Page; owned: boolean }> {
  const existing = context.pages().filter((p) => p.url().startsWith("https://gemini.google.com"));
  if (existing.length > 0) return { page: existing[0], owned: false };
  const page = await context.newPage();
  await page.goto(GEMINI_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 2_000));
  return { page, owned: true };
}

/**
 * Count model-response elements on the page (= number of assistant turns).
 */
async function countResponses(page: Page): Promise<number> {
  return page.evaluate(() => document.querySelectorAll("model-response").length);
}

/**
 * Get the text of the last model-response via message-content element.
 * Uses message-content (cleanest, no "Gemini hat gesagt" prefix).
 */
async function getLastResponseText(page: Page): Promise<string> {
  return page.evaluate(() => {
    const els = [...document.querySelectorAll("message-content")];
    if (!els.length) return "";
    return els[els.length - 1].textContent?.trim() ?? "";
  });
}

/**
 * Check if Gemini is still generating (streaming indicator present).
 */
async function isStreaming(page: Page): Promise<boolean> {
  return page.evaluate(() => {
    // Gemini shows a stop button while streaming
    const stopBtn = document.querySelector('button[aria-label*="stop"], button[aria-label*="Stop"], button[aria-label*="stopp"]');
    return !!stopBtn;
  });
}

/**
 * Send a message and wait for a stable response via DOM-polling.
 */
async function sendAndWait(
  page: Page,
  message: string,
  timeoutMs: number,
  log: (msg: string) => void
): Promise<string> {
  const countBefore = await countResponses(page);

  // Quill editor: use page.type() (not execCommand — Quill ignores it)
  const editor = page.locator(".ql-editor");
  await editor.click();
  await editor.type(message, { delay: 10 });
  await new Promise((r) => setTimeout(r, 300));
  await page.keyboard.press("Enter");

  log(`gemini-browser: message sent (${message.length} chars), waiting…`);

  const deadline = Date.now() + timeoutMs;
  let lastText = "";
  let stableCount = 0;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

    // Wait for new response to appear
    const currentCount = await countResponses(page);
    if (currentCount <= countBefore) continue;

    // Still streaming? Don't start stable-check yet
    const streaming = await isStreaming(page);
    if (streaming) {
      stableCount = 0;
      lastText = await getLastResponseText(page);
      continue;
    }

    const text = await getLastResponseText(page);
    if (!text) continue;

    if (text === lastText) {
      stableCount++;
      if (stableCount >= STABLE_CHECKS) {
        log(`gemini-browser: response stable (${text.length} chars)`);
        return text;
      }
    } else {
      stableCount = 0;
      lastText = text;
    }
  }

  throw new Error(`gemini.google.com response timeout after ${timeoutMs}ms`);
}

// ─────────────────────────────────────────────────────────────────────────────

export async function geminiComplete(
  context: BrowserContext,
  opts: GeminiBrowserOptions,
  log: (msg: string) => void
): Promise<GeminiBrowserResult> {
  // TODO: Gemini model switching requires UI interaction (model picker dropdown), not yet implemented
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`gemini-browser: complete model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(GEMINI_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));
    const content = await sendAndWait(page, prompt, timeoutMs, log);
    return { content, model, finishReason: "stop" };
  } finally {
    await page.close().catch(() => {});
  }
}

export async function geminiCompleteStream(
  context: BrowserContext,
  opts: GeminiBrowserOptions,
  onToken: (token: string) => void,
  log: (msg: string) => void
): Promise<GeminiBrowserResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`gemini-browser: stream model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(GEMINI_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));

    const countBefore = await countResponses(page);

    const editor = page.locator(".ql-editor");
    await editor.click();
    await editor.type(prompt, { delay: 10 });
    await new Promise((r) => setTimeout(r, 300));
    await page.keyboard.press("Enter");

    const deadline = Date.now() + timeoutMs;
    let emittedLength = 0;
    let lastText = "";
    let stableCount = 0;

    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

      const currentCount = await countResponses(page);
      if (currentCount <= countBefore) continue;

      const text = await getLastResponseText(page);

      if (text.length > emittedLength) {
        onToken(text.slice(emittedLength));
        emittedLength = text.length;
      }

      const streaming = await isStreaming(page);
      if (streaming) { stableCount = 0; continue; }

      if (text && text === lastText) {
        stableCount++;
        if (stableCount >= STABLE_CHECKS) {
          log(`gemini-browser: stream done (${text.length} chars)`);
          return { content: text, model, finishReason: "stop" };
        }
      } else {
        stableCount = 0;
        lastText = text;
      }
    }

    throw new Error(`gemini.google.com stream timeout after ${timeoutMs}ms`);
  } finally {
    await page.close().catch(() => {});
  }
}
