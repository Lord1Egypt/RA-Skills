import crypto from "node:crypto";

import { resolveWecomEgressProxyUrlFromNetwork } from "../../config/index.js";
import { readResponseBodyAsBuffer, wecomFetch } from "../../http.js";
import { API_ENDPOINTS, LIMITS } from "../../types/constants.js";
import type { ResolvedAgentAccount } from "../../types/index.js";

type TokenCache = {
  token: string;
  expiresAt: number;
  refreshPromise: Promise<string> | null;
};

const tokenCaches = new Map<string, TokenCache>();

// 企业微信媒体上传大小限制（与 Bot WS 路径保持一致）
// https://developer.work.weixin.qq.com/document/path/90253
const WECOM_MEDIA_SIZE_LIMITS: Record<string, number> = {
  image: 10 * 1024 * 1024,   // 10MB
  voice: 2 * 1024 * 1024,    // 2MB
  video: 10 * 1024 * 1024,   // 10MB
  file: 20 * 1024 * 1024,    // 20MB
};

function resolveEffectiveUploadType(
  type: "image" | "voice" | "video" | "file",
  bufferSize: number,
): { effectiveType: "image" | "voice" | "video" | "file"; downgraded: boolean } {
  // 文件/语音超过各自上限直接由 uploadMedia 抛出清晰错误
  // 图片/视频超过自身上限但未超文件上限 → 降级为 file
  if (
    (type === "image" || type === "video") &&
    bufferSize > WECOM_MEDIA_SIZE_LIMITS[type] &&
    bufferSize <= WECOM_MEDIA_SIZE_LIMITS.file
  ) {
    return { effectiveType: "file", downgraded: true };
  }
  return { effectiveType: type, downgraded: false };
}

function truncateForLog(raw: string, maxChars = 180): string {
  const compact = raw.replace(/\s+/g, " ").trim();
  if (compact.length <= maxChars) return compact;
  return `${compact.slice(0, maxChars)}...(truncated)`;
}

export function normalizeUploadFilename(filename: string): string {
  const trimmed = filename.trim();
  if (!trimmed) return "file.bin";
  const ext = trimmed.includes(".") ? `.${trimmed.split(".").pop()!.toLowerCase()}` : "";
  const base = ext ? trimmed.slice(0, -ext.length) : trimmed;
  const sanitizedBase = base
    .replace(/[^\x20-\x7e]/g, "_")
    .replace(/["\\/;=]/g, "_")
    .replace(/\s+/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "");
  const safeBase = sanitizedBase || "file";
  const safeExt = ext.replace(/[^a-z0-9.]/g, "");
  return `${safeBase}${safeExt || ".bin"}`;
}

export function guessUploadContentType(filename: string): string {
  const ext = filename.split(".").pop()?.toLowerCase() || "";
  const contentTypeMap: Record<string, string> = {
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
    gif: "image/gif",
    webp: "image/webp",
    bmp: "image/bmp",
    amr: "voice/amr",
    mp3: "audio/mpeg",
    wav: "audio/wav",
    m4a: "audio/mp4",
    ogg: "audio/ogg",
    mp4: "video/mp4",
    mov: "video/quicktime",
    txt: "text/plain",
    md: "text/markdown",
    csv: "text/csv",
    tsv: "text/tab-separated-values",
    json: "application/json",
    xml: "application/xml",
    yaml: "application/yaml",
    yml: "application/yaml",
    pdf: "application/pdf",
    doc: "application/msword",
    docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    xls: "application/vnd.ms-excel",
    xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ppt: "application/vnd.ms-powerpoint",
    pptx: "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    rtf: "application/rtf",
    odt: "application/vnd.oasis.opendocument.text",
    zip: "application/zip",
    rar: "application/vnd.rar",
    "7z": "application/x-7z-compressed",
    gz: "application/gzip",
    tgz: "application/gzip",
    tar: "application/x-tar",
  };
  return contentTypeMap[ext] || "application/octet-stream";
}

function requireAgentId(agent: ResolvedAgentAccount): number {
  if (typeof agent.agentId === "number" && Number.isFinite(agent.agentId)) return agent.agentId;
  throw new Error(`wecom agent account=${agent.accountId} missing agentId; sending via cgi-bin/message/send requires agentId`);
}

/**
 * 获取主企业的 access_token
 * 使用 corpid + corpsecret
 */
export async function getAccessToken(agent: ResolvedAgentAccount): Promise<string> {
  const cacheKey = `${agent.corpId}:${String(agent.agentId ?? "na")}`;
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
      const url = `${API_ENDPOINTS.GET_TOKEN}?corpid=${encodeURIComponent(agent.corpId)}&corpsecret=${encodeURIComponent(agent.corpSecret)}`;
      
      const res = await wecomFetch(url, undefined, {
        proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network),
        timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
      });
      const json = (await res.json()) as { access_token?: string; expires_in?: number; errcode?: number; errmsg?: string };

      if (!json?.access_token) {
        throw new Error(`gettoken failed: ${json?.errcode} ${json?.errmsg}`);
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

/**
 * 获取下游企业的 access_token
 * 
 * 根据企业微信文档：https://developer.work.weixin.qq.com/document/path/95816
 * 
 * 请求方式：POST（HTTPS）
 * 请求地址：https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/gettoken?access_token=ACCESS_TOKEN
 * 
 * 请求体：
 * {
 *   "corpid": "下游企业corpid",
 *   "business_type": 1,  // 1 表示上下游企业
 *   "agentid": 下游企业应用ID
 * }
 * 
 * 注意：需要使用上游企业的 access_token 作为调用凭证
 */
export async function getUpstreamAccessToken(params: {
  primaryAgent: ResolvedAgentAccount;
  upstreamCorpId: string;
  upstreamAgentId: number;
}): Promise<string> {
  const { primaryAgent, upstreamCorpId, upstreamAgentId } = params;

  // 缓存 key 增加 primaryCorpId 维度，避免多主企业之间碰撞
  const cacheKey = `upstream:${primaryAgent.corpId}:${upstreamCorpId}:${upstreamAgentId}`;
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
      // 1. 先获取上游企业的 access_token
      const primaryToken = await getAccessToken(primaryAgent);

      // 2. 调用 corpgroup/corp/gettoken 获取下游企业的 access_token
      const url = `https://qyapi.weixin.qq.com/cgi-bin/corpgroup/corp/gettoken?access_token=${encodeURIComponent(primaryToken)}`;
      
      const requestBody = {
        corpid: upstreamCorpId,
        business_type: 1,  // 1 表示上下游企业
        agentid: upstreamAgentId,
      };

      const res = await wecomFetch(
        url,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(requestBody),
        },
        {
          proxyUrl: resolveWecomEgressProxyUrlFromNetwork(primaryAgent.network),
          timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
        },
      );
      
      const json = (await res.json()) as { 
        access_token?: string; 
        expires_in?: number; 
        errcode?: number; 
        errmsg?: string 
      };

      if (!json?.access_token) {
        throw new Error(`get upstream token failed: ${json?.errcode} ${json?.errmsg}`);
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

export async function sendText(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  text: string;
}): Promise<void> {
  const { agent, toUser, toParty, toTag, chatId, text } = params;
  console.log(
    `[wecom-agent-api] sendText request account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} corpId=${agent.corpId} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `textLen=${text.length} textPreview=${JSON.stringify(truncateForLog(text))}`,
  );
  const token = await getAccessToken(agent);

  const useChat = Boolean(chatId);
  const url = useChat
    ? `${API_ENDPOINTS.SEND_APPCHAT}?access_token=${encodeURIComponent(token)}`
    : `${API_ENDPOINTS.SEND_MESSAGE}?access_token=${encodeURIComponent(token)}`;

  const body = useChat
    ? { chatid: chatId, msgtype: "text", text: { content: text } }
    : {
        touser: toUser,
        toparty: toParty,
        totag: toTag,
        msgtype: "text",
        agentid: requireAgentId(agent),
        text: { content: text },
      };

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    { proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network), timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
  );
  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    invaliduser?: string;
    invalidparty?: string;
    invalidtag?: string;
  };

  console.log(
    `[wecom-agent-api] sendText response account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} corpId=${agent.corpId} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `errcode=${String(json?.errcode ?? "N/A")} errmsg=${json?.errmsg ?? ""} ` +
      `invaliduser=${json?.invaliduser ?? ""} invalidparty=${json?.invalidparty ?? ""} invalidtag=${json?.invalidtag ?? ""}`,
  );

  if (json?.errcode !== 0) {
    throw new Error(`send failed: ${json?.errcode} ${json?.errmsg}`);
  }

  if (json?.invaliduser || json?.invalidparty || json?.invalidtag) {
    const details = [
      json.invaliduser ? `invaliduser=${json.invaliduser}` : "",
      json.invalidparty ? `invalidparty=${json.invalidparty}` : "",
      json.invalidtag ? `invalidtag=${json.invalidtag}` : "",
    ]
      .filter(Boolean)
      .join(", ");
    throw new Error(`send partial failure: ${details}`);
  }
}

export async function sendMarkdown(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  text: string;
}): Promise<void> {
  const { agent, toUser, toParty, toTag, chatId, text } = params;
  console.log(
    `[wecom-agent-api] sendMarkdown request account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `textLen=${text.length} textPreview=${JSON.stringify(truncateForLog(text))}`,
  );
  const token = await getAccessToken(agent);

  const useChat = Boolean(chatId);
  const url = useChat
    ? `${API_ENDPOINTS.SEND_APPCHAT}?access_token=${encodeURIComponent(token)}`
    : `${API_ENDPOINTS.SEND_MESSAGE}?access_token=${encodeURIComponent(token)}`;

  // v2.9.3 ⭐ 企微官方 /cgi-bin/message/send 与 /cgi-bin/appchat/send API 的 msgtype 列表是
  // text/image/voice/video/file/textcard/news/mpnews/markdown/miniprogram_notice/template_card——
  // **不包含 markdown_v2**。markdown_v2 仅在群机器人 webhook 路径（/cgi-bin/webhook/send）支持。
  // v2.8.32 误以为 agent-api 支持 markdown_v2，实际从 v2.x 起所有 agent-api 路径发 markdown 内容
  // 一直撞 errcode=40008 invalid message type。
  const body = useChat
    ? { chatid: chatId, msgtype: "markdown", markdown: { content: text } }
    : {
        touser: toUser,
        toparty: toParty,
        totag: toTag,
        msgtype: "markdown",
        agentid: requireAgentId(agent),
        markdown: { content: text },
      };

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    { proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network), timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
  );
  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    invaliduser?: string;
    invalidparty?: string;
    invalidtag?: string;
  };

  console.log(
    `[wecom-agent-api] sendMarkdown response account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `errcode=${String(json?.errcode ?? "N/A")} errmsg=${json?.errmsg ?? ""} ` +
      `invaliduser=${json?.invaliduser ?? ""} invalidparty=${json?.invalidparty ?? ""} invalidtag=${json?.invalidtag ?? ""}`,
  );

  if (json?.errcode !== 0) {
    throw new Error(`send failed: ${json?.errcode} ${json?.errmsg}`);
  }

  if (json?.invaliduser || json?.invalidparty || json?.invalidtag) {
    const details = [
      json.invaliduser ? `invaliduser=${json.invaliduser}` : "",
      json.invalidparty ? `invalidparty=${json.invalidparty}` : "",
      json.invalidtag ? `invalidtag=${json.invalidtag}` : "",
    ]
      .filter(Boolean)
      .join(", ");
    throw new Error(`send partial failure: ${details}`);
  }
}

export async function sendTextcard(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  title: string;
  description: string;
  url?: string;
  btntxt?: string;
}): Promise<void> {
  const { agent, toUser, toParty, toTag, chatId, title, description, url, btntxt } = params;
  console.log(
    `[wecom-agent-api] sendTextcard request account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `title=${JSON.stringify(truncateForLog(title))} descLen=${description.length} url=${url ?? ""} btntxt=${btntxt ?? ""}`,
  );
  const token = await getAccessToken(agent);

  const useChat = Boolean(chatId);
  const sendUrl = useChat
    ? `${API_ENDPOINTS.SEND_APPCHAT}?access_token=${encodeURIComponent(token)}`
    : `${API_ENDPOINTS.SEND_MESSAGE}?access_token=${encodeURIComponent(token)}`;

  const textcardBody = {
    title,
    description,
    url: url ?? "",
    btntxt: btntxt ?? "",
  };

  const body = useChat
    ? { chatid: chatId, msgtype: "textcard", textcard: textcardBody }
    : {
        touser: toUser,
        toparty: toParty,
        totag: toTag,
        msgtype: "textcard",
        agentid: requireAgentId(agent),
        textcard: textcardBody,
      };

  const res = await wecomFetch(
    sendUrl,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    { proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network), timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
  );
  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    invaliduser?: string;
    invalidparty?: string;
    invalidtag?: string;
  };

  console.log(
    `[wecom-agent-api] sendTextcard response account=${agent.accountId} agentId=${String(agent.agentId ?? "N/A")} ` +
      `toUser=${toUser ?? ""} toParty=${toParty ?? ""} toTag=${toTag ?? ""} chatId=${chatId ?? ""} ` +
      `errcode=${String(json?.errcode ?? "N/A")} errmsg=${json?.errmsg ?? ""} ` +
      `invaliduser=${json?.invaliduser ?? ""} invalidparty=${json?.invalidparty ?? ""} invalidtag=${json?.invalidtag ?? ""}`,
  );

  if (json?.errcode !== 0) {
    throw new Error(`send failed: ${json?.errcode} ${json?.errmsg}`);
  }

  if (json?.invaliduser || json?.invalidparty || json?.invalidtag) {
    const details = [
      json.invaliduser ? `invaliduser=${json.invaliduser}` : "",
      json.invalidparty ? `invalidparty=${json.invalidparty}` : "",
      json.invalidtag ? `invalidtag=${json.invalidtag}` : "",
    ]
      .filter(Boolean)
      .join(", ");
    throw new Error(`send partial failure: ${details}`);
  }
}

export async function uploadMedia(params: {
  agent: ResolvedAgentAccount;
  type: "image" | "voice" | "video" | "file";
  buffer: Buffer;
  filename: string;
}): Promise<string> {
  const { agent, type, buffer, filename } = params;
  const safeFilename = normalizeUploadFilename(filename);
  const sizeLimit = WECOM_MEDIA_SIZE_LIMITS[type];
  const fileSizeMB = (buffer.length / (1024 * 1024)).toFixed(2);

  // 检查文件是否超过全局上限（20MB）
  if (buffer.length > WECOM_MEDIA_SIZE_LIMITS.file) {
    throw new Error(
      `文件大小 ${fileSizeMB}MB 超过了企业微信允许的最大限制 20MB，无法发送。`,
    );
  }

  // 如果需要降级（图片/视频超过自身上限但未超文件上限），转为 file 类型上传
  const { effectiveType, downgraded } = resolveEffectiveUploadType(type, buffer.length);
  if (downgraded) {
    console.log(
      `[wecom-upload] Downgrading upload type from ${type} to file (size=${fileSizeMB}MB > ${(sizeLimit / (1024 * 1024)).toFixed(0)}MB limit)`,
    );
  }

  // 检查非降级场景下是否超过该类型的上限（语音无降级路径，直接拒绝）
  if (!downgraded && buffer.length > sizeLimit) {
    const limitMB = (sizeLimit / (1024 * 1024)).toFixed(0);
    throw new Error(
      `文件大小 ${fileSizeMB}MB 超过了企业微信 ${type} 类型允许的最大限制 ${limitMB}MB，无法发送。`,
    );
  }

  const token = await getAccessToken(agent);
  const proxyUrl = resolveWecomEgressProxyUrlFromNetwork(agent.network);
  const url = `${API_ENDPOINTS.UPLOAD_MEDIA}?access_token=${encodeURIComponent(token)}&type=${encodeURIComponent(effectiveType)}&debug=1`;

  console.log(`[wecom-upload] Uploading media: originalType=${type} effectiveType=${effectiveType} filename=${safeFilename}, size=${buffer.length} bytes, corpId=${agent.corpId}`);

  const uploadOnce = async (fileContentType: string) => {
    const boundary = `----WebKitFormBoundary${crypto.randomBytes(16).toString("hex")}`;
    const header = Buffer.from(
      `--${boundary}\r\n` +
        `Content-Disposition: form-data; name="media"; filename="${safeFilename}"; filelength=${buffer.length}\r\n` +
        `Content-Type: ${fileContentType}\r\n\r\n`,
    );
    const footer = Buffer.from(`\r\n--${boundary}--\r\n`);
    const body = Buffer.concat([header, buffer, footer]);

    console.log(`[wecom-upload] Multipart body size=${body.length}, boundary=${boundary}, fileContentType=${fileContentType}`);

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
    const json = (await res.json()) as { media_id?: string; errcode?: number; errmsg?: string };
    console.log(`[wecom-upload] Response:`, JSON.stringify(json));
    return json;
  };

  const preferredContentType = guessUploadContentType(safeFilename);
  let json = await uploadOnce(preferredContentType);

  if (!json?.media_id && preferredContentType !== "application/octet-stream") {
    console.warn(
      `[wecom-upload] Upload failed with ${preferredContentType}, retrying as application/octet-stream: ${json?.errcode} ${json?.errmsg}`,
    );
    json = await uploadOnce("application/octet-stream");
  }

  if (!json?.media_id) {
    throw new Error(`upload failed: ${json?.errcode} ${json?.errmsg}`);
  }
  return json.media_id;
}

export async function sendMedia(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  mediaId: string;
  mediaType: "image" | "voice" | "video" | "file";
  title?: string;
  description?: string;
}): Promise<void> {
  const { agent, toUser, toParty, toTag, chatId, mediaId, mediaType, title, description } = params;
  const token = await getAccessToken(agent);

  const useChat = Boolean(chatId);
  const url = useChat
    ? `${API_ENDPOINTS.SEND_APPCHAT}?access_token=${encodeURIComponent(token)}`
    : `${API_ENDPOINTS.SEND_MESSAGE}?access_token=${encodeURIComponent(token)}`;

  const mediaPayload = mediaType === "video" ? { media_id: mediaId, title: title ?? "Video", description: description ?? "" } : { media_id: mediaId };
  const body = useChat
    ? { chatid: chatId, msgtype: mediaType, [mediaType]: mediaPayload }
    : {
        touser: toUser,
        toparty: toParty,
        totag: toTag,
        msgtype: mediaType,
        agentid: requireAgentId(agent),
        [mediaType]: mediaPayload,
      };

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    { proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network), timeoutMs: LIMITS.REQUEST_TIMEOUT_MS },
  );
  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    invaliduser?: string;
    invalidparty?: string;
    invalidtag?: string;
  };

  if (json?.errcode !== 0) {
    throw new Error(`send ${mediaType} failed: ${json?.errcode} ${json?.errmsg}`);
  }

  if (json?.invaliduser || json?.invalidparty || json?.invalidtag) {
    const details = [
      json.invaliduser ? `invaliduser=${json.invaliduser}` : "",
      json.invalidparty ? `invalidparty=${json.invalidparty}` : "",
      json.invalidtag ? `invalidtag=${json.invalidtag}` : "",
    ]
      .filter(Boolean)
      .join(", ");
    throw new Error(`send ${mediaType} partial failure: ${details}`);
  }
}

export async function downloadMedia(params: {
  agent: ResolvedAgentAccount;
  mediaId: string;
  maxBytes?: number;
}): Promise<{ buffer: Buffer; contentType: string; filename?: string }> {
  const { agent, mediaId } = params;
  const token = await getAccessToken(agent);
  const url = `${API_ENDPOINTS.DOWNLOAD_MEDIA}?access_token=${encodeURIComponent(token)}&media_id=${encodeURIComponent(mediaId)}`;

  const res = await wecomFetch(url, undefined, {
    proxyUrl: resolveWecomEgressProxyUrlFromNetwork(agent.network),
    timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
  });

  if (!res.ok) {
    throw new Error(`download failed: ${res.status}`);
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
    throw new Error(`download failed: ${json?.errcode} ${json?.errmsg}`);
  }

  const buffer = await readResponseBodyAsBuffer(res, params.maxBytes);
  return { buffer, contentType, filename };
}
