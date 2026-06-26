/**
 * 用户标签 + 用户管理 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/User_Management/User_Tag_Management.html
 *
 * - 每个公众号最多可创建 100 个标签
 * - 每个用户最多打 20 个标签
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type WechatUserTag = {
  id: number;
  name: string;
  count?: number;
};

export async function createUserTag(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  name: string;
}): Promise<WechatUserTag> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ tag?: WechatUserTag }>({
    method: "POST",
    endpoint: "cgi-bin/tags/create",
    query: { access_token: accessToken },
    body: { tag: { name: params.name } },
    network: params.account.network,
  });
  if (!data.tag) throw new Error("[wechat-service] tags/create missing tag");
  return data.tag;
}

export async function listUserTags(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<WechatUserTag[]> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ tags?: WechatUserTag[] }>({
    method: "GET",
    endpoint: "cgi-bin/tags/get",
    query: { access_token: accessToken },
    network: params.account.network,
  });
  return data.tags ?? [];
}

export async function updateUserTag(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  id: number;
  name: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/update",
    query: { access_token: accessToken },
    body: { tag: { id: params.id, name: params.name } },
    network: params.account.network,
  });
}

export async function deleteUserTag(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  id: number;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/delete",
    query: { access_token: accessToken },
    body: { tag: { id: params.id } },
    network: params.account.network,
  });
}

export async function listTagUsers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  tagid: number;
  next_openid?: string;
}): Promise<{ count?: number; data?: { openid?: string[] }; next_openid?: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<{ count?: number; data?: { openid?: string[] }; next_openid?: string }>({
    method: "POST",
    endpoint: "cgi-bin/user/tag/get",
    query: { access_token: accessToken },
    body: { tagid: params.tagid, next_openid: params.next_openid ?? "" },
    network: params.account.network,
  });
}

export async function batchTagUsers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid_list: string[];
  tagid: number;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/members/batchtagging",
    query: { access_token: accessToken },
    body: { openid_list: params.openid_list, tagid: params.tagid },
    network: params.account.network,
  });
}

export async function batchUntagUsers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid_list: string[];
  tagid: number;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/members/batchuntagging",
    query: { access_token: accessToken },
    body: { openid_list: params.openid_list, tagid: params.tagid },
    network: params.account.network,
  });
}

export async function getUserTagIds(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid: string;
}): Promise<number[]> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ tagid_list?: number[] }>({
    method: "POST",
    endpoint: "cgi-bin/tags/getidlist",
    query: { access_token: accessToken },
    body: { openid: params.openid },
    network: params.account.network,
  });
  return data.tagid_list ?? [];
}

/**
 * 设置 / 获取用户备注名
 */
export async function setUserRemark(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid: string;
  remark: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/user/info/updateremark",
    query: { access_token: accessToken },
    body: { openid: params.openid, remark: params.remark },
    network: params.account.network,
  });
}

/**
 * 拉黑 / 取消拉黑
 */
export async function blacklistUsers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid_list: string[];
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/members/batchblacklist",
    query: { access_token: accessToken },
    body: { openid_list: params.openid_list },
    network: params.account.network,
  });
}

export async function unblacklistUsers(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  openid_list: string[];
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/members/batchunblacklist",
    query: { access_token: accessToken },
    body: { openid_list: params.openid_list },
    network: params.account.network,
  });
}

export async function listBlacklist(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  begin_openid?: string;
}): Promise<{ total?: number; count?: number; data?: { openid?: string[] }; next_openid?: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/tags/members/getblacklist",
    query: { access_token: accessToken },
    body: { begin_openid: params.begin_openid ?? "" },
    network: params.account.network,
  });
}
