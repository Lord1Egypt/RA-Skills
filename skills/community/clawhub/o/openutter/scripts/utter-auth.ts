#!/usr/bin/env npx tsx
/**
 * utter-auth.ts — Sign the OpenUtter bot into Google via Playwright
 *
 * Usage:
 *   npx tsx skills/openutter/scripts/utter-auth.ts
 *
 * Opens a headed Chromium browser at accounts.google.com. Sign in manually,
 * then press Enter in the terminal. The browser session (cookies + localStorage)
 * is saved to ~/.openutter/auth.json via Playwright's storageState.
 *
 * On subsequent runs, utter-join.ts loads auth.json so the bot joins as an
 * authenticated Google user — no guest admission needed.
 *
 * No client_secret.json or OAuth setup required.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createInterface } from "node:readline";
import { homedir } from "node:os";
import { join } from "node:path";

const OPENUTTER_DIR = join(homedir(), ".openutter");
const AUTH_FILE = join(OPENUTTER_DIR, "auth.json");
const AUTH_META_FILE = join(OPENUTTER_DIR, "auth-meta.json");

async function waitForEnter(prompt: string): Promise<void> {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => {
    rl.question(prompt, () => {
      rl.close();
      resolve();
    });
  });
}

async function main() {
  mkdirSync(OPENUTTER_DIR, { recursive: true });

  let pw: typeof import("playwright-core");
  try {
    pw = await import("playwright-core");
  } catch {
    console.error("playwright-core not found. Install it: pnpm add -D playwright-core");
    process.exit(1);
  }

  console.log("OpenUtter — Google Account Login\n");

  if (existsSync(AUTH_FILE)) {
    console.log(`Existing auth found at ${AUTH_FILE}`);
    console.log("This will overwrite it with a new session.\n");
  }

  console.log("A browser window will open. Sign into your Google account,");
  console.log("then come back here and press Enter to save the session.\n");

  // Launch a headed browser — user signs in manually
  const browser = await pw.chromium.launch({
    headless: false,
    args: [
      "--disable-blink-features=AutomationControlled",
      "--no-first-run",
      "--no-default-browser-check",
      "--window-size=1280,720",
    ],
    ignoreDefaultArgs: ["--enable-automation"],
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
  });

  const page = await context.newPage();

  // Navigate to Google sign-in
  await page.goto("https://accounts.google.com", { waitUntil: "domcontentloaded" });

  console.log("Browser opened — sign into Google now.\n");

  // Wait for user to finish signing in
  await waitForEnter("Press Enter after you've signed in to Google... ");

  // Try to extract the signed-in email
  let email = "unknown";
  try {
    // Navigate to myaccount page which shows the email
    await page.goto("https://myaccount.google.com", { waitUntil: "domcontentloaded", timeout: 10_000 });
    await page.waitForTimeout(2000);

    email = await page.evaluate(() => {
      // Try data-email attribute (common on Google pages)
      const emailEl = document.querySelector("[data-email]");
      if (emailEl) return emailEl.getAttribute("data-email") || "";

      // Try aria-label on profile button (e.g. "Google Account: name (email@gmail.com)")
      const profileBtn = document.querySelector('[aria-label*="@"]');
      if (profileBtn) {
        const match = profileBtn.getAttribute("aria-label")?.match(/[\w.+-]+@[\w-]+\.[\w.]+/);
        if (match) return match[0];
      }

      // Scan page text for email pattern
      const bodyText = document.body.innerText || "";
      const match = bodyText.match(/[\w.+-]+@(gmail|googlemail|google)\.[\w.]+/);
      return match ? match[0] : "";
    });
  } catch {
    // Not critical — email detection is best-effort
  }

  if (email && email !== "unknown") {
    console.log(`\nSigned in as: ${email}`);
  } else {
    console.log("\nCould not detect email — session will still be saved.");
  }

  // Save the storage state (cookies + localStorage)
  await context.storageState({ path: AUTH_FILE });
  console.log(`Session saved to ${AUTH_FILE}`);

  // Save metadata (email + timestamp)
  const meta = { email: email || "unknown", savedAt: new Date().toISOString() };
  writeFileSync(AUTH_META_FILE, JSON.stringify(meta, null, 2));

  // Show what was saved
  try {
    const state = JSON.parse(readFileSync(AUTH_FILE, "utf-8"));
    const cookieCount = state.cookies?.length ?? 0;
    const originCount = state.origins?.length ?? 0;
    console.log(`  ${cookieCount} cookies, ${originCount} origins saved`);
  } catch {
    // Not critical
  }

  await browser.close();

  console.log("\nDone! The bot will now join meetings as an authenticated user.");
  console.log("Run: npx tsx skills/openutter/scripts/utter-join.ts <meet-url>");
  console.log("\nTo join as a guest instead, use: --no-auth");
  console.log("If the session expires, re-run this script to sign in again.");
}

const isMain = process.argv[1]?.endsWith("utter-auth.ts");
if (isMain) {
  main().catch((err) => {
    console.error("Fatal:", err instanceof Error ? err.message : String(err));
    process.exit(1);
  });
}
