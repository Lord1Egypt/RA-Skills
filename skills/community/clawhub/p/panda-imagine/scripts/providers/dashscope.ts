import type { CliArgs, Quality } from "../types";

const DEFAULT_MODEL = "qwen-image-2.0-pro";
const NEGATIVE_PROMPT = "低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感，构图混乱，文字模糊，扭曲";

type ModelFamily = "qwen2" | "qwenFixed" | "legacy";

const FAMILY_MAP: Record<string, ModelFamily> = {
  "qwen-image-2.0-pro": "qwen2", "qwen-image-2.0-pro-2026-03-03": "qwen2",
  "qwen-image-2.0": "qwen2", "qwen-image-2.0-2026-03-03": "qwen2",
  "qwen-image-max": "qwenFixed", "qwen-image-max-2025-12-30": "qwenFixed",
  "qwen-image-plus": "qwenFixed", "qwen-image-plus-2026-01-09": "qwenFixed",
  "qwen-image": "qwenFixed",
};

const QWEN2_SIZES: Record<string, Record<Quality, string>> = {
  "1:1": { normal: "1024*1024", "2k": "1536*1536" },
  "2:3": { normal: "768*1152", "2k": "1024*1536" },
  "3:2": { normal: "1152*768", "2k": "1536*1024" },
  "3:4": { normal: "960*1280", "2k": "1080*1440" },
  "4:3": { normal: "1280*960", "2k": "1440*1080" },
  "9:16": { normal: "720*1280", "2k": "1080*1920" },
  "16:9": { normal: "1280*720", "2k": "1920*1080" },
  "21:9": { normal: "1344*576", "2k": "2048*872" },
};

const FIXED_SIZES: Record<string, string> = {
  "16:9": "1664*928", "4:3": "1472*1104", "1:1": "1328*1328",
  "3:4": "1104*1472", "9:16": "928*1664",
};

function getFamily(model: string): ModelFamily {
  return FAMILY_MAP[model.trim().toLowerCase()] ?? "legacy";
}

function parseRatio(ar: string): number | null {
  const m = ar.match(/^(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)$/);
  if (!m) return null;
  return parseFloat(m[1]!) / parseFloat(m[2]!);
}

function closestRatioKey(ar: string, keys: string[]): string | null {
  const target = parseRatio(ar);
  if (target == null) return null;
  let best: string | null = null;
  let bestDiff = Infinity;
  for (const k of keys) {
    const r = parseRatio(k);
    if (r == null) continue;
    const d = Math.abs(r - target);
    if (d < bestDiff) { bestDiff = d; best = k; }
  }
  return bestDiff <= 0.02 ? best : null;
}

function resolveSize(model: string, args: Pick<CliArgs, "size" | "aspectRatio" | "quality">): string {
  const family = getFamily(model);
  const quality: Quality = args.quality === "normal" ? "normal" : "2k";

  if (args.size) return args.size.replace("x", "*");

  if (family === "qwen2") {
    const key = args.aspectRatio ? closestRatioKey(args.aspectRatio, Object.keys(QWEN2_SIZES)) : null;
    return QWEN2_SIZES[key ?? "1:1"]![quality];
  }

  if (family === "qwenFixed") {
    const key = args.aspectRatio ? closestRatioKey(args.aspectRatio, Object.keys(FIXED_SIZES)) : null;
    if (!key && args.aspectRatio)
      throw new Error(`qwen-image-max/plus 仅支持固定比例 ${Object.keys(FIXED_SIZES).join(", ")}，自定义比例请用 --model qwen-image-2.0-pro`);
    return FIXED_SIZES[key ?? "16:9"]!;
  }

  return quality === "2k" ? "1536*1536" : "1024*1024";
}

export function getDefaultModel(): string {
  return process.env.DASHSCOPE_IMAGE_MODEL || DEFAULT_MODEL;
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.DASHSCOPE_API_KEY;
  if (!apiKey) throw new Error("需要设置 DASHSCOPE_API_KEY");
  if (args.referenceImages.length) throw new Error("DashScope 不支持 --ref 参考图，请使用 --provider google 等");

  const family = getFamily(model);
  const size = resolveSize(model, args);
  const baseUrl = (process.env.DASHSCOPE_BASE_URL || "https://dashscope.aliyuncs.com").replace(/\/+$/, "");

  const parameters: Record<string, unknown> = { prompt_extend: false, size };
  if (family === "qwen2" || family === "qwenFixed") {
    parameters.watermark = false;
    parameters.negative_prompt = NEGATIVE_PROMPT;
  }

  const body = {
    model,
    input: { messages: [{ role: "user", content: [{ text: prompt }] }] },
    parameters,
  };

  console.error(`DashScope (${model}): 尺寸 ${size}`);

  const res = await fetch(`${baseUrl}/api/v1/services/aigc/multimodal-generation/generation`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`DashScope API error (${res.status}): ${await res.text()}`);

  const result = await res.json() as {
    output?: {
      result_image?: string;
      choices?: Array<{ message?: { content?: Array<{ image?: string }> } }>;
    };
  };

  let imageData: string | null = null;
  if (result.output?.result_image) {
    imageData = result.output.result_image;
  } else {
    const content = result.output?.choices?.[0]?.message?.content;
    if (content) for (const item of content) { if (item.image) { imageData = item.image; break; } }
  }

  if (!imageData) throw new Error("DashScope 响应中没有图片数据");

  if (imageData.startsWith("http")) {
    const imgRes = await fetch(imageData);
    if (!imgRes.ok) throw new Error("下载图片失败");
    return new Uint8Array(await imgRes.arrayBuffer());
  }
  return Uint8Array.from(Buffer.from(imageData, "base64"));
}
