import path from "node:path";

import type { ResolvedKefuAccount } from "../../types/index.js";
import { resolveOutboundMediaAsset } from "../../shared/media-asset.js";
import { guessUploadContentType, normalizeUploadFilename } from "../agent-api/core.js";
import {
  sendKefuFile,
  sendKefuImage,
  sendKefuLink,
  sendKefuText,
  sendKefuVideo,
  sendKefuVoice,
  uploadKefuMedia,
} from "./api-client.js";

export type KefuDeliveryTarget = {
  kefu: ResolvedKefuAccount;
  openKfId: string;
  externalUserId: string;
};

const MAX_KEFU_TEXT_CHARS = 3500;

export async function deliverKefuText(
  target: KefuDeliveryTarget,
  text: string,
): Promise<{ msgid?: string }[]> {
  const trimmed = (text ?? "").trim();
  if (!trimmed) return [];
  const chunks: string[] = [];
  for (let i = 0; i < trimmed.length; i += MAX_KEFU_TEXT_CHARS) {
    chunks.push(trimmed.slice(i, i + MAX_KEFU_TEXT_CHARS));
  }
  const results: { msgid?: string }[] = [];
  for (const chunk of chunks) {
    const result = await sendKefuText({
      kefu: target.kefu,
      toUser: target.externalUserId,
      openKfid: target.openKfId,
      text: chunk,
    });
    results.push(result);
  }
  return results;
}

function classifyKefuMediaType(
  contentType: string,
  filename: string,
): "image" | "voice" | "video" | "file" {
  if (contentType.startsWith("image/")) return "image";
  if (contentType.startsWith("audio/")) return "voice";
  if (contentType.startsWith("video/")) return "video";
  const ext = path.extname(filename).toLowerCase();
  if ([".amr", ".mp3", ".wav", ".m4a", ".ogg"].includes(ext)) return "voice";
  if ([".mp4", ".mov"].includes(ext)) return "video";
  if ([".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"].includes(ext)) return "image";
  return "file";
}

export async function deliverKefuMediaUrl(
  target: KefuDeliveryTarget,
  mediaUrl: string,
): Promise<{ msgid?: string } | undefined> {
  const asset = await resolveOutboundMediaAsset({
    mediaUrl,
    network: target.kefu.network,
  });
  const filename = normalizeUploadFilename(asset.filename || "file.bin");
  const contentType = asset.contentType || guessUploadContentType(filename);
  const mediaType = classifyKefuMediaType(contentType, filename);
  const mediaId = await uploadKefuMedia({
    kefu: target.kefu,
    type: mediaType,
    buffer: asset.buffer,
    filename,
  });
  const args = {
    kefu: target.kefu,
    toUser: target.externalUserId,
    openKfid: target.openKfId,
    mediaId,
  };
  if (mediaType === "image") return sendKefuImage(args);
  if (mediaType === "voice") return sendKefuVoice(args);
  if (mediaType === "video") return sendKefuVideo(args);
  return sendKefuFile(args);
}

export async function deliverKefuLink(
  target: KefuDeliveryTarget,
  link: { title: string; desc?: string; url: string; thumbMediaId?: string },
): Promise<{ msgid?: string }> {
  return sendKefuLink({
    kefu: target.kefu,
    toUser: target.externalUserId,
    openKfid: target.openKfId,
    title: link.title,
    desc: link.desc,
    url: link.url,
    thumbMediaId: link.thumbMediaId,
  });
}
