/**
 * 模板消息 / 一次性订阅消息 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html
 *
 * 服务号可以给关注用户发模板消息（需要先申请模板）。
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type TemplateDataEntry = {
  value: string;
  color?: string;
};

export type TemplateMessagePayload = {
  touser: string;
  template_id: string;
  url?: string;
  miniprogram?: {
    appid: string;
    pagepath: string;
  };
  data: Record<string, TemplateDataEntry>;
  client_msg_id?: string;
};

export async function sendTemplateMessage(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  message: TemplateMessagePayload;
}): Promise<{ msgid: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ msgid?: number }>({
    method: "POST",
    endpoint: "cgi-bin/message/template/send",
    query: { access_token: accessToken },
    body: params.message,
    network: params.account.network,
  });
  return { msgid: Number(data.msgid ?? 0) };
}

export async function listTemplates(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<Array<Record<string, unknown>>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ template_list?: Array<Record<string, unknown>> }>({
    method: "GET",
    endpoint: "cgi-bin/template/get_all_private_template",
    query: { access_token: accessToken },
    network: params.account.network,
  });
  return data.template_list ?? [];
}

export async function deleteTemplate(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  templateId: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/template/del_private_template",
    query: { access_token: accessToken },
    body: { template_id: params.templateId },
    network: params.account.network,
  });
}

/**
 * 设置所属行业（模板消息前置要求，年度 2 次上限）
 */
export async function setIndustry(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  industry_id1: string;
  industry_id2?: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/template/api_set_industry",
    query: { access_token: accessToken },
    body: { industry_id1: params.industry_id1, industry_id2: params.industry_id2 },
    network: params.account.network,
  });
}

export async function getIndustry(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "GET",
    endpoint: "cgi-bin/template/get_industry",
    query: { access_token: accessToken },
    network: params.account.network,
  });
}

/**
 * 一次性订阅消息（subscribe.go → onetime）
 */
export async function sendSubscribeOnceMessage(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  touser: string;
  template_id: string;
  scene: string;
  title: string;
  data: Record<string, { value: string; color?: string }>;
  url?: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/template/subscribe",
    query: { access_token: accessToken },
    body: {
      touser: params.touser,
      template_id: params.template_id,
      scene: params.scene,
      title: params.title,
      url: params.url,
      data: params.data,
    },
    network: params.account.network,
  });
}

/**
 * 选用模板（从模板库添加到自己的模板列表）
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Template_Message_Interface.html#0
 *
 * @returns 新模板的 template_id
 */
export async function addTemplate(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 模板库中模板的编号，例 TM00015 */
  templateIdShort: string;
  /** 选用的关键词 id 列表（顺序与模板要求一致）。模板库 v2 起允许配 keyword_id_list */
  keywordIdList?: number[];
}): Promise<{ templateId: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ template_id?: string }>({
    method: "POST",
    endpoint: "cgi-bin/template/api_add_template",
    query: { access_token: accessToken },
    body: {
      template_id_short: params.templateIdShort,
      ...(params.keywordIdList ? { keyword_id_list: params.keywordIdList } : {}),
    },
    network: params.account.network,
  });
  return { templateId: String(data.template_id ?? "") };
}

/**
 * 获取公模板库标题列表
 *
 * 用于浏览公模板库，再用 `getTemplateLibraryById` 拉详情、`addTemplate` 选用。
 */
export async function getTemplateLibraryList(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 起始位置，0-based */
  offset?: number;
  /** 拉取数量，最大 20 */
  count?: number;
}): Promise<{ totalCount: number; list: Array<Record<string, unknown>> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ total_count?: number; list?: Array<Record<string, unknown>> }>({
    method: "POST",
    endpoint: "cgi-bin/template/get_template_library_list",
    query: { access_token: accessToken },
    body: {
      offset: params.offset ?? 0,
      count: Math.min(params.count ?? 20, 20),
    },
    network: params.account.network,
  });
  return {
    totalCount: Number(data.total_count ?? 0),
    list: data.list ?? [],
  };
}

/**
 * 获取公模板库单条详情（含关键词列表）
 */
export async function getTemplateLibraryById(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 模板库编号，例 TM00015 */
  id: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/template/get_template_library_by_id",
    query: { access_token: accessToken },
    body: { id: params.id },
    network: params.account.network,
  });
}
