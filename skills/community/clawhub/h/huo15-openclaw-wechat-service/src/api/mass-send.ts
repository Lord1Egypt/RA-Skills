/**
 * 群发（高级接口）API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Batch_Sends_and_Originality_Checks.html
 *
 * 支持按标签群发 + 按 openid 列表群发，内容类型 text / image / voice / mpvideo / mpnews / wxcard。
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type MassSendContent =
  | { type: "mpnews"; media_id: string }
  | { type: "text"; content: string }
  | { type: "voice"; media_id: string }
  | { type: "image"; media_ids: string[] | { media_ids: string[]; recommend?: string; need_open_comment?: 0 | 1; only_fans_can_comment?: 0 | 1 } }
  | { type: "mpvideo"; media_id: string }
  | { type: "wxcard"; card_id: string };

function buildMsgPayload(content: MassSendContent): Record<string, unknown> {
  switch (content.type) {
    case "text":
      return { text: { content: content.content }, msgtype: "text" };
    case "image":
      return {
        images: Array.isArray(content.media_ids)
          ? { media_ids: content.media_ids }
          : content.media_ids,
        msgtype: "image",
      };
    case "voice":
      return { voice: { media_id: content.media_id }, msgtype: "voice" };
    case "mpnews":
      return { mpnews: { media_id: content.media_id }, msgtype: "mpnews" };
    case "mpvideo":
      return { mpvideo: { media_id: content.media_id }, msgtype: "mpvideo" };
    case "wxcard":
      return { wxcard: { card_id: content.card_id }, msgtype: "wxcard" };
  }
}

export async function massSendByTag(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  is_to_all?: boolean;
  tag_id?: number;
  content: MassSendContent;
  send_ignore_reprint?: 0 | 1;
}): Promise<{ msg_id?: number; msg_data_id?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const payload = {
    filter: {
      is_to_all: params.is_to_all ?? false,
      tag_id: params.tag_id,
    },
    ...buildMsgPayload(params.content),
    send_ignore_reprint: params.send_ignore_reprint ?? 0,
  };
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/sendall",
    query: { access_token: accessToken },
    body: payload,
    network: params.account.network,
  });
}

export async function massSendByOpenids(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  touser: string[];
  content: MassSendContent;
  send_ignore_reprint?: 0 | 1;
}): Promise<{ msg_id?: number; msg_data_id?: number }> {
  if (params.touser.length < 2) {
    throw new Error("[wechat-service] mass send by openid requires at least 2 users");
  }
  const accessToken = await params.tokenHandle.getAccessToken();
  const payload = {
    touser: params.touser,
    ...buildMsgPayload(params.content),
    send_ignore_reprint: params.send_ignore_reprint ?? 0,
  };
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/send",
    query: { access_token: accessToken },
    body: payload,
    network: params.account.network,
  });
}

export async function massSendPreview(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  touser?: string;
  towxname?: string;
  content: MassSendContent;
}): Promise<{ msg_id?: number }> {
  if (!params.touser && !params.towxname) {
    throw new Error("[wechat-service] mass preview requires touser or towxname");
  }
  const accessToken = await params.tokenHandle.getAccessToken();
  const payload: Record<string, unknown> = {
    ...buildMsgPayload(params.content),
  };
  if (params.touser) payload.touser = params.touser;
  if (params.towxname) payload.towxname = params.towxname;
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/preview",
    query: { access_token: accessToken },
    body: payload,
    network: params.account.network,
  });
}

export async function massSendDelete(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  msg_id: number;
  article_idx?: number;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/delete",
    query: { access_token: accessToken },
    body: { msg_id: params.msg_id, article_idx: params.article_idx ?? 0 },
    network: params.account.network,
  });
}

export async function massSendStatus(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  msg_id: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/get",
    query: { access_token: accessToken },
    body: { msg_id: params.msg_id },
    network: params.account.network,
  });
}

/**
 * 设置群发速度（0=80w/min, 1=60w/min, 2=45w/min, 3=30w/min, 4=10w/min）
 */
export async function setMassSendSpeed(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  speed: 0 | 1 | 2 | 3 | 4;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/speed/set",
    query: { access_token: accessToken },
    body: { speed: params.speed },
    network: params.account.network,
  });
}

export async function getMassSendSpeed(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<{ speed?: number; realspeed?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/mass/speed/get",
    query: { access_token: accessToken },
    body: {},
    network: params.account.network,
  });
}
