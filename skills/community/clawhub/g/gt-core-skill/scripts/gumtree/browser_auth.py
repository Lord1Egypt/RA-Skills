from __future__ import annotations

import json
import time
from typing import Any

from .bridge import BridgePage
from .browser_urls import build_home_url
from .errors import BrowserAutomationError

_EXTRACT_LOGIN_STATUS_JS = """
(() => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const toBoolOrNull = (value) => typeof value === "boolean" ? value : null;
  const toStringOrNull = (value) => {
    const text = normalizeText(value);
    return text || null;
  };
  const toNumberOrNull = (value) => {
    if (typeof value === "number" && Number.isFinite(value)) {
      return value;
    }
    return null;
  };
  const toObjectOrNull = (value) => {
    return value && typeof value === "object" && !Array.isArray(value) ? value : null;
  };
  const containsText = (needle) => {
    const matcher = needle.toLowerCase();
    const nodes = Array.from(document.querySelectorAll("a, button, span, div"));
    return nodes.some((node) => normalizeText(node.textContent).toLowerCase() === matcher);
  };
  const queryHref = (selector) => {
    const node = document.querySelector(selector);
    if (!node) {
      return null;
    }
    const href = toStringOrNull(node.getAttribute("href"));
    if (!href) {
      return null;
    }
    try {
      return new URL(href, window.location.origin).toString();
    } catch {
      return href;
    }
  };

  const analyticsConfig = window.__GUMTREE_ANALYTICS_CONFIG__ || null;
  const dataLayerEntries = Array.isArray(window.dataLayer) ? window.dataLayer : [];
  const initialDataLayer = dataLayerEntries.find(
    (entry) => entry && typeof entry === "object" && !Array.isArray(entry) && entry.name === "HomePageViewEvent"
  ) || null;
  const gumtreeDataLayer = Array.isArray(window.gumtreeDataLayer) ? window.gumtreeDataLayer : [];
  let clientData = null;
  if (typeof window.clientData === "string" && window.clientData) {
    try {
      clientData = JSON.parse(decodeURIComponent(window.clientData));
    } catch {
      clientData = null;
    }
  } else {
    clientData = toObjectOrNull(window.clientData);
  }
  const clientUserData = toObjectOrNull(clientData?.userData);
  const pageDeclaration = gumtreeDataLayer.find(
    (entry) => entry && typeof entry === "object" && !Array.isArray(entry) && entry.event === "pageDeclaration"
  ) || null;

  const signals = {
    analytics_islogin: toBoolOrNull(analyticsConfig?.islogin),
    analytics_user_id: toStringOrNull(analyticsConfig?.userId),
    initial_datalayer_logged_in: toBoolOrNull(initialDataLayer?.u?.li),
    gumtree_logged_in_status: toStringOrNull(pageDeclaration?.user?.loggedInStatus),
    legacy_logged_in: toBoolOrNull(pageDeclaration?.legacy?.loggedIn),
    gumtree_user_id: toNumberOrNull(pageDeclaration?.user?.userId),
    dom_manage_my_ads: containsText("Manage my Ads"),
    dom_my_orders: containsText("My Orders"),
    dom_favourites: containsText("Favourites"),
    dom_my_alerts: containsText("My Alerts"),
    dom_my_details: containsText("My Details"),
    dom_sign_up: containsText("Sign up"),
    dom_login: containsText("Login"),
  };
  const account = {
    id: toNumberOrNull(clientUserData?.id) ?? toNumberOrNull(pageDeclaration?.user?.userId),
    email: toStringOrNull(clientUserData?.email),
    first_name: toStringOrNull(clientUserData?.firstName),
    last_name: toStringOrNull(clientUserData?.lastName),
    full_name: toStringOrNull(
      [clientUserData?.firstName, clientUserData?.lastName].filter(Boolean).join(" ")
    ),
  };
  const menuLinks = {
    manage_my_ads: queryHref('[data-q="user-menu-link-manage-my-ads"]'),
    my_orders: queryHref('[data-q="user-menu-link-my-orders"]'),
    favourites: queryHref('[data-q="user-menu-link-favourites"]'),
    my_alerts: queryHref('[data-q="user-menu-link-my-alerts"]'),
    my_details: queryHref('[data-q="user-menu-link-my-details"]'),
  };

  let positiveScore = 0;
  let negativeScore = 0;
  const matchedSignals = [];

  const push = (name, outcome, weight, detail) => {
    matchedSignals.push({ name, outcome, weight, detail });
    if (outcome === "positive") {
      positiveScore += weight;
    } else if (outcome === "negative") {
      negativeScore += weight;
    }
  };

  if (signals.analytics_islogin === true) {
    push("analytics_islogin", "positive", 5, "window.__GUMTREE_ANALYTICS_CONFIG__.islogin === true");
  } else if (signals.analytics_islogin === false) {
    push("analytics_islogin", "negative", 5, "window.__GUMTREE_ANALYTICS_CONFIG__.islogin === false");
  }

  if (signals.analytics_user_id) {
    push("analytics_user_id", "positive", 3, "window.__GUMTREE_ANALYTICS_CONFIG__.userId 非空");
  } else if (signals.analytics_user_id === null && analyticsConfig && analyticsConfig.userId === "") {
    push("analytics_user_id", "negative", 3, "window.__GUMTREE_ANALYTICS_CONFIG__.userId 为空");
  }

  if (signals.initial_datalayer_logged_in === true) {
    push("initial_datalayer_logged_in", "positive", 4, "initialDataLayer.u.li === true");
  } else if (signals.initial_datalayer_logged_in === false) {
    push("initial_datalayer_logged_in", "negative", 4, "initialDataLayer.u.li === false");
  }

  if (signals.gumtree_logged_in_status === "logged in") {
    push("gumtree_logged_in_status", "positive", 4, "gumtreeDataLayer.user.loggedInStatus === 'logged in'");
  } else if (signals.gumtree_logged_in_status === "logged out") {
    push("gumtree_logged_in_status", "negative", 4, "gumtreeDataLayer.user.loggedInStatus === 'logged out'");
  }

  if (signals.legacy_logged_in === true) {
    push("legacy_logged_in", "positive", 3, "gumtreeDataLayer.legacy.loggedIn === true");
  } else if (signals.legacy_logged_in === false) {
    push("legacy_logged_in", "negative", 3, "gumtreeDataLayer.legacy.loggedIn === false");
  }

  if (signals.gumtree_user_id != null) {
    push("gumtree_user_id", "positive", 2, "gumtreeDataLayer.user.userId 非空");
  }

  const positiveDomSignals = [
    ["dom_manage_my_ads", signals.dom_manage_my_ads, "DOM 包含 Manage my Ads"],
    ["dom_my_orders", signals.dom_my_orders, "DOM 包含 My Orders"],
    ["dom_favourites", signals.dom_favourites, "DOM 包含 Favourites"],
    ["dom_my_alerts", signals.dom_my_alerts, "DOM 包含 My Alerts"],
    ["dom_my_details", signals.dom_my_details, "DOM 包含 My Details"],
  ];
  for (const [name, present, detail] of positiveDomSignals) {
    if (present) {
      push(name, "positive", 1, detail);
    }
  }

  const negativeDomSignals = [
    ["dom_sign_up", signals.dom_sign_up, "DOM 包含 Sign up"],
    ["dom_login", signals.dom_login, "DOM 包含 Login"],
  ];
  for (const [name, present, detail] of negativeDomSignals) {
    if (present) {
      push(name, "negative", 1, detail);
    }
  }

  let loggedIn = null;
  if (signals.analytics_islogin !== null) {
    loggedIn = signals.analytics_islogin;
  } else if (signals.initial_datalayer_logged_in !== null) {
    loggedIn = signals.initial_datalayer_logged_in;
  } else if (signals.gumtree_logged_in_status === "logged in") {
    loggedIn = true;
  } else if (signals.gumtree_logged_in_status === "logged out") {
    loggedIn = false;
  } else if (positiveScore !== negativeScore) {
    loggedIn = positiveScore > negativeScore;
  }

  const scoreDelta = Math.abs(positiveScore - negativeScore);
  let confidence = "low";
  if (signals.analytics_islogin !== null && signals.initial_datalayer_logged_in !== null) {
    confidence = "high";
  } else if (scoreDelta >= 4) {
    confidence = "medium";
  }
  if (signals.analytics_islogin === signals.initial_datalayer_logged_in && signals.analytics_islogin !== null) {
    confidence = "high";
  }

  return JSON.stringify({
    source: "gumtree-login-signals",
    logged_in: loggedIn,
    confidence,
    positive_score: positiveScore,
    negative_score: negativeScore,
    signals,
    matched_signals: matchedSignals,
    page_title: toStringOrNull(document.title),
    current_url: window.location.href,
    account,
    menu_links: menuLinks,
  });
})()
"""

_HAS_EMAIL_LOGIN_FORM_JS = """
(() => {
  return Boolean(
    document.querySelector('input[data-testid="input-username"]') &&
    document.querySelector('input[data-testid="input-password"]')
  );
})()
"""

_IS_LOGIN_SUBMIT_ENABLED_JS = """
(() => {
  const submitButton = document.querySelector('form[action="/bff-api/login/via-form"] button[type="submit"]');
  return Boolean(submitButton && !submitButton.disabled);
})()
"""

_OPEN_LOGIN_UI_JS = """
(() => {
  if (document.querySelector('input[data-testid="input-username"]')) {
    return JSON.stringify({ ok: true, state: "form_visible" });
  }
  const btn = document.querySelector('[data-q="hm-login"]');
  if (!btn) {
    throw new Error("Login button not found");
  }
  btn.click();
  return JSON.stringify({ ok: true, state: "login_opened" });
})()
"""

_CLICK_EMAIL_LOGIN_JS = """
(() => {
  if (document.querySelector('input[data-testid="input-username"]')) {
    return JSON.stringify({ ok: true, state: "form_visible" });
  }
  const btn = document.querySelector('[data-q="email-login"]');
  if (!btn) {
    throw new Error("Continue with email button not found");
  }
  btn.click();
  return JSON.stringify({ ok: true, state: "email_login_opened" });
})()
"""

_OPEN_USER_MENU_JS = """
(() => {
  const menuButton = document.querySelector('[data-q="user-menu-button"]');
  if (!menuButton) {
    throw new Error("User menu button not found");
  }
  const logoutForm = document.querySelector('form[data-testid="logout-form"]');
  if (logoutForm) {
    return JSON.stringify({ ok: true, state: "menu_visible" });
  }
  menuButton.click();
  return JSON.stringify({ ok: true, state: "menu_opened" });
})()
"""

_HAS_LOGOUT_FORM_JS = """
(() => {
  return Boolean(document.querySelector('form[data-testid="logout-form"] button[type="submit"]'));
})()
"""

_EXTRACT_LOGIN_ERROR_JS = """
(() => {
  const normalizeText = (value) => String(value ?? "").replace(/\\s+/g, " ").trim();
  const selectors = [
    '[role="alert"]',
    '[aria-live="assertive"]',
    '[aria-live="polite"]',
    '.form-element--error',
    '.error-message',
    '.notification-error',
    '[data-testid*="error"]',
  ];
  for (const selector of selectors) {
    const nodes = Array.from(document.querySelectorAll(selector));
    for (const node of nodes) {
      const text = normalizeText(node.textContent);
      if (text) {
        return text;
      }
    }
  }
  return null;
})()
"""


def _build_fill_login_form_js(username: str, password: str) -> str:
    return f"""
(() => {{
  const usernameValue = {json.dumps(username, ensure_ascii=False)};
  const passwordValue = {json.dumps(password, ensure_ascii=False)};
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype,
    "value"
  )?.set;
  const findInput = (selectors) => {{
    for (const selector of selectors) {{
      const input = document.querySelector(selector);
      if (input) {{
        return input;
      }}
    }}
    return null;
  }};
  const setInputValue = (selectors, value) => {{
    const input = findInput(selectors);
    if (!input) {{
      throw new Error(`Input not found: ${{selectors.join(", ")}}`);
    }}
    if (!nativeInputValueSetter) {{
      throw new Error("Native input value setter not available");
    }}
    input.focus();
    nativeInputValueSetter.call(input, "");
    input.dispatchEvent(new InputEvent("input", {{ bubbles: true, data: "", inputType: "deleteContentBackward" }}));
    nativeInputValueSetter.call(input, value);
    input.dispatchEvent(new InputEvent("input", {{ bubbles: true, data: value, inputType: "insertText" }}));
    input.dispatchEvent(new Event("change", {{ bubbles: true }}));
    input.dispatchEvent(new Event("blur", {{ bubbles: true }}));
    input.setAttribute("value", value);
    if (input.value !== value) {{
      nativeInputValueSetter.call(input, value);
    }}
    return input;
  }};

  const usernameInput = setInputValue(
    ['input[data-testid="input-username"]', '#username', 'input[name="username"]'],
    usernameValue
  );
  const passwordInput = setInputValue(
    ['input[data-testid="input-password"]', '#password', 'input[name="form.password"]', 'input.input-password'],
    passwordValue
  );

  const submitButton = document.querySelector('form[action="/bff-api/login/via-form"] button[type="submit"]');
  return JSON.stringify({{
    ok: true,
    username_filled: usernameInput.value === usernameValue,
    password_filled: passwordInput.value === passwordValue,
    username_length: usernameInput.value.length,
    password_length: passwordInput.value.length,
    submit_disabled: Boolean(submitButton?.disabled),
  }});
}})()
"""


_SUBMIT_EMAIL_LOGIN_JS = """
(() => {
  const form = document.querySelector('form[action="/bff-api/login/via-form"]');
  if (!form) {
    throw new Error("Email login form not found");
  }
  const submitButton = form.querySelector('button[type="submit"]');
  if (!submitButton) {
    throw new Error("Login submit button not found");
  }
  if (submitButton.disabled) {
    throw new Error("Login submit button is disabled");
  }
  submitButton.click();
  return JSON.stringify({ ok: true });
})()
"""

_SUBMIT_LOGOUT_JS = """
(() => {
  const form = document.querySelector('form[data-testid="logout-form"]');
  if (!form) {
    throw new Error("Logout form not found");
  }
  const submitButton = form.querySelector('button[type="submit"]');
  if (!submitButton) {
    throw new Error("Logout submit button not found");
  }
  submitButton.click();
  return JSON.stringify({ ok: true });
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


def _wait_for_expression(page: BridgePage, expression: str, timeout: float, interval: float, message: str) -> Any:
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = page.evaluate(expression)
        if result:
            return result
        time.sleep(interval)
    raise BrowserAutomationError(message)


def _extract_login_status_from_current_page(page: BridgePage) -> dict[str, Any]:
    raw = page.evaluate(_EXTRACT_LOGIN_STATUS_JS)
    if not raw:
        raise BrowserAutomationError("未能从 Gumtree 页面提取登录状态")

    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise BrowserAutomationError("登录状态结果格式异常")

    logged_in = payload.get("logged_in")
    if logged_in is not None and not isinstance(logged_in, bool):
        raise BrowserAutomationError("登录状态字段格式异常")

    result = {"ok": True, "logged_in": logged_in}

    if logged_in:
        account = payload.get("account")
        if not isinstance(account, dict):
            raise BrowserAutomationError("登录用户信息格式异常")
        menu_links = payload.get("menu_links")
        if not isinstance(menu_links, dict):
            raise BrowserAutomationError("登录菜单信息格式异常")
        result["account"] = account
        result["menu_links"] = menu_links

    return result


def run_browser_check_login(page: BridgePage) -> dict[str, Any]:
    home_url = build_home_url()
    page.navigate(home_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)
    return _extract_login_status_from_current_page(page)


def run_browser_login(page: BridgePage, username: str, password: str) -> dict[str, Any]:
    home_url = build_home_url()
    page.navigate(home_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    current_status = _extract_login_status_from_current_page(page)
    if current_status.get("logged_in") is True:
        current_status["already_logged_in"] = True
        return current_status

    page.evaluate(_OPEN_LOGIN_UI_JS)
    time.sleep(1)
    page.evaluate(_CLICK_EMAIL_LOGIN_JS)
    _wait_for_expression(
        page,
        _HAS_EMAIL_LOGIN_FORM_JS,
        timeout=10,
        interval=0.5,
        message="等待 Gumtree 邮箱登录表单出现超时",
    )

    fill_result = _evaluate_json(page, _build_fill_login_form_js(username=username, password=password))
    if fill_result.get("username_filled") is not True:
        raise BrowserAutomationError("登录表单未成功填入邮箱")
    if fill_result.get("password_filled") is not True:
        raise BrowserAutomationError("登录表单未成功填入密码")
    if fill_result.get("submit_disabled") is True:
        _wait_for_expression(
            page,
            _IS_LOGIN_SUBMIT_ENABLED_JS,
            timeout=5,
            interval=0.5,
            message="登录表单未就绪，提交按钮仍然不可用",
        )

    page.evaluate(_SUBMIT_EMAIL_LOGIN_JS)

    deadline = time.time() + 20
    while time.time() < deadline:
        time.sleep(1)
        page.wait_dom_stable(timeout=5000)

        error_text = page.evaluate(_EXTRACT_LOGIN_ERROR_JS)
        if isinstance(error_text, str) and error_text.strip():
            raise BrowserAutomationError(f"Gumtree 登录失败: {error_text.strip()}")

        current_status = _extract_login_status_from_current_page(page)
        if current_status.get("logged_in") is True:
            current_status["just_logged_in"] = True
            return current_status

    raise BrowserAutomationError("等待 Gumtree 登录完成超时，请检查账号密码或页面验证码/风控提示")


def run_browser_logout(page: BridgePage) -> dict[str, Any]:
    home_url = build_home_url()
    page.navigate(home_url)
    page.wait_for_load()
    page.wait_dom_stable(timeout=15000)

    current_status = _extract_login_status_from_current_page(page)
    if current_status.get("logged_in") is not True:
        return {"ok": True, "logged_in": False, "already_logged_out": True}

    page.evaluate(_OPEN_USER_MENU_JS)
    _wait_for_expression(
        page,
        _HAS_LOGOUT_FORM_JS,
        timeout=10,
        interval=0.5,
        message="等待 Gumtree 用户菜单中的退出表单出现超时",
    )
    page.evaluate(_SUBMIT_LOGOUT_JS)

    deadline = time.time() + 20
    while time.time() < deadline:
        time.sleep(1)
        page.wait_dom_stable(timeout=5000)
        current_status = _extract_login_status_from_current_page(page)
        if current_status.get("logged_in") is False:
            return {"ok": True, "logged_in": False, "just_logged_out": True}

    raise BrowserAutomationError("等待 Gumtree 退出登录完成超时")
