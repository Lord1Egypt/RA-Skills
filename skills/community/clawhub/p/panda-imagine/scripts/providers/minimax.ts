import { readFile } from "node:fs/promises";
import path from "node:path";
import type { CliArgs } from "../types";

const DEFAULT_MODEL = "image-01";
const VALID_RATIOS = ["1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16", "21:9"];

export function getDefaultModel(): string {
  return process.env.MINIMAX_IMAGE_MODEL || DEFAULT_MODEL;
}

export function validateArgs(model: string, args: CliArgs): void {
  if (args.size) {
    if (model !== "image-01") {
      console.warn("MiniMax 自定义尺寸仅 image-01 支持");
    }
    const m = args.size.match(/^(\d+)[x*](\d+)$/);
    if (m) {
      const w = parseInt(m[1]!, 10);
      const h = parseInt(m[2]!, 10);
      if (w < 512 || w > 2048 || h < 512 || h > 2048 || w % 8 !== 0 || h % 8 !== 0) {
        throw new Error("MiniMax 尺寸需在 512-2048 之间且为 8 的倍数");
      }
    }
  }
}

async function fileToDataUrl(filePath: string): Promise<string> {
  const buf = await readFile(path.resolve(filePath));
  const ext = path.extname(filePath).toLowerCase();
  if (ext !== ".jpg" && ext !== ".jpeg" && ext !== ".png") {
    throw new Error("MiniMax 参考图仅支持 JPG/PNG 格式");
  }
  const mime = ext === ".png" ? "image/png" : "image/jpeg";
  return `data:${mime};base64,${buf.toString("base64")}`;
}

export async function generateImage(prompt: string, model: string, args: CliArgs): Promise<Uint8Array> {
  const apiKey = process.env.MINIMAX_API_KEY;
  if (!apiKey) throw new Error("需要设置 MINIMAX_API_KEY");

  let baseUrl = (process.env.MINIMAX_BASE_URL || "https://api.minimax.io").replace(/\/+$/, "");
  if (!baseUrl.endsWith("/v1")) baseUrl += "/v1";

  const body: Record<string, unknown> = {
    model, prompt, response_format: "base64", n: args.n,
  };

  if (args.size) {
    const m = args.size.match(/^(\d+)[x*](\d+)$/);
    if (m) { body.width = parseInt(m[1]!, 10); body.height = parseInt(m[2]!, 10); }
  } else if (args.aspectRatio && VALID_RATIOS.includes(args.aspectRatio)) {
    body.aspect_ratio = args.aspectRatio;
  }

  if (args.referenceImages.length) {
    const refs: { type: string; image_file: string }[] = [];
    for (const ref of args.referenceImages) {
      refs.push({ type: "character", image_file: await fileToDataUrl(ref) });
    }
    body.subject_reference = refs;
  }

  const res = await fetch(`${baseUrl}/image_generation`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${apiKey}` },
    body: JSON.stringify(body),
  });

  if (!res.ok) throw new Error(`MiniMax API error (${res.status}): ${await res.text()}`);

  const json = await res.json() as any;
  if (json.base_resp?.status_code !== 0) {
    throw new Error(`MiniMax 业务错误: ${json.base_resp?.status_msg ?? JSON.stringify(json.base_resp)}`);
  }

  if (json.data?.image_base64?.[0]) {
    return Uint8Array.from(Buffer.from(json.data.image_base64[0], "base64"));
  }
  if (json.data?.image_urls?.[0]) {
    const imgRes = await fetch(json.data.image_urls[0]);
    if (!imgRes.ok) throw new Error("下载图片失败");
    return new Uint8Array(await imgRes.arrayBuffer());
  }
  throw new Error("MiniMax 响应中没有图片数据");
}
