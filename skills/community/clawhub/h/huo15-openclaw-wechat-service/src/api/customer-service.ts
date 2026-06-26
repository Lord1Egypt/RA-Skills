/**
 * 客服消息 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Service_Center_messages.html
 *
 * 48 小时窗口规则：用户在过去 48 小时内与公众号有过交互（发消息/点菜单/扫码等）时，可主动下发。
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";
import {
  renderMarkdownForWechatText,
  truncateForWechatText,
} from "../shared/markdown-to-wechat.js";

export type CustomerServiceTextMessage = {
  touser: string;
  msgtype: "text";
  text: { content: string };
  customservice?: { kf_account: string };
};

export type CustomerServiceImageMessage = {
  touser: string;
  msgtype: "image";
  image: { media_id: string };
};

export type CustomerServiceVoiceMessage = {
  touser: string;
  msgtype: "voice";
  voice: { media_id: string };
};

export type CustomerServiceVideoMessage = {
  touser: string;
  msgtype: "video";
  video: {
    media_id: string;
    thumb_media_id: string;
    title?: string;
    description?: string;
  };
};

export type CustomerServiceNewsMessage = {
  touser: string;
  msgtype: "news";
  news: {
    articles: Array<{
      title: string;
      description?: string;
      url: string;
      picurl?: string;
    }>;
  };
};

export type CustomerServiceMpNewsMessage = {
  touser: string;
  msgtype: "mpnews";
  mpnews: { media_id: string };
};

export type CustomerServiceMpNewsArticleMessage = {
  touser: string;
  msgtype: "mpnewsarticle";
  mpnewsarticle: { article_id: string };
};

export type CustomerServiceMenuMessage = {
  touser: string;
  msgtype: "msgmenu";
  msgmenu: {
    head_content: string;
    list: Array<{ id: string; content: string }>;
    tail_content?: string;
  };
};

export type CustomerServiceWxcardMessage = {
  touser: string;
  msgtype: "wxcard";
  wxcard: { card_id: string };
};

export type CustomerServiceMiniprogrampageMessage = {
  touser: string;
  msgtype: "miniprogrampage";
  miniprogrampage: {
    title: string;
    appid: string;
    pagepath: string;
    thumb_media_id: string;
  };
};

export type CustomerServiceMessage =
  | CustomerServiceTextMessage
  | CustomerServiceImageMessage
  | CustomerServiceVoiceMessage
  | CustomerServiceVideoMessage
  | CustomerServiceNewsMessage
  | CustomerServiceMpNewsMessage
  | CustomerServiceMpNewsArticleMessage
  | CustomerServiceMenuMessage
  | CustomerServiceWxcardMessage
  | CustomerServiceMiniprogrampageMessage;

/**
 * **renderTextMessage**（v2.3.1+）—— sendCustomerServiceMessage 内部最后一道闸。
 *
 * 任何 `msgtype === "text"` 的客服消息在发送给微信之前，content 都会被强制过一遍
 * `renderMarkdownForWechatText` —— 即使上游忘了或绕过 dispatcher.ts 直接调
 * （比如 outbound.ts / message-tool / auto-reply 关键词回复 / subscribe 欢迎语），
 * 粉丝也不会看到 `**` `#` `- ` 这些原始 markdown 字符。
 *
 * 渲染器对纯文本是**幂等**的（render(render(x)) === render(x)），所以双层渲染不会出 bug。
 */
function renderTextMessage(message: CustomerServiceMessage): CustomerServiceMessage {
  if (message.msgtype !== "text") return message;
  const original = message.text?.content ?? "";
  // 微信 text 限 2048 字节（errcode 45002）；默认 1900 字节留余量给 envelope
  const rendered = truncateForWechatText(
    renderMarkdownForWechatText(original),
  );
  if (rendered === original) return message;
  return {
    ...message,
    text: { content: rendered },
  };
}

export async function sendCustomerServiceMessage(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  message: CustomerServiceMessage;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const body = renderTextMessage(params.message);
  try {
    await jsonRequest({
      method: "POST",
      endpoint: "cgi-bin/message/custom/send",
      query: { access_token: accessToken },
      body,
      network: params.account.network,
    });
  } catch (err) {
    if ((err as { errcode?: number }).errcode === 40001) {
      params.tokenHandle.invalidate();
      const refreshed = await params.tokenHandle.getAccessToken({ forceRefresh: true });
      await jsonRequest({
        method: "POST",
        endpoint: "cgi-bin/message/custom/send",
        query: { access_token: refreshed },
        body,
        network: params.account.network,
      });
      return;
    }
    throw err;
  }
}

export async function sendCustomerServiceTyping(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  touser: string;
  command?: "Typing" | "CancelTyping";
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/message/custom/typing",
    query: { access_token: accessToken },
    body: { touser: params.touser, command: params.command ?? "Typing" },
    network: params.account.network,
  });
}
