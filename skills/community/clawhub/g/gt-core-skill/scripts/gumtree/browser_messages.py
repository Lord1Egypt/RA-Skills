from __future__ import annotations

import json
import time
from typing import Any

from .bridge import BridgePage
from .browser_auth import _extract_login_status_from_current_page
from .browser_urls import build_messages_url
from .errors import BrowserAutomationError

_CLICK_DETAIL_MESSAGE_BUTTON_JS = """
(() => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const candidates = Array.from(document.querySelectorAll(
    'button[data-q="contact-email"], .seller-contact__button-group button, button'
  ));
  const button = candidates.find((node) => {
    if (!(node instanceof HTMLButtonElement)) {
      return false;
    }
    const text = normalizeText(node.textContent).toLowerCase();
    return node.getAttribute("data-q") === "contact-email" || text === "message";
  });
  if (!button) {
    throw new Error("详情页未找到 Message 按钮");
  }
  if (button.disabled) {
    throw new Error("详情页 Message 按钮不可点击");
  }
  button.click();
  return JSON.stringify({
    ok: true,
    button_text: normalizeText(button.textContent),
    button_data_q: button.getAttribute("data-q"),
  });
})()
"""

_EXTRACT_MESSAGES_API_JS = """
(async () => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const optionalString = (value) => {
    const text = normalizeText(value);
    return text || null;
  };
  const optionalBoolean = (value) => {
    if (typeof value !== "boolean") {
      return null;
    }
    return value;
  };
  const optionalFiniteNumber = (value) => {
    if (typeof value !== "number" || !Number.isFinite(value)) {
      return null;
    }
    return value;
  };

  const url = new URL(window.location.href);
  const selectedConversationId = url.searchParams.get("conversationId");
  const response = await fetch("/bff-api/message-centre/conversations", {
    method: "GET",
    credentials: "include",
    headers: {
      "Accept": "application/json",
    },
  });

  if (response.status === 401 || response.status === 403) {
    return JSON.stringify({
      source: "message-centre-api",
      auth_required: true,
      status_code: response.status,
      ok: false,
      error: `message-centre API 返回未授权状态 ${response.status}`,
    });
  }
  if (!response.ok) {
    return JSON.stringify({
      source: "message-centre-api",
      auth_required: null,
      status_code: response.status,
      ok: false,
      error: `message-centre API 返回异常状态 ${response.status}`,
    });
  }

  const payload = await response.json();
  const rawConversations = Array.isArray(payload?.conversations) ? payload.conversations : [];
  const conversations = rawConversations.map((item) => {
    const messages = Array.isArray(item?.messages) ? item.messages : [];
    const lastMessage = messages.length ? messages[messages.length - 1] : null;
    return {
      conversation_id: optionalString(item?.id),
      ad_id: optionalFiniteNumber(item?.adId),
      seller_id: optionalFiniteNumber(item?.sellerId),
      buyer_id: optionalFiniteNumber(item?.buyerId),
      created_at: optionalString(item?.createdAt),
      updated_at: optionalString(item?.updatedAt),
      unread_messages_count: optionalFiniteNumber(item?.unreadMessagesCount),
      is_blocked: optionalBoolean(item?.isBlocked),
      title: null,
      preview: optionalString(lastMessage?.text),
      last_activity: optionalString(lastMessage?.createdAt) || optionalString(item?.updatedAt),
      is_selected: optionalString(item?.id) === selectedConversationId,
      thread_messages: messages.map((message) => ({
        id: optionalString(message?.id),
        text: optionalString(message?.text),
        created_at: optionalString(message?.createdAt),
        updated_at: optionalString(message?.updatedAt),
        user_role: optionalString(message?.userRole),
        user_id: optionalFiniteNumber(message?.userId),
        attachments: Array.isArray(message?.attachments) ? message.attachments : [],
      })),
    };
  });

  const selectedConversation =
    conversations.find((item) => item.is_selected) ||
    conversations[0] ||
    null;

  return JSON.stringify({
    source: "message-centre-api",
    auth_required: false,
    status_code: response.status,
    ok: true,
    meta: {
      current_url: window.location.href,
      selected_conversation_id: selectedConversationId,
      open_chat: url.searchParams.get("openChat") === "true",
    },
    conversation_count: conversations.length,
    conversations: conversations.map((item) => ({
      conversation_id: item.conversation_id,
      ad_id: item.ad_id,
      seller_id: item.seller_id,
      buyer_id: item.buyer_id,
      created_at: item.created_at,
      updated_at: item.updated_at,
      unread_messages_count: item.unread_messages_count,
      is_blocked: item.is_blocked,
      title: item.title,
      preview: item.preview,
      last_activity: item.last_activity,
      is_selected: item.is_selected,
      thread_messages: item.thread_messages,
      thread_message_count: item.thread_messages.length,
    })),
    selected_conversation: selectedConversation ? {
      conversation_id: selectedConversation.conversation_id,
      ad_id: selectedConversation.ad_id,
      seller_id: selectedConversation.seller_id,
      buyer_id: selectedConversation.buyer_id,
      counterpart_name: null,
      listing_title: null,
      listing_price: null,
      listing_location: null,
      is_blocked: selectedConversation.is_blocked,
      unread_messages_count: selectedConversation.unread_messages_count,
      thread_messages: selectedConversation.thread_messages,
      thread_message_count: selectedConversation.thread_messages.length,
      composer: null,
    } : {
      conversation_id: selectedConversationId,
      counterpart_name: null,
      listing_title: null,
      listing_price: null,
      listing_location: null,
      is_blocked: null,
      unread_messages_count: null,
      thread_messages: [],
      thread_message_count: 0,
      composer: null,
    },
  });
})()
"""

_EXTRACT_MESSAGES_PAGE_JS = """
(() => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const optionalString = (value) => {
    const text = normalizeText(value);
    return text || null;
  };
  const optionalBoolean = (value) => {
    if (typeof value !== "boolean") {
      return null;
    }
    return value;
  };
  const toAbsoluteUrl = (value) => {
    const text = normalizeText(value);
    if (!text) {
      return null;
    }
    try {
      return new URL(text, window.location.origin).toString();
    } catch {
      return null;
    }
  };
  const toConversationId = (value) => {
    const url = toAbsoluteUrl(value);
    if (!url) {
      return null;
    }
    try {
      return new URL(url).searchParams.get("conversationId");
    } catch {
      return null;
    }
  };
  const isVisible = (el) => {
    if (!(el instanceof HTMLElement)) return false;
    if (el.hidden) return false;
    const style = window.getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return false;
    return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length);
  };
  const collectLeafTexts = (root) => {
    if (!(root instanceof HTMLElement)) {
      return [];
    }
    const nodes = Array.from(root.querySelectorAll("div, p, span, a, button, li, h1, h2, h3, h4"));
    const texts = [];
    for (const node of nodes) {
      if (!(node instanceof HTMLElement) || !isVisible(node)) {
        continue;
      }
      const text = normalizeText(node.textContent);
      if (!text) {
        continue;
      }
      const childText = Array.from(node.children)
        .map((child) => normalizeText(child.textContent))
        .filter(Boolean)
        .join(" ");
      if (childText && childText === text) {
        continue;
      }
      texts.push(text);
    }
    return texts;
  };
  const queryText = (root, selector) => {
    if (!(root instanceof Element)) {
      return null;
    }
    const node = root.querySelector(selector);
    return optionalString(node?.textContent);
  };
  const isTimeText = (text) => {
    return /^(today|yesterday|mon|tue|wed|thu|fri|sat|sun)\\b/i.test(text)
      || /^\\d{1,2}:\\d{2}(?:\\s?[ap]m)?$/i.test(text)
      || /^\\d{1,2}(?:st|nd|rd|th)?\\s+[a-z]+$/i.test(text);
  };
  const controlTexts = new Set([
    "Hide",
    "More options",
    "Delete conversation",
    "Upload Image",
    "Make an offer",
  ]);
  const isNoiseText = (text) => {
    if (!text) {
      return true;
    }
    if (controlTexts.has(text)) {
      return true;
    }
    if (/^(block|report)\\b/i.test(text)) {
      return true;
    }
    return false;
  };
  const textarea = document.querySelector('textarea#message-field, textarea[name="message-field"]');
  const submitButton = document.querySelector('button[data-q="message-centre-submit"][aria-label="send"], button[data-q="message-centre-submit"]');
  const composeForm = textarea ? textarea.closest("form") : null;
  let conversationPanel = composeForm ? composeForm.parentElement : null;
  for (let i = 0; conversationPanel && i < 6; i += 1) {
    if (
      conversationPanel.querySelector?.('button[data-q="message-centre-submit"]')
      && /more options/i.test(normalizeText(conversationPanel.textContent))
    ) {
      break;
    }
    conversationPanel = conversationPanel.parentElement;
  }

  const url = new URL(window.location.href);
  const selectedConversationId = url.searchParams.get("conversationId");

  const dataLayerEntries = Array.isArray(window.dataLayer) ? window.dataLayer : [];
  const loadMessagesEvent = dataLayerEntries.find(
    (entry) => entry && typeof entry === "object" && entry.name === "LoadMessagesEvent"
  ) || null;
  const gumtreeDataLayer = Array.isArray(window.gumtreeDataLayer) ? window.gumtreeDataLayer : [];
  const pageDeclaration = gumtreeDataLayer.find(
    (entry) => entry && typeof entry === "object" && entry.event === "pageDeclaration"
  ) || null;

  const conversationAnchors = Array.from(document.querySelectorAll('a[data-q="conversation-link"]'));
  const conversations = conversationAnchors.map((anchor) => {
    const href = anchor.getAttribute("href");
    const conversationId = toConversationId(href);
    const title = queryText(anchor, "h6") || queryText(anchor, '[class*="e15e95g53"]');
    const preview = queryText(anchor, 'p[class*="e15e95g52"]');
    const lastActivity = queryText(anchor, 'p[class*="e15e95g51"]');
    const adState = queryText(anchor, '[class*="e15e95g55"]');
    return {
      conversation_id: conversationId,
      url: toAbsoluteUrl(href),
      title,
      preview,
      last_activity: lastActivity,
      ad_state: adState,
      is_selected: conversationId != null && conversationId === selectedConversationId,
      raw_text: normalizeText(anchor.textContent),
    };
  });

  const counterpartName =
    queryText(conversationPanel, '.css-1i61i7z')
    || queryText(conversationPanel, '[class*="ee7da151"]')
    || null;
  const listingCard =
    conversationPanel?.querySelector('.css-z0xpcq.ec8s6h31')
    || conversationPanel?.querySelector('[class*="ec8s6h31"]')
    || document.querySelector('.css-z0xpcq.ec8s6h31')
    || document.querySelector('[class*="ec8s6h31"]')
    || null;
  const listingTitle =
    queryText(listingCard, '.css-1a7pxff')
    || queryText(listingCard, '[class*="ec8s6h36"]')
    || null;
  const listingPrice =
    queryText(listingCard, '.css-f8asvg')
    || queryText(listingCard, '[class*="eiwoz5f1"]')
    || null;
  const listingLocation =
    queryText(listingCard, '.css-3e1s6r')
    || queryText(listingCard, '[class*="ec8s6h32"]')
    || null;

  const messageNodes = conversationPanel
    ? Array.from(conversationPanel.querySelectorAll('div[id].css-1l95blj, div[id][class*="e1b1ybr611"]'))
    : [];
  const threadMessages = messageNodes.map((node) => ({
    id: optionalString(node.getAttribute("id")),
    text:
      queryText(node, '.css-uqea2t')
      || queryText(node, '[class*="e1b1ybr610"]')
      || null,
    timestamp:
      queryText(node, '[data-testid="timestamp"]')
      || queryText(node, '.css-1gbzq6y')
      || null,
  })).filter((item) => item.text);

  const inferredSelectedConversation = (
    conversations.find((item) => item.is_selected) ||
    (counterpartName
      ? conversations.find((item) => item.title === counterpartName)
      : null) ||
    conversations[0] ||
    null
  );
  const resolvedSelectedConversationId =
    selectedConversationId || inferredSelectedConversation?.conversation_id || null;
  const normalizedConversations = conversations.map((item) => ({
    ...item,
    is_selected: item.conversation_id != null && item.conversation_id === resolvedSelectedConversationId,
  }));

  return JSON.stringify({
    source: "strict-message-centre",
    meta: {
      current_url: window.location.href,
      page_type: optionalString(loadMessagesEvent?.p?.t) || optionalString(pageDeclaration?.page?.legacyType),
      platform: optionalString(loadMessagesEvent?.p?.pl),
      logged_in: optionalBoolean(pageDeclaration?.legacy?.loggedIn),
      selected_conversation_id: resolvedSelectedConversationId,
      open_chat: url.searchParams.get("openChat") === "true",
    },
    conversation_count: conversations.length,
    conversations: normalizedConversations,
    selected_conversation: {
      conversation_id: resolvedSelectedConversationId,
      counterpart_name: counterpartName,
      listing_title: listingTitle,
      listing_price: listingPrice,
      listing_location: listingLocation,
      thread_messages: threadMessages,
      thread_message_count: threadMessages.length,
      composer: {
        can_send: Boolean(textarea && submitButton),
        message_placeholder: optionalString(textarea?.getAttribute("placeholder")),
        draft_length: textarea instanceof HTMLTextAreaElement ? textarea.value.length : null,
      },
    },
  });
})()
"""

_SEND_MESSAGE_JS = """
((messageText) => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const text = normalizeText(messageText);
  if (!text) {
    throw new Error("消息内容不能为空");
  }
  const textarea = document.querySelector('textarea#message-field, textarea[name="message-field"]');
  if (!(textarea instanceof HTMLTextAreaElement)) {
    throw new Error("未找到消息输入框");
  }
  const button = document.querySelector('button[data-q="message-centre-submit"][aria-label="send"], button[data-q="message-centre-submit"]');
  if (!(button instanceof HTMLButtonElement)) {
    throw new Error("未找到发送按钮");
  }
  const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value")?.set;
  if (!setter) {
    throw new Error("无法设置消息输入框内容");
  }
  textarea.focus();
  setter.call(textarea, text);
  textarea.dispatchEvent(new Event("input", { bubbles: true }));
  textarea.dispatchEvent(new Event("change", { bubbles: true }));
  textarea.dispatchEvent(new KeyboardEvent("keydown", { key: "H", bubbles: true }));
  textarea.dispatchEvent(new KeyboardEvent("keyup", { key: "H", bubbles: true }));
  if (button.disabled) {
    throw new Error("填写消息后发送按钮仍然不可用");
  }
  button.click();
  return JSON.stringify({
    ok: true,
    message: text,
    button_disabled_before_click: button.disabled,
  });
})
"""

_MESSAGE_CENTRE_READY_JS = """
(() => {
  return window.location.pathname.includes("/manage/messages")
    && !!document.querySelector('textarea#message-field, textarea[name="message-field"]');
})()
"""


def _evaluate_json(page: BridgePage, expression: str) -> dict[str, Any]:
    raw = page.evaluate(expression)
    if not raw:
        raise BrowserAutomationError("浏览器返回了空结果")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("浏览器结果格式异常")
    return payload


def _extract_messages_dom_state(page: BridgePage) -> dict[str, Any]:
    payload = _evaluate_json(page, _EXTRACT_MESSAGES_PAGE_JS)
    if not isinstance(payload.get("meta"), dict):
        raise BrowserAutomationError("站内消息页元信息格式异常")
    if not isinstance(payload.get("selected_conversation"), dict):
        raise BrowserAutomationError("站内消息页会话信息格式异常")
    return payload


def _extract_messages_state(page: BridgePage) -> dict[str, Any]:
    api_error: str | None = None
    try:
        payload = _evaluate_json(page, _EXTRACT_MESSAGES_API_JS)
        if payload.get("ok") is True:
            if not isinstance(payload.get("meta"), dict):
                raise BrowserAutomationError("站内消息 API 元信息格式异常")
            if not isinstance(payload.get("selected_conversation"), dict):
                raise BrowserAutomationError("站内消息 API 会话信息格式异常")
            try:
                dom_payload = _extract_messages_dom_state(page)
            except BrowserAutomationError:
                dom_payload = None
            if isinstance(dom_payload, dict):
                payload["dom_source"] = dom_payload.get("source")
                payload["meta"] = {
                    **dom_payload.get("meta", {}),
                    **payload.get("meta", {}),
                }
                payload_conversations = payload.get("conversations")
                dom_selected_conversation = dom_payload.get("selected_conversation", {})
                dom_meta = dom_payload.get("meta", {})
                resolved_selected_conversation_id = None
                if isinstance(dom_selected_conversation, dict):
                    resolved_selected_conversation_id = dom_selected_conversation.get("conversation_id")
                if not resolved_selected_conversation_id and isinstance(dom_meta, dict):
                    resolved_selected_conversation_id = dom_meta.get("selected_conversation_id")

                selected_conversation = payload.get("selected_conversation", {})
                if (
                    resolved_selected_conversation_id
                    and isinstance(payload_conversations, list)
                ):
                    matched_api_conversation = next(
                        (
                            item for item in payload_conversations
                            if isinstance(item, dict) and item.get("conversation_id") == resolved_selected_conversation_id
                        ),
                        None,
                    )
                    if isinstance(matched_api_conversation, dict):
                        selected_conversation = {
                            **selected_conversation,
                            **matched_api_conversation,
                            "conversation_id": resolved_selected_conversation_id,
                        }
                dom_selected_conversation = dom_payload.get("selected_conversation", {})
                if isinstance(selected_conversation, dict) and isinstance(dom_selected_conversation, dict):
                    payload["selected_conversation"] = {
                        **selected_conversation,
                        "counterpart_name": (
                            selected_conversation.get("counterpart_name")
                            or dom_selected_conversation.get("counterpart_name")
                        ),
                        "listing_title": dom_selected_conversation.get("listing_title"),
                        "listing_price": dom_selected_conversation.get("listing_price"),
                        "listing_location": dom_selected_conversation.get("listing_location"),
                        "thread_messages": dom_selected_conversation.get("thread_messages") or selected_conversation.get("thread_messages"),
                        "thread_message_count": dom_selected_conversation.get("thread_message_count") or selected_conversation.get("thread_message_count"),
                        "composer": dom_selected_conversation.get("composer"),
                    }
                dom_conversations = dom_payload.get("conversations")
                api_conversations = payload.get("conversations")
                if isinstance(dom_conversations, list) and isinstance(api_conversations, list):
                    dom_by_id = {
                        item.get("conversation_id"): item
                        for item in dom_conversations
                        if isinstance(item, dict) and item.get("conversation_id")
                    }
                    merged_conversations = []
                    for item in api_conversations:
                        if not isinstance(item, dict):
                            merged_conversations.append(item)
                            continue
                        dom_item = dom_by_id.get(item.get("conversation_id"), {})
                        if not isinstance(dom_item, dict):
                            dom_item = {}
                        merged_conversations.append({
                            **item,
                            "title": item.get("title") or dom_item.get("title"),
                            "preview": item.get("preview") or dom_item.get("preview"),
                            "last_activity": item.get("last_activity") or dom_item.get("last_activity"),
                            "ad_state": item.get("ad_state") or dom_item.get("ad_state"),
                            "is_selected": (
                                item.get("conversation_id") == resolved_selected_conversation_id
                                if resolved_selected_conversation_id
                                else bool(item.get("is_selected") or dom_item.get("is_selected"))
                            ),
                            "thread_messages": item.get("thread_messages"),
                            "thread_message_count": item.get("thread_message_count"),
                        })
                    payload["conversations"] = merged_conversations
            return payload
        api_error = str(payload.get("error") or "message-centre API 返回失败")
        if payload.get("auth_required") is True:
            raise BrowserAutomationError("当前未登录 Gumtree，无法访问站内消息 API")
    except BrowserAutomationError:
        raise
    except Exception as exc:
        api_error = str(exc)

    payload = _extract_messages_dom_state(page)
    payload["source"] = f"{payload.get('source', 'strict-message-centre')}-dom-fallback"
    if api_error:
        payload["api_fallback_reason"] = api_error
    return payload


def _wait_for_expression(page: BridgePage, expression: str, timeout: float, interval: float, message: str) -> Any:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = page.evaluate(expression)
        if result:
            return result
        time.sleep(interval)
    raise BrowserAutomationError(message)


def _wait_until_message_sent(
    page: BridgePage,
    message: str,
    before_count: int,
) -> dict[str, Any]:
    deadline = time.time() + 20
    latest_state: dict[str, Any] | None = None
    normalized_message = " ".join(message.split())
    while time.time() < deadline:
        time.sleep(1)
        page.wait_dom_stable(timeout=5000)
        latest_state = _extract_messages_state(page)
        selected_conversation = latest_state.get("selected_conversation", {})
        if not isinstance(selected_conversation, dict):
            continue
        thread_messages = selected_conversation.get("thread_messages", [])
        if not isinstance(thread_messages, list):
            continue
        latest_text = None
        if thread_messages:
            last_message = thread_messages[-1]
            if isinstance(last_message, dict):
                latest_text = last_message.get("text")
        message_count = selected_conversation.get("thread_message_count")
        if isinstance(message_count, int) and message_count > before_count:
            return latest_state
        if isinstance(latest_text, str) and " ".join(latest_text.split()) == normalized_message:
            return latest_state
        composer = selected_conversation.get("composer")
        if isinstance(composer, dict) and composer.get("draft_length") == 0:
            return latest_state

    raise BrowserAutomationError(
        f"发送消息后未确认成功，最后状态: {json.dumps(latest_state, ensure_ascii=False)}"
    )


def _build_readable_messages_result(state: dict[str, Any], detail_url: str | None = None) -> dict[str, Any]:
    meta = state.get("meta", {})
    if not isinstance(meta, dict):
        meta = {}

    raw_conversations = state.get("conversations", [])
    selected_conversation = state.get("selected_conversation", {})
    if not isinstance(selected_conversation, dict):
        selected_conversation = {}

    raw_thread_messages = selected_conversation.get("thread_messages", [])
    thread_messages: list[dict[str, Any]] = []
    if isinstance(raw_thread_messages, list):
        for message in raw_thread_messages:
            if not isinstance(message, dict):
                continue
            thread_messages.append({
                "message_id": message.get("id"),
                "text": message.get("text"),
                "time": message.get("timestamp") or message.get("created_at"),
                "updated_at": message.get("updated_at"),
                "sender": {
                    "role": message.get("user_role"),
                    "user_id": message.get("user_id"),
                },
                # "attachments": message.get("attachments") if isinstance(message.get("attachments"), list) else [],
            })

    composer = selected_conversation.get("composer", {})
    if not isinstance(composer, dict):
        composer = {}

    selected_conversation_id = selected_conversation.get("conversation_id") or meta.get("selected_conversation_id")
    selected_conversation_id = selected_conversation_id if isinstance(selected_conversation_id, str) else None

    selected_thread_messages = thread_messages

    readable_conversations: list[dict[str, Any]] = []
    if isinstance(raw_conversations, list):
        for item in raw_conversations:
            if not isinstance(item, dict):
                continue
            conversation_id = item.get("conversation_id")
            is_current = bool(
                (selected_conversation_id and conversation_id == selected_conversation_id)
                or item.get("is_selected")
            )
            raw_item_messages = item.get("thread_messages", [])
            item_messages: list[dict[str, Any]] = []
            if isinstance(raw_item_messages, list):
                for message in raw_item_messages:
                    if not isinstance(message, dict):
                        continue
                    item_messages.append({
                        "message_id": message.get("id"),
                        "text": message.get("text"),
                        "time": message.get("timestamp") or message.get("created_at"),
                        "updated_at": message.get("updated_at"),
                        "sender": {
                            "role": message.get("user_role"),
                            "user_id": message.get("user_id"),
                        },
                        # "attachments": message.get("attachments") if isinstance(message.get("attachments"), list) else [],
                    })
            if is_current and selected_thread_messages:
                item_messages = selected_thread_messages
            readable_conversations.append({
                "conversation_id": conversation_id,
                "display_name": item.get("title"),
                "is_current": is_current,
                "latest_message": item.get("preview"),
                "latest_time": item.get("last_activity"),
                "ad_status": item.get("ad_state"),
                "listing_info": {
                    "title": selected_conversation.get("listing_title") if is_current else None,
                    "price": selected_conversation.get("listing_price") if is_current else None,
                    "location": selected_conversation.get("listing_location") if is_current else None,
                },
                "message_count": item.get("thread_message_count") if item.get("thread_message_count") is not None else len(item_messages),
                "messages": item_messages,
                # "composer_info": {
                #     "can_send": composer.get("can_send") if is_current else None,
                #     "placeholder": composer.get("message_placeholder") if is_current else None,
                # },
            })

    result = {
        "ok": True,
        "mode": "browser",
        "source": state.get("source"),
        "meta": {
            "current_url": meta.get("current_url"),
            "api_fallback_reason": state.get("api_fallback_reason"),
        },
        "conversation_count": state.get("conversation_count"),
        "conversations": readable_conversations,
        "sent_message": state.get("sent_message"),
    }
    if detail_url is not None:
        result["detail_url"] = detail_url
    return result


def _send_message_if_requested(page: BridgePage, message: str | None) -> dict[str, Any]:
    state = _extract_messages_state(page)
    if not message:
        return state

    selected_conversation = state.get("selected_conversation", {})
    if not isinstance(selected_conversation, dict):
        raise BrowserAutomationError("站内消息页会话信息格式异常")
    composer = selected_conversation.get("composer", {})
    if not isinstance(composer, dict) or composer.get("can_send") is not True:
        raise BrowserAutomationError("当前会话没有可用的消息输入框或发送按钮")

    thread_message_count = selected_conversation.get("thread_message_count")
    before_count = thread_message_count if isinstance(thread_message_count, int) else 0
    _evaluate_json(page, f"{_SEND_MESSAGE_JS}({json.dumps(message, ensure_ascii=False)})")
    final_state = _wait_until_message_sent(page=page, message=message, before_count=before_count)
    final_state["sent_message"] = {
        "attempted": True,
        "content": " ".join(message.split()),
    }
    return final_state


def run_browser_messages(
    page: BridgePage,
    conversation_id: str | None = None,
    message: str | None = None,
) -> dict[str, Any]:
    page.navigate(build_messages_url(conversation_id=conversation_id, open_chat=conversation_id is not None))
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    state = _send_message_if_requested(page=page, message=message)
    meta = state.get("meta", {})
    if isinstance(meta, dict) and meta.get("logged_in") is False:
        raise BrowserAutomationError("当前未登录 Gumtree，无法访问站内消息页")
    return _build_readable_messages_result(state)


def run_browser_detail_message(
    page: BridgePage,
    detail_url: str,
    message: str | None = None,
) -> dict[str, Any]:
    page.navigate(detail_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    login_status = _extract_login_status_from_current_page(page)
    if login_status.get("logged_in") is not True:
        raise BrowserAutomationError("当前未登录 Gumtree，无法从详情页进入站内消息")

    _evaluate_json(page, _CLICK_DETAIL_MESSAGE_BUTTON_JS)
    _wait_for_expression(
        page,
        _MESSAGE_CENTRE_READY_JS,
        timeout=20,
        interval=1,
        message="点击详情页 Message 后未进入站内交流页",
    )
    page.wait_dom_stable(timeout=15000)

    state = _send_message_if_requested(page=page, message=message)
    return _build_readable_messages_result(state, detail_url=detail_url)
