import { Buffer } from "node:buffer";
import { mkdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

export const MODEL = "seedance-2-0";
export const SKILL_ID = "hiapi-seedance-2-0-video";
export const SKILL_VERSION = "0.1.4";
export const DEFAULT_BASE_URL = "https://api.hiapi.ai";
export const DEFAULT_SKILLS_MANIFEST_URL = "https://raw.githubusercontent.com/HiAPIAI/hiapi-skills/main/skills.json";
export const DEFAULT_SECONDS = "5";
export const DEFAULT_RESOLUTION = "720p";
export const DEFAULT_RATIO = "16:9";
export const DEFAULT_OUTPUT_DIR = "outputs";
export const POLL_INTERVAL_MS = 5000;
export const POLL_TIMEOUT_MS = 180000;
export const HIAPI_API_KEYS_URL = "https://www.hiapi.ai/en/register";
export const HIAPI_DASHBOARD_URL = "https://www.hiapi.ai/en/dashboard";
export const HIAPI_PRICING_URL = "https://www.hiapi.ai/en/pricing";

export const MIN_SECONDS = 4;
export const MAX_SECONDS = 15;
export const SUPPORTED_RESOLUTIONS = new Set(["480p", "720p", "1080p"]);
export const SUPPORTED_RATIOS = new Set(["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "adaptive"]);
export const MAX_REFERENCE_IMAGES_WITH_FRAMES = 9;
export const MAX_REFERENCE_VIDEO_COUNT = 3;
export const MAX_REFERENCE_AUDIO_COUNT = 3;
export const MIN_REFERENCE_MEDIA_SECONDS = 2;
export const MAX_REFERENCE_MEDIA_SECONDS = 15;
export const MAX_REFERENCE_MEDIA_TOTAL_SECONDS = 15;
export const MIN_SEED = 0;
export const MAX_SEED = 2147483647;

export function resolveConfig(env = process.env) {
  const apiKey = env.HIAPI_API_KEY?.trim();
  if (!apiKey) {
    throw new Error(
      `HIAPI_API_KEY is required. Get one at ${HIAPI_API_KEYS_URL}, then run: export HIAPI_API_KEY="your_hiapi_api_key_here"`,
    );
  }

  return {
    apiKey,
    baseUrl: (env.HIAPI_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, ""),
  };
}

export function normalizeSeconds(value = DEFAULT_SECONDS) {
  const seconds = String(value).trim();
  const numeric = Number(seconds);
  if (!Number.isInteger(numeric) || numeric < MIN_SECONDS || numeric > MAX_SECONDS) {
    throw new Error(`Unsupported duration "${seconds}". Use an integer from ${MIN_SECONDS} to ${MAX_SECONDS}.`);
  }
  return seconds;
}

export function normalizeResolution(value = DEFAULT_RESOLUTION) {
  const resolution = String(value).trim().toLowerCase();
  if (!SUPPORTED_RESOLUTIONS.has(resolution)) {
    throw new Error(`Unsupported resolution "${resolution}". Use one of: ${Array.from(SUPPORTED_RESOLUTIONS).join(", ")}.`);
  }
  return resolution;
}

export function normalizeRatio(value = DEFAULT_RATIO) {
  const ratio = String(value).trim();
  if (!SUPPORTED_RATIOS.has(ratio)) {
    throw new Error(`Unsupported ratio "${ratio}". Use one of: ${Array.from(SUPPORTED_RATIOS).join(", ")}.`);
  }
  return ratio;
}

export function normalizeSeed(value) {
  const seed = Number(String(value).trim());
  if (!Number.isInteger(seed) || seed < MIN_SEED || seed > MAX_SEED) {
    throw new Error(`Unsupported seed "${value}". Use an integer from ${MIN_SEED} to ${MAX_SEED}.`);
  }
  return seed;
}

export function buildVideoPayload({
  prompt,
  seconds,
  resolution,
  ratio,
  inputReference,
  firstFrameUrl,
  lastFrameUrl,
  referenceImageUrls,
  referenceVideoUrls,
  referenceAudioUrls,
  referenceVideoDurations,
  referenceAudioDurations,
  returnLastFrame,
  generateAudio,
  webSearch,
  nsfwChecker,
  seed,
} = {}) {
  const cleanPrompt = String(prompt || "").trim();
  if (!cleanPrompt) {
    throw new Error("A prompt is required.");
  }

  const media = normalizeMediaOptions({
    inputReference,
    firstFrameUrl,
    lastFrameUrl,
    referenceImageUrls,
    referenceVideoUrls,
    referenceAudioUrls,
    referenceVideoDurations,
    referenceAudioDurations,
  });

  const payload = {
    model: MODEL,
    input: {
      prompt: cleanPrompt,
      duration: Number(normalizeSeconds(seconds)),
      resolution: normalizeResolution(resolution),
      aspect_ratio: normalizeRatio(ratio),
    },
  };

  // Omit generate_audio unless explicitly set so the API default (true) applies.
  if (generateAudio !== undefined) payload.input.generate_audio = normalizeBoolean(generateAudio, "generate_audio");
  if (seed !== undefined && seed !== null && seed !== "") payload.input.seed = normalizeSeed(seed);

  if (media.firstFrameUrl) payload.input.first_frame_url = media.firstFrameUrl;
  if (media.lastFrameUrl) payload.input.last_frame_url = media.lastFrameUrl;
  if (media.referenceImageUrls.length > 0) payload.input.reference_image_urls = media.referenceImageUrls;
  if (media.referenceVideoUrls.length > 0) payload.input.reference_video_urls = media.referenceVideoUrls;
  if (media.referenceAudioUrls.length > 0) payload.input.reference_audio_urls = media.referenceAudioUrls;
  if (returnLastFrame !== undefined) payload.input.return_last_frame = normalizeBoolean(returnLastFrame, "return_last_frame");
  if (webSearch !== undefined) payload.input.web_search = normalizeBoolean(webSearch, "web_search");
  if (nsfwChecker !== undefined) payload.input.nsfw_checker = normalizeBoolean(nsfwChecker, "nsfw_checker");
  return payload;
}

export function normalizeMediaOptions({
  inputReference,
  firstFrameUrl,
  lastFrameUrl,
  referenceImageUrls,
  referenceVideoUrls,
  referenceAudioUrls,
  referenceVideoDurations,
  referenceAudioDurations,
} = {}) {
  const resolvedFirstFrameUrl = firstNonEmpty(firstFrameUrl, inputReference);
  const resolvedLastFrameUrl = firstNonEmpty(lastFrameUrl);
  const imageUrls = normalizeUrlList(referenceImageUrls);
  const videoUrls = normalizeUrlList(referenceVideoUrls);
  const audioUrls = normalizeUrlList(referenceAudioUrls);
  const hasFrameMode = Boolean(resolvedFirstFrameUrl || resolvedLastFrameUrl);
  const hasMultimodalReferences = imageUrls.length > 0 || videoUrls.length > 0 || audioUrls.length > 0;

  if (resolvedLastFrameUrl && !resolvedFirstFrameUrl) {
    throw new Error("Seedance 2.0 last-frame mode requires a first frame. Provide --first-frame-url together with --last-frame-url.");
  }
  if (hasFrameMode && hasMultimodalReferences) {
    throw new Error("Seedance 2.0 media modes are mutually exclusive: first-frame / first+last-frame image-to-video cannot be mixed with reference_image_urls, reference_video_urls, or reference_audio_urls.");
  }

  const frameCount = [resolvedFirstFrameUrl, resolvedLastFrameUrl].filter(Boolean).length;
  if (frameCount + imageUrls.length > MAX_REFERENCE_IMAGES_WITH_FRAMES) {
    throw new Error(`Seedance 2.0 accepts at most ${MAX_REFERENCE_IMAGES_WITH_FRAMES} images total across first/last frames and reference_image_urls.`);
  }
  if (videoUrls.length > MAX_REFERENCE_VIDEO_COUNT) {
    throw new Error(`Seedance 2.0 accepts at most ${MAX_REFERENCE_VIDEO_COUNT} reference videos.`);
  }
  if (audioUrls.length > MAX_REFERENCE_AUDIO_COUNT) {
    throw new Error(`Seedance 2.0 accepts at most ${MAX_REFERENCE_AUDIO_COUNT} reference audio clips.`);
  }

  validateTimedReferences("reference video", videoUrls, referenceVideoDurations);
  validateTimedReferences("reference audio", audioUrls, referenceAudioDurations);

  return {
    firstFrameUrl: resolvedFirstFrameUrl,
    lastFrameUrl: resolvedLastFrameUrl,
    referenceImageUrls: imageUrls,
    referenceVideoUrls: videoUrls,
    referenceAudioUrls: audioUrls,
  };
}

export function normalizeUrlList(value) {
  if (value === undefined || value === null || value === "") return [];
  const raw = Array.isArray(value) ? value : [value];
  return raw
    .flatMap((entry) => String(entry).split(","))
    .map((entry) => entry.trim())
    .filter(Boolean);
}

export function normalizeDurationList(value) {
  if (value === undefined || value === null || value === "") return [];
  const raw = Array.isArray(value) ? value : [value];
  return raw
    .flatMap((entry) => String(entry).split(","))
    .map((entry) => entry.trim())
    .filter(Boolean)
    .map((entry) => {
      const numeric = Number(entry);
      if (!Number.isFinite(numeric)) {
        throw new Error(`Reference media duration "${entry}" must be a number of seconds.`);
      }
      return numeric;
    });
}

function validateTimedReferences(label, urls, durations) {
  if (urls.length === 0) return;
  const normalizedDurations = normalizeDurationList(durations);
  if (normalizedDurations.length !== urls.length) {
    throw new Error(`Provide one --${label.replace(" ", "-")}-duration value for each ${label} URL so the skill can validate 2-15 second clips and the 15 second total limit.`);
  }
  const total = normalizedDurations.reduce((sum, duration) => sum + duration, 0);
  for (const duration of normalizedDurations) {
    if (duration < MIN_REFERENCE_MEDIA_SECONDS || duration > MAX_REFERENCE_MEDIA_SECONDS) {
      throw new Error(`Each Seedance 2.0 ${label} must be ${MIN_REFERENCE_MEDIA_SECONDS}-${MAX_REFERENCE_MEDIA_SECONDS} seconds.`);
    }
  }
  if (total > MAX_REFERENCE_MEDIA_TOTAL_SECONDS) {
    throw new Error(`Seedance 2.0 ${label} total duration must not exceed ${MAX_REFERENCE_MEDIA_TOTAL_SECONDS} seconds.`);
  }
}

function firstNonEmpty(...values) {
  for (const value of values) {
    const normalized = String(value || "").trim();
    if (normalized) return normalized;
  }
  return "";
}

function normalizeBoolean(value, field) {
  if (typeof value === "boolean") return value;
  if (value === "true" || value === "1") return true;
  if (value === "false" || value === "0") return false;
  throw new Error(`${field} must be a boolean.`);
}

export function extractTaskId(response) {
  return response?.data?.taskId || response?.data?.id || response?.data?.task_id || response?.id || response?.task_id || "";
}

export function extractVideoUrl(response) {
  const output = response?.data?.output || response?.output;
  if (Array.isArray(output)) {
    const item = output.find((entry) => entry?.url);
    if (item?.url) return item.url;
  }
  return (
    response?.output?.url ||
    response?.metadata?.url ||
    response?.data?.output?.url ||
    response?.data?.metadata?.url ||
    response?.video_url ||
    response?.url ||
    response?.data?.video_url ||
    response?.data?.url ||
    ""
  );
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

export function buildHttpErrorMessage(status, body) {
  const summary = summarizeErrorBody(body);
  const lowerSummary = summary.toLowerCase();
  const prefix = `HTTP ${status}: ${summary}`;

  if (status === 402 || lowerSummary.includes("balance") || lowerSummary.includes("credit") || lowerSummary.includes("quota")) {
    return `${prefix}\nYour HiAPI balance or credits may be insufficient. Add credits or check billing in the HiAPI dashboard: ${HIAPI_DASHBOARD_URL}. Pricing: ${HIAPI_PRICING_URL}`;
  }

  if (status === 401 || status === 403 || lowerSummary.includes("api key")) {
    return `${prefix}\nCheck your HiAPI API key or create a new one: ${HIAPI_API_KEYS_URL}`;
  }

  if (status === 400 || lowerSummary.includes("input_reference") || lowerSummary.includes("invalid")) {
    return `${prefix}\nCheck duration, resolution, ratio, audio flag, media mode, reference counts, and reference audio/video durations. Seedance 2.0 supports integer durations from 4 to 15 seconds; resolutions 480p, 720p, 1080p; ratios 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, adaptive; mutually exclusive first-frame, first+last-frame, or multimodal reference modes.`;
  }

  if (status === 429 || lowerSummary.includes("rate limit") || lowerSummary.includes("too many")) {
    return `${prefix}\nThe request was rate limited. Wait and retry, or reduce concurrent video generations.`;
  }

  if (status >= 500 || lowerSummary.includes("failed")) {
    return `${prefix}\nVideo generation failed. Try a clearer prompt or a different image, then run the skill again.`;
  }

  return `${prefix}\nIf this keeps happening, verify your HiAPI key, account status, and model access in the HiAPI dashboard: ${HIAPI_DASHBOARD_URL}`;
}

export async function createVideoTask(payload, config = resolveConfig()) {
  return requestJson(`${config.baseUrl}/v1/tasks`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

export async function getVideoTask(taskId, config = resolveConfig()) {
  return requestJson(`${config.baseUrl}/v1/tasks/${encodeURIComponent(taskId)}`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${config.apiKey}`,
    },
  });
}

export async function waitForVideo(taskId, config = resolveConfig(), options = {}) {
  const pollIntervalMs = Number(options.pollIntervalMs ?? POLL_INTERVAL_MS);
  const timeoutMs = Number(options.timeoutMs ?? POLL_TIMEOUT_MS);
  const deadline = Date.now() + timeoutMs;

  while (Date.now() < deadline) {
    await sleep(pollIntervalMs);
    const response = await getVideoTask(taskId, config);
    const status = getTaskStatus(response);

    if (status === "success" || status === "succeeded" || status === "completed") {
      const videoUrl = extractVideoUrl(response);
      if (!videoUrl) throw new Error("Video succeeded but no URL was returned.");
      return { response, videoUrl };
    }

    if (status === "fail" || status === "failed") {
      throw new Error(`Video generation failed: ${extractTaskFailureSummary(response)}`);
    }
  }

  throw new Error("Video generation timed out after 3 minutes. The task may still be running; try again later.");
}

export async function generateVideo(options, config = resolveConfig()) {
  const payload = buildVideoPayload(options);
  const created = await createVideoTask(payload, config);
  const taskId = extractTaskId(created);
  if (!taskId) {
    throw new Error(`No video task id returned: ${JSON.stringify(created)}`);
  }

  if (options.wait === false) {
    return { model: MODEL, taskId, status: "created", outputs: [] };
  }

  const { response, videoUrl } = await waitForVideo(taskId, config, options);
  const output = { kind: "url", value: videoUrl };

  if (options.save !== false) {
    const saved = await saveVideoOutput(videoUrl, options.outputDir || DEFAULT_OUTPUT_DIR);
    if (saved) {
      output.kind = "file";
      output.value = saved.path;
      output.path = saved.path;
      output.mimeType = saved.mimeType;
      output.sourceUrl = videoUrl;
    }
  }

  return {
    model: MODEL,
    taskId,
    seconds: String(payload.input.duration),
    resolution: payload.input.resolution,
    ratio: payload.input.aspect_ratio,
    generateAudio: payload.input.generate_audio,
    outputs: [output],
    rawStatus: response,
  };
}

export async function saveVideoOutput(videoUrl, outputDir = DEFAULT_OUTPUT_DIR) {
  if (!/^https?:\/\//i.test(videoUrl)) return null;

  let response;
  try {
    response = await fetch(videoUrl);
  } catch {
    return null;
  }

  if (!response.ok) return null;

  const contentType = response.headers.get("content-type") || "video/mp4";
  const bytes = Buffer.from(await response.arrayBuffer());
  const absoluteOutputDir = resolve(outputDir);
  await mkdir(absoluteOutputDir, { recursive: true });

  const fileName = `${MODEL}-${timestamp()}.mp4`;
  const path = join(absoluteOutputDir, fileName);
  await writeFile(path, bytes);
  return { path, mimeType: contentType };
}

export async function requestJson(url, init) {
  const response = await fetch(url, init);
  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { message: text };
  }

  if (!response.ok) {
    throw new Error(buildHttpErrorMessage(response.status, body));
  }

  return body;
}

export function parseArgs(argv) {
  const options = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    const next = argv[index + 1];

    if (arg === "--prompt") {
      options.prompt = next;
      index += 1;
    } else if (arg === "--seconds") {
      options.seconds = next;
      index += 1;
    } else if (arg === "--resolution") {
      options.resolution = next;
      index += 1;
    } else if (arg === "--ratio") {
      options.ratio = next;
      index += 1;
    } else if (arg === "--input-reference" || arg === "--image-url" || arg === "--first-frame-url") {
      options.inputReference = next;
      index += 1;
    } else if (arg === "--last-frame-url") {
      options.lastFrameUrl = next;
      index += 1;
    } else if (arg === "--reference-image-url" || arg === "--reference-image-urls") {
      pushOption(options, "referenceImageUrls", next);
      index += 1;
    } else if (arg === "--reference-video-url" || arg === "--reference-video-urls") {
      pushOption(options, "referenceVideoUrls", next);
      index += 1;
    } else if (arg === "--reference-audio-url" || arg === "--reference-audio-urls") {
      pushOption(options, "referenceAudioUrls", next);
      index += 1;
    } else if (arg === "--reference-video-duration" || arg === "--reference-video-durations") {
      pushOption(options, "referenceVideoDurations", next);
      index += 1;
    } else if (arg === "--reference-audio-duration" || arg === "--reference-audio-durations") {
      pushOption(options, "referenceAudioDurations", next);
      index += 1;
    } else if (arg === "--generate-audio") {
      options.generateAudio = true;
    } else if (arg === "--no-audio" || arg === "--no-generate-audio") {
      options.generateAudio = false;
    } else if (arg === "--seed") {
      options.seed = next;
      index += 1;
    } else if (arg === "--return-last-frame") {
      options.returnLastFrame = true;
    } else if (arg === "--web-search") {
      options.webSearch = true;
    } else if (arg === "--nsfw-checker") {
      options.nsfwChecker = true;
    } else if (arg === "--output-dir") {
      options.outputDir = next;
      index += 1;
    } else if (arg === "--no-save") {
      options.save = false;
    } else if (arg === "--no-wait") {
      options.wait = false;
    } else if (arg === "--help" || arg === "-h") {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }
  return options;
}

function pushOption(options, key, value) {
  if (!options[key]) options[key] = [];
  options[key].push(value);
}

export function usage() {
  return `Usage:
  node scripts/hiapi-seedance-2-video.mjs --prompt "A cinematic ocean cliff shot" [--seconds 5] [--resolution 720p] [--ratio 16:9]

Options:
  --prompt <text>              Required video description
  --seconds <4-15>             Integer seconds. Default: 5
  --resolution <480p|720p|1080p>
                              Default: 720p
  --ratio <16:9|9:16|1:1|4:3|3:4|21:9|adaptive>
                              Default: 16:9
  --input-reference <url>      Alias for --first-frame-url
  --first-frame-url <url>      Optional first-frame image URL or asset:// id
  --last-frame-url <url>       Optional last-frame image URL or asset:// id
  --reference-image-url <url>  Repeatable. Multimodal reference image URL or asset:// id
  --reference-video-url <url>  Repeatable. Multimodal reference video URL or asset:// id
  --reference-video-duration <seconds>
                              Repeat once per reference video. Each 2-15s, total <=15s
  --reference-audio-url <url>  Repeatable. Multimodal reference audio URL or asset:// id
  --reference-audio-duration <seconds>
                              Repeat once per reference audio. Each 2-15s, total <=15s
  --generate-audio             Explicitly enable generated audio (API default: enabled)
  --no-audio                   Disable generated audio (alias: --no-generate-audio)
  --seed <0-2147483647>        Optional integer seed for reproducible generation
  --return-last-frame          Return the generated video's last frame when supported
  --web-search                 Enable web search when supported
  --nsfw-checker               Enable content checking when supported
  --output-dir <path>          Default: outputs
  --no-save                    Return the remote video URL without downloading
  --no-wait                    Create the task and return the task id

Media modes are mutually exclusive:
  1. first-frame image-to-video
  2. first+last-frame image-to-video
  3. multimodal references via reference image/video/audio URLs
`;
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
  const updateCommand = policy.updateCommand || "npx -y github:HiAPIAI/hiapi-seedance-2-0-video-skill -y";

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

function summarizeErrorBody(body) {
  if (!body) return "Unknown error";
  if (typeof body === "string") return body;
  if (typeof body === "object" && body.code && body.message && body.message !== "success") {
    return `${body.code}: ${body.message}`;
  }
  return (
    body.error?.message ||
    body.message ||
    body.error ||
    body.detail ||
    JSON.stringify(body)
  );
}

function isUsefulFailureSummary(summary) {
  const normalized = String(summary || "").trim().toLowerCase();
  return normalized !== "" && normalized !== "unknown error" && normalized !== "success" && normalized !== "ok";
}

function timestamp() {
  return new Date().toISOString().replace(/[-:]/g, "").replace(/\..+/, "").replace("T", "-");
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
