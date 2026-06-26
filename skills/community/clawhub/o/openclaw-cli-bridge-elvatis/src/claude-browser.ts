/**
 * claude-browser.ts
 *
 * Claude.ai browser automation via Playwright DOM-polling.
 * Identical strategy to grok-client.ts — no direct API calls,
 * everything runs through the authenticated browser page.
 *
 * DOM structure (as of 2026-03-11):
 *   Editor:   .ProseMirror (tiptap)
 *   Messages: [data-test-render-count] divs, alternating user/assistant
 *             Assistant messages: child div with class "group" (no "mb-1 mt-6")
 */

import type { BrowserContext, Page } from "playwright";

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface ClaudeBrowserOptions {
  messages: ChatMessage[];
  model?: string;
  timeoutMs?: number;
}

export interface ClaudeBrowserResult {
  content: string;
  model: string;
  finishReason: string;
}

const DEFAULT_TIMEOUT_MS = 120_000;
const STABLE_CHECKS = 3;
const STABLE_INTERVAL_MS = 500;
const CLAUDE_HOME = "https://claude.ai/new";

const MODEL_MAP: Record<string, string> = {
  "claude-sonnet":       "claude-sonnet",
  "claude-opus":         "claude-opus",
  "claude-haiku":        "claude-haiku",
  "claude-sonnet-4-5":   "claude-sonnet-4-5",
  "claude-sonnet-4-6":   "claude-sonnet-4-6",
  "claude-opus-4-5":     "claude-opus-4-5",
  "claude-opus-4-6":     "claude-opus-4-6",
  "claude-haiku-4-5":    "claude-haiku-4-5",
};

function resolveModel(m?: string): string {
  const clean = (m ?? "claude-sonnet").replace("web-claude/", "");
  return MODEL_MAP[clean] ?? "claude-sonnet";
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
 * Get or create a claude.ai/new page in the given context.
 */
export async function getOrCreateClaudePage(
  context: BrowserContext
): Promise<{ page: Page; owned: boolean }> {
  const existing = context.pages().filter((p) => p.url().startsWith("https://claude.ai"));
  if (existing.length > 0) return { page: existing[0], owned: false };
  const page = await context.newPage();
  await page.goto(CLAUDE_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 2_000));
  return { page, owned: true };
}

/**
 * Count assistant message containers currently on the page.
 * Assistant messages: [data-test-render-count] where child div lacks "mb-1 mt-6".
 */
async function countAssistantMessages(page: Page): Promise<number> {
  return page.evaluate(() => {
    const all = [...document.querySelectorAll("[data-test-render-count]")];
    return all.filter((el) => {
      const child = el.querySelector("div");
      return child && !child.className.includes("mb-1");
    }).length;
  });
}

/**
 * Get the text of the last assistant message.
 */
async function getLastAssistantText(page: Page): Promise<string> {
  return page.evaluate(() => {
    const all = [...document.querySelectorAll("[data-test-render-count]")];
    const assistants = all.filter((el) => {
      const child = el.querySelector("div");
      return child && !child.className.includes("mb-1");
    });
    return assistants[assistants.length - 1]?.textContent?.trim() ?? "";
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
  const countBefore = await countAssistantMessages(page);

  // Type into ProseMirror editor
  await page.evaluate((msg: string) => {
    const ed = document.querySelector(".ProseMirror") as HTMLElement | null;
    if (!ed) throw new Error("Claude editor not found");
    ed.focus();
    document.execCommand("insertText", false, msg);
  }, message);

  await new Promise((r) => setTimeout(r, 300));
  await page.keyboard.press("Enter");

  log(`claude-browser: message sent (${message.length} chars), waiting…`);

  const deadline = Date.now() + timeoutMs;
  let lastText = "";
  let stableCount = 0;

  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, STABLE_INTERVAL_MS));

    const currentCount = await countAssistantMessages(page);
    if (currentCount <= countBefore) continue; // response not started yet

    const text = await getLastAssistantText(page);

    if (text && text === lastText) {
      stableCount++;
      if (stableCount >= STABLE_CHECKS) {
        log(`claude-browser: response stable (${text.length} chars)`);
        return text;
      }
    } else {
      stableCount = 0;
      lastText = text;
    }
  }

  throw new Error(`claude.ai response timeout after ${timeoutMs}ms`);
}

// ─────────────────────────────────────────────────────────────────────────────

export async function claudeComplete(
  context: BrowserContext,
  opts: ClaudeBrowserOptions,
  log: (msg: string) => void
): Promise<ClaudeBrowserResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`claude-browser: complete model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(CLAUDE_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));
    const content = await sendAndWait(page, prompt, timeoutMs, log);
    return { content, model, finishReason: "stop" };
  } finally {
    await page.close().catch(() => {});
  }
}

export async function claudeCompleteStream(
  context: BrowserContext,
  opts: ClaudeBrowserOptions,
  onToken: (token: string) => void,
  log: (msg: string) => void
): Promise<ClaudeBrowserResult> {
  const model = resolveModel(opts.model);
  const prompt = flattenMessages(opts.messages);
  const timeoutMs = opts.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  log(`claude-browser: stream model=${model}`);

  const page = await context.newPage();
  try {
    await page.goto(CLAUDE_HOME, { waitUntil: "domcontentloaded", timeout: 15_000 });
    await new Promise((r) => setTimeout(r, 2_000));

    const countBefore = await countAssistantMessages(page);

    await page.evaluate((msg: string) => {
      const ed = document.querySelector(".ProseMirror") as HTMLElement | null;
      if (!ed) throw new Error("Claude editor not found");
      ed.focus();
      document.execCommand("insertText", false, msg);
    }, prompt);
    await new Promise((r) => setTimeout(r, 300));
    await page.keyboard.press("Enter");

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

      if (text && text === lastText) {
        stableCount++;
        if (stableCount >= STABLE_CHECKS) {
          log(`claude-browser: stream done (${text.length} chars)`);
          return { content: text, model, finishReason: "stop" };
        }
      } else {
        stableCount = 0;
        lastText = text;
      }
    }

    throw new Error(`claude.ai stream timeout after ${timeoutMs}ms`);
  } finally {
    await page.close().catch(() => {});
  }
}
