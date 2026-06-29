import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

export const MODEL = "gpt-image-2";
export const SKILL_ID = "hiapi-gpt-image-2";
export const SKILL_VERSION = "0.1.4";
export const DEFAULT_BASE_URL = "https://api.hiapi.ai";
export const DEFAULT_SKILLS_MANIFEST_URL = "https://raw.githubusercontent.com/HiAPIAI/hiapi-skills/main/skills.json";
export const DEFAULT_ASPECT_RATIO = "auto";
export const DEFAULT_RESOLUTION = "1K";
export const DEFAULT_OUTPUT_DIR = "outputs";
export const POLL_INTERVAL_MS = 3000;
export const POLL_TIMEOUT_MS = 180000;
export const HIAPI_HOME_URL = "https://www.hiapi.ai";
export const HIAPI_API_KEYS_URL = "https://www.hiapi.ai/en/register";
export const HIAPI_DASHBOARD_URL = "https://www.hiapi.ai/en/dashboard";
export const HIAPI_PRICING_URL = "https://www.hiapi.ai/en/pricing";
export const SUPPORTED_ASPECT_RATIOS = new Set([
  "auto",
  "1:1",
  "3:2",
  "2:3",
  "4:3",
  "3:4",
  "5:4",
  "4:5",
  "16:9",
  "9:16",
  "2:1",
  "1:2",
  "3:1",
  "1:3",
  "21:9",
  "9:21",
]);
export const SUPPORTED_RESOLUTIONS = new Set(["1K", "2K", "4K"]);
export const SUPPORTED_MODELS = new Set([
  "gpt-image-2",
  "gpt-image-2-pro",
  "gpt-image-2-image-to-image",
  "gpt-image-2-image-to-image-pro",
]);
export const IMAGE_TO_IMAGE_MODELS = new Set([
  "gpt-image-2-image-to-image",
  "gpt-image-2-image-to-image-pro",
]);
const GPT_PRO_ASPECT_RATIOS = new Set(["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]);
const GPT_IMAGE_TO_IMAGE_PRO_ASPECT_RATIOS = new Set(["auto", ...GPT_PRO_ASPECT_RATIOS]);

export function normalizeModel(value = MODEL) {
  const model = String(value || MODEL).trim();
  if (!SUPPORTED_MODELS.has(model)) {
    throw new Error(`Unsupported model "${model}". Supported values: ${Array.from(SUPPORTED_MODELS).join(", ")}`);
  }
  return model;
}

export function normalizeAspectRatio(value = DEFAULT_ASPECT_RATIO, model = MODEL) {
  const normalized = String(value || DEFAULT_ASPECT_RATIO).trim();
  const normalizedModel = normalizeModel(model);
  const supported = normalizedModel === "gpt-image-2-pro"
    ? GPT_PRO_ASPECT_RATIOS
    : normalizedModel === "gpt-image-2-image-to-image-pro"
      ? GPT_IMAGE_TO_IMAGE_PRO_ASPECT_RATIOS
      : SUPPORTED_ASPECT_RATIOS;
  if (!supported.has(normalized)) {
    throw new Error(
      `Unsupported aspect ratio "${normalized}" for ${normalizedModel}. Supported values: ${Array.from(supported).join(", ")}`,
    );
  }
  return normalized;
}

export function normalizeResolution(value = DEFAULT_RESOLUTION, model = MODEL) {
  const resolution = String(value || DEFAULT_RESOLUTION).trim().toUpperCase();
  const normalizedModel = normalizeModel(model);
  const supported = normalizedModel === "gpt-image-2" || normalizedModel === "gpt-image-2-image-to-image"
    ? SUPPORTED_RESOLUTIONS
    : new Set(["1K", "2K"]);
  if (!supported.has(resolution)) {
    throw new Error(
      `Unsupported resolution "${resolution}" for ${normalizedModel}. Supported values: ${Array.from(supported).join(", ")}`,
    );
  }
  return resolution;
}

export function normalizeInputUrls(value) {
  if (value === undefined || value === null || value === "") return [];
  const raw = Array.isArray(value) ? value : [value];
  return raw
    .flatMap((entry) => String(entry).split(","))
    .map((entry) => entry.trim())
    .filter(Boolean);
}

export function buildImagePayload({
  model = MODEL,
  prompt,
  aspectRatio = DEFAULT_ASPECT_RATIO,
  resolution = DEFAULT_RESOLUTION,
  inputUrls,
} = {}) {
  const normalizedModel = normalizeModel(model);
  const normalizedPrompt = String(prompt || "").trim();
  if (!normalizedPrompt) {
    throw new Error("A non-empty prompt is required.");
  }

  const normalizedInputUrls = normalizeInputUrls(inputUrls);
  if (IMAGE_TO_IMAGE_MODELS.has(normalizedModel) && (normalizedInputUrls.length < 1 || normalizedInputUrls.length > 5)) {
    throw new Error(`${normalizedModel} requires 1-5 input image URLs via input_urls.`);
  }
  if (!IMAGE_TO_IMAGE_MODELS.has(normalizedModel) && normalizedInputUrls.length > 0) {
    throw new Error(`${normalizedModel} does not accept input_urls. Use gpt-image-2-image-to-image or gpt-image-2-image-to-image-pro.`);
  }

  const normalizedAspectRatio = normalizeAspectRatio(aspectRatio, normalizedModel);
  const normalizedResolution = normalizeResolution(resolution, normalizedModel);

  // Cross-field constraints documented for gpt-image-2 and gpt-image-2-image-to-image.
  if (normalizedModel === "gpt-image-2" || normalizedModel === "gpt-image-2-image-to-image") {
    if (normalizedAspectRatio === "auto" && normalizedResolution !== "1K") {
      throw new Error(
        `aspect_ratio "auto" only supports resolution "1K" for ${normalizedModel}. Use --resolution 1K, or pick an explicit aspect ratio for ${normalizedResolution}.`,
      );
    }
    if (normalizedAspectRatio === "1:1" && normalizedResolution === "4K") {
      throw new Error(
        `aspect_ratio "1:1" cannot be combined with resolution "4K" for ${normalizedModel}. Use 1K or 2K, or pick a non-square aspect ratio for 4K.`,
      );
    }
  }

  const input = {
    prompt: normalizedPrompt,
    ...(normalizedInputUrls.length > 0 ? { input_urls: normalizedInputUrls } : {}),
    aspect_ratio: normalizedAspectRatio,
    resolution: normalizedResolution,
  };

  return {
    model: normalizedModel,
    input,
  };
}

export const buildChatPayload = buildImagePayload;

export function resolveConfig(env = process.env) {
  const apiKey = String(env.HIAPI_API_KEY || "").trim();
  if (!apiKey) {
    throw new Error(
      `HIAPI_API_KEY is required. Get one at ${HIAPI_API_KEYS_URL}, then run: export HIAPI_API_KEY="your_hiapi_api_key_here"`,
    );
  }

  const baseUrl = String(env.HIAPI_BASE_URL || DEFAULT_BASE_URL)
    .trim()
    .replace(/\/+$/, "");

  if (!/^https?:\/\//.test(baseUrl)) {
    throw new Error("HIAPI_BASE_URL must start with http:// or https://.");
  }

  return { apiKey, baseUrl };
}

export function extractImageOutputs(response) {
  const taskOutput = response?.data?.output || response?.output;
  if (Array.isArray(taskOutput)) {
    return taskOutput.flatMap((entry) => imageOutputFromEntry(entry)).filter(Boolean);
  }

  const directTaskOutput = imageOutputFromEntry(taskOutput || response?.data);
  if (directTaskOutput) return [directTaskOutput];

  const content = response?.choices?.[0]?.message?.content;
  if (typeof content !== "string" || !content.trim()) {
    return [];
  }

  const outputs = [];
  const markdownImagePattern = /!\[[^\]]*]\(([^)\s]+)\)/g;

  for (const match of content.matchAll(markdownImagePattern)) {
    const target = match[1];
    if (target.startsWith("data:image/")) {
      const mimeMatch = target.match(/^data:([^;]+);base64,/);
      outputs.push({
        kind: "data-uri",
        mimeType: mimeMatch?.[1] || "image/png",
        value: target,
      });
    } else if (/^https?:\/\//.test(target)) {
      outputs.push({ kind: "url", value: target });
    }
  }

  return outputs;
}

export function extractTaskId(response) {
  return response?.data?.taskId || response?.data?.id || response?.data?.task_id || response?.id || response?.task_id || "";
}

export function getTaskStatus(response) {
  const status = response?.status || response?.data?.status || "";
  return String(status).toLowerCase();
}

export function extractTaskFailureSummary(response) {
  const candidates = [
    response?.data?.error,
    response?.data?.fail_reason,
    response?.data?.failReason,
    response?.data?.error_message,
    response?.data?.errorMessage,
    response?.data?.task_status_msg,
    response?.data?.taskStatusMsg,
    response?.data?.output?.error,
    response?.data?.output?.fail_reason,
    response?.data?.output?.error_message,
    response?.data?.output?.task_status_msg,
    response?.error,
    response?.fail_reason,
    response?.error_message,
    response?.task_status_msg,
    response?.message,
  ];

  for (const candidate of candidates) {
    const summary = summarizeErrorBody(candidate);
    if (isUsefulFailureSummary(summary)) return summary;
  }

  const taskId = extractTaskId(response);
  return taskId
    ? `task failed without a public failure reason. Task ID: ${taskId}`
    : "task failed without a public failure reason.";
}

export async function createImageTask(payload, { config = resolveConfig(), fetchImpl = fetch } = {}) {
  return requestJson(`${config.baseUrl}/v1/tasks`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  }, fetchImpl);
}

export async function getImageTask(taskId, { config = resolveConfig(), fetchImpl = fetch } = {}) {
  return requestJson(`${config.baseUrl}/v1/tasks/${encodeURIComponent(taskId)}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
    },
  }, fetchImpl);
}

export async function waitForImage(taskId, { config = resolveConfig(), fetchImpl = fetch, pollIntervalMs = POLL_INTERVAL_MS, timeoutMs = POLL_TIMEOUT_MS } = {}) {
  const deadline = Date.now() + Number(timeoutMs);

  while (Date.now() < deadline) {
    await sleep(Number(pollIntervalMs));
    const response = await getImageTask(taskId, { config, fetchImpl });
    const status = getTaskStatus(response);

    if (status === "success" || status === "succeeded" || status === "completed") {
      const outputs = extractImageOutputs(response);
      if (outputs.length === 0) {
        throw new Error("Image task succeeded but no image output was returned.");
      }
      return { response, outputs };
    }

    if (status === "fail" || status === "failed") {
      throw new Error(`Image generation failed: ${extractTaskFailureSummary(response)}`);
    }
  }

  throw new Error("Image generation timed out after 3 minutes. The task may still be running; try again later.");
}

export async function generateImage(options, config = resolveConfig()) {
  const payload = buildImagePayload(options);
  const created = await createImageTask(payload, { config });
  const taskId = extractTaskId(created);
  if (!taskId) {
    throw new Error(`No image task id returned: ${JSON.stringify(created)}`);
  }

  if (options.wait === false) {
    return {
      model: payload.model,
      taskId,
      status: "created",
      aspectRatio: payload.input.aspect_ratio,
      resolution: payload.input.resolution,
      outputs: [],
    };
  }

  const { response, outputs } = await waitForImage(taskId, {
    config,
    pollIntervalMs: options.pollIntervalMs,
    timeoutMs: options.timeoutMs,
  });
  const savedOutputs = options.save === false
    ? outputs.map((output) => output.kind === "url"
      ? { kind: "url", url: output.value }
      : { kind: "data-uri", value: output.value, mimeType: output.mimeType })
    : await saveImageOutputs(outputs, {
      outputDir: options.outputDir || DEFAULT_OUTPUT_DIR,
    });

  return {
    model: payload.model,
    taskId,
    aspectRatio: payload.input.aspect_ratio,
    resolution: payload.input.resolution,
    outputs: savedOutputs,
    rawStatus: response,
  };
}

export async function callHiApi({ config, payload, fetchImpl = fetch }) {
  return createImageTask(payload, { config, fetchImpl });
}

export async function requestJson(url, init, fetchImpl = fetch) {
  const response = await fetchImpl(url, init);
  const text = await response.text();
  let json;
  try {
    json = text ? JSON.parse(text) : {};
  } catch {
    json = { raw: text };
  }

  if (!response.ok) {
    throw new Error(buildHttpErrorMessage(response.status, json));
  }

  return json;
}

export async function checkSkillUpdate({
  currentVersion = SKILL_VERSION,
  skillId = SKILL_ID,
  manifestUrl = process.env.HIAPI_SKILLS_MANIFEST_URL || DEFAULT_SKILLS_MANIFEST_URL,
  fetchImpl = fetch,
  timeoutMs = 1200,
  env = process.env,
} = {}) {
  if (env.HIAPI_SKIP_UPDATE_CHECK === "1" || env.HIAPI_SKIP_UPDATE_CHECK === "true") {
    return { status: "skipped" };
  }

  let response;
  const controller = typeof AbortController === "function" ? new AbortController() : null;
  const timer = controller ? setTimeout(() => controller.abort(), timeoutMs) : null;
  try {
    response = await fetchImpl(manifestUrl, {
      headers: { Accept: "application/json" },
      signal: controller?.signal,
    });
  } catch {
    return { status: "skipped" };
  } finally {
    if (timer) clearTimeout(timer);
  }

  if (!response?.ok) return { status: "skipped" };

  let manifest;
  try {
    manifest = await response.json();
  } catch {
    return { status: "skipped" };
  }

  const skill = Array.isArray(manifest.skills)
    ? manifest.skills.find((entry) => entry?.id === skillId)
    : null;
  const policy = skill?.updatePolicy;
  if (!policy) return { status: "current" };

  const minimumVersion = policy.minimumVersion || skill.version || currentVersion;
  const latestVersion = policy.latestVersion || skill.version || minimumVersion;
  const updateCommand = policy.updateCommand || `npx -y github:HiAPIAI/hiapi-gpt-image-2-skill -y`;

  if (compareVersions(currentVersion, minimumVersion) < 0) {
    return {
      status: "required",
      message: [
        policy.requiredNotice || "This HiAPI skill version is no longer compatible with the current HiAPI API.",
        `Installed version: ${currentVersion}; required version: ${minimumVersion}.`,
        `Update now: ${updateCommand}`,
      ].join("\n"),
      latestVersion,
      minimumVersion,
      updateCommand,
    };
  }

  if (compareVersions(currentVersion, latestVersion) < 0) {
    return {
      status: "available",
      message: [
        policy.notice || "A newer HiAPI skill is available.",
        `Installed version: ${currentVersion}; latest version: ${latestVersion}.`,
        `Update: ${updateCommand}`,
      ].join("\n"),
      latestVersion,
      minimumVersion,
      updateCommand,
    };
  }

  return { status: "current", latestVersion, minimumVersion, updateCommand };
}

export async function warnOrRequireSkillUpdate(options = {}) {
  const result = await checkSkillUpdate(options);
  if (result.status === "required") {
    throw new Error(result.message);
  }
  if (result.status === "available" && result.message) {
    console.error(result.message);
  }
  return result;
}

export function compareVersions(left, right) {
  const parse = (value) => String(value || "0.0.0")
    .split(/[+-]/, 1)[0]
    .split(".")
    .map((part) => Number.parseInt(part, 10) || 0);
  const a = parse(left);
  const b = parse(right);
  for (let index = 0; index < Math.max(a.length, b.length, 3); index += 1) {
    const delta = (a[index] || 0) - (b[index] || 0);
    if (delta !== 0) return delta > 0 ? 1 : -1;
  }
  return 0;
}

export function summarizeErrorBody(body) {
  if (!body) return "Unknown error";
  if (typeof body === "string") return body.slice(0, 500);
  if (body?.code && body?.message && body.message !== "success") {
    return `${body.code}: ${body.message}`.slice(0, 500);
  }
  if (body?.error?.message) return String(body.error.message).slice(0, 500);
  if (body?.message) return String(body.message).slice(0, 500);
  if (body?.raw) return String(body.raw).slice(0, 500);
  return JSON.stringify(body).slice(0, 500);
}

function isUsefulFailureSummary(summary) {
  const normalized = String(summary || "").trim().toLowerCase();
  return normalized !== "" && normalized !== "unknown error" && normalized !== "success" && normalized !== "ok";
}

export function buildHttpErrorMessage(status, body) {
  const summary = summarizeErrorBody(body);
  const lowerSummary = summary.toLowerCase();
  const guidance = guidanceForHttpError(status, lowerSummary);
  return `HiAPI request failed with HTTP ${status}: ${summary}\n${guidance}`;
}

function guidanceForHttpError(status, lowerSummary) {
  if (status === 401 || status === 403) {
    return `Check your HiAPI API key or create a new one: ${HIAPI_API_KEYS_URL}`;
  }

  if (
    status === 402 ||
    lowerSummary.includes("insufficient") ||
    lowerSummary.includes("balance") ||
    lowerSummary.includes("credit") ||
    lowerSummary.includes("quota")
  ) {
    return `Your HiAPI balance or credits may be insufficient. Add credits or check billing in the HiAPI dashboard: ${HIAPI_DASHBOARD_URL}. Pricing: ${HIAPI_PRICING_URL}`;
  }

  if (status === 429) {
    return "The request was rate limited. Please wait and retry, or reduce concurrent image generation requests.";
  }

  if (
    lowerSummary.includes("content_policy") ||
    lowerSummary.includes("policy") ||
    lowerSummary.includes("safety")
  ) {
    return "The prompt may have triggered a safety policy. Revise the prompt and try again.";
  }

  return `If this keeps happening, verify your HiAPI key, account status, and model access in the HiAPI dashboard: ${HIAPI_DASHBOARD_URL}`;
}

function imageOutputFromEntry(entry) {
  if (!entry || typeof entry !== "object") return null;
  const value =
    entry.url ||
    entry.image_url ||
    entry.data ||
    entry.b64_json ||
    entry.base64 ||
    entry.content ||
    "";

  if (typeof value !== "string" || !value.trim()) return null;
  if (value.startsWith("data:image/")) {
    const mimeMatch = value.match(/^data:([^;]+);base64,/);
    return {
      kind: "data-uri",
      mimeType: mimeMatch?.[1] || entry.mime_type || "image/png",
      value,
    };
  }
  if (/^https?:\/\//.test(value)) {
    return { kind: "url", value };
  }
  if (/^[A-Za-z0-9+/=]+$/.test(value) && value.length > 64) {
    const mimeType = entry.mime_type || entry.mimeType || "image/png";
    return {
      kind: "data-uri",
      mimeType,
      value: `data:${mimeType};base64,${value}`,
    };
  }
  return null;
}

export async function saveImageOutputs(outputs, { outputDir, now = new Date() }) {
  await mkdir(outputDir, { recursive: true });
  const saved = [];
  let index = 1;

  for (const output of outputs) {
    if (output.kind === "url") {
      saved.push({ kind: "url", url: output.value });
      continue;
    }

    const extension = extensionForMimeType(output.mimeType);
    const fileName = `${MODEL}-${formatTimestamp(now)}-${index}${extension}`;
    const filePath = path.resolve(outputDir, fileName);
    const base64 = output.value.replace(/^data:[^;]+;base64,/, "");
    await writeFile(filePath, Buffer.from(base64, "base64"));
    saved.push({ kind: "file", path: filePath, mimeType: output.mimeType });
    index += 1;
  }

  return saved;
}

export function extensionForMimeType(mimeType) {
  if (mimeType === "image/jpeg") return ".jpg";
  if (mimeType === "image/webp") return ".webp";
  return ".png";
}

function formatTimestamp(date) {
  return date
    .toISOString()
    .replace(/[-:]/g, "")
    .replace(/\..+$/, "")
    .replace("T", "-");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
