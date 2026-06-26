/**
 * **订阅通知（长期订阅消息）API**
 *
 * 服务号"订阅通知"是 2020 年新版（区别于老的"模板消息"）：
 *  - 用户在前端先调起"订阅"弹窗（JS-SDK 或小程序 wx.requestSubscribeMessage）
 *  - 后端再下发通知（不限次数，但每次需要前端授权一条）
 *  - 模板从"公共模板库"选用（getCategory → pubTemplateTitles → addTemplate）
 *
 * 与"一次性订阅消息"（`message/template/subscribe` 端点）不同，订阅通知
 * 走 `/wxaapi/newtmpl/...` 端点 + `cgi-bin/message/subscribe/bizsend`。
 *
 * 官方文档：
 *   https://developers.weixin.qq.com/doc/offiaccount/Subscription_Messages/intro.html
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type SubscribeTemplateData = Record<string, { value: string; color?: string }>;

/**
 * 获取公众号所属类目（订阅通知申请前置）
 */
export async function getSubscribeCategory(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<{ list: Array<{ id: number; name: string }> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ data?: Array<{ id: number; name: string }> }>({
    method: "GET",
    endpoint: "wxaapi/newtmpl/getcategory",
    query: { access_token: accessToken },
    network: params.account.network,
  });
  return { list: data.data ?? [] };
}

/**
 * 浏览公模板库（按类目）—— 找到适合的模板再 addTemplate 选用
 */
export async function getSubscribePubTemplateTitles(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 类目 id，逗号分隔字符串 */
  ids: string;
  /** 起始位置 0-based */
  start?: number;
  /** 一次拉取数量，最大 30 */
  limit?: number;
}): Promise<{ count: number; list: Array<Record<string, unknown>> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ count?: number; data?: Array<Record<string, unknown>> }>({
    method: "GET",
    endpoint: "wxaapi/newtmpl/getpubtemplatetitles",
    query: {
      access_token: accessToken,
      ids: params.ids,
      start: params.start ?? 0,
      limit: Math.min(params.limit ?? 30, 30),
    },
    network: params.account.network,
  });
  return { count: Number(data.count ?? 0), list: data.data ?? [] };
}

/**
 * 查模板的关键词列表（用于 addTemplate 选项）
 */
export async function getSubscribePubTemplateKeywords(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 公模板库 tid */
  tid: string;
}): Promise<{ count: number; list: Array<Record<string, unknown>> }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ count?: number; data?: Array<Record<string, unknown>> }>({
    method: "GET",
    endpoint: "wxaapi/newtmpl/getpubtemplatekeywords",
    query: { access_token: accessToken, tid: params.tid },
    network: params.account.network,
  });
  return { count: Number(data.count ?? 0), list: data.data ?? [] };
}

/**
 * 选用订阅通知模板（公模板 → 自己的模板列表）
 *
 * @returns 新模板的 priTmplId（个人模板 id），用于 sendSubscribeMessage
 */
export async function addSubscribeTemplate(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 公模板 tid */
  tid: string;
  /** 选用的关键词 id 列表（来自 getSubscribePubTemplateKeywords） */
  kidList: number[];
  /** 业务场景描述（最多 15 字） */
  sceneDesc?: string;
}): Promise<{ priTmplId: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ priTmplId?: string }>({
    method: "POST",
    endpoint: "wxaapi/newtmpl/addtemplate",
    query: { access_token: accessToken },
    body: {
      tid: params.tid,
      kidList: params.kidList,
      ...(params.sceneDesc ? { sceneDesc: params.sceneDesc } : {}),
    },
    network: params.account.network,
  });
  return { priTmplId: String(data.priTmplId ?? "") };
}

/**
 * 删除订阅通知模板
 */
export async function deleteSubscribeTemplate(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  /** 个人模板 id */
  priTmplId: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "wxaapi/newtmpl/deltemplate",
    query: { access_token: accessToken },
    body: { priTmplId: params.priTmplId },
    network: params.account.network,
  });
}

/**
 * 获取已选用的订阅通知模板列表
 */
export async function listSubscribeTemplates(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<Array<Record<string, unknown>>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ data?: Array<Record<string, unknown>> }>({
    method: "GET",
    endpoint: "wxaapi/newtmpl/gettemplate",
    query: { access_token: accessToken },
    network: params.account.network,
  });
  return data.data ?? [];
}

/**
 * **发送订阅通知（长期订阅消息）**
 *
 * 与"一次性订阅消息"区别：用户已订阅过该模板（前端 wx.requestSubscribeMessage
 * 或 JS-SDK），后端可在用户授权次数额度内发送，不需要 scene/title。
 *
 * 端点: `cgi-bin/message/subscribe/bizsend`
 */
export async function sendSubscribeMessage(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  touser: string;
  /** 个人模板 id（priTmplId） */
  templateId: string;
  /** 跳转页面（可选） */
  page?: string;
  /** 跳转小程序（可选） */
  miniprogram?: { appid: string; pagepath: string };
  /** 模板内容（key 与模板字段对齐） */
  data: SubscribeTemplateData;
}): Promise<{ msgid?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<{ msgid?: number }>({
    method: "POST",
    endpoint: "cgi-bin/message/subscribe/bizsend",
    query: { access_token: accessToken },
    body: {
      touser: params.touser,
      template_id: params.templateId,
      ...(params.page ? { page: params.page } : {}),
      ...(params.miniprogram ? { miniprogram: params.miniprogram } : {}),
      data: params.data,
    },
    network: params.account.network,
  });
}
