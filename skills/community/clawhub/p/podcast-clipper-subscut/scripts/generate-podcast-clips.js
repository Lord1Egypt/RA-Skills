#!/usr/bin/env node

const HELP_TEXT = `Generate short-form clips from a long-form spoken video.

Usage:
  npm run generate-podcast-clips -- --video-url <url> [options]

Options:
  --video-url <url>            Public long-form video URL to process
  --max-clips <number>         Number of clips to generate (1-20, default 5)
  --clip-style <style>         viral | clean | minimal | leon | hormozi (default: viral)
  --format <format>            dynamic | hook_frame (default: dynamic)
  --captions <boolean>         true | false (default: true)
  --min-clip-duration <secs>   Minimum clip length in seconds (default 20, min 10)
  --max-clip-duration <secs>   Maximum clip length in seconds (default 60, max 60)
  --api-key <token>            Overrides SUBSCUT_API_KEY
  --api-base-url <url>         Overrides SUBSCUT_API_BASE_URL
  --help                       Show this help text

Environment:
  SUBSCUT_API_KEY              Required if --api-key is not passed
  SUBSCUT_API_BASE_URL         Optional, defaults to https://subscut.com

Formats:
  dynamic     Auto-detects split-screen vs. solo framing, reframes to 9:16 (default)
  hook_frame  Preserves original frame, adds a title card at top and captions at bottom

Styles:
  viral / beast    Bold animated-word captions (default)
  leon / hormozi   Single highlighted word, clean font
  clean / minimal  Plain white subtitles, no animation`;

function parseArgs(argv) {
  if (argv.includes("--help")) {
    console.log(HELP_TEXT);
    process.exit(0);
  }

  const values = new Map();

  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (!token.startsWith("--")) {
      continue;
    }

    const key = token.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      values.set(key, "true");
      continue;
    }

    values.set(key, next);
    index += 1;
  }

  const apiBaseUrl =
    values.get("api-base-url") ||
    process.env.SUBSCUT_API_BASE_URL ||
    "https://subscut.com";
  const apiKey = values.get("api-key") || process.env.SUBSCUT_API_KEY || "";
  const videoUrl = values.get("video-url") || "";
  const maxClips = Number.parseInt(values.get("max-clips") || "5", 10);
  const clipStyle = values.get("clip-style") || "viral";
  const format = values.get("format") || "dynamic";
  const captions = parseBoolean(values.get("captions"), true);
  const minClipDuration = Number.parseInt(
    values.get("min-clip-duration") || "20",
    10,
  );
  const maxClipDuration = Number.parseInt(
    values.get("max-clip-duration") || "60",
    10,
  );

  if (!videoUrl) {
    throw new Error("Missing required argument: --video-url");
  }

  if (!apiKey) {
    throw new Error("Missing API key. Set SUBSCUT_API_KEY or pass --api-key.");
  }

  const normalizedFormat = normalizeFormat(format);
  const normalizedApiBaseUrl = normalizeApiBaseUrl(apiBaseUrl);

  const normalizedMinClip = Math.max(10, Number.isFinite(minClipDuration) ? minClipDuration : 20);
  const normalizedMaxClip = Math.max(
    normalizedMinClip,
    Math.min(60, Number.isFinite(maxClipDuration) ? maxClipDuration : 60),
  );

  return {
    apiBaseUrl: normalizedApiBaseUrl,
    apiKey,
    videoUrl,
    maxClips: Number.isFinite(maxClips)
      ? Math.max(1, Math.min(20, maxClips))
      : 5,
    clipStyle,
    format: normalizedFormat,
    captions,
    minClipDuration: normalizedMinClip,
    maxClipDuration: normalizedMaxClip,
  };
}

function parseBoolean(value, fallback) {
  if (!value) {
    return fallback;
  }

  const normalized = value.trim().toLowerCase();
  if (["1", "true", "yes", "y"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "n"].includes(normalized)) {
    return false;
  }

  return fallback;
}

function normalizeFormat(value) {
  const normalized = (value || "").trim().toLowerCase();
  return normalized === "hook_frame" ? "hook_frame" : "dynamic";
}

function normalizeApiBaseUrl(value) {
  let parsed;

  try {
    parsed = new URL(value);
  } catch {
    throw new Error(`Invalid API base URL: ${value}`);
  }

  const isLocalhost =
    parsed.hostname === "localhost" || parsed.hostname === "127.0.0.1";

  if (parsed.protocol !== "https:" && !isLocalhost) {
    throw new Error(
      "SUBSCUT_API_BASE_URL must use https unless you are targeting localhost.",
    );
  }

  return parsed.toString().replace(/\/$/, "");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const response = await fetch(`${args.apiBaseUrl}/podcast-to-clips`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${args.apiKey}`,
    },
    body: JSON.stringify({
      video_url: args.videoUrl,
      max_clips: args.maxClips,
      captions: args.captions,
      style: args.clipStyle,
      format: args.format,
      clip_duration: {
        min: args.minClipDuration,
        max: args.maxClipDuration,
      },
    }),
  });

  const rawText = await response.text();
  const parsed = safeJson(rawText);

  if (!response.ok) {
    console.error(
      JSON.stringify(
        {
          ok: false,
          status: response.status,
          error: parsed ?? rawText,
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  console.log(
    JSON.stringify(
      {
        ok: true,
        clips: parsed?.clips ?? [],
      },
      null,
      2,
    ),
  );
}

function safeJson(value) {
  try {
    return JSON.parse(value);
  } catch {
    return null;
  }
}

main().catch((error) => {
  console.error(
    JSON.stringify(
      {
        ok: false,
        error: error instanceof Error ? error.message : String(error),
      },
      null,
      2,
    ),
  );
  process.exit(1);
});
