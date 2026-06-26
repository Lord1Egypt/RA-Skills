import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "google/nano-banana-pro";
const MAX_POLL = 300;
const POLL_INTERVAL = 2000;

export function getDefaultModel(): string {
  return process.env.REPLICATE_IMAGE_MODEL || DEFAULT_MODEL;
}

async function fileToDataUrl(filePath: string): Promise<string> {
  const buf = await readFile(path.resolve(filePath));
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg"
    : ext === ".webp" ? "image/webp" : "image/png";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

function parseModelId(model: string): { owner: string; name: string; version: string | null } {
  const versionIdx = model.indexOf(":");
  if (versionIdx >= 0) {
    const ownerName = model.slice(0, versionIdx);
    const version = model.slice(versionIdx + 1);
    const slash = ownerName.indexOf("/");
    return { owner: ownerName.slice(0, slash), name: ownerName.slice(slash + 1), version };
  }
  const slash = model.indexOf("/");
  return { owner: model.slice(0, slash), name: model.slice(slash + 1), version: null };
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiToken = process.env.REPLICATE_API_TOKEN;
  if (!apiToken) throw new Error("需要设置 REPLICATE_API_TOKEN");

  const baseUrl = (process.env.REPLICATE_BASE_URL || "https://api.replicate.com").replace(/\/+$/, "");
  const { owner, name, version } = parseModelId(model);

  const input: Record<string, unknown> = {
    prompt,
    number_of_images: 1,
    output_format: "png",
  };

  if (args.aspectRatio) {
    input.aspect_ratio = args.aspectRatio;
  } else if (args.referenceImages.length) {
    input.aspect_ratio = "match_input_image";
  }

  const resolution = args.quality === "normal" ? "1K" : "2K";
  input.resolution = resolution;

  if (args.referenceImages.length) {
    input.image_input = await fileToDataUrl(args.referenceImages[0]!);
  }

  let url: string;
  let body: Record<string, unknown>;
  if (version) {
    url = `${baseUrl}/v1/predictions`;
    body = { version, input };
  } else {
    url = `${baseUrl}/v1/models/${owner}/${name}/predictions`;
    body = { input };
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiToken}`,
    Prefer: "wait=60",
  };

  const createRes = await fetch(url, { method: "POST", headers, body: JSON.stringify(body) });
  if (!createRes.ok) throw new Error(`Replicate API error (${createRes.status}): ${await createRes.text()}`);

  let prediction = await createRes.json() as any;

  if (prediction.status === "succeeded") {
    return extractOutput(prediction);
  }

  const getUrl = prediction.urls?.get;
  if (!getUrl) throw new Error("Replicate 未返回轮询 URL");

  for (let i = 0; i < MAX_POLL; i++) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL));
    const pollRes = await fetch(getUrl, {
      headers: { Authorization: `Bearer ${apiToken}` },
    });
    if (!pollRes.ok) throw new Error(`Replicate 轮询错误 (${pollRes.status})`);
    prediction = await pollRes.json();

    if (prediction.status === "succeeded") return extractOutput(prediction);
    if (prediction.status === "failed" || prediction.status === "canceled") {
      throw new Error(`Replicate 任务失败: ${prediction.error ?? prediction.status}`);
    }
  }

  throw new Error("Replicate 任务超时");
}

async function extractOutput(prediction: any): Promise<Uint8Array> {
  const output = prediction.output;
  let imageUrl: string | null = null;

  if (typeof output === "string") {
    imageUrl = output;
  } else if (Array.isArray(output) && typeof output[0] === "string") {
    imageUrl = output[0];
  } else if (output?.url) {
    imageUrl = output.url;
  }

  if (!imageUrl) throw new Error("Replicate 响应中没有图片数据");

  if (imageUrl.startsWith("data:")) {
    const b64 = imageUrl.split(",")[1];
    if (b64) return Uint8Array.from(Buffer.from(b64, "base64"));
  }

  const res = await fetch(imageUrl);
  if (!res.ok) throw new Error("下载图片失败");
  return new Uint8Array(await res.arrayBuffer());
}
