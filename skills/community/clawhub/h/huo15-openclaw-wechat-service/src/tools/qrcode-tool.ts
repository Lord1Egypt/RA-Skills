/**
 * 带参数二维码 + 短链 agent tool。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import { createQrcode, genShortKey, fetchShortKey, type QrcodeCreateParams } from "../api/qrcode.js";
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
      enum: ["create_qrcode", "shorten_gen", "shorten_fetch"],
      description: "create_qrcode=生成带参数二维码；shorten_*=长数据短 key（替代已下线 shorturl）。",
    },
    mode: {
      type: "string",
      enum: ["temp_id", "temp_str", "perm_id", "perm_str"],
      description: "二维码模式：temp_*=临时（可设 expire_seconds，最长 30 天），perm_*=永久（scene_id ≤ 100000 或 scene_str）。",
    },
    scene_id: { type: "number", description: "*_id 模式下的 scene_id。" },
    scene_str: { type: "string", description: "*_str 模式下的 scene_str（64 字符内）。" },
    expire_seconds: { type: "number", description: "temp_* 用：有效期秒数，默认 7 天，最大 2592000（30 天）。" },
    long_data: { type: "string", description: "shorten_gen 用：要缩短的原始数据（≤4KB）。" },
    short_key: { type: "string", description: "shorten_fetch 用：shorten_gen 返回的 short_key。" },
    shorten_expire_seconds: {
      type: "number",
      description: "shorten_gen 用：过期秒数，默认 2592000（30 天）。",
    },
  },
} as const;

export function registerQrcodeTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_qrcode",
      label: "WeChat Service QR Code",
      description:
        "微信服务号带参数二维码（临时/永久）+ 长链接到 short_key 的工具。生成的 showQrcodeUrl 可直接作为图片 src 展示或下载保存。",
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
            toolName: "wechat_service_qrcode",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "create_qrcode": {
              const mode = String(params.mode ?? "") as QrcodeCreateParams["mode"];
              let request: QrcodeCreateParams;
              switch (mode) {
                case "temp_id":
                  request = {
                    mode,
                    scene_id: requireNum(params.scene_id, "scene_id"),
                    expire_seconds: params.expire_seconds as number | undefined,
                  };
                  break;
                case "temp_str":
                  request = {
                    mode,
                    scene_str: requireStr(params.scene_str, "scene_str"),
                    expire_seconds: params.expire_seconds as number | undefined,
                  };
                  break;
                case "perm_id":
                  request = { mode, scene_id: requireNum(params.scene_id, "scene_id") };
                  break;
                case "perm_str":
                  request = { mode, scene_str: requireStr(params.scene_str, "scene_str") };
                  break;
                default:
                  throw new Error(`Unsupported mode: ${mode}`);
              }
              const result = await createQrcode({ account, tokenHandle, request });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                ticket: result.ticket,
                expire_seconds: result.expire_seconds,
                url: result.url,
                showQrcodeUrl: result.showQrcodeUrl,
                summary: `二维码已生成（${mode}），扫码时会触发对应的 subscribe/scan 事件`,
              });
            }
            case "shorten_gen": {
              const longData = requireStr(params.long_data, "long_data");
              const result = await genShortKey({
                account,
                tokenHandle,
                long_data: longData,
                expire_seconds: params.shorten_expire_seconds as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                short_key: result.short_key,
                summary: `short_key 已生成：${result.short_key}`,
              });
            }
            case "shorten_fetch": {
              const shortKey = requireStr(params.short_key, "short_key");
              const result = await fetchShortKey({ account, tokenHandle, short_key: shortKey });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `short_key ${shortKey} 已解出`,
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

function requireNum(value: unknown, name: string): number {
  if (typeof value !== "number" || !Number.isFinite(value)) {
    throw new Error(`${name} required (number)`);
  }
  return value;
}
