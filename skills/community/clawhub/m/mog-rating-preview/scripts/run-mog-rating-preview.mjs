#!/usr/bin/env node

import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SOURCE = "mogscore-web";
const WORKFLOW = "mog-rating-preview-v0";
const DEFAULT_BASE_URL = "https://mogscore.ai";
const DEFAULT_TIMEOUT_MS = 90_000;
const UPLOAD_LABEL = "Selfie image";
const SUBMIT_BUTTON_LABELS = ["Get Score", "Get my score"];

export class UsageError extends Error {}

export class WorkflowError extends Error {
  constructor(code, message, retryable = true) {
    super(message);
    this.code = code;
    this.retryable = retryable;
  }
}

export function parseArgs(argv = process.argv.slice(2), env = process.env) {
  const options = {
    baseUrl: env.MOGSCORE_BASE_URL?.trim() || DEFAULT_BASE_URL,
    browserExecutable: env.MOGSCORE_BROWSER_EXECUTABLE?.trim() || "",
    headed: true,
    image: "",
    timeoutMs: DEFAULT_TIMEOUT_MS
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];

    if (arg === "--headed") {
      options.headed = true;
      continue;
    }

    if (arg === "--image" || arg === "--base-url" || arg === "--browser-executable" || arg === "--timeout-ms") {
      const value = argv[index + 1];
      if (!value || value.startsWith("--")) {
        throw new UsageError(`${arg} requires a value.`);
      }

      index += 1;

      if (arg === "--image") {
        options.image = value;
      } else if (arg === "--base-url") {
        options.baseUrl = value;
      } else if (arg === "--browser-executable") {
        options.browserExecutable = value;
      } else {
        const timeoutMs = Number(value);
        if (!Number.isFinite(timeoutMs) || timeoutMs <= 0) {
          throw new UsageError("--timeout-ms must be a positive number.");
        }
        options.timeoutMs = Math.round(timeoutMs);
      }
      continue;
    }

    throw new UsageError(`Unknown argument: ${arg}`);
  }

  if (!options.image) {
    throw new UsageError("--image is required.");
  }

  return options;
}

export function buildTargetUrl(baseUrl) {
  const origin = new URL(baseUrl).origin;
  const target = new URL("/mog-rating", origin);
  target.searchParams.set("mode", "upload");
  return target.toString();
}

export function buildSuccessPayload({ baseUrl, previewPath, report, targetUrl }) {
  return {
    ok: true,
    source: SOURCE,
    workflow: WORKFLOW,
    url: targetUrl,
    previewPath,
    previewUrl: previewPath ? new URL(previewPath, baseUrl).toString() : null,
    report
  };
}

export function buildErrorPayload(code, message, retryable = true) {
  return {
    ok: false,
    source: SOURCE,
    workflow: WORKFLOW,
    error: {
      code,
      message,
      retryable
    }
  };
}

export function isReportsResponse(response) {
  try {
    const method = response.request().method();
    const responseUrl = new URL(response.url());
    return method === "POST" && responseUrl.pathname === "/api/reports";
  } catch {
    return false;
  }
}

export async function resolveBrowserExecutable(options) {
  if (options.browserExecutable) {
    return options.browserExecutable;
  }

  for (const candidate of browserExecutableCandidates()) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {
      // Try the next common system browser path.
    }
  }

  return "";
}

export function browserExecutableCandidates(platform = process.platform) {
  if (platform === "darwin") {
    return [
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      path.join(os.homedir(), "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
      "/Applications/Chromium.app/Contents/MacOS/Chromium"
    ];
  }

  if (platform === "win32") {
    return [
      "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
      "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    ];
  }

  return [
    "/usr/bin/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser"
  ];
}

export function buildBrowserLaunchOptions(options, executablePath = options.browserExecutable) {
  return {
    ...(executablePath ? { executablePath } : {}),
    headless: false
  };
}

export async function clickPreviewSubmitButton(page, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  let lastError;

  while (Date.now() <= deadline) {
    for (const label of SUBMIT_BUTTON_LABELS) {
      const button = page.getByRole("button", { exact: true, name: label });

      try {
        if ((await button.count()) === 1 && (await button.isEnabled())) {
          await button.click({ timeout: Math.max(1, Math.min(5_000, deadline - Date.now())) });
          return label;
        }
      } catch (error) {
        lastError = error;
      }
    }

    const remainingMs = deadline - Date.now();
    if (remainingMs <= 0) {
      break;
    }

    await page.waitForTimeout(Math.min(250, remainingMs));
  }

  const labels = SUBMIT_BUTTON_LABELS.map((label) => `"${label}"`).join(" or ");
  const suffix = lastError instanceof Error ? ` Last error: ${lastError.message}` : "";
  throw new WorkflowError(
    "submit_button_not_found",
    `Could not find the staged preview submit button (${labels}).${suffix}`,
    true
  );
}

export async function runMogRatingPreview(options) {
  const imagePath = path.resolve(options.image);
  const targetUrl = buildTargetUrl(options.baseUrl);

  try {
    await fs.access(imagePath);
  } catch {
    return buildErrorPayload("upload_failed", `Image file is not readable: ${imagePath}`, false);
  }

  let browser;
  try {
    const executablePath = await resolveBrowserExecutable(options);
    const { chromium } = await import("playwright-core");
    browser = await chromium.launch(buildBrowserLaunchOptions(options, executablePath));
    const page = await browser.newPage();

    await page.goto(targetUrl, {
      timeout: options.timeoutMs,
      waitUntil: "domcontentloaded"
    });

    const input = page.getByLabel(UPLOAD_LABEL);
    try {
      await input.waitFor({ state: "attached", timeout: options.timeoutMs });
    } catch {
      throw new WorkflowError(
        "upload_input_not_found",
        `Could not find upload input labeled "${UPLOAD_LABEL}".`,
        true
      );
    }

    try {
      await input.setInputFiles(imagePath, { timeout: options.timeoutMs });
    } catch (error) {
      throw new WorkflowError(
        "upload_failed",
        error instanceof Error ? error.message : "Could not attach the image file.",
        true
      );
    }

    const responsePromise = page.waitForResponse(isReportsResponse, {
      timeout: options.timeoutMs
    });

    try {
      await clickPreviewSubmitButton(page, options.timeoutMs);
    } catch (error) {
      responsePromise.catch(() => {});
      throw error;
    }

    let response;
    try {
      response = await responsePromise;
    } catch {
      const visibleFailure = await classifyVisibleFailure(page);
      if (visibleFailure) {
        throw visibleFailure;
      }
      throw new WorkflowError("timeout", "Timed out waiting for POST /api/reports.", true);
    }

    const responseJson = await readResponseJson(response);

    if (!response.ok()) {
      const message = publicErrorMessage(responseJson) || `POST /api/reports returned ${response.status()}.`;
      throw new WorkflowError("preview_create_failed", message, true);
    }

    if (!responseJson || typeof responseJson !== "object" || !responseJson.report) {
      throw new WorkflowError("preview_response_missing", "POST /api/reports did not return a report.", true);
    }

    return buildSuccessPayload({
      baseUrl: options.baseUrl,
      previewPath: typeof responseJson.previewPath === "string" ? responseJson.previewPath : null,
      report: responseJson.report,
      targetUrl
    });
  } catch (error) {
    if (error instanceof WorkflowError) {
      return buildErrorPayload(error.code, error.message, error.retryable);
    }

    return buildErrorPayload(
      "local_scan_failed",
      error instanceof Error ? error.message : "Could not complete the MogScore web flow.",
      true
    );
  } finally {
    if (browser) {
      await browser.close().catch(() => {});
    }
  }
}

async function classifyVisibleFailure(page) {
  try {
    const bodyText = await page.locator("body").innerText({ timeout: 1_000 });

    if (bodyText.includes("Local face scan was unavailable")) {
      return new WorkflowError(
        "scanner_unavailable",
        "Local face scan was unavailable. Refresh and try again, or use another browser.",
        true
      );
    }

    if (bodyText.includes("Could not generate a preview")) {
      return new WorkflowError("local_scan_failed", "Could not generate a preview.", true);
    }
  } catch {
    return null;
  }

  return null;
}

async function readResponseJson(response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function publicErrorMessage(responseJson) {
  if (!responseJson || typeof responseJson !== "object") {
    return "";
  }

  return typeof responseJson.error === "string" ? responseJson.error : "";
}

export async function runCli() {
  let payload;

  try {
    payload = await runMogRatingPreview(parseArgs());
  } catch (error) {
    payload = buildErrorPayload(
      "upload_failed",
      error instanceof Error ? error.message : "Could not start Mog Rating preview.",
      false
    );
  }

  process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  process.exitCode = payload.ok ? 0 : 1;
}

const currentFilePath = fileURLToPath(import.meta.url);
const invokedFilePath = process.argv[1] ? path.resolve(process.argv[1]) : "";

if (invokedFilePath === currentFilePath) {
  await runCli();
}
