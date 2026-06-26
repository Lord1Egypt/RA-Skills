/**
 * 草稿箱 + 图文发布 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Publish/Add_draft.html
 *
 * 流程：
 *   1. 用 uploadPermanentImage（material.ts）拿图片 URL / thumb_media_id
 *   2. addDraft() 把文章 → 草稿箱，返回 media_id
 *   3. publishDraft(media_id) 异步发布
 *   4. getPublishStatus(publish_id) 轮询，直到 status == 0（发布成功）
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type WechatDraftArticle = {
  title: string;
  author?: string;
  digest?: string;
  content: string;
  content_source_url?: string;
  thumb_media_id: string;
  need_open_comment?: 0 | 1;
  only_fans_can_comment?: 0 | 1;
  /** 是否显示封面图 */
  show_cover_pic?: 0 | 1;
};

export async function addDraft(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  articles: WechatDraftArticle[];
}): Promise<{ media_id: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ media_id?: string }>({
    method: "POST",
    endpoint: "cgi-bin/draft/add",
    query: { access_token: accessToken },
    body: { articles: params.articles },
    network: params.account.network,
  });
  if (!data.media_id) {
    throw new Error("[wechat-service] draft/add missing media_id");
  }
  return { media_id: data.media_id };
}

export async function getDraft(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  media_id: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/draft/get",
    query: { access_token: accessToken },
    body: { media_id: params.media_id },
    network: params.account.network,
  });
}

export async function deleteDraft(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  media_id: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/draft/delete",
    query: { access_token: accessToken },
    body: { media_id: params.media_id },
    network: params.account.network,
  });
}

export async function updateDraft(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  media_id: string;
  index: number;
  articles: WechatDraftArticle;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/draft/update",
    query: { access_token: accessToken },
    body: {
      media_id: params.media_id,
      index: params.index,
      articles: params.articles,
    },
    network: params.account.network,
  });
}

export async function listDrafts(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  offset?: number;
  count?: number;
  no_content?: 0 | 1;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/draft/batchget",
    query: { access_token: accessToken },
    body: {
      offset: params.offset ?? 0,
      count: params.count ?? 20,
      no_content: params.no_content ?? 0,
    },
    network: params.account.network,
  });
}

export async function getDraftCount(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<{ total_count?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<{ total_count?: number }>({
    method: "GET",
    endpoint: "cgi-bin/draft/count",
    query: { access_token: accessToken },
    network: params.account.network,
  });
}

export async function publishDraft(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  media_id: string;
}): Promise<{ publish_id: string; msg_data_id?: number }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ publish_id?: string; msg_data_id?: number }>({
    method: "POST",
    endpoint: "cgi-bin/freepublish/submit",
    query: { access_token: accessToken },
    body: { media_id: params.media_id },
    network: params.account.network,
  });
  if (!data.publish_id) {
    throw new Error("[wechat-service] freepublish/submit missing publish_id");
  }
  return { publish_id: String(data.publish_id), msg_data_id: data.msg_data_id };
}

export async function getPublishStatus(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  publish_id: string;
}): Promise<{
  publish_id: string;
  publish_status: number;
  article_id?: string;
  article_detail?: { item: Array<{ idx: number; article_url: string }> };
  fail_idx?: number[];
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{
    publish_id?: string | number;
    publish_status?: number;
    article_id?: string;
    article_detail?: { item: Array<{ idx: number; article_url: string }> };
    fail_idx?: number[];
  }>({
    method: "POST",
    endpoint: "cgi-bin/freepublish/get",
    query: { access_token: accessToken },
    body: { publish_id: params.publish_id },
    network: params.account.network,
  });
  return {
    publish_id: String(data.publish_id ?? params.publish_id),
    publish_status: Number(data.publish_status ?? -1),
    article_id: data.article_id,
    article_detail: data.article_detail,
    fail_idx: data.fail_idx,
  };
}

export async function getPublishedArticle(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  article_id: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/freepublish/getarticle",
    query: { access_token: accessToken },
    body: { article_id: params.article_id },
    network: params.account.network,
  });
}

export async function listPublished(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  offset?: number;
  count?: number;
  no_content?: 0 | 1;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/freepublish/batchget",
    query: { access_token: accessToken },
    body: {
      offset: params.offset ?? 0,
      count: params.count ?? 20,
      no_content: params.no_content ?? 0,
    },
    network: params.account.network,
  });
}

export async function deletePublished(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  article_id: string;
  index?: number;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/freepublish/delete",
    query: { access_token: accessToken },
    body: { article_id: params.article_id, index: params.index ?? 0 },
    network: params.account.network,
  });
}
