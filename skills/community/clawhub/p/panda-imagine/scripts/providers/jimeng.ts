import { createHmac, createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile, mkdtemp, readdir } from "node:fs/promises";
import { tmpdir, homedir } from "node:os";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "jimeng_t2i_v40";
const SERVICE = "cv";
const CLI_POLL_SECONDS = 120;

const SIZE_PRESETS: Record<string, Record<string, { w: number; h: number }>> = {
  "1:1": { normal: { w: 1024, h: 1024 }, "2k": { w: 1536, h: 1536 } },
  "16:9": { normal: { w: 1280, h: 720 }, "2k": { w: 1920, h: 1080 } },
  "9:16": { normal: { w: 720, h: 1280 }, "2k": { w: 1080, h: 1920 } },
  "4:3": { normal: { w: 1280, h: 960 }, "2k": { w: 1440, h: 1080 } },
  "3:4": { normal: { w: 960, h: 1280 }, "2k": { w: 1080, h: 1440 } },
};

function resolveSize(args: CliArgs): { width: number; height: number } {
  if (args.size) {
    const m = args.size.match(/^(\d+)[x*](\d+)$/);
    if (m) return { width: parseInt(m[1]!, 10), height: parseInt(m[2]!, 10) };
  }
  const quality = args.quality === "normal" ? "normal" : "2k";
  const key = args.aspectRatio ?? "1:1";
  const preset = SIZE_PRESETS[key]?.[quality] ?? SIZE_PRESETS["1:1"]![quality];
  return { width: preset.w, height: preset.h };
}

export function getDefaultModel(): string {
  return process.env.JIMENG_IMAGE_MODEL || DEFAULT_MODEL;
}

// ---------------------------------------------------------------------------
// dreamina CLI 检测
// ---------------------------------------------------------------------------

let _cliChecked: boolean | null = null;

export function isDreaminaAvailable(): boolean {
  if (_cliChecked !== null) return _cliChecked;
  const credPath = path.join(homedir(), ".dreamina_cli", "credential.json");
  _cliChecked = existsSync(credPath);
  return _cliChecked;
}

function runCommand(cmd: string, args: string[]): Promise<{ stdout: string; stderr: string; code: number }> {
  return new Promise((resolve, reject) => {
    const proc = spawn(cmd, args, { stdio: ["ignore", "pipe", "pipe"] });
    const stdoutBufs: Buffer[] = [];
    const stderrBufs: Buffer[] = [];
    proc.stdout.on("data", (d: Buffer) => stdoutBufs.push(d));
    proc.stderr.on("data", (d: Buffer) => stderrBufs.push(d));
    proc.on("close", (code) => {
      resolve({
        stdout: Buffer.concat(stdoutBufs).toString("utf8"),
        stderr: Buffer.concat(stderrBufs).toString("utf8"),
        code: code ?? 1,
      });
    });
    proc.on("error", reject);
  });
}

// ---------------------------------------------------------------------------
// dreamina CLI 模式
// ---------------------------------------------------------------------------

function extractJsonFromOutput(output: string): any | null {
  const lines = output.split("\n");
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i]!.trim();
    if (line.startsWith("{")) {
      try { return JSON.parse(line); } catch { /* 继续 */ }
    }
  }
  const jsonBlock = output.match(/\{[\s\S]*?\n\}/);
  if (jsonBlock) {
    try { return JSON.parse(jsonBlock[0]); } catch { /* 忽略 */ }
  }
  return null;
}

function findImageUrls(obj: any, urls: string[] = []): string[] {
  if (!obj || typeof obj !== "object") return urls;
  if (typeof obj === "string" && (obj.startsWith("http://") || obj.startsWith("https://")) &&
      /\.(png|jpg|jpeg|webp)/i.test(obj)) {
    urls.push(obj);
    return urls;
  }
  for (const val of Object.values(obj)) {
    if (typeof val === "string" && (val.startsWith("http://") || val.startsWith("https://")) &&
        /\.(png|jpg|jpeg|webp)/i.test(val)) {
      urls.push(val);
    } else if (typeof val === "object" && val !== null) {
      findImageUrls(val, urls);
    }
  }
  return urls;
}

function findSubmitId(obj: any): string | null {
  if (!obj || typeof obj !== "object") return null;
  if (obj.submit_id) return String(obj.submit_id);
  if (obj.data?.submit_id) return String(obj.data.submit_id);
  return null;
}

async function downloadToBytes(url: string): Promise<Uint8Array> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`下载图片失败 (${res.status})`);
  return new Uint8Array(await res.arrayBuffer());
}

async function generateViaCli(prompt: string, args: CliArgs): Promise<Uint8Array> {
  const cliArgs: string[] = [];
  const resolution = args.quality === "normal" ? "1k" : "2k";

  if (args.referenceImages.length) {
    cliArgs.push("image2image");
    cliArgs.push("--images", path.resolve(args.referenceImages[0]!));
    cliArgs.push(`--prompt=${prompt}`);
  } else {
    cliArgs.push("text2image");
    cliArgs.push(`--prompt=${prompt}`);
  }

  if (args.aspectRatio) cliArgs.push(`--ratio=${args.aspectRatio}`);
  cliArgs.push(`--resolution_type=${resolution}`);
  cliArgs.push(`--poll=${CLI_POLL_SECONDS}`);

  console.error(`即梦 CLI: dreamina ${cliArgs.join(" ")}`);

  const { stdout, stderr, code } = await runCommand("dreamina", cliArgs);
  const combined = stdout + "\n" + stderr;

  if (code !== 0 && !stdout.includes("submit_id") && !stdout.includes("success")) {
    throw new Error(`dreamina 命令失败 (exit ${code}): ${stderr || stdout}`);
  }

  const result = extractJsonFromOutput(combined);

  if (result) {
    const imageUrls = findImageUrls(result);
    if (imageUrls.length) return downloadToBytes(imageUrls[0]!);

    const submitId = findSubmitId(result);
    if (submitId) return downloadViaQueryResult(submitId);
  }

  throw new Error("即梦 CLI 未返回可用的图片结果。请检查 dreamina 登录状态（运行 dreamina user_credit）");
}

async function downloadViaQueryResult(submitId: string): Promise<Uint8Array> {
  const tmpDir = await mkdtemp(path.join(tmpdir(), "panda-jimeng-"));

  console.error(`即梦 CLI: 轮询异步任务 ${submitId}...`);

  const maxAttempts = 60;
  for (let i = 0; i < maxAttempts; i++) {
    const { stdout, stderr } = await runCommand("dreamina", [
      "query_result", `--submit_id=${submitId}`, `--download_dir=${tmpDir}`,
    ]);

    const files = await readdir(tmpDir);
    const imgFile = files.find(f => /\.(png|jpg|jpeg|webp)$/i.test(f));
    if (imgFile) {
      return new Uint8Array(await readFile(path.join(tmpDir, imgFile)));
    }

    const result = extractJsonFromOutput(stdout + "\n" + stderr);
    if (result) {
      const imageUrls = findImageUrls(result);
      if (imageUrls.length) return downloadToBytes(imageUrls[0]!);

      const status = result.status ?? result.data?.status ?? result.gen_status;
      if (status === "failed" || status === "error") {
        throw new Error(`即梦任务失败: ${JSON.stringify(result)}`);
      }
    }

    await new Promise(r => setTimeout(r, 2000));
  }

  throw new Error("即梦 CLI 任务超时（120秒）");
}

// ---------------------------------------------------------------------------
// 火山引擎 API 模式（HMAC-SHA256 签名）
// ---------------------------------------------------------------------------

function hmacSha256(key: string | Buffer, data: string): Buffer {
  return createHmac("sha256", key).update(data).digest();
}

function sha256Hex(data: string): string {
  return createHash("sha256").update(data).digest("hex");
}

function buildAuth(
  method: string, urlPath: string, query: string, bodyHash: string,
  accessKeyId: string, secretAccessKey: string, region: string, date: string,
): string {
  const shortDate = date.slice(0, 8);
  const scope = `${shortDate}/${region}/${SERVICE}/request`;
  const signedHeaders = "content-type;host;x-date";
  const host = new URL(process.env.JIMENG_BASE_URL || "https://visual.volcengineapi.com").host;

  const canonicalRequest = [
    method, urlPath, query,
    `content-type:application/json`, `host:${host}`, `x-date:${date}`,
    "", signedHeaders, bodyHash,
  ].join("\n");

  const stringToSign = `HMAC-SHA256\n${date}\n${scope}\n${sha256Hex(canonicalRequest)}`;

  let signingKey: Buffer = Buffer.from(secretAccessKey, "utf8");
  signingKey = hmacSha256(signingKey, shortDate);
  signingKey = hmacSha256(signingKey, region);
  signingKey = hmacSha256(signingKey, SERVICE);
  signingKey = hmacSha256(signingKey, "request");

  const signature = hmacSha256(signingKey, stringToSign).toString("hex");
  return `HMAC-SHA256 Credential=${accessKeyId}/${scope}, SignedHeaders=${signedHeaders}, Signature=${signature}`;
}

async function callApi(action: string, body: Record<string, unknown>): Promise<any> {
  const accessKeyId = process.env.JIMENG_ACCESS_KEY_ID;
  const secretAccessKey = process.env.JIMENG_SECRET_ACCESS_KEY;
  if (!accessKeyId || !secretAccessKey) throw new Error("需要设置 JIMENG_ACCESS_KEY_ID 和 JIMENG_SECRET_ACCESS_KEY");

  const baseUrl = (process.env.JIMENG_BASE_URL || "https://visual.volcengineapi.com").replace(/\/+$/, "");
  const region = process.env.JIMENG_REGION || "cn-north-1";
  const version = "2022-08-31";
  const queryString = `Action=${action}&Version=${version}`;
  const jsonBody = JSON.stringify(body);
  const bodyHash = sha256Hex(jsonBody);
  const now = new Date();
  const xDate = now.toISOString().replace(/[-:]/g, "").replace(/\.\d+Z$/, "Z");

  const auth = buildAuth("POST", "/", queryString, bodyHash, accessKeyId, secretAccessKey, region, xDate);

  const res = await fetch(`${baseUrl}/?${queryString}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Date": xDate, Authorization: auth },
    body: jsonBody,
  });

  if (!res.ok) throw new Error(`即梦 API error (${res.status}): ${await res.text()}`);
  return res.json();
}

async function generateViaApi(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  if (args.referenceImages.length) {
    throw new Error("即梦 API 模式不支持 --ref 参考图。请安装 dreamina CLI（curl -fsSL https://jimeng.jianying.com/cli | bash）以获得参考图支持");
  }

  const { width, height } = resolveSize(args);

  const submitResult = await callApi("CVSync2AsyncSubmitTask", {
    req_key: model, prompt, width, height,
  });

  if (submitResult.code !== 10000) {
    throw new Error(`即梦提交失败 (${submitResult.code}): ${submitResult.message ?? JSON.stringify(submitResult)}`);
  }

  const taskId = submitResult.data?.task_id;
  if (!taskId) throw new Error("即梦未返回 task_id");

  const maxPoll = 120;
  for (let i = 0; i < maxPoll; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const pollResult = await callApi("CVSync2AsyncGetResult", { req_key: model, task_id: taskId });

    if (pollResult.code === 10000 && pollResult.data?.status === "done") {
      const b64 = pollResult.data.binary_data_base64?.[0];
      if (b64) return Uint8Array.from(Buffer.from(b64, "base64"));
      const url = pollResult.data.image_urls?.[0];
      if (url) {
        const imgRes = await fetch(url);
        if (!imgRes.ok) throw new Error("下载图片失败");
        return new Uint8Array(await imgRes.arrayBuffer());
      }
      throw new Error("即梦任务完成但无图片数据");
    }

    if (pollResult.code !== 10000 && pollResult.data?.status !== "running") {
      throw new Error(`即梦轮询错误 (${pollResult.code}): ${pollResult.message ?? ""}`);
    }
  }

  throw new Error("即梦任务超时（240秒）");
}

// ---------------------------------------------------------------------------
// 统一入口：CLI 优先，API fallback
// ---------------------------------------------------------------------------

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const hasApiKeys = !!(process.env.JIMENG_ACCESS_KEY_ID && process.env.JIMENG_SECRET_ACCESS_KEY);
  const hasCli = isDreaminaAvailable();

  if (hasCli) {
    console.error("即梦: 使用 dreamina CLI 模式");
    return generateViaCli(prompt, args);
  }

  if (hasApiKeys) {
    console.error("即梦: 使用火山引擎 API 模式");
    return generateViaApi(prompt, model, args);
  }

  throw new Error(
    "即梦需要以下任一配置：\n" +
    "  1. 安装 dreamina CLI（推荐）：curl -fsSL https://jimeng.jianying.com/cli | bash\n" +
    "  2. 设置 JIMENG_ACCESS_KEY_ID + JIMENG_SECRET_ACCESS_KEY 环境变量"
  );
}
