import type { ResolvedAgentAccount } from "../../types/index.js";
import { API_ENDPOINTS, LIMITS } from "../../types/constants.js";
import { resolveWecomEgressProxyUrlFromNetwork } from "../../config/index.js";
import { readResponseBodyAsBuffer, wecomFetch } from "../../http.js";
import {
  downloadMedia as downloadLegacyMedia,
  getAccessToken as getLegacyAccessToken,
  getUpstreamAccessToken as getLegacyUpstreamAccessToken,
  sendMedia as sendLegacyMedia,
  sendMarkdown as sendLegacyMarkdown,
  sendText as sendLegacyText,
  sendTextcard as sendLegacyTextcard,
} from "./core.js";

export async function getAgentApiAccessToken(agent: ResolvedAgentAccount): Promise<string> {
  return getLegacyAccessToken(agent);
}

export async function getUpstreamAgentApiAccessToken(params: {
  primaryAgent: ResolvedAgentAccount;
  upstreamCorpId: string;
  upstreamAgentId: number;
}): Promise<string> {
  return getLegacyUpstreamAccessToken(params);
}

export async function sendAgentApiText(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  text: string;
}): Promise<void> {
  await sendLegacyText(params);
}

export async function sendAgentApiMarkdown(params: {
  agent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  text: string;
}): Promise<void> {
  console.log(
    `[wecom-agent-api] sendMarkdown account=${params.agent.accountId} ` +
      `toUser=${params.toUser ?? ""} toParty=${params.toParty ?? ""} toTag=${params.toTag ?? ""} chatId=${params.chatId ?? ""} ` +
      `textLen=${params.text.length}`,
  );
  await sendLegacyMarkdown(params);
}

export async function sendAgentApiMedia(params: {
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
  await sendLegacyMedia(params);
}

export async function downloadAgentApiMedia(params: {
  agent: ResolvedAgentAccount;
  mediaId: string;
  maxBytes?: number;
}): Promise<{ buffer: Buffer; contentType: string; filename?: string }> {
  return downloadLegacyMedia(params);
}

export async function sendAgentApiTextcard(params: {
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
  console.log(
    `[wecom-agent-api] sendTextcard account=${params.agent.accountId} ` +
      `toUser=${params.toUser ?? ""} toParty=${params.toParty ?? ""} toTag=${params.toTag ?? ""} chatId=${params.chatId ?? ""} ` +
      `title=${JSON.stringify(params.title)} descLen=${params.description.length}`,
  );
  await sendLegacyTextcard(params);
}

export async function sendUpstreamAgentApiText(params: {
  upstreamAgent: ResolvedAgentAccount;
  primaryAgent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  text: string;
}): Promise<void> {
  const { upstreamAgent, primaryAgent, toUser, toParty, toTag, chatId, text } = params;

  const token = await getUpstreamAgentApiAccessToken({
    primaryAgent,
    upstreamCorpId: upstreamAgent.corpId,
    upstreamAgentId: upstreamAgent.agentId!,
  });

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
        agentid: upstreamAgent.agentId,
        text: { content: text },
      };

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    {
      proxyUrl: resolveWecomEgressProxyUrlFromNetwork(upstreamAgent.network),
      timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
    },
  );

  const json = (await res.json()) as {
    errcode?: number;
    errmsg?: string;
    invaliduser?: string;
    invalidparty?: string;
    invalidtag?: string;
  };

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

export async function sendUpstreamAgentApiMedia(params: {
  upstreamAgent: ResolvedAgentAccount;
  primaryAgent: ResolvedAgentAccount;
  toUser?: string;
  toParty?: string;
  toTag?: string;
  chatId?: string;
  mediaId: string;
  mediaType: "image" | "voice" | "video" | "file";
  title?: string;
  description?: string;
}): Promise<void> {
  const {
    upstreamAgent,
    primaryAgent,
    toUser,
    toParty,
    toTag,
    chatId,
    mediaId,
    mediaType,
    title,
    description,
  } = params;

  const token = await getUpstreamAgentApiAccessToken({
    primaryAgent,
    upstreamCorpId: upstreamAgent.corpId,
    upstreamAgentId: upstreamAgent.agentId!,
  });

  console.log(
    `[wecom-upstream-api] sendMedia corpId=${upstreamAgent.corpId} agentId=${upstreamAgent.agentId} ` +
      `toUser=${toUser ?? ""} mediaType=${mediaType}`,
  );

  const useChat = Boolean(chatId);
  const url = useChat
    ? `${API_ENDPOINTS.SEND_APPCHAT}?access_token=${encodeURIComponent(token)}`
    : `${API_ENDPOINTS.SEND_MESSAGE}?access_token=${encodeURIComponent(token)}`;

  const mediaPayload =
    mediaType === "video"
      ? { media_id: mediaId, title: title ?? "Video", description: description ?? "" }
      : { media_id: mediaId };

  const body = useChat
    ? { chatid: chatId, msgtype: mediaType, [mediaType]: mediaPayload }
    : {
        touser: toUser,
        toparty: toParty,
        totag: toTag,
        msgtype: mediaType,
        agentid: upstreamAgent.agentId,
        [mediaType]: mediaPayload,
      };

  const res = await wecomFetch(
    url,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
    {
      proxyUrl: resolveWecomEgressProxyUrlFromNetwork(upstreamAgent.network),
      timeoutMs: LIMITS.REQUEST_TIMEOUT_MS,
    },
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

export async function downloadUpstreamAgentApiMedia(params: {
  upstreamAgent: ResolvedAgentAccount;
  primaryAgent: ResolvedAgentAccount;
  mediaId: string;
  maxBytes?: number;
}): Promise<{ buffer: Buffer; contentType: string; filename?: string }> {
  const { upstreamAgent, primaryAgent, mediaId, maxBytes } = params;

  const token = await getUpstreamAgentApiAccessToken({
    primaryAgent,
    upstreamCorpId: upstreamAgent.corpId,
    upstreamAgentId: upstreamAgent.agentId!,
  });

  const url = `${API_ENDPOINTS.DOWNLOAD_MEDIA}?access_token=${encodeURIComponent(token)}&media_id=${encodeURIComponent(mediaId)}`;

  const res = await wecomFetch(url, undefined, {
    proxyUrl: resolveWecomEgressProxyUrlFromNetwork(upstreamAgent.network),
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

  const buffer = await readResponseBodyAsBuffer(res, maxBytes);
  return { buffer, contentType, filename };
}
