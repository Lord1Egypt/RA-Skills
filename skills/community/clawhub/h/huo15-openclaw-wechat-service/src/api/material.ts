/**
 * 素材管理（临时/永久）
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
 *
 * 当前覆盖：
 * - uploadTemporaryMedia(type, buffer)：上传临时素材 (3 天有效)
 * - uploadPermanentImage：图文消息内图片专用（返回 url 而不是 media_id）
 * - uploadPermanentMedia：永久素材 (image/voice/video/thumb)
 * - deletePermanentMaterial / listPermanentMaterial / getPermanentMaterial
 */

import { Agent, ProxyAgent, fetch as undiciFetch, FormData } from "undici";

import type { AccessTokenHandle } from "../access-token.js";
import { DEFAULT_API_BASE_URL, buildWechatApiError } from "../http-client.js";
import { jsonRequest } from "../http-client.js";
import type { ResolvedWechatServiceAccount, WechatServiceNetworkConfig } from "../types.js";

export type TemporaryMediaType = "image" | "voice" | "video" | "thumb";

function selectDispatcher(network?: WechatServiceNetworkConfig) {
  if (network?.egressProxyUrl?.trim()) {
    return new ProxyAgent({ uri: network.egressProxyUrl.trim() });
  }
  return new Agent({
    connect: { timeout: network?.timeoutMs ?? 15_000 },
    bodyTimeout: network?.timeoutMs ?? 60_000,
    headersTimeout: network?.timeoutMs ?? 15_000,
  });
}

async function multipartUpload<T extends Record<string, unknown>>(params: {
  url: string;
  form: FormData;
  network?: WechatServiceNetworkConfig;
}): Promise<T> {
  const dispatcher = selectDispatcher(params.network);
  const res = await undiciFetch(params.url, {
    method: "POST",
    body: params.form,
    dispatcher,
  });
  const contentType = res.headers.get("content-type") ?? "";
  const text = await res.text();
  let parsed: Record<string, unknown> = {};
  if (contentType.includes("application/json") || /^\s*\{/.test(text)) {
    try {
      parsed = JSON.parse(text);
    } catch {
      parsed = {};
    }
  }
  if (!res.ok) {
    throw buildWechatApiError({
      endpoint: params.url,
      errcode: parsed.errcode as number | undefined,
      errmsg: parsed.errmsg as string | undefined,
      httpStatus: res.status,
      raw: parsed,
    });
  }
  const errcode = parsed.errcode as number | undefined;
  if (typeof errcode === "number" && errcode !== 0) {
    throw buildWechatApiError({
      endpoint: params.url,
      errcode,
      errmsg: parsed.errmsg as string | undefined,
      httpStatus: res.status,
      raw: parsed,
    });
  }
  return parsed as T;
}

function buildUploadUrl(params: {
  account: ResolvedWechatServiceAccount;
  endpoint: string;
  query: Record<string, string>;
}): string {
  const base = params.account.network?.apiBaseUrl ?? DEFAULT_API_BASE_URL;
  const u = new URL(
    params.endpoint,
    base.endsWith("/") ? base : `${base}/`,
  );
  for (const [k, v] of Object.entries(params.query)) {
    u.searchParams.set(k, v);
  }
  return u.toString();
}

/**
 * **uploadTemporaryMedia**
 *
 * 临时素材上传：返回 media_id，有效期 3 天。
 */
export async function uploadTemporaryMedia(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  type: TemporaryMediaType;
  buffer: Buffer;
  filename: string;
  contentType?: string;
}): Promise<{
  mediaId: string;
  type: string;
  createdAt: number;
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const url = buildUploadUrl({
    account: params.account,
    endpoint: "cgi-bin/media/upload",
    query: { access_token: accessToken, type: params.type },
  });
  const form = new FormData();
  const blob = new Blob([new Uint8Array(params.buffer)], {
    type: params.contentType ?? "application/octet-stream",
  });
  form.append("media", blob, params.filename);
  const data = await multipartUpload<{
    type?: string;
    media_id?: string;
    created_at?: number;
  }>({
    url,
    form,
    network: params.account.network,
  });
  if (!data.media_id) {
    throw new Error(
      `[wechat-service] uploadTemporaryMedia missing media_id: ${JSON.stringify(data)}`,
    );
  }
  return {
    mediaId: data.media_id,
    type: data.type ?? params.type,
    createdAt: data.created_at ?? Math.floor(Date.now() / 1000),
  };
}

/**
 * **uploadPermanentImage**
 *
 * 图文消息内嵌图片专用：返回图片 URL（非 media_id），可直接在图文正文里用。
 */
export async function uploadPermanentImage(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  buffer: Buffer;
  filename: string;
  contentType?: string;
}): Promise<{ url: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const url = buildUploadUrl({
    account: params.account,
    endpoint: "cgi-bin/media/uploadimg",
    query: { access_token: accessToken },
  });
  const form = new FormData();
  const blob = new Blob([new Uint8Array(params.buffer)], {
    type: params.contentType ?? "image/jpeg",
  });
  form.append("media", blob, params.filename);
  const data = await multipartUpload<{ url?: string }>({
    url,
    form,
    network: params.account.network,
  });
  if (!data.url) {
    throw new Error(
      `[wechat-service] uploadPermanentImage missing url: ${JSON.stringify(data)}`,
    );
  }
  return { url: data.url };
}

export type PermanentMediaType = "image" | "voice" | "video" | "thumb";

/**
 * **uploadPermanentMedia**
 *
 * 永久素材：图片/语音/缩略图直接返回 media_id；video 需要额外的 description。
 */
export async function uploadPermanentMedia(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  type: PermanentMediaType;
  buffer: Buffer;
  filename: string;
  contentType?: string;
  videoDescription?: { title: string; introduction: string };
}): Promise<{
  mediaId: string;
  url?: string;
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const url = buildUploadUrl({
    account: params.account,
    endpoint: "cgi-bin/material/add_material",
    query: { access_token: accessToken, type: params.type },
  });
  const form = new FormData();
  const blob = new Blob([new Uint8Array(params.buffer)], {
    type: params.contentType ?? "application/octet-stream",
  });
  form.append("media", blob, params.filename);
  if (params.type === "video") {
    if (!params.videoDescription) {
      throw new Error(
        "[wechat-service] uploadPermanentMedia(video) requires videoDescription={title, introduction}",
      );
    }
    form.append("description", JSON.stringify(params.videoDescription));
  }
  const data = await multipartUpload<{
    media_id?: string;
    url?: string;
  }>({
    url,
    form,
    network: params.account.network,
  });
  if (!data.media_id) {
    throw new Error(
      `[wechat-service] uploadPermanentMedia missing media_id: ${JSON.stringify(data)}`,
    );
  }
  return { mediaId: data.media_id, url: data.url };
}

export async function deletePermanentMaterial(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  mediaId: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/material/del_material",
    query: { access_token: accessToken },
    body: { media_id: params.mediaId },
    network: params.account.network,
  });
}

export async function getPermanentMaterial(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  mediaId: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/material/get_material",
    query: { access_token: accessToken },
    body: { media_id: params.mediaId },
    network: params.account.network,
  });
}

export async function listPermanentMaterial(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  type: PermanentMediaType;
  offset?: number;
  count?: number;
}): Promise<{
  totalCount?: number;
  itemCount?: number;
  item?: Array<Record<string, unknown>>;
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{
    total_count?: number;
    item_count?: number;
    item?: Array<Record<string, unknown>>;
  }>({
    method: "POST",
    endpoint: "cgi-bin/material/batchget_material",
    query: { access_token: accessToken },
    body: {
      type: params.type,
      offset: params.offset ?? 0,
      count: params.count ?? 20,
    },
    network: params.account.network,
  });
  return {
    totalCount: data.total_count,
    itemCount: data.item_count,
    item: data.item,
  };
}

export async function getMaterialCount(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<{
  voiceCount?: number;
  videoCount?: number;
  imageCount?: number;
  newsCount?: number;
}> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{
    voice_count?: number;
    video_count?: number;
    image_count?: number;
    news_count?: number;
  }>({
    method: "GET",
    endpoint: "cgi-bin/material/get_materialcount",
    query: { access_token: accessToken },
    network: params.account.network,
  });
  return {
    voiceCount: data.voice_count,
    videoCount: data.video_count,
    imageCount: data.image_count,
    newsCount: data.news_count,
  };
}
