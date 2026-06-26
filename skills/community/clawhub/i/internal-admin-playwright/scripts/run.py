#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from getpass import getpass
from pathlib import Path
from urllib.parse import urlparse

import yaml
from playwright.sync_api import sync_playwright

from whitelist import enforce_route
from command_router import resolve_command, CommandNotFound


def _load_dotenv(skill_root: Path) -> None:
    env_file = skill_root / "references" / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if key and key not in os.environ:
            os.environ[key] = val



def _get_proxy_config() -> dict | None:
    """从环境变量读取代理配置，Playwright 会将所有流量走此代理。"""
    http_proxy = os.getenv("HTTP_PROXY") or os.getenv("HTTPS_PROXY")
    if not http_proxy:
        return None
    # Playwright proxy 需要 server URL + 可选 username/password
    server = http_proxy.rstrip("/")
    return {"server": server}

def load_whitelist(skill_root: Path) -> tuple[list[str], list[str], dict[str, str]]:
    p = skill_root / "references" / "whitelist.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return (
        data.get("allowed_hosts", []) or [],
        data.get("allowed_host_suffixes", []) or [],
        data.get("host_overrides", {}) or {},
    )


def run_vpn_check(skill_root: Path) -> None:
    script = skill_root / "scripts" / "vpn_check.py"
    subprocess.run([sys.executable, str(script)], check=True)


def maybe_auto_vpn(skill_root: Path, action: str) -> None:
    if os.getenv("AUTO_VPN", "0") != "1":
        return
    script = skill_root / "scripts" / "vpn_l2tp.py"
    subprocess.run([sys.executable, str(script), action], check=True)


def _collect_login_diagnostics(page):
    info = {}
    info["url"] = page.url
    candidates = [
        ".layui-layer-content",
        ".layui-form-mid",
        ".layui-form-danger",
        ".error",
        ".alert",
        ".msg",
        "body",
    ]
    errors = []
    for sel in candidates:
        try:
            loc = page.locator(sel)
            n = min(loc.count(), 5)
            for i in range(n):
                txt = (loc.nth(i).inner_text(timeout=500) or "").strip()
                if not txt:
                    continue
                if any(k in txt for k in ["错误", "失败", "验证码", "无效", "请", "不正确", "登录"]):
                    errors.append(txt)
        except Exception:
            pass
    dedup = []
    for e in errors:
        if e not in dedup:
            dedup.append(e)
    info["hints"] = dedup[:10]
    return info


def login(page, base_url: str, username: str, password: str):
    user_sel = os.getenv("LOGIN_USER_SELECTOR", 'input[name="username"], input[name="user_name"], input[type="text"], input[placeholder*="账号"], input[placeholder*="用户名"], input[id*="user"]')
    pass_sel = os.getenv("LOGIN_PASS_SELECTOR", 'input[name="password"], input[type="password"], input[placeholder*="密码"], input[id*="pass"]')
    code_sel = os.getenv("LOGIN_CODE_SELECTOR", 'input[name="card_num"], input[placeholder*="标识码"], input[placeholder*="验证码"]')
    submit_sel = os.getenv("LOGIN_SUBMIT_SELECTOR", 'button[lay-filter="LAY-user-login-submit"], button:has-text("登 入"), button:has-text("登录"), button:has-text("Sign in"), button[type="submit"], input[type="submit"]')

    resp = page.goto(base_url, wait_until="domcontentloaded")
    if resp and resp.status == 503:
        page.wait_for_timeout(1500)
        page.goto(base_url, wait_until="domcontentloaded")
    page.wait_for_timeout(1200)

    login_code = (os.getenv("GOOGLE_OTP") or "").strip()

    try:
        page.locator(user_sel).first.fill(username, timeout=8000, force=True)
        page.locator(pass_sel).first.fill(password, timeout=8000, force=True)
        if login_code and page.locator(code_sel).count() > 0:
            page.locator(code_sel).first.fill(login_code, timeout=8000, force=True)
        page.locator(submit_sel).first.click(timeout=8000, force=True)
        return
    except Exception:
        pass

    for fr in page.frames:
        if fr == page.main_frame:
            continue
        try:
            fr.locator(user_sel).first.fill(username, timeout=3000, force=True)
            fr.locator(pass_sel).first.fill(password, timeout=3000, force=True)
            if login_code and fr.locator(code_sel).count() > 0:
                fr.locator(code_sel).first.fill(login_code, timeout=3000, force=True)
            fr.locator(submit_sel).first.click(timeout=3000, force=True)
            return
        except Exception:
            continue

    raise RuntimeError("未找到登录输入框，请提供登录页截图或HTML")


def goto_by_command(page, base_url: str, action: dict):
    if action.get("url"):
        page.goto(action["url"], wait_until="domcontentloaded")

    for label in action.get("clicks", []):
        clicked = False
        candidates = [
            page.get_by_text(label, exact=True).first,
            page.get_by_text(label).first,
            page.locator(f'a:has-text("{label}")').first,
            page.locator(f'.J_menuItem:has-text("{label}")').first,
            page.locator(f'li:has-text("{label}")').first,
        ]
        for loc in candidates:
            try:
                loc.click(timeout=5000, force=True)
                clicked = True
                page.wait_for_timeout(500)
                break
            except Exception:
                continue
        if not clicked:
            diag = _collect_login_diagnostics(page)
            raise RuntimeError(f"菜单点击失败: {label}; page={diag}")

    check_text = action.get("assert_text")
    if check_text:
        try:
            page.get_by_text(check_text).first.wait_for(timeout=10000)
        except Exception:
            if check_text not in page.content():
                raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", required=True, help='例: "进入评论管理->视频评论"')
    parser.add_argument("--otp", default="", help="动态验证码（标识码），也可用 GOOGLE_OTP 环境变量传入")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]

    # 自动加载 references/.env（不覆盖已有环境变量）
    _load_dotenv(skill_root)
    # --otp 参数优先级最高，直接覆盖环境变量
    if args.otp:
        os.environ["GOOGLE_OTP"] = args.otp.strip()

    base_url = os.getenv("LOGIN_URL", "https://staff.bluemv.net/d.php")
    username = os.getenv("STAFF_USERNAME", "").strip() or input("请输入后台账号: ").strip()
    password = os.getenv("STAFF_PASSWORD", "").strip() or getpass("请输入后台密码(输入不回显): ").strip()
    if not username or not password:
        raise SystemExit("账号或密码为空，已终止")

    maybe_auto_vpn(skill_root, "up")
    run_vpn_check(skill_root)

    allowed_hosts, allowed_suffixes, host_overrides = load_whitelist(skill_root)

    try:
        action = resolve_command(skill_root, args.command)
    except CommandNotFound as e:
        raise SystemExit(str(e))

    # 提前获取 OTP（从参数或环境变量），若没有则稍后在页面加载后再问
    _otp_preset = (args.otp or os.getenv("GOOGLE_OTP") or "").strip()

    headless = os.getenv("HEADLESS", "1") != "0"
    slow_mo = int(os.getenv("SLOW_MO_MS", "0"))
    force_ipv4 = os.getenv("FORCE_IPV4", "1") != "0"

    with sync_playwright() as p:
        launch_args = []
        if force_ipv4:
            launch_args += ["--disable-ipv6", "--disable-quic"]

        rules = []
        for host, ip in host_overrides.items():
            if host and ip:
                rules.append(f"MAP {host} {ip}")
        if rules:
            launch_args += [f"--host-resolver-rules={','.join(rules)},EXCLUDE localhost"]

        browser = p.chromium.launch(headless=headless, slow_mo=slow_mo, args=launch_args)

        debug_dir = skill_root / "debug"
        debug_dir.mkdir(exist_ok=True)
        state_file = debug_dir / "auth_state.json"

        ctx_kwargs = {"ignore_https_errors": True}

        # 注入代理配置（走 Clash Verge 本地代理）
        proxy_cfg = _get_proxy_config()
        if proxy_cfg and os.getenv("PROXY_BYPASS") != "1":
            ctx_kwargs["proxy"] = proxy_cfg

        # 不再复用旧登录态，避免脏 cookie 干扰
        # if state_file.exists():
        #     ctx_kwargs["storage_state"] = str(state_file)
        context = browser.new_context(**ctx_kwargs)
        # 白名单只拦截 document 导航，静态资源全放行（在 whitelist.py 中已处理）
        context.route("**/*", lambda route: enforce_route(route, allowed_hosts, allowed_suffixes))
        page = context.new_page()

        try:
            page.goto(base_url, wait_until="domcontentloaded")
            # 等待 JS 跳转完成（未登录时会被 JS 重定向到登录页）
            page.wait_for_timeout(3000)
            print(f"[DEBUG] goto后URL: {page.url}")
            # 用 URL 或 DOM 判断是否需要登录
            login_needed = (
                "code=login" in page.url
                or "mod=login" in page.url
                or page.locator('input[name="username"]').count() > 0
                or page.locator('input[name="card_num"]').count() > 0
            )
            print(f"[DEBUG] login_needed={login_needed}")
            if login_needed:
                # 浏览器已就位，现在获取验证码
                otp = _otp_preset or input("请输入动态验证码: ").strip()
                os.environ["GOOGLE_OTP"] = otp
                print(f"[DEBUG] OTP={otp} username={username} base_url={base_url}")
                print(f"[DEBUG] 登录前URL: {page.url}")
                login(page, base_url, username, password)
                print(f"[DEBUG] 点击登录后，等待跳转...")
                # 等待跳转，最多15秒
                for i in range(30):
                    page.wait_for_timeout(500)
                    cur = page.url
                    print(f"[DEBUG] {i*0.5:.1f}s URL={cur}")
                    if "code=login" not in cur:
                        print(f"[DEBUG] 已跳出登录页！")
                        break
                page.wait_for_timeout(3000)
            else:
                print(f"[DEBUG] 已有登录态，跳过登录")
                page.wait_for_timeout(1000)

            print(f"[DEBUG] 最终URL: {page.url}")
            print(f"[DEBUG] 页面标题: {page.title()}")

            # 确认已离开登录页
            if "code=login" in page.url:
                raise RuntimeError(f"登录后仍在登录页。URL: {page.url}")

            # 等待菜单渲染
            wait_ms = action.get("wait_after_login", 2000)
            page.wait_for_timeout(wait_ms)
            goto_by_command(page, base_url, action)
            print(f"执行完成: {args.command}")
        except Exception as e:
            debug_dir = skill_root / "debug"
            debug_dir.mkdir(exist_ok=True)
            try:
                page.screenshot(path=str(debug_dir / "last_error.png"), full_page=True)
            except Exception:
                pass
            html_dump = ""
            for _ in range(3):
                try:
                    html_dump = page.content()
                    break
                except Exception:
                    page.wait_for_timeout(300)
            try:
                (debug_dir / "last_error.html").write_text(html_dump, encoding="utf-8")
            except Exception:
                pass
            raise SystemExit(f"执行失败: {e}；已输出调试文件到 {debug_dir}")
        finally:
            context.close()
            browser.close()
            maybe_auto_vpn(skill_root, "down")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
