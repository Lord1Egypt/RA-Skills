/**
 * Media transcript extractor
 * Usage: npx tsx extract-transcript.ts --media-url "<URL>" --output-dir "<dir>" --config <path> --referer "<url>"
 * Output: JSON to stdout
 */

import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { createHash, createHmac } from "node:crypto";
import { readFileSync, writeFileSync, unlinkSync, existsSync, mkdirSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { ErrorCode, HandlerError } from "./types.js";
import { loadConfig, parseConfigArg } from "./config.js";
import type { LinkMindConfig } from "./config.js";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface AsrResult {
  srt: string;      // SRT formatted subtitle content
  fullText: string; // plain text transcript (for deep summary)
}

export interface TranscriptOutput {
  srtPath: string;
  fullText: string;
}

// ---------------------------------------------------------------------------
// SRT time formatting
// ---------------------------------------------------------------------------

/**
 * Format milliseconds as SRT timestamp: HH:MM:SS,mmm
 */
export function formatSrtTime(ms: number): string {
  const h = Math.floor(ms / 3_600_000);
  const m = Math.floor((ms % 3_600_000) / 60_000);
  const s = Math.floor((ms % 60_000) / 1_000);
  const millis = ms % 1_000;
  return (
    String(h).padStart(2, "0") + ":" +
    String(m).padStart(2, "0") + ":" +
    String(s).padStart(2, "0") + "," +
    String(millis).padStart(3, "0")
  );
}

// ---------------------------------------------------------------------------
// iFlytek LFASR result parsing
// ---------------------------------------------------------------------------

// Actual iFlytek LFASR v2 word structure (ws = word segment)
interface LfasrWordSegment {
  wb: number;              // word begin (10ms units)
  we: number;              // word end (10ms units)
  cw: Array<{ w: string }>;// candidate words (cw[0] = best)
}

/**
 * Parse iFlytek LFASR orderResult JSON string → SRT + fullText
 * Actual structure: lattice[].json_1best → { st: { rt: [{ ws: LfasrWordSegment[] }] } }
 * Time unit: 10ms per unit (multiply × 10 to get ms)
 */
export function parseLfasrResult(orderResult: string): AsrResult {
  const data = JSON.parse(orderResult) as {
    lattice: Array<{ json_1best: string }>;
  };

  const entries: Array<{ start: number; end: number; text: string }> = [];

  for (const item of data.lattice ?? []) {
    const sentence = JSON.parse(item.json_1best) as {
      st: { rt: Array<{ ws: LfasrWordSegment[] }> };
    };
    const words: LfasrWordSegment[] = (sentence.st?.rt ?? []).flatMap((rt) => rt.ws ?? []);
    if (words.length === 0) continue;

    const start = words[0].wb * 10;
    const end = words[words.length - 1].we * 10;
    const text = words.map((w) => w.cw[0]?.w ?? "").join("").trim();
    if (text) entries.push({ start, end, text });
  }

  if (entries.length === 0) return { srt: "", fullText: "" };

  const srt = entries
    .map(
      (e, i) =>
        `${i + 1}\n${formatSrtTime(e.start)} --> ${formatSrtTime(e.end)}\n${e.text}`,
    )
    .join("\n\n");

  const fullText = entries.map((e) => e.text).join(" ");

  return { srt, fullText };
}

// ---------------------------------------------------------------------------
// System dependency check
// ---------------------------------------------------------------------------

const INSTALL_HINTS: Record<string, string> = {
  "yt-dlp": "brew install yt-dlp  # 或: pip install yt-dlp",
  "ffmpeg": "brew install ffmpeg",
};

/**
 * Check if a system command exists in PATH.
 * Throws an error with depCode="DEPENDENCY" if not found.
 */
export function checkDependency(cmd: string): void {
  const result = spawnSync("which", [cmd], { encoding: "utf-8" });
  if (result.status !== 0) {
    const hint = INSTALL_HINTS[cmd] ?? `请安装 ${cmd}`;
    const err = new Error(`${cmd} 未找到，请运行: ${hint}`);
    (err as any).depCode = "DEPENDENCY";
    throw err;
  }
}

// ---------------------------------------------------------------------------
// iFlytek LFASR auth
// ---------------------------------------------------------------------------

function iflytekAuth(
  appId: string,
  secretKey: string,
): { appId: string; ts: string; signa: string } {
  const ts = String(Math.floor(Date.now() / 1000));
  const md5 = createHash("md5").update(appId + ts).digest("hex");
  const signa = createHmac("sha1", secretKey).update(md5).digest("base64");
  return { appId, ts, signa };
}

// ---------------------------------------------------------------------------
// iFlytek LFASR transcription
// ---------------------------------------------------------------------------

const LFASR_UPLOAD_URL = "https://raasr.xfyun.cn/v2/api/upload";
const LFASR_QUERY_URL  = "https://raasr.xfyun.cn/v2/api/getResult";
const POLL_INTERVAL_MS = 3_000;
const POLL_TIMEOUT_MS  = 10 * 60 * 1_000; // 10 minutes

/**
 * Convert audio to 16kHz mono mp3 (required by iFlytek LFASR).
 * Returns the converted file path; caller must delete it.
 */
function convertTo16kHz(inputPath: string): string {
  const outputPath = `${inputPath}.16k.mp3`;
  const result = spawnSync(
    "ffmpeg",
    ["-i", inputPath, "-ar", "16000", "-ac", "1", "-f", "mp3", "-y", outputPath],
    { encoding: "utf-8", timeout: 5 * 60 * 1_000 },
  );
  if (result.status !== 0) {
    throw new Error(`音频转换失败: ${result.stderr}`);
  }
  return outputPath;
}

/** Get audio duration in milliseconds using ffprobe. */
function getAudioDurationMs(filePath: string): number {
  const result = spawnSync(
    "ffprobe",
    ["-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", filePath],
    { encoding: "utf-8" },
  );
  const seconds = parseFloat(result.stdout?.trim() ?? "0");
  return Math.round(seconds * 1_000);
}

export async function transcribeIflytek(
  mp3Path: string,
  appId: string,
  secretKey: string,
): Promise<AsrResult> {
  // iFlytek LFASR requires 8kHz or 16kHz audio; convert if needed.
  const converted = convertTo16kHz(mp3Path);
  try {
    return await _uploadAndPollIflytek(converted, appId, secretKey);
  } finally {
    try { if (existsSync(converted)) unlinkSync(converted); } catch { /* ignore */ }
  }
}

async function _uploadAndPollIflytek(
  mp3Path: string,
  appId: string,
  secretKey: string,
): Promise<AsrResult> {
  // 1. Upload
  // iFlytek LFASR v2 expects raw binary body; auth + file metadata in query string.
  const { ts, signa } = iflytekAuth(appId, secretKey);
  const fileBuffer = readFileSync(mp3Path);
  const durationMs = getAudioDurationMs(mp3Path);
  const uploadParams = new URLSearchParams({
    appId, ts, signa,
    fileSize: String(fileBuffer.length),
    fileName: "audio.mp3",
    duration: String(durationMs),
  });

  const uploadResp = await fetch(`${LFASR_UPLOAD_URL}?${uploadParams}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: fileBuffer,
  });
  if (!uploadResp.ok) {
    throw new Error(`讯飞上传失败: HTTP ${uploadResp.status}`);
  }
  const uploadJson = (await uploadResp.json()) as {
    code: string;
    descInfo?: string;
    content?: { orderId?: string };
  };
  if (uploadJson.code !== "000000" || !uploadJson.content?.orderId) {
    throw new Error(`讯飞上传错误: ${uploadJson.descInfo ?? uploadJson.code}`);
  }
  const orderId = uploadJson.content.orderId;

  // 2. Poll for result
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  while (Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));

    const { ts: ts2, signa: signa2 } = iflytekAuth(appId, secretKey);
    // orderId goes in query string (not body) for getResult
    const queryParams = new URLSearchParams({ appId, ts: ts2, signa: signa2, orderId });

    const queryResp = await fetch(`${LFASR_QUERY_URL}?${queryParams}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!queryResp.ok) continue;

    const queryJson = (await queryResp.json()) as {
      code: string;
      content?: {
        orderInfo?: { status?: number };
        orderResult?: string;
      };
    };
    if (queryJson.code !== "000000") continue;

    const status = queryJson.content?.orderInfo?.status;
    const orderResult = queryJson.content?.orderResult;
    // status 4 = complete; status 3 = processing (do not break early)
    if (status === 4 && orderResult) {
      return parseLfasrResult(orderResult);
    }
  }

  throw new Error("讯飞转写超时（超过 10 分钟），请稍后重试");
}

// ---------------------------------------------------------------------------
// OpenAI Whisper transcription
// ---------------------------------------------------------------------------

export async function transcribeOpenai(
  mp3Path: string,
  apiKey: string,
  baseUrl: string = "https://api.openai.com/v1",
  model: string = "whisper-1",
): Promise<AsrResult> {
  const fileBuffer = readFileSync(mp3Path);
  const form = new FormData();
  form.append("model", model);
  form.append("response_format", "srt");
  form.append(
    "file",
    new Blob([fileBuffer], { type: "audio/mp3" }),
    "audio.mp3",
  );

  const resp = await fetch(`${baseUrl}/audio/transcriptions`, {
    method: "POST",
    headers: { Authorization: `Bearer ${apiKey}` },
    body: form,
  });

  if (!resp.ok) {
    const body = await resp.text().catch(() => "");
    throw new Error(`OpenAI Whisper 失败: HTTP ${resp.status} ${body}`);
  }

  const srt = await resp.text();
  // Extract plain text from SRT: remove sequence numbers and timestamps
  const fullText = srt
    .split("\n")
    .filter(
      (line) =>
        line.trim() !== "" &&
        !/^\d+$/.test(line.trim()) &&
        !line.includes("-->"),
    )
    .join(" ")
    .trim();

  return { srt, fullText };
}

// ---------------------------------------------------------------------------
// Time argument parsing
// ---------------------------------------------------------------------------

/**
 * Parse a time argument string to seconds.
 * Accepts: "MM:SS", "HH:MM:SS", or plain seconds (e.g. "1023").
 * Returns null if value is undefined or cannot be parsed.
 */
export function parseTimeArg(value: string | undefined): number | null {
  if (value === undefined || value.trim() === "") return null;
  const parts = value.trim().split(":");
  if (parts.length === 1) {
    const n = Number(parts[0]);
    return Number.isFinite(n) && n >= 0 ? n : null;
  }
  if (parts.length === 2) {
    const [mm, ss] = parts.map(Number);
    if (!Number.isFinite(mm) || !Number.isFinite(ss)) return null;
    return mm * 60 + ss;
  }
  if (parts.length === 3) {
    const [hh, mm, ss] = parts.map(Number);
    if (!Number.isFinite(hh) || !Number.isFinite(mm) || !Number.isFinite(ss)) return null;
    return hh * 3600 + mm * 60 + ss;
  }
  return null;
}

// ---------------------------------------------------------------------------
// Media download
// ---------------------------------------------------------------------------

const MOBILE_UA =
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) " +
  "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"; // used by fetch fallback

/**
 * Download media URL and convert to mp3.
 * Strategy: yt-dlp first (handles all platforms), fetch+ffmpeg as fallback.
 * Writes mp3 to `outputMp3Path`.
 * Optional startSeconds/endSeconds limit extraction to that time window.
 */
export async function downloadMedia(
  url: string,
  referer: string,
  outputMp3Path: string,
  startSeconds?: number,
  endSeconds?: number,
): Promise<void> {
  // yt-dlp: download and convert to mp3 directly
  // The -o template uses %(ext)s so yt-dlp writes to outputMp3Path with .mp3 extension.
  // We derive the template base by stripping .mp3 extension.
  const templateBase = outputMp3Path.endsWith(".mp3")
    ? outputMp3Path.slice(0, -4)
    : outputMp3Path;

  const ytdlpArgs: string[] = [
    "-x",
    "--audio-format", "mp3",
    "--audio-quality", "5",
    "-o", `${templateBase}.%(ext)s`,
    "--no-playlist",
    "--quiet",
  ];

  if (startSeconds !== undefined || endSeconds !== undefined) {
    const start = startSeconds ?? 0;
    const end = endSeconds !== undefined ? endSeconds : undefined;
    const section = end !== undefined ? `*${start}-${end}` : `*${start}-`;
    ytdlpArgs.push("--download-sections", section);
  }

  ytdlpArgs.push(url);

  const ytdlp = spawnSync("yt-dlp", ytdlpArgs, {
    encoding: "utf-8",
    timeout: 5 * 60 * 1000,
  });

  if (ytdlp.status === 0 && existsSync(outputMp3Path)) return;

  // Fallback: fetch raw file, then extract audio with ffmpeg
  const tmpVideoPath = `${templateBase}.mp4`;

  const resp = await fetch(url, {
    headers: { "User-Agent": MOBILE_UA, Referer: referer },
  });
  if (!resp.ok) {
    throw Object.assign(
      new Error(`媒体下载失败: HTTP ${resp.status} (yt-dlp 和 fetch 均失败)`),
      { httpStatus: resp.status },
    );
  }

  const buf = await resp.arrayBuffer();
  writeFileSync(tmpVideoPath, Buffer.from(buf));

  const ffmpegArgs: string[] = ["-i", tmpVideoPath];
  if (startSeconds !== undefined) ffmpegArgs.push("-ss", String(startSeconds));
  if (endSeconds !== undefined) ffmpegArgs.push("-to", String(endSeconds));
  ffmpegArgs.push("-vn", "-ar", "16000", "-ac", "1", "-f", "mp3", "-y", outputMp3Path);

  const ffmpeg = spawnSync("ffmpeg", ffmpegArgs, {
    encoding: "utf-8",
    timeout: 5 * 60 * 1000,
  });

  try { unlinkSync(tmpVideoPath); } catch { /* ignore */ }

  if (ffmpeg.status !== 0) {
    throw new Error(`ffmpeg 音频提取失败: ${ffmpeg.stderr}`);
  }
}

// ---------------------------------------------------------------------------
// ASR routing
// ---------------------------------------------------------------------------

async function routeAsr(
  mp3Path: string,
  config: LinkMindConfig,
): Promise<AsrResult> {
  const asr = config.asr ?? {};
  const iflytek = asr.iflytek;
  const openai = asr.openai;

  const hasIflytek =
    !!iflytek?.app_id && !!iflytek?.secret_key;
  const hasOpenai = !!openai?.api_key;

  if (!hasIflytek && !hasOpenai) {
    const err = new Error(
      "ASR 服务未配置。请在 .env 中配置讯飞或 OpenAI 凭据（参考 .env.example）。",
    );
    (err as any).authCode = "AUTH";
    throw err;
  }

  if (hasIflytek) {
    try {
      return await transcribeIflytek(
        mp3Path,
        iflytek!.app_id!,
        iflytek!.secret_key!,
      );
    } catch (e) {
      if (!hasOpenai) throw e;
      console.error(
        `[linkmind] 讯飞转写失败，切换到 OpenAI: ${(e as Error).message}`,
      );
    }
  }

  return await transcribeOpenai(
    mp3Path,
    openai!.api_key!,
    openai!.base_url,
    openai!.model,
  );
}

// ---------------------------------------------------------------------------
// Error categorization
// ---------------------------------------------------------------------------

function categorizeError(e: unknown): { code: ErrorCode; details: string } {
  const msg = e instanceof Error ? e.message : String(e);
  const lower = msg.toLowerCase();

  if ((e as any).depCode === "DEPENDENCY")
    return { code: "DEPENDENCY", details: msg };
  if ((e as any).authCode === "AUTH" || lower.includes("未配置"))
    return { code: "AUTH", details: msg };
  if (
    lower.includes("timeout") ||
    lower.includes("超时") ||
    lower.includes("network") ||
    lower.includes("fetch")
  )
    return { code: "NETWORK", details: msg };
  return { code: "UNKNOWN", details: msg };
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  // Parse CLI args
  const args = process.argv.slice(2);
  function getArg(flag: string): string | undefined {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : undefined;
  }

  const mediaUrl  = getArg("--media-url");
  const outputDir = getArg("--output-dir");
  const configPath = getArg("--config") ?? parseConfigArg(process.argv);
  const referer   = getArg("--referer") ?? "https://weibo.com";
  const startSeconds = parseTimeArg(getArg("--start"));
  const endSeconds   = parseTimeArg(getArg("--end"));

  if (!mediaUrl || !outputDir || !configPath) {
    const err: HandlerError = {
      error: "缺少必要参数: --media-url, --output-dir, --config",
    };
    console.log(JSON.stringify(err));
    process.exit(1);
  }

  // Temp file paths
  const hash = createHash("md5").update(mediaUrl).digest("hex").slice(0, 8);
  const tmpMp3 = join(tmpdir(), `linkmind-${hash}.mp3`);

  try {
    // Load config
    const config = loadConfig(configPath);

    // Check dependencies
    checkDependency("yt-dlp");
    checkDependency("ffmpeg");

    // Ensure output dir exists
    if (!existsSync(outputDir)) {
      mkdirSync(outputDir, { recursive: true });
    }

    // Download media → mp3
    await downloadMedia(
      mediaUrl, referer, tmpMp3,
      startSeconds ?? undefined,
      endSeconds ?? undefined,
    );

    // Transcribe
    const asrResult = await routeAsr(tmpMp3, config);

    // Save SRT
    const srtPath = join(outputDir, "transcript.srt");
    writeFileSync(srtPath, asrResult.srt, "utf-8");

    const output: TranscriptOutput = {
      srtPath: "transcript.srt",
      fullText: asrResult.fullText,
    };
    console.log(JSON.stringify(output, null, 2));
  } catch (e) {
    const { code, details } = categorizeError(e);
    const err: HandlerError = {
      error: e instanceof Error ? e.message : String(e),
      code,
      details,
    };
    console.log(JSON.stringify(err, null, 2));
    process.exit(1);
  } finally {
    try { if (existsSync(tmpMp3)) unlinkSync(tmpMp3); } catch { /* ignore */ }
  }
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  main();
}
