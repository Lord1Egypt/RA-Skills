"""OK.com 登录检测与登录操作"""

from __future__ import annotations

import logging
import re
import time

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound, OKNotLoggedIn, OKTimeout
from .human import medium_delay, short_delay

logger = logging.getLogger("ok-login")


# ─── 登录状态检测 ─────────────────────────────────────────


def check_login(
    bridge: BaseClient,
    subdomain: str | None = None,
) -> dict:
    """检查登录状态

    Args:
        bridge: 浏览器客户端
        subdomain: 目标站点子域名（如 "au"、"sg"）。
                   传入时先导航到该站点首页再检测，不传则检测当前页面。

    Returns:
        {"logged_in": bool, "user_name": str | None, "subdomain": str | None}
    """
    if subdomain:
        from .urls import build_base_url

        current = bridge.get_url() or ""
        if f"{subdomain}.ok.com" not in current:
            target = build_base_url(subdomain, "en")
            bridge.navigate(target)
            bridge.wait_dom_stable(timeout=10000)

    has_avatar = bridge.has_element(sel.USER_AVATAR)
    user_name = None

    if has_avatar:
        user_name = bridge.get_element_text(sel.USER_NAME)

    result = {
        "logged_in": has_avatar,
        "user_name": user_name,
        "subdomain": subdomain,
    }

    site = f" ({subdomain}.ok.com)" if subdomain else ""
    if has_avatar:
        logger.info("已登录%s: %s", site, user_name or "(未获取到用户名)")
    else:
        logger.info("未登录%s", site)

    return result


def require_login(bridge: BaseClient) -> dict:
    """要求登录状态，未登录则抛出异常"""
    status = check_login(bridge)
    if not status["logged_in"]:
        raise OKNotLoggedIn("未登录，请先在浏览器中登录 ok.com")
    return status


# ─── 登录弹窗操作 ─────────────────────────────────────────


def _click_login_entry_js() -> str:
    """在页面内查找并点击「登录 / 注册」入口，返回结果说明（用于日志）。"""
    return """
    (() => {
      const tryClick = (el) => {
        if (!el) return false;
        el.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
        if (typeof el.click === 'function') el.click();
        return true;
      };
      let el = document.querySelector("#pcUserInfoArea [class*='PcUserInfo_loginButton']");
      if (tryClick(el)) return "pc-nested";
      el = document.querySelector("[class*='PcUserInfo_loginButton']");
      if (tryClick(el)) return "pc-class-anywhere";
      const texts = ["Log in / Register", "Log In / Register", "登录", "Login"];
      const nodes = document.querySelectorAll("a, button, div, span");
      for (const n of nodes) {
        const t = (n.textContent || "").trim();
        if (!t || t.length > 40) continue;
        if (texts.some((x) => t === x || t.toLowerCase() === x.toLowerCase())) {
          let cur = n;
          for (let i = 0; i < 6 && cur; i++) {
            const cls = cur.className && cur.className.toString ? cur.className.toString() : "";
            if (cls.includes("login") || cls.includes("Login") || cur.tagName === "BUTTON" || cur.tagName === "A") {
              if (tryClick(cur)) return "text-walk:" + t.slice(0, 20);
              break;
            }
            cur = cur.parentElement;
          }
          if (tryClick(n)) return "text-direct:" + t.slice(0, 20);
        }
      }
      return "";
    })()
    """


def _open_login_modal(bridge: BaseClient) -> None:
    """点击 'Log in / Register' 按钮打开登录弹窗"""
    # 不使用 wait_for_selector（Bridge 对长时间 Promise 可能卡住）；用短轮询 + 点击兜底

    deadline = time.monotonic() + 12
    while time.monotonic() < deadline:
        if bridge.has_element(sel.LOGIN_TRIGGER) or bridge.has_element(sel.LOGIN_TRIGGER_ANY):
            break
        time.sleep(0.35)
    else:
        logger.warning("未在超时内看到 PcUserInfo_loginButton，尝试全页文本匹配")

    if bridge.has_element(sel.LOGIN_TRIGGER):
        bridge.click_element(sel.LOGIN_TRIGGER)
    elif bridge.has_element(sel.LOGIN_TRIGGER_ANY):
        bridge.click_element(sel.LOGIN_TRIGGER_ANY)
    else:
        via = bridge.evaluate(_click_login_entry_js())
        if not via:
            diag = bridge.evaluate("""
            (() => {
              const w = window.innerWidth || 0;
              const hasPc = !!document.querySelector("#pcUserInfoArea");
              const hasClass = !!document.querySelector("[class*='PcUserInfo_loginButton']");
              return "innerWidth=" + w + ", pcUserInfoArea=" + hasPc
                + ", PcUserInfo_loginButton=" + hasClass
                + ", path=" + (window.location.pathname || "");
            })()
            """)
            logger.warning("登录入口诊断: %s", diag)
            raise OKElementNotFound(
                "找不到登录入口。若为窄窗口或开启了移动设备模拟，请拉宽浏览器窗口或关闭 Device Toolbar 后重试。"
                f" 诊断: {diag}"
            )
        logger.info("已通过 JS 兜底点击登录入口: %s", via)

    short_delay()

    deadline = time.monotonic() + 12
    while time.monotonic() < deadline:
        if bridge.has_element(sel.LOGIN_MODAL):
            return
        time.sleep(0.3)

    raise OKTimeout("登录弹窗未出现")


def _close_login_modal(bridge: BaseClient) -> None:
    """关闭登录弹窗"""
    if bridge.has_element(sel.LOGIN_MODAL_CLOSE):
        bridge.click_element(sel.LOGIN_MODAL_CLOSE)
        short_delay()


def _dismiss_cookie_banner(bridge: BaseClient) -> None:
    """关闭 Cookie 横幅（如果存在）"""
    if bridge.has_element(sel.COOKIE_ACCEPT_BTN):
        bridge.click_element(sel.COOKIE_ACCEPT_BTN)
        short_delay()


def _fill_email(bridge: BaseClient, email: str) -> None:
    """在登录弹窗中填入邮箱（严格限定在 modal 内）。"""
    bridge.wait_for_selector(sel.LOGIN_MODAL, timeout=10000)

    value = bridge.evaluate(f"""
    (() => {{
        const modal = document.querySelector("{sel.LOGIN_MODAL}");
        if (!modal) return null;

        let input = modal.querySelector("{sel.LOGIN_EMAIL_INPUT}");
        if (!input) {{
            input = modal.querySelector("input[type='email'], input[type='text'], input[type='tel']");
        }}
        if (!input) return null;

        input.focus();
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        setter.call(input, '');
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        setter.call(input, '{email}');
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        input.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles: true, key: 'a' }}));
        input.blur();
        return input.value || '';
    }})()
    """)

    if not value:
        raise OKElementNotFound("邮箱输入框未找到或输入失败")

    short_delay()


def _click_continue(bridge: BaseClient) -> None:
    """点击 Continue 按钮（兼容不同 class 命名）。"""
    # 先尝试原始选择器
    if bridge.has_element(sel.LOGIN_CONTINUE_BTN):
        bridge.click_element(sel.LOGIN_CONTINUE_BTN)
        medium_delay()
        short_delay()
        return

    # 兜底：在登录弹窗内按按钮文案/属性查找
    clicked = bridge.evaluate("""
    (() => {
      const modal = document.querySelector("[class*='LoginPC_loginContainer']") || document;
      const btns = modal.querySelectorAll("button");
      for (const b of btns) {
        const t = (b.textContent || "").trim().toLowerCase();
        const aria = (b.getAttribute("aria-label") || "").trim().toLowerCase();
        if (["continue", "next", "继续"].includes(t) || ["continue", "next", "继续"].includes(aria)) {
          if (!b.disabled) {
            b.click();
            return true;
          }
        }
      }

      // 最后兜底：找 form 内第一个可点 submit/button
      const form = modal.querySelector("form");
      if (form) {
        let b = form.querySelector("button[type='submit']");
        if (!b) b = form.querySelector("button");
        if (b && !b.disabled) {
          b.click();
          return true;
        }
      }
      return false;
    })()
    """)
    if not clicked:
        raise OKElementNotFound("找不到 Continue 按钮")

    # 某些页面点击后过渡较慢，适度延长等待
    medium_delay()
    short_delay()


def _dump_modal_diagnostics(bridge: BaseClient) -> str:
    """导出当前登录弹窗的结构摘要，便于定位分支卡点。"""
    diag = bridge.evaluate("""
    (() => {
      const modal = document.querySelector("[class*='LoginPC_loginContainer']");
      if (!modal) return "modal-missing";

      const titleNodes = modal.querySelectorAll("span, div, h1, h2, h3");
      const titles = [];
      for (const el of titleNodes) {
        const t = (el.textContent || "").trim();
        if (t && t.length <= 80) titles.push(t);
        if (titles.length >= 8) break;
      }

      const inputs = [];
      for (const el of modal.querySelectorAll("input")) {
        inputs.push({
          type: el.type || "",
          placeholder: el.placeholder || "",
          value: el.value || "",
        });
      }

      const buttons = [];
      for (const el of modal.querySelectorAll("button")) {
        buttons.push({
          text: (el.textContent || "").trim(),
          disabled: !!el.disabled,
          cls: (el.className || "").toString().slice(0, 120),
        });
      }

      return JSON.stringify({ titles, inputs, buttons });
    })()
    """)
    return diag or "diag-empty"


def _wait_for_password_page(bridge: BaseClient, timeout: float = 10) -> str:
    """等待下一步页面出现，返回 ``login`` / ``register`` / ``verify_code``。"""
    deadline = time.monotonic() + timeout
    last_diag = ""
    while time.monotonic() < deadline:
        page_type = bridge.evaluate("""
        (() => {
            const modal = document.querySelector("[class*='LoginPC_loginContainer']");
            if (!modal) return '';

            const shortTexts = Array.from(modal.querySelectorAll('span, div, h1, h2, h3, p'))
              .map((el) => (el.textContent || '').trim().toLowerCase())
              .filter(Boolean)
              .slice(0, 30);
            const joined = shortTexts.join(' ');

            if (joined.includes('verification code') || joined.includes('enter code') || joined.includes('resend')) {
                return 'verify_code:Verification code';
            }

            const welcomeTitle = modal.querySelector("[class*='WelcomeTip_welcomeTitle']");
            if (welcomeTitle) {
                const raw = (welcomeTitle.textContent || '').trim();
                const text = raw.toLowerCase();
                if (text.includes('new friend') || text.includes('new') || text.includes('create')) {
                    return 'register:' + raw;
                }
                return 'login:' + raw;
            }
            const registerTitle = modal.querySelector("[class*='ValidAccount_title']");
            if (registerTitle) {
                const raw = (registerTitle.textContent || '').trim();
                const text = raw.toLowerCase();
                if (text.includes('friend') || text.includes('new') || text.includes('create')) {
                    return 'register:' + raw;
                }
            }
            const pwdInput = modal.querySelector("input[type='password']");
            if (pwdInput) return 'login:(password input found)';
            return '';
        })()
        """)
        if page_type:
            if page_type.startswith("verify_code:"):
                logger.info("检测到验证码页面: %s", page_type[12:])
                return "verify_code"
            if page_type.startswith("register:"):
                logger.info("检测到注册页面: %s", page_type[9:])
                return "register"
            if page_type.startswith("login:"):
                logger.info("检测到登录页面: %s", page_type[6:])
                return "login"
        last_diag = _dump_modal_diagnostics(bridge)
        time.sleep(0.3)

    logger.warning("密码页诊断: %s", last_diag)
    raise OKTimeout(f"密码输入页面未出现。诊断: {last_diag}")


def _fill_password_and_submit(bridge: BaseClient, password: str) -> None:
    """在密码页面填入密码并点击提交按钮

    已注册用户登录页和新用户注册页的 DOM 结构不同：
    - 登录页: input[type='password'] with CustomCounterInput class
    - 注册页: .ok_login_input_label_content_input (第二个)
    统一使用 input[type='password'] 定位，兼容两种情况。
    """
    escaped = password.replace("\\", "\\\\").replace("'", "\\'")

    bridge.evaluate(f"""
    (() => {{
        const modal = document.querySelector("[class*='LoginPC_loginContainer']");
        if (!modal) return;
        // 优先找 type=password 的输入框（兼容登录和注册）
        let input = modal.querySelector("input[type='password']");
        if (!input) {{
            // fallback: 找所有文本输入框中的最后一个
            const inputs = modal.querySelectorAll("input");
            input = inputs[inputs.length - 1];
        }}
        if (!input) return;
        input.focus();
        const setter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value'
        ).set;
        setter.call(input, '');
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        setter.call(input, '{escaped}');
        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
    }})()
    """)
    short_delay()

    # 等待按钮变为可点击状态
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        clicked = bridge.evaluate("""
        (() => {
            const modal = document.querySelector("[class*='LoginPC_loginContainer']");
            if (!modal) return false;
            // 优先找 LoginPC_continueButton（已注册用户的 Log in 按钮）
            let btn = modal.querySelector("[class*='LoginPC_continueButton']");
            if (!btn) {
                // fallback: ValidAccount_loginBtn（注册页的 Register 按钮）
                btn = modal.querySelector("[class*='ValidAccount_loginBtn']");
            }
            if (!btn) {
                // 最后兜底：找按钮文字
                const btns = modal.querySelectorAll("button");
                for (const b of btns) {
                    const t = b.textContent.trim().toLowerCase();
                    if (['log in','login','sign in','register'].includes(t)) { btn = b; break; }
                }
            }
            if (btn && !btn.disabled) { btn.click(); return true; }
            return false;
        })()
        """)
        if clicked:
            break
        time.sleep(0.3)

    medium_delay()


def _wait_for_login_success(bridge: BaseClient, timeout: float = 30) -> bool:
    """等待登录成功（弹窗消失 + 头像出现）"""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        modal_exists = bridge.has_element(sel.LOGIN_MODAL)
        if not modal_exists:
            short_delay()
            has_avatar = bridge.has_element(sel.USER_AVATAR)
            if has_avatar:
                logger.info("登录成功")
                return True
            # 弹窗关闭但还没检测到头像，再等一下
        time.sleep(0.5)

    return False


def _get_login_error(bridge: BaseClient) -> str | None:
    """获取登录错误信息"""
    err = bridge.evaluate("""
    (() => {
        const selectors = [
            "[class*='errorMsg']", "[class*='error-msg']",
            "[class*='ErrorTip']", "[class*='errTip']",
            "[class*='LoginPC_loginContainer'] [class*='error']",
        ];
        for (const s of selectors) {
            const el = document.querySelector(s);
            if (el && el.textContent.trim()) return el.textContent.trim();
        }
        return null;
    })()
    """)
    return err


def _infer_subdomain_from_url(url: str | None) -> str | None:
    if not url:
        return None
    m = re.search(r"https?://([a-z]+)\.ok\.com", url)
    if not m:
        return None
    return m.group(1).lower()


def _probe_target_url_for_subdomain(subdomain: str) -> str:
    """为探测固定子域构建稳定城市页 URL。"""
    sub = subdomain.lower()
    if sub == "ae":
        return "https://ae.ok.com/en/city-dubai/"
    if sub == "uk":
        return "https://uk.ok.com/en/city-london/"
    if sub == "au":
        return "https://au.ok.com/en/city-canberra/"
    return f"https://{sub}.ok.com/en/"


def _probe_email_on_current_site(
    bridge: BaseClient,
    email: str,
    keep_modal_open: bool = False,
) -> str:
    """在当前站点只探测邮箱分支，不提交密码。

    Returns:
        "login" | "register"
    """
    _dismiss_cookie_banner(bridge)
    _open_login_modal(bridge)
    _fill_email(bridge, email)
    _click_continue(bridge)
    branch = _wait_for_password_page(bridge)
    if not keep_modal_open:
        _close_login_modal(bridge)
    return branch


def _probe_email_across_sites(
    bridge: BaseClient,
    email: str,
    probe_subdomains: list[str],
) -> list[dict]:
    """跨站点探测邮箱归属（仅探测，不提交密码）。"""
    results: list[dict] = []
    for sub in probe_subdomains:
        sub = (sub or "").strip().lower()
        if not sub:
            continue
        target = _probe_target_url_for_subdomain(sub)
        try:
            bridge.navigate(target)
            bridge.wait_dom_stable(timeout=10000, interval=500)
            branch = _probe_email_on_current_site(bridge, email, keep_modal_open=True)
            results.append({"subdomain": sub, "branch": branch, "url": target})
            logger.info("跨站点探测: %s -> %s", sub, branch)
            if branch == "login":
                break
            _close_login_modal(bridge)
        except Exception as e:
            results.append({"subdomain": sub, "branch": "unknown", "error": str(e), "url": target})
            logger.warning("跨站点探测失败: %s -> %s", sub, e)

    return results


# ─── 对外暴露的登录函数 ─────────────────────────────────────


def login_with_email(
    bridge: BaseClient,
    email: str,
    password: str,
    probe_subdomains: list[str] | None = None,
) -> dict:
    """通过邮箱密码登录 OK.com。

    当当前站点把邮箱判定为注册页时，可自动在指定子域（默认 ae/uk/au）做无密码探测，
    找到登录页后自动切换并继续登录。
    """
    # 等待页面 DOM 稳定（确保 React 完成 hydration）
    bridge.wait_dom_stable(timeout=10000, interval=500)
    logger.info("页面 DOM 已稳定")

    # 关闭可能存在的 Cookie 横幅
    _dismiss_cookie_banner(bridge)

    # 如果已登录，直接返回
    status = check_login(bridge)
    if status["logged_in"]:
        return {
            "logged_in": True,
            "account_type": "existing",
            "message": f"已登录: {status['user_name'] or '(未知用户)'}",
        }

    original_url = bridge.get_url() or ""
    original_subdomain = _infer_subdomain_from_url(original_url)

    # 先在当前站点探测邮箱分支（保留弹窗，若为登录页可直接输密码）
    account_type = _probe_email_on_current_site(bridge, email, keep_modal_open=True)
    logger.info("当前站点账号类型: %s", account_type)

    probe_results: list[dict] = []

    # 命中注册分支时的处理
    if account_type == "register":
        subs = probe_subdomains if probe_subdomains is not None else ["ae", "uk", "au"]

        if not subs:
            # 明确指定了目标站点（probe_subdomains=[]），不做跨站探测
            return {
                "logged_in": False,
                "account_type": "register",
                "message": f"该邮箱在 {original_subdomain}.ok.com 未注册",
                "site_hint": {
                    "current_subdomain": original_subdomain,
                    "probes": [],
                },
            }

        probe_results = _probe_email_across_sites(bridge, email, subs)

        login_hit = next((r for r in probe_results if r.get("branch") == "login"), None)
        verify_hit = next((r for r in probe_results if r.get("branch") == "verify_code"), None)

        if login_hit:
            account_type = "login"
            logger.info("已自动切换到 %s 继续登录", login_hit.get("subdomain"))
        elif verify_hit:
            account_type = "verify_code"
            logger.info("已自动切换到 %s，命中验证码登录分支", verify_hit.get("subdomain"))
            return {
                "logged_in": False,
                "account_type": "verify_code",
                "message": "当前账号进入邮箱验证码登录流程，请输入验证码后继续",
                "site_hint": {
                    "current_subdomain": _infer_subdomain_from_url(bridge.get_url()),
                    "probes": probe_results,
                },
            }
        else:
            msg = "该邮箱在 ae/uk/au 均被判定为新账号，请确认是否需要先注册"
            return {
                "logged_in": False,
                "account_type": "register",
                "message": msg,
                "site_hint": {
                    "current_subdomain": original_subdomain,
                    "probes": probe_results,
                },
            }

    if account_type == "verify_code":
        return {
            "logged_in": False,
            "account_type": "verify_code",
            "message": "当前账号进入邮箱验证码登录流程，请输入验证码后继续",
            "site_hint": {
                "current_subdomain": _infer_subdomain_from_url(bridge.get_url()),
                "probes": probe_results,
            },
        }

    # 进入密码登录流程（当前页面应已是目标站点）
    _fill_password_and_submit(bridge, password)
    logger.info("已输入密码并提交")

    # 检查是否有错误
    err = _get_login_error(bridge)
    if err:
        logger.warning("登录出错: %s", err)
        return {
            "logged_in": False,
            "account_type": account_type,
            "message": f"登录失败: {err}",
            "site_hint": {
                "current_subdomain": _infer_subdomain_from_url(bridge.get_url()),
                "probes": probe_results,
            },
        }

    # 等待登录成功
    success = _wait_for_login_success(bridge, timeout=30)

    if success:
        final_status = check_login(bridge)
        current_sub = _infer_subdomain_from_url(bridge.get_url())
        switched = bool(original_subdomain and current_sub and original_subdomain != current_sub)
        return {
            "logged_in": True,
            "account_type": account_type,
            "user_name": final_status.get("user_name"),
            "message": "登录成功",
            "site_hint": {
                "original_subdomain": original_subdomain,
                "current_subdomain": current_sub,
                "auto_switched": switched,
                "probes": probe_results,
            },
        }

    # 再次检查错误
    err = _get_login_error(bridge)
    return {
        "logged_in": False,
        "account_type": account_type,
        "message": f"登录超时{': ' + err if err else ''}",
        "site_hint": {
            "current_subdomain": _infer_subdomain_from_url(bridge.get_url()),
            "probes": probe_results,
        },
    }


def wait_for_login(bridge: BaseClient, timeout: float = 120) -> dict:
    """等待用户手动完成登录（用于 OAuth 等场景）

    Agent 引导用户在浏览器中手动操作（如点击 Google 登录），
    此函数轮询检测登录状态直到成功或超时。

    Returns:
        {"logged_in": bool, "message": str}
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        has_avatar = bridge.has_element(sel.USER_AVATAR)
        modal_exists = bridge.has_element(sel.LOGIN_MODAL)

        if has_avatar and not modal_exists:
            user_name = bridge.get_element_text(sel.USER_NAME)
            return {
                "logged_in": True,
                "user_name": user_name,
                "message": "登录成功",
            }
        time.sleep(1)

    return {
        "logged_in": False,
        "message": "等待登录超时",
    }
