/**
 * chatgpt-browser.ts
 *
 * ChatGPT web automation via Playwright DOM-polling.
 * Strategy identical to claude-browser.ts / grok-client.ts.
 *
 * DOM structure (confirmed 2026-03-11):
 *   Editor:   #prompt-textarea (ProseMirror — use execCommand)
 *   Send btn: button[data-testid="send-button"]
 *   Response: [data-message-author-role="assistant"] (last element)
 *   Streaming indicator: button[data-testid="stop-button"]
 */

import type { BrowserContext, Page } from "playwright";

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ChatGPTBrowserOptions {
  messages: ChatMessage[];
  model?: string;
  timeoutMs?: number;
}

export interface ChatGPTBrowserResult {
  content: string;
  model: string;
  finishReason: string;
}

const DEFAULT_TIMEOUT_MS = 120_000;
const STABLE_CHECKS = 3;
const STABLE_INTERVAL_MS = 500;
const CHATGPT_HOME = "https://chatgpt.com";

const MODEL_URLS: Record<string, string> = {
  "gpt-4o":       "https://chatgpt.com/?model=gpt-4o",
  "gpt-4o-mini":  "https://chatgpt.com/?model=gpt-4o-mini",
  "gpt-4.1":      "https://chatgpt.com/?model=gpt-4.1",
  "o3":           "https://chatgpt.com/?model=o3",
  "o4-mini":      "https://chatgpt.com/?model=o4-mini",
  "gpt-5":        "https://chatgpt.com/?model=gpt-5",
  "gpt-5-mini":   "https://chatgpt.com/?model=gpt-5-mini",
};

const MODEL_MAP: Record<string, string> = {
  // canonical names
  "gpt-4o":        "gpt-4o",
  "gpt-4o-mini":   "gpt-4o-mini",
  "gpt-4.1":       "gpt-4.1",
  "o3":            "o3",
  "o4-mini":       "o4-mini",
  "gpt-5":         "gpt-5",
  "gpt-5-mini":    "gpt-5-mini",
  // aliases (web-chatgpt/* prefix stripped by proxy)
  "gpt-o3":        "o3",
  "gpt-o4-mini":   "o4-mini",
  "gpt-4-1":       "gpt-4.1",
};

function resolveModel(m?: string): string {
  const clean = (m ?? "gpt-4o").replace("web-chatgpt/", "");
  return MODEL_MAP[clean] ?? clean;
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
 * Get or create a chatgpt.com page in the given context.
 */
export async function getOrCreateChatGPTPage(
  context: BrowserContext
): Promise<{ page: Page; owned: boolean }> {
  const existing = context.pages().filter((p) => p.url().startsWith("https://chatgpt.com"));
  if (existing.length > 0) return { page: existing[0], owned: false };
  const page = await context.newPage();
  await page.goto(CHATGPT_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 2_000));
  return { page, owned: true };
}

/**
 * Count assistant messages on the page.
 */
async function countAssistantMessages(page: Page): Promise<number> {
  return page.evaluate(() =>
    document.querySelectorAll('[data-message-author-role="assistant"]').length
  );
}

/**
 * Get the text of the last assistant message.
 */
async function getLastAssistantText(page: Page): Promise<string> {
  return page.evaluate(() => {
    const els = [...document.querySelectorAll('[data-message-author-role="assistant"]')];
    return els[els.length - 1]?.textContent?.trim() ?? "";
  });
}

/**
 * Check if ChatGPT is still generating (stop button visible).
 */
async function isStreaming(page: Page): Promise<boolean> {
  return page.evaluate(() =>
    !!document.querySelector('button[data-testid="stop-button"]')
  );
}

/**
 * Send a message and wait for stable response.
 */
async function sendAndWait(
  page: Page,
  message: string,
  timeoutMs: number,
  log: (msg: string) => void
): Promise<string> {
  const countBefore = await countAssistantMessages(page);

  // Type into ProseMirror via execCommand
  await page.evaluate((msg: string) => {
    const ed = document.querySelector("#prompt-textarea") as HTMLElement | null;
    if (!ed) throw new Error("ChatGPT editor (#prompt-textarea) not found");
    ed.focus();
    document.execCommand("insertText", false, msg);
  }, message);

  await new Promise((r) => setTimeout(r, 300));

  // Click send button (preferred) or Enter
  const sendBtn = page.locator('button[data-testid="send-button"]').first();
  const hasSendBtn = await sendBtn.isVisible().catch(() => false);
  if (hasSendBtn) {
    await sendBtn.click();
  } else {
    await page.keyboard.press("Enter");
  }

  log(`chatgpt-browser: message sent (${message.length} chars), waiting…`);

  const deadline = Date.now() + timeoutMs;
  let lastText = "";
  let stableCount = 0;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

    const currentCount = await countAssistantMessages(page);
    if (currentCount <= countBefore) continue;

    // Still generating?
    const streaming = await isStreaming(page);
    if (streaming) { stableCount = 0; continue; }

    const text = await getLastAssistantText(page);
    if (!text) continue;

    if (text === lastText) {
      stableCount++;
      if (stableCount >= STABLE_CHECKS) {
        log(`chatgpt-browser: response stable (${text.length} chars)`);
        return text;
      }
    } else {
      stableCount = 0;
      lastText = text;
    }
  }

  throw new Error(`chatgpt.com response timeout after ${timeoutMs}ms`);
}

// ─────────────────────────────────────────────────────────────────────────────

export async function chatgptComplete(
  context: BrowserContext,
  opts: ChatGPTBrowserOptions,
  log: (msg: string) => void
): Promise<ChatGPTBrowserResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const navUrl = MODEL_URLS[model] ?? CHATGPT_HOME;

  log(`chatgpt-browser: complete model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(navUrl, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));
    const content = await sendAndWait(page, prompt, timeoutMs, log);
    return { content, model, finishReason: "stop" };
  } finally {
    await page.close().catch(() => {});
  }
}

export async function chatgptCompleteStream(
  context: BrowserContext,
  opts: ChatGPTBrowserOptions,
  onToken: (token: string) => void,
  log: (msg: string) => void
): Promise<ChatGPTBrowserResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;
  const navUrl = MODEL_URLS[model] ?? CHATGPT_HOME;

  log(`chatgpt-browser: stream model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(navUrl, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));

    const countBefore = await countAssistantMessages(page);

    await page.evaluate((msg: string) => {
      const ed = document.querySelector("#prompt-textarea") as HTMLElement | null;
      if (!ed) throw new Error("ChatGPT editor not found");
      ed.focus();
      document.execCommand("insertText", false, msg);
    }, prompt);
    await new Promise((r) => setTimeout(r, 300));
    const sendBtn = page.locator('button[data-testid="send-button"]').first();
    if (await sendBtn.isVisible().catch(() => false)) await sendBtn.click();
    else await page.keyboard.press("Enter");

    const deadline = Date.now() + timeoutMs;
    let emittedLength = 0;
    let lastText = "";
    let stableCount = 0;

    while (Date.now() < deadline) {
      await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

      const currentCount = await countAssistantMessages(page);
      if (currentCount <= countBefore) continue;

      const text = await getLastAssistantText(page);

      if (text.length > emittedLength) {
        onToken(text.slice(emittedLength));
        emittedLength = text.length;
      }

      const streaming = await isStreaming(page);
      if (streaming) { stableCount = 0; continue; }

      if (text && text === lastText) {
        stableCount++;
        if (stableCount >= STABLE_CHECKS) {
          log(`chatgpt-browser: stream done (${text.length} chars)`);
          return { content: text, model, finishReason: "stop" };
        }
      } else {
        stableCount = 0;
        lastText = text;
      }
    }

    throw new Error(`chatgpt.com stream timeout after ${timeoutMs}ms`);
  } finally {
    await page.close().catch(() => {});
  }
}
