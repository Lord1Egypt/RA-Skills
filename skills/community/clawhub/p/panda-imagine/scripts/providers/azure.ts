import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "gpt-image-1.5";

const SIZE_MAP: Record<string, string> = {
  "1:1": "1024x1024", "16:9": "1536x1024", "9:16": "1024x1536",
  "4:3": "1536x1024", "3:4": "1024x1536",
};

function getSize(ar: string | null, quality: string | null): string {
  if (!ar) return quality === "2k" ? "2048x2048" : "1024x1024";
  return SIZE_MAP[ar] ?? "1024x1024";
}

function parseBaseUrl(rawUrl: string): { resourceBase: string; deployment: string | null } {
  const url = rawUrl.replace(/\/+$/, "");
  const deployMatch = url.match(/\/deployments\/([^/]+)/);
  if (deployMatch) {
    return { resourceBase: url.slice(0, url.indexOf("/deployments/")), deployment: deployMatch[1]! };
  }
  const openaiMatch = url.match(/\/openai$/);
  if (openaiMatch) {
    return { resourceBase: url, deployment: null };
  }
  return { resourceBase: url.endsWith("/openai") ? url : `${url}/openai`, deployment: null };
}

export function getDefaultModel(): string {
  return process.env.AZURE_OPENAI_DEPLOYMENT || process.env.AZURE_OPENAI_IMAGE_MODEL || DEFAULT_MODEL;
}

export function validateArgs(_model: string, args: CliArgs): void {
  for (const ref of args.referenceImages) {
    const ext = path.extname(ref).toLowerCase();
    if (ext !== ".png" && ext !== ".jpg" && ext !== ".jpeg") {
      throw new Error("Azure OpenAI 参考图仅支持 PNG/JPG 格式");
    }
  }
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.AZURE_OPENAI_API_KEY;
  const rawBase = process.env.AZURE_OPENAI_BASE_URL;
  if (!apiKey) throw new Error("需要设置 AZURE_OPENAI_API_KEY");
  if (!rawBase) throw new Error("需要设置 AZURE_OPENAI_BASE_URL");

  const { resourceBase, deployment: urlDeployment } = parseBaseUrl(rawBase);
  const deployment = urlDeployment ?? model;
  const apiVersion = process.env.AZURE_API_VERSION || "2025-04-01-preview";
  const size = args.size?.replace("*", "x") ?? getSize(args.aspectRatio, args.quality);
  const qualityVal = args.quality === "2k" ? "high" : "medium";

  if (args.referenceImages.length) {
    const form = new FormData();
    form.append("prompt", prompt);
    form.append("size", size);
    form.append("n", "1");
    form.append("quality", qualityVal);
    for (const ref of args.referenceImages) {
      const buf = await readFile(path.resolve(ref));
      const ext = path.extname(ref).toLowerCase();
      const mime = ext === ".png" ? "image/png" : "image/jpeg";
      form.append("image[]", new Blob([buf], { type: mime }), path.basename(ref));
    }

    const res = await fetch(`${resourceBase}/deployments/${deployment}/images/edits?api-version=${apiVersion}`, {
      method: "POST",
      headers: { "api-key": apiKey },
      body: form,
    });
    if (!res.ok) throw new Error(`Azure API error (${res.status}): ${await res.text()}`);
    return extractImage(await res.json());
  }

  const body = { prompt, size, n: 1, quality: qualityVal };

  const res = await fetch(`${resourceBase}/deployments/${deployment}/images/generations?api-version=${apiVersion}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "api-key": apiKey },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Azure API error (${res.status}): ${await res.text()}`);
  return extractImage(await res.json());
}

function extractImage(json: any): Uint8Array {
  const item = json?.data?.[0];
  if (!item) throw new Error("Azure 响应中没有图片数据");
  if (item.b64_json) return Uint8Array.from(Buffer.from(item.b64_json, "base64"));
  if (item.url) return fetchUrl(item.url);
  throw new Error("Azure 响应格式未知");
}

async function fetchUrl(url: string): Promise<Uint8Array> {
  const res = await fetch(url);
  if (!res.ok) throw new Error("下载图片失败");
  return new Uint8Array(await res.arrayBuffer());
}
