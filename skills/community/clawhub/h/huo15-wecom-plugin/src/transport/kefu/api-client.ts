import crypto from "node:crypto";

import { resolveWecomEgressProxyUrlFromNetwork } from "../../config/index.js";
import { readResponseBodyAsBuffer, wecomFetch } from "../../http.js";
import { API_ENDPOINTS, LIMITS } from "../../types/constants.js";
import type { ResolvedKefuAccount } from "../../types/index.js";
import {
  guessUploadContentType,
  normalizeUploadFilename,
} from "../agent-api/core.js";

type TokenCache = {
  token: string;
  expiresAt: number;
  refreshPromise: Promise<string> | null;
};

const tokenCaches = new Map<string, TokenCache>();

export async function getKefuAccessToken(kefu: ResolvedKefuAccount): Promise<string> {
  const cacheKey = `kefu:${kefu.corpId}:${kefu.accountId}`;
  let cache = tokenCaches.get(cacheKey);
  if (!cache) {
    cache = { token: "", expiresAt: 0, refreshPromise: null };
    tokenCaches.set(cacheKey, cache);
  }

  const now = Date.now();
  if (cache.token && cache.expiresAt > now + LIMITS.TOKEN_REFRESH_BUFFER_MS) {
    return cache.token;
  }
  if (cache.refreshPromise) {
    return cache.refreshPromise;
  }

  cache.refreshPromise = (async () => {
    try {
      const url = `${API_ENDPOINTS.GET_TOKEN}?corpid=${encodeURIComponent(kefu.corpId)}&corpsecret=${encodeURIComponent(kefu.corpSecret)}`;
      const res = await wecomFetch(url, undefined, {
        proxyUrl: resolveWecomEgressProxyUrlFromNetwork(kefu.network),
        timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
      });
      const json = (await res.json()) as {
        access_token?: string;
        expires_in?: number;
        errcode?: number;
        errmsg?: string;
      };
      if (!json?.access_token) {
        throw new Error(`kefu gettoken failed: ${json?.errcode} ${json?.errmsg}`);
      }
      cache!.token = json.access_token;
      cache!.expiresAt = Date.now() + (json.expires_in ?? 7200) * 1000;
      return cache!.token;
    } finally {
      cache!.refreshPromise = null;
    }
  })();

  return cache.refreshPromise;
}

export type KefuSyncMessage = Record<string, unknown> & {
  msgid?: string;
  open_kfid?: string;
  external_userid?: string;
  send_time?: number;
  origin?: number;
  servicer_userid?: string;
  msgtype?: string;
  event?: {
    event_type?: string;
    open_kfid?: string;
    external_userid?: string;
    scene?: string;
    welcome_code?: string;
    [k: string]: unknown;
  };
};

export type KefuSyncResult = {
  next_cursor?: string;
  has_more?: number;
  msg_list: KefuSyncMessage[];
  errcode: number;
  errmsg: string;
};

export async function syncKefuMessages(params: {
  kefu: ResolvedKefuAccount;
  token: string;
  cursor?: string;
  openKfid?: string;
  limit?: number;
}): Promise<KefuSyncResult> {
  const accessToken = await getKefuAccessToken(params.kefu);
  const url = `${API_ENDPOINTS.KEFU_SYNC_MSG}?access_token=${encodeURIComponent(accessToken)}`;
  const body: Record<string, unknown> = {
    token: params.token,
    limit: params.limit ?? 1000,
  };
  if (params.cursor) body.cursor = params.cursor;
  if (params.openKfid) body.open_kfid = params.openKfid;

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    {
      proxyUrl: resolveWecomEgressProxyUrlFromNetwork(params.kefu.network),
      timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
    },
  );
  const json = (await res.json()) as Partial<KefuSyncResult> & {
    errcode?: number;
    errmsg?: string;
  };
  if ((json?.errcode ?? -1) !== 0) {
    throw new Error(`kefu sync_msg failed: ${json?.errcode} ${json?.errmsg ?? ""}`);
  }
  return {
    next_cursor: json.next_cursor,
    has_more: json.has_more ?? 0,
    msg_list: Array.isArray(json.msg_list) ? json.msg_list : [],
    errcode: json.errcode ?? 0,
    errmsg: json.errmsg ?? "",
  };
}

type KefuSendMsgPayload = {
  touser: string;
  open_kfid: string;
  msgtype: string;
  [key: string]: unknown;
};

async function postKefuSendMsg(params: {
  kefu: ResolvedKefuAccount;
  payload: KefuSendMsgPayload;
}): Promise<{ msgid?: string }> {
  const accessToken = await getKefuAccessToken(params.kefu);
  const url = `${API_ENDPOINTS.KEFU_SEND_MSG}?access_token=${encodeURIComponent(accessToken)}`;
  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params.payload),
    },
    {
      proxyUrl: resolveWecomEgressProxyUrlFromNetwork(params.kefu.network),
      timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
    },
  );
  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    msgid?: string;
  };
  if ((json?.errcode ?? -1) !== 0) {
    throw new Error(`kefu send_msg failed: ${json?.errcode} ${json?.errmsg ?? ""}`);
  }
  return { msgid: json.msgid };
}

export async function sendKefuText(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  text: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "text",
      text: { content: params.text },
    },
  });
}

export async function sendKefuImage(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  mediaId: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "image",
      image: { media_id: params.mediaId },
    },
  });
}

export async function sendKefuVoice(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  mediaId: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "voice",
      voice: { media_id: params.mediaId },
    },
  });
}

export async function sendKefuVideo(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  mediaId: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "video",
      video: { media_id: params.mediaId },
    },
  });
}

export async function sendKefuFile(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  mediaId: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "file",
      file: { media_id: params.mediaId },
    },
  });
}

export async function sendKefuLink(params: {
  kefu: ResolvedKefuAccount;
  toUser: string;
  openKfid: string;
  title: string;
  desc?: string;
  url: string;
  thumbMediaId?: string;
}): Promise<{ msgid?: string }> {
  return postKefuSendMsg({
    kefu: params.kefu,
    payload: {
      touser: params.toUser,
      open_kfid: params.openKfid,
      msgtype: "link",
      link: {
        title: params.title,
        desc: params.desc ?? "",
        url: params.url,
        thumb_media_id: params.thumbMediaId ?? "",
      },
    },
  });
}

export async function uploadKefuMedia(params: {
  kefu: ResolvedKefuAccount;
  type: "image" | "voice" | "video" | "file";
  buffer: Buffer;
  filename: string;
}): Promise<string> {
  const safeFilename = normalizeUploadFilename(params.filename);
  const accessToken = await getKefuAccessToken(params.kefu);
  const proxyUrl = resolveWecomEgressProxyUrlFromNetwork(params.kefu.network);
  const url = `${API_ENDPOINTS.KEFU_UPLOAD_MEDIA}?access_token=${encodeURIComponent(accessToken)}&type=${encodeURIComponent(params.type)}`;

  const uploadOnce = async (fileContentType: string) => {
    const boundary = `----WebKitFormBoundary${crypto.randomBytes(16).toString("hex")}`;
    const header = Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="media"; filename="${safeFilename}"; filelength=${params.buffer.length}\r\n` +
        `Content-Type: ${fileContentType}\r\n\r\n`,
    );
    const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
    const body = Buffer.concat([header, params.buffer, footer]);
    const res = await wecomFetch(
      url,
      {
        method: "POST",
        headers: {
          "Content-Type": `multipart/form-data; boundary=${boundary}`,
          "Content-Length": String(body.length),
        },
        body,
      },
      { proxyUrl, timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
    );
    return (await res.json()) as { media_id?: string; errcode?: number; errmsg?: string };
  };

  const preferred = guessUploadContentType(safeFilename);
  let json = await uploadOnce(preferred);
  if (!json?.media_id && preferred !== "application/octet-stream") {
    json = await uploadOnce("application/octet-stream");
  }
  if (!json?.media_id) {
    throw new Error(`kefu upload failed: ${json?.errcode} ${json?.errmsg ?? ""}`);
  }
  return json.media_id;
}

export async function downloadKefuMedia(params: {
  kefu: ResolvedKefuAccount;
  mediaId: string;
  maxBytes?: number;
}): Promise<{ buffer: Buffer; contentType: string; filename?: string }> {
  const accessToken = await getKefuAccessToken(params.kefu);
  const url = `${API_ENDPOINTS.DOWNLOAD_MEDIA}?access_token=${encodeURIComponent(accessToken)}&media_id=${encodeURIComponent(params.mediaId)}`;
  const res = await wecomFetch(url, undefined, {
    proxyUrl: resolveWecomEgressProxyUrlFromNetwork(params.kefu.network),
    timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
  });
  if (!res.ok) {
    throw new Error(`kefu media download failed: ${res.status}`);
  }
  const contentType = res.headers.get("content-type") || "application/octet-stream";
  const disposition = res.headers.get("content-disposition") || "";
  const filename = (() => {
    const mStar = disposition.match(/filename\*\s*=\s*([^;]+)/i);
    if (mStar) {
      const raw = mStar[1]!.trim().replace(/^"(.*)"$/, "$1");
      const parts = raw.split("''");
      const encoded = parts.length === 2 ? parts[1]! : raw;
      try {
        return decodeURIComponent(encoded);
      } catch {
        return encoded;
      }
    }
    const m = disposition.match(/filename\s*=\s*([^;]+)/i);
    if (!m) return undefined;
    return m[1]!.trim().replace(/^"(.*)"$/, "$1") || undefined;
  })();
  if (contentType.includes("application/json")) {
    const json = (await res.json()) as { errcode?: number; errmsg?: string };
    throw new Error(`kefu media download failed: ${json?.errcode} ${json?.errmsg ?? ""}`);
  }
  const buffer = await readResponseBodyAsBuffer(res, params.maxBytes);
  return { buffer, contentType, filename };
}
