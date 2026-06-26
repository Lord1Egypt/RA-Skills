import path from "node:path";

import { resolveWecomEgressProxyUrlFromNetwork } from "../config/index.js";
import { wecomFetch } from "../http.js";
import type { WecomNetworkConfig } from "../types/index.js";

function inferContentTypeFromFilePath(filePath: string): string {
  const ext = path.extname(filePath).slice(1).toLowerCase();
  const mimeTypes: Record<string, string> = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    webp: "image/webp",
    bmp: "image/bmp",
    mp3: "audio/mpeg",
    wav: "audio/wav",
    amr: "audio/amr",
    mp4: "video/mp4",
    pdf: "application/pdf",
    doc: "application/msword",
    docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    xls: "application/vnd.ms-excel",
    xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ppt: "application/vnd.ms-powerpoint",
    pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    txt: "text/plain",
    csv: "text/csv",
    tsv: "text/tab-separated-values",
    md: "text/markdown",
    json: "application/json",
    xml: "application/xml",
    yaml: "application/yaml",
    yml: "application/yaml",
    zip: "application/zip",
    rar: "application/vnd.rar",
    "7z": "application/x-7z-compressed",
    tar: "application/x-tar",
    gz: "application/gzip",
    tgz: "application/gzip",
    rtf: "application/rtf",
    odt: "application/vnd.oasis.opendocument.text",
  };
  return mimeTypes[ext] || "application/octet-stream";
}

export async function resolveOutboundMediaAsset(params: {
  mediaUrl: string;
  network?: WecomNetworkConfig;
  timeoutMs?: number;
}): Promise<{ buffer: Buffer; filename: string; contentType: string }> {
  const { mediaUrl, network, timeoutMs = 30000 } = params;
  if (/^https?:\/\//i.test(mediaUrl)) {
    const response = await wecomFetch(
      mediaUrl,
      { method: "GET" },
      {
        proxyUrl: resolveWecomEgressProxyUrlFromNetwork(network),
        timeoutMs,
      },
    );
    if (!response.ok) {
      throw new Error(`Failed to download media: ${response.status}`);
    }
    const buffer = Buffer.from(await response.arrayBuffer());
    const contentType = response.headers.get("content-type") || "application/octet-stream";
    const filename = path.basename(new URL(mediaUrl).pathname) || "media";
    return { buffer, filename, contentType };
  }

  const fs = await import("node:fs/promises");
  const buffer = await fs.readFile(mediaUrl);
  return {
    buffer,
    filename: path.basename(mediaUrl),
    contentType: inferContentTypeFromFilePath(mediaUrl),
  };
}