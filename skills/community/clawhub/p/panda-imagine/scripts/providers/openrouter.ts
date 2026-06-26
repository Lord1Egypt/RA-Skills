import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "google/gemini-3.1-flash-image-preview";

function getImageSize(quality: string | null, imageSize: string | null): string {
  if (imageSize) return imageSize;
  return quality === "normal" ? "1K" : "2K";
}

export function getDefaultModel(): string {
  return process.env.OPENROUTER_IMAGE_MODEL || DEFAULT_MODEL;
}

async function fileToDataUrl(filePath: string): Promise<string> {
  const buf = await readFile(path.resolve(filePath));
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg"
    : ext === ".webp" ? "image/webp" : "image/png";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.OPENROUTER_API_KEY;
  if (!apiKey) throw new Error("需要设置 OPENROUTER_API_KEY");

  const baseUrl = (process.env.OPENROUTER_BASE_URL || "https://openrouter.ai/api/v1").replace(/\/+$/, "");
  const imgSize = getImageSize(args.quality, args.imageSize);

  const contentParts: any[] = [];

  for (const ref of args.referenceImages) {
    contentParts.push({ type: "image_url", image_url: { url: await fileToDataUrl(ref) } });
  }
  contentParts.push({ type: "text", text: prompt });

  const imageConfig: Record<string, unknown> = { image_size: imgSize };
  if (args.aspectRatio) imageConfig.aspect_ratio = args.aspectRatio;
  if (args.size) {
    const m = args.size.match(/^(\d+)[x*](\d+)$/);
    if (m) {
      const w = parseInt(m[1]!, 10);
      const h = parseInt(m[2]!, 10);
      const ratio = w > h ? `${Math.round(w / h * 10) / 10}:1` : `1:${Math.round(h / w * 10) / 10}`;
      imageConfig.aspect_ratio = ratio;
    }
  }

  const body: Record<string, unknown> = {
    model,
    messages: [{ role: "user", content: args.referenceImages.length ? contentParts : prompt }],
    modalities: ["image"],
    stream: false,
    image_config: imageConfig,
    provider: { require_parameters: true },
  };

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${apiKey}`,
  };
  if (process.env.OPENROUTER_HTTP_REFERER) headers["HTTP-Referer"] = process.env.OPENROUTER_HTTP_REFERER;
  if (process.env.OPENROUTER_TITLE) headers["X-Title"] = process.env.OPENROUTER_TITLE;

  const res = await fetch(`${baseUrl}/chat/completions`, {
    method: "POST", headers, body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`OpenRouter API error (${res.status}): ${await res.text()}`);

  const json = await res.json() as any;
  const choice = json.choices?.[0];
  if (!choice) throw new Error("OpenRouter 响应中没有选项");

  if (choice.message?.images?.[0]) {
    return downloadImage(choice.message.images[0]);
  }

  const content = choice.message?.content;
  if (typeof content === "string") {
    const b64Match = content.match(/data:image\/[^;]+;base64,([A-Za-z0-9+/=]+)/);
    if (b64Match) return Uint8Array.from(Buffer.from(b64Match[1]!, "base64"));
  }
  if (Array.isArray(content)) {
    for (const part of content) {
      if (part.type === "image_url" && part.image_url?.url) {
        return downloadImage(part.image_url.url);
      }
    }
  }

  throw new Error("OpenRouter 响应中没有图片数据");
}

async function downloadImage(urlOrData: string): Promise<Uint8Array> {
  if (urlOrData.startsWith("data:")) {
    const b64 = urlOrData.split(",")[1];
    if (b64) return Uint8Array.from(Buffer.from(b64, "base64"));
  }
  if (/^[A-Za-z0-9+/=]{100,}$/.test(urlOrData)) {
    return Uint8Array.from(Buffer.from(urlOrData, "base64"));
  }
  const res = await fetch(urlOrData);
  if (!res.ok) throw new Error("下载图片失败");
  return new Uint8Array(await res.arrayBuffer());
}
