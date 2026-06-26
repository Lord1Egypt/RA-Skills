/**
 * 带参数二维码 + 短链 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Generating_a_Parametric_QR_Code.html
 *
 * 两类二维码：
 *  - 临时：30 天内有效，scene_id 整数或 scene_str 字符串
 *  - 永久：永久有效，scene_id ≤ 100000 或 scene_str
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type QrcodeCreateParams =
  | {
      mode: "temp_id";
      scene_id: number;
      expire_seconds?: number;
    }
  | {
      mode: "temp_str";
      scene_str: string;
      expire_seconds?: number;
    }
  | {
      mode: "perm_id";
      scene_id: number;
    }
  | {
      mode: "perm_str";
      scene_str: string;
    };

export type QrcodeCreateResult = {
  ticket: string;
  expire_seconds?: number;
  url: string;
  /** https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=xxx */
  showQrcodeUrl: string;
};

export async function createQrcode(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  request: QrcodeCreateParams;
}): Promise<QrcodeCreateResult> {
  const accessToken = await params.tokenHandle.getAccessToken();
  let body: Record<string, unknown>;
  switch (params.request.mode) {
    case "temp_id":
      body = {
        expire_seconds: params.request.expire_seconds ?? 604800,
        action_name: "QR_SCENE",
        action_info: { scene: { scene_id: params.request.scene_id } },
      };
      break;
    case "temp_str":
      body = {
        expire_seconds: params.request.expire_seconds ?? 604800,
        action_name: "QR_STR_SCENE",
        action_info: { scene: { scene_str: params.request.scene_str } },
      };
      break;
    case "perm_id":
      body = {
        action_name: "QR_LIMIT_SCENE",
        action_info: { scene: { scene_id: params.request.scene_id } },
      };
      break;
    case "perm_str":
      body = {
        action_name: "QR_LIMIT_STR_SCENE",
        action_info: { scene: { scene_str: params.request.scene_str } },
      };
      break;
    default:
      throw new Error("[wechat-service] qrcode/create unsupported mode");
  }
  const data = await jsonRequest<{
    ticket?: string;
    expire_seconds?: number;
    url?: string;
  }>({
    method: "POST",
    endpoint: "cgi-bin/qrcode/create",
    query: { access_token: accessToken },
    body,
    network: params.account.network,
  });
  if (!data.ticket) {
    throw new Error("[wechat-service] qrcode/create missing ticket");
  }
  const ticket = data.ticket;
  return {
    ticket,
    expire_seconds: data.expire_seconds,
    url: data.url ?? "",
    showQrcodeUrl: `https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=${encodeURIComponent(ticket)}`,
  };
}

/**
 * 长链接转短 key（替代已下线的 shorturl）
 */
export async function genShortKey(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  long_data: string;
  expire_seconds?: number;
}): Promise<{ short_key: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ short_key?: string }>({
    method: "POST",
    endpoint: "cgi-bin/shorten/gen",
    query: { access_token: accessToken },
    body: {
      long_data: params.long_data,
      expire_seconds: params.expire_seconds ?? 2592000,
    },
    network: params.account.network,
  });
  if (!data.short_key) throw new Error("[wechat-service] shorten/gen missing short_key");
  return { short_key: data.short_key };
}

export async function fetchShortKey(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  short_key: string;
}): Promise<{ long_data?: string; create_time?: number; expire_seconds?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/shorten/fetch",
    query: { access_token: accessToken },
    body: { short_key: params.short_key },
    network: params.account.network,
  });
}
