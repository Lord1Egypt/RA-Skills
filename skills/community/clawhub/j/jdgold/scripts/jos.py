#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""京东 OAuth2 登录辅助（jdgold，仅本地使用）。

所有业务接口通过 ``bff_client`` 调用 cf-gold-ai 后端（经金融网关）。
本文件只负责 PKCE 登录流程的客户端部分：
  - 第一步：CSPRNG 生成 code_verifier + state，算 code_challenge(S256)，
    调后端 ``auth_login_url`` 取授权 URL（authCode 全程不离开后端）。
  - 完成信号：同机=本地回调收 state；沙箱=轮询后端 ``auth_status``。
  - 第二步：凭 state + code_verifier 调后端 ``auth_exchange`` 换 access_token。
  - token / pin / login-session 本地缓存。

子命令：
  login [--daemon] [--kill-stale] [--force] [--no-browser]
  stop
  oauth-url | exchange | refresh | token | holdings
"""
import os, sys, json, time, hashlib, base64, secrets, argparse, socket, webbrowser, subprocess, signal, re
import urllib.parse, urllib.request
from datetime import datetime, timezone, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import bff_client
import secure_store

_orig_getaddrinfo = socket.getaddrinfo


def _ipv4_only_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    except socket.gaierror:
        return _orig_getaddrinfo(host, port, family, type, proto, flags)


socket.getaddrinfo = _ipv4_only_getaddrinfo

# 授权 URL 由后端拼装（APPKEY / scope 等凭据信息只在后端持有）。
# 回调端口勿用 6666 等：Chrome/Edge 会报 ERR_UNSAFE_PORT（IRC 封禁端口）
DEFAULT_CALLBACK_PORT = 8765
LOGIN_WAIT_SEC = 300  # 5分钟超时，非8小时

CACHE_DIR = os.path.expanduser("~/.openclaw/service-env/jdgold")

os.makedirs(CACHE_DIR, exist_ok=True)
TOKEN_FILE = os.path.join(CACHE_DIR, "token.json")
LOGIN_SESSION_FILE = os.path.join(CACHE_DIR, "login-session.json")
LOGIN_PID_FILE = os.path.join(CACHE_DIR, "login.pid")
AUTH_SESSION_FILE = os.path.join(CACHE_DIR, "auth-session.json")
LOGIN_LOG_FILE = os.path.join(CACHE_DIR, "login.log")
PENDING_HOLDINGS_FILE = os.path.join(CACHE_DIR, "pending-holdings.json")
SESSION_PIN_FILE = os.path.join(CACHE_DIR, "session-pin.json")


def gen_request_id(prefix: str = "gold-skill") -> str:
    """生成 JHub 链路追踪 requestId，格式：{prefix}-{timestampms}-{rand8hex}。"""
    import uuid
    ts = int(time.time() * 1000)
    rand8 = uuid.uuid4().hex[:8]
    return f"{prefix}-{ts}-{rand8}"


_SUCCESS_HTML = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>已登录</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{min-height:100vh;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;background:#fff;padding:24px}.card{width:100%;max-width:420px;background:#fff;padding:56px 40px;text-align:center}.check{width:56px;height:56px;margin:0 auto 24px;border-radius:50%;background:#fdf1e5;display:flex;align-items:center;justify-content:center}h1{font-size:22px;font-weight:600;color:#1f2937;margin-bottom:10px;letter-spacing:.3px}h1 .gold{color:#EB9654}p{font-size:14px;color:#8a8f99;line-height:1.7}</style></head>
<body><div class="card"><div class="check"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#EB9654" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5 L10 17 L19 7.5"/></svg></div>
<h1>已登录 <span class="gold">京东黄金 Skills</span></h1><p>你现在可以关闭此页面。</p></div></body></html>"""


def _callback_host(hostname):
    if not hostname or hostname in ("localhost", "::1", "[::1]"):
        return "127.0.0.1"
    return hostname


def _normalize_redirect_uri(uri):
    p = urlparse(uri)
    return f"{p.scheme or 'http'}://{_callback_host(p.hostname)}:{p.port or DEFAULT_CALLBACK_PORT}{p.path or '/callback'}"


# 本地回调地址：同机模式下后端授权完成后 302 回跳到此（仅带 state 作完成信号）。
REDIRECT_URI = _normalize_redirect_uri(
    os.environ.get("GOLD_JD_REDIRECT_URI", f"http://127.0.0.1:{DEFAULT_CALLBACK_PORT}/callback")
)


# token 在系统级加密存储中的条目名（Keychain account / DPAPI 文件名）
TOKEN_SECRET_NAME = "access-token"


def _save_token(tok):
    """将 token 整体（含 access_token + 元数据）写入系统级加密存储。

    敏感数据不再以明文落盘：macOS 走 Keychain，Windows 走 DPAPI，
    其余平台回退到 0o600 明文文件（由 secure_store 内部处理）。
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    tok["_obtained_at"] = int(time.time())
    secure_store.save_secret(
        TOKEN_SECRET_NAME, json.dumps(tok, ensure_ascii=False))
    # 清理可能存在的旧明文文件，避免敏感数据残留
    try:
        os.remove(TOKEN_FILE)
    except FileNotFoundError:
        pass


def _load_token():
    """从系统级加密存储读取 token；若不存在则尝试迁移旧明文文件。"""
    raw = secure_store.load_secret(TOKEN_SECRET_NAME)
    if raw:
        try:
            return json.loads(raw)
        except (ValueError, TypeError):
            return None
    # 兼容旧版本：迁移历史明文 token.json 到加密存储后删除明文
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, encoding="utf-8") as f:
                tok = json.load(f)
        except (ValueError, OSError):
            return None
        secure_store.save_secret(
            TOKEN_SECRET_NAME, json.dumps(tok, ensure_ascii=False))
        try:
            os.remove(TOKEN_FILE)
        except FileNotFoundError:
            pass
        return tok
    return None


def _mask_token(token):
    """对 token 做脱敏，仅用于日志/展示，绝不可用于接口传参。

    规则：保留前 4 后 4 位，中间以 *** 掩码；过短则整体掩码。
    例：``eyJhbGci...abcd`` → ``eyJh***abcd``。
    """
    if not token:
        return "<empty>"
    s = str(token)
    if len(s) <= 8:
        return "***"
    return f"{s[:4]}***{s[-4:]}"


def _mask_in_text(text):
    """对一段可能包含 token 的文本做脱敏，掩码其中较长的 url-safe 串。"""
    if not text:
        return text
    return re.sub(r"[A-Za-z0-9_\-\.]{16,}",
                  lambda m: _mask_token(m.group(0)), str(text))


def _expires_sec_of(tok):
    """读取 token 有效期（秒）。

    后端 expiresIn 单位为「毫秒」，本地按原值（毫秒）存储，
    此处统一 /1000 归一为秒供过期判断/剩余时长计算使用。
    """
    try:
        v = int(tok.get("expires_in", 0))
    except (TypeError, ValueError):
        return 0
    return v // 1000


def _is_expired(tok):
    try:
        exp = int(tok.get("_obtained_at", 0)) + _expires_sec_of(tok) - 300
        return time.time() >= exp
    except Exception:
        return True


def _gen_state():
    """CSPRNG 生成 state（反 CSRF + 后端缓存查找 key）。"""
    return secrets.token_urlsafe(24)


def _gen_verifier():
    """CSPRNG 生成 PKCE code_verifier（43–128 字符，url-safe）。"""
    # token_urlsafe(64) -> ~86 字符，落在 RFC 7636 的 43–128 区间。
    return secrets.token_urlsafe(64)


def _compute_challenge(verifier):
    """S256：base64url(sha256(verifier)) 去填充。"""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def _pids_listening_on(port):
    try:
        out = subprocess.check_output(
            ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"],
            stderr=subprocess.DEVNULL, text=True,
        )
        return [int(x) for x in out.split() if x.strip().isdigit()]
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return []


def _process_cmdline(pid):
    try:
        return subprocess.check_output(
            ["ps", "-p", str(pid), "-o", "command="], stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return ""


def _pid_alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def _is_jos_login_process(pid):
    """识别 jos.py 或 OpenClaw 的 `import jos` / cmd_login 调用。"""
    if pid == os.getpid():
        return False
    cmd = _process_cmdline(pid).lower()
    if "python" not in cmd:
        return False
    return any(k in cmd for k in ("jos.py", "import jos", "cmd_login"))


def _kill_stale_on_port(port):
    killed = []
    for pid in _pids_listening_on(port):
        if not _is_jos_login_process(pid):
            print(f"端口 {port} 被 PID {pid} 占用（非 jos login，跳过）：{_process_cmdline(pid)}")
            continue
        try:
            os.kill(pid, signal.SIGTERM)
            killed.append(pid)
            print(f"已发送 SIGTERM 至旧 login 进程 PID {pid}")
        except (ProcessLookupError, PermissionError) as e:
            print(f"无法终止 PID {pid}：{e}")
    if killed:
        time.sleep(0.4)
        for pid in killed[:]:
            if pid in _pids_listening_on(port):
                try:
                    os.kill(pid, signal.SIGKILL)
                    print(f"旧 login PID {pid} 未释放端口，已 SIGKILL")
                except (ProcessLookupError, PermissionError):
                    pass
        time.sleep(0.2)
    return killed


def _write_login_session(info):
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(LOGIN_SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    with open(LOGIN_PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(info["pid"]))


def _clear_login_session():
    for p in (LOGIN_SESSION_FILE, LOGIN_PID_FILE):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass


def _read_login_session():
    if not os.path.exists(LOGIN_SESSION_FILE):
        return None
    try:
        with open(LOGIN_SESSION_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _active_login_session():
    """返回仍存活且未超时的 login 会话，避免重复启动造成死循环。"""
    info = _read_login_session()
    if not info:
        return None
    pid = info.get("pid")
    port = info.get("port", DEFAULT_CALLBACK_PORT)
    if not pid or not _pid_alive(pid):
        return None
    if pid not in _pids_listening_on(port):
        return None
    if time.time() - info.get("started_at", 0) > LOGIN_WAIT_SEC:
        return None
    return info


def _append_login_log(msg):
    os.makedirs(CACHE_DIR, exist_ok=True)
    ts = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGIN_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


class _LoginLogRedirect:
    def __init__(self):
        self._orig_out = self._orig_err = None
        self._logf = None

    def __enter__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        self._orig_out, self._orig_err = sys.stdout, sys.stderr
        self._logf = open(LOGIN_LOG_FILE, "a", encoding="utf-8", buffering=1)
        ts = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        self._logf.write(f"\n--- login {ts} PID {os.getpid()} ---\n")
        self._logf.flush()
        sys.stdout = sys.stderr = self._logf
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._logf:
            if exc:
                self._logf.write(f"login 异常退出：{exc}\n")
            self._logf.flush()
            self._logf.close()
        sys.stdout, sys.stderr = self._orig_out, self._orig_err
        return False

    def emit_token(self, token):
        # 仅记录/展示脱敏后的 token；真实 token 已写入 0o600 缓存，供接口调用时读取
        masked = _mask_token(token)
        if self._logf and not self._logf.closed:
            self._logf.write(f"access_token={masked}\n")
            self._logf.flush()
        if self._orig_out:
            print(masked, file=self._orig_out)


def _prepare_port(base_port, kill_stale=True):
    if kill_stale:
        killed = _kill_stale_on_port(base_port)
        if killed:
            print(f"已清理 {len(killed)} 个占用端口 {base_port} 的旧 login 进程")
    blocking = []
    for pid in _pids_listening_on(base_port):
        if _is_jos_login_process(pid):
            continue
        blocking.append((pid, _process_cmdline(pid)))
    return not blocking, blocking


def _build_login_url(state, verifier, redirect_uri=None):
    """调后端 auth_login_url 取授权 URL（后端持凭据拼 URL，并绑定 state->challenge）。

    :param redirect_uri: 同机模式本地回调；沙箱模式传 None / 空（后端不回跳，置就绪供轮询）
    :return: 授权 URL
    """
    challenge = _compute_challenge(verifier)
    data = bff_client.auth_login_url(challenge, state, local_redirect=redirect_uri)
    if not isinstance(data, dict) or not data.get("authorizeUrl"):
        raise RuntimeError(f"后端未返回授权 URL：{json.dumps(data, ensure_ascii=False)[:200]}")
    return data["authorizeUrl"]


def _reuse_or_none(args):
    if getattr(args, "force", False):
        return None
    existing = _active_login_session()
    if not existing:
        return None
    _append_login_log(f"复用已有 login PID {existing['pid']} state={existing['state']}")
    print(existing["url"])
    print(f"已有 login 回调服务运行中 PID {existing['pid']}（state={existing['state']}），未重复启动。")
    print(f"强制重启：python3 jos.py login --force --kill-stale")
    print(f"日志：{LOGIN_LOG_FILE}")
    # 复用路径也唤起浏览器，避免用户需手动打开 URL
    try:
        webbrowser.open(existing["url"])
    except Exception:
        pass
    return existing


def _login_blocking(args):
    reused = _reuse_or_none(args)
    if reused:
        return
    with _LoginLogRedirect() as log_ctx:
        _login_blocking_impl(args, log_ctx)


def _login_blocking_impl(args, log_ctx):
    state = _gen_state()
    verifier = _gen_verifier()
    cb = urlparse(REDIRECT_URI)
    base_port = cb.port or DEFAULT_CALLBACK_PORT
    cb_path = cb.path or "/callback"
    kill_stale = not getattr(args, "no_kill_stale", False)

    ok, blocking = _prepare_port(base_port, kill_stale=kill_stale)
    if not ok:
        for pid, cmd in blocking:
            print(f"端口 {base_port} 被 PID {pid} 占用（非 jos login）：{cmd}")
        print(f"请先 kill {blocking[0][0]} 或 lsof -nP -iTCP:{base_port} -sTCP:LISTEN")
        sys.exit(1)

    result = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            # /health 健康检查：回调页前端用于探测本地服务是否就绪
            if parsed.path == "/health":
                self._reply_json(200, {"status": "ok", "state": state})
                return
            print(f"收到回调：{self.path}（期望 state={state}）")
            if parsed.path != cb_path:
                self._reply(404, "Not Found")
                return
            qs = parse_qs(parsed.query)
            recv_state = (qs.get("state") or [""])[0]
            # PKCE：后端回调仅带 state 作完成信号，authCode 不出后端（不再期待 code）。
            if not recv_state:
                self._reply(400, "缺少授权参数，请从授权页完成登录")
                print("收到空回调探活请求，继续等待…")
                return
            if recv_state != state:
                self._reply(403, "403 Forbidden: state 校验失败（与发起授权时不一致）")
                print(f"state 不匹配：收到 {recv_state!r}，期望 {state!r}，继续等待…")
                return
            result["ready"] = True
            self._reply_html(200, _SUCCESS_HTML)

        def _reply(self, status, msg):
            body = msg.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _reply_html(self, status, html):
            body = html.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _reply_json(self, status, obj):
            body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, fmt, *args):
            print(f"[HTTP] {self.address_string()} - {fmt % args}")

    class V4Server(HTTPServer):
        allow_reuse_address = True

    def _try_bind(port):
        if _pids_listening_on(port):
            raise OSError(f"127.0.0.1:{port} 仍被 PID {_pids_listening_on(port)} 监听")
        return V4Server(("127.0.0.1", port), Handler), "IPv4 127.0.0.1"

    httpd = bind_desc = None
    port = base_port
    for port in range(base_port, base_port + 100):
        try:
            httpd, bind_desc = _try_bind(port)
            break
        except OSError as e:
            print(f"端口 {port} 绑定失败：{e}")
    if httpd is None:
        print(f"端口 {base_port}~{base_port + 99} 均无法绑定")
        sys.exit(1)

    httpd.timeout = 1
    redirect_uri = f"{cb.scheme}://{_callback_host(cb.hostname)}:{port}{cb_path}"
    url = _build_login_url(state, verifier, redirect_uri)
    if port != base_port:
        print(f"端口 {base_port} 不可用，已改用 {port}（须确保后端 localRedirect 校验放行该端口）")

    _write_login_session({
        "pid": os.getpid(), "port": port, "redirect_uri": redirect_uri,
        "state": state, "verifier": verifier, "url": url, "started_at": int(time.time()),
    })
    # 统一写入 auth-session.json，确保 exchange 兜底可读
    _write_auth_session(state, verifier, mode="local", authorize_url=url,
                        callback_port=port, daemon_pid=os.getpid())

    print("请在浏览器完成授权（未自动打开则手动访问以下链接）：")
    print(url)
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    print(f"本地回调服务已启动：{redirect_uri}（{bind_desc}，PID {os.getpid()}，state={state}，等待 {LOGIN_WAIT_SEC}s）…")
    deadline = time.time() + LOGIN_WAIT_SEC
    while "ready" not in result and time.time() < deadline:
        httpd.handle_request()
    print("本地回调服务已关闭")
    httpd.server_close()
    _clear_login_session()

    if "ready" not in result:
        print("⏳ 本地回调超时：未在限定时间内收到有效授权回调。")
        print("可能原因：后端未 302 回跳本地（预发环境常见）、或用户未完成授权。")
        print(f"👉 若用户已在浏览器完成授权，请执行: python3 jos.py exchange")
        sys.exit(10)  # 非致命，可通过手动 exchange 恢复

    print("授权完成，开始换取 access_token…")
    at, err_code = _exchange(state, verifier)
    if not at:
        sys.exit(err_code or 1)
    log_ctx.emit_token(at)
    if load_pending_holdings():
        print("登录成功。")


def _exchange(state, verifier):
    """凭 state + code_verifier 调后端换 access_token（authCode 不出后端）。

    返回 (access_token, None) 成功，或 (None, exit_code) 失败。
    退出码语义：11=会话过期, 12=verifier不匹配, 13=授权未完成, 14=网络异常, 15=风控限流
    """
    try:
        data = bff_client.auth_exchange(state, verifier)
    except bff_client.BffError as e:
        # 错误分类
        msg_lower = (e.message or "").lower()
        if e.code == 403 or "限制" in (e.message or "") or "频繁" in (e.message or ""):
            print(f"⚠️ 风控限流（等待 120s 后重试）: {e.message}")
            return None, 15
        elif "不存在" in (e.message or "") or "过期" in (e.message or "") or "expired" in msg_lower:
            print(f"❌ 会话过期（需重新 login-auto）: {e.message}")
            return None, 11
        elif "校验" in (e.message or "") or "verifier" in msg_lower or "challenge" in msg_lower:
            print(f"❌ verifier 不匹配（需重新 login-auto）: {e.message}")
            return None, 12
        elif "未完成" in (e.message or "") or "pending" in msg_lower or "not ready" in msg_lower:
            print(f"⏳ 授权尚未完成（稍后重试 exchange）")
            return None, 13
        else:
            print(f"❌ 兑换失败: code={e.code} msg={e.message}")
            return None, 14
    except (urllib.error.URLError, OSError, TimeoutError) as e:
        print(f"❌ 网络异常（自动重试中）: {e}")
        return None, 14
    if not isinstance(data, dict) or not data.get("accessToken"):
        print(f"❌ 换 token 失败，响应: {_mask_in_text(json.dumps(data, ensure_ascii=False)[:200])}")
        return None, 14
    # 后端返回字段为 camelCase，转换为本地缓存兼容字段（refresh_token 不再下发）
    # ⚠️ 后端 expiresIn 单位为「毫秒」，原值存储，剩余时长计算时在读取端统一归一（见 _expires_sec_of）
    tok = {
        "access_token": data.get("accessToken"),
        "expires_in": data.get("expiresIn"),
        "token_type": data.get("tokenType") or "Bearer",
    }
    _save_token(tok)
    _clear_auth_session()
    return tok["access_token"], None


# ── 统一 auth-session 管理（替代 login-session.json + oauth-state.json 双文件）──

def _write_auth_session(state, verifier, mode, authorize_url, **kwargs):
    """统一写入 auth-session.json，所有模式共用。"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    session = {
        "state": state,
        "verifier": verifier,
        "mode": mode,  # "local" | "sandbox"
        "authorize_url": authorize_url,
        "created_at": int(time.time()),
        "ttl_sec": 600,  # 10分钟过期
    }
    session.update(kwargs)
    with open(AUTH_SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)
    os.chmod(AUTH_SESSION_FILE, 0o600)
    return session


def _read_auth_session():
    """读取 auth-session.json，兼容旧的 oauth-state.json 和 login-session.json。"""
    # 优先读统一文件
    if os.path.exists(AUTH_SESSION_FILE):
        try:
            with open(AUTH_SESSION_FILE, encoding="utf-8") as f:
                sess = json.load(f)
            # TTL 检查
            created = sess.get("created_at", 0)
            ttl = sess.get("ttl_sec", 600)
            if time.time() - created > ttl:
                return None, "session_expired"
            return sess, None
        except Exception:
            pass
    # 兼容旧 oauth-state.json
    old_oauth = os.path.join(CACHE_DIR, "oauth-state.json")
    if os.path.exists(old_oauth):
        try:
            with open(old_oauth, encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("state") and cached.get("verifier"):
                created = cached.get("created_at", 0)
                if time.time() - created <= 600:
                    return cached, None
                return None, "session_expired"
        except Exception:
            pass
    # 兼容旧 login-session.json
    if os.path.exists(LOGIN_SESSION_FILE):
        try:
            with open(LOGIN_SESSION_FILE, encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("state") and cached.get("verifier"):
                created = cached.get("started_at", 0)
                if time.time() - created <= 600:
                    return cached, None
                return None, "session_expired"
        except Exception:
            pass
    return None, "no_session"


def _clear_auth_session():
    """清理所有 auth session 文件。"""
    for p in (AUTH_SESSION_FILE,
              os.path.join(CACHE_DIR, "oauth-state.json"),
              LOGIN_SESSION_FILE, LOGIN_PID_FILE):
        try:
            os.remove(p)
        except FileNotFoundError:
            pass


def _oauth_state_file():
    return os.path.join(CACHE_DIR, "oauth-state.json")


def _write_success_page():
    """将登录成功页落地为本地 HTML 文件，供沙箱模式下用户按需打开确认。

    返回文件路径；写入失败时返回 None（不影响登录主流程）。
    """
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        path = os.path.join(CACHE_DIR, "login-success.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(_SUCCESS_HTML)
        return path
    except Exception:
        return None


def cmd_oauth_url(_):
    """沙箱两步走第一步：生成授权链接，缓存 state+verifier 供 exchange 使用。

    沙箱模式下用户浏览器与 Agent 不同机，本地回调 127.0.0.1 不可达。
    因此**不传 localRedirect**：后端授权完成后不做 302 回跳（改置就绪态供 exchange 主动兑换），
    用户在京东授权页原地看到「授权完成」，绝不会被重定向到不可达的本地回调而看到浏览器报错页。
    """
    state = _gen_state()
    verifier = _gen_verifier()
    url = _build_login_url(state, verifier, redirect_uri=None)
    # 统一写入 auth-session.json
    _write_auth_session(state, verifier, mode="sandbox", authorize_url=url)
    # 兼容：同时写旧格式文件（过渡期）
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(_oauth_state_file(), "w", encoding="utf-8") as f:
        json.dump({"state": state, "verifier": verifier, "created_at": int(time.time())}, f)
    os.chmod(_oauth_state_file(), 0o600)
    print(url)


def cmd_exchange(args):
    """兑换 token：统一读取 auth-session.json（兼容旧文件），支持重试。

    退出码：0=成功, 11=会话过期, 12=verifier不匹配, 13=授权未完成, 14=网络异常, 15=风控限流
    """
    state = getattr(args, "state", None) or ""
    verifier = getattr(args, "verifier", None) or ""
    retry_count = int(getattr(args, "retry", None) or 3)
    backoff_sec = int(getattr(args, "backoff", None) or 5)

    # 统一从 auth-session.json 读取（兼容旧文件）
    if not state or not verifier:
        sess, err_reason = _read_auth_session()
        if sess:
            state = state or sess.get("state", "")
            verifier = verifier or sess.get("verifier", "")
        elif err_reason == "session_expired":
            print("❌ 授权会话已过期（超过 10 分钟），请重新执行 login-auto。", file=sys.stderr)
            sys.exit(11)

    if not state or not verifier:
        print("❌ 缺少 state / verifier，请先执行 login-auto 生成授权链接。", file=sys.stderr)
        sys.exit(1)

    # 带重试的兑换
    last_err_code = 1
    for attempt in range(1, retry_count + 1):
        at, err_code = _exchange(state, verifier)
        if at:
            _write_success_page()
            print(_mask_token(at))
            print("登录成功 ✅")
            return
        last_err_code = err_code or 1
        # 仅网络异常(14)和授权未完成(13)值得重试
        if err_code not in (13, 14):
            break
        if attempt < retry_count:
            wait = backoff_sec * attempt
            print(f"  第 {attempt}/{retry_count} 次失败，{wait}s 后重试…")
            time.sleep(wait)

    sys.exit(last_err_code)


def cmd_stop(_):
    if os.path.exists(LOGIN_PID_FILE):
        with open(LOGIN_PID_FILE, encoding="utf-8") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"已停止 login PID {pid}")
        except ProcessLookupError:
            print(f"PID {pid} 已不存在")
    else:
        print("无后台 login 进程")
    _clear_login_session()


def _detect_env():
    """自动探测运行环境，返回 'local' 或 'sandbox'。

    判定「沙箱」（Agent 与用户浏览器不同机，本地 127.0.0.1 回调不可达）的信号：
    - 显式声明：GOLD_JD_ENV=sandbox / local（最高优先级，便于强制覆盖）
    - SSH 远程会话（SSH_CONNECTION / SSH_TTY 存在）
    - 容器环境（/.dockerenv 存在 或 常见容器编排环境变量）
    - 无本机浏览器可拉起（webbrowser 找不到可用浏览器）
    命中任一沙箱信号即判沙箱；否则视为本地同机。
    """
    forced = (os.environ.get("GOLD_JD_ENV") or "").strip().lower()
    if forced in ("sandbox", "remote"):
        return "sandbox"
    if forced in ("local", "same-machine"):
        return "local"
    if os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY"):
        return "sandbox"
    if os.path.exists("/.dockerenv"):
        return "sandbox"
    if os.environ.get("KUBERNETES_SERVICE_HOST") or os.environ.get("CODESPACES"):
        return "sandbox"
    try:
        webbrowser.get()
    except Exception:
        return "sandbox"
    return "local"


def _redirect_is_local():
    """判断 REDIRECT_URI 是否指向本机（127.0.0.1 / localhost）。
    当用户通过 GOLD_JD_REDIRECT_URI 指定外部域名（如 msinner.jr.jd.com）时返回 False。
    """
    cb = urlparse(REDIRECT_URI)
    host = (cb.hostname or "").lower()
    return host in ("127.0.0.1", "localhost", "::1")


def cmd_login_auto(args):
    """统一登录入口：脚本自动探测环境并选择正确的登录模式，杜绝调用方误选。

    - --force：忽略现有 token，强制重新授权（内部自动清缓存）。
    - 已登录且非 force：直接输出「登录成功 ✅」（幂等）。
    - 本地同机 + 本机回调：走 daemon 模式（本地回调 127.0.0.1 可达，自动拉浏览器）。
    - 本地同机 + 外部回调域名：走本地轮询模式（自动拉浏览器 + 轮询 exchange，无需 hosts）。
    - 远端沙箱：走 oauth-url（不传本地回调），提示 exchange 兑换。

    退出码：0=已登录 / 10=等待授权（URL 已输出）
    """
    force = getattr(args, "force", False)
    if not force:
        logged_in, _info = check_token()
        if logged_in:
            print("登录成功 ✅")
            return
    else:
        # force 模式：清除旧 token 和 session（含系统级加密存储中的 token）
        secure_store.delete_secret(TOKEN_SECRET_NAME)
        for f in (TOKEN_FILE, SESSION_PIN_FILE):
            try:
                os.remove(f)
            except FileNotFoundError:
                pass
    env = _detect_env()
    if env == "local":
        if _redirect_is_local():
            # 回调域名指向本机，走经典 daemon 模式（本地 HTTP 回调）
            setattr(args, "daemon", True)
            setattr(args, "kill_stale", True)
            return cmd_login(args)
        else:
            # 回调域名指向外部（如 msinner.jr.jd.com），走本地轮询模式
            return _login_local_poll(args)
    # sandbox：生成授权链接（内部不传本地回调），提示两步走
    cmd_oauth_url(args)
    print("[内部] 沙箱模式：请将上方授权链接发给用户完成授权，随后执行 exchange 兑换。")
    sys.exit(10)


def _login_local_poll(args):
    """本地轮询模式：回调域名非本机时使用。

    场景：环境为 local（可拉浏览器），但 GOLD_JD_REDIRECT_URI 指向外部域名
    （如 msinner.jr.jd.com），后端302回跳无法到达本地回调服务。

    流程：
    1. 生成授权URL（传入 REDIRECT_URI 作为 localRedirect）
    2. 自动打开浏览器
    3. 轮询 exchange 直到授权完成或超时（默认 180s）
    """
    state = _gen_state()
    verifier = _gen_verifier()
    # 传入 REDIRECT_URI 让后端302到该域名（而非127.0.0.1）
    url = _build_login_url(state, verifier, redirect_uri=REDIRECT_URI)
    _write_auth_session(state, verifier, mode="local-poll", authorize_url=url,
                        redirect_uri=REDIRECT_URI)

    print(f"本地轮询模式：回调域名 {urlparse(REDIRECT_URI).hostname} 不指向本机，"
          f"将轮询 exchange 等待授权完成。")
    print("请在浏览器完成授权（未自动打开则手动访问以下链接）：")
    print(url)
    no_browser = getattr(args, "no_browser", False)
    if not no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    # 轮询 exchange（授权未完成=13，每3秒重试，最多180秒）
    poll_interval = 3
    max_wait = 180
    deadline = time.time() + max_wait
    attempt = 0
    print(f"轮询开始（每 {poll_interval}s 检查一次，最长等待 {max_wait}s）…")
    while time.time() < deadline:
        attempt += 1
        at, err_code = _exchange(state, verifier)
        if at:
            print(_mask_token(at))
            print("登录成功 ✅")
            return
        # 仅「授权未完成(13)」和「网络异常(14)」值得继续轮询
        if err_code not in (13, 14):
            print(f"❌ 兑换失败（错误码 {err_code}），轮询终止。")
            sys.exit(err_code or 1)
        if time.time() + poll_interval < deadline:
            time.sleep(poll_interval)

    print(f"⏳ 轮询超时（{max_wait}s 内未完成授权）。")
    print(f"👉 若用户已在浏览器完成授权，请执行: python3 jos.py exchange")
    sys.exit(10)


def cmd_login(args):
    if _reuse_or_none(args):
        return
    if getattr(args, "daemon", False):
        os.makedirs(CACHE_DIR, exist_ok=True)
        _append_login_log("daemon 启动子进程")
        child_args = [sys.executable, os.path.abspath(__file__), "login", "--no-browser"]
        if getattr(args, "kill_stale", False):
            child_args.append("--kill-stale")
        if getattr(args, "force", False):
            child_args.append("--force")
        proc = subprocess.Popen(
            child_args, start_new_session=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        for _ in range(50):
            time.sleep(0.1)
            info = _read_login_session()
            if info and info.get("pid") == proc.pid and info.get("url"):
                _append_login_log(f"daemon 就绪 PID {proc.pid}")
                print(info["url"])
                print(f"后台回调服务 PID {proc.pid}：{info['redirect_uri']}")
                print(f"日志：{LOGIN_LOG_FILE}")
                print(f"停止：python3 jos.py stop")
                # daemon 模式：子进程 --no-browser，父进程负责唤起浏览器
                try:
                    webbrowser.open(info["url"])
                except Exception:
                    pass
                return
            if proc.poll() is not None:
                break
        print(f"后台启动失败，见 {LOGIN_LOG_FILE}")
        sys.exit(1)
    _login_blocking(args)


def cmd_refresh(_):
    # TODO: 等后端 cf-gold-ai 实现 /oauth/refresh 后再接入；当前提示用户重新登录。
    print("当前版本不支持 token 刷新，请重新登录。", file=sys.stderr)
    sys.exit(1)


def check_token():
    """非退出式登录检查。返回 (logged_in: bool, info: dict)。

    Token 过期暂不自动刷新（待后端 ``/oauth/refresh`` 接口就绪），
    过期视为未登录，由调用方引导重新授权。
    info 中 warning 字段用于提前预警即将过期。
    """
    tok = _load_token()
    if not tok:
        return False, {"reason": "not_logged_in"}
    if _is_expired(tok):
        return False, {"reason": "expired"}
    info = {
        "access_token": tok["access_token"],
        "uid": tok.get("uid"),
        "open_id": tok.get("open_id"),
    }
    # 过期预警：剩余不足 1 天
    remaining = _remaining_sec(tok)
    if remaining is not None and remaining < 86400:
        info["warning"] = "token_expiring_soon"
        info["remaining_sec"] = remaining
    return True, info


def _remaining_sec(tok):
    """返回 token 剩余有效秒数，无法计算时返回 None。"""
    try:
        exp = int(tok.get("_obtained_at", 0)) + _expires_sec_of(tok)
        return max(0, exp - int(time.time()))
    except Exception:
        return None


def _valid_access_token():
    ok, info = check_token()
    if not ok:
        print("未登录"); sys.exit(2)
    return info["access_token"]


def get_login_auth_url():
    """返回进行中的或新建的授权链接（不阻塞等待回调）。

    新建时不绑定本地回调（沙箱风格）：生成 state+verifier 并缓存，
    供后续 exchange 兑换；authCode 不回传客户端。
    """
    existing = _active_login_session()
    if existing and existing.get("url"):
        return existing["url"], "reuse"
    state = _gen_state()
    verifier = _gen_verifier()
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(_oauth_state_file(), "w", encoding="utf-8") as f:
        json.dump({"state": state, "verifier": verifier, "created_at": int(time.time())}, f)
    os.chmod(_oauth_state_file(), 0o600)
    url = _build_login_url(state, verifier, redirect_uri=None)
    return url, "new"


def start_login_daemon():
    """后台启动 login 回调服务，返回授权 URL。"""
    existing = _active_login_session()
    if existing and existing.get("url"):
        return existing["url"]
    child_args = [sys.executable, os.path.abspath(__file__), "login", "--daemon", "--kill-stale"]
    proc = subprocess.Popen(
        child_args, start_new_session=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    for _ in range(50):
        time.sleep(0.1)
        info = _read_login_session()
        if info and info.get("pid") == proc.pid and info.get("url"):
            return info["url"]
        if proc.poll() is not None:
            break
    raise RuntimeError(f"login 后台启动失败，见 {LOGIN_LOG_FILE}")


def save_pending_holdings(payload):
    os.makedirs(CACHE_DIR, exist_ok=True)
    payload["saved_at"] = int(time.time())
    with open(PENDING_HOLDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def load_pending_holdings():
    if not os.path.exists(PENDING_HOLDINGS_FILE):
        return None
    try:
        with open(PENDING_HOLDINGS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def clear_pending_holdings():
    try:
        os.remove(PENDING_HOLDINGS_FILE)
    except FileNotFoundError:
        pass


def wait_for_token(timeout_sec=300, poll_sec=2):
    """轮询直到 token 可用或超时。返回 (ok, info)。"""
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        ok, info = check_token()
        if ok:
            return True, info
        time.sleep(poll_sec)
    return False, {"reason": "login_timeout"}


def _cache_session_pin(pin, uid=None):
    if not pin:
        return
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(SESSION_PIN_FILE, "w", encoding="utf-8") as f:
        json.dump({"pin": pin, "uid": uid, "cached_at": int(time.time())}, f, ensure_ascii=False, indent=2)


def get_session_pin():
    """获取当前登录会话 pin。

    优先读取本地缓存；BFF 暂未提供独立 pin 反查接口，未缓存时返回 (None, uid)，
    由具体业务接口在响应中携带 pin 时回填缓存（见 ``fetch_holdings``）。
    """
    if os.path.exists(SESSION_PIN_FILE):
        try:
            with open(SESSION_PIN_FILE, encoding="utf-8") as f:
                cached = json.load(f)
            if cached.get("pin"):
                return cached["pin"], cached.get("uid")
        except Exception:
            pass
    ok, info = check_token()
    if not ok:
        return None, info.get("uid")
    return None, info.get("uid")


def cmd_token(args):
    # 校验登录态（退出码 0=已登录 / 2=未登录）；回显脱敏值，不暴露明文。
    # --json：额外输出剩余有效期，供本地托管脚本判断“还能托管多久”。
    if getattr(args, "json", False):
        ok, info = check_token()
        tok = _load_token() or {}
        remaining = _remaining_sec(tok) if ok else 0
        out = {
            "logged_in": ok,
            "reason": info.get("reason") if not ok else None,
            "remaining_sec": remaining,
            "remaining_human": _humanize_duration(remaining),
        }
        print(json.dumps(out, ensure_ascii=False))
        sys.exit(0 if ok else 2)
    print(_mask_token(_valid_access_token()))


def _humanize_duration(sec):
    """把剩余秒数转成大白话，如 '约 2 天 3 小时' / '约 45 分钟' / '已过期'。"""
    try:
        sec = int(sec)
    except Exception:
        return "未知"
    if sec <= 0:
        return "已过期"
    days, rem = divmod(sec, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days > 0:
        return f"约 {days} 天 {hours} 小时" if hours else f"约 {days} 天"
    if hours > 0:
        return f"约 {hours} 小时 {minutes} 分钟" if minutes else f"约 {hours} 小时"
    return f"约 {minutes} 分钟"


def fetch_holdings():
    """查询当前账号持仓/收益。"""
    access_token = _valid_access_token()
    try:
        data = bff_client.get(bff_client.PATH_HOLDINGS_QUERY, {"accessToken": access_token})
    except bff_client.BffError as e:
        raise
    if not isinstance(data, dict):
        raise RuntimeError("持仓响应格式异常")
    # 若响应体中带 pin，顺手缓存
    pin = data.get("pin") or data.get("sessionPin")
    if pin:
        _cache_session_pin(pin)
    return data


def cmd_holdings(args):
    import holdings_entry
    text = getattr(args, "text", None) or "查询持仓和收益"
    return holdings_entry.run(
        text, "both",
        wait_login=getattr(args, "wait_login", False),
        json_out=getattr(args, "json", False),
        resume=False,
    )


def cmd_morning_report(args):
    import query_morning_report
    query_morning_report.main(["--json"] if getattr(args, "json", False) else [])


def cmd_price(args):
    import query_price_jhub
    argv = []
    if getattr(args, "json", False):
        argv.append("--json")
    if getattr(args, "analyze", False):
        argv.append("--analyze")
    if getattr(args, "parse", None):
        argv.extend(["--parse", args.parse])
    elif getattr(args, "bank", None):
        argv.extend(["--bank", args.bank])
    elif getattr(args, "unique_code", None):
        argv.append(args.unique_code)
    rc = query_price_jhub.main(argv)
    if isinstance(rc, int) and rc != 0:
        sys.exit(rc)


def cmd_news_flash(args):
    import query_news_flash
    argv = []
    if getattr(args, "json", False):
        argv.append("--json")
    if getattr(args, "tag_id", None):
        argv.extend(["--tag-id", str(args.tag_id)])
    if getattr(args, "page_size", None):
        argv.extend(["--page-size", str(args.page_size)])
    query_news_flash.main(argv)


def cmd_trade_records(args):
    import query_trade_records
    argv = []
    if getattr(args, "json", False):
        argv.append("--json")
    if getattr(args, "type", None):
        argv.extend(["--type", args.type])
    if getattr(args, "start_date", None):
        argv.extend(["--start-date", args.start_date])
    if getattr(args, "end_date", None):
        argv.extend(["--end-date", args.end_date])
    if getattr(args, "page_size", None):
        argv.extend(["--page-size", str(args.page_size)])
    if getattr(args, "sum_only", False):
        argv.append("--sum-only")
    if getattr(args, "list_only", False):
        argv.append("--list-only")
    query_trade_records.main(argv)


def main():
    p = argparse.ArgumentParser()
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    sub = p.add_subparsers(dest="cmd", required=True)
    lg = sub.add_parser("login", parents=[common])
    lg.add_argument("--no-browser", action="store_true")
    lg.add_argument("--daemon", action="store_true")
    lg.add_argument("--kill-stale", action="store_true")
    lg.add_argument("--no-kill-stale", action="store_true")
    lg.add_argument("--force", action="store_true", help="强制重启（忽略已有 login 会话）")
    la = sub.add_parser("login-auto", parents=[common], help="统一登录入口：自动探测环境并选对模式（推荐调用方只用此命令）")
    la.add_argument("--no-browser", action="store_true")
    la.add_argument("--kill-stale", action="store_true")
    la.add_argument("--force", action="store_true")
    sub.add_parser("stop", parents=[common])
    sub.add_parser("oauth-url", parents=[common])
    ex = sub.add_parser("exchange", parents=[common], help="兑换 token（自动读取 auth-session，支持重试）")
    ex.add_argument("--state", default="", help="授权 state（缺省读 auth-session 缓存）")
    ex.add_argument("--verifier", default="", help="PKCE code_verifier（缺省读 auth-session 缓存）")
    ex.add_argument("--retry", type=int, default=3, help="网络异常/未就绪时重试次数（默认 3）")
    ex.add_argument("--backoff", type=int, default=5, help="重试退避基数秒（默认 5，第 N 次等 N*5s）")
    sub.add_parser("refresh", parents=[common])
    tk = sub.add_parser("token", parents=[common])
    tk.add_argument("--json", action="store_true",
                    help="输出登录态与剩余有效期（JSON），供托管脚本读取")
    hd = sub.add_parser("holdings", parents=[common])
    hd.add_argument("--json", action="store_true", help="输出原始 JSON")
    hd.add_argument("--wait-login", action="store_true", help="未登录时等待授权后自动查询")
    mr = sub.add_parser("morning-report", parents=[common])
    mr.add_argument("--json", action="store_true", help="输出原始 JSON")
    pr = sub.add_parser("price", parents=[common])
    pr.add_argument("unique_code", nargs="?", default="WG-JDAU", help="证券唯一码（默认 WG-JDAU）")
    pr.add_argument("--parse", "-p", help="从用户原文解析金价标的")
    pr.add_argument("--bank", help="按银行 code 查询（如 CMBC、CZB）")
    pr.add_argument("--json", action="store_true", help="输出原始 JSON")
    pr.add_argument("--analyze", "-a", action="store_true", help="输出金价走势分析")
    nf = sub.add_parser("news-flash", parents=[common])
    nf.add_argument("--json", action="store_true", help="输出原始 JSON")
    nf.add_argument("--tag-id", type=int, default=20225, help="场景ID（默认20225黄金资讯流）")
    nf.add_argument("--page-size", type=int, default=10, help="每页条数")
    tr = sub.add_parser("trade-records", parents=[common])
    tr.add_argument("--json", action="store_true", help="输出原始 JSON")
    tr.add_argument("--type", "-t", default="", help="交易类型过滤(BUY_GOLD/SELL_GOLD等)")
    tr.add_argument("--start-date", default="", help="起始日期(YYYY-MM-DD)")
    tr.add_argument("--end-date", default="", help="结束日期(YYYY-MM-DD)")
    tr.add_argument("--page-size", type=int, default=10, help="每页条数")
    tr.add_argument("--sum-only", action="store_true", help="仅查询汇总")
    tr.add_argument("--list-only", action="store_true", help="仅查询订单列表")
    args = p.parse_args()
    bff_client.set_claw(getattr(args, "claw", None))
    handlers = {"login": cmd_login, "stop": cmd_stop, "oauth-url": cmd_oauth_url, "exchange": cmd_exchange,
                "login-auto": cmd_login_auto,                "refresh": cmd_refresh, "token": cmd_token, "holdings": cmd_holdings,
                "morning-report": cmd_morning_report, "price": cmd_price, "news-flash": cmd_news_flash,
                "trade-records": cmd_trade_records}
    rc = handlers[args.cmd](args)
    if isinstance(rc, int) and rc != 0:
        sys.exit(rc)


if __name__ == "__main__":
    main()
