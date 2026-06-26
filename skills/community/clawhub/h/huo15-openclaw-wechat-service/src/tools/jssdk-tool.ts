/**
 * JS-SDK 签名 agent tool：为前端 wx.config() 生成 signature。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import { signJsapi, getJsapiTicket, invalidateJsapiTicket } from "../api/jssdk.js";
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
      enum: ["sign", "get_ticket", "invalidate_ticket"],
      description: "sign=为给定 URL 生成 wx.config 所需 signature；get_ticket=获取 jsapi_ticket（不签名）；invalidate_ticket=手动失效。",
    },
    url: {
      type: "string",
      description: "sign 用：当前页面 URL（需带 query，不带 #fragment）。",
    },
    nonceStr: { type: "string", description: "sign 可选：自定义 nonceStr（不传则随机）。" },
    timestamp: { type: "number", description: "sign 可选：自定义时间戳（秒）。" },
    ticketType: {
      type: "string",
      enum: ["jsapi", "wx_card"],
      description: "get_ticket / invalidate_ticket 用，默认 jsapi。",
    },
  },
} as const;

export function registerJssdkTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_jssdk",
      label: "WeChat Service JS-SDK",
      description:
        "微信服务号 JS-SDK 签名：为前端页面 wx.config({appId, timestamp, nonceStr, signature}) 生成 signature，以启用 wx.uploadImage / wx.chooseImage / wx.scanQRCode 等网页侧 JSAPI。",
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
            toolName: "wechat_service_jssdk",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;
          switch (action) {
            case "sign": {
              const url = requireStr(params.url, "url");
              const result = await signJsapi({
                account,
                tokenHandle,
                url,
                nonceStr: params.nonceStr as string | undefined,
                timestamp: params.timestamp as number | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                appId: result.appId,
                timestamp: result.timestamp,
                nonceStr: result.nonceStr,
                signature: result.signature,
                url: result.url,
                summary: "JS-SDK 签名已生成",
              });
            }
            case "get_ticket": {
              const ticketType = (params.ticketType as "jsapi" | "wx_card" | undefined) ?? "jsapi";
              const entry = await getJsapiTicket({ account, tokenHandle, type: ticketType });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                ticket: entry.ticket,
                expiresAt: entry.expiresAt,
                summary: `jsapi_ticket（${ticketType}）已获取`,
              });
            }
            case "invalidate_ticket": {
              const ticketType = (params.ticketType as "jsapi" | "wx_card" | undefined) ?? "jsapi";
              invalidateJsapiTicket(account.accountId, ticketType);
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                summary: `jsapi_ticket（${ticketType}）已失效，下次调用将重新获取`,
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
