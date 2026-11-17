#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OwlWrite 接口层（2026-11-09，v1.3.0）。

CLI（`owl.py`）的唯一接口层，只用标准库（urllib），零第三方依赖——这是「不配 MCP 也能用」的地基。
MCP 服务器（mcp_server.py）是独立实现（异步 httpx，远程常驻场景不能引入同步阻塞）；
两条路径的能力对齐由发布仓的 parity 测试守护（owlwrite-paper 仓库 `_tools/test_cli_parity.py`，
不在技能分发包内）。

约定：
  · 所有函数返回 dict（服务端 JSON 原样，字段名与服务端一致）；
  · 出错抛 ApiError（带 code / message / http_status），调用方按 code 分支，不吞错；
  · 活动公告（owl_notice）统一补 `_notice_tip`，两条路径都会转告用户；
  · 版本头 X-Owl-Skill-Version 必须随每个请求带上（网关据此判旧版）。

凭据解析顺序：环境变量 OWL_API_KEY > ~/.owl_creds.json 的 owl_api_key（OWL_CREDS 可指定文件）。
安全边界：默认只向官方网关发凭据；非官方 base 需显式 OWL_ALLOW_CUSTOM_BASE=1；
拒绝跟随 HTTP 重定向（防 302 把 Authorization 带去别的域）。
"""
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile

# 版本同源：SKILL.md / README / scripts/mcp_server.py / connector-meta.json / owl_api.py
OWL_SKILL_VERSION = "1.3.2"

DEFAULT_BASE = "https://owl.skillsutra.cn"
OFFICIAL_HOSTS = {"owl.skillsutra.cn"}
LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
CREDS_PATHS = (
    os.path.expanduser("~/.owl_creds.json"),
    os.path.expanduser("~/.workbuddy/owl_creds.json"),
)
NOTICE_SEEN_PATH = os.path.expanduser("~/.owl_notice_seen.json")

# run_id / order_no 是服务端下发的标识，只允许安全字符，杜绝路径注入
_ID_RE = re.compile(r"^[A-Za-z0-9_\-]{1,80}$")
# signed_query 是服务端生成的查询串，只放行安全字符（防开放重定向/参数注入）
_SQ_RE = re.compile(r"^[A-Za-z0-9=&%_.\-]*$")

class ApiError(Exception):
    """服务端结构化错误（code/message/http_status + 附加字段）。"""

    def __init__(self, code, message, http_status=0, extra=None):
        self.code = code
        self.message = message
        self.http_status = http_status
        self.extra = extra or {}
        super().__init__(f"{code}: {message}")

    def as_dict(self):
        d = {"error": self.code, "message": self.message, "http_status": self.http_status}
        d.update(self.extra)
        return d


# ---------------- 配置与凭据 ----------------

def load_key(explicit=None):
    """凭据解析：显式 > 环境变量 > 凭据文件。找不到抛 ApiError(no_api_key)。

    OWL_CREDS 可指定凭据文件路径（测试 / 多账号隔离用，默认 ~/.owl_creds.json）。
    """
    if explicit and str(explicit).strip():
        return str(explicit).strip()
    k = os.environ.get("OWL_API_KEY", "").strip()
    if k:
        return k
    for p in creds_paths():
        if os.path.exists(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                k = (d.get("owl_api_key") or d.get("api_key") or "").strip()
                if k:
                    return k
            except Exception:  # noqa: BLE001
                pass
    raise ApiError("no_api_key",
                   "还没有配置 API key：运行 python scripts/owl.py init 粘贴一次即可"
                   "（或设环境变量 OWL_API_KEY）；没有账号请到 paper.skillsutra.cn 注册")


def creds_paths():
    """凭据文件候选。OWL_CREDS 一旦设置即**独占**——避免测试/多账号场景误读到真实凭据。"""
    env = os.environ.get("OWL_CREDS", "").strip()
    return (env,) if env else CREDS_PATHS


def save_key(key, path=None):
    """把 key 写入凭据文件，返回写入路径。

    安全：创建瞬间即 0600（os.open 权限位）；写前把旧文件备份为 .bak；
    chmod 失败会在 stderr 明确告警（绝不静默）。
    """
    p = os.path.abspath(path or creds_paths()[0])
    d = os.path.dirname(p)
    os.makedirs(d, exist_ok=True)
    try:
        os.chmod(d, 0o700)
    except Exception:  # noqa: BLE001 — Windows/特殊文件系统上无效，忽略
        pass
    # 备份旧文件（包括旧 key，防覆盖丢失）
    if os.path.exists(p):
        try:
            with open(p, "rb") as src:
                raw = src.read()
            fd = os.open(p + ".bak", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "wb") as dst:
                dst.write(raw)
        except Exception:  # noqa: BLE001
            print("# 警告：旧凭据备份失败，继续写入", file=sys.stderr)
    # 保留旧文件里的其他字段（多账号备注等），只更新 owl_api_key
    d = {}
    try:
        with open(p, encoding="utf-8") as f:
            d = json.load(f) or {}
    except Exception:  # noqa: BLE001 — 文件损坏/不存在都当作空
        d = {}
    if not isinstance(d, dict):
        d = {}
    d["owl_api_key"] = key.strip()
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    try:
        os.chmod(p, 0o600)          # Windows 上是 no-op，Linux/macOS 生效
    except Exception:  # noqa: BLE001
        print("# 警告：当前平台无法收紧凭据文件权限，请勿在多人共用的电脑上保存 key",
              file=sys.stderr)
    return p


def resolve_base(base=None):
    """解析并校验网关地址。只允许 https（本地 127.0.0.1/localhost 可 http），
    禁止 userinfo/query/fragment——防 --base/OWL_BASE 被诱导指向伪装主机。"""
    raw = (base or os.environ.get("OWL_BASE") or DEFAULT_BASE).strip().rstrip("/")
    u = urllib.parse.urlsplit(raw)
    host = (u.hostname or "").lower()
    if not host:
        raise ApiError("bad_base", f"网关地址无效：{raw or '(空)'}")
    if u.username or u.password:
        raise ApiError("bad_base", "网关地址不应包含用户名/密码（形如 https://user@host）")
    if u.query or u.fragment:
        raise ApiError("bad_base", "网关地址不应包含 ?query 或 #fragment")
    if u.scheme != "https" and host not in LOCAL_HOSTS:
        raise ApiError("insecure_base",
                       f"网关地址必须是 https://（{host} 不是本机地址，明文 http 会被窃听）；"
                       f"官方网关是 {DEFAULT_BASE}")
    return raw


def public_base(base=None):
    """对外可访问基址。远程 MCP 由 OWL_PUBLIC_BASE 注入公网域名；否则同 base。"""
    return (os.environ.get("OWL_PUBLIC_BASE") or resolve_base(base)).rstrip("/")


def _asset_url(root, path_or_url):
    """把服务端返回的资源路径拼成完整 URL；拒绝跨主机/非 https 的绝对地址（防钓鱼下载链接）。"""
    u = urllib.parse.urljoin((root or "").rstrip("/") + "/", str(path_or_url or ""))
    sp = urllib.parse.urlsplit(u)
    rp = urllib.parse.urlsplit(root or DEFAULT_BASE)
    if sp.scheme and sp.scheme != "https":
        raise ApiError("bad_response", "服务端返回了非 https 的下载地址，已拒绝")
    if sp.netloc and sp.netloc != rp.netloc:
        raise ApiError("bad_response", "服务端返回了指向其他域名的下载地址，已拒绝")
    return u


# ---------------- 公告透传 ----------------

def notices_tip(data):
    """把响应顶层 owl_notice 转成给 Agent 的硬提示（未看过的才提示，写不了文件也照提）。"""
    try:
        if not isinstance(data, dict):
            return data
        items = data.get("owl_notice")
        if not items:
            return data
        seen = set()
        try:
            with open(NOTICE_SEEN_PATH, encoding="utf-8") as f:
                seen = set(json.load(f) or [])
        except Exception:  # noqa: BLE001
            seen = set()
        fresh = [n for n in items if isinstance(n, dict) and n.get("id") and n["id"] not in seen]
        if not fresh:
            return data
        texts = "；".join(str(n.get("text") or "").strip() for n in fresh)
        data["_notice_tip"] = (
            "【请转告用户】" + texts +
            "。把这件事用一两句话顺口告诉用户即可，不要打断正在进行的任务，也不要替他做选择。")
        try:
            with open(NOTICE_SEEN_PATH, "w", encoding="utf-8") as f:
                json.dump(sorted(seen | {n["id"] for n in fresh}), f)
        except Exception:  # noqa: BLE001
            pass
    except Exception:  # noqa: BLE001 — 公告透传绝不影响主流程
        pass
    return data


# ---------------- 底层请求 ----------------

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """拒绝跟随任何 HTTP 重定向：标准库会把 Authorization 原样转发到 Location 主机。"""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ApiError("unexpected_redirect",
                       f"服务端返回 {code} 跳转，已拒绝跟随（防止凭据外泄）。"
                       "请直接访问官方网关 " + DEFAULT_BASE)


_OPENER = urllib.request.build_opener(_NoRedirect)


def request(method, path, body=None, params=None, key=None, base=None, timeout=120,
            raw_body=None, extra_headers=None, auth=True):
    """发一个请求并返回 dict。raw_body 用于上传（bytes）；auth=False 用于匿名接口。"""
    base_url = resolve_base(base)
    url = base_url + path
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    headers = {
        "Accept": "application/json",
        "X-Owl-Skill-Version": OWL_SKILL_VERSION,
    }
    if host not in OFFICIAL_HOSTS and host not in LOCAL_HOSTS:
        # 非官方主机一律告警（含匿名接口——伪造的价格/公告同样能骗人），凭据类请求再拦
        print(f"# 警告：请求将发送到非官方网关 {host}", file=sys.stderr)
    if auth:
        # 凭据只发给官方网关（本机调试地址放行）；非官方主机必须显式 OWL_ALLOW_CUSTOM_BASE=1
        if host not in OFFICIAL_HOSTS and host not in LOCAL_HOSTS:
            allow = os.environ.get("OWL_ALLOW_CUSTOM_BASE", "").strip().lower()
            if allow not in ("1", "true", "yes"):
                raise ApiError("untrusted_base",
                               f"拒绝把 API key 发送到非官方网关 {host}。官方网关是 "
                               f"{DEFAULT_BASE}；确属自建网关时，设环境变量 OWL_ALLOW_CUSTOM_BASE=1 后重试")
            print(f"# 警告：API key 将发送到非官方网关 {host}", file=sys.stderr)
        headers["Authorization"] = "Bearer " + load_key(key)
    data = raw_body
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with _OPENER.open(req, timeout=timeout) as r:
            payload = r.read().decode("utf-8", "replace")
            status = r.status
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", "replace")
        status = e.code
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), TimeoutError):
            raise ApiError("timeout", "请求超时。长任务请用 run 拿 run_id 后分块轮询，不要一次等到底")
        raise ApiError("network_error",
                       f"连不上服务端（{_safe_base_display(base_url)}）：{getattr(e, 'reason', e)}。"
                       "检查网络后重试；若本机开了代理/VPN，可先关掉再试",
                       http_status=0)
    except TimeoutError:
        raise ApiError("timeout", "请求超时。长任务请用 run 拿 run_id 后分块轮询，不要一次等到底")
    try:
        out = json.loads(payload or "{}")
    except Exception:  # noqa: BLE001
        out = {"raw": (payload or "")[:500]}
    if status >= 400:
        err = out.get("detail") if isinstance(out, dict) and isinstance(out.get("detail"), dict) else out
        err = err if isinstance(err, dict) else {}
        code = str(err.get("code") or "").strip()
        msg = str(err.get("message") or "").strip()
        if not (code or msg):  # 非结构化错误体（HTML 维护页/代理错误页等）——不外泄内部细节
            raise ApiError(f"http_{status}",
                           f"服务暂时不可用（HTTP {status}），请稍后重试；若持续出现请把当前操作反馈给客服",
                           status, {})
        extra = {k: v for k, v in err.items() if k not in ("code", "message", "detail")}
        code = code or f"http_{status}"
        if code == "unauthorized" or (status == 401 and code in ("http_401",)):
            # 401 ≠ key 无效：先区分「没带凭据」与「key 无效」，别让用户白改 key（验收报告 P0-2）
            extra["tip"] = ("401 有两种：code=unauthorized 表示请求没带凭据（多为旧版脚本或匿名接口误用，"
                            "重跑 owl.py doctor 排查），code=invalid_key 才是 key 无效。"
                            "先看 code 再决定是否让用户重签 key。")
        raise ApiError(code, msg or f"服务返回错误（HTTP {status}）",
                       status, extra)
    if not isinstance(out, dict):  # 200 但响应不是 JSON 对象（维护页/异常网关）
        raise ApiError("bad_response",
                       "服务返回了无法解析的结果，请稍后重试；若持续出现请反馈",
                       status, {"raw": (payload or "")[:200]})
    return notices_tip(out)


def _safe_base_display(base_url):
    """错误信息里只显示 scheme://host，不带 userinfo/query。"""
    u = urllib.parse.urlsplit(base_url or "")
    return f"{u.scheme or 'https'}://{u.netloc.split('@')[-1] or u.hostname or ''}"


# ---------------- 21 个操作（与 MCP 工具一一对应） ----------------

def search(query, limit=5, lang="all", expand=False, key=None, base=None):
    body = {"query": query, "limit": limit, "lang": lang}
    if expand:
        body["expand"] = True
    return request("POST", "/v1/search", body, key=key, base=base)


def _sid(value, what="标识"):
    """校验服务端下发的 run_id / order_no（只允许字母数字下划线连字符，防路径注入）。"""
    s = str(value or "").strip()
    if not _ID_RE.match(s):
        raise ApiError("bad_params",
                       f"{what}格式不对（应为服务端返回的原样标识，不含空格/斜杠/问号）：{s[:60]}")
    return s


def products(key=None, base=None):
    return request("GET", "/v1/prices", key=key, base=base, auth=False)


def meta(key=None, base=None):
    return request("GET", "/v1/meta", key=key, base=base, auth=False)


def disciplines(key=None, base=None):
    # 服务端要求鉴权（无 Bearer 恒 401）——务必带 key（TeleAgent 验收报告 P0-1，2026-11-10）
    return request("GET", "/v1/disciplines", key=key, base=base)


def quote(action, params, key=None, base=None):
    return request("POST", "/v1/quote", {"action": action, "params": params},
                   key=key, base=base)


def docx_hanzi(path):
    """数 .docx 正文汉字数（口径与网关一致：800 汉字 ≈ 1 页）。读不出返回 0。"""
    try:
        with zipfile.ZipFile(path) as z:
            info = z.getinfo("word/document.xml")
            if info.file_size > 64 * 1024 * 1024:  # 防 zip 炸弹拖垮本地进程
                return 0
            xml = z.read("word/document.xml").decode("utf-8", "ignore")
        return len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"<[^>]+>", "", xml)))
    except Exception:  # noqa: BLE001
        return 0


def upload(file_path, max_mb=60, key=None, base=None):
    """上传本机文件，返回 file_id。.zip 上限 60MB，其它 30MB。"""
    p = os.path.expanduser(str(file_path or "").strip().strip('"').strip("'"))
    if not os.path.isfile(p):
        raise ApiError("file_not_found", f"本机找不到这个文件：{p}")
    size = os.path.getsize(p)
    limit = max_mb if p.lower().endswith(".zip") else 30
    if size > limit * 1024 * 1024:
        raise ApiError("file_too_large",
                       f"文件 {size / 1024 / 1024:.1f}MB 超过 {limit}MB 上限；"
                       f"请删掉工程里的 PDF 成品与 build 目录后重新打包")
    with open(p, "rb") as f:
        raw = f.read()
    return request("POST", "/v1/files", raw_body=raw, key=key, base=base, timeout=300,
                   extra_headers={
                       "X-Filename": urllib.parse.quote(os.path.basename(p)),
                       "Content-Type": "application/octet-stream",
                   })


def run(quote_id, key=None, base=None):
    return request("POST", "/v1/runs", {"quote_id": quote_id}, key=key, base=base)


def run_status(run_id, key=None, base=None, timeout=120):
    return request("GET", f"/v1/runs/{_sid(run_id, 'run_id')}", key=key, base=base,
                   timeout=timeout)


def run_content(run_id, key=None, base=None):
    return request("GET", f"/v1/runs/{_sid(run_id, 'run_id')}/content", key=key, base=base)


def run_report(run_id, part="", key=None, base=None):
    """任务报告：核验给逐条摘要；检测给结论 + 4 份报告链接。"""
    data = run_status(run_id, key=key, base=base)
    run_id = _sid(run_id, "run_id")
    status, action = data.get("status"), data.get("action")
    result = data.get("result") or {}
    sq = data.get("signed_query") or ""
    if not _SQ_RE.match(sq):  # 服务端签名串异常时丢弃，只退化为无签名链接
        sq = ""
    base_url = f"{public_base(base)}/v1/runs/{run_id}/report" + (f"?{sq}" if sq else "")

    if action == "check":
        rep = result.get("report") or {}
        files = rep.get("files") or []
        parts = {f.get("kind"): f.get("file") for f in files
                 if f.get("kind") and not str(f.get("kind")).startswith("other")}
        if not parts:
            parts = {"main": "", "compare": "", "simple": "", "fulltext": ""}
        pick = (part or "main").strip().lower()
        if pick not in parts:
            return {"run_id": run_id, "status": status, "error": "unknown_part",
                    "available_parts": sorted(parts)}
        sep = "&" if sq else "?"
        url_of = lambda k: base_url if k == "main" else f"{base_url}{sep}part={k}"
        return {
            "run_id": run_id, "status": status, "action": "check",
            "headline": result.get("headline"),
            "result_mode": result.get("result_mode"),
            "repeat_rate": result.get("repeat_rate"),
            "grade": result.get("grade"),
            "error_count": result.get("error_count"),
            "word_count": result.get("word_count"),
            "num": result.get("num"),
            "report_status": rep.get("status") or "unknown",
            "report_url": url_of(pick),
            "available_parts": {k: url_of(k) for k in sorted(parts)},
            "report_tip": "检测类共 4 份：综合(HTML)/比对(HTML)/简洁(PDF)/原文对照(PDF)",
        }

    items = result.get("items") or []
    summary = result.get("summary") or {}
    if not items:
        return {"run_id": run_id, "status": data.get("status"),
                "note": "任务尚无核验结果（未完成或非 verify 任务）",
                "report_url": base_url}
    s = summary
    head = (f"共 {s.get('total')} 条：已证实 {s.get('verified')}，元数据不符 "
            f"{s.get('metadata_mismatch')}，疑似匹配 {s.get('likely')}，存疑 "
            f"{s.get('suspect')}，未找到 {s.get('not_found')}，失败 {s.get('error')}")
    lines = [head]
    for i in items:
        diffs = "；".join(
            f"{d['field']}：引用「{d['cited']}」→ 实际「{d['actual']}」"
            for d in (i.get("diffs") or []))
        note = f"  ← {i['note']}" if i.get("note") else ""
        diff_txt = f"  ← 可修正：{diffs}" if diffs else ""
        lines.append(f"[{i['idx']}] {i['verdict']}  {str(i['title'])[:48]}{diff_txt}{note}")
    return {"run_id": run_id, "summary": summary, "digest": lines,
            "report_url": f"{public_base(base)}/v1/runs/{run_id}/report"
                          + (f"?{sq}" if sq else ""),
            "report_tip": "report_url 自带 24 小时签名，浏览器可直接打开（带判定徽标的完整 HTML）"}


def wait(run_id, timeout=120, interval=4, key=None, base=None):
    """分块轮询：最多等 timeout 秒就返回当前状态（不阻塞到底），调用方可续调。"""
    deadline = time.time() + max(5, int(timeout))
    last = {}
    while True:
        remaining = max(5, int(deadline - time.time()))
        try:
            # 单次请求超时取「剩余时间」与 30s 的较小值：--timeout 是真硬上限
            last = run_status(run_id, key=key, base=base, timeout=min(30, remaining))
        except ApiError:
            raise
        if last.get("status") in ("succeeded", "failed", "cancelled"):
            return last
        if time.time() >= deadline:
            last["_wait_tip"] = (f"本轮已等 {int(timeout)} 秒仍未结束；"
                                 "再调一次 wait/status 继续等即可，任务在服务端继续跑，不要重建单")
            return last
        time.sleep(min(interval, max(0.01, deadline - time.time())))


def figure(mode, description, count=1, data="", file_id="", figure_type="",
           timeout=180, key=None, base=None):
    """科研配图。内部先报价再执行；最多轮询 timeout 秒，未完成返回 running 状态。"""
    params = {"mode": mode, "description": description, "count": count}
    if data:
        params["data"] = data
    if file_id:
        params["file_id"] = file_id
    if figure_type:
        params["figure_type"] = figure_type
    q = quote("figure", params, key=key, base=base)
    if not (isinstance(q, dict) and q.get("quote_id")):
        return q
    r = run(q["quote_id"], key=key, base=base)
    rid = (r or {}).get("run_id")
    if not rid:
        return r
    final = wait(rid, timeout=timeout, interval=3, key=key, base=base)
    if final.get("status") not in ("succeeded", "failed", "cancelled"):
        return {"run_id": rid, "status": "running",
                "message": "仍未完成，用 status/wait 继续查；积分按实际交付张数结算"}
    res = final.get("result") or {}
    sq = final.get("signed_query") or ""
    if not _SQ_RE.match(sq):
        sq = ""
    for f in res.get("figures") or []:
        f["download_url"] = _asset_url(public_base(base), f.get("url")) + (f"?{sq}" if sq else "")
        f["hint"] = "链接自带 24 小时签名，可直接下载（也可带 Authorization 头）；存 04-图/"
    return {"run_id": rid, "status": final.get("status"),
            "points_charged": final.get("points_settled"),
            "figures": res.get("figures") or [],
            "tikz_code": res.get("tikz_code") or "",
            "warnings": res.get("warnings") or [],
            "error": final.get("error_msg")}


def typeset(file_path="", mode="latex", template_path="", entry="", pages=0, hanzi=0,
            title="", file_id="", template_file_id="", author="", student_id="",
            college="", major="", advisor="", date="", blind=False, refs_std="2015",
            key=None, base=None):
    """按学校模板排版。可用性守卫 → 上传 → 报价 → 执行（超时放宽 330s）。"""
    mode = (mode or "latex").strip().lower()
    if mode not in ("latex", "docx"):
        raise ApiError("bad_params", "mode 只能是 latex 或 docx")

    # 可用性守卫必须在上传之前：先传 60MB 工程包再被拒，等于让用户白等一场
    ch = {}
    try:
        ch = (meta(key=key, base=base) or {}).get("channels") or {}
    except ApiError:
        pass  # meta 拉不到不阻塞主流程，交给服务端执行时最终判定
    if ch and ch.get("typeset_ready") is not True:
        raise ApiError("typeset_disabled",
                       ch.get("typeset_detail") or "排版功能暂未对外开放",
                       extra={"tip": "如实告诉用户当前不可用即可；不要报价、不要让用户打包或上传。"})
    if mode == "docx" and ch.get("typeset_docx_ready") is False:
        raise ApiError("typeset_docx_disabled",
                       "Word 按模板排版这条通路暂未开放，目前只支持 LaTeX 工程包")

    if not file_id:
        if not file_path:
            raise ApiError("bad_params", "请给 file_path（本机文件）或 file_id（已上传）")
        file_id = upload(file_path, key=key, base=base)["file_id"]
        if mode == "docx" and not hanzi:
            hanzi = docx_hanzi(file_path)
    if mode == "docx" and not template_file_id:
        if not template_path:
            raise ApiError("bad_params",
                           "Word 模式需要学校模板：请给 template_path，或先 upload 模板拿 template_file_id")
        template_file_id = upload(template_path, key=key, base=base)["file_id"]

    qparams = {"mode": mode}
    if pages:
        qparams["pages"] = int(pages)
    if hanzi:
        qparams["hanzi"] = int(hanzi)
    try:
        q = quote("typeset", qparams, key=key, base=base)
    except ApiError as exc:
        # 保留服务端原始错误码（不洗白），只附加可操作的 tip
        raise ApiError(exc.code, exc.message[:300], exc.http_status,
                       {"tip": "latex 模式必须带 pages（正文页数）；docx 模式请确认文件是 .docx 且没加密。"})

    body = {"file_id": file_id, "mode": mode, "quote_id": (q or {}).get("quote_id", "")}
    if pages:
        body["pages"] = int(pages)
    if hanzi:
        body["hanzi"] = int(hanzi)
    if template_file_id:
        body["template_file_id"] = template_file_id
    if entry:
        body["entry"] = entry
    if title:
        body["title"] = title
    for k, v in (("author", author), ("student_id", student_id), ("college", college),
                 ("major", major), ("advisor", advisor), ("date", date)):
        if v:
            body[k] = v
    if mode == "docx":
        if blind:
            body["blind"] = True
        if refs_std and refs_std != "2015":
            body["refs_std"] = refs_std

    try:
        r = request("POST", "/v1/typeset", body, key=key, base=base, timeout=330)
    except ApiError as exc:
        if exc.code in ("timeout", "network_error"):
            return {"error": "timeout",
                    "message": "这次排版没有在预期时间内完成，可能是一次性的引擎卡住（不代表你的稿有问题）。"
                               "扣费状态未知：重试前先用 wallet 查余额核对，避免重复扣费。",
                    "detail": str(exc)[:200]}
        raise

    out = dict(r or {})
    for k, src in (("pdf_url", "pdf_path"), ("docx_url", "docx_path")):
        p = out.pop(src, None)
        out[k] = _asset_url(public_base(base), p) if p else None
    out["est_points"] = (q or {}).get("est_points")
    out["points_charged"] = r.get("points_charged")
    out["checklist_tip"] = ("逐项「期望 vs 实测」讲给用户；⚠ 项说清是哪一项不一致、要不要改。"
                            "状态为「—」的是本稿测不了的项，不要念成不合格。"
                            "只讲返回里出现的项，没有的项不要编。")
    gaps = out.get("content_gaps") or []
    out["content_gaps_tip"] = ("这条非空就必须原样转告用户（公式/脚注/图/表列数没搬过去），"
                               "不要说成「已全部排好」。用户据此决定要不要先补稿。"
                               if gaps else None)
    if out.get("font_notice"):
        out["font_notice_tip"] = ("这条必须原样转告用户：PDF 与 Word 用的不是同一套字体。"
                                  "用 font_notice.text（长版）或 .short（短版）的原文讲，"
                                  "不要改写口径，也不要说「PDF 里就是宋体」。")
    if out.get("blind"):
        out["blind_tip"] = ("本次是盲审版：封面作者/学号/导师已脱敏为 ***、致谢整节已隐藏。"
                            "交付时必须说清这两点，并提醒用户：正式提交版要关掉 blind 重排一次"
                            "（72 小时内同一篇稿只收 1 积分工本）。")
    out["files_tip"] = ("pdf_url / docx_url 自带 7 天签名，可直接下载；"
                        "建议存到用户论文目录 07-交付/ 下，文件名用「题目-排版-v1.pdf」")
    return out


def wallet(key=None, base=None):
    return request("GET", "/v1/me/wallet", key=key, base=base)


def ledger(limit=50, offset=0, key=None, base=None):
    """逐笔积分流水（充值/消耗/赠送/退款/过期/佣金），含每笔后的余额轨迹。

    用户问「钱怎么少/多了一笔」时用它对账，不要靠余额差倒推。
    """
    return request("GET", "/v1/me/ledger",
                   params={"limit": max(1, min(int(limit or 50), 500)),
                           "offset": max(0, int(offset or 0))},
                   key=key, base=base)


def recharge(amount_cny, channel="wechat", key=None, base=None):
    if amount_cny not in (10, 30, 50, 100, 500):
        raise ApiError("bad_amount", "充值档位仅支持 10/30/50/100/500 元")
    r = request("POST", "/v1/pay/recharge",
                {"points": amount_cny * 100, "channel": channel}, key=key, base=base)
    if isinstance(r, dict) and r.get("qr_path"):
        r["qr_url"] = _asset_url(public_base(base), r.pop("qr_path"))
        r["notice"] = ("请把 qr_url 发给用户在浏览器打开并扫码支付；到账约 1 分钟，"
                       "支付后可用 recharge-status 或 wallet 确认。"
                       "不要重复调用——重复创建会产生多笔未支付订单。")
    return r


def recharge_status(order_no, key=None, base=None):
    return request("GET", f"/v1/pay/recharge/{_sid(order_no, '充值单号')}",
                   params={"refresh": "1"}, key=key, base=base)


def fulltext(identifier, key=None, base=None):
    return request("POST", "/v1/fulltext", {"identifier": identifier}, key=key, base=base)


def article(identifier, lang="zh", key=None, base=None):
    return request("GET", "/v1/article", params={"identifier": identifier, "lang": lang},
                   key=key, base=base)


def oa(doi="", title="", key=None, base=None):
    body = {}
    if doi and doi.strip():
        body["doi"] = doi.strip()
    if title and title.strip():
        body["title"] = title.strip()
    if not body:
        raise ApiError("bad_params", "doi 或 title 至少给一个")
    return request("POST", "/v1/oa", body, key=key, base=base)


def citations(doi, direction="refs", limit=20, key=None, base=None):
    return request("GET", "/v1/citations",
                   params={"doi": doi, "direction": direction, "limit": limit},
                   key=key, base=base)


def campaign(code="", key=None, base=None):
    if code and code.strip():
        return request("POST", "/v1/campaign/redeem", {"code": code.strip()},
                       key=key, base=base)
    return request("GET", "/v1/campaigns", key=key, base=base)


def claim_favorite(image_path, key=None, base=None):
    p = os.path.expanduser(str(image_path or "").strip().strip('"').strip("'"))
    if not p or not os.path.isfile(p):
        raise ApiError("file_not_found", f"截图文件不存在：{p or '(空路径)'}")
    with open(p, "rb") as f:
        raw = f.read()
    if len(raw) > 5 * 1024 * 1024:
        raise ApiError("image_too_large", "截图超过 5MB，请压缩后重试")
    if len(raw) < 1024:
        raise ApiError("bad_image", "截图太小（不足 1KB），请上传完整页面截图")
    return request("POST", "/v1/campaign/favorite-claim",
                   {"image_base64": base64.b64encode(raw).decode()},
                   key=key, base=base, timeout=180)
