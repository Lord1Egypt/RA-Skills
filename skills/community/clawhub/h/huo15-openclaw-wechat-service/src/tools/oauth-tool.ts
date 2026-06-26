/**
 * 网页授权 OAuth2 agent tool。
 *
 * actions:
 *   build_authorize_url  —— 同步：构造授权跳转 URL
 *   code_to_token        —— 用 code 换网页授权 access_token + openid
 *   refresh_token        —— 刷新网页授权 access_token
 *   userinfo             —— 拉用户信息（仅 snsapi_userinfo scope）
 *   validate             —— 校验网页授权 access_token 是否有效
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

import {
  buildOAuthAuthorizeUrl,
  oauthCodeToAccessToken,
  oauthRefreshToken,
  oauthGetUserInfo,
  oauthValidateAccessToken,
} from "../api/oauth.js";
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
      enum: ["build_authorize_url", "code_to_token", "refresh_token", "userinfo", "validate"],
      description: "OAuth 网页授权动作。",
    },
    redirectUri: {
      type: "string",
      description: "build_authorize_url 用：用户同意后跳回的 URL（必须是公众号后台已配置的授权域名）。",
    },
    scope: {
      type: "string",
      enum: ["snsapi_base", "snsapi_userinfo"],
      description:
        "build_authorize_url 用：snsapi_base 静默授权只能拿 openid；snsapi_userinfo 弹确认页可拿用户信息+unionid。",
    },
    state: {
      type: "string",
      description: "build_authorize_url 可选：业务侧 csrf / 上下文标记，回调原样回传（≤128 字节）。",
    },
    code: { type: "string", description: "code_to_token 用：微信回调 URL 上带的 code（5min 内有效）。" },
    refreshToken: {
      type: "string",
      description: "refresh_token 用：上次拿到的 refresh_token（30 天有效）。",
    },
    webAccessToken: {
      type: "string",
      description: "userinfo / validate 用：网页授权 access_token（不是普通 cgi-bin/token）。",
    },
    openid: {
      type: "string",
      description: "userinfo / validate 用：用户 openid。",
    },
    lang: {
      type: "string",
      enum: ["zh_CN", "zh_TW", "en"],
      description: "userinfo 可选：返回语言，默认 zh_CN。",
    },
  },
} as const;

export function registerOAuthTool(api: OpenClawPluginApi): void {
  if (typeof api?.registerTool !== "function") return;
  api.registerTool((toolContext: unknown) => {
    return {
      name: "wechat_service_oauth",
      label: "WeChat Service OAuth",
      description:
        "微信公众号网页授权 OAuth2.0：构造授权 URL、code 换 token、刷新 token、拉用户信息、校验 token 有效性。snsapi_base 静默授权（openid）/ snsapi_userinfo 弹确认页（含 unionid + 用户资料）。",
      parameters,
      async execute(_toolCallId: string, params: Record<string, unknown>) {
        try {
          const { account } = resolveToolAccount({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            explicitAccountId: params.accountId as string | undefined,
          });
          const action = String(params.action ?? "");
          const denied = assertAuthorized({
            ctx: toolContext as ToolContext,
            apiConfig: api.config,
            toolName: "wechat_service_oauth",
            action,
            accountId: account.accountId,
          });
          if (denied) return denied;

          switch (action) {
            case "build_authorize_url": {
              const redirectUri = requireStr(params.redirectUri, "redirectUri");
              const scope = String(params.scope ?? "snsapi_base") as "snsapi_base" | "snsapi_userinfo";
              if (scope !== "snsapi_base" && scope !== "snsapi_userinfo") {
                throw new Error("scope must be 'snsapi_base' or 'snsapi_userinfo'");
              }
              const url = buildOAuthAuthorizeUrl({
                account,
                redirectUri,
                scope,
                state: params.state as string | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                authorizeUrl: url,
                summary: `授权 URL 已生成（scope=${scope}）`,
              });
            }
            case "code_to_token": {
              const code = requireStr(params.code, "code");
              const result = await oauthCodeToAccessToken({ account, code });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                openid: result.openid,
                accessToken: result.access_token,
                refreshToken: result.refresh_token,
                expiresIn: result.expires_in,
                scope: result.scope,
                unionid: result.unionid,
                summary: `code 已换取 access_token（openid=${result.openid}, scope=${result.scope}）`,
              });
            }
            case "refresh_token": {
              const refreshToken = requireStr(params.refreshToken, "refreshToken");
              const result = await oauthRefreshToken({ account, refreshToken });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                openid: result.openid,
                accessToken: result.access_token,
                refreshToken: result.refresh_token,
                expiresIn: result.expires_in,
                scope: result.scope,
                summary: `access_token 已刷新（openid=${result.openid}）`,
              });
            }
            case "userinfo": {
              const webAccessToken = requireStr(params.webAccessToken, "webAccessToken");
              const openid = requireStr(params.openid, "openid");
              const info = await oauthGetUserInfo({
                account,
                webAccessToken,
                openid,
                lang: params.lang as "zh_CN" | "zh_TW" | "en" | undefined,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                userInfo: info,
                summary: `用户信息已获取（${info.nickname || info.openid}）`,
              });
            }
            case "validate": {
              const webAccessToken = requireStr(params.webAccessToken, "webAccessToken");
              const openid = requireStr(params.openid, "openid");
              const result = await oauthValidateAccessToken({
                account,
                webAccessToken,
                openid,
              });
              return buildToolResult({
                ok: true,
                action,
                accountId: account.accountId,
                valid: result.valid,
                summary: result.valid ? "access_token 有效" : "access_token 已失效或不匹配 openid",
                raw: result.raw,
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
