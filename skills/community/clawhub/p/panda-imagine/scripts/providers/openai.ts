import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "gpt-image-1.5";

const SIZE_MAP: Record<string, Record<string, string>> = {
  "gpt-image": {
    "1:1": "1024x1024", "16:9": "1536x1024", "9:16": "1024x1536",
    "4:3": "1536x1024", "3:4": "1024x1536", "2.35:1": "1536x1024",
  },
  "dall-e-3": {
    "1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792",
    "4:3": "1792x1024", "3:4": "1024x1792",
  },
};

function getOpenAISize(model: string, ar: string | null, quality: string | null): string {
  const family = model.startsWith("dall-e-3") ? "dall-e-3" : "gpt-image";
  const map = SIZE_MAP[family]!;
  if (!ar) return quality === "2k" && family === "gpt-image" ? "2048x2048" : "1024x1024";
  return map[ar] ?? "1024x1024";
}

function isEditsModel(model: string): boolean {
  return model.startsWith("gpt-image") || model.startsWith("gpt-4o");
}

export function getDefaultModel(): string {
  return process.env.OPENAI_IMAGE_MODEL || DEFAULT_MODEL;
}

export function getDefaultOutputExtension(model: string, _args: CliArgs): string {
  return model.startsWith("gpt-image") ? ".png" : ".png";
}

async function fileToBase64(filePath: string): Promise<string> {
  const buf = await readFile(path.resolve(filePath));
  return buf.toString("base64");
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error("需要设置 OPENAI_API_KEY");
  const baseUrl = (process.env.OPENAI_BASE_URL || "https://api.openai.com/v1").replace(/\/+$/, "");
  const size = args.size?.replace("*", "x") ?? getOpenAISize(model, args.aspectRatio, args.quality);
  const headers: Record<string, string> = { Authorization: `Bearer ${apiKey}` };

  if (args.referenceImages.length) {
    if (!isEditsModel(model)) throw new Error(`${model} 不支持 --ref，请使用 gpt-image 系列模型`);

    const form = new FormData();
    form.append("model", model);
    form.append("prompt", prompt);
    form.append("size", size);
    if (model.startsWith("gpt-image")) {
      form.append("quality", args.quality === "2k" ? "high" : "medium");
    }
    for (const refPath of args.referenceImages) {
      const buf = await readFile(path.resolve(refPath));
      const ext = path.extname(refPath).toLowerCase();
      const mime = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : "image/png";
      form.append("image[]", new Blob([buf], { type: mime }), path.basename(refPath));
    }

    const res = await fetch(`${baseUrl}/images/edits`, { method: "POST", headers, body: form });
    if (!res.ok) throw new Error(`OpenAI API error (${res.status}): ${await res.text()}`);
    return extractImage(await res.json());
  }

  const body: Record<string, unknown> = { model, prompt, size, n: 1 };
  if (model.startsWith("gpt-image")) {
    body.quality = args.quality === "2k" ? "high" : "medium";
  } else if (model.startsWith("dall-e-3")) {
    body.quality = args.quality === "2k" ? "hd" : "standard";
  }

  headers["Content-Type"] = "application/json";
  const res = await fetch(`${baseUrl}/images/generations`, {
    method: "POST", headers, body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`OpenAI API error (${res.status}): ${await res.text()}`);
  return extractImage(await res.json());
}

function extractImage(json: any): Uint8Array {
  const item = json?.data?.[0];
  if (!item) throw new Error("OpenAI 响应中没有图片数据");
  if (item.b64_json) return Uint8Array.from(Buffer.from(item.b64_json, "base64"));
  if (item.url) {
    return fetchImageUrl(item.url);
  }
  throw new Error("OpenAI 响应格式未知");
}

async function fetchImageUrl(url: string): Promise<Uint8Array> {
  const res = await fetch(url);
  if (!res.ok) throw new Error("下载图片失败");
  return new Uint8Array(await res.arrayBuffer());
}
