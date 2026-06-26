import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "doubao-seedream-5-0-260128";

type SeedreamFamily = "v5" | "v4.5" | "v4" | "v3" | "unknown";

function getFamily(model: string): SeedreamFamily {
  const m = model.toLowerCase();
  if (m.includes("seedream-5") || m.includes("seedream5")) return "v5";
  if (m.includes("seedream-4-5") || m.includes("seedream-4.5")) return "v4.5";
  if (m.includes("seedream-4") || m.includes("seedream4")) return "v4";
  if (m.includes("seedream-3") || m.includes("seedream3")) return "v3";
  return "unknown";
}

const SIZE_PRESETS: Record<string, Record<string, string>> = {
  "1:1": { normal: "1024x1024", "2k": "2048x2048" },
  "16:9": { normal: "1280x720", "2k": "1920x1080" },
  "9:16": { normal: "720x1280", "2k": "1080x1920" },
  "4:3": { normal: "1280x960", "2k": "1440x1080" },
  "3:4": { normal: "960x1280", "2k": "1080x1440" },
  "3:2": { normal: "1152x768", "2k": "1536x1024" },
  "2:3": { normal: "768x1152", "2k": "1024x1536" },
};

function resolveSize(args: CliArgs): string {
  if (args.size) return args.size.replace("*", "x");
  const quality = args.quality === "normal" ? "normal" : "2k";
  const key = args.aspectRatio ?? "1:1";
  return SIZE_PRESETS[key]?.[quality] ?? SIZE_PRESETS["1:1"]![quality];
}

export function getDefaultModel(): string {
  return process.env.SEEDREAM_IMAGE_MODEL || DEFAULT_MODEL;
}

async function fileToDataUrl(filePath: string): Promise<string> {
  const buf = await readFile(path.resolve(filePath));
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" : "image/png";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.ARK_API_KEY;
  if (!apiKey) throw new Error("需要设置 ARK_API_KEY");

  const family = getFamily(model);
  const baseUrl = (process.env.SEEDREAM_BASE_URL || "https://ark.cn-beijing.volces.com/api/v3").replace(/\/+$/, "");

  if (args.referenceImages.length) {
    if (family === "v3") throw new Error("Seedream 3.0 不支持 --ref 参考图");
  }

  const size = resolveSize(args);
  const body: Record<string, unknown> = {
    model, prompt, size, response_format: "url", watermark: false,
  };

  if (family === "v5") body.output_format = "png";

  if (args.referenceImages.length) {
    if (args.referenceImages.length === 1) {
      body.image = await fileToDataUrl(args.referenceImages[0]!);
    } else {
      body.image = await Promise.all(args.referenceImages.map(f => fileToDataUrl(f)));
    }
  }

  const res = await fetch(`${baseUrl}/images/generations`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`Seedream API error (${res.status}): ${await res.text()}`);

  const json = await res.json() as any;
  const item = json.data?.[0];
  if (!item) throw new Error("Seedream 响应中没有图片数据");
  if (item.error) throw new Error(`Seedream 错误: ${item.error.message ?? JSON.stringify(item.error)}`);

  if (item.b64_json) return Uint8Array.from(Buffer.from(item.b64_json, "base64"));
  if (item.url) {
    const imgRes = await fetch(item.url);
    if (!imgRes.ok) throw new Error("下载图片失败");
    return new Uint8Array(await imgRes.arrayBuffer());
  }
  throw new Error("Seedream 响应格式未知");
}
