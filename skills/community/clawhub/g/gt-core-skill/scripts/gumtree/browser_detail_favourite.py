from __future__ import annotations

import json
import time
from typing import Any

from .bridge import BridgePage
from .browser_auth import _extract_login_status_from_current_page
from .errors import BrowserAutomationError

_EXTRACT_DETAIL_FAVOURITE_STATE_JS = """
(() => {
  const fail = (message) => {
    throw new Error(message);
  };
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
  const expectObject = (value, message) => {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      fail(message);
    }
    return value;
  };
  const decodeClientData = () => {
    const rawClientData = window.clientData;
    if (rawClientData == null) {
      fail("window.clientData 缺失");
    }
    if (typeof rawClientData === "string") {
      try {
        return JSON.parse(decodeURIComponent(rawClientData));
      } catch (error) {
        fail(`window.clientData 解析失败: ${error.message}`);
      }
    }
    if (typeof rawClientData === "object" && !Array.isArray(rawClientData)) {
      return rawClientData;
    }
    fail("window.clientData 格式异常");
  };
  const extractListingId = (clientData) => {
    const fromListingDetails = optionalFiniteNumber(clientData?.listingDetails?.id);
    if (fromListingDetails != null) {
      return String(fromListingDetails);
    }
    const path = optionalString(clientData?.request?.path) || window.location.pathname;
    const match = path.match(/\\/(\\d+)(?:[/?#]|$)/);
    return match ? match[1] : null;
  };

  const clientData = expectObject(decodeClientData(), "clientData 格式异常");
  const sellerActions = expectObject(clientData.sellerActions, "clientData.sellerActions 缺失");
  const savedAds = sellerActions.savedAds && typeof sellerActions.savedAds === "object" && !Array.isArray(sellerActions.savedAds)
    ? sellerActions.savedAds
    : {};
  const listingId = extractListingId(clientData);
  const favouriteButton = document.querySelector('button.favourite, button[data-q="empty-heart"], button[data-q="full-heart"], button[data-q="filled-heart"]');
  const favouriteIcon = favouriteButton?.querySelector(".icon");
  const buttonClass = optionalString(favouriteButton?.getAttribute("class"));
  const buttonDataQ = optionalString(favouriteButton?.getAttribute("data-q"));
  const iconClass = optionalString(favouriteIcon?.getAttribute("class"));
  const savedByDataLayer = listingId ? savedAds[listingId] === true : null;
  const savedByButtonClass = buttonClass ? buttonClass.includes("is-saved") : false;
  const savedByDataQ = buttonDataQ === "full-heart" || buttonDataQ === "filled-heart";
  const savedByIconClass = iconClass ? iconClass.includes("icon--color-pink") : false;
  const isSaved = savedByDataLayer === true || savedByButtonClass || savedByDataQ || savedByIconClass;

  return JSON.stringify({
    listing_id: listingId,
    title: optionalString(clientData?.listingDetails?.title),
    current_url: window.location.href,
    button_found: Boolean(favouriteButton),
    button_disabled: Boolean(favouriteButton?.disabled),
    button_class: buttonClass,
    button_data_q: buttonDataQ,
    button_text: optionalString(favouriteButton?.textContent),
    icon_class: iconClass,
    logged_in: optionalBoolean(clientData?.userData?.userLoggedIn),
    saved_by_data_layer: savedByDataLayer,
    saved_by_button_class: savedByButtonClass,
    saved_by_data_q: savedByDataQ,
    saved_by_icon_class: savedByIconClass,
    is_saved: isSaved,
  });
})()
"""

_CLICK_DETAIL_FAVOURITE_JS = """
(() => {
  const button = document.querySelector('button.favourite, button[data-q="empty-heart"], button[data-q="full-heart"], button[data-q="filled-heart"]');
  if (!button) {
    throw new Error("Favourite button not found");
  }
  if (button.disabled) {
    throw new Error("Favourite button is disabled");
  }
  button.click();
  return JSON.stringify({
    ok: true,
    button_text: String(button.textContent ?? "").replace(/\\s+/g, " ").trim(),
    button_data_q: button.getAttribute("data-q"),
  });
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


def run_browser_detail_favourite(
    page: BridgePage,
    detail_url: str,
) -> dict[str, Any]:
    page.navigate(detail_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    login_status = _extract_login_status_from_current_page(page)
    if login_status.get("logged_in") is not True:
        raise BrowserAutomationError("当前未登录 Gumtree，无法收藏详情页")

    before = _evaluate_json(page, _EXTRACT_DETAIL_FAVOURITE_STATE_JS)
    listing_id = before.get("listing_id")
    if not isinstance(listing_id, str) or not listing_id:
        raise BrowserAutomationError("未能识别当前详情页 listing_id")
    if before.get("button_found") is not True:
        raise BrowserAutomationError("详情页未找到 Favourite 按钮")
    if before.get("button_disabled") is True:
        raise BrowserAutomationError("详情页 Favourite 按钮不可点击")
    if before.get("is_saved") is True:
        return {
            "ok": True,
            "mode": "browser",
            "detail_url": detail_url,
            "listing_id": listing_id,
            "title": before.get("title"),
            "already_favourited": True,
            "just_favourited": False,
            "state": before,
        }

    _evaluate_json(page, _CLICK_DETAIL_FAVOURITE_JS)

    deadline = time.time() + 15
    latest_state = before
    while time.time() < deadline:
        time.sleep(1)
        page.wait_dom_stable(timeout=5000)
        latest_state = _evaluate_json(page, _EXTRACT_DETAIL_FAVOURITE_STATE_JS)
        if latest_state.get("is_saved") is True:
            return {
                "ok": True,
                "mode": "browser",
                "detail_url": detail_url,
                "listing_id": listing_id,
                "title": latest_state.get("title"),
                "already_favourited": False,
                "just_favourited": True,
                "state": latest_state,
            }

    raise BrowserAutomationError(
        f"点击 Favourite 后未确认收藏成功，最后状态: {json.dumps(latest_state, ensure_ascii=False)}"
    )
