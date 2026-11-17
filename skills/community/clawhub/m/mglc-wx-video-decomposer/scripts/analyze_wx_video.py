#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频号视频拆解（曼格云 API 版）。

接收一条视频号分享链接 **或** 本地视频文件，自动完成：
  分享链接 → 作品资料（元信息+媒体+互动，接口33）
           → 下载 playbackUrl + ISAAC64 解密前 128KiB
           → 临时上传换 fileUrl
           → 视频视觉理解 decompose（接口27）
           → 渲染综合 Markdown 报告
  本地视频   → 临时上传换 fileUrl
           → 视频视觉理解 decompose
           → 渲染报告（仅有视觉部分）

进度打到 stderr 供调用方转述，最终报告用分隔符包裹打到 stdout。
纯标准库实现（urllib / http.client），无第三方依赖。

用法：
    python3 analyze_wx_video.py "<分享链接>"
    python3 analyze_wx_video.py "<本地视频路径>"
    python3 analyze_wx_video.py --balance
    python3 analyze_wx_video.py "<输入>" --mode decompose --format all --out report.md
    python3 analyze_wx_video.py --render wm_video_raw.json --analysis wm_analysis.json
        （零 API 调用重渲染：注入 AI 分析层，重新生成三种格式报告）

工作流（两阶段）：
    阶段1 采集：analyze_wx_video.py "<输入>" —— 调 API 拿数据，落地
          wm_video_raw.json（含 info/analysis/billing），并输出基础报告。
    阶段2 分析+渲染：assistant 依据 raw 数据按 references/analysis-schema.md
          写 wm_analysis.json，然后 --render 重渲染，把深度分析（受众画像/
          爆款归因/六维评分/运营建议等）注入 Markdown/Excel/HTML，零扣费。

输出格式（--format）：
    markdown  仅输出 Markdown 报告
    excel     仅输出 .xlsx 文件（6 个 sheet）
    html      仅输出 HTML 结果看板
    all       同时生成三种（默认）

API Key：
    自动从「技能目录」下的 config.json 的 WM_API_KEY 字段读取
    （技能目录 = scripts/ 的上一级，即 SKILL.md 所在目录）。
    兼容环境变量 WM_API_KEY 作为回退。

base url 默认 https://api.we-media.cn（写死在脚本里）。

退出码：
    0   成功，报告已输出
    2   输入错误（未给输入 / 链接格式不符 / 文件不存在 / 超限）
    3   未取到 API Key 或鉴权失效（401/403）
    4   API 业务失败（code≠OK：余额不足等）
    5   视觉理解失败
    6   网络错误（下载失败等）
    7   视觉分析为空
    9   上传失败
    124 超时

============================================================================
接口契约 —— 与 references/api.md 一一对应
============================================================================
"""

import argparse
import hashlib
import http.client
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse
from platform_contract import USER_AGENT, identity_headers, failure, catalog, price_micros, product_path

BASE_URL = "https://api.we-media.cn"

# --- 接口路径 --------------------------------------------------------------
PATH_BALANCE = "/openapi/account-balance/"
PATH_INFO = "/openapi/wechat-native-channel-info/videos/info"
PATH_TICKET = "/api/v1/file-uploads/ticket"
PATH_ANALYZE = "/openapi/video-understanding/analyze"

PREFIX_BYTES = 128 * 1024  # 131072
MAX_VIDEO_BYTES = 128 * 1024 * 1024  # 128 MiB
HTTP_TIMEOUT = 120  # 秒
DOWNLOAD_TIMEOUT = 90  # 秒
UPLOAD_TIMEOUT = 600  # 秒
ANALYZE_TIMEOUT = 600  # 秒
REPORT_START = "=== WM_VIDEO_REPORT_START ==="
REPORT_END = "=== WM_VIDEO_REPORT_END ==="

SHARE_URL_RE = re.compile(
    r"^https://(?:(?:weixin\.qq\.com|channels\.weixin\.qq\.com)/sph/[A-Za-z0-9_-]{1,512}"
    r"|channels\.weixin\.qq\.com/finder-preview/pages/(?:sph\?id=[A-Za-z0-9_-]{4,256}"
    r"|feed\?eid=export/[A-Za-z0-9_-]{1,505}&token=0&is_fallback=1))$"
)
SUPPORTED_EXTS = {".mp4", ".mov", ".m4v", ".avi", ".mkv", ".webm", ".flv", ".wmv"}
CST = timezone(timedelta(hours=8))  # 北京时间

# --- 付费接口响应缓存 --------------------------------------------------------
# 目的：重试时不重复扣费。付费接口（作品资料、视觉理解）成功响应写入本地缓存，
# 后续对同一请求（path + 请求体）直接复用，不再调用接口、不再扣费。
# 仅缓存 code==OK 的成功响应；失败响应不缓存，以便修正后能真正重跑。
CACHE_TTL_SECONDS = 24 * 3600  # 缓存有效期 24 小时
CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".cache")
# 需要缓存的付费接口（按 path 匹配）
CACHEABLE_PATHS = {PATH_INFO, PATH_ANALYZE}
# 通过环境变量关闭：WM_VIDEO_CACHE=0
CACHE_ENABLED = os.environ.get("WM_VIDEO_CACHE", "0") == "1"

# --- 瞬时故障重试 ------------------------------------------------------------
# 上游（阶跃视觉理解）偶发不可用/返回格式异常。这类错误平台会退回费用，
# 因此自动退避重试是安全的。鉴权、参数等业务性错误不重试。
RETRY_TIMES = 4                       # 总尝试次数（1 次首发 + 3 次重试）
RETRY_BACKOFF = [8, 20, 45]           # 每次重试前的等待秒数
TRANSIENT_CODES = {
    "UPSTREAM_UNAVAILABLE",
    "INVALID_UPSTREAM_RESPONSE",
    "UPSTREAM_TIMEOUT",
    "SERVICE_UNAVAILABLE",
    "INTERNAL_ERROR",
    "RATE_LIMITED",
    "TOO_MANY_REQUESTS",
    # 前一次请求已失败时，服务端拒绝复用同一 Idempotency-Key；
    # 重试时会换新 key，因此这类失败同样可安全重试。
    "IDEMPOTENT_REQUEST_FAILED",
}

# ---------------------------------------------------------------------------
# 日志 / 退出
# ---------------------------------------------------------------------------

def log(*args, **kwargs):
    print(*args, file=sys.stderr, flush=True, **kwargs)

def fail(code, message):
    log(message)
    sys.exit(code)

# ===========================================================================
# ISAAC64 — 纯 Python 实现（移植自 finder-decrypt.mjs）
# ===========================================================================

class Isaac64:
    """ISAAC64 伪随机数生成器，用于视频号 Finder 首段解密。

    使用 Python 原生任意精度整数实现 64 位无符号运算，
    不依赖原生扩展或额外运行时资源。
    """
    MASK = (1 << 64) - 1
    GOLDEN = 0x9E3779B97F4A7C13

    def __init__(self, key):
        self.rand_count = 255
        self.seed = [0] * 256
        self.memory = [0] * 256
        self.a = 0
        self.b = 0
        self.c = 0
        self.seed[0] = key & self.MASK

        a = b = c = d = e = f = g = h = self.GOLDEN
        for _ in range(4):
            a, b, c, d, e, f, g, h = self._mix(a, b, c, d, e, f, g, h)

        for i in range(0, 256, 8):
            a = self._u64(a + self.seed[i])
            b = self._u64(b + self.seed[i + 1])
            c = self._u64(c + self.seed[i + 2])
            d = self._u64(d + self.seed[i + 3])
            e = self._u64(e + self.seed[i + 4])
            f = self._u64(f + self.seed[i + 5])
            g = self._u64(g + self.seed[i + 6])
            h = self._u64(h + self.seed[i + 7])
            a, b, c, d, e, f, g, h = self._mix(a, b, c, d, e, f, g, h)
            self.memory[i] = a
            self.memory[i + 1] = b
            self.memory[i + 2] = c
            self.memory[i + 3] = d
            self.memory[i + 4] = e
            self.memory[i + 5] = f
            self.memory[i + 6] = g
            self.memory[i + 7] = h

        for i in range(0, 256, 8):
            a = self._u64(a + self.memory[i])
            b = self._u64(b + self.memory[i + 1])
            c = self._u64(c + self.memory[i + 2])
            d = self._u64(d + self.memory[i + 3])
            e = self._u64(e + self.memory[i + 4])
            f = self._u64(f + self.memory[i + 5])
            g = self._u64(g + self.memory[i + 6])
            h = self._u64(h + self.memory[i + 7])
            a, b, c, d, e, f, g, h = self._mix(a, b, c, d, e, f, g, h)
            self.memory[i] = a
            self.memory[i + 1] = b
            self.memory[i + 2] = c
            self.memory[i + 3] = d
            self.memory[i + 4] = e
            self.memory[i + 5] = f
            self.memory[i + 6] = g
            self.memory[i + 7] = h

        self.generate()

    @staticmethod
    def _u64(v):
        return v & Isaac64.MASK

    @staticmethod
    def _mix(a, b, c, d, e, f, g, h):
        M = Isaac64.MASK
        a = (a - e) & M
        f = (f ^ (h >> 9)) & M
        h = (h + a) & M
        b = (b - f) & M
        g = (g ^ ((a << 9) & M)) & M
        a = (a + b) & M
        c = (c - g) & M
        h = (h ^ (b >> 23)) & M
        b = (b + c) & M
        d = (d - h) & M
        a = (a ^ ((c << 15) & M)) & M
        c = (c + d) & M
        e = (e - a) & M
        b = (b ^ (d >> 14)) & M
        d = (d + e) & M
        f = (f - b) & M
        c = (c ^ ((e << 20) & M)) & M
        e = (e + f) & M
        g = (g - c) & M
        d = (d ^ (f >> 17)) & M
        f = (f + g) & M
        h = (h - d) & M
        e = (e ^ ((g << 14) & M)) & M
        g = (g + h) & M
        return a, b, c, d, e, f, g, h

    def generate(self):
        M = self.MASK
        self.c = (self.c + 1) & M
        self.b = (self.b + self.c) & M
        for i in range(256):
            mod = i % 4
            if mod == 0:
                self.a = (~(self.a ^ ((self.a << 21) & M))) & M
            elif mod == 1:
                self.a = (self.a ^ (self.a >> 5)) & M
            elif mod == 2:
                self.a = (self.a ^ ((self.a << 12) & M)) & M
            else:
                self.a = (self.a ^ (self.a >> 33)) & M
            self.a = (self.a + self.memory[(i + 128) % 256]) & M
            x = self.memory[i]
            y = (self.memory[(x >> 3) & 0xFF] + self.a + self.b) & M
            self.memory[i] = y
            self.b = (self.memory[(y >> 11) & 0xFF] + x) & M
            self.seed[i] = self.b

    def next(self):
        result = self.seed[self.rand_count]
        if self.rand_count == 0:
            self.generate()
            self.rand_count = 255
        else:
            self.rand_count -= 1
        return result


def generate_finder_keystream(decode_key, size=PREFIX_BYTES):
    """生成 ISAAC64 密钥流（size 字节）。"""
    key_text = str(decode_key).strip() if decode_key is not None else ""
    if not re.match(r"^\d{1,20}$", key_text):
        raise SkillError(4, "视频解密参数无效（decodeKey 不是 1-20 位十进制数字）")
    key = int(key_text)
    if key > Isaac64.MASK:
        raise SkillError(4, "视频解密参数超出 64 位范围")
    if size < 1 or size > PREFIX_BYTES:
        raise SkillError(4, "视频解密长度无效")

    isaac = Isaac64(key)
    stream = bytearray(size)
    offset = 0
    while offset < size:
        word = isaac.next()
        for shift in range(56, -1, -8):
            if offset >= size:
                break
            stream[offset] = (word >> shift) & 0xFF
            offset += 1
    # 安全清理
    isaac.a = 0
    isaac.b = 0
    isaac.c = 0
    isaac.seed = [0] * 256
    isaac.memory = [0] * 256
    return bytes(stream)


# ===========================================================================
# 异常
# ===========================================================================

class SkillError(Exception):
    def __init__(self, exit_code, message, http_status=0):
        self.exit_code = exit_code
        self.message = message
        self.http_status = http_status
        super().__init__(message)


# ===========================================================================
# API Key
# ===========================================================================

def get_api_key():
    configured = (os.environ.get("WM_API_KEY") or "").strip()
    if configured:
        return configured
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(skill_dir, "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            key = str(data.get("WM_API_KEY") or "").strip()
            if key and key.isascii() and not any(c.isspace() for c in key):
                return key
    except json.JSONDecodeError:
        log("⚠️ config.json JSON 格式错误：%s" % config_path)
    except OSError:
        pass
    return ""


# ===========================================================================
# 付费接口响应缓存（避免重试重复扣费）
# ===========================================================================

def _cache_key(path, body, cache_extra=None):
    """按 path + 请求体（+ 可选稳定附加标识）生成缓存键（请求体键序无关）。

    cache_extra 存在时（视觉理解），请求体里的 videoUrl 是每次上传重新生成的
    临时地址，若参与哈希会导致同一视频重跑必然缓存未命中、重复扣费。因此此时
    把 videoUrl 从参与哈希的字段中剔除，改由 cache_extra（视频内容 sha256）
    承担"这是同一个视频"的身份标识。
    """
    body_for_key = body
    if cache_extra:
        body_for_key = {k: v for k, v in (body or {}).items() if k != "videoUrl"}
    raw = path + "|" + json.dumps(body_for_key, sort_keys=True, ensure_ascii=False)
    if cache_extra:
        raw += "|" + str(cache_extra)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _cache_read(path, body, cache_extra=None):
    """命中缓存则返回 payload dict，否则返回 None。"""
    if not CACHE_ENABLED or path not in CACHEABLE_PATHS:
        return None
    fp = os.path.join(CACHE_DIR, _cache_key(path, body, cache_extra) + ".json")
    try:
        if not os.path.exists(fp):
            return None
        if time.time() - os.path.getmtime(fp) > CACHE_TTL_SECONDS:
            return None
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict) or data.get("code") != "OK":
            return None
        log("  [缓存命中] %s（本次不再扣费）" % path.rsplit("/", 1)[-1])
        return data
    except (OSError, ValueError):
        return None


def _cache_write(path, body, payload, cache_extra=None):
    """把成功响应写入缓存。失败不写，保证修正后能真正重跑。"""
    if not CACHE_ENABLED or path not in CACHEABLE_PATHS:
        return
    if not isinstance(payload, dict) or payload.get("code") != "OK":
        return
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        fp = os.path.join(CACHE_DIR, _cache_key(path, body, cache_extra) + ".json")
        tmp = fp + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)
        os.replace(tmp, fp)
    except OSError as e:
        log("⚠️ 缓存写入失败（不影响本次结果）：%s" % e)


# ===========================================================================
# HTTP 基础
# ===========================================================================

def _make_conn(parsed, timeout):
    if parsed.scheme == "https":
        return http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=timeout)
    return http.client.HTTPConnection(parsed.hostname, parsed.port or 80, timeout=timeout)

def _full_path(parsed):
    p = parsed.path
    if parsed.query:
        p += "?" + parsed.query
    return p

def http_get(url, headers=None, timeout=HTTP_TIMEOUT):
    parsed = urlparse(url)
    conn = _make_conn(parsed, timeout)
    try:
        conn.putrequest("GET", _full_path(parsed))
        conn.putheader("User-Agent", USER_AGENT)
        conn.putheader("X-WM-Source", identity_headers()["X-WM-Source"])
        conn.putheader("X-Source", identity_headers()["X-Source"])
        if headers:
            for k, v in headers.items():
                conn.putheader(k, str(v))
        conn.endheaders()
        resp = conn.getresponse()
        body = resp.read()
        return resp.status, dict(resp.headers), body
    finally:
        conn.close()

def _http_post_once(path, body_bytes, api_key, idempotency_key, timeout):
    """发起单次 POST。

    成功返回 (payload, status, charge_micros, call_id, None, None)；
    失败返回 (None, status, None, None, code, msg)。
    """
    parsed = urlparse(BASE_URL + path)
    conn = _make_conn(parsed, timeout)
    try:
        conn.putrequest("POST", _full_path(parsed))
        conn.putheader("Content-Type", "application/json")
        conn.putheader("Accept", "application/json")
        conn.putheader("X-API-Key", api_key)
        conn.putheader("X-WM-Source", identity_headers()["X-WM-Source"])
        conn.putheader("X-Source", identity_headers()["X-Source"])
        conn.putheader("User-Agent", USER_AGENT)
        conn.putheader("Content-Length", str(len(body_bytes)))
        if idempotency_key:
            conn.putheader("Idempotency-Key", idempotency_key)
        conn.endheaders()
        conn.send(body_bytes)
        resp = conn.getresponse()
        raw = resp.read()
        status = resp.status
        charge_micros = resp.headers.get("X-Charge-Micros")
        call_id = resp.headers.get("X-Call-Id")
    finally:
        conn.close()

    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        return None, status, None, None, "INVALID_JSON", \
            "平台接口返回了无效 JSON（HTTP %d）" % status

    if status >= 200 and status < 300 and payload.get("code") == "OK" and not failure(payload):
        return payload, status, charge_micros, call_id, None, None

    code = str(payload.get("code") or "API_REQUEST_FAILED")
    msg = failure(payload) or str(payload.get("message") or "平台接口调用失败（HTTP %d）" % status)
    return None, status, None, None, code, msg


def http_post_json(path, body, api_key, idempotency_key=None, timeout=HTTP_TIMEOUT,
                   cache_extra=None):
    """POST JSON 到网关，返回解析后的 payload dict。

    付费接口（PATH_INFO / PATH_ANALYZE）成功响应会写入本地缓存，
    后续同一请求直接复用，不再调用接口、不再扣费；命中时 payload 带 _fromCache=True。

    cache_extra：附加进缓存 key 的稳定标识。视觉理解的请求体包含每次上传
    重新生成的 fileUrl，会导致重跑必然缓存未命中而重复扣费；调用方传入
    视频内容的 sha256 作为 cache_extra 后，同一视频的重跑即可命中缓存。
    """
    # 1. 先查缓存（命中则直接返回，不发起请求、不扣费）
    cache_body = {**body, "_accountScope": hashlib.sha256(api_key.encode()).hexdigest()}
    cached = _cache_read(path, cache_body, cache_extra=cache_extra)
    if cached is not None:
        cached["_fromCache"] = True
        cached["_chargeMicros"] = 0
        return cached

    body_bytes = json.dumps(body).encode("utf-8")
    # Reuse the logical request ID; an ambiguous failure is not proof of refund.
    last_code, last_msg, last_status = None, None, None
    idempotency_key = idempotency_key or uuid.uuid4().hex
    for attempt in range(1, RETRY_TIMES + 1):
        attempt_key = idempotency_key
        payload_or_none, status, charge_micros, call_id, code, msg = \
            _http_post_once(path, body_bytes, api_key, attempt_key, timeout)

        if payload_or_none is not None:
            # 成功
            payload = payload_or_none
            payload["_chargeMicros"] = int(charge_micros) if charge_micros and charge_micros.isdigit() else None
            payload["_callId"] = call_id if call_id else None
            payload["_fromCache"] = False
            # 3. 成功响应写入缓存（失败不写，保证修正后能真正重跑）
            _cache_write(path, cache_body, payload, cache_extra=cache_extra)
            return payload

        last_code, last_msg, last_status = code, msg, status
        # 鉴权类错误不重试
        if status in (401, 403) or code in ("UNAUTHORIZED", "FORBIDDEN", "API_KEY_INVALID"):
            raise SkillError(3, msg, status)
        # 非瞬时错误不重试
        if code not in TRANSIENT_CODES:
            raise SkillError(4, "%s: %s" % (code, msg), status)
        # 瞬时错误：还有次数则退避后重试
        if attempt < RETRY_TIMES:
            wait = RETRY_BACKOFF[min(attempt - 1, len(RETRY_BACKOFF) - 1)]
            log("  上游瞬时故障（%s），%d 秒后复用同一请求标识重试（%d/%d），计费状态以平台记录为准"
                % (code, wait, attempt, RETRY_TIMES - 1))
            time.sleep(wait)

    raise SkillError(4, "%s: %s（已重试 %d 次仍失败）"
                     % (last_code, last_msg, RETRY_TIMES), last_status)


# ===========================================================================
# 视频下载 + 解密
# ===========================================================================

def download_video(playback_url, target_path, on_progress=None):
    """从 finder.video.qq.com 下载视频到 target_path，返回字节数。"""
    url = playback_url
    redirects = 0
    while redirects < 6:
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise SkillError(6, "播放地址不是 HTTPS")
        if parsed.hostname and parsed.hostname.lower() != "finder.video.qq.com":
            raise SkillError(6, "播放地址不是受信任的视频号 CDN（finder.video.qq.com）")

        conn = _make_conn(parsed, DOWNLOAD_TIMEOUT)
        try:
            conn.putrequest("GET", _full_path(parsed))
            conn.putheader("Accept", "video/mp4,video/*;q=0.9,*/*;q=0.8")
            conn.putheader("User-Agent", USER_AGENT)
            conn.endheaders()
            resp = conn.getresponse()

            # 处理重定向
            if 300 <= resp.status < 400:
                loc = resp.headers.get("location")
                resp.read()
                if not loc:
                    raise SkillError(6, "视频下载重定向但缺少 Location 头")
                url = loc
                redirects += 1
                continue

            if resp.status < 200 or resp.status >= 300:
                resp.read()
                raise SkillError(6, "视频下载失败（HTTP %d）" % resp.status, resp.status)

            content_length_str = resp.headers.get("content-length")
            declared = int(content_length_str) if content_length_str and content_length_str.isdigit() else 0
            if declared and declared >= MAX_VIDEO_BYTES:
                resp.read()
                raise SkillError(2, "视频必须小于 128MB（Content-Length=%d）" % declared)

            received = 0
            last_pct = -1
            with open(target_path, "wb") as f:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    received += len(chunk)
                    if received >= MAX_VIDEO_BYTES:
                        raise SkillError(2, "视频必须小于 128MB（已接收 %d 字节）" % received)
                    f.write(chunk)
                    if on_progress and declared > 0:
                        pct = min(99, received * 100 // declared)
                        bucket = (pct // 10) * 10
                        if bucket > last_pct:
                            last_pct = bucket
                            on_progress(bucket)
        finally:
            conn.close()

        if received == 0:
            raise SkillError(6, "下载到的视频为空")
        return received

    raise SkillError(6, "视频下载重定向次数过多（>5）")


def looks_like_mp4(data):
    return len(data) >= 12 and data[4:8] == b"ftyp"

def decrypt_prefix(file_path, decode_key):
    """就地解密文件前 128KiB（如果需要），返回 (decrypted: bool)。"""
    file_size = os.path.getsize(file_path)
    if file_size <= 0:
        raise SkillError(6, "视频文件为空")
    if file_size >= MAX_VIDEO_BYTES:
        raise SkillError(2, "视频必须小于 128MB（实际 %d 字节）" % file_size)

    size = min(PREFIX_BYTES, file_size)
    with open(file_path, "rb+") as f:
        prefix = f.read(size)
        if looks_like_mp4(prefix):
            return False  # 已经是明文 MP4

        if not decode_key:
            raise SkillError(4, "视频需要解密，但播放地址接口没有返回 decodeKey")

        log("  正在用 ISAAC64 解密前 %d KiB…" % (size // 1024))
        keystream = generate_finder_keystream(decode_key, size)
        decrypted = bytearray(size)
        for i in range(size):
            decrypted[i] = prefix[i] ^ keystream[i]
        del keystream  # 释放密钥流

        if not looks_like_mp4(bytes(decrypted)):
            raise SkillError(4, "视频首段解密后未通过 MP4 ftyp 校验")

        f.seek(0)
        f.write(bytes(decrypted))
        f.flush()
        os.fsync(f.fileno())
    return True


# ===========================================================================
# 临时文件上传（multipart）
# ===========================================================================

def upload_ticket(api_key, filename, file_size, content_type="video/mp4"):
    """第一步：申请上传票据。"""
    payload = http_post_json(
        PATH_TICKET,
        {"filename": filename, "bytes": file_size, "contentType": content_type},
        api_key,
        timeout=HTTP_TIMEOUT,
    )
    data = payload.get("data") or {}
    upload_url = data.get("uploadUrl")
    file_url = data.get("fileUrl")
    required = data.get("requiredFields") or {}
    if not upload_url or not file_url:
        raise SkillError(9, "上传票据没有返回 uploadUrl 或 fileUrl")
    return {"uploadUrl": upload_url, "fileUrl": file_url, "requiredFields": required}

def upload_multipart(upload_url, required_fields, file_path, filename,
                     content_type="video/mp4", on_progress=None):
    """第二步：multipart 直传到对象存储。"""
    parsed = urlparse(upload_url)
    if parsed.scheme != "https":
        raise SkillError(9, "上传地址不是 HTTPS")

    boundary = "----WMVideoUpload" + uuid.uuid4().hex

    # 构建 multipart 前缀
    prefix_parts = []
    for key, value in required_fields.items():
        prefix_parts.append(("--%s\r\n" % boundary).encode())
        prefix_parts.append(
            ('Content-Disposition: form-data; name="%s"\r\n\r\n' % key)
            .encode()
        )
        prefix_parts.append(("%s\r\n" % value).encode())
    prefix_parts.append(("--%s\r\n" % boundary).encode())
    prefix_parts.append(
        ('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % filename)
        .encode()
    )
    prefix_parts.append(("Content-Type: %s\r\n\r\n" % content_type).encode())
    prefix = b"".join(prefix_parts)

    suffix = ("\r\n--%s--\r\n" % boundary).encode()

    file_size = os.path.getsize(file_path)
    total = len(prefix) + file_size + len(suffix)

    host = parsed.hostname
    port = parsed.port or 443
    path = _full_path(parsed)

    conn = http.client.HTTPSConnection(host, port, timeout=UPLOAD_TIMEOUT)
    try:
        conn.putrequest("POST", path)
        conn.putheader("Content-Type", "multipart/form-data; boundary=%s" % boundary)
        conn.putheader("Content-Length", str(total))
        conn.putheader("User-Agent", USER_AGENT)
        conn.endheaders()

        conn.send(prefix)
        sent = len(prefix)
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                conn.send(chunk)
                sent += len(chunk)
                if on_progress:
                    pct = min(99, sent * 100 // total)
                    on_progress(pct)
        conn.send(suffix)

        resp = conn.getresponse()
        resp.read()  # 消费响应体
        status = resp.status
    finally:
        conn.close()

    if status < 200 or status >= 300:
        raise SkillError(9, "视频直传失败（HTTP %d）" % status, status)
    return True


# ===========================================================================
# API 调用
# ===========================================================================

def get_balance(api_key):
    """接口13：免费余额查询。"""
    url = BASE_URL + PATH_BALANCE
    status, headers, raw = http_get(
        url,
        {"X-API-Key": api_key, "Accept": "application/json"},
        timeout=HTTP_TIMEOUT,
    )
    try:
        payload = json.loads(raw.decode("utf-8"))
    except Exception:
        raise SkillError(6, "余额接口返回了无效 JSON（HTTP %d）" % status, status)
    if status < 200 or status >= 300 or payload.get("code") != "OK":
        if status in (401, 403):
            raise SkillError(3, str(payload.get("message", "鉴权失败")), status)
        raise SkillError(4, str(payload.get("message", "余额查询失败")), status)
    return payload.get("data", {}).get("balance")

def resolve_video_info(api_key, share_url):
    """接口33：视频号作品资料——一次拿元信息+媒体+互动。"""
    payload = http_post_json(PATH_INFO, {"url": share_url}, api_key)
    return payload


def _file_sha256(path):
    """计算文件内容 sha256，作为视觉理解缓存的稳定附加标识。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def analyze_video(api_key, video_url, mode="decompose", extra_prompt=None, cache_extra=None):
    """接口27：视频视觉理解。

    cache_extra 传视频内容的 sha256：请求体里的 fileUrl 每次上传都重新生成，
    直接按请求体做缓存 key 会让同一视频的重跑必然未命中而重复扣费；
    以视频内容哈希为附加标识后，同一视频（内容不变）重跑可命中缓存。
    """
    body = {"videoUrl": video_url, "analysisMode": mode}
    if extra_prompt:
        body["extraPrompt"] = extra_prompt[:4000]
    idempotency_key = uuid.uuid4().hex
    payload = http_post_json(PATH_ANALYZE, body, api_key,
                             idempotency_key=idempotency_key, timeout=ANALYZE_TIMEOUT,
                             cache_extra=cache_extra)
    return payload


# ===========================================================================
# 报告渲染
# ===========================================================================

def _fmt_duration(ms):
    """毫秒 → 可读时长。"""
    if not ms:
        return "未知"
    try:
        ms = float(ms)
    except (TypeError, ValueError):
        return str(ms)
    s = ms / 1000.0
    m = int(s // 60)
    sec = s % 60
    if m > 0:
        return "%d分%.1f秒" % (m, sec)
    return "%.1f秒" % sec

def _fmt_seconds(sec):
    """秒 → 可读时间。"""
    if sec is None:
        return "?"
    try:
        sec = float(sec)
    except (TypeError, ValueError):
        return str(sec)
    m = int(sec // 60)
    s = sec % 60
    if m > 0:
        return "%d:%05.2f" % (m, s)
    return "%.2fs" % s

def _fmt_bytes(n):
    """字节数 → 可读大小。"""
    if not n:
        return "未知"
    try:
        n = float(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 1024 * 1024:
        return "%.1f MB" % (n / (1024 * 1024))
    if n >= 1024:
        return "%.1f KB" % (n / 1024)
    return "%d B" % n

def _fmt_time(iso_str):
    """ISO-8601 → 北京时间可读。"""
    if not iso_str:
        return "未知"
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.astimezone(CST).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return iso_str

def _conf_label(conf):
    """置信度 → 文字标签。"""
    if conf is None:
        return ""
    try:
        f = float(conf)
    except (TypeError, ValueError):
        return str(conf)
    if f >= 0.8:
        return "（高置信 %.0f%%）" % (f * 100)
    if f >= 0.5:
        return "（中置信 %.0f%%）" % (f * 100)
    return "（低置信 %.0f%%）" % (f * 100)

def _seg_field(seg, *keys, default=""):
    """从 segment dict 安全取嵌套字段。"""
    val = seg
    for k in keys:
        if isinstance(val, dict):
            val = val.get(k)
        else:
            return default
    return val if val is not None else default


def _pick(obj, *keys, default=""):
    """按别名依次取值，返回第一个非空结果。

    接口实际返回字段名与文档描述不一致（如 startSeconds vs start），
    这里同时兼容两套命名，避免任一来源取空。
    """
    if not isinstance(obj, dict):
        return default
    for k in keys:
        v = obj.get(k)
        if v not in (None, "", [], {}):
            return v
    return default


def _media_duration_seconds(media, spec=None):
    """从 media/spec 归一化出「秒」。

    注意两个来源单位不同：
      - media.videoPlayLen 单位是「秒」（如 18 表示 18 秒）
      - media.spec[].durationMs 单位是「毫秒」（如 18900 表示 18.9 秒）
    优先取 durationMs（精度更高），缺失时回退 videoPlayLen。
    """
    spec = spec or {}
    dur_ms = spec.get("durationMs")
    val = None
    if dur_ms is not None:
        try:
            val = float(dur_ms) / 1000.0
        except (TypeError, ValueError):
            val = None
    if val is None:
        play_len = media.get("videoPlayLen")
        if play_len is not None:
            try:
                val = float(play_len)  # videoPlayLen 单位就是秒
            except (TypeError, ValueError):
                val = None
    return val


def _fmt_dur_seconds(sec):
    """秒 → 可读时长（用于作品时长）。"""
    if sec is None:
        return "未知"
    try:
        sec = float(sec)
    except (TypeError, ValueError):
        return str(sec)
    if sec <= 0:
        return "未知"
    m = int(sec // 60)
    s = sec % 60
    if m > 0:
        return "%d分%.1f秒" % (m, s)
    return "%.1f秒" % s


def _as_text(val, sep=" / "):
    """把字符串或字符串数组渲染成展示文本。"""
    if val is None:
        return ""
    if isinstance(val, (list, tuple)):
        parts = [str(x).strip() for x in val if str(x).strip()]
        return sep.join(parts)
    return str(val).strip()

# All report formats and AI analysis use the same versioned interaction facts.
from interaction_metrics import (
    INTERACTION_KEYS as _INTERACTION_KEYS, METRIC_NOTE, METHOD_NOTE,
    SEMANTICS_VERSION, normalize_info, norm_metrics as _norm_metrics,
    infer_interaction_profile, interaction_basis, interaction_total, metric_display,
)

# ===========================================================================
# 分析层（AI 深度分析注入）
# ---------------------------------------------------------------------------
# 数据层（接口33/27 的原始返回）只回答"视频里有什么"；分析层回答"为什么
# 有效、怎么借鉴"。分析由 assistant 依据 wm_video_raw.json 产出，按
# references/analysis-schema.md 写成 wm_analysis.json，再经 --render 渲染
# 进 Markdown / Excel / HTML 三种格式（零 API 调用、零扣费）。
# 渲染时 analysis 为 None 则自动降级为纯数据报告，不报错。
# ===========================================================================

def _an(analysis, *keys, default=None):
    """从分析 JSON 中按路径安全取值。"""
    cur = analysis
    for k in keys:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(k)
        if cur is None:
            return default
    return cur


def _an_score_text(val):
    """评分统一显示为 x/10。"""
    try:
        return "%.1f/10" % float(val)
    except (TypeError, ValueError):
        return str(val or "-")


def render_report(info_payload, analysis_payload, billing_list, input_desc, is_local=False,
                  analysis=None):
    """整合所有数据维度 + 可选 AI 分析层，渲染综合 Markdown 报告。"""
    info_payload = normalize_info(info_payload)
    lines = []
    lines.append("# 视频号视频拆解报告")
    lines.append("")
    info_data_head = (info_payload or {}).get("data") or {}
    _rpt_title = info_data_head.get("title") or info_data_head.get("description") or "(无标题)"
    lines.append("**分析对象**：%s" % _rpt_title)
    lines.append("")
    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 报告生成时间 | %s |" % datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"))
    lines.append("| 数据来源 | 曼格云 API（作品资料接口 + 视觉理解接口） |")
    lines.append("| 输入来源 | %s |" % input_desc)
    lines.append("| 数据性质 | 标注「实测」为接口返回值；「模型输出」为视觉理解模型观察结果；「推断」为分析判断 |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 执行摘要（结论前置） ---
    _m_head = _norm_metrics(info_data_head.get("metrics") or {})
    _prof_head = infer_interaction_profile(_m_head) if not is_local else None
    _ov_head = (analysis or {}).get("overall") or {}
    _attr_head = (analysis or {}).get("viralAttribution") or []
    lines.append("## 执行摘要")
    lines.append("")
    if _prof_head:
        lines.append("- 互动结构：主导指标 **%s**（占四指标总量 %.1f%%），互动结构为 **%s**。" % (
            _prof_head["dominant"], _prof_head["shares"][_prof_head["dominant"]], _prof_head["type"]))
    if _attr_head:
        _t0 = _attr_head[0]
        lines.append("- 优先分析因素：%s（分析权重 %s%%，非实测传播贡献）。%s" % (
            _t0.get("factor", ""), _t0.get("contribution", ""), _t0.get("detail", "")))
    if _ov_head.get("totalScore") is not None:
        lines.append("- 综合评分：%s / 100%s。" % (
            _ov_head.get("totalScore"),
            "（可复制性 %s / 5）" % _ov_head.get("replicabilityStars")
            if _ov_head.get("replicabilityStars") else ""))
    if _ov_head.get("primaryImprovement"):
        lines.append("- 最优先改进项：%s" % _ov_head["primaryImprovement"])
    if is_local:
        lines.append("- 本地视频文件，无互动数据，本节仅覆盖内容维度。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 一、作品基本信息 ---
    info_data = (info_payload or {}).get("data") or {}
    lines.append("## 基本信息　`实测`")
    lines.append("")
    title = info_data.get("title") or info_data.get("description") or "(无标题)"
    desc = info_data.get("description") or "(无描述)"
    account = info_data.get("accountName") or "未知"
    published = _fmt_time(info_data.get("publishedAt"))
    cover = info_data.get("coverUrl") or ""

    # 媒体信息
    media_list = info_data.get("media") or []
    media = media_list[0] if media_list else {}
    width = media.get("width")
    height = media.get("height")
    file_size = media.get("fileSize")
    spec_list = media.get("spec") or []
    spec = spec_list[0] if spec_list else {}
    # 时长：单位已由 _media_duration_seconds 归一化成秒
    duration_sec = _media_duration_seconds(media, spec)
    if not width and spec.get("width"):
        width = spec.get("width")
    if not height and spec.get("height"):
        height = spec.get("height")

    lines.append("| 项目 | 内容 |")
    lines.append("| --- | --- |")
    lines.append("| 标题/文案 | %s |" % title)
    lines.append("| 描述 | %s |" % (desc if desc != title else "(同标题)"))
    lines.append("| 发布账号 | %s |" % account)
    lines.append("| 发布时间 | %s |" % published)
    lines.append("| 时长 | %s |" % _fmt_dur_seconds(duration_sec))
    if width and height:
        lines.append("| 分辨率 | %sx%s |" % (width, height))
    else:
        lines.append("| 分辨率 | 未知 |")
    lines.append("| 文件大小 | %s |" % _fmt_bytes(file_size))
    if cover:
        lines.append("| 封面 | [查看封面](%s) |" % cover)
    else:
        lines.append("| 封面 | 无 |")
    lines.append("")

    # --- 受众画像（分析层） ---
    aud = _an(analysis, "audience") or {}
    if aud:
        lines.append("## 受众画像　`推断`")
        lines.append("")
        lines.append("| 维度 | 判断 |")
        lines.append("| --- | --- |")
        if aud.get("ageRange"):
            lines.append("| 年龄段 | %s |" % aud["ageRange"])
        if aud.get("gender"):
            lines.append("| 性别比例 | %s |" % aud["gender"])
        if aud.get("interests"):
            interests = aud["interests"]
            if isinstance(interests, list):
                interests = "、".join(str(i) for i in interests)
            lines.append("| 兴趣标签 | %s |" % interests)
        if aud.get("consumption"):
            lines.append("| 消费能力 | %s |" % aud["consumption"])
        lines.append("")

    # --- 二、互动数据 ---
    if not is_local:
        metrics = _norm_metrics(info_data.get("metrics"))
        # 视频号 API 不返回 viewCount（播放量），指标只保留四类互动
        metric_details = info_data.get("metricDetails") or {}
        lines.append("## 互动数据　`实测`")
        lines.append("")
        lines.append("| 指标 | 精确值 | 页面展示 |")
        lines.append("| --- | --- | --- |")
        for key, label in [("likeCount", "点赞"), ("shareCount", "转发"),
                           ("commentCount", "评论"), ("recommendCount", "推荐")]:
            val = metrics.get(key)
            detail = metric_details.get(key, {})
            display = detail.get("display") or ""
            if val is not None:
                v = str(val)
            else:
                v = "未获取精确值"
            lines.append("| %s | %s | %s |" % (label, v, display))
        lines.append("")

        # 互动总量（视频号无播放量，互动率无法计算）
        like_c = metrics.get("likeCount") or 0
        share_c = metrics.get("shareCount") or 0
        comment_c = metrics.get("commentCount") or 0
        recommend_c = metrics.get("recommendCount") or 0
        total_inter = interaction_total(metrics)
        lines.append("> 互动计数合计：%s（点赞+转发+评论+推荐，非去重人数）" % (str(total_inter) if total_inter is not None else "数据不全，未计算"))
        lines.append("> " + METRIC_NOTE)
        lines.append("")

        # --- 二·B、互动结构反推 ---
        prof = infer_interaction_profile(metrics)
        lines.append("## 互动数据反推　`推断`")
        lines.append("")
        if prof:
            lines.append("以下仅描述互动计数的相对结构，不据此直接判定传播原因或受众动机。")
            lines.append("")
            lines.append("| 指标 | 数值 | 占比 | 相对点赞 |")
            lines.append("| --- | --- | --- | --- |")
            ratio_of = {"点赞": "—", "转发": "转发/点赞", "评论": "评论/点赞", "推荐": "推荐/点赞"}
            for _k, _label in _INTERACTION_KEYS:
                name = _label
                rk = ratio_of[name]
                rv = "—" if rk == "—" else "%.1f%%" % prof["ratios"][rk]
                lines.append("| %s | %d | %.1f%% | %s |" % (
                    name, prof["counts"][name], prof["shares"][name], rv))
            lines.append("")
            lines.append("**结构判定**：主导指标 **%s**，互动结构 **%s**" % (prof["dominant"], prof["type"]))
            lines.append("")
            lines.append("**逐项解读**：")
            lines.append("")
            for name, level, text in prof["signals"]:
                lines.append("- **%s（%s）**：%s" % (name, level, text))
            lines.append("")
            if prof["actions"]:
                lines.append("**由互动结构推导的动作**：")
                lines.append("")
                for i, act in enumerate(prof["actions"], 1):
                    lines.append("%d. %s" % (i, act))
                lines.append("")
            notes = (analysis or {}).get("interactionNotes")
            if notes:
                lines.append("**分析层补充解读**：")
                lines.append("")
                for n in notes:
                    lines.append("- %s" % _as_text(n))
                lines.append("")
        else:
            lines.append("> 互动数据不足（存在缺失/非精确值，或点赞为 0），无法进行结构反推。")
            lines.append("")
    else:
        lines.append("## 互动数据　`实测`")
        lines.append("")
        lines.append("> 本地视频文件无互动数据。")
        lines.append("")

    # --- 三、内容摘要 ---
    obs = {}
    if analysis_payload:
        a_data = analysis_payload.get("data") or {}
        obs = a_data.get("observation") or {}
    summary = obs.get("summary") or ""
    est_duration = obs.get("durationSeconds")
    try:
        est_duration = float(est_duration) if est_duration is not None else None
    except (TypeError, ValueError):
        est_duration = None
    lines.append("## 内容摘要　`模型输出`")
    lines.append("")
    if summary:
        lines.append(summary)
    else:
        lines.append("(视觉理解未返回摘要)")
    if est_duration:
        lines.append("")
        lines.append("> 模型估计时长：%.1f 秒" % est_duration)
    lines.append("")

    # --- 结构拆解（数据层时间线 + 分析层解读） ---
    segments = obs.get("segments") or []
    lines.append("## 结构拆解　`推断`")
    lines.append("")
    struct = _an(analysis, "structure") or {}
    seg_notes = struct.get("segmentNotes") or {}
    if struct:
        if struct.get("scriptType"):
            lines.append("**脚本类型**：%s" % struct["scriptType"])
        if struct.get("rationale"):
            lines.append("")
            lines.append("**判断依据**：%s" % struct["rationale"])
        lines.append("")
    if segments:
        for idx, seg in enumerate(segments, 1):
            # 接口实际返回 startSeconds/endSeconds/onscreenTexts/speechSummary/
            # shotType/cameraMovement/emotionCues；同时兼容文档命名
            start = _pick(seg, "startSeconds", "start")
            end = _pick(seg, "endSeconds", "end")
            visual = _pick(seg, "visual", "visualDescription")
            onscreen = _pick(seg, "onscreenTexts", "onscreenText", "onScreenText")
            speech = _pick(seg, "speechSummary", "speech")
            shot = _pick(seg, "shotType", "shot", "shotInfo")
            camera = _pick(seg, "cameraMovement", "camera")
            narrative = _pick(seg, "narrativeFunction", "narrative")
            transition = _pick(seg, "transition")
            emotion = _pick(seg, "emotionCues", "emotion")
            confidence = _pick(seg, "confidence", default=None)

            lines.append("### 片段 %d（%s – %s）%s" % (
                idx, _fmt_seconds(start), _fmt_seconds(end), _conf_label(confidence)
            ))
            lines.append("")
            if visual:
                lines.append("- **画面**：%s" % _as_text(visual))
            if onscreen:
                lines.append("- **屏幕文字**：%s" % _as_text(onscreen, sep=" ｜ "))
            if speech:
                lines.append("- **语音/解说**：%s" % _as_text(speech))
            if shot:
                lines.append("- **景别**：%s" % _as_text(shot))
            if camera:
                lines.append("- **运镜**：%s" % _as_text(camera))
            if transition:
                lines.append("- **转场**：%s" % _as_text(transition))
            if emotion:
                lines.append("- **情绪线索**：%s" % _as_text(emotion, sep=" ｜ "))
            if narrative:
                lines.append("- **叙事作用**：%s" % _as_text(narrative))
            note = seg_notes.get(str(idx)) or seg_notes.get(idx)
            if note:
                lines.append("- **为什么有效**：%s" % note)
            lines.append("")
        if struct.get("summary"):
            lines.append("**结构总结**：%s" % struct["summary"])
            lines.append("")
    else:
        lines.append("(视觉理解未返回分段数据)")
        lines.append("")

    # --- 五、画面事实与证据 ---
    facts = obs.get("visualFacts") or []
    lines.append("## 画面事实与证据　`实测`")
    lines.append("")
    if facts:
        for idx, fact in enumerate(facts, 1):
            # 接口实际字段：statement / startSeconds / endSeconds / confidence
            # 同时兼容文档命名：description / timeRange / evidenceType
            desc = _pick(fact, "statement", "description", "fact", default="")
            if not desc:
                desc = _as_text(fact)
            conf = _pick(fact, "confidence", default=None)
            f_start = _pick(fact, "startSeconds", "start", default=None)
            f_end = _pick(fact, "endSeconds", "end", default=None)
            evidence = _pick(fact, "evidenceType", "evidence", default="")
            time_range = _pick(fact, "timeRange", "time", default="")
            if not time_range and f_start is not None:
                time_range = "%s – %s" % (_fmt_seconds(f_start), _fmt_seconds(f_end))

            lines.append("%d. %s %s" % (idx, _as_text(desc), _conf_label(conf)))
            if time_range:
                lines.append("   - 时间范围：%s" % time_range)
            if evidence:
                lines.append("   - 证据类型：%s" % evidence)
            lines.append("")
    else:
        lines.append("(视觉理解未返回画面事实)")
        lines.append("")

    # --- 六、不确定项 ---
    uncertainties = obs.get("uncertainties") or []
    lines.append("## 不确定项　`实测`")
    lines.append("")
    lines.append("> 以下内容无法从视频中确认，请勿当作事实引用。")
    lines.append("")
    if uncertainties:
        for idx, item in enumerate(uncertainties, 1):
            if isinstance(item, dict):
                desc = item.get("description") or item.get("item") or str(item)
                reason = item.get("reason") or item.get("cause") or ""
            else:
                desc = str(item)
                reason = ""
            lines.append("%d. %s" % (idx, desc))
            if reason:
                lines.append("   - 原因：%s" % reason)
        lines.append("")
    else:
        lines.append("(无不确定项)")
        lines.append("")

    # --- 分析层：爆款归因 / 爆款公式 / 六维评分 / 运营建议 / 总体评估 ---
    viral = _an(analysis, "viralAttribution") or []
    formula = _an(analysis, "viralFormula")
    six_dim = _an(analysis, "sixDimScores") or []
    ops_list = _an(analysis, "operations") or []
    overall = _an(analysis, "overall") or {}
    tags = _an(analysis, "tags") or []

    if analysis:
        # 爆款归因
        if viral:
            lines.append("## 爆款归因　`推断`")
            lines.append("")
            lines.append("| 排序 | 层 | 因素 | 详细描述 | 分析权重（非因果贡献） | 数据佐证 |")
            lines.append("| --- | --- | --- | --- | --- | --- |")
            for i, item in enumerate(viral, 1):
                contrib = item.get("contribution")
                contrib_str = ("%d%%" % int(contrib)) if contrib is not None else "-"
                lines.append("| %s | %s | %s | %s | %s | %s |" % (
                    item.get("rank") or i,
                    item.get("layer", ""),
                    item.get("factor", ""),
                    item.get("detail", ""),
                    contrib_str,
                    item.get("evidence", "") or "-",
                ))
            lines.append("")

        # 爆款公式 + 可复刻性
        if formula:
            lines.append("## 爆款公式　`推断`")
            lines.append("")
            lines.append("> **%s**" % formula)
            lines.append("")
        repl = _an(analysis, "replicability") or {}
        if repl.get("score") is not None or repl.get("note"):
            lines.append("- **可复刻性评分**：%s/5" % repl.get("score", "-"))
            if repl.get("note"):
                lines.append("- **可复刻性说明**：%s" % repl["note"])
            if repl.get("replicableStrategy"):
                lines.append("- **可复刻策略**：%s" % repl["replicableStrategy"])
            if repl.get("notApplicableScenarios"):
                lines.append("- **不适用场景**：%s" % repl["notApplicableScenarios"])
            lines.append("")

        # 六维评分
        if six_dim:
            lines.append("## 六维评分　`推断`")
            lines.append("")
            lines.append("| 维度 | 评分 | 节奏证据 | 评分理由 | 改进建议 |")
            lines.append("| --- | --- | --- | --- | --- |")
            for item in six_dim:
                lines.append("| %s | %s | %s | %s | %s |" % (
                    item.get("dimension", ""),
                    _an_score_text(item.get("score")),
                    item.get("evidence", "") or "-",
                    item.get("reason", ""),
                    item.get("suggestion", "") or "-",
                ))
            lines.append("")

        # 运营建议
        if ops_list:
            lines.append("## 运营建议　`推断`")
            lines.append("")
            for item in ops_list:
                lines.append("- %s" % item)
            lines.append("")

        # 总体评估
        if overall:
            lines.append("## 总体评估　`推断`")
            lines.append("")
            if overall.get("totalScore") is not None:
                lines.append("- **总体评分**：%s/100" % overall.get("totalScore"))
            if overall.get("replicabilityStars") is not None:
                stars = int(overall.get("replicabilityStars") or 0)
                lines.append("- **可复制性**：%d/5（%s）" % (stars, "★" * stars + "☆" * (5 - stars)))
            for hl in overall.get("highlights") or []:
                hl_type = hl.get("type", "亮点")
                lines.append("- **%s**：%s" % (hl_type, hl.get("text", "")))
            if overall.get("primaryImprovement"):
                lines.append("- **首要改进**：%s" % overall["primaryImprovement"])
            lines.append("")

        # 标签
        if tags:
            lines.append("## 标签　`推断`")
            lines.append("")
            lines.append("`%s`" % "` · `".join(str(t) for t in tags))
            lines.append("")
    else:
        # 无分析层时降级：输出规则驱动的浅层借鉴要点
        lines.append("## 可借鉴策略要点（基础版）　`推断`")
        lines.append("")
        lines.append("> 本报告未注入 AI 分析层。深度分析（受众画像/爆款归因/六维评分等）"
                     "由 assistant 依据 wm_video_raw.json 生成 wm_analysis.json 后，"
                     "用 --render 重新渲染获得。")
        lines.append("")
        if title and title != "(无标题)":
            lines.append("- **文案策略**：标题「%s」%s" % (title, "—简洁有力，直接点明价值" if len(title) < 20 else "—内容详尽，信息密度高"))
        if segments:
            lines.append("- **节奏结构**：全片分为 %d 个分段，时长 %s" % (
                len(segments), _fmt_dur_seconds(duration_sec)
            ))
        if not is_local and metrics:
            like_c = metrics.get("likeCount")
            comment_c = metrics.get("commentCount")
            if like_c and comment_c is not None:
                ratio = comment_c / like_c * 100
                lines.append("- **互动表现**：评论/点赞比 %.2f%%；是否存在争议须结合评论内容判断。" % ratio)
        if segments:
            has_onscreen = any(_seg_field(s, "onscreenText") or _seg_field(s, "onScreenText") for s in segments)
            has_speech = any(_seg_field(s, "speech") or _seg_field(s, "speechSummary") for s in segments)
            if has_onscreen:
                lines.append("- **视觉策略**：使用了屏幕文字辅助信息传达")
            if has_speech:
                lines.append("- **听觉策略**：包含语音解说，增强信息密度")
        lines.append("")

    # --- 费用明细 ---
    lines.append("## 费用明细　`实测`")
    lines.append("")
    lines.append("| 步骤 | 接口 | 消费(元) | 余额(元) |")
    lines.append("| --- | --- | --- | --- |")
    total_consumption = 0
    for item in billing_list:
        name = item.get("name", "")
        consumption = item.get("consumption")
        balance = item.get("balance")
        if consumption is not None:
            total_consumption += consumption
        lines.append("| %s | %s | %s | %s |" % (
            name,
            item.get("endpoint", ""),
            ("%.6f" % consumption) if consumption is not None else "-",
            ("%.6f" % balance) if balance is not None else "-",
        ))
    lines.append("| **合计** | | **%.6f** | |" % total_consumption)
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 附录：方法论与数据说明")
    lines.append("")
    lines.append("**数据来源**")
    lines.append("")
    lines.append("- 作品元信息、互动数据：曼格云视频号作品资料接口")
    lines.append("- 画面分段、镜头语言、屏幕文字、语音摘要：视频视觉理解模型")
    lines.append("")
    lines.append("**数据性质分级**")
    lines.append("")
    lines.append("- `实测`：接口直接返回的数据")
    lines.append("- `模型输出`：模型对画面的观察结果，可能存在识别误差")
    lines.append("- `推断`：基于上述数据作出的分析判断，属于观点而非事实")
    lines.append("")
    lines.append("**互动结构反推口径**")
    lines.append("")
    lines.append("- " + METHOD_NOTE)
    lines.append("- " + METRIC_NOTE)
    lines.append("")
    lines.append("**口径限制**")
    lines.append("")
    lines.append("- 视频号接口不提供播放量，因此本报告不含播放量与互动率；"
                "所有传播判断基于四项互动的相对结构，不代表触达规模")
    lines.append("- 评论区内容、账号粉丝量、流量来源、完播率未纳入本次采集范围")
    lines.append("- 受众画像为推断结果，非平台官方统计")
    lines.append("")
    lines.append("**使用声明**")
    lines.append("")
    lines.append("本报告为内容分析方法论产出，评分与结论用于创作参考，不构成对账号运营效果的保证，"
                "亦不构成任何商业或法律意见。推断类内容依赖有限样本与经验规则，请结合账号自身数据判断。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*生成时间：%s ｜ 本报告由 WorkBuddy 视频拆解技能生成*"
                % datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"))

    return "\n".join(lines)


# ===========================================================================
# Excel 导出（纯标准库 zipfile + XML，生成 .xlsx）
# ===========================================================================

def _xlsx_escape(text):
    """XML 转义。"""
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace('"', "&quot;").replace("'", "&apos;")
    return s

def _col_letter(idx):
    """0-based 列号 → Excel 列字母（0→A, 25→Z, 26→AA）。"""
    result = ""
    idx += 1
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        result = chr(65 + rem) + result
    return result

def render_xlsx(info_payload, analysis_payload, billing_list, input_desc, is_local=False,
                out_path=None, analysis=None):
    """生成 .xlsx 文件，包含多个 sheet（数据层 + 可选 AI 分析层）。返回文件路径。"""
    info_payload = normalize_info(info_payload)
    import zipfile
    import io

    info_data = (info_payload or {}).get("data") or {}
    a_data = (analysis_payload or {}).get("data") or {}
    obs = a_data.get("observation") or {}
    media_list = info_data.get("media") or []
    media = media_list[0] if media_list else {}
    _spec_list_x = media.get("spec") or []
    _spec_x = _spec_list_x[0] if _spec_list_x else {}
    metrics = _norm_metrics(info_data.get("metrics"))

    # --- 构建 sheet 数据 ---
    sheets = []

    # Sheet 1: 基本信息
    rows1 = [["项目", "内容"]]
    rows1.append(["标题/文案", info_data.get("title") or info_data.get("description") or "(无)"])
    rows1.append(["描述", info_data.get("description") or "(同标题)"])
    rows1.append(["发布账号", info_data.get("accountName") or "未知"])
    rows1.append(["发布时间", _fmt_time(info_data.get("publishedAt"))])
    rows1.append(["时长", _fmt_dur_seconds(_media_duration_seconds(media, _spec_x))])
    rows1.append(["分辨率", "%sx%s" % (media.get("width", "?"), media.get("height", "?")) if media.get("width") else "未知"])
    rows1.append(["文件大小", _fmt_bytes(media.get("fileSize"))])
    rows1.append(["封面链接", info_data.get("coverUrl") or ""])
    rows1.append(["输入来源", input_desc])
    sheets.append(("基本信息", rows1))

    # Sheet 2: 互动数据
    if not is_local:
        rows2 = [["指标", "精确值", "页面展示"]]
        for key, label in [("likeCount", "点赞"), ("shareCount", "转发"),
                           ("commentCount", "评论"), ("recommendCount", "推荐")]:
            val = metrics.get(key)
            display = (info_data.get("metricDetails") or {}).get(key, {}).get("display", "")
            rows2.append([label, str(val) if val is not None else "未获取", display])
        like_c = metrics.get("likeCount") or 0
        share_c = metrics.get("shareCount") or 0
        comment_c = metrics.get("commentCount") or 0
        recommend_c = metrics.get("recommendCount") or 0
        total_inter = interaction_total(metrics)
        rows2.append(["互动计数合计", str(total_inter) if total_inter is not None else "数据不全，未计算", "非去重人数"])
        rows2.append(["指标口径", METRIC_NOTE, ""])
        rows2.append(["备注", "视频号 API 不返回播放量（viewCount），故无互动率", ""])
        sheets.append(("互动数据", rows2))

        # Sheet 2.5: 互动反推（由四指标结构反推内容性质与传播机制）
        prof = infer_interaction_profile(metrics)
        rows2b = [["维度", "项目", "数值/内容"]]
        if prof:
            rows2b.append(["结论", "主导指标", prof["dominant"]])
            rows2b.append(["结论", "互动结构", prof["type"]])
            rows2b.append(["结论", "互动总量", prof["total"]])
            for name in ("点赞", "转发", "评论", "推荐"):
                rows2b.append(["占比", name, "%.1f%%" % prof["shares"][name]])
            for rk in ("转发/点赞", "评论/点赞", "推荐/点赞"):
                rows2b.append(["比值", rk, "%.1f%%" % prof["ratios"][rk]])
            for name, level, text in prof["signals"]:
                rows2b.append(["逐项解读", "%s（%s）" % (name, level), text])
            for i, act in enumerate(prof["actions"], 1):
                rows2b.append(["推导动作", "动作%d" % i, act])
            for n in (analysis or {}).get("interactionNotes") or []:
                rows2b.append(["分析层补充", "解读", _as_text(n)])
        else:
            rows2b.append(["结论", "状态", "互动数据不足（存在缺失/非精确值，或点赞为 0），无法反推"])
        sheets.append(("互动反推", rows2b))
    else:
        sheets.append(("互动数据", [["说明", "本地视频无互动数据"]]))

    # Sheet 3: 时间线分段
    segments = obs.get("segments") or []
    rows3 = [["片段", "开始", "结束", "画面描述", "屏幕文字", "语音/解说", "景别", "运镜", "转场", "情绪", "叙事作用", "置信度"]]
    for idx, seg in enumerate(segments, 1):
        rows3.append([
            idx,
            _fmt_seconds(_pick(seg, "startSeconds", "start")),
            _fmt_seconds(_pick(seg, "endSeconds", "end")),
            _as_text(_pick(seg, "visual", "visualDescription")),
            _as_text(_pick(seg, "onscreenTexts", "onscreenText", "onScreenText"), sep=" ｜ "),
            _as_text(_pick(seg, "speechSummary", "speech")),
            _as_text(_pick(seg, "shotType", "shot", "shotInfo")),
            _as_text(_pick(seg, "cameraMovement", "camera")),
            _as_text(_pick(seg, "transition")),
            _as_text(_pick(seg, "emotionCues", "emotion"), sep=" ｜ "),
            _as_text(_pick(seg, "narrativeFunction", "narrative")),
            str(_pick(seg, "confidence", default="") or ""),
        ])
    if not segments:
        rows3.append(["(无分段数据)"] + [""] * 11)
    sheets.append(("时间线分段", rows3))

    # Sheet 4: 画面事实
    facts = obs.get("visualFacts") or []
    rows4 = [["序号", "画面事实", "时间范围", "证据类型", "置信度"]]
    for idx, fact in enumerate(facts, 1):
        f_start = _pick(fact, "startSeconds", "start", default=None)
        f_end = _pick(fact, "endSeconds", "end", default=None)
        time_range = _pick(fact, "timeRange", "time", default="")
        if not time_range and f_start is not None:
            time_range = "%s – %s" % (_fmt_seconds(f_start), _fmt_seconds(f_end))
        rows4.append([
            idx,
            _as_text(_pick(fact, "statement", "description", "fact", default=fact)),
            time_range,
            _as_text(_pick(fact, "evidenceType", "evidence")),
            str(_pick(fact, "confidence", default="") or ""),
        ])
    if not facts:
        rows4.append(["(无画面事实)"] + [""] * 4)
    sheets.append(("画面事实", rows4))

    # Sheet 5: 不确定项
    uncertainties = obs.get("uncertainties") or []
    rows5 = [["序号", "描述", "原因"]]
    for idx, item in enumerate(uncertainties, 1):
        if isinstance(item, dict):
            rows5.append([idx, item.get("description") or item.get("item") or str(item),
                          item.get("reason") or item.get("cause") or ""])
        else:
            rows5.append([idx, str(item), ""])
    if not uncertainties:
        rows5.append(["(无不确定项)", "", ""])
    sheets.append(("不确定项", rows5))

    # --- AI 分析层 sheets（analysis 提供时） ---
    if analysis:
        aud = analysis.get("audience") or {}
        rowsa = [["维度", "判断"]]
        if aud.get("ageRange"):
            rowsa.append(["年龄段", aud["ageRange"]])
        if aud.get("gender"):
            rowsa.append(["性别比例", aud["gender"]])
        interests = aud.get("interests")
        if interests:
            if isinstance(interests, list):
                interests = "、".join(str(i) for i in interests)
            rowsa.append(["兴趣标签", interests])
        if aud.get("consumption"):
            rowsa.append(["消费能力", aud["consumption"]])
        if len(rowsa) > 1:
            sheets.append(("分析-受众画像", rowsa))

        struct = analysis.get("structure") or {}
        rowsb = [["字段", "内容"]]
        if struct.get("scriptType"):
            rowsb.append(["脚本类型", struct["scriptType"]])
        if struct.get("rationale"):
            rowsb.append(["判断依据", struct["rationale"]])
        if struct.get("summary"):
            rowsb.append(["结构总结", struct["summary"]])
        seg_notes = struct.get("segmentNotes") or {}
        for k in sorted(seg_notes, key=lambda x: int(x) if str(x).isdigit() else 999):
            rowsb.append(["片段%s 为什么有效" % k, seg_notes[k]])
        if len(rowsb) > 1:
            sheets.append(("分析-结构解读", rowsb))

        viral = analysis.get("viralAttribution") or []
        rowsc = [["排序", "层", "因素", "详细描述", "分析权重(%，非实测贡献)", "数据佐证"]]
        for i, item in enumerate(viral, 1):
            contrib = item.get("contribution")
            rowsc.append([
                item.get("rank") or i,
                item.get("layer", ""),
                item.get("factor", ""),
                item.get("detail", ""),
                int(contrib) if contrib is not None else "",
                item.get("evidence", "") or "-",
            ])
        if viral:
            sheets.append(("分析-爆款归因", rowsc))

        six_dim = analysis.get("sixDimScores") or []
        rowsd = [["维度", "评分(/10)", "节奏证据", "评分理由", "改进建议"]]
        for item in six_dim:
            try:
                score = float(item.get("score"))
            except (TypeError, ValueError):
                score = ""
            rowsd.append([
                item.get("dimension", ""),
                score,
                item.get("evidence", "") or "-",
                item.get("reason", ""),
                item.get("suggestion", "") or "-",
            ])
        if six_dim:
            sheets.append(("分析-六维评分", rowsd))

        rowse = [["类型", "内容"]]
        formula = analysis.get("viralFormula")
        if formula:
            rowse.append(["爆款公式", formula])
        repl = analysis.get("replicability") or {}
        if repl.get("score") is not None:
            rowse.append(["可复刻性评分(/5)", repl.get("score")])
        if repl.get("note"):
            rowse.append(["可复刻性说明", repl["note"]])
        if repl.get("replicableStrategy"):
            rowse.append(["可复刻策略", repl["replicableStrategy"]])
        if repl.get("notApplicableScenarios"):
            rowse.append(["不适用场景", repl["notApplicableScenarios"]])
        for item in analysis.get("operations") or []:
            rowse.append(["运营建议", item])
        overall = analysis.get("overall") or {}
        if overall.get("totalScore") is not None:
            rowse.append(["总体评分(/100)", overall.get("totalScore")])
        if overall.get("replicabilityStars") is not None:
            rowse.append(["可复制性(/5)", overall.get("replicabilityStars")])
        for hl in overall.get("highlights") or []:
            rowse.append([hl.get("type", "亮点"), hl.get("text", "")])
        if overall.get("primaryImprovement"):
            rowse.append(["首要改进", overall["primaryImprovement"]])
        tags = analysis.get("tags") or []
        if tags:
            rowse.append(["标签", "、".join(str(t) for t in tags)])
        if len(rowse) > 1:
            sheets.append(("分析-策略建议", rowse))

    # Sheet 6: 费用明细
    rows6 = [["步骤", "接口", "消费(元)", "余额(元)"]]
    total = 0
    for item in billing_list:
        consumption = item.get("consumption")
        if consumption is not None:
            total += consumption
        rows6.append([
            item.get("name", ""),
            item.get("endpoint", ""),
            "%.6f" % consumption if consumption is not None else "-",
            "%.6f" % item.get("balance") if item.get("balance") is not None else "-",
        ])
    rows6.append(["合计", "", "%.6f" % total, ""])
    sheets.append(("费用明细", rows6))

    # Sheet: 报告说明（方法论、口径、限制、声明）
    rows_notes = [["项目", "说明"]]
    rows_notes.append(["数据来源", "作品元信息与互动数据：曼格云视频号作品资料接口；"
                                  "画面分段与镜头语言：视频视觉理解模型"])
    rows_notes.append(["数据性质-实测", "接口直接返回的数据"])
    rows_notes.append(["数据性质-模型输出", "模型对画面的观察结果，可能存在识别误差"])
    rows_notes.append(["数据性质-推断", "基于上述数据作出的分析判断，属于观点而非事实"])
    rows_notes.append(["指标口径", METRIC_NOTE])
    rows_notes.append(["计算口径", METHOD_NOTE])
    rows_notes.append(["限制1", "视频号接口不提供播放量，本报告不含播放量与互动率；"
                               "传播判断基于四项互动的相对结构，不代表触达规模"])
    rows_notes.append(["限制2", "评论区内容、账号粉丝量、流量来源、完播率未纳入采集范围"])
    rows_notes.append(["限制3", "受众画像为推断结果，非平台官方统计"])
    rows_notes.append(["使用声明", "本报告为内容分析方法论产出，评分与结论用于创作参考，"
                                  "不构成对账号运营效果的保证，亦不构成任何商业或法律意见"])
    rows_notes.append(["生成时间", datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")])
    sheets.append(("报告说明", rows_notes))

    # --- 生成 xlsx ---
    shared_strings = []
    string_map = {}

    def _str_idx(s):
        s = str(s) if s is not None else ""
        if s in string_map:
            return string_map[s]
        idx = len(shared_strings)
        shared_strings.append(s)
        string_map[s] = idx
        return idx

    def _cell_xml(col_idx, row_idx, value):
        ref = "%s%d" % (_col_letter(col_idx), row_idx)
        if value is None or value == "":
            return ""
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return '<c r="%s" t="n"><v>%s</v></c>' % (ref, value)
        sidx = _str_idx(value)
        return '<c r="%s" t="s"><v>%d</v></c>' % (ref, sidx)

    def _build_sheet(name, rows):
        xml_parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
        xml_parts.append(
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        )
        # 列宽
        max_cols = max(len(r) for r in rows) if rows else 1
        xml_parts.append("<cols>")
        for ci in range(max_cols):
            width = 18
            for row in rows:
                if ci < len(row) and len(str(row[ci] or "")) > 20:
                    width = max(width, min(50, len(str(row[ci])) + 2))
            xml_parts.append('<col min="%d" max="%d" width="%d" customWidth="1"/>' % (ci + 1, ci + 1, width))
        xml_parts.append("</cols>")
        xml_parts.append('<sheetData>')
        for ri, row in enumerate(rows, 1):
            xml_parts.append('<row r="%d">' % ri)
            for ci, val in enumerate(row):
                xml_parts.append(_cell_xml(ci, ri, val))
            xml_parts.append('</row>')
        xml_parts.append('</sheetData></worksheet>')
        return "".join(xml_parts)

    # 构建各 sheet XML（这一步会通过 _cell_xml/_str_idx 填充 shared_strings）
    sheet_data = []
    sheet_rels = []
    workbook_sheets = []
    for si, (name, rows) in enumerate(sheets):
        sheet_path = "xl/worksheets/sheet%d.xml" % (si + 1)
        sheet_data.append((sheet_path, _build_sheet(name, rows)))
        sheet_rels.append(
            '<Relationship Id="rId%d" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            'Target="worksheets/sheet%d.xml"/>' % (si + 1, si + 1)
        )
        workbook_sheets.append(
            '<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (_xlsx_escape(name), si + 1, si + 1)
        )

    # 构建 sharedStrings.xml（必须在 _build_sheet 之后，否则列表为空！）
    ss_parts = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    ss_parts.append(
        '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="%d" uniqueCount="%d">'
        % (len(shared_strings), len(shared_strings))
    )
    for s in shared_strings:
        ss_parts.append('<si><t xml:space="preserve">%s</t></si>' % _xlsx_escape(s))
    ss_parts.append('</sst>')
    shared_strings_xml = "".join(ss_parts)

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/sharedStrings.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
        + "".join(
            '<Override PartName="/xl/worksheets/sheet%d.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (i + 1)
            for i in range(len(sheets))
        )
        + '</Types>'
    )

    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        '</Relationships>'
    )

    workbook = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        '<sheets>' + "".join(workbook_sheets) + '</sheets>'
        '</workbook>'
    )

    workbook_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + "".join(sheet_rels)
        + '<Relationship Id="rId%d" '
          'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" '
          'Target="sharedStrings.xml"/>' % (len(sheets) + 1)
        + '</Relationships>'
    )

    # 写入 zip
    if not out_path:
        out_path = os.path.join(os.getcwd(), "wm_video_report.xlsx")
    if os.path.isdir(out_path):
        out_path = os.path.join(out_path, "wm_video_report.xlsx")

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types)
        zf.writestr("_rels/.rels", rels)
        zf.writestr("xl/workbook.xml", workbook)
        zf.writestr("xl/_rels/workbook.xml.rels", workbook_rels)
        zf.writestr("xl/sharedStrings.xml", shared_strings_xml)
        for path, content in sheet_data:
            zf.writestr(path, content)

    return os.path.abspath(out_path)


# ===========================================================================
# HTML 结果看板（自包含 Dashboard）
# ===========================================================================

def render_html_dashboard(info_payload, analysis_payload, billing_list, input_desc, is_local=False,
                          out_path=None, analysis=None):
    """生成自包含 HTML 看板文件（数据层 + 可选 AI 分析层）。返回文件路径。"""
    info_payload = normalize_info(info_payload)
    info_data = (info_payload or {}).get("data") or {}
    a_data = (analysis_payload or {}).get("data") or {}
    obs = a_data.get("observation") or {}
    media_list = info_data.get("media") or []
    media = media_list[0] if media_list else {}
    _spec_list_h = media.get("spec") or []
    _spec_h = _spec_list_h[0] if _spec_list_h else {}
    metrics = _norm_metrics(info_data.get("metrics"))
    segments = obs.get("segments") or []
    facts = obs.get("visualFacts") or []
    uncertainties = obs.get("uncertainties") or []

    title = info_data.get("title") or info_data.get("description") or "(无标题)"
    account = info_data.get("accountName") or "未知"
    published = _fmt_time(info_data.get("publishedAt"))
    cover = info_data.get("coverUrl") or ""
    summary = obs.get("summary") or "(未返回摘要)"

    # 互动数据（视频号 API 不返回播放量 viewCount，不展示）
    like_c = metrics.get("likeCount")
    share_c = metrics.get("shareCount")
    comment_c = metrics.get("commentCount")
    recommend_c = metrics.get("recommendCount")
    total_inter = interaction_total(metrics)

    # 最大值用于条形图比例（不包含播放量）
    metric_vals = [v for v in (like_c, share_c, comment_c, recommend_c) if v is not None]
    max_metric = max(metric_vals + [1])

    # 费用
    total_cost = sum(b["consumption"] or 0 for b in billing_list)

    # HTML 模板
    html = []
    html.append("<!DOCTYPE html>")
    html.append('<html lang="zh-CN">')
    html.append("<head>")
    html.append('<meta charset="UTF-8">')
    html.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append("<title>%s - 视频拆解看板</title>" % _html_escape(title))
    html.append("<style>")
    html.append(_dashboard_css())
    html.append("</style>")
    html.append("</head>")
    html.append("<body>")
    html.append('<div class="dashboard">')

    # --- 头部 ---
    html.append('<header class="header">')
    html.append('<div class="header-left">')
    html.append('<div class="badge">视频号视频拆解报告</div>')
    html.append('<h1>%s</h1>' % _html_escape(title))
    html.append('<div class="meta-row">')
    html.append('<span class="meta-item">发布账号：<strong>%s</strong></span>' % _html_escape(account))
    html.append('<span class="meta-item">发布时间：%s</span>' % _html_escape(published))
    duration_str = _fmt_dur_seconds(_media_duration_seconds(media, _spec_h))
    width_val = media.get("width")
    height_val = media.get("height")
    res_str = "%sx%s" % (width_val, height_val) if width_val and height_val else "未知"
    html.append('<span class="meta-item">时长：%s</span>' % _html_escape(duration_str))
    html.append('<span class="meta-item">分辨率：%s</span>' % _html_escape(res_str))
    html.append('<span class="meta-item">大小：%s</span>' % _html_escape(_fmt_bytes(media.get("fileSize"))))
    html.append('</div>')
    html.append('</div>')
    if cover:
        html.append('<div class="header-right">')
        html.append('<img src="%s" alt="封面" class="cover-img">' % _html_escape_attr(cover))
        html.append('</div>')
    html.append('</header>')

    # --- 执行摘要（结论前置：先给判断，再给依据） ---
    _prof_h = infer_interaction_profile(metrics) if not is_local else None
    _ov_h = (analysis or {}).get("overall") or {}
    _attr_h = (analysis or {}).get("viralAttribution") or []
    html.append('<section class="exec">')
    html.append('<div class="exec-title">执行摘要</div>')
    html.append('<div class="exec-kv">')
    if not is_local:
        for _key, _lbl in _INTERACTION_KEYS:
            html.append('<div>%s<b>%s</b></div>' % (_lbl, _html_escape(metric_display(info_data, _key))))
    html.append('<div>时长<b>%s</b></div>' % _html_escape(
        _fmt_dur_seconds(_media_duration_seconds(media, _spec_h))))
    if _ov_h.get("totalScore") is not None:
        html.append('<div>综合评分<b>%s / 100</b></div>' % _html_escape(str(_ov_h.get("totalScore"))))
    html.append('</div>')
    html.append('<div class="exec-body">')
    if _prof_h:
        html.append('<p>互动结构显示：主导指标为<b>%s</b>（占四指标总量 %.1f%%），'
                    '互动结构为<b>%s</b>。' % (
                        _html_escape(_prof_h["dominant"]),
                        _prof_h["shares"][_prof_h["dominant"]],
                        _html_escape(_prof_h["type"])))
    if _attr_h:
        _top = _attr_h[0]
        html.append('<p>优先分析因素：%s（分析权重 %s%%，非实测传播贡献）——%s' % (
            _html_escape(_top.get("factor", "")), _html_escape(str(_top.get("contribution", ""))),
            _html_escape(_top.get("detail", ""))))
    if _ov_h.get("primaryImprovement"):
        html.append('<p>最优先改进项：%s</p>' % _html_escape(_ov_h["primaryImprovement"]))
    html.append('</div>')
    html.append('</section>')

    # --- 图例：数据性质说明 ---
    html.append('<div class="legend" style="background:var(--paper);border:1px solid var(--rule);'
                'padding:12px 34px;margin-bottom:18px">')
    for _cls, _lab, _desc in (("src-fact", "实测", "接口直接返回的数据"),
                              ("src-model", "模型输出", "视觉理解模型的画面观察结果"),
                              ("src-infer", "推断", "基于上述数据作出的分析判断，非事实")):
        html.append('<span class="legend-item"><span class="src-tag %s">%s</span>%s</span>'
                    % (_cls, _lab, _desc))
    html.append('</div>')

    # --- 总体评估横幅（分析层，置于最前给结论） ---
    overall_h = (analysis or {}).get("overall") or {}
    if overall_h and (overall_h.get("totalScore") is not None or overall_h.get("highlights")):
        html.append('<section class="card overall-card">')
        html.append('<div class="overall-score">')
        if overall_h.get("totalScore") is not None:
            html.append('<div class="overall-num">%s</div>' % _html_escape(str(overall_h.get("totalScore"))))
            html.append('<div class="overall-unit">/100 总体评分</div>')
        if overall_h.get("replicabilityStars") is not None:
            try:
                st = int(overall_h.get("replicabilityStars") or 0)
            except (TypeError, ValueError):
                st = 0
            html.append('<div class="overall-stars">%s</div>' % _html_escape("★" * st + "☆" * (5 - st)))
            html.append('<div class="overall-unit">可复制性</div>')
        html.append('</div>')
        html.append('<div class="overall-body">')
        for hl in overall_h.get("highlights") or []:
            hl_type = hl.get("type", "亮点")
            cls = "hl-good" if hl_type == "亮点" else "hl-bad"
            html.append('<p class="%s"><strong>【%s】</strong>%s</p>' % (
                cls, _html_escape(hl_type), _html_escape(hl.get("text", ""))))
        if overall_h.get("primaryImprovement"):
            html.append('<p class="hl-fix"><strong>首要改进：</strong>%s</p>' % _html_escape(overall_h["primaryImprovement"]))
        html.append('</div>')
        html.append('</section>')

    # --- 受众画像（分析层） ---
    aud_h = (analysis or {}).get("audience") or {}
    if aud_h:
        html.append('<section class="card">')
        html.append(_sec_title("受众画像", 'infer'))
        html.append('<table class="data-table aud-table">')
        html.append('<tbody>')
        if aud_h.get("ageRange"):
            html.append('<tr><td class="aud-label">年龄段</td><td>%s</td></tr>' % _html_escape(aud_h["ageRange"]))
        if aud_h.get("gender"):
            html.append('<tr><td class="aud-label">性别比例</td><td>%s</td></tr>' % _html_escape(aud_h["gender"]))
        interests = aud_h.get("interests")
        if interests:
            if isinstance(interests, list):
                interests = "、".join(str(i) for i in interests)
            html.append('<tr><td class="aud-label">兴趣标签</td><td>%s</td></tr>' % _html_escape(interests))
        if aud_h.get("consumption"):
            html.append('<tr><td class="aud-label">消费能力</td><td>%s</td></tr>' % _html_escape(aud_h["consumption"]))
        html.append('</tbody></table>')
        html.append('</section>')

    # --- KPI 卡片（视频号无播放量，只有四类互动 + 互动总量） ---
    if not is_local:
        html.append('<section class="kpi-grid">')
        kpi_items = [
            ("点赞", like_c, "#E74C3C"),
            ("转发", share_c, "#2ECC71"),
            ("评论", comment_c, "#F39C12"),
            ("推荐", recommend_c, "#9B59B6"),
            ("互动计数合计", total_inter, "#34495E"),
        ]
        for label, val, color in kpi_items:
            html.append('<div class="kpi-card" style="border-top:3px solid %s">' % color)
            html.append('<div class="kpi-label">%s</div>' % label)
            key = next((k for k, label_ in _INTERACTION_KEYS if label_ == label), None)
            display = metric_display(info_data, key) if key else (str(val) if val is not None else "数据不全，未计算")
            html.append('<div class="kpi-value">%s</div>' % _html_escape(display))
            html.append('</div>')
        html.append('</section>')

        # --- 条形图（不含播放量） ---
        html.append('<section class="card">')
        html.append(_sec_title("互动数据对比", 'fact'))
        bar_items = [
            ("点赞", like_c, "#E74C3C"),
            ("转发", share_c, "#2ECC71"),
            ("评论", comment_c, "#F39C12"),
            ("推荐", recommend_c, "#9B59B6"),
        ]
        for label, val, color in bar_items:
            pct = (val / max_metric * 100) if val is not None else 0
            html.append('<div class="bar-row">')
            html.append('<span class="bar-label">%s</span>' % label)
            html.append('<div class="bar-track">')
            html.append('<div class="bar-fill" style="width:%.1f%%;background:%s"></div>' % (pct, color))
            html.append('</div>')
            key = next(k for k, label_ in _INTERACTION_KEYS if label_ == label)
            html.append('<span class="bar-val">%s</span>' % _html_escape(metric_display(info_data, key)))
            html.append('</div>')
        html.append('<p class="muted">%s 视频号 API 不返回播放量，故无互动率；合计不代表去重人数。</p>' % _html_escape(METRIC_NOTE))
        html.append('</section>')

    # --- 互动结构反推 ---
    prof = infer_interaction_profile(metrics)
    if prof:
        html.append('<section class="card">')
        html.append(_sec_title("互动数据反推", 'infer'))
        html.append('<p class="muted">以下仅描述互动计数的相对结构，不据此直接判定传播原因或受众动机。</p>')
        html.append('<div class="infer-banner">')
        html.append('<div><span class="infer-label">主导指标</span>'
                    '<strong class="infer-dominant">%s</strong></div>' % _html_escape(prof["dominant"]))
        html.append('<div><span class="infer-label">互动结构</span>'
                    '<strong class="infer-type">%s</strong></div>' % _html_escape(prof["type"]))
        html.append('</div>')

        # 占比条形图
        html.append('<div class="bars">')
        for name in ("点赞", "转发", "评论", "推荐"):
            pct = prof["shares"][name]
            html.append('<div class="bar-row">')
            html.append('<span class="bar-label">%s</span>' % name)
            html.append('<div class="bar-track">')
            html.append('<div class="bar-fill" style="width:%.1f%%"></div>' % pct)
            html.append('</div>')
            html.append('<span class="bar-val">%.1f%%</span>' % pct)
            html.append('</div>')
        html.append('</div>')
        html.append('<p class="muted">占比 = 该指标 / 四指标之和；'
                    '转发/点赞 %.1f%%｜评论/点赞 %.1f%%｜推荐/点赞 %.1f%%</p>' % (
                        prof["ratios"]["转发/点赞"], prof["ratios"]["评论/点赞"],
                        prof["ratios"]["推荐/点赞"]))

        # 逐项解读
        html.append('<h3 class="sub-title">逐项解读</h3>')
        html.append('<ul class="signal-list">')
        for name, level, text in prof["signals"]:
            html.append('<li class="signal-item lv-%s">'
                        '<span class="signal-tag">%s · %s</span>'
                        '<span class="signal-text">%s</span></li>' % (
                            {"强": "high", "中": "mid", "弱": "low"}.get(level, "mid"),
                            _html_escape(name), _html_escape(level), _html_escape(text)))
        html.append('</ul>')

        # 推导动作
        if prof["actions"]:
            html.append('<h3 class="sub-title">由互动结构推导的动作</h3>')
            html.append('<ol class="action-list">')
            for act in prof["actions"]:
                html.append('<li>%s</li>' % _html_escape(act))
            html.append('</ol>')
        notes_h = (analysis or {}).get("interactionNotes") or []
        if notes_h:
            html.append('<h3 class="sub-title">分析层补充解读</h3>')
            html.append('<ul class="action-list">')
            for n in notes_h:
                html.append('<li>%s</li>' % _html_escape(_as_text(n)))
            html.append('</ul>')
        html.append('</section>')
    elif not is_local:
        html.append('<section class="card"><p class="muted">互动数据不足，无法进行结构反推。</p></section>')
    else:
        html.append('<section class="card"><p class="muted">本地视频无互动数据。</p></section>')

    # --- 内容摘要 ---
    html.append('<section class="card">')
    html.append(_sec_title("内容摘要", 'model'))
    html.append('<p class="summary-text">%s</p>' % _html_escape(summary))
    _est_dur = obs.get("durationSeconds")
    try:
        _est_dur = float(_est_dur) if _est_dur is not None else None
    except (TypeError, ValueError):
        _est_dur = None
    if _est_dur:
        html.append('<p class="muted">模型估计时长：%.1f 秒</p>' % _est_dur)
    html.append('</section>')

    # --- 时间线分段（数据层 + 分析层解读） ---
    if segments:
        struct_h = (analysis or {}).get("structure") or {}
        seg_notes_h = struct_h.get("segmentNotes") or {}
        html.append('<section class="card">')
        html.append(_sec_title("结构拆解", 'infer'))
        if struct_h.get("scriptType"):
            html.append('<p class="struct-type">脚本类型：<strong>%s</strong></p>' % _html_escape(struct_h["scriptType"]))
        if struct_h.get("rationale"):
            html.append('<p class="struct-rationale"><strong>判断依据：</strong>%s</p>' % _html_escape(struct_h["rationale"]))
        html.append('<div class="timeline">')
        for idx, seg in enumerate(segments, 1):
            start = _pick(seg, "startSeconds", "start")
            end = _pick(seg, "endSeconds", "end")
            visual = _pick(seg, "visual", "visualDescription")
            onscreen = _pick(seg, "onscreenTexts", "onscreenText", "onScreenText")
            speech = _pick(seg, "speechSummary", "speech")
            shot = _pick(seg, "shotType", "shot", "shotInfo")
            camera = _pick(seg, "cameraMovement", "camera")
            narrative = _pick(seg, "narrativeFunction", "narrative")
            transition = _pick(seg, "transition")
            emotion = _pick(seg, "emotionCues", "emotion")
            confidence = _pick(seg, "confidence", default=None)
            conf_pct = int(float(confidence) * 100) if confidence else None

            html.append('<div class="tl-item">')
            html.append('<div class="tl-marker">')
            html.append('<div class="tl-dot"></div>')
            html.append('</div>')
            html.append('<div class="tl-content">')
            html.append('<div class="tl-header">')
            html.append('<span class="tl-seg">片段 %d</span>' % idx)
            html.append('<span class="tl-time">%s – %s</span>' % (_fmt_seconds(start), _fmt_seconds(end)))
            if conf_pct is not None:
                color = "#2ECC71" if conf_pct >= 80 else "#F39C12" if conf_pct >= 50 else "#E74C3C"
                html.append('<span class="tl-conf" style="background:%s">%d%%</span>' % (color, conf_pct))
            html.append('</div>')
            if visual:
                html.append('<p class="tl-field"><strong>画面：</strong>%s</p>' % _html_escape(_as_text(visual)))
            if onscreen:
                html.append('<p class="tl-field"><strong>屏幕文字：</strong>%s</p>' % _html_escape(_as_text(onscreen, sep=" ｜ ")))
            if speech:
                html.append('<p class="tl-field"><strong>语音/解说：</strong>%s</p>' % _html_escape(_as_text(speech)))
            if shot:
                html.append('<p class="tl-field"><strong>景别：</strong>%s</p>' % _html_escape(_as_text(shot)))
            if camera:
                html.append('<p class="tl-field"><strong>运镜：</strong>%s</p>' % _html_escape(_as_text(camera)))
            if transition:
                html.append('<p class="tl-field"><strong>转场：</strong>%s</p>' % _html_escape(_as_text(transition)))
            if emotion:
                html.append('<p class="tl-field"><strong>情绪：</strong>%s</p>' % _html_escape(_as_text(emotion, sep=" ｜ ")))
            if narrative:
                html.append('<p class="tl-field"><strong>叙事作用：</strong>%s</p>' % _html_escape(_as_text(narrative)))
            note_h = seg_notes_h.get(str(idx)) or seg_notes_h.get(idx)
            if note_h:
                html.append('<p class="tl-note"><strong>💡 为什么有效：</strong>%s</p>' % _html_escape(note_h))
            html.append('</div>')
            html.append('</div>')
        html.append('</div>')
        if struct_h.get("summary"):
            html.append('<p class="struct-summary"><strong>结构总结：</strong>%s</p>' % _html_escape(struct_h["summary"]))
        html.append('</section>')

    # --- 爆款归因（分析层） ---
    viral_h = (analysis or {}).get("viralAttribution") or []
    if viral_h:
        html.append('<section class="card">')
        html.append(_sec_title("爆款归因", 'infer'))
        html.append('<table class="data-table">')
        html.append('<thead><tr><th>#</th><th>层</th><th>因素</th><th>详细描述</th><th>分析权重（非因果贡献）</th><th>数据佐证</th></tr></thead>')
        html.append('<tbody>')
        for i, item in enumerate(viral_h, 1):
            contrib = item.get("contribution")
            try:
                contrib_num = float(contrib) if contrib is not None else 0
            except (TypeError, ValueError):
                contrib_num = 0
            html.append('<tr>')
            html.append('<td>%s</td>' % _html_escape(str(item.get("rank") or i)))
            html.append('<td><span class="layer-chip">%s</span></td>' % _html_escape(item.get("layer", "")))
            html.append('<td><strong>%s</strong></td>' % _html_escape(item.get("factor", "")))
            html.append('<td class="contrib-detail">%s</td>' % _html_escape(item.get("detail", "")))
            if contrib is not None:
                html.append('<td><div class="contrib-bar"><div class="contrib-fill" style="width:%.0f%%"></div></div><span class="contrib-num">%d%%</span></td>'
                            % (min(100, contrib_num), int(contrib_num)))
            else:
                html.append('<td>-</td>')
            html.append('<td class="evid-cell">%s</td>' % _html_escape(item.get("evidence", "") or "-"))
            html.append('</tr>')
        html.append('</tbody></table>')
        html.append('</section>')

    # --- 爆款公式 + 可复刻性（分析层） ---
    formula_h = (analysis or {}).get("viralFormula")
    repl_h = (analysis or {}).get("replicability") or {}
    if formula_h or repl_h:
        html.append('<section class="card">')
        if formula_h:
            html.append(_sec_title("爆款公式", 'infer'))
            html.append('<div class="formula-box">%s</div>' % _html_escape(formula_h))
        if repl_h.get("score") is not None or repl_h.get("note"):
            html.append('<div class="repl-grid">')
            if repl_h.get("score") is not None:
                html.append('<div class="repl-item"><span class="repl-label">可复刻性</span><span class="repl-val">%s/5</span></div>'
                            % _html_escape(str(repl_h.get("score"))))
            if repl_h.get("replicableStrategy"):
                html.append('<div class="repl-item"><span class="repl-label">可复刻策略</span><span class="repl-text">%s</span></div>'
                            % _html_escape(repl_h["replicableStrategy"]))
            if repl_h.get("notApplicableScenarios"):
                html.append('<div class="repl-item"><span class="repl-label">不适用场景</span><span class="repl-text">%s</span></div>'
                            % _html_escape(repl_h["notApplicableScenarios"]))
            if repl_h.get("note"):
                html.append('<div class="repl-item"><span class="repl-label">说明</span><span class="repl-text">%s</span></div>'
                            % _html_escape(repl_h["note"]))
            html.append('</div>')
        html.append('</section>')

    # --- 六维评分（分析层） ---
    six_h = (analysis or {}).get("sixDimScores") or []
    if six_h:
        html.append('<section class="card">')
        html.append(_sec_title("六维评分", 'infer'))
        for item in six_h:
            try:
                sc = float(item.get("score"))
            except (TypeError, ValueError):
                sc = None
            html.append('<div class="score-row">')
            html.append('<div class="score-head">')
            html.append('<span class="score-name">%s</span>' % _html_escape(item.get("dimension", "")))
            if sc is not None:
                color = "#2ECC71" if sc >= 8 else "#F39C12" if sc >= 6 else "#E74C3C"
                html.append('<span class="score-val" style="color:%s">%.1f/10</span>' % (color, sc))
            html.append('</div>')
            if sc is not None:
                html.append('<div class="score-track"><div class="score-fill" style="width:%.0f%%;background:%s"></div></div>'
                            % (min(100, sc * 10), "#2ECC71" if sc >= 8 else "#F39C12" if sc >= 6 else "#E74C3C"))
            if item.get("evidence"):
                html.append('<p class="score-evid"><strong>节奏证据：</strong>%s</p>' % _html_escape(item["evidence"]))
            if item.get("reason"):
                html.append('<p class="score-reason">%s</p>' % _html_escape(item["reason"]))
            if item.get("suggestion"):
                html.append('<p class="score-sugg"><strong>改进建议：</strong>%s</p>' % _html_escape(item["suggestion"]))
            html.append('</div>')
        html.append('</section>')

    # --- 运营建议（分析层） ---
    ops_h = (analysis or {}).get("operations") or []
    if ops_h:
        html.append('<section class="card">')
        html.append(_sec_title("运营建议", 'infer'))
        html.append('<ol class="ops-list">')
        for item in ops_h:
            html.append('<li>%s</li>' % _html_escape(str(item)))
        html.append('</ol>')
        html.append('</section>')

    # --- 标签（分析层） ---
    tags_h = (analysis or {}).get("tags") or []
    if tags_h:
        html.append('<section class="card">')
        html.append(_sec_title("标签", 'infer'))
        html.append('<div class="tag-chips">')
        for t in tags_h:
            html.append('<span class="tag-chip">%s</span>' % _html_escape(str(t)))
        html.append('</div>')
        html.append('</section>')

    # --- 画面事实 ---
    if facts:
        html.append('<section class="card">')
        html.append(_sec_title("画面事实与证据", 'fact'))
        html.append('<table class="data-table">')
        html.append('<thead><tr><th>#</th><th>画面事实</th><th>时间范围</th><th>证据类型</th><th>置信度</th></tr></thead>')
        html.append('<tbody>')
        for idx, fact in enumerate(facts, 1):
            desc = _pick(fact, "statement", "description", "fact", default="")
            if not desc:
                desc = _as_text(fact)
            ev = _pick(fact, "evidenceType", "evidence", default="")
            f_start = _pick(fact, "startSeconds", "start", default=None)
            f_end = _pick(fact, "endSeconds", "end", default=None)
            tr = _pick(fact, "timeRange", "time", default="")
            if not tr and f_start is not None:
                tr = "%s – %s" % (_fmt_seconds(f_start), _fmt_seconds(f_end))
            conf = _pick(fact, "confidence", default=None)
            conf_str = "%.0f%%" % (float(conf) * 100) if conf else ""
            html.append('<tr>')
            html.append('<td>%d</td>' % idx)
            html.append('<td>%s</td>' % _html_escape(_as_text(desc)))
            html.append('<td>%s</td>' % _html_escape(tr))
            html.append('<td>%s</td>' % _html_escape(ev))
            html.append('<td>%s</td>' % _html_escape(conf_str))
            html.append('</tr>')
        html.append('</tbody></table>')
        html.append('</section>')

    # --- 不确定项 ---
    if uncertainties:
        html.append('<section class="card">')
        html.append(_sec_title("不确定项", 'fact'))
        html.append('<ul class="uncert-list">')
        for idx, item in enumerate(uncertainties, 1):
            if isinstance(item, dict):
                desc = item.get("description") or item.get("item") or str(item)
                reason = item.get("reason") or item.get("cause") or ""
            else:
                desc = str(item)
                reason = ""
            html.append('<li class="uncert-item">')
            html.append('<span class="uncert-num">%d</span>' % idx)
            html.append('<div>')
            html.append('<p>%s</p>' % _html_escape(desc))
            if reason:
                html.append('<p class="muted">原因：%s</p>' % _html_escape(reason))
            html.append('</div>')
            html.append('</li>')
        html.append('</ul>')
        html.append('</section>')

    # --- 费用明细 ---
    html.append('<section class="card">')
    html.append(_sec_title("费用明细", 'fact'))
    html.append('<table class="data-table">')
    html.append('<thead><tr><th>步骤</th><th>接口</th><th>消费(元)</th><th>余额(元)</th></tr></thead>')
    html.append('<tbody>')
    for item in billing_list:
        consumption = item.get("consumption")
        balance = item.get("balance")
        html.append('<tr>')
        html.append('<td>%s</td>' % _html_escape(item.get("name", "")))
        html.append('<td class="mono">%s</td>' % _html_escape(item.get("endpoint", "")))
        html.append('<td>%s</td>' % ("%.6f" % consumption if consumption is not None else "-"))
        html.append('<td>%s</td>' % ("%.6f" % balance if balance is not None else "-"))
        html.append('</tr>')
    html.append('<tr class="total-row">')
    html.append('<td colspan="2">合计</td>')
    html.append('<td>%.6f</td>' % total_cost)
    html.append('<td></td>')
    html.append('</tr>')
    html.append('</tbody></table>')
    html.append('</section>')

    # --- 方法论与数据说明 ---
    html.append('<section class="method">')
    html.append('<h3>方法论与数据说明</h3>')
    html.append('<ul>')
    html.append('<li><b>数据来源</b>：作品元信息与互动数据取自曼格云视频号作品资料接口；'
                '画面分段、镜头语言、屏幕文字、语音摘要取自视频视觉理解模型。</li>')
    html.append('<li><b>数据性质</b>：标注「实测」为接口返回值；「模型输出」为模型对画面的观察，'
                '可能存在识别误差；「推断」为基于前两者的分析判断，属于观点而非事实。</li>')
    html.append('<li><b>互动结构口径</b>：%s %s</li>' % (_html_escape(METHOD_NOTE), _html_escape(METRIC_NOTE)))
    html.append('<li><b>口径限制</b>：视频号接口<b>不提供播放量</b>，因此本报告不含播放量与互动率；'
                '所有传播判断均基于四项互动的相对结构，不代表触达规模。'
                '评论区内容、账号粉丝量、流量来源未纳入本次采集范围。</li>')
    html.append('</ul>')
    html.append('<p><b>使用声明</b>：本报告为内容分析方法论产出，评分与结论用于创作参考，'
                '不构成对账号运营效果的保证，亦不构成任何商业或法律意见。'
                '受众画像、爆款归因等「推断」类内容依赖有限样本与经验规则，请结合账号自身数据判断。</p>')
    html.append('</section>')

    # --- 页脚 ---
    html.append('<footer class="footer">')
    html.append('<p>生成时间：%s ｜ 数据来源：曼格云 API ｜ 本报告由 WorkBuddy 视频拆解技能生成</p>'
                % datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S"))
    html.append('</footer>')

    html.append('</div>')
    html.append("</body></html>")

    html_content = "\n".join(html)

    if not out_path:
        out_path = os.path.join(os.getcwd(), "wm_video_dashboard.html")
    if os.path.isdir(out_path):
        out_path = os.path.join(out_path, "wm_video_dashboard.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return os.path.abspath(out_path)


def _fmt_num(n):
    """数字格式化（千分位）。"""
    if isinstance(n, str):
        return n
    if n is None:
        return "未获取"
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    if n >= 10000:
        return "%.1f万" % (n / 10000)
    return format(n, ",")

def _html_escape(text):
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s

def _html_escape_attr(text):
    if text is None:
        return ""
    s = str(text)
    s = s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return s

_SEC_SRC_LABEL = {
    "fact": ("实测", "src-fact"),
    "model": ("模型输出", "src-model"),
    "infer": ("推断", "src-infer"),
}


def _sec_title(text, src=None):
    """章节标题：CSS 自动编号 + 数据来源标注（实测 / 模型输出 / 推断）。"""
    if src and src in _SEC_SRC_LABEL:
        label, cls = _SEC_SRC_LABEL[src]
        return ('<h2 class="card-title">%s'
                '<span class="src-tag %s">%s</span></h2>'
                % (_html_escape(text), cls, label))
    return '<h2 class="card-title">%s</h2>' % _html_escape(text)


def _dashboard_css():
    """返回报告样式。优先读取同目录 report_style.css，缺失时回退到内嵌精简样式。"""
    css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_style.css")
    try:
        with io.open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return "*{margin:0;padding:0;box-sizing:border-box}body{font-family:sans-serif;background:#f2f3f5}"


# ===========================================================================
# 主流程
# ===========================================================================

def is_share_url(text):
    return bool(SHARE_URL_RE.match(text.strip()))

def is_local_video(path):
    if not os.path.isfile(path):
        return False
    ext = os.path.splitext(path)[1].lower()
    if ext not in SUPPORTED_EXTS:
        return False
    size = os.path.getsize(path)
    return 0 < size < MAX_VIDEO_BYTES

def _billing_record(name, payload, endpoint=""):
    # 缓存命中的响应：本次未实际调用接口、未扣费，消费按 0 计并标注来源
    if payload.get("_fromCache"):
        return {
            "name": name + "（缓存）",
            "endpoint": endpoint,
            "consumption": 0.0,
            "balance": None,
        }
    return {
        "name": name,
        "endpoint": endpoint,
        "consumption": payload.get("consumption") if isinstance(payload.get("consumption"), (int, float)) else None,
        "balance": payload.get("balance") if isinstance(payload.get("balance"), (int, float)) else None,
    }

# 计费单价（元/次，与 references/api.md 一致；缓存命中时该步骤不扣费）
PRICE_INFO = 0.21                      # 接口33 作品资料（url 路线）
PRICE_ANALYZE = {"summary": 0.12, "timeline": 0.18, "decompose": 0.24}
MODE_LABELS = {
    "summary": "摘要档：仅内容摘要，无时间线",
    "timeline": "时间线档：内容摘要 + 分段时间线",
    "decompose": "深度档（推荐）：摘要 + 分段 + 镜头/运镜/转场/情绪 + 画面事实",
}


def estimate_cost(input_text, mode="decompose", visual=True):
    """预估本次拆解费用，不调用任何接口、不扣费。

    返回 (明细列表, 合计)。分享链接需作品资料费；本地视频无元信息，只计视觉理解。
    """
    items = []
    products = {product_path(p): p for p in catalog(BASE_URL, get_api_key() or "")}
    total = 0.0
    is_share = False
    try:
        is_share = bool(is_share_url(input_text))
    except Exception:
        is_share = False
    if is_share:
        price = price_micros(products[PATH_INFO], {"url": input_text}) / 1000000
        items.append(("作品资料", price))
        total += price
    if visual:
        price = price_micros(products[PATH_ANALYZE], {"analysisMode": mode}) / 1000000
        items.append(("视觉理解·%s（接口27）" % mode, price))
        total += price
    return items, round(total, 4)


def run_estimate(input_text, mode="decompose", visual=True):
    """输出费用预估（零 API 调用）。"""
    items, total = estimate_cost(input_text, mode, visual)
    print("实时费用预估（只查询产品目录，实际以接口响应 consumption 为准）")
    print("输入：%s" % input_text)
    print("视觉理解：%s" % ("开启（%s）" % mode if visual else "关闭"))
    print("-" * 46)
    for name, price in items:
        print("  %-28s ¥%.2f" % (name, price))
    print("-" * 46)
    print("  %-28s ¥%.2f" % ("合计", total))
    if not is_share_url(input_text):
        print("（本地视频无作品元信息与互动数据，只计视觉理解费用）")
    print()
    if not visual and not is_share_url(input_text):
        print("注意：本地视频关闭视觉理解后将没有任何内容可分析，脚本会拒绝执行。"
              "本地视频请保留视觉理解，或改用视频号分享链接 + --no-visual。")
    print("提示：修改报告请使用 --render 复用已保存数据；重新采集可能产生费用。")


def run_share_link(api_key, share_url, mode, out_path, fmt="all", visual=True):
    """分享链接分支：作品资料 →（可选）下载解密+上传+视觉理解 → 报告。"""
    billing = []

    # 1. 作品资料（接口33）
    log("[进度] 正在获取作品资料（元信息+媒体+互动）…")
    info_payload = resolve_video_info(api_key, share_url)
    billing.append(_billing_record("作品资料", info_payload, PATH_INFO))
    log("  作品资料已获取")

    info_data = info_payload.get("data") or {}
    title = info_data.get("title") or "(无标题)"
    log("  标题：%s" % title)

    # 提取播放地址和解密密钥
    media_list = info_data.get("media") or []
    if not media_list:
        raise SkillError(4, "作品资料未返回媒体信息，无法下载视频")
    media = media_list[0]
    playback_url = media.get("playbackUrl")
    decode_key = media.get("decodeKey")
    if visual and not playback_url:
        raise SkillError(4, "作品资料未返回播放地址（playbackUrl 为空），可能已过期或无权限")

    # 2. 下载视频
    temp_dir = tempfile.mkdtemp(prefix="wm-video-")
    local_video = os.path.join(temp_dir, "video.mp4")
    try:
        if visual:
            log("[进度] 正在本机下载视频…")
            file_size = download_video(
                playback_url, local_video,
                on_progress=lambda pct: log("  下载 %d%%" % pct),
            )
            log("  下载完成，%s" % _fmt_bytes(file_size))

            # 3. 解密
            log("[进度] 正在校验/解密视频…")
            decrypted = decrypt_prefix(local_video, decode_key)
            log("  %s" % ("本机解密和 MP4 校验已完成" if decrypted else "视频无需解密，MP4 校验已完成"))

            # 4. 临时上传
            log("[进度] 正在申请平台临时上传票据…")
            ticket = upload_ticket(api_key, "video.mp4", os.path.getsize(local_video))
            log("[进度] 正在直传视频到平台临时存储…")
            upload_multipart(
                ticket["uploadUrl"], ticket["requiredFields"],
                local_video, "video.mp4",
                on_progress=lambda pct: log("  上传 %d%%" % pct),
            )
            file_url = ticket["fileUrl"]
            log("  上传完成")
        else:
            log("[进度] 已按 --no-visual 跳过视频下载与上传")


        # 5. 视觉理解（接口27，可选）
        if visual:
            log("[进度] 正在进行视觉理解（%s 档位）…" % mode)
            video_sha = _file_sha256(local_video)
            analysis_payload = analyze_video(api_key, file_url, mode, cache_extra=video_sha)
            billing.append(_billing_record("视觉理解", analysis_payload, PATH_ANALYZE))

            a_data = analysis_payload.get("data") or {}
            obs = a_data.get("observation") or {}
            if not obs.get("summary") and not obs.get("segments"):
                raise SkillError(7, "视觉理解完成但返回的 observation 为空")

            log("  视觉理解已完成")
        else:
            log("[进度] 已按 --no-visual 跳过视觉理解，本次仅输出作品资料维度")
            analysis_payload = None

        # 6. 输出结果
        _output_results(info_payload, analysis_payload, billing, share_url,
                        is_local=False, out_path=out_path, fmt=fmt)

    finally:
        # 清理临时目录
        import shutil
        try:
            shutil.rmtree(temp_dir)
            log("[进度] 本机临时文件已清理")
        except Exception:
            pass


def run_local_video(api_key, video_path, mode, out_path, fmt="all", visual=True):
    """本地视频分支：（可选）上传 + 视觉理解 → 报告。"""
    billing = []

    if not os.path.isfile(video_path):
        raise SkillError(2, "文件不存在：%s" % video_path)
    ext = os.path.splitext(video_path)[1].lower()
    if ext not in SUPPORTED_EXTS:
        raise SkillError(2, "不支持的视频格式 %s，支持：%s" % (ext, ", ".join(sorted(SUPPORTED_EXTS))))
    file_size = os.path.getsize(video_path)
    if file_size == 0:
        raise SkillError(2, "文件为空")
    if file_size >= MAX_VIDEO_BYTES:
        raise SkillError(2, "文件超过 128MB（%s），请压缩后重试" % _fmt_bytes(file_size))

    filename = os.path.basename(video_path)
    content_type = "video/mp4"
    if ext in (".mov", ".m4v"):
        content_type = "video/quicktime" if ext == ".mov" else "video/mp4"

    if not visual:
        raise SkillError(2, "本地视频没有作品元信息与互动数据，关闭视觉理解后将无任何内容可分析；"
                            "如需仅看画面拆解请保留视觉理解，或改用视频号分享链接 + --no-visual")

    # 1. 临时上传（无视觉理解时不需要）
    file_url = None
    if visual:
        log("[进度] 正在申请平台临时上传票据…")
        ticket = upload_ticket(api_key, filename, file_size, content_type)
        log("[进度] 正在直传视频到平台临时存储…")
        upload_multipart(
            ticket["uploadUrl"], ticket["requiredFields"],
            video_path, filename, content_type,
            on_progress=lambda pct: log("  上传 %d%%" % pct),
        )
        file_url = ticket["fileUrl"]
        log("  上传完成")

    # 2. 视觉理解（可选）
    if visual:
        log("[进度] 正在进行视觉理解（%s 档位）…" % mode)
        video_sha = _file_sha256(video_path)
        analysis_payload = analyze_video(api_key, file_url, mode, cache_extra=video_sha)
        billing.append(_billing_record("视觉理解", analysis_payload, PATH_ANALYZE))

        a_data = analysis_payload.get("data") or {}
        obs = a_data.get("observation") or {}
        if not obs.get("summary") and not obs.get("segments"):
            raise SkillError(7, "视觉理解完成但返回的 observation 为空")

        log("  视觉理解已完成")
    else:
        log("[进度] 已按 --no-visual 跳过视觉理解")
        analysis_payload = None

    # 3. 输出结果（本地视频无元信息/互动数据）
    _output_results(None, analysis_payload, billing, video_path,
                    is_local=True, out_path=out_path, fmt=fmt)


def _output_results(info_payload, analysis_payload, billing, input_desc,
                     is_local=False, out_path=None, fmt="all", analysis=None,
                     dump_raw=True):
    """根据格式生成并输出结果；同时落地 wm_video_raw.json 供分析层复用。"""
    total = sum(b["consumption"] or 0 for b in billing)
    files = {}

    # 确定输出目录
    out_dir = os.path.dirname(os.path.abspath(out_path)) if out_path else os.getcwd()
    if out_path and os.path.isdir(out_path):
        out_dir = out_path
    os.makedirs(out_dir, exist_ok=True) if out_dir else None

    # Canonical, public interaction facts for the AI stage, including old raw re-renders.
    basis = interaction_basis(info_payload, is_local)
    basis_path = os.path.join(out_dir, "wm_interaction_facts.json")
    with open(basis_path, "w", encoding="utf-8") as f:
        json.dump(basis, f, ensure_ascii=False, indent=2)
    files["interaction_facts"] = os.path.abspath(basis_path)

    # Preserve source response separately; never relabel the raw gateway fields.
    if dump_raw:
        raw = {
            "schemaVersion": "1.0",
            "inputDesc": input_desc,
            "isLocal": bool(is_local),
            "interactionBasis": basis,
            "info": info_payload,
            "analysis": analysis_payload,
            "billing": billing,
        }
        raw_path = os.path.join(out_dir, "wm_video_raw.json")
        try:
            with open(raw_path, "w", encoding="utf-8") as f:
                json.dump(raw, f, ensure_ascii=False, indent=2)
            files["raw"] = os.path.abspath(raw_path)
        except OSError as e:
            log("⚠️ 原始数据落地失败：%s" % e)

    do_md = fmt in ("markdown", "md", "all")
    do_xlsx = fmt in ("excel", "xlsx", "all")
    do_html = fmt in ("html", "dashboard", "all")

    # Markdown
    if do_md:
        report = render_report(info_payload, analysis_payload, billing, input_desc, is_local,
                                analysis=analysis)
        md_path = out_path if out_path and not os.path.isdir(out_path) and not out_path.endswith((".xlsx", ".html")) else os.path.join(out_dir, "wm_video_report.md")
        if md_path.endswith((".xlsx", ".html")):
            md_path = os.path.join(out_dir, "wm_video_report.md")
        try:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(report)
            files["markdown"] = os.path.abspath(md_path)
        except OSError as e:
            log("⚠️ Markdown 写入失败：%s" % e)

    # Excel
    if do_xlsx:
        xlsx_path = os.path.join(out_dir, "wm_video_report.xlsx")
        try:
            xlsx_path = render_xlsx(info_payload, analysis_payload, billing, input_desc,
                                    is_local, out_path=xlsx_path, analysis=analysis)
            files["xlsx"] = xlsx_path
            log("  Excel 报告已保存：%s" % xlsx_path)
        except Exception as e:
            log("⚠️ Excel 生成失败：%s" % e)

    # HTML 看板
    if do_html:
        html_path = os.path.join(out_dir, "wm_video_dashboard.html")
        try:
            html_path = render_html_dashboard(info_payload, analysis_payload, billing, input_desc,
                                              is_local, out_path=html_path, analysis=analysis)
            files["html"] = html_path
            log("  HTML 看板已保存：%s" % html_path)
        except Exception as e:
            log("⚠️ HTML 看板生成失败：%s" % e)

    # stdout 输出（始终输出 Markdown 报告内容 + 文件路径）
    report = render_report(info_payload, analysis_payload, billing, input_desc, is_local,
                           analysis=analysis)
    print("WM_VIDEO_TOTAL_CONSUMPTION=%.6f" % (total if dump_raw else 0.0))
    if not dump_raw:
        print("WM_VIDEO_HISTORICAL_CONSUMPTION=%.6f" % total)
    for fmt_key, fpath in files.items():
        print("WM_VIDEO_FILE_%s=%s" % (fmt_key.upper(), fpath))
    print(REPORT_START)
    print(report)
    print(REPORT_END)


SIX_DIMENSIONS = ["Hook强度", "信息密度", "节奏控制", "产品展示", "情绪曲线", "转化引导"]
ATTRIBUTION_LAYERS = ["内容因素", "传播因素", "表现因素", "账号因素"]


def _vstr(analysis, key, path, errors):
    """校验 analysis[path] 是非空字符串。"""
    val = analysis.get(key)
    if not isinstance(val, str) or not val.strip():
        errors.append("%s.%s 必须是非空字符串" % (path, key))


def validate_analysis(analysis, raw):
    """按 references/analysis-schema.md 强制校验分析层结构。

    返回错误列表（空列表 = 通过）。保证任何通过校验的分析文件
    渲染出的报告结构完全一致（相同板块/表格列/评分维度）。
    """
    errors = []
    basis = analysis.get("interactionBasis")
    if not isinstance(basis, dict) or basis.get("semanticsVersion") != SEMANTICS_VERSION:
        errors.append("缺少新版 interactionBasis：先用 --render 原始数据生成 wm_interaction_facts.json，"
                      "按更正后的点赞/推荐重新分析和评分；不要只替换旧分析的版本号")
    elif raw is not None and basis != interaction_basis(raw.get("info"), bool(raw.get("isLocal"))):
        errors.append("interactionBasis 与本次原始数据不一致，必须使用 wm_interaction_facts.json 的真实指标重新分析")

    # --- 顶层必填键 ---
    required_top = ["audience", "structure", "viralAttribution", "viralFormula",
                    "replicability", "sixDimScores", "operations", "overall"]
    for key in required_top:
        if key not in analysis:
            errors.append("缺少顶层字段 %s" % key)
    if analysis.get("schemaVersion") != "1.0":
        errors.append('schemaVersion 必须是 "1.0"')

    # --- audience：dict，子字段若存在必须是字符串 ---
    audience = analysis.get("audience")
    if audience is not None:
        if not isinstance(audience, dict):
            errors.append("audience 必须是对象")
        else:
            for sub in ("ageRange", "gender", "interests", "consumption"):
                if sub in audience and not isinstance(audience[sub], (str, list)):
                    errors.append("audience.%s 必须是字符串或数组" % sub)

    # --- structure ---
    structure = analysis.get("structure")
    seg_count = 0
    if raw:
        obs = ((raw.get("analysis") or {}).get("data") or {}).get("observation") or {}
        seg_count = len(obs.get("segments") or [])
    if structure is not None:
        if not isinstance(structure, dict):
            errors.append("structure 必须是对象")
        else:
            _vstr(structure, "scriptType", "structure", errors)
            _vstr(structure, "rationale", "structure", errors)
            _vstr(structure, "summary", "structure", errors)
            notes = structure.get("segmentNotes")
            if notes is not None:
                if not isinstance(notes, dict) or not notes:
                    errors.append("structure.segmentNotes 必须是非空对象")
                else:
                    for k, v in notes.items():
                        if not str(k).isdigit():
                            errors.append('structure.segmentNotes 的 key 必须是片段序号字符串，如 "1"，得到 %r' % k)
                        elif seg_count and int(k) > seg_count:
                            errors.append("structure.segmentNotes key %s 超出实际片段数 %d" % (k, seg_count))
                        if not isinstance(v, str) or not v.strip():
                            errors.append("structure.segmentNotes[%s] 必须是非空字符串" % k)

    # --- viralAttribution：2-4 条，字段齐全，layer 受限，contribution 合计≈100 ---
    va = analysis.get("viralAttribution")
    if va is not None:
        if not isinstance(va, list) or not (2 <= len(va) <= 4):
            errors.append("viralAttribution 必须是 2-4 条的数组")
        else:
            total = 0
            for i, item in enumerate(va, 1):
                if not isinstance(item, dict):
                    errors.append("viralAttribution[%d] 必须是对象" % i)
                    continue
                for key in ("layer", "factor", "detail", "evidence"):
                    v = item.get(key)
                    if not isinstance(v, str) or not v.strip():
                        errors.append("viralAttribution[%d].%s 必须是非空字符串" % (i, key))
                if item.get("layer") not in ATTRIBUTION_LAYERS:
                    errors.append("viralAttribution[%d].layer 必须是 %s 之一" % (i, "/".join(ATTRIBUTION_LAYERS)))
                c = item.get("contribution")
                if not isinstance(c, (int, float)) or isinstance(c, bool) or not (0 < c <= 100):
                    errors.append("viralAttribution[%d].contribution 必须是 1-100 的数值" % i)
                else:
                    total += c
                if "rank" in item and item["rank"] != i:
                    errors.append("viralAttribution[%d].rank 应等于序号 %d" % (i, i))
            if va and isinstance(va[0], dict) and abs(total - 100) > 5:
                errors.append("viralAttribution 的 contribution 合计应为 100（当前 %.1f）" % total)

    # --- viralFormula ---
    if "viralFormula" in analysis:
        _vstr(analysis, "viralFormula", "(顶层)", errors)

    # --- replicability ---
    rep = analysis.get("replicability")
    if rep is not None:
        if not isinstance(rep, dict):
            errors.append("replicability 必须是对象")
        else:
            s = rep.get("score")
            if not isinstance(s, int) or isinstance(s, bool) or not (1 <= s <= 5):
                errors.append("replicability.score 必须是 1-5 的整数")
            for key in ("note", "replicableStrategy", "notApplicableScenarios"):
                if key in rep:
                    v = rep[key]
                    if not isinstance(v, str) or not v.strip():
                        errors.append("replicability.%s 必须是非空字符串" % key)

    # --- sixDimScores：六个固定维度，顺序固定，score 0-10 ---
    six = analysis.get("sixDimScores")
    if six is not None:
        if not isinstance(six, list) or len(six) != 6:
            errors.append("sixDimScores 必须恰好包含 6 个维度：%s" % "、".join(SIX_DIMENSIONS))
        else:
            for i, item in enumerate(six):
                dim = SIX_DIMENSIONS[i]
                if not isinstance(item, dict):
                    errors.append("sixDimScores[%d] 必须是对象" % i)
                    continue
                if item.get("dimension") != dim:
                    errors.append('sixDimScores[%d].dimension 必须是 "%s"（顺序固定）' % (i, dim))
                s = item.get("score")
                if not isinstance(s, (int, float)) or isinstance(s, bool) or not (0 <= s <= 10):
                    errors.append("sixDimScores[%d].score 必须是 0-10 的数值" % i)
                for key in ("evidence", "reason", "suggestion"):
                    v = item.get(key)
                    if not isinstance(v, str) or not v.strip():
                        errors.append("sixDimScores[%d].%s 必须是非空字符串" % (i, key))

    # --- operations：3-5 条可执行动作 ---
    ops = analysis.get("operations")
    if ops is not None:
        if not isinstance(ops, list) or not (3 <= len(ops) <= 5):
            errors.append("operations 必须是 3-5 条的数组")
        else:
            for i, op in enumerate(ops, 1):
                if not isinstance(op, str) or not op.strip():
                    errors.append("operations[%d] 必须是非空字符串" % i)

    # --- overall ---
    overall = analysis.get("overall")
    if overall is not None:
        if not isinstance(overall, dict):
            errors.append("overall 必须是对象")
        else:
            t = overall.get("totalScore")
            if not isinstance(t, int) or isinstance(t, bool) or not (0 <= t <= 100):
                errors.append("overall.totalScore 必须是 0-100 的整数")
            r = overall.get("replicabilityStars")
            if not isinstance(r, int) or isinstance(r, bool) or not (1 <= r <= 5):
                errors.append("overall.replicabilityStars 必须是 1-5 的整数")
            hl = overall.get("highlights")
            if not isinstance(hl, list) or not (2 <= len(hl) <= 3):
                errors.append("overall.highlights 必须是 2-3 条的数组")
            else:
                for i, item in enumerate(hl, 1):
                    if not isinstance(item, dict):
                        errors.append("overall.highlights[%d] 必须是对象" % i)
                        continue
                    if item.get("type") not in ("亮点", "问题"):
                        errors.append('overall.highlights[%d].type 必须是 "亮点" 或 "问题"' % i)
                    v = item.get("text")
                    if not isinstance(v, str) or not v.strip():
                        errors.append("overall.highlights[%d].text 必须是非空字符串" % i)
            _vstr(overall, "primaryImprovement", "overall", errors)
        # 六维均值 ×10 与 totalScore 自洽性（±15 容差）
        if isinstance(six, list) and len(six) == 6 and isinstance(t, int):
            scores = [s.get("score") for s in six if isinstance(s, dict)
                      and isinstance(s.get("score"), (int, float))
                      and not isinstance(s.get("score"), bool)]
            if len(scores) == 6:
                expect = sum(scores) / 6.0 * 10
                if abs(expect - t) > 15:
                    errors.append("overall.totalScore=%d 与六维均值×10=%.0f 偏差超过 15，不自洽" % (t, expect))

    # --- interactionNotes：分析层对「互动结构反推」的补充解读（可选）---
    inotes = analysis.get("interactionNotes")
    if inotes is not None:
        if not isinstance(inotes, list) or not (2 <= len(inotes) <= 4):
            errors.append("interactionNotes 必须是 2-4 条的数组（不提供则只渲染脚本自动反推）")
        else:
            for i, n in enumerate(inotes, 1):
                if not isinstance(n, str) or not n.strip():
                    errors.append("interactionNotes[%d] 必须是非空字符串" % i)

    # --- tags ---
    tags = analysis.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or not (4 <= len(tags) <= 6):
            errors.append("tags 必须是 4-6 个的数组")
        else:
            for i, tag in enumerate(tags, 1):
                if not isinstance(tag, str) or not tag.strip():
                    errors.append("tags[%d] 必须是非空字符串" % i)

    return errors


def run_check_analysis(analysis_path, raw_path):
    """仅校验分析文件 schema（可选与 raw 交叉校验），零 API 调用。"""
    try:
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis = json.load(f)
    except (OSError, ValueError) as e:
        fail(2, "无法读取分析文件 %s：%s" % (analysis_path, e))
    if not isinstance(analysis, dict):
        fail(2, "分析文件 %s 顶层必须是 JSON 对象" % analysis_path)

    raw = None
    if raw_path:
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (OSError, ValueError) as e:
            fail(2, "无法读取原始数据文件 %s：%s" % (raw_path, e))

    log("[校验] 分析文件：%s" % analysis_path)
    if raw:
        log("[校验] 交叉校验原始数据：%s" % raw_path)
    errs = validate_analysis(analysis, raw)
    if errs:
        log("[校验] 未通过（%d 处）：" % len(errs))
        for e in errs:
            log("    - %s" % e)
        fail(8, "分析文件结构不合契约（契约见 references/analysis-schema.md）")
    log("[校验] 通过：结构完全符合 schema 契约")


def run_render(raw_path, analysis_path, fmt, out_path):
    """零 API 调用重渲染：读取 wm_video_raw.json（+ 可选 wm_analysis.json），
    重新生成 Markdown / Excel / HTML 报告。不产生任何扣费。"""
    try:
        with open(raw_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (OSError, ValueError) as e:
        fail(2, "无法读取原始数据文件 %s：%s" % (raw_path, e))

    info_payload = raw.get("info")
    analysis_payload = raw.get("analysis")
    billing = raw.get("billing") or []
    input_desc = raw.get("inputDesc") or "(未知输入)"
    is_local = bool(raw.get("isLocal"))

    analysis = None
    if analysis_path:
        try:
            with open(analysis_path, "r", encoding="utf-8") as f:
                analysis = json.load(f)
        except (OSError, ValueError) as e:
            fail(2, "无法读取分析文件 %s：%s" % (analysis_path, e))
        if not isinstance(analysis, dict):
            fail(2, "分析文件 %s 顶层必须是 JSON 对象" % analysis_path)
        # 强制 schema 校验：结构不合规直接拒绝渲染，保证报告结构稳定
        errs = validate_analysis(analysis, raw)
        if errs:
            log("[校验] 分析文件未通过 schema 校验（%d 处）：" % len(errs))
            for e in errs:
                log("    - %s" % e)
            fail(8, "分析文件结构不合契约，详见上方错误清单；修正后重试（契约见 references/analysis-schema.md）")

    log("[渲染] 使用原始数据：%s" % raw_path)
    if analysis:
        log("[渲染] 注入 AI 分析层：%s" % analysis_path)
    else:
        log("[渲染] 未提供分析文件，输出基础数据报告")

    _output_results(info_payload, analysis_payload, billing, input_desc,
                    is_local=is_local, out_path=out_path, fmt=fmt,
                    analysis=analysis, dump_raw=False)
    log("[渲染] 完成（零 API 调用、零扣费）")


def run_balance(api_key):
    """仅查询余额。"""
    log("[进度] 正在查询账户余额…")
    balance = get_balance(api_key)
    print("账户可用余额：%.6f 元" % balance)
    log("余额查询完成")


def main():
    parser = argparse.ArgumentParser(
        description="视频号视频拆解（曼格云 API 版）",
        usage="python3 analyze_wx_video.py \"<分享链接|本地路径>\" [--no-visual] [--mode decompose] "
              "[--format all] [--estimate] [--out 路径]  |  "
              "--render wm_video_raw.json [--analysis wm_analysis.json]  |  --balance",
    )
    parser.add_argument("input", nargs="?", help="视频号分享链接或本地视频文件路径")
    parser.add_argument("--mode", default="decompose",
                        choices=["summary", "timeline", "decompose"],
                        help="视觉理解档位（默认 decompose 最详细；summary ¥0.12 / timeline ¥0.18 / decompose ¥0.24）")
    parser.add_argument("--no-visual", action="store_true", dest="no_visual",
                        help="关闭视觉理解：只取作品资料（文案/发布时间/时长/互动），不下载视频、不做画面拆解")
    parser.add_argument("--estimate", action="store_true",
                        help="只查询免费产品目录并输出费用预估，不调用付费接口（可在无 API Key 时使用）")
    parser.add_argument("--yes", action="store_true", help="用户已授权当前采集费用；开启视觉分析时同时授权临时上传视频")
    parser.add_argument("--format", default="all", dest="fmt",
                        choices=["markdown", "md", "excel", "xlsx", "html", "dashboard", "all"],
                        help="输出格式：markdown/excel/html/all（默认 all 同时生成三种）")
    parser.add_argument("--out", default=None, help="报告输出路径（目录或文件均可）")
    parser.add_argument("--balance", action="store_true", help="仅查询账户余额，不拆解")
    parser.add_argument("--render", default=None, metavar="RAW_JSON",
                        help="零扣费重渲染模式：读取 wm_video_raw.json 重新生成报告，不调用任何 API")
    parser.add_argument("--analysis", default=None, metavar="ANALYSIS_JSON",
                        help="配合 --render / --check-analysis：AI 分析层（wm_analysis.json，schema 见 references/analysis-schema.md）")
    parser.add_argument("--check-analysis", default=None, dest="check_analysis", metavar="ANALYSIS_JSON",
                        help="仅校验分析文件是否符合 schema 契约（配合 --render 指定 raw 做交叉校验），不生成报告")
    args = parser.parse_args()
    visual = not args.no_visual

    # 费用预估模式（零 API 调用，无需 key）
    if args.estimate:
        if not args.input:
            fail(2, "缺少输入：请提供视频号分享链接或本地视频文件路径\n用法：%s" % parser.usage)
        run_estimate(args.input.strip(), args.mode, visual)
        return

    # 余额模式
    if args.balance:
        api_key = get_api_key()
        if not api_key:
            fail(3, "缺少 API Key，请在 config.json 中配置 WM_API_KEY 或设置环境变量")
        try:
            run_balance(api_key)
        except SkillError as e:
            fail(e.exit_code, e.message)
        return

    # 分析文件校验模式（零 API 调用、零扣费）
    if args.check_analysis:
        run_check_analysis(args.check_analysis, args.render)
        return

    # 重渲染模式（零 API 调用、零扣费）
    if args.render:
        run_render(args.render, args.analysis, args.fmt, args.out)
        return

    # 拆解模式
    if not args.input:
        fail(2, "缺少输入：请提供视频号分享链接或本地视频文件路径\n用法：%s" % parser.usage)

    api_key = get_api_key()
    if not api_key:
        fail(3, "缺少 API Key。请前往 https://api.we-media.cn 注册并创建 API Key，"
                "把拿到的 Key 写入技能目录下 config.json 的 WM_API_KEY 字段，或设置环境变量 WM_API_KEY。"
                "未拿到 Key 前不会调用任何接口，也不产生费用。")

    text = args.input.strip()
    items, est_total = estimate_cost(text, args.mode, visual)
    log("[费用预估] %s ｜ 合计约 ¥%.2f（实际以接口响应 consumption 为准；默认获取新数据，修改报告请使用 --render）"
        % (" + ".join("%s ¥%.2f" % (n, p) for n, p in items), est_total))
    if not args.yes:
        fail(2, "尚未执行采集或上传。用户授权本次范围、费用及视觉分析所需临时视频上传后，使用 --yes 执行；已有授权无需重复询问。")

    try:
        if is_share_url(text):
            log("[进度] 识别为视频号分享链接，开始拆解…")
            run_share_link(api_key, text, args.mode, args.out, args.fmt, visual=visual)
        elif is_local_video(text):
            log("[进度] 识别为本地视频文件，开始拆解…")
            run_local_video(api_key, text, args.mode, args.out, args.fmt, visual=visual)
        else:
            # 更详细的错误
            if os.path.exists(text):
                ext = os.path.splitext(text)[1].lower()
                if ext and ext not in SUPPORTED_EXTS:
                    fail(2, "不支持的视频格式 %s，支持：%s" % (ext, ", ".join(sorted(SUPPORTED_EXTS))))
                size = os.path.getsize(text)
                if size >= MAX_VIDEO_BYTES:
                    fail(2, "文件超过 128MB（%s），请压缩后重试" % _fmt_bytes(size))
            fail(2, "无法识别输入：%s\n请提供视频号分享链接（https://weixin.qq.com/sph/...）或本地视频文件路径" % text)
    except SkillError as e:
        fail(e.exit_code, e.message)
    except KeyboardInterrupt:
        fail(124, "用户中断")
    except Exception as e:
        log("未预期的错误：%s" % e)
        import traceback
        traceback.print_exc(file=sys.stderr)
        fail(6, "执行过程中发生未预期错误：%s" % e)


if __name__ == "__main__":
    main()
