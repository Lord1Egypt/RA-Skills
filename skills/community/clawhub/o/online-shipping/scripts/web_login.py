#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
web_login.py — 网页登录取 token（快递报价查询的登录前置）

为什么需要它：
  报价接口 `POST /ToDoorOrder/GetFreightPredictList` 走的是**网页侧鉴权**——
  请求头带 `auth: <userToken>`，这个 token 只存在于浏览器 localStorage 里，
  只能通过在网页上真实登录一次拿到。所以查报价前必须先登录。

登录页只有「用户名或邮箱 + 密码」两个字段，**没有**短信验证码和滑块
（验证码与滑块是注册页的）。所以给了账号密码就能全自动：填表 → 点登录 → 取 token。
没给账号时才退化成人工填写；若页面额外弹出验证码/滑块，脚本会继续等待人工完成。

用法：
  python web_login.py --username 138****1234 --password '***'   # 全自动登录（推荐）
  python web_login.py                                       # 已有 token 就复用，否则人工填
  python web_login.py --force                               # 忽略已有 token，重新登录
  python web_login.py --check                               # 只检查 token 是否存在
"""

import argparse
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    load_creds, update_creds, get_token, price_hint,
)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    # 只能在运行期标记为「不可用」，不能在导入期 sys.exit()。
    # 否则进程会裸退，客户看不到任何提示。
    sync_playwright = None
    PLAYWRIGHT_ERROR = "缺少依赖 Playwright"
else:
    PLAYWRIGHT_ERROR = ""

LOGIN_URL = "https://xdccy.com/login.html"

# Chrome 探测候选：环境变量 → PATH → 各系统通用安装路径。
# 不做任何硬编码的「某台开发机」路径，避免换机器即失效、也避免泄露用户名。
_CHROME_CANDIDATES = [
    os.environ.get("CHROME_PATH", ""),
    os.environ.get("CHROME_BIN", ""),
    shutil.which("chrome"),
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
    shutil.which("msedge"),
    shutil.which("microsoft-edge"),
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

# 页面内引导条（fixed 顶部，pointer-events:none 不挡点击）
#
# 合规约束：本条位于第三方页面之上，必须做成**中性、无品牌、无推广**的
# 操作提示条——不使用品牌色置顶条幅、不放大字号、不压任何标识、不引导跳转。
# 它只回答「这一步做什么」，不回答「去哪里找人」。
_BANNER_CSS = """
#xdcc_login_guide {
  position: fixed; top: 0; left: 0; right: 0; z-index: 2147483000;
  background: rgba(255,255,255,.94); color: #24292f;
  font-family: -apple-system,"Microsoft YaHei",sans-serif; font-size:12px; line-height:1.55;
  padding: 6px 14px; border-bottom: 1px solid #d8dee4; pointer-events: none;
}
#xdcc_login_guide b { color: #24292f; }
#xdcc_login_guide .step { margin: 1px 0; }
#xdcc_login_guide .now { background: #f0f3f6; border-radius: 4px; padding: 1px 6px; }
"""

_BANNER_HTML = """
<div id="xdcc_login_guide">
  <div class="step"><b>登录提示</b>（登录后才能查询快递报价，约 1 分钟）</div>
  <div class="step" id="g1">① 用户名 / 密码已由助手填好，请核对</div>
  <div class="step" id="g2"><span class="now">② 点「登录」即可；若弹出短信或滑块，手动完成一次</span></div>
  <div class="step" id="g4">③ 登录成功后本窗口会自动关闭</div>
  <div class="step" style="opacity:.8">遇阻请把控制台提示发回会话，助手会接着帮你处理。</div>
</div>
"""


def detect_chrome():
    """探测本机已安装的桌面浏览器。返回可执行文件路径或 None（此时用 Playwright 自带内核）。"""
    for c in _CHROME_CANDIDATES:
        if c and os.path.isfile(c):
            return c
    return None


def inject_banner(page):
    try:
        page.add_style_tag(content=_BANNER_CSS)
        page.evaluate(
            "(html) => { document.body.insertAdjacentHTML('afterbegin', html); }",
            _BANNER_HTML,
        )
    except Exception:
        pass  # 横幅只是辅助，失败不影响主流程


def set_banner_step(page, step_id, text):
    try:
        page.evaluate(
            "(args) => { const e=document.getElementById(args.id);"
            " if(e){e.innerHTML='<span class=\"now\">'+args.t+'</span>';} }",
            {"id": step_id, "t": text},
        )
    except Exception:
        pass


def autofill(page, username, password):
    """自动填用户名/密码。返回 (用户名已填?, 密码已填?)。

    定位策略：**ID 优先**。登录页字段 id 是稳定的 `usernameOrEmail` / `password`，
    而 placeholder 是「请输入用户名或邮箱」——早期版本按「手机号」去匹配 placeholder，
    实测匹配数为 0，导致用户名根本填不进去。placeholder 只作兜底。
    """
    u_ok = p_ok = False
    if username:
        for sel in ("#usernameOrEmail", "input[name='usernameOrEmail']"):
            try:
                page.fill(sel, username, timeout=2500)
                u_ok = True
                break
            except Exception:
                continue
        if not u_ok:
            for ph in ("用户名或邮箱", "用户名", "邮箱", "账号", "手机号", "手机号码", "手机"):
                try:
                    page.get_by_placeholder(ph, exact=False).first.fill(username, timeout=1500)
                    u_ok = True
                    break
                except Exception:
                    continue
    if password:
        for sel in ("#password", "input[name='password']", "input[type='password']"):
            try:
                page.fill(sel, password, timeout=2500)
                p_ok = True
                break
            except Exception:
                continue
        if not p_ok:
            for ph in ("密码",):
                try:
                    page.get_by_placeholder(ph, exact=False).first.fill(password, timeout=1500)
                    p_ok = True
                    break
                except Exception:
                    continue
    return u_ok, p_ok


def try_click_login(page):
    """尝试自动点「登录」。

    登录页本身**没有**短信验证码和滑块（只有用户名+密码），所以给了账号就能全自动。
    这里仍做成「尽力而为」：点不动就返回 False，交给客户手动点，不影响人工兜底。
    """
    for sel in ("button:has-text('登录')", "#loginBtn", "button.layui-btn",
                "a:has-text('登录')"):
        try:
            page.click(sel, timeout=2000)
            return True
        except Exception:
            continue
    return False


def wait_for_token(page, timeout):
    """轮询 localStorage.userToken，直到客户完成登录。"""
    print(f"\n[等待] 等待登录完成（若页面弹出验证码或滑块，请手动完成）"
          f"，最长等待 {timeout}s…")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            tok = page.evaluate("localStorage.getItem('userToken')")
        except Exception:
            tok = None
        if tok:
            return tok.strip()
        time.sleep(2)
    return None


def interactive_login(username=None, password=None, timeout=600,
                      creds_path=None, chrome_path=None, quiet=False):
    """拉起浏览器登录，取回 userToken 并落盘。返回 (token, err)。

    登录页只有「用户名或邮箱 + 密码」，**没有**短信验证码和滑块
    （验证码和滑块是注册页的）。所以只要给了账号密码，这里可以全自动完成：
    填表 → 点登录 → 轮询 token。缺账号密码时才退化成人工填写。
    """
    if sync_playwright is None:
        return None, (f"{PLAYWRIGHT_ERROR}。请先安装："
                      "pip install playwright && playwright install chromium")

    auto = bool(username and password)
    if not quiet:
        print("=" * 56)
        print("  小递查查 · 网页登录（查询快递报价需要）")
        print("=" * 56)
        if auto:
            print("已拿到账号密码，登录将自动完成，无需人工操作。")
        else:
            print("请在弹出的浏览器里填写「用户名或邮箱」与「密码」并点击登录。")
        print("（若页面额外弹出验证码/滑块，请手动完成，脚本会继续等待。）\n")

    with sync_playwright() as pw:
        launch_kwargs = {"headless": False}
        chrome = chrome_path or detect_chrome()
        if chrome:
            launch_kwargs["executable_path"] = chrome
        browser = pw.chromium.launch(**launch_kwargs)
        page = browser.new_page()
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        if not quiet:
            print(f"[已打开] {LOGIN_URL}")
        inject_banner(page)

        u_ok, p_ok = autofill(page, username, password)
        if auto:
            if u_ok and p_ok:
                print("[自动填表] 已填入账号与密码，正在自动登录…")
            else:
                print(f"[自动填表] 未完全填入（账号={u_ok} 密码={p_ok}），"
                      f"请在页面里补齐后手动点击登录。")
            if try_click_login(page):
                print("[自动登录] 已点击登录按钮，等待登录结果…")
            else:
                print("[自动登录] 未找到登录按钮，请在页面里手动点击。")

        token = wait_for_token(page, timeout)
        if not token:
            browser.close()
            return None, "等待超时，未取得登录凭证（userToken）。请确认账号密码是否正确。"
        set_banner_step(page, "g4", "✅ 已登录，正在保存…")
        browser.close()

    update_creds(creds_path, {"XDCC_USER_TOKEN": token})
    return token, None


def ensure_token(creds_path=None, username=None, password=None, timeout=600,
                 chrome_path=None, force=False, allow_interactive=True, quiet=False):
    """确保拿到可用的网页登录 token。

    优先复用凭据文件里已保存的 token；缺失或 --force 时才拉起浏览器登录。
    返回 (token, err)。
    """
    creds_path = creds_path or os.path.expanduser("~/.workbuddy/xdcc-credentials.env")
    if not force:
        token = get_token(load_creds(creds_path))
        if token:
            return token, None
    if not allow_interactive:
        return None, "没有可用的网页登录 token，且当前不允许交互式登录"
    return interactive_login(username, password, timeout, creds_path, chrome_path, quiet)


def main(argv=None):
    p = argparse.ArgumentParser(description="小递查查 网页登录取 token（快递报价查询前置）")
    # 登录页字段是「用户名或邮箱」；小递查查账号通常就是手机号，故两者等价
    p.add_argument("--phone", "--username", dest="username",
                   help="用户名 / 邮箱 / 手机号（自动填入，可留空手动填）")
    p.add_argument("--password", help="密码（自动填入，可留空手动填）")
    p.add_argument("--timeout", type=int, default=600, help="等待登录完成的秒数（默认600）")
    p.add_argument("--creds", default=os.path.expanduser("~/.workbuddy/xdcc-credentials.env"),
                   help="凭据文件路径（默认 ~/.workbuddy/xdcc-credentials.env）")
    p.add_argument("--chrome-path", default=None, help="Chrome 可执行文件路径（默认自动探测）")
    p.add_argument("--force", action="store_true", help="忽略已保存的 token，重新登录")
    p.add_argument("--check", action="store_true", help="只检查 token 是否存在，不拉起浏览器")
    p.add_argument("--quiet", action="store_true", help="静默模式（供其他脚本调用）")
    args = p.parse_args(argv)

    if args.check:
        token = get_token(load_creds(args.creds))
        if token:
            print(f"[已就绪] 登录 token 已存在（前8位：{token[:8]}…），可直接查询快递报价。")
            return 0
        print("[缺失] 尚未登录，需执行一次网页登录才能查询报价。", file=sys.stderr)
        print(price_hint("缺少网页登录 token"), file=sys.stderr)
        return 1

    token, err = ensure_token(args.creds, args.username, args.password,
                              args.timeout, args.chrome_path, args.force,
                              quiet=args.quiet)
    if err:
        print(f"\n[失败] {err}", file=sys.stderr)
        print("常见原因：未点「获取验证码」、短信码填错、滑块未通过、或网络不畅。", file=sys.stderr)
        print(price_hint(f"网页登录失败：{err}"), file=sys.stderr)
        return 1
    print(f"\n✅ 已登录并保存 token（前8位：{token[:8]}…）→ {args.creds}")
    print("现在可以查询快递报价了：")
    print('  python price_query.py --from "广东 深圳 南山" --to "浙江 杭州 西湖" --weight 1')
    return 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())
