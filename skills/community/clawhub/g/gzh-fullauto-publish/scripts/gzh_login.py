# -*- coding: utf-8 -*-
"""公众号扫码登录：打开一个可见浏览器窗口，扫码后自动保存登录态。

用法
----
    python gzh_login.py --profile ./gzh-profile --port 9333
    python gzh_login.py --check --profile ./gzh-profile --port 9333

它做了什么
----------
1. 先探测 `--port` 上有没有已经在跑的浏览器实例：
   - 有 → 直接附着（attach），不会新开实例（同一个数据目录开第二个实例会因目录
     锁而崩溃），也不会去关别人的浏览器，只关掉本脚本自己打开的标签页。
   - 没有 → 用本机 Chrome / Chromium 以独立数据目录 `--profile` 打开一个**可见**
     窗口，并监听 `--remote-debugging-port`，然后附着上去。
2. 窗口打开后用 Win32 API 把窗口摆回屏幕内并置前（窗口有被放到屏幕外的前例，
   使用者会看不到、扫不到）。
3. 若窗口停在登录页，遍历页面所有 frame 找到二维码图片，另存为 PNG，
   打印 `QR_PATH: <文件>`，可以拿手机直接扫。
4. 后台轮询登录状态；登录成功后**在同一个浏览器上下文里**导出全部 cookie 到
   `<profile>/gzh_cookies.json`（分两个进程导出会丢登录态），并打印 `LOGIN_OK`。

登录态大致能撑 4 天左右，期间直接跑 gzh_save.py 即可，不必重复扫码。
浏览器窗口会保持运行，方便后续 gzh_save.py / gzh_verify.py 附着使用。
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

DEFAULT_PROFILE = os.path.join(".", "gzh-profile")
DEFAULT_PORT = 9333

# 从页面正文里出现这些词 = 还停在登录页
LOGIN_PAGE_MARKS = ("扫一扫", "使用账号登录", "扫码登录")


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------
def log(msg):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), msg), flush=True)


def port_json(port, timeout=2.0):
    """探测端口上是否有 DevTools 协议服务在跑；有则返回它的版本信息。"""
    url = "http://127.0.0.1:%d/json/version" % int(port)
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", "replace"))
    except Exception:
        return None


def find_browser(explicit=None):
    """找一个可用的 Chrome / Chromium 可执行文件（不写死任何本机路径）。"""
    cands = []
    if explicit:
        cands.append(explicit)
    env = os.environ.get("GZH_BROWSER_PATH")
    if env:
        cands.append(env)
    pf = os.environ.get("PROGRAMFILES", "")
    pf86 = os.environ.get("PROGRAMFILES(X86)", "")
    lad = os.environ.get("LOCALAPPDATA", "")
    for p in (pf, pf86):
        if p:
            cands.append(os.path.join(p, "Google", "Chrome", "Application", "chrome.exe"))
    if lad:
        cands.append(os.path.join(lad, "Google", "Chrome", "Application", "chrome.exe"))
    cands += [
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    # Playwright 自带的 chromium（推荐：与本机已装的 Chrome 互不干扰）
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            cands.append(p.chromium.executable_path)
    except Exception:
        pass

    for c in cands:
        if c and os.path.isfile(c):
            return c

    raise SystemExit(
        "错误：没找到可用的 Chrome / Chromium。\n"
        "请任选一种方式指定：\n"
        "  1) 加参数 --browser-path \"<浏览器可执行文件完整路径>\"\n"
        "  2) 设置环境变量 GZH_BROWSER_PATH=<路径>\n"
        "  3) 安装 Playwright 自带 chromium：python -m playwright install chromium"
    )


# --------------------------------------------------------------------------
# Windows 窗口摆位（其它系统直接跳过）
# --------------------------------------------------------------------------
def _enum_windows():
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    result = []
    proc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    def cb(hwnd, _lparam):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True
            n = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(n + 1)
            user32.GetWindowTextW(hwnd, buf, n + 1)
            cls = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, cls, 256)
            rect = wintypes.RECT()
            user32.GetWindowRect(hwnd, ctypes.byref(rect))
            result.append(
                {
                    "hwnd": int(hwnd),
                    "title": buf.value,
                    "cls": cls.value,
                    "rect": (rect.left, rect.top, rect.right, rect.bottom),
                }
            )
        except Exception:
            pass
        return True

    user32.EnumWindows(proc(cb), 0)
    return result


def fix_window(prefer_titles=("微信",), window_size=(920, 1020)):
    """把浏览器窗口摆回屏幕内并置前。找不到就静默跳过（不阻塞登录）。"""
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        user32 = ctypes.windll.user32
        wa = wintypes.RECT()
        # SPI_GETWORKAREA = 0x0030：当前显示器的工作区（不含任务栏）
        user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(wa), 0)
        wl, wt, wr, wb = wa.left, wa.top, wa.right, wa.bottom

        best, best_score = None, -1
        for w in _enum_windows():
            if w["cls"] != "Chrome_WidgetWin_1":
                continue
            l, t, r, b = w["rect"]
            if r - l < 200 or b - t < 200:
                continue
            inside = (l >= wl and t >= wt and r <= wr and b <= wb)
            score = 0
            if any(s in w["title"] for s in prefer_titles):
                score += 3
            if not inside:
                score += 2
            if w["title"].strip():
                score += 1
            if score > best_score:
                best, best_score = w, score
        if not best:
            log("窗口摆位：没找到浏览器窗口，跳过（不影响登录）")
            return None

        l, t, r, b = best["rect"]
        inside = (l >= wl and t >= wt and r <= wr and b <= wb)
        if not inside:
            w, h = window_size
            w = min(w, max(600, wr - wl - 40))
            h = min(h, max(400, wb - wt - 40))
            x, y = wl + 60, wt + 40
            # SWP_NOZORDER=0x0004（不改变层级，下面单独置前）
            user32.SetWindowPos(best["hwnd"], 0, x, y, w, h, 0x0004)
            log("窗口原本在屏幕外/被挤压，已摆到 (%d, %d) 尺寸 %dx%d" % (x, y, w, h))
        else:
            log("窗口位置正常：%s" % (best["title"][:40] or "Chrome"))
        user32.ShowWindow(best["hwnd"], 9)  # SW_RESTORE
        user32.SetForegroundWindow(best["hwnd"])
        return best["title"]
    except Exception as e:
        log("窗口摆位失败（不影响登录）：%s" % e)
        return None


# --------------------------------------------------------------------------
# 页面判定 / 二维码 / cookie
# --------------------------------------------------------------------------
def page_state(page):
    """返回 (是否已登录, token)。判据：URL 带 token 或正文里没有登录页标记。"""
    token = None
    m = re.search(r"token=(\d+)", page.url or "")
    if m:
        token = m.group(1)
    if token:
        return True, token
    try:
        body = page.inner_text("body")
    except Exception:
        body = ""
    if body and len(body) > 200 and not any(k in body for k in LOGIN_PAGE_MARKS):
        mm = re.search(r"token=(\d+)", page.content() or "")
        return True, (mm.group(1) if mm else None)
    return False, None


def grab_qr(page, out_path):
    """遍历所有 frame 抓二维码图片，落盘为 PNG。返回文件路径或 None。"""
    for fr in page.frames:
        try:
            src = fr.evaluate(
                "() => { const i = [...document.querySelectorAll('img')]"
                ".find(x => (x.src || '').includes('scanloginqrcode')); return i ? i.src : null; }"
            )
        except Exception:
            src = None
        if not src:
            continue
        try:
            data = page.request.get(src).body()
            with open(out_path, "wb") as f:
                f.write(data)
            log("二维码已保存（网页图片）: %s (%d 字节)" % (out_path, len(data)))
            return out_path
        except Exception as e:
            log("下载二维码失败：%s" % e)

    # 退路 1：base64 内嵌图
    try:
        src = page.evaluate(
            "() => { const i = [...document.querySelectorAll('img')]"
            ".find(x => (x.src || '').startsWith('data:image')); return i ? i.src : null; }"
        )
        if src and "," in src:
            data = base64.b64decode(src.split(",", 1)[1])
            with open(out_path, "wb") as f:
                f.write(data)
            log("二维码已保存（内嵌图）: %s (%d 字节)" % (out_path, len(data)))
            return out_path
    except Exception:
        pass

    # 退路 2：元素截图
    for fr in page.frames:
        try:
            el = fr.query_selector("img[src*='scanloginqrcode']") or fr.query_selector(".qrcode img")
        except Exception:
            el = None
        if el:
            try:
                el.screenshot(path=out_path)
                log("二维码已保存（元素截图）: %s" % out_path)
                return out_path
            except Exception:
                pass
    log("没能定位到二维码元素；窗口已打开，请直接在窗口里扫码。")
    return None


def export_cookies(ctx, out_path):
    """把当前上下文的全部 cookie 导出到 JSON（必须与扫码同一个上下文）。"""
    cks = ctx.cookies()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cks, f, ensure_ascii=False, indent=1)
    key = {c["name"] for c in cks if "weixin" in (c.get("domain") or "")}
    log("已导出 %d 个 cookie（weixin 域 %d 个）→ %s" % (len(cks), len(key), out_path))
    return cks


# --------------------------------------------------------------------------
# 主流程
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="公众号扫码登录：可见窗口 + 二维码 + 登录态（cookie）持久化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--profile", default=DEFAULT_PROFILE, help="浏览器数据目录（独立，默认 ./gzh-profile）")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help="远程调试端口（默认 9333）")
    ap.add_argument("--check", action="store_true", help="只检查当前登录态，不启动新浏览器")
    ap.add_argument("--qr-out", default=None, help="二维码保存路径（默认 <profile>/gzh_login_qr.png）")
    ap.add_argument("--timeout", type=int, default=300, help="等待扫码的秒数（默认 300）")
    ap.add_argument("--browser-path", default=None, help="浏览器可执行文件路径（不填则自动探测）")
    ap.add_argument("--no-window-fix", action="store_true", help="不自动把窗口摆进屏幕内/置前")
    args = ap.parse_args()

    profile = os.path.abspath(args.profile)
    os.makedirs(profile, exist_ok=True)
    qr_path = args.qr_out or os.path.join(profile, "gzh_login_qr.png")
    ck_path = os.path.join(profile, "gzh_cookies.json")

    from playwright.sync_api import sync_playwright

    alive = port_json(args.port)
    launched = None

    if not alive and args.check:
        print("NO_INSTANCE 端口 %d 上没有正在运行的浏览器实例" % args.port)
        print("（需要查看登录态请先运行：python gzh_login.py --profile %s --port %d）" % (args.profile, args.port))
        return 3

    if not alive:
        exe = find_browser(args.browser_path)
        log("浏览器：%s" % exe)
        log("数据目录：%s" % profile)
        cmd = [
            exe,
            "--user-data-dir=%s" % profile,
            "--remote-debugging-port=%d" % args.port,
            "--remote-allow-origins=*",
            "--no-first-run",
            "--no-default-browser-check",
            "--window-size=920,1020",
            "--window-position=80,60",
            "--disable-features=Translate,MediaRouter",
            "about:blank",
        ]
        flags = 0
        if os.name == "nt":
            flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        launched = subprocess.Popen(
            cmd, creationflags=flags, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True
        )
        log("已启动浏览器（PID %d），等待调试端口就绪…" % launched.pid)
        for _ in range(40):
            time.sleep(0.5)
            if port_json(args.port):
                break
        if not port_json(args.port):
            raise SystemExit(
                "错误：浏览器已启动但调试端口 %d 未就绪。\n"
                "常见原因：同一数据目录已被另一个实例占用，或端口被防火墙拦截。" % args.port
            )

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:%d" % args.port)
        ctx = browser.contexts[0] if browser.contexts else browser.new_context()
        page = ctx.new_page()
        try:
            page.goto("https://mp.weixin.qq.com/", wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            log("打开公众平台首页超时/失败：%s（继续按当前页面状态判断）" % e)

        if launched and not args.no_window_fix:
            time.sleep(1.0)
            fix_window()

        logged, token = False, None
        for _ in range(10):
            time.sleep(2)
            logged, token = page_state(page)
            if logged:
                break

        if logged:
            log("当前已是登录状态（token=%s）" % (token or "从页面取"))
            export_cookies(ctx, ck_path)
            print("LOGIN_OK" if not args.check else "LOGIN_ALREADY")
            page.close()
            return 0

        if args.check:
            print("LOGIN_REQUIRED 登录态已失效，需要重新扫码")
            page.close()
            return 2

        # 未登录 → 抓二维码
        grabbed = grab_qr(page, qr_path)
        if grabbed:
            print("QR_PATH: %s" % os.path.abspath(grabbed))
            log("二维码约 2-5 分钟内有效，请尽快用微信扫码。")
        else:
            log("窗口已打开，请在窗口里直接扫码。")

        deadline = time.time() + max(30, args.timeout)
        while time.time() < deadline:
            time.sleep(3)
            try:
                logged, token = page_state(page)
            except Exception:
                continue
            if logged:
                break

        if not logged:
            print("LOGIN_TIMEOUT 等待扫码超时（%d 秒）" % args.timeout)
            page.close()
            return 4

        time.sleep(4)  # 等登录后的跳转与 cookie 落定
        export_cookies(ctx, ck_path)
        log("登录成功（token=%s）" % (token or "从页面取"))
        print("LOGIN_OK")
        page.close()  # 只关自己开的标签页，浏览器保持运行
        return 0


if __name__ == "__main__":
    sys.exit(main())
