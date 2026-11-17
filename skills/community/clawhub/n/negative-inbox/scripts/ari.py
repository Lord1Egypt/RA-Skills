#!/usr/bin/env python3
"""ARI CLI for the amazon-negative-review-inbox Skill.

Uses only Python's standard library. Paid collection and AI analysis commands
require an explicit --confirm flag after a free preview/quote.
"""

import argparse
import getpass
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor


# VERSION 必须与 _meta.json 的 version 一致：它进 User-Agent，服务端据此统计版本分布
# 并判定最低支持版本。发版时两处一起改。
VERSION = "1.5.3"
# CHANNEL 标记分发渠道（不同市场 listing），由打包脚本按变体烙入；官方母版为空串。
# 非空时 User-Agent 追加 " ch/<渠道>"，服务端据此统计各渠道的注册与用量。
CHANNEL = "negative-inbox"
PROD_BASE = "https://ari.funewa.com"
TIMEOUT_SEC = 120
SITES = ("amz_us", "amz_uk", "amz_de", "amz_jp", "amz_ca", "amz_fr", "amz_es", "amz_it")
_exit_code = 0
# 服务端在每个 API Key 响应上广播最新版本，任意一条命令都能顺带发现有新版，
# 不必等用户想起来跑 check。
_release = {"latest": "", "url": ""}

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


class EndpointBlocked(ValueError):
    """Local security failure; never include an untrusted URL or credentials."""

    code = "ARI_ENDPOINT_BLOCKED"


class RedirectBlocked(EndpointBlocked):
    code = "ARI_REDIRECT_BLOCKED"


def validate_official_url(url):
    """Exact HTTPS origin, including authority syntax; TLS verifies the hostname."""
    if not isinstance(url, str) or any(ord(c) <= 32 or ord(c) == 127 for c in url) or "\\" in url:
        raise EndpointBlocked()
    try:
        parsed = urllib.parse.urlsplit(url)
        if (parsed.scheme != "https" or
                parsed.netloc.lower() not in ("ari.funewa.com", "ari.funewa.com:443") or
                parsed.hostname != "ari.funewa.com" or parsed.port not in (None, 443) or
                parsed.username is not None or parsed.password is not None or parsed.fragment):
            raise EndpointBlocked()
    except ValueError:
        raise EndpointBlocked() from None
    return parsed


def base_url():
    """Production builds do not support custom endpoints, even with the old opt-in."""
    override = os.environ.get("ARI_BASE_URL")
    if override:
        parsed = validate_official_url(override)
        if parsed.path not in ("", "/") or parsed.query or "?" in override or "#" in override:
            raise EndpointBlocked()
    return PROD_BASE


def web_root():
    """Account, billing and report links always use the official website."""
    return PROD_BASE


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        # Reject before parsing Location, copying headers, or issuing another request.
        fp.close()
        raise RedirectBlocked()

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def api_request(method, path, payload=None, params=None, accept="application/json", authenticated=True):
    """Validate the final destination before reading any API key."""
    if not isinstance(path, str) or not path.startswith("/api/v1/") or "?" in path or "#" in path:
        raise EndpointBlocked()
    url = base_url() + path
    if params:
        url += "?" + urllib.parse.urlencode(params, doseq=True)
    validate_official_url(url)
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {"Accept": accept, "User-Agent": user_agent()}
    if data is not None:
        headers["Content-Type"] = "application/json"
    if authenticated:
        headers["Authorization"] = "Bearer " + require_key()
    return urllib.request.Request(url, data=data, headers=headers, method=method)


def open_api(req, timeout):
    validate_official_url(req.full_url)
    # A private opener avoids globally installed redirect handlers. Default HTTPS
    # certificate/hostname verification is retained; do not install an insecure context.
    return urllib.request.build_opener(NoRedirect()).open(req, timeout=timeout)


def endpoint_error(exc):
    return error_obj(exc.code, 0, "安全策略已阻止非官方地址或重定向",
                     "仅支持 https://ari.funewa.com。清除自定义 ARI_BASE_URL；"
                     "ARI_ALLOW_CUSTOM_BASE 不再生效。若官方请求发生跳转，请联系 ARI 支持。")


def user_agent():
    """版本号后随渠道尾巴（若有）。服务端按第一个空格截断取版本。"""
    ua = "ARI-Review-Skill/" + VERSION
    return ua + " ch/" + CHANNEL if CHANNEL else ua


def links():
    root = web_root()
    return {
        "apiKeys": root + "/zh/account?ui=d47626f#api-keys",
        "billing": root + "/zh/billing",
        "products": root + "/zh/products",
        "reports": root + "/zh/reports",
        "dashboard": root + "/zh/dashboard",
        "notify": root + "/zh/account#notify",
        "monitor": root + "/zh/monitor",
    }








def config_path():
    return os.path.expanduser("~/.ari/config.json")


def resolve_key():
    """Key 只从 ARI_API_KEY 或用户配置目录读取。

    刻意不回退到 Skill 包目录：那个位置会随 Skill 一起被打包、复制或提交，
    与「Key 只保存在本机用户配置中」的承诺相悖。
    """
    key = os.environ.get("ARI_API_KEY", "").strip()
    if not key:
        path = config_path()
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as fh:
                    key = (json.load(fh).get("api_key") or "").strip()
            except (OSError, json.JSONDecodeError):
                key = ""
    # configure/setup 写入前都校验过前缀，这里再拦一道：环境变量或手工编辑过的
    # 配置文件里放了残缺 Key 时，与其让每个请求 401，不如本地直接说清楚。
    if key and not key.startswith("ari_live_"):
        emit(error_obj(
            "ARI_API_KEY_INVALID_FORMAT", 0,
            "已配置的 Key 不是 ari_live_ 开头，可能残缺或被改动过",
            "运行 python ari.py setup 重新授权，或 configure 重新粘贴完整 Key。"))
        raise SystemExit(2)
    return key or None


def require_key():
    key = resolve_key()
    if key:
        return key
    emit(error_obj(
        "ARI_API_KEY_MISSING", 0,
        "未找到 ARI API Key",
        "推荐运行 python ari.py setup 浏览器一键授权；也可 configure 手动粘贴或设置 ARI_API_KEY。",
    ))
    raise SystemExit(2)


def error_obj(code, status, message, hint="", query=None, partial=None):
    out = {
        "success": False,
        "error": {"code": code, "status": status, "message": message, "hint": hint},
        "links": links(),
    }
    if query is not None:
        out["_query"] = query
    if partial:
        out["partial"] = partial
    return out


def version_tuple(v):
    out = []
    for part in str(v or "").split("."):
        try:
            out.append(int(part.strip()))
        except ValueError:
            out.append(0)
    return tuple(out)


def version_cmp(a, b):
    """比较点分版本号，返回 -1/0/1。与服务端 compareVersions 同语义。

    段数不同时短的补 0：裸用元组比较会把 1.0 判成早于 1.0.0（前缀更短即更小），
    从而对已是最新版的用户反复弹升级提示。
    """
    at, bt = version_tuple(a), version_tuple(b)
    n = max(len(at), len(bt))
    at += (0,) * (n - len(at))
    bt += (0,) * (n - len(bt))
    return (at > bt) - (at < bt)


def note_release(headers):
    """记录服务端广播的最新版本（响应头），供 update_info 生成升级提示。"""
    try:
        latest = (headers.get("X-ARI-Skill-Latest") or "").strip()
        url = (headers.get("X-ARI-Skill-Update-Url") or "").strip()
    except Exception:
        return
    if latest:
        _release["latest"] = latest
    if url:
        _release["url"] = url


def update_info():
    """本地版本低于服务端最新版时返回升级提示，否则 None。

    只在「确实更旧」时提示：本地版本更新（开发中）不该反复告警。
    """
    latest = _release.get("latest") or ""
    if not latest or version_cmp(VERSION, latest) >= 0:
        return None
    return {
        "current": VERSION, "latest": latest,
        "url": _release.get("url") or links()["apiKeys"],
        "message": "有新版 Skill（%s → %s）。请通过原安装渠道更新后再使用；"
                   "本 CLI 不会自行下载或执行任何远端代码。" % (VERSION, latest),
    }


def emit(obj, compact=False):
    global _exit_code
    if isinstance(obj, dict) and obj.get("success") is False:
        _exit_code = 1
    if isinstance(obj, dict):
        upd = update_info()
        if upd:
            obj["update"] = upd
    print(json.dumps(
        obj, ensure_ascii=False,
        separators=((",", ":") if compact else (", ", ": ")),
        indent=(None if compact else 2),
    ))


def err_code(out):
    if not isinstance(out, dict):
        return ""
    err = out.get("error")
    if isinstance(err, dict) and err.get("code"):
        return str(err["code"])
    return str(out.get("code") or "")




def parse_http_error(exc, query):
    note_release(exc.headers)  # 426（版本过旧）等错误响应同样带广播头
    try:
        detail = json.loads(exc.read().decode("utf-8", errors="replace"))
    except Exception:
        detail = {}
    if isinstance(detail, dict) and detail:
        detail["_httpStatus"] = exc.code
        detail["_query"] = query
        detail["links"] = links()
        return detail
    return error_obj("HTTP_ERROR", exc.code, "HTTP %d" % exc.code, query=query)


def as_collecting(out, http_status):
    """把「采集中、暂无足够数据」的 202 转成显式错误码。

    服务端在这种情况下返回 202 + success:true，但信封里既没有报告也没有内容；
    照原样交给上层会被当成一次成功的分析。该分支未扣点，重试是免费的。
    """
    if http_status != 202 or not isinstance(out, dict):
        return None
    data = out.get("data")
    if not isinstance(data, dict) or data.get("status") != "COLLECTING":
        return None
    wait = data.get("retryAfterSeconds") or 30
    return error_obj(
        "ARI_COLLECTING", 202, "该 ASIN 正在采集中，暂无足够数据可分析",
        "本次未扣点。等待约 %s 秒后重试即可（该分支重试免费）。" % wait)


def request_json(method, path, payload=None, params=None):
    query = {
        "method": method,
        "path": path,
        "params": {k: v for k, v in (params or {}).items() if v not in (None, "")},
        "payload": payload,
    }
    try:
        req = api_request(method, path, payload, query["params"])
        with open_api(req, timeout=TIMEOUT_SEC) as resp:
            note_release(resp.headers)
            raw = resp.read().decode("utf-8")
            out = json.loads(raw) if raw else {"success": True, "data": None}
            if isinstance(out, dict):
                alt = as_collecting(out, resp.status)
                if alt is not None:
                    alt["_query"] = query
                    return alt
                out["_query"] = query
            return out
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI 官方服务状态", query)




def fetch_release():
    """读取公开的版本发布信息（免认证，Key 缺失或失效时也能拿到升级入口）。

    失败一律静默返回 None——查不到新版说明不该影响任何正常命令。
    """
    try:
        req = api_request("GET", "/api/v1/public/config", authenticated=False)
        with open_api(req, timeout=15) as resp:
            note_release(resp.headers)
            body = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None
    rel = ((body or {}).get("data") or {}).get("skillRelease")
    if not isinstance(rel, dict):
        return None
    if rel.get("latest"):
        _release["latest"] = str(rel["latest"])
    if rel.get("url"):
        _release["url"] = str(rel["url"])
    return rel


def data_of(out):
    return out.get("data") if isinstance(out, dict) else None


def ok(out):
    return isinstance(out, dict) and out.get("success") is True






def save_key(key):
    """写本机用户配置（0600 直接创建，避免「默认权限 → chmod」之间的可读窗口）。"""
    path = config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump({"api_key": key}, fh)
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return path


def cmd_configure(args):
    key = getpass.getpass("ARI API Key (ari_live_*): ").strip()
    if not key.startswith("ari_live_"):
        emit(error_obj("ARI_API_KEY_INVALID_FORMAT", 0, "Key 必须以 ari_live_ 开头"), args.compact)
        raise SystemExit(2)
    path = save_key(key)
    emit({"success": True, "data": {
        "configured": True, "path": path,
        "note": "Windows 上 POSIX 权限位不生效，请自行确保该路径不被共享或同步到云端。",
    }}, args.compact)


def request_public(method, path, payload=None, timeout=15):
    """免认证请求（设备码授权等公开端点），错误统一转 error_obj。"""
    query = {"method": method, "path": path, "params": {}, "payload": payload}
    try:
        req = api_request(method, path, payload, authenticated=False)
        with open_api(req, timeout=timeout) as resp:
            note_release(resp.headers)
            out = json.loads(resp.read().decode("utf-8"))
            if isinstance(out, dict):
                out["_query"] = query
            return out
    except EndpointBlocked as exc:
        return endpoint_error(exc)
    except urllib.error.HTTPError as exc:
        return parse_http_error(exc, query)
    except Exception as exc:
        return error_obj("NETWORK_ERROR", 0, str(exc), "检查网络或 ARI 官方服务状态", query)


def cmd_setup(args):
    """设备码授权：浏览器点一下，Key 自动落到本机，全程无复制粘贴。

    进度提示走 stderr（用户/代理立即可见），stdout 仍只输出最终 JSON。
    刻意不在 CLI 里做注册：注册留在网页（人机验证与邮箱验证防线不动）。
    """
    start = request_public("POST", "/api/v1/auth/device/start", {})
    if not ok(start):
        emit(start, args.compact)
        return
    data = start.get("data") or {}
    code = str(data.get("code") or "")
    verify_url = str(data.get("verifyUrl") or "")
    token = str(data.get("pollToken") or "")
    interval = max(1, int(data.get("interval") or 3))
    expires = int(data.get("expiresIn") or 600)
    if not (code and verify_url and token):
        emit(error_obj("ARI_DEVICE_START_MALFORMED", 0, "服务端响应缺少必要字段"), args.compact)
        return

    try:
        validate_official_url(verify_url)
    except EndpointBlocked as exc:
        emit(endpoint_error(exc), args.compact)
        return

    print("请在浏览器打开以下链接完成授权（设备码 %s，%d 分钟内有效）：" % (code, expires // 60),
          file=sys.stderr)
    print("  " + verify_url, file=sys.stderr)
    print("未注册会先引导注册（需完成邮箱验证）；授权后本命令自动完成。", file=sys.stderr)

    deadline = time.time() + expires
    while time.time() < deadline:
        time.sleep(interval)
        poll = request_public("POST", "/api/v1/auth/device/poll", {"pollToken": token})
        if not ok(poll):
            if err_code(poll) in ("ARI_NOT_FOUND", "ARI_ENDPOINT_BLOCKED", "ARI_REDIRECT_BLOCKED"):
                emit(poll, args.compact)
                return
            continue  # 网络抖动/限流：下轮再试
        status = str((poll.get("data") or {}).get("status") or "")
        if status == "APPROVED":
            key = str((poll.get("data") or {}).get("apiKey") or "")
            if not key.startswith("ari_live_"):
                emit(error_obj("ARI_DEVICE_KEY_MALFORMED", 0, "服务端未返回有效 Key"), args.compact)
                return
            path = save_key(key)
            emit({"success": True, "data": {
                "configured": True, "path": path,
                "keyPrefix": key[:len("ari_live_") + 8],
                "note": "API Key 已保存到本机用户配置，其余命令可直接使用。",
            }}, args.compact)
            return
        if status == "CLAIMED":
            emit(error_obj(
                "ARI_DEVICE_ALREADY_CLAIMED", 0, "该会话的 Key 已被领取",
                "若非你本人操作，请到用户中心撤销该 Key 后重新运行 setup。"), args.compact)
            return
        if status == "EXPIRED":
            break
    emit(error_obj(
        "ARI_DEVICE_EXPIRED", 0, "授权未在有效期内完成",
        "重新运行 python ari.py setup 并尽快在浏览器完成授权。"), args.compact)


def cmd_check(args):
    # 先取公开发布信息：Key 无效时也能顺带告诉用户「你的版本旧了、去哪儿更新」。
    release = fetch_release()
    me = request_json("GET", "/api/v1/user/me")
    if not ok(me):
        emit(me, args.compact)
        return
    balance = request_json("GET", "/api/v1/credits/balance")
    if not ok(balance):
        emit(balance, args.compact)
        return
    # 1.4.11：不再回报账户免确认策略。它只服务于「小额付费操作直接生成」，等于把
    # 「不用先问」交给 agent，与全系列「先报价、用户明确确认才执行」的契约冲突
    # （ClawSweeper 归类为 Autonomous Decision Making）。付费门槛仍由服务端策略
    # 控制，本地不做任何隐式确认，所以 check 只回 Key、账户与余额。
    emit({"success": True, "data": {
        "skillVersion": VERSION,
        "release": release,
        "user": data_of(me),
        "balance": data_of(balance),
    }, "links": links()}, args.compact)






















































def cmd_reviews(args):
    """读取已采集评论。

    --sort helpful 配合 --stars negative 就是「高赞差评榜」：买家在商品页最先看到的
    就是这几条，对转化伤害最大，也是卖家最该先处理的。1.3.0 只能按时间排，这批评论
    永远沉在后面。
    """
    params = {"asin": args.asin.upper(), "site": args.site, "star": args.star,
              "stars": args.stars, "q": args.query, "page": args.page,
              "sort": args.sort}
    if getattr(args, "topic", ""):
        params["topic"] = args.topic  # 1.4.7：按话题标签筛，返回行带 tags（原句可引用）
    if args.with_images:
        params["withImages"] = "1"
    if args.vine:
        params["vine"] = "1"
    if args.purchased:
        params["purchased"] = "1"
    emit(request_json("GET", "/api/v1/reviews", params=params), args.compact)
























def allowed_commands():
    """专属包构建期写入的命令白名单；返回 None 表示不限制。

    1.4.11 起打包脚本会把文档没有承诺的命令从本文件里整段删掉。这里再读
    一次 skill-defaults.json 兜底：只删代码不留闸的话，任何人把命令加回来
    就绕过了收窄。母版与全功能马甲包没有这个字段，行为完全不变。
    """
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "skill-defaults.json")
    try:
        with open(path, encoding="utf-8") as fh:
            value = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(value, dict):
        return None
    commands = value.get("allowedCommands")
    if not isinstance(commands, list):
        return None
    allowed = {item.strip() for item in commands
               if isinstance(item, str) and item.strip()}
    return allowed or None


































def cmd_alerts(args):
    """情感预警（免费）。差评突增等预警由服务端离线生成，这里只读。"""
    if args.mark_read:
        emit(request_json("POST", "/api/v1/alerts/read"), args.compact)
        return
    emit(request_json("GET", "/api/v1/alerts", params={"limit": args.limit}), args.compact)












ASIN_RE = re.compile(r"^[A-Z0-9]{10}$")
# 文档示例里的占位 ASIN：格式合法但必然不是真实商品，单独拦截并给出明确指引。
PLACEHOLDER_ASINS = {"B0XXXXXXXX", "B0AAAAAAAA", "B0BBBBBBBB"}


def check_asin_args(args):
    """本地快速失败：格式错误的 ASIN 不值得打到服务端换一个模糊的 4xx。

    ASIN 只保证 10 位字母数字，不保证以 B 开头（书类沿用 ISBN-10，数字开头），
    所以校验不能写死 B 前缀。顺手把值归一成大写，后续命令不必再 upper()。
    """
    for attr in ("asin", "competitor"):
        value = getattr(args, attr, None)
        if value in (None, ""):
            continue
        normalized = str(value).strip().upper()
        if not ASIN_RE.match(normalized) or normalized in PLACEHOLDER_ASINS:
            emit(error_obj(
                "ARI_INVALID_ASIN", 0,
                "%s 不是有效的 ASIN（应为 10 位字母数字，如 B08N5WRWNW）" % value,
                "请从商品详情页 URL 的 /dp/ 后复制真实 ASIN；文档中的占位符示例不能直接使用。"),
                args.compact)
            raise SystemExit(2)
        setattr(args, attr, normalized)


def cmd_version(args):
    emit({"success": True, "data": {
        "skillVersion": VERSION,
        "channel": CHANNEL or "official",
        "python": sys.version.split()[0],
    }}, args.compact)








def main():
    # --compact 用 parents 挂到每个子命令上，这样放在子命令前后都能识别。
    # default=SUPPRESS 是必须的：否则子解析器会用自己的默认值覆盖掉
    # 已经在顶层解析出来的 --compact。缺省值只能在 parse_args 之后补，
    # 不能用 set_defaults——parents 共享同一个 action 对象，
    # set_defaults 会把 SUPPRESS 改掉，反而把覆盖问题带回来。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--compact", action="store_true",
                        default=argparse.SUPPRESS, help="输出单行 JSON")

    ap = argparse.ArgumentParser(prog="ari.py", parents=[common],
                                 description="ARI Amazon 评论采集与智能分析 CLI")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("setup", parents=[common],
                       help="浏览器一键授权，自动获取并保存 API Key（推荐首次使用）")
    p.set_defaults(fn=cmd_setup)

    p = sub.add_parser("configure", parents=[common], help="隐藏输入并保存 ARI API Key")
    p.set_defaults(fn=cmd_configure)

    p = sub.add_parser("check", parents=[common], help="验证 Key、账户和积点余额")
    p.set_defaults(fn=cmd_check)


    p = sub.add_parser("version", parents=[common], help="显示 Skill 版本与渠道（无需 Key）")
    p.set_defaults(fn=cmd_version)




    p = sub.add_parser("reviews", parents=[common],
                       help="读取已采集评论（支持高赞差评榜 / 带图 / Vine / 真实购买）")
    p.add_argument("--asin", required=True)
    p.add_argument("--site", default="amz_us", choices=SITES)
    p.add_argument("--star", type=int, choices=range(1, 6), help="单一星级，与 --stars 互斥（优先）")
    p.add_argument("--stars", default="", choices=("", "negative", "positive"),
                   help="negative=1-3星 positive=4-5星")
    p.add_argument("--sort", default="recent",
                   choices=("recent", "helpful", "star_asc", "oldest"),
                   help="helpful=高赞优先（配 --stars negative 即高赞差评榜）")
    p.add_argument("--with-images", action="store_true", help="只看带买家实拍图的评论")
    p.add_argument("--vine", action="store_true", help="只看 Vine 评论")
    p.add_argument("--purchased", action="store_true", help="只看已验证购买")
    p.add_argument("--query")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--topic", default="", help="按话题 key 筛（1.4.7，key 来自 topics 命令）")
    p.set_defaults(fn=cmd_reviews)



























    p = sub.add_parser("alerts", parents=[common], help="情感预警列表（免费）")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--mark-read", action="store_true", help="把全部未读预警置为已读")
    p.set_defaults(fn=cmd_alerts)








    args = ap.parse_args()
    if not hasattr(args, "compact"):
        args.compact = False
    # 专属包的运行期兜底闸。打包脚本（scripts/build_skill_variants.py）已把
    # 未承诺的命令从本文件整段删掉，这里再按 skill-defaults.json 的
    # allowedCommands 复核一次——只删代码不留闸的话，把命令加回来就绕过了收窄。
    allowed = allowed_commands()
    if allowed is not None and getattr(args, "command", None) not in allowed:
        emit(error_obj(
            "ARI_COMMAND_NOT_ALLOWED", 0,
            "本包不提供 %s 命令" % getattr(args, "command", "?"),
            "此 Skill 只提供：%s。需要其他能力请安装对应的 ARI Skill 包。" %
            "、".join(sorted(allowed))), args.compact)
        raise SystemExit(2)
    check_asin_args(args)
    args.fn(args)
    raise SystemExit(_exit_code)


if __name__ == "__main__":
    main()
