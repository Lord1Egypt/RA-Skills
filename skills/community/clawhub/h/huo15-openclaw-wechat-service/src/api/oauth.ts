/**
 * **网页授权 OAuth2.0 API**
 *
 * 公众号用户在网页/H5 里授权后获取 openid 和（snsapi_userinfo scope 时）用户信息。
 * 与"普通 access_token（cgi-bin/token）"不同：OAuth 流程产生 **网页授权 access_token**，
 * 用 appid + secret 直连 sns 端点，不经过 access_token manager。
 *
 * 完整流程：
 *  1. 前端跳转 buildOAuthAuthorizeUrl() 生成的 URL → 用户同意 → 跳回 redirectUri 带 code
 *  2. 后端 oauthCodeToAccessToken(code) → 拿到 { access_token, openid, refresh_token, scope, ... }
 *  3. 如果 scope 是 snsapi_userinfo → oauthGetUserInfo(access_token, openid)
 *  4. token 60min 过期前用 oauthRefreshToken(refresh_token) 刷新（refresh_token 30 天有效）
 *  5. 任何时刻可用 oauthValidateAccessToken 校验有效性
 *
 * 官方文档：
 *   https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html
 */

import { jsonRequest } from "../http-client.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type OAuthScope = "snsapi_base" | "snsapi_userinfo";
export type OAuthLang = "zh_CN" | "zh_TW" | "en";

const OAUTH_AUTHORIZE_BASE = "https://open.weixin.qq.com/connect/oauth2/authorize";

/**
 * 构造网页授权跳转 URL（同步，不发 HTTP 请求）。
 *
 * @param scope 'snsapi_base'（静默授权，只能拿 openid）/ 'snsapi_userinfo'（弹出确认页，可拿 unionid + 用户信息）
 * @param state 业务侧 csrf / 上下文标记，回调时原样回传（≤128 字节）
 */
export function buildOAuthAuthorizeUrl(params: {
  account: ResolvedWechatServiceAccount;
  redirectUri: string;
  scope: OAuthScope;
  state?: string;
}): string {
  const u = new URL(OAUTH_AUTHORIZE_BASE);
  u.searchParams.set("appid", params.account.appId);
  u.searchParams.set("redirect_uri", params.redirectUri);
  u.searchParams.set("response_type", "code");
  u.searchParams.set("scope", params.scope);
  if (params.state) u.searchParams.set("state", params.state);
  // 微信侧要求 hash fragment 必须是 #wechat_redirect
  return `${u.toString()}#wechat_redirect`;
}

export type OAuthAccessToken = {
  access_token: string;
  expires_in: number;
  refresh_token: string;
  openid: string;
  scope: OAuthScope | string;
  unionid?: string;
};

/**
 * 用 code 换网页授权 access_token（含 openid）
 */
export async function oauthCodeToAccessToken(params: {
  account: ResolvedWechatServiceAccount;
  code: string;
}): Promise<OAuthAccessToken> {
  return jsonRequest<OAuthAccessToken & Record<string, unknown>>({
    method: "GET",
    endpoint: "sns/oauth2/access_token",
    query: {
      appid: params.account.appId,
      secret: params.account.appSecret,
      code: params.code,
      grant_type: "authorization_code",
    },
    network: params.account.network,
  }) as Promise<OAuthAccessToken>;
}

/**
 * 刷新网页授权 access_token（refresh_token 30 天有效）
 */
export async function oauthRefreshToken(params: {
  account: ResolvedWechatServiceAccount;
  refreshToken: string;
}): Promise<OAuthAccessToken> {
  return jsonRequest<OAuthAccessToken & Record<string, unknown>>({
    method: "GET",
    endpoint: "sns/oauth2/refresh_token",
    query: {
      appid: params.account.appId,
      grant_type: "refresh_token",
      refresh_token: params.refreshToken,
    },
    network: params.account.network,
  }) as Promise<OAuthAccessToken>;
}

export type OAuthUserInfo = {
  openid: string;
  nickname: string;
  sex: number;
  province: string;
  city: string;
  country: string;
  headimgurl: string;
  privilege: string[];
  unionid?: string;
};

/**
 * 拉用户信息（仅 snsapi_userinfo scope 可用）
 */
export async function oauthGetUserInfo(params: {
  account: ResolvedWechatServiceAccount;
  /** 网页授权 access_token（来自 oauthCodeToAccessToken / oauthRefreshToken） */
  webAccessToken: string;
  openid: string;
  lang?: OAuthLang;
}): Promise<OAuthUserInfo> {
  return jsonRequest<OAuthUserInfo & Record<string, unknown>>({
    method: "GET",
    endpoint: "sns/userinfo",
    query: {
      access_token: params.webAccessToken,
      openid: params.openid,
      lang: params.lang ?? "zh_CN",
    },
    network: params.account.network,
  }) as Promise<OAuthUserInfo>;
}

/**
 * 校验网页授权 access_token 是否有效
 */
export async function oauthValidateAccessToken(params: {
  account: ResolvedWechatServiceAccount;
  webAccessToken: string;
  openid: string;
}): Promise<{ valid: boolean; raw: Record<string, unknown> }> {
  // sns/auth 在 token 失效时返回非 0 errcode；jsonRequest 会抛 WechatApiError。
  // 这里捕获并归一为 valid:false 而不抛错（业务侧只关心布尔）。
  try {
    const data = await jsonRequest<Record<string, unknown>>({
      method: "GET",
      endpoint: "sns/auth",
      query: {
        access_token: params.webAccessToken,
        openid: params.openid,
      },
      network: params.account.network,
    });
    return { valid: true, raw: data };
  } catch (err) {
    return { valid: false, raw: { error: err instanceof Error ? err.message : String(err) } };
  }
}
