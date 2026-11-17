#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最小 CDP 客户端（零依赖，只用 Python 标准库）。

为什么自带一套而不用别的项目的模块
----------------------------------
本 skill 要能脱离 ai-case-library 独立跑（换台机器、换个项目），
所以把「WebSocket + CDP 命令」这两件事收进一个文件。

设计原则：**只连、不管**
----------------------
本模块**只连接用户自己已经启动好的 Chrome**，不代用户启动、也不代用户
结束浏览器进程：

- 端口通 → 直接用
- 端口不通 → 打印一条可直接复制的启动命令，让用户自己跑

理由很简单：替用户 spawn / kill 浏览器进程是高影响操作，
既可能误伤用户自己开着的窗口，也不该由自动化脚本代劳。
（脚本对浏览器的唯一写入是「点页面上的领取按钮」，只此而已。）

三个已实测的硬坑（照抄前先读完，别再踩）
------------------------------------------
1. **Chrome 136+ 拒绝在【默认 user-data-dir】上开调试端口**（官方设计，
   见 https://developer.chrome.com/blog/remote-debugging-port），
   所以必须用独立 profile —— 登录态天然与日常 Chrome 分家，这是预期行为
   不是故障。日常 Chrome 的 cookie 是 App-Bound 加密（v20 前缀），
   **读不出来**，也不需要读。
2. **访问 127.0.0.1 的调试端口要绕开系统代理**，否则 WebSocket 会被
   10053/10054 重置。做法是用 `urllib.request.ProxyHandler({})` 只让
   **本模块的 urllib** 不走代理；**不去改 os.environ**——改全局代理变量
   会连带影响调用方的其他网络访问，那不是本脚本该做的副作用。
3. **profile 里的 SingletonLock 不去动它**。它是浏览器自己的运行期文件，
   本脚本没有理由替用户删。若真被强杀残留卡住，正确做法是换一个
   profile 目录，而不是由脚本去动别人的浏览器文件。

WS 实现说明：只做客户端→服务端方向的帧掩码（RFC 6455 要求），
不处理分片重组的续帧以外的情况，够用即可。
"""
import base64
import json
import os
import re
import select
import socket
import threading
import struct
import time
import urllib.request

__all__ = [
    "WS", "CDP", "cdp_up", "clear_proxy", "browser_endpoint", "remove_lock",
    "pick_chrome", "ensure_chrome", "stop_chrome", "log",
]


def log(msg):
    print(msg, flush=True)


def _host_matches(url, host_suffixes):
    """判断 URL 的 host 是否落在允许的后缀列表里。

    ⚠ 用**后缀**而不是精确相等，是为了兼容 www.modelscope.cn / modelscope.cn
      两种写法；但必须防住「evil-modelscope.cn」这类后缀拼接攻击 ——
      所以要求 host 要么等于后缀，要么以「.」+ 后缀结尾。
    """
    m = re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://([^/?#]+)", url or "")
    if not m:
        return False
    host = m.group(1).split("@")[-1].split(":")[0].lower()
    for suf in host_suffixes:
        suf = suf.lower().lstrip(".")
        if host == suf or host.endswith("." + suf):
            return True
    return False


# --------------------------------------------------------------------------
# WebSocket（最小实现）
# --------------------------------------------------------------------------
class WS:
    """够用的 WebSocket 客户端：文本帧收发 + 客户端掩码。"""

    def __init__(self, url, timeout=45):
        m = re.match(r"ws://([^:/]+):(\d+)(/.*)", url)
        if not m:
            raise ValueError("不支持的 ws url: %r" % url)
        self.host, self.port, self.path = m.group(1), int(m.group(2)), m.group(3)
        self.sock = socket.create_connection((self.host, self.port), timeout=timeout)
        self.sock.settimeout(timeout)
        self._handshake()
        self._buf = b""

    def _handshake(self):
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            "GET %s HTTP/1.1\r\nHost: %s:%d\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            "Sec-WebSocket-Version: 13\r\nSec-WebSocket-Key: %s\r\n\r\n"
            % (self.path, self.host, self.port, key)
        )
        self.sock.sendall(req.encode())
        data = b""
        while b"\r\n\r\n" not in data:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise ConnectionError("ws 握手失败：连接被对端关闭")
            data += chunk
        if b"101" not in data.split(b"\r\n", 1)[0]:
            raise ConnectionError("ws 握手被拒：%r" % data.split(b"\r\n", 1)[0])

    def _read_exact(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("ws closed")
            buf += chunk
        return buf

    def _recv_frame(self):
        b0, b1 = self._read_exact(2)
        fin = (b0 & 0x80) != 0
        opcode = b0 & 0x0F
        masked = (b1 & 0x80) != 0
        length = b1 & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._read_exact(2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._read_exact(8))[0]
        if masked:
            self._read_exact(4)
        return fin, opcode, self._read_exact(length)

    def recv_text(self):
        parts = []
        while True:
            fin, opcode, payload = self._recv_frame()
            if opcode in (0x1, 0x0):
                parts.append(payload)
            if fin:
                break
        return b"".join(parts).decode("utf-8", "replace")

    def send_text(self, text):
        payload = text.encode("utf-8")
        mask = os.urandom(4)
        header = bytes([0x81])
        n = len(payload)
        if n < 126:
            header += bytes([0x80 | n])
        elif n < 65536:
            header += bytes([0x80 | 126]) + struct.pack(">H", n)
        else:
            header += bytes([0x80 | 127]) + struct.pack(">Q", n)
        masked = bytes(payload[i] ^ mask[i % 4] for i in range(n))
        self.sock.sendall(header + mask + masked)

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass

    def readable(self, timeout=0.3):
        try:
            r, _, _ = select.select([self.sock], [], [], timeout)
            return bool(r)
        except Exception:
            return False


# --------------------------------------------------------------------------
# CDP
# --------------------------------------------------------------------------
class CDP:
    """够用的 CDP 封装：建 target / 连 target / 求值 JS。"""

    def __init__(self, port):
        self.port = port
        self._opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            ver = self._http("/json/version")
        except Exception as e:
            raise SystemExit(
                "\n✗ 连不上 Chrome 调试端口 127.0.0.1:%d\n"
                "  Chrome 136+ 拒绝在【默认 user-data-dir】上开调试端口"
                "（官方说明：\n"
                "  https://developer.chrome.com/blog/remote-debugging-port）。\n"
                "  ⇒ CDP 只能跑在【独立 profile】上，登录态与日常 Chrome 分家，\n"
                "    这是官方设计，不是本机故障。\n"
                "  请依次确认：\n"
                "    1) 调试端口号的 Chrome 确实还开着\n"
                "    2) 启动时带了 --user-data-dir=<独立目录>\n"
                "    3) 端口号与本脚本的 --port 一致\n"
                "  原始错误：%s" % (port, e))
        self.bws = WS(ver["webSocketDebuggerUrl"])
        self.ws = None
        self.tid = None
        self._id = 0
        self._main_context = None
        # 🚨 WebSocket 发送/收帧必须**串行化**：
        #   将来若引入后台线程（处理 CDP 事件），
        #   与主线程并发收发会让 requestId 与响应交错 ⇒ 协议错乱。
        self._lock = threading.RLock()

    # ---- HTTP 侧 ----
    def _http(self, path):
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.port, path))
        with self._opener.open(req, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))

    def list_targets(self):
        return self._http("/json")

    def find_target(self, needle, host_suffixes=None):
        """按 URL 子串找已存在的 target；找不到返回 None。

        ⚠ host_suffixes 不为空时**只接受 host 匹配**的 target。
          这个限制是安全边界，不是可选优化：
          只按子串找 tab，理论上会连上任意含该子串的页面
          （比如用户开着某个第三方站点，路径里恰好有 "magicube"），
          而本模块连上之后会**在那个页面上点按钮**。
          ⇒ 凡是「连上别人的页面并操作」的路径，都必须限定 host。
        """
        for t in self.list_targets():
            url = t.get("url") or ""
            if needle not in url:
                continue
            if host_suffixes and not _host_matches(url, host_suffixes):
                continue
            if t.get("webSocketDebuggerUrl"):
                return t
        return None

    # ---- 浏览器级 ----
    def send_browser(self, method, params=None):
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        self.bws.send_text(json.dumps(msg))
        while True:
            resp = json.loads(self.bws.recv_text())
            if resp.get("id") == self._id:
                return resp

    def new_target(self, url):
        """走 CDP 原生 Target.createTarget —— HTTP /json/new 在新版 Chrome 被禁（405）。"""
        r = self.send_browser("Target.createTarget", {"url": url})
        if "error" in r:
            raise RuntimeError("Target.createTarget 失败: %s" % r["error"])
        tid = r["result"]["targetId"]
        return {"id": tid, "targetId": tid}

    def connect_target(self, target_id):
        for _ in range(10):
            for t in self.list_targets():
                if t.get("id") == target_id and t.get("webSocketDebuggerUrl"):
                    self.ws = WS(t["webSocketDebuggerUrl"])
                    self.tid = target_id
                    self._main_context = self._enable_and_grab_context()
                    return True
            time.sleep(0.5)
        return False

    def close_target(self, target_id):
        try:
            self.send_browser("Target.closeTarget", {"targetId": target_id})
        except Exception:
            pass

    def close_ws(self):
        """只关闭 WebSocket 连接，不断浏览器、不关标签页。

        ⚠ 本模块**不提供**「关闭浏览器」的能力：浏览器是用户自己的，
          脚本无权替他关掉，也关不掉别人的窗口。
        """
        for ws in (self.ws, self.bws):
            try:
                if ws is not None:
                    ws.close()
            except Exception:
                pass
        self.ws = None

    # ---- 页面级 ----
    def _enable_and_grab_context(self, timeout=6):
        """发 Runtime.enable 并抓主帧默认执行上下文 id（SPA 导航会换上下文）。"""
        try:
            self.send("Runtime.enable")
        except Exception:
            pass
        end = time.time() + timeout
        best = None
        while time.time() < end:
            if not self.ws.readable(0.3):
                if best is not None:
                    break
                continue
            try:
                raw = self.ws.recv_text()
            except Exception:
                break
            try:
                ev = json.loads(raw)
            except Exception:
                continue
            if ev.get("method") == "Runtime.executionContextCreated":
                p = ev.get("params", {})
                if p.get("auxData", {}).get("isDefault"):
                    best = p.get("id")
            elif ev.get("method") == "Runtime.executionContextsCleared":
                best = None
        return best

    def send(self, method, params=None):
        if self.ws is None:
            raise RuntimeError("未连接页面 target，先 new_target + connect_target")
        with self._lock:
            self._id += 1
            msg = {"id": self._id, "method": method, "params": params or {}}

            def _roundtrip():
                self.ws.send_text(json.dumps(msg))
                while True:
                    raw = self.ws.recv_text()
                    resp = json.loads(raw)
                    if resp.get("id") == self._id:
                        return resp
                    # 其余是事件帧，忽略
                    # ⚠ 本 skill 不用任何需要处理事件的 CDP 域
                    #   （Fetch/Network 拦截都不需要）⇒ 事件直接丢弃。

            try:
                return _roundtrip()
            except ConnectionError:
                tid = getattr(self, "tid", None)
                if not tid or not self.connect_target(tid):
                    raise
                log("  [warn] CDP 页面连接断开，已重连同一标签页")
                return _roundtrip()

    def eval(self, expr, refresh_context=False, context_id=None):
        if refresh_context or (context_id is None and self._main_context is None):
            self._main_context = self._enable_and_grab_context()
        params = {"expression": expr, "returnByValue": True, "awaitPromise": True}
        ctx = context_id if context_id is not None else self._main_context
        if ctx is not None:
            params["contextId"] = ctx
        last = None
        for _ in range(6):
            r = self.send("Runtime.evaluate", params)
            if "error" in r:
                err = r["error"]
                if err.get("code") == -32000 and self._main_context is not None:
                    self._main_context = self._enable_and_grab_context()
                    params["contextId"] = self._main_context
                    time.sleep(1)
                    continue
                raise RuntimeError("CDP 协议错误: %s" % err)
            if "exceptionDetails" in r:
                exc = r["exceptionDetails"].get("exception", {})
                raise RuntimeError("JS 执行异常: %s"
                                   % exc.get("description", r["exceptionDetails"]))
            last = r.get("result", {}).get("result", {}).get("value")
            if last is not None:
                return last
            time.sleep(1)
        if last is None and ctx is not None and context_id is None:
            r = self.send("Runtime.evaluate",
                          {"expression": expr, "returnByValue": True,
                           "awaitPromise": True})
            last = r.get("result", {}).get("result", {}).get("value")
        return last


# --------------------------------------------------------------------------
# Chrome 启动
# --------------------------------------------------------------------------
CHROME_CANDIDATES = [
    # 优先 Chrome for Testing（官方对自动化场景的推荐浏览器）
    (r"%LOCALAPPDATA%\Google\ChromeForTesting\chrome-win64\chrome.exe",
     "Chrome for Testing"),
    (r"%ProgramFiles%\Google\Chrome\Application\chrome.exe", "system Chrome"),
    (r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe", "system Chrome x86"),
    (r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe", "user Chrome"),
    (r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe", "Edge"),
]

# Git Bash 起的 python 缺这两个变量 → Chrome 会找不到自己的 DLL/目录
for _k, _v in (("LOCALAPPDATA", r"C:\Users\DELL\AppData\Local"),
               ("ProgramFiles", r"C:\Program Files")):
    if not os.environ.get(_k):
        os.environ[_k] = _v


def cdp_up(port):
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with op.open("http://127.0.0.1:%d/json/version" % port, timeout=3) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception:
        return None


def clear_proxy():
    """返回一个**不走系统代理**的 urllib opener（仅本模块内部用）。

    ⚠ 为什么需要：走系统代理访问 127.0.0.1 的调试端口会被代理截走，
      表现为 WebSocket 10053/10054 连接重置。
    ⚠ 只用 ProxyHandler({}) 让**本模块的 urllib** 不走代理，**不改
      os.environ** —— 改全局代理变量会连带影响调用方的其他网络访问，
      属于不该由本脚本做的副作用。
    """
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def browser_endpoint(port):
    """返回调试端口的 URL（供调用方拼 /json/version 等路径）。"""
    return "http://127.0.0.1:%d" % port


def remove_lock(profile):
    """检查 Chrome profile 里的 SingletonLock 是否存在（**不删除、不挪动**）。

    ⚠ 这里刻意只做「探测」，不做任何删除/改名：
      Chrome 的 SingletonLock 属于浏览器自己的运行期文件，本脚本没有
      理由替用户删它。若真被强杀残留卡住，正确做法是让用户换一个
      profile 目录（--profile），而不是由脚本动别人的浏览器文件。
    """
    lock = os.path.join(profile, "Default", "LOCK")
    if os.path.exists(lock):
        log("  [info] profile 里存在 LOCK 文件（可能是上次异常退出的残留）。"
            "本脚本不删除它；若 Chrome 因此启动不了，请换一个 --profile 目录。")
    return False


def pick_chrome():
    seen = set()
    for path_tpl, label in CHROME_CANDIDATES:
        if path_tpl in seen:
            continue
        seen.add(path_tpl)
        p = os.path.expandvars(path_tpl)
        if os.path.exists(p):
            return p, (label or "Chrome")
    return None, None


def wait_cdp(timeout=40, port=None):
    """轮询 DevTools 端口，返回 True 表示已通。

    ⚠ 用 urllib 而不是 curl：curl 会带上系统代理，必须显式清空。
    """
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    url = "http://127.0.0.1:%d/json/version" % (port or 9333)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            op.open(url, timeout=2).read()
            return True
        except Exception:
            time.sleep(1.5)
    return False


def ensure_chrome(port=9333, url="about:blank", profile=None):
    """确保调试端口可用。

    ✅ 首选：**连接用户已经开着的 Chrome**（端口已通就直接用，不碰任何进程）。
    ❌ 端口不通时：**不自动代用户启动浏览器**，而是打印一条可直接复制的
       启动命令，让用户自己决定要不要跑。

    这样做的原因：脚本替用户 spawn/结束浏览器进程属于高影响操作，
    既容易误伤用户自己的窗口，也不该由一个自动化脚本代劳。
    返回 (proc_or_None, launched_bool) —— 本实现下 proc 恒为 None。

    🔒 命令里**默认不带 `--no-sandbox`**：关掉 Chrome 沙箱会显著降低
       浏览器自身的安全隔离，所以它只是「容器 / 受管沙箱里 Chrome 起不来」
       时的**显式兜底**，不该是默认动作。默认命令另外做了两件加固：
       调试端口显式绑定 127.0.0.1（不监听所有网卡）、
       强制使用独立 profile（与日常浏览器的登录态、cookie 天然分开）。
    """
    if cdp_up(port):
        return None, False
    chrome, _label = pick_chrome()
    exe = chrome or "<Chrome 可执行文件路径>"
    prof = profile or os.path.expanduser("~/chrome-ms-profile")
    cmd = ('"%s" --remote-debugging-port=%d --remote-debugging-address=127.0.0.1 '
           '--user-data-dir="%s" --no-first-run --no-default-browser-check %s'
           % (exe, port, prof, url))
    raise SystemExit(
        "调试端口 127.0.0.1:%d 没开。\n"
        "请自己启动一个带调试端口的 Chrome（下面这条可直接复制）：\n\n"
        "  %s\n\n"
        "说明：\n"
        "  · 独立 profile 是 Chrome 136+ 的官方要求（默认 user-data-dir "
        "不允许开调试端口），也让这个实例的登录态与日常 Chrome 分开。\n"
        "  · 调试端口已显式绑定 127.0.0.1，不会暴露到局域网。\n"
        "  · 窗口会一直留着，用完自己关掉即可。\n"
        "  · 若在容器 / 受管沙箱里 Chrome 启动即退出，可再加 --no-sandbox\n"
        "    （那会关闭浏览器沙箱、降低安全隔离，仅限这种受限环境）。"
        % (port, cmd))


def stop_chrome(cdp, proc):
    """**只断开 WebSocket 连接，不结束任何浏览器进程**。

    本脚本只连接用户自己启动的 Chrome，用完就断开 ——
    浏览器窗口归用户所有，脚本无权替他关掉。
    """
    try:
        if cdp is not None:
            cdp.close_ws()
    except Exception:
        pass
    log("[ms] 已断开 CDP 连接（浏览器窗口保持不变，由你决定何时关闭）")


if __name__ == "__main__":
    # 自检：列候选 Chrome + 当前端口状态
    p, label = pick_chrome()
    print("Chrome:", p, label)
    for port in (9333,):
        print("port %d:" % port, "UP" if cdp_up(port) else "down")
