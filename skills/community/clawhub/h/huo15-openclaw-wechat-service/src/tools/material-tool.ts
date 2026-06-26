/**
 * 素材管理 agent tool：临时/永久素材上传、图文内嵌图片、永久素材 CRUD。
 *
 * 上传支持：
 *  - 本地文件路径（filePath）
 *  - 远程 URL（url）
 *  - Base64 内容（base64）
 */

import fs from "node:fs/promises";

import { fetch as undiciFetch } from "undici";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  uploadTemporaryMedia,
  uploadPermanentImage,
  uploadPermanentMedia,
  deletePermanentMaterial,
  listPermanentMaterial,
  getPermanentMaterial,
  getMaterialCount,
  type TemporaryMediaType,
  type PermanentMediaType,
} from "../api/material.js";
import {
  ACCOUNT_ID_SCHEMA_PROPERTY,
  asErrorMessage,
  buildErrorResult,
  buildToolResult,
  assertAuthorized,
  resolveToolAccount,
  type ToolContext,
} from "./shared.js";

const parameters = {
  type: "object",
  additionalProperties: false,
  required: ["action"],
  properties: {
    accountId: ACCOUNT_ID_SCHEMA_PROPERTY,
    action: {
      type: "string",
      enum: [
        "upload_temp",
        "upload_permanent_image",
        "upload_permanent",
        "delete_permanent",
        "list_permanent",
        "get_permanent",
        "count_permanent",
      ],
      description:
        "upload_temp=上传临时素材（3天有效，回 media_id）；upload_permanent_image=图文正文内图片（回 url，不占永久素材数）；upload_permanent=永久素材（回 media_id）；delete/list/get/count=永久素材管理。",
    },
    type: {
      type: "string",
      enum: ["image", "voice", "video", "thumb"],
      description: "素材类型。upload_temp / upload_permanent 必填；list_permanent 必填。",
    },
    filePath: { type: "string", description: "本地文件路径（优先）。" },
    url: { type: "string", description: "远程文件 URL（filePath 未给时用）。" },
    base64: { type: "string", description: "Base64 编码内容（filePath/url 都没有时用）。" },
    filename: { type: "string", description: "文件名（不提供则从 url/filePath 推断）。" },
    contentType: { type: "string", description: "MIME（不提供则按扩展名推断）。" },
    videoTitle: { type: "string", description: "upload_permanent type=video 必填。" },
    videoIntroduction: { type: "string", description: "upload_permanent type=video 必填。" },
    mediaId: { type: "string", description: "delete_permanent / get_permanent 用。" },
    offset: { type: "number", description: "list_permanent 分页偏移，默认 0。" },
    count: { type: "number", description: "list_permanent 每页条数，默认 20，最大 20。" },
  },
} as const;

async function loadFileBuffer(input: {
  filePath?: string;
  url?: string;
  base64?: string;
}): Promise<{ buffer: Buffer; filename: string; contentType?: string }> {
  if (input.filePath) {
    const buffer = await fs.readFile(input.filePath);
    const filename = input.filePath.split("/").pop() || "upload.bin";
    return { buffer, filename };
  }
  if (input.url) {
    const res = await undiciFetch(input.url);
    if (!res.ok) {
      throw new Error(`[wechat-service] download ${input.url} failed: ${res.status}`);
    }
    const buf = Buffer.from(await res.arrayBuffer());
    const contentType = res.headers.get("content-type") ?? undefined;
    const filename = new URL(input.url).pathname.split("/").pop() || "download.bin";
    return { buffer: buf, filename, contentType };
  }
  if (input.base64) {
    const buffer = Buffer.from(input.base64, "base64");
    return { buffer, filename: "upload.bin" };
  }
  throw new Error("must provide one of filePath / url / base64");
}

export function registerMaterialTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_material",
      label: "WeChat Service Material",
      description:
        "微信服务号素材管理：上传临时/永久素材（图片/语音/视频/缩略图），图文正文内图片上传（返回可直接嵌入的 URL），永久素材列表/详情/删除。",
      parameters,
      async execute(_toolCallId: string, params: Record<string, unknown>) {
        try {
          const { account, tokenHandle } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId as string | undefined,
          });
          const action = String(params.action ?? "");
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_material",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "upload_temp": {
              const type = String(params.type ?? "") as TemporaryMediaType;
              if (!type) throw new Error("type required for action=upload_temp");
              const { buffer, filename, contentType } = await loadFileBuffer({
                filePath: params.filePath as string | undefined,
                url: params.url as string | undefined,
                base64: params.base64 as string | undefined,
              });
              const result = await uploadTemporaryMedia({
                account,
                tokenHandle,
                type,
                buffer,
                filename: (params.filename as string | undefined) ?? filename,
                contentType: (params.contentType as string | undefined) ?? contentType,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                mediaId: result.mediaId,
                type: result.type,
                createdAt: result.createdAt,
                summary: `临时素材已上传（media_id: ${result.mediaId}，3 天有效）`,
              });
            }
            case "upload_permanent_image": {
              const { buffer, filename, contentType } = await loadFileBuffer({
                filePath: params.filePath as string | undefined,
                url: params.url as string | undefined,
                base64: params.base64 as string | undefined,
              });
              const result = await uploadPermanentImage({
                account,
                tokenHandle,
                buffer,
                filename: (params.filename as string | undefined) ?? filename,
                contentType: (params.contentType as string | undefined) ?? contentType,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                url: result.url,
                summary: "图文正文内嵌图片已上传（返回可直接嵌入的 url）",
              });
            }
            case "upload_permanent": {
              const type = String(params.type ?? "") as PermanentMediaType;
              if (!type) throw new Error("type required for action=upload_permanent");
              const { buffer, filename, contentType } = await loadFileBuffer({
                filePath: params.filePath as string | undefined,
                url: params.url as string | undefined,
                base64: params.base64 as string | undefined,
              });
              const videoDescription =
                type === "video"
                  ? {
                      title: (params.videoTitle as string | undefined) ?? "",
                      introduction: (params.videoIntroduction as string | undefined) ?? "",
                    }
                  : undefined;
              if (type === "video" && (!videoDescription?.title || !videoDescription?.introduction)) {
                throw new Error("videoTitle + videoIntroduction required for type=video");
              }
              const result = await uploadPermanentMedia({
                account,
                tokenHandle,
                type,
                buffer,
                filename: (params.filename as string | undefined) ?? filename,
                contentType: (params.contentType as string | undefined) ?? contentType,
                videoDescription,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                mediaId: result.mediaId,
                url: result.url,
                summary: `永久素材已上传（media_id: ${result.mediaId}）`,
              });
            }
            case "delete_permanent": {
              const mediaId = requireStr(params.mediaId, "mediaId");
              await deletePermanentMaterial({ account, tokenHandle, mediaId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `永久素材 ${mediaId} 已删除`,
              });
            }
            case "list_permanent": {
              const type = String(params.type ?? "") as PermanentMediaType;
              if (!type) throw new Error("type required for action=list_permanent");
              const result = await listPermanentMaterial({
                account,
                tokenHandle,
                type,
                offset: params.offset as number | undefined,
                count: params.count as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                totalCount: result.totalCount,
                itemCount: result.itemCount,
                items: result.item,
                summary: `永久素材列表已获取（type=${type}，共 ${result.itemCount ?? 0} 条）`,
              });
            }
            case "get_permanent": {
              const mediaId = requireStr(params.mediaId, "mediaId");
              const result = await getPermanentMaterial({ account, tokenHandle, mediaId });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `永久素材 ${mediaId} 详情已获取`,
                raw: result,
              });
            }
            case "count_permanent": {
              const result = await getMaterialCount({ account, tokenHandle });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: "永久素材总数已获取",
                raw: result,
              });
            }
            default:
              throw new Error(`Unsupported action: ${action}`);
          }
        } catch (err) {
          return buildErrorResult({ action: String(params?.action), error: asErrorMessage(err) });
        }
      },
    };
  });
}

function requireStr(value: unknown, name: string): string {
  const str = typeof value === "string" ? value.trim() : "";
  if (!str) throw new Error(`${name} required`);
  return str;
}
