/**
 * 用户管理 / 粉丝信息 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/User_Management/Getting_a_User_Basic_Information.html
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type WechatUserInfo = {
  subscribe?: 0 | 1;
  openid: string;
  language?: string;
  subscribe_time?: number;
  unionid?: string;
  remark?: string;
  groupid?: number;
  tagid_list?: number[];
  subscribe_scene?: string;
  qr_scene?: number;
  qr_scene_str?: string;
};

export async function getUserInfo(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid: string;
  lang?: "zh_CN" | "zh_TW" | "en";
}): Promise<WechatUserInfo> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<WechatUserInfo>({
    method: "GET",
    endpoint: "cgi-bin/user/info",
    query: {
      access_token: accessToken,
      openid: params.openid,
      lang: params.lang ?? "zh_CN",
    },
    network: params.account.network,
  });
}

export async function batchGetUserInfo(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  user_list: Array<{ openid: string; lang?: "zh_CN" | "zh_TW" | "en" }>;
}): Promise<WechatUserInfo[]> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ user_info_list?: WechatUserInfo[] }>({
    method: "POST",
    endpoint: "cgi-bin/user/info/batchget",
    query: { access_token: accessToken },
    body: { user_list: params.user_list },
    network: params.account.network,
  });
  return data.user_info_list ?? [];
}

export async function listFollowers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  next_openid?: string;
}): Promise<{
  total?: number;
  count?: number;
  data?: { openid?: string[] };
  next_openid?: string;
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest({
    method: "GET",
    endpoint: "cgi-bin/user/get",
    query: {
      access_token: accessToken,
      next_openid: params.next_openid ?? "",
    },
    network: params.account.network,
  });
}
