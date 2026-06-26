import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "gemini-3-pro-image-preview";

const MULTIMODAL_MODELS = [
  "gemini-3-pro-image-preview", "gemini-2.5-flash-preview-image",
  "gemini-2.5-pro-preview-image", "gemini-3.1-flash-image-preview",
];

function isMultimodal(model: string): boolean {
  return MULTIMODAL_MODELS.some(m => model.includes(m));
}

function getImageSize(quality: string | null, imageSize: string | null): string {
  if (imageSize) return imageSize;
  return quality === "normal" ? "1K" : "2K";
}

export function getDefaultModel(): string {
  return process.env.GOOGLE_IMAGE_MODEL || DEFAULT_MODEL;
}

async function fileToBase64(filePath: string): Promise<{ data: string; mimeType: string }> {
  const buf = await readFile(path.resolve(filePath));
  const ext = path.extname(filePath).toLowerCase();
  const mimeType = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg"
    : ext === ".webp" ? "image/webp" : "image/png";
  return { data: buf.toString("base64"), mimeType };
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY;
  if (!apiKey) throw new Error("需要设置 GOOGLE_API_KEY 或 GEMINI_API_KEY");

  const baseUrl = (process.env.GOOGLE_BASE_URL || "https://generativelanguage.googleapis.com").replace(/\/+$/, "");
  const versionedBase = baseUrl.endsWith("/v1beta") ? baseUrl : `${baseUrl}/v1beta`;
  const imgSize = getImageSize(args.quality, args.imageSize);

  if (args.referenceImages.length && !isMultimodal(model)) {
    throw new Error(`${model} 不支持 --ref，请使用 Gemini multimodal 模型`);
  }

  if (isMultimodal(model)) {
    return generateGemini(versionedBase, apiKey, model, prompt, args, imgSize);
  }

  return generateImagen(versionedBase, apiKey, model, prompt, args, imgSize);
}

async function generateGemini(
  base: string, apiKey: string, model: string,
  prompt: string, args: CliArgs, imgSize: string,
): Promise<Uint8Array> {
  const parts: any[] = [];

  for (const ref of args.referenceImages) {
    const { data, mimeType } = await fileToBase64(ref);
    parts.push({ inlineData: { data, mimeType } });
  }

  let textPrompt = prompt;
  if (args.aspectRatio) textPrompt += `\n\nAspect ratio: ${args.aspectRatio}`;
  parts.push({ text: textPrompt });

  const body = {
    contents: [{ role: "user", parts }],
    generationConfig: {
      responseModalities: ["IMAGE"],
      imageConfig: { imageSize: imgSize },
    },
  };

  const res = await fetch(`${base}/models/${model}:generateContent?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`Google API error (${res.status}): ${await res.text()}`);

  const json = await res.json() as any;
  const candidates = json.candidates ?? [];
  for (const c of candidates) {
    for (const p of c.content?.parts ?? []) {
      if (p.inlineData?.data) {
        return Uint8Array.from(Buffer.from(p.inlineData.data, "base64"));
      }
    }
  }
  throw new Error("Google 响应中没有图片数据");
}

async function generateImagen(
  base: string, apiKey: string, model: string,
  prompt: string, args: CliArgs, imgSize: string,
): Promise<Uint8Array> {
  const parameters: Record<string, unknown> = { sampleCount: 1, imageSize: imgSize };
  if (args.aspectRatio) parameters.aspectRatio = args.aspectRatio;

  const body = { instances: [{ prompt }], parameters };

  const res = await fetch(`${base}/models/${model}:predict?key=${apiKey}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "x-goog-api-key": apiKey },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`Google Imagen API error (${res.status}): ${await res.text()}`);

  const json = await res.json() as any;
  const predictions = json.predictions ?? json.generatedImages ?? [];
  for (const p of predictions) {
    const b64 = p.imageBytes ?? p.bytesBase64Encoded ?? p.data ?? p.image?.imageBytes;
    if (b64) return Uint8Array.from(Buffer.from(b64, "base64"));
  }
  throw new Error("Google Imagen 响应中没有图片数据");
}
