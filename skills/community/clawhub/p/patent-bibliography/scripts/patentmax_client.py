#!/usr/bin/env python3
"""PatentMax API 客户端 —— 专利检索与统计分析。

给 AI 用的命令行工具。每个子命令往 stdout 吐一份 JSON，出错时 JSON 里带
error 和给人看的中文提示，不抛栈。

几件事在这里处理掉，免得让模型自己踩：

1. **一篇专利 = 一次调用**。`brief` 打的是整篇接口，一次拿回著录 + 权利要求 +
   说明书全文，计一次价。不要为了"只要权项"去单独打 claims —— 那是按字段零售，
   同样的内容会收好几遍钱。

2. **字段名不稳定**。上游同一个东西可能叫 pn、publicationNumber 或 documentNumber，
   pick() 按候选名依次取，取不到返回 None，不让 KeyError 冒出来。

3. **花了多少钱由服务端说了算**。输出里的 `_spent` / `_balance` 全部来自响应头，
   不是本地估算。客户端**不做**任何价格推算——历史上本地估价和实际账单对不上，
   比不给还糟。

依赖：只用标准库，不需要 pip install。

────────────────────────────────────────────────────────────────
v3.0.0 相对 v2 的变化（2026-09-22 服务端改版后）：

· 整篇接口 /api/patent 上线：brief 从「换 id + 取详情 + 取权项 + 取全文」
  四次调用压成一次，单篇从 ¥0.25 降到 ¥0.10。
· **临时 id 那一整套没了**。所有按篇取数的接口现在都直接认公开号（pn），
  换 id 的前置检索由服务端承担、不进用户账单。于是删掉：落盘 id 缓存、
  TTL、404 作废重取、以及散落各处的「传 --id 能省 ¥0.10」提示。
  ——那些机制当初存在的唯一理由就是躲开那笔过路费，过路费取消了，它们
  只剩下复杂度和失效 id 带来的 404。
· 不再输出每条命令的 `_cost` 估算，只输出服务端回的真实 `_spent`。
· 检索和整篇每天前 30 次免费，输出里会带 `_free_remaining`。

v3.3.0（2026-10-10）：
· **失败不能读成 0 条**。--json-out 先写一个 incomplete 占位，失败时把错误写进
  同一个文件——旧版失败时文件不动，模型会读到上一次的成功结果；结构认不出的响应
  也直接报错，不再静默返回空列表。
· 同一任务内的付费请求带 Idempotency-Key：网络超时后重跑同一条命令不会重复扣费，
  同一篇专利重复 brief 也由服务端直接重放。
· 候选台账：search / similar 的每条结果标 seen_before，输出 new_candidates，
  饱和判断（「这一式没带来新专利」）不用再靠模型记忆；`candidates` 命令列出 / 标注。
· `read`：从已保存的结果文件里只取需要的那部分（索引、单篇、按关键词定位全文段落），
  不调接口、不花钱。
· 检索结果附本页 IPC / 申请人分布，第一式就能拿到下一式要用的分类线索。
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import uuid
import urllib.error
import urllib.parse
import urllib.request

class SameOriginRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Never forward credentials or trial request bodies to a different origin."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        def origin(url):
            parsed = urllib.parse.urlsplit(url)
            return (parsed.scheme.lower(), (parsed.hostname or "").lower(),
                    parsed.port or (443 if parsed.scheme.lower() == "https" else 80))
        try:
            if origin(req.full_url) != origin(newurl):
                return None
        except ValueError:
            return None
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def safe_urlopen(req, timeout):
    return urllib.request.build_opener(SameOriginRedirectHandler()).open(req, timeout=timeout)


# Windows 控制台默认按 GBK 解码，中文专利标题会乱码
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "https://api.ip930.com"
API_KEY = os.environ.get("PATENTMAX_API_KEY", "").strip()


# 试用金用完后，用户注册拿到的正式密钥由 AI 写进这个文件（只写密钥一行），所有 PatentMax 技能都会自动读取
def _saved_key_path():
    root = os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")
    return os.path.join(root, "api_key.txt")


if not API_KEY:
    try:
        API_KEY = open(_saved_key_path(), encoding="utf-8").read().strip()
    except OSError:
        pass

TRIAL_CONTINUE = "\n注册后在「API 平台」创建一个密钥（pm_live_ 开头）发给我，我存好后接着帮你做。"


def trial_end_extra():
    return {"free_trial": True,
            "ai_hint": "把message原样转告用户，注册链接不要省略。用户提供密钥后，默认仅在本次命令的进程环境中设置PATENTMAX_API_KEY重跑，不修改全局环境变量。"
                       "先让用户选择是否保存到本机；仅明确同意持久保存时，才将一行密钥写入当前用户的私有目录中的"
                       f"{_saved_key_path()}。POSIX文件权限必须为0600，Windows必须使用仅当前用户有读取权限的目录/文件。"
                       "无法确认私有权限时只临时使用，不落盘。不要回显密钥或把密钥写进交付文件。"}


TIMEOUT = 60


# ─────────────────────── 免费试用密钥 ───────────────────────
#
# 没设 PATENTMAX_API_KEY 时，第一次调用自动领一把免费试用密钥（不用注册），
# 存在 ~/.patentmax/ 下，之后接着用。规则由服务端定：每把 ¥8、30 天有效、
# 只开通这个 Skill 用到的功能。用完或过期后，注册 PatentMax 换正式密钥即可。
# 设了 PATENTMAX_API_KEY 就一律用它，不会去领试用。
TRIAL_SOURCE = "patent-search-cn"
TRIAL_GROUP = "patent-search"
TRIAL_REGISTER_URL = "https://api.ip930.com/features/api-platform"
KEY_FROM_TRIAL = False


def _trial_key_path():
    root = os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")
    return os.path.join(root, f"trial-key-{TRIAL_GROUP}.json")


def _load_trial_key():
    try:
        with open(_trial_key_path(), encoding="utf-8") as fh:
            saved = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(saved, dict) or saved.get("base_url") != BASE_URL:
        return None
    expires = str(saved.get("expires_at") or "")
    # ISO 时间同为 UTC，可直接按字符串比
    if expires and expires <= time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()):
        return None
    return saved.get("api_key") or None


def _server_message(detail):
    try:
        body = json.loads(detail)
    except ValueError:
        return ""
    error = body.get("error") if isinstance(body, dict) else None
    return str(error.get("message") or "") if isinstance(error, dict) else ""


def _claim_trial_key():
    url = f"{BASE_URL}/api/v1/trial-keys"
    data = json.dumps({"source": TRIAL_SOURCE}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with safe_urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        message = _server_message(exc.read().decode("utf-8", "replace"))
        die(message or f"领取免费试用密钥失败（HTTP {exc.code}）。也可以注册 PatentMax 创建正式密钥：{TRIAL_REGISTER_URL}",
            free_trial=True, register_url=TRIAL_REGISTER_URL)
    except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as exc:
        die(f"领取免费试用密钥失败：{getattr(exc, 'reason', exc)}", free_trial=True)
    data = payload.get("data") if isinstance(payload, dict) else None
    key = data.get("api_key") if isinstance(data, dict) else None
    if not key:
        die("领取免费试用密钥失败：服务端没有返回密钥。", free_trial=True)
    path = _trial_key_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({
                "api_key": key,
                "expires_at": data.get("expires_at"),
                "spending_limit_yuan": data.get("spending_limit_yuan"),
                "source": TRIAL_SOURCE,
                "base_url": BASE_URL,
            }, fh, ensure_ascii=False, indent=2)
        os.chmod(path, 0o600)
    except OSError:
        pass  # 存不下就只用这一次，下次再领
    # 走 stderr，不混进 stdout 的 JSON；请把这句话转告用户。Windows 控制台默认 GBK，¥ 会变成转义
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    print(f"[PatentMax] 已自动领取免费试用：{data.get('note') or ''}", file=sys.stderr)
    return key


def ensure_api_key():
    """有 PATENTMAX_API_KEY 用它；没有就用本地存的试用密钥，再没有就领一把。"""
    global API_KEY, KEY_FROM_TRIAL
    if API_KEY:
        return API_KEY
    API_KEY = _load_trial_key() or _claim_trial_key()
    KEY_FROM_TRIAL = True
    return API_KEY


def explain_trial_error(code, detail, url):
    """试用密钥碰到额度用完、功能没开通时，原样给出服务端的话（里面有下一步怎么办）。"""
    if not KEY_FROM_TRIAL:
        return
    if code == 401:
        # 过期或被停用：清掉本地缓存，下次运行自动领新的
        try:
            os.remove(_trial_key_path())
        except OSError:
            pass
        die("免费试用密钥已过期或失效，本地缓存已清除。重跑同一条命令会自动领取新的试用密钥；"
            f"也可以注册 PatentMax 换正式密钥：{TRIAL_REGISTER_URL}",
            free_trial=True, url=url.split("?")[0])
    # 只接管试用特有的错误（额度用完、功能没开通），其余照常走通用提示
    message = _server_message(detail)
    if "免费试用" in message:
        extra = trial_end_extra()
        extra.update(register_url=TRIAL_REGISTER_URL, url=url.split("?")[0])
        die(message + (TRIAL_CONTINUE if "用完" in message else ""), **extra)

# 单价（元），跟服务端 defaultPatentDataPrices 对齐。
#
# **只给预算闸门做放行估算用，不打印给模型看。**
# 真实扣费一律以响应头里的 x-patentmax-charged-cents 为准：本地表迟早和服务端
# 走偏（v2 就是这样，表里还写着 claims ¥0.20 而服务端早已是 ¥0.05），
# 而一旦打印出来，模型就会拿这个错数去跟用户交代花了多少钱。
PRICES = {
    "search": 0.10, "patent": 0.10,
    "detail": 0.05, "claims": 0.05, "fulltext": 0.05,
    "legal": 0.05, "citation": 0.05, "similar": 0.10, "img": 0.05,
    "pdf": 0.30, "portrait": 0.30, "ration": 0.30,
}


#: 本次命令的 --json-out 路径。die() 也要往这里写，见 die() 的说明。
_json_out = None


def die(message, exit_code=1, **extra):
    """出错也走 stdout 的 JSON，让调用方只解析一个地方。

    退出码约定：1 = 参数错/网络错/上游错（改了再试）；
    3 = 预算拦截（不是故障，是"本次任务的钱不够了"，要先问用户）。

    给了 --json-out 时错误**同时写进那个文件**。旧版只打 stdout、文件不动——
    同名文件里还躺着上一次的成功结果，模型去读文件就把失败当成了成功。
    """
    payload = {"error": True, "message": message}
    payload.update(extra)
    payload.setdefault("_meaning", "命令失败，不等于检索到 0 条。不要写成「未检索到相关专利」，"
                                   "先按 message 处理，处理不了就如实告诉用户这一步没跑成。")
    if _json_out:
        try:
            with open(_json_out, "w", encoding="utf-8") as fh:
                json.dump(payload, fh, ensure_ascii=False, indent=2)
            payload["saved_to"] = os.path.abspath(_json_out)
        except OSError:
            pass
    # 有 --json-out 说明调用方的控制台不可靠（Windows GBK），stdout 一律转义成 ASCII
    print(json.dumps(payload, ensure_ascii=bool(_json_out), indent=2))
    sys.exit(exit_code)


# 本次进程内累计的实扣、最近一次返回的余额、以及每日免费额度用量（单位：分）
# saw_header 区分"服务端说这次扣了 0 元"和"服务端根本没回这个头"：
# 老版本服务端没有计费头，此时绝不能输出 _spent: ¥0.00 —— 那等于告诉模型本次免费，
# 比不给还糟。只有真收到过头才输出这些字段。
_billing = {"charged_cents": 0, "balance_cents": None, "saw_header": False,
            "free_used": None, "free_quota": None, "replayed": False}


def _record_billing(response_headers):
    """从响应头收集计费信息。头缺失时静默跳过——老版本服务端没有这些头。"""
    def as_int(name):
        value = response_headers.get(name)
        return None if value is None else int(value)

    try:
        charged = as_int("x-patentmax-charged-cents")
        if charged is not None:
            _billing["charged_cents"] += charged
            _billing["saw_header"] = True
        balance = as_int("x-patentmax-balance-cents")
        if balance is not None:
            _billing["balance_cents"] = balance
        used, quota = as_int("x-patentmax-free-used"), as_int("x-patentmax-free-quota")
        if used is not None and quota is not None:
            _billing["free_used"], _billing["free_quota"] = used, quota
        if response_headers.get("x-patentmax-idempotent-replay") == "true":
            _billing["replayed"] = True
    except (TypeError, ValueError):
        pass


def billing_summary():
    """附加到每个命令输出里的计费信息。

    三个数全部来自服务端，客户端不做算术：
      _spent          本次命令的合计实扣
      _balance        扣完后的账户余额（权威值）
      _free_remaining 今天还剩几次免费调用
    """
    if not _billing["saw_header"]:
        # 服务端没回计费头（未升级），保持沉默好过报一个编出来的数
        return {}
    out = {"_spent": f"¥{_billing['charged_cents'] / 100:.2f}"}
    if _billing["balance_cents"] is not None:
        out["_balance"] = f"¥{_billing['balance_cents'] / 100:.2f}"
        if _billing["balance_cents"] < 500 and not KEY_FROM_TRIAL:  # 试用用户不提醒，用完时服务端会给注册指引
            out["_balance_warning"] = (
                "余额不足 ¥5，继续批量检索会很快耗尽。"
                "请先提醒用户到 https://api.ip930.com/features/api-platform 充值。"
            )
    if _billing["free_quota"]:
        left = max(0, _billing["free_quota"] - (_billing["free_used"] or 0))
        out["_free_remaining"] = f"{left}/{_billing['free_quota']} 次（每日重置，仅检索与整篇）"
    if _billing["replayed"]:
        out["_replayed"] = "本任务里跑过一模一样的请求，服务端直接返回上次结果，未扣费"
    return out


#: 当前任务 id。设置后，request() 给每个请求带上由它派生的 Idempotency-Key。
_task_id = None


def idempotency_key(method, path, params):
    """同一任务 + 同一请求 → 同一个键。

    服务端对已成功的键直接重放、不再扣费（patent-data-api-service 的幂等处理）。
    带上它有两个好处：
      · 网络超时后重跑同一条命令，上游其实已经成功的那次不会被扣第二遍；
      · 同一篇专利在一个任务里被 brief 两次，第二次是免费重放。
    键里带任务 id：任务结束（闲置 1 小时）后同样的检索会重新取数，不会一直吃旧结果。
    """
    clean = sorted((k, str(v)) for k, v in (params or {}).items() if v is not None and v != "")
    raw = f"{_task_id}|{method}|{path}|{urllib.parse.urlencode(clean)}"
    return "pms-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:40]


def request(path, params=None, method="GET", body=None, headers=None, raw=False):
    ensure_api_key()

    url = f"{BASE_URL}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        url += "?" + urllib.parse.urlencode(clean)

    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    if _task_id:
        req.add_header("Idempotency-Key", idempotency_key(method, path, params))
    for key, value in (headers or {}).items():
        req.add_header(key, value)

    try:
        with safe_urlopen(req, timeout=TIMEOUT) as response:
            payload = response.read()
            # 服务端每个响应都回本次实扣和扣完后的余额。记下来，供 _spent/_balance 输出。
            # 拿服务端的真值，而不是在本地累加估价：跨进程累加迟早算岔，
            # 而余额是权威的——对账类的数字错一次就再也不被信任。
            _record_billing(response.headers)
            return payload if raw else json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        explain_trial_error(exc.code, detail, url)
        hint = {
            400: "参数有问题，检查必填项和取值范围。",
            401: "密钥无效或已撤销。确认 PATENTMAX_API_KEY 是 pm_live_ 或 pm_test_ 开头的完整密钥。",
            402: "余额不足。到 https://api.ip930.com/features/api-platform 充值。",
            403: "该密钥没有此接口的权限。",
            404: "没找到这篇专利。确认公开号正确且带国别代码，如 CN109761224A。",
            409: "同一个请求上一次还在处理中。等几秒重跑同一条命令即可，不会重复扣费。",
            429: "触发限流。生产密钥 600 次/分，测试密钥每天 30 次。",
        }.get(exc.code, "")
        die(f"HTTP {exc.code}：{hint}", detail=detail, url=url.split("?")[0])
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        die(f"网络请求失败：{getattr(exc, 'reason', exc)}",
            hint="请求可能已经到了服务端。重跑同一条命令即可——同一任务里的重复请求服务端会直接重放，"
                 "不重复扣费（说明书超长的极少数专利除外）。不要换个写法重发。")
    except json.JSONDecodeError:
        die("响应不是合法 JSON，可能上游异常。")


def pick(row, *names):
    """上游字段名不统一，按候选名依次取第一个非空值。"""
    if not isinstance(row, dict):
        return None
    for name in names:
        value = row.get(name)
        if value not in (None, "", []):
            return value
    return None


def rows_of(payload):
    """取出结果列表。不同接口的列表字段名不一样。

    2026-09-22 实测修正：相似专利接口把列表放在 **patentLikeList**，
    而这里原来只认 patents/list/data/records/rows —— 于是 `similar` **永远返回 0 条**，
    表现得像"服务端接口不可用"。SKILL.md 又把语义扩展当作检索空转时的救命动作，
    等于那条路一直是断的。

    所以除了列举已知字段名，最后再兜一层：**取第一个"元素是对象"的列表**。
    上游以后再冒出新名字也不会静默返回空。
    """
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if not isinstance(payload, dict):
        return []
    for name in ("patents", "patentLikeList", "list", "data", "records", "rows"):
        value = payload.get(name)
        if isinstance(value, list):
            return [r for r in value if isinstance(r, dict)]
    for value in payload.values():
        if isinstance(value, list) and value and all(isinstance(r, dict) for r in value):
            return value
    return []


def require_rows(payload, what):
    """取结果列表；**认不出结构就报错，不返回空列表**。

    rows_of() 兜底返回 [] 是给「列表就是空的」用的。响应根本不是列表结构
    （上游报错、网关返回 HTML 被代理改写、字段整体改名）时也返回 []，
    模型就会写出「未检索到相关专利」——这是检索报告里最严重的一种错。
    """
    if isinstance(payload, dict) and (payload.get("success") is False or payload.get("error")):
        reason = payload.get("message") or payload.get("msg") or payload.get("error")
        die(f"{what}接口返回失败：{str(reason)[:200]}")
    if isinstance(payload, list) or (
            isinstance(payload, dict) and any(isinstance(v, list) for v in payload.values())):
        return rows_of(payload)
    die(f"{what}接口的响应里没有结果列表，结构认不出来，不能当作 0 条。",
        detail=str(payload)[:300])


def page_profile(rows):
    """本页结果里的 IPC（到大组）和申请人分布，各取前 5。

    给下一式检索找分类和术语线索用：第一式跑完，从强相关那几篇对得上的分类号
    就是最该加的限定。**只统计本页这几十条**，不是全量分布——全量要 stats。
    """
    ipc, applicant = {}, {}
    for row in rows:
        code = re.sub(r"\s+", "", str(row.get("ipc") or "")).split("/")[0]
        if code:
            ipc[code] = ipc.get(code, 0) + 1
        for name in re.split(r"[;；]", str(row.get("applicant") or "")):
            name = name.strip()
            if name:
                applicant[name] = applicant.get(name, 0) + 1

    def top(counter):
        return [{"value": k, "count": v} for k, v in sorted(counter.items(), key=lambda kv: -kv[1])[:5]]

    return {"ipc_group": top(ipc), "applicant": top(applicant),
            "_note": f"只统计本页 {len(rows)} 条，用来找下一式的分类和术语线索，不是全量分布。"}


# ── 候选台账 ─────────────────────────────────────────────────
#
# 一个任务里所有检索、相似专利出现过的专利，按公开号去重记一本账。
#
# 为什么要有：饱和判断（「这一式还有没有带来新专利」）以前全靠模型记，
# 跑到第五六式时前面的结果早被挤出上下文，于是要么不敢停、要么重复 brief 同一篇。
# 现在每条结果标 seen_before，每次输出 new_candidates，停不停看数字。
#
# 台账跟着任务走（和次数闸同一个 task_id），闲置 1 小时后新任务从空账开始。
CANDIDATE_STATUSES = ("pending", "keep", "exclude")


def _ledger_path():
    return os.path.join(os.path.dirname(_session_path()), "candidates.json")


def _load_ledger(task_id):
    try:
        with open(_ledger_path(), encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        data = None
    if not isinstance(data, dict) or data.get("task_id") != task_id:
        return {"task_id": task_id, "items": {}}
    return data


def _save_ledger(ledger):
    try:
        with open(_ledger_path(), "w", encoding="utf-8") as fh:
            json.dump(ledger, fh, ensure_ascii=False)
    except OSError:
        pass


def validated_patent_number(value):
    raw = str(value or "").strip().upper()
    # Permit familiar publication-number separators, never filesystem syntax.
    if not raw or not re.fullmatch(r"[A-Z]{2}[A-Z0-9 /-]+", raw):
        raise ValueError("公开号格式不正确；请给国别代码、号码和类型码。")
    number = re.sub(r"[ /-]", "", raw)
    if not re.fullmatch(r"[A-Z]{2}[0-9][A-Z0-9]{1,39}", number):
        raise ValueError("公开号格式不正确；请核对原始文献号码。")
    return number


def _pn(value):
    return re.sub(r"[^A-Z0-9]", "", str(value or "").upper())


def same_patent(asked, returned):
    """请求的号和返回的号是不是同一篇。

    允许省略类型码（问 CN109761224，回 CN109761224A），也忽略斜杠、横线这类分隔符；
    除此之外不一致就是不同的专利。
    """
    a, b = (re.sub(r"[^A-Z0-9]", "", _pn(x)) for x in (asked, returned))
    return bool(a and b) and (a == b or (b.startswith(a) and re.fullmatch(r"[A-Z]\d?", b[len(a):]) is not None))


def track_candidates(rows, source):
    """把这批结果记进台账，给每行打 seen_before，返回本批新出现的篇数。"""
    if not _task_id:
        return None
    ledger = _load_ledger(_task_id)
    new = 0
    for row in rows:
        pn = _pn(row.get("patent_number"))
        if not pn:
            continue
        item = ledger["items"].get(pn)
        row["seen_before"] = item is not None
        if item is None:
            new += 1
            item = ledger["items"][pn] = {
                "title": row.get("title"), "applicant": row.get("applicant"),
                "application_date": row.get("application_date"),
                "legal_status": row.get("legal_status"),
                "first_seen": source, "hits": 0, "status": "pending", "reason": None,
            }
        item["hits"] += 1
    _save_ledger(ledger)
    return new


def mark_briefed(pn, basic, saved_to):
    if not _task_id or not pn:
        return
    ledger = _load_ledger(_task_id)
    item = ledger["items"].setdefault(_pn(pn), {
        "title": (basic or {}).get("title"), "applicant": (basic or {}).get("applicant"),
        "application_date": (basic or {}).get("application_date"),
        "legal_status": (basic or {}).get("legal_status"),
        "first_seen": "brief", "hits": 0, "status": "pending", "reason": None,
    })
    item["briefed"] = True
    if saved_to:
        item["brief_file"] = saved_to
    _save_ledger(ledger)


def with_ledger_summary(result, rows, source):
    new = track_candidates(rows, source)
    if new is not None:
        result["new_candidates"] = new
        result["seen_candidates"] = len(rows) - new
        if rows and new == 0:
            result["_saturation"] = "这一批全是本任务里已经出现过的专利，没有带来新候选。"
    return result


def normalize(row):
    """把一行结果压成稳定的字段名。

    2026-09-22 实测修正两处一直取不到的字段：

    · **摘要在 `summary` 里，不叫 abstract**（上游压根没有 abstract 这个字段）。
      原来每行返回的 abstract 都是 null —— 而整个「先筛后读」策略的前提就是
      "检索结果自带摘要，靠摘要判断相不相关"。摘要为空时模型只能逐篇取正文，
      这正是费用失控的根因之一。
    · **公开日在 `documentDate` 里**，publicationDate 同样不存在。
    """
    return {
        "patent_number": pick(row, "documentNumber", "publicationNumber", "pn"),
        "title": pick(row, "title", "ti"),
        "applicant": pick(row, "applicant", "currentAssignee", "pa"),
        "inventor": pick(row, "inventor", "pi"),
        "application_date": pick(row, "applicationDate", "ad"),
        "publication_date": pick(row, "documentDate", "publicationDate", "pd"),
        "ipc": pick(row, "mainIpc", "ipc"),
        "type": pick(row, "type", "documentType"),
        "legal_status": pick(row, "legalStatus", "currentStatus"),
        "abstract": pick(row, "summary", "abstract", "ab"),
    }


def patent_number_of(args):
    """取本次要操作的公开号。

    所有按篇取数的接口都直接认公开号，不再需要先换临时 id。
    保留 --id 只为兼容：手上已有内部 id 时可以直接用，价钱一样。
    """
    given = (getattr(args, "id", None) or "").strip()
    if given:
        return {"id": given}
    number = (getattr(args, "patent", None) or "").strip()
    if not number:
        die("请给 --patent（公开号，如 CN109761224A）。")
    try:
        return {"pn": validated_patent_number(number)}
    except ValueError as exc:
        die(str(exc))


def do_search(args):
    payload = request("/api/search", {
        "q": args.q,
        "ds": "cn" if args.scope == "cn" else "all",
        "page": args.page,
        "size": args.size,
        "sort": getattr(args, "sort", None),
        "hl": "1" if getattr(args, "highlight", False) else None,
    })
    rows = [normalize(r) for r in require_rows(payload, "检索")]
    total = payload.get("total") if isinstance(payload, dict) else None
    result = {
        "query": args.q,
        "total": total if total is not None else len(rows),
        "page": args.page,
        "returned": len(rows),
        "results": rows,
        "page_profile": page_profile(rows),
        # 摘要就在检索结果里，这是免费初筛的前提：先读摘要挑出少数几篇，
        # 再对那几篇调 brief。不要拿到一串公开号就逐篇 brief 过去。
        "_note": "每行都带 abstract，先读摘要筛选，只对入围的少数几篇调 brief。",
    }
    if not rows and isinstance(total, int) and total > 0:
        result["_note"] = f"总命中 {total} 条，但第 {args.page} 页已经没有结果——页码超出范围，不是没有专利。"
    return with_ledger_summary(result, rows, f"search: {args.q}")


def do_brief(args):
    """单篇速览：一次调用拿回著录 + 权利要求 + 说明书全文。

    这三块是**打包**返回的，关掉任何一项都不省钱，只是少占上下文。
    真正另外收钱的只有法律事件流水（单独的接口）。
    """
    target = patent_number_of(args)
    whole = _load_patent_cache(args.patent)
    if whole is None:
        payload = request("/api/patent", target)
        if not isinstance(payload, dict) or not any(
                payload.get(k) for k in ("basic", "claims", "description")):
            die("整篇接口没有返回著录、权项或全文，结构认不出来。", detail=str(payload)[:300])
        basic = payload.get("basic")
        row = rows_of(basic)[0] if rows_of(basic) else (
            basic.get("patent") if isinstance(basic, dict) else None) or basic
        whole = {"basic": normalize(row) if isinstance(row, dict) else basic,
                 "claims": section_text(payload.get("claims"), "claims"),
                 "description": section_text(payload.get("description"), "description"),
                 "unavailable": payload.get("unavailable")}
        returned = whole["basic"].get("patent_number") if isinstance(whole["basic"], dict) else None
        if args.patent and not same_patent(args.patent, returned):
            # 实测：查一个不存在的号（ZZ999），服务端按全文检索取了第一条，
            # 返回一篇权项里碰巧出现 "ZZ999" 字样的美国洗衣机专利。
            # 模型编出来的公开号会因此「查到」一篇真实但毫不相干的专利——必须拦下。
            die(f"查的是 {args.patent}，返回的却是 {returned}，不是同一篇。"
                "这个公开号很可能不存在或写错了，不要使用返回的内容。",
                hint="核对公开号（国别代码 + 号码 + 类型码，如 CN109761224A）。"
                     "号码来自模型记忆而不是检索结果时，先用 search 确认它真的存在。")
        _save_patent_cache(args.patent, whole)
        reused = False
    else:
        reused = True

    result = {"patent_number": args.patent or f"(by id {args.id})", "basic": whole["basic"]}
    if not args.no_claims:
        result["claims"] = whole["claims"]
    # 说明书全文动辄上万字，默认不回给模型——**不是为了省钱**（它已经在
    # 这次调用里一起取回来了），是为了不把上下文占满。要逐段分析时才开，
    # 或者存文件后用 `read --find` 只取命中的段落。
    if args.fulltext:
        result["description"] = whole["description"]
    if whole.get("unavailable"):
        result["_unavailable"] = whole["unavailable"]
    if reused:
        result["_reused"] = "本任务里已经取过这篇，直接用本地缓存，没有调接口、没有扣费"
        result["_spent"] = "¥0.00"

    # 法律事件是另一个接口，确实另外收钱
    if args.legal:
        result["legal_events"] = request("/api/legal", target)

    mark_briefed(args.patent, result["basic"] if isinstance(result["basic"], dict) else None,
                 os.path.abspath(_json_out) if _json_out else None)
    return result


def _patent_cache_dir(task_id=None):
    # Task IDs can be loaded from a session file; never put them directly in paths.
    task = str(task_id or _task_id or "_")
    task_name = hashlib.sha256(task.encode("utf-8")).hexdigest()
    return os.path.join(os.path.dirname(_session_path()), "patents", task_name)


def _patent_cache_path(pn):
    number = validated_patent_number(pn)
    root = os.path.realpath(_patent_cache_dir())
    name = hashlib.sha256(number.encode("ascii")).hexdigest() + ".json"
    path = os.path.realpath(os.path.join(root, name))
    if os.path.commonpath([root, path]) != root:
        raise ValueError("缓存路径不在本任务目录内。")
    return path


def _load_patent_cache(pn):
    """Only reuse an in-task, identity-matched cache entry."""
    if not _task_id or not pn:
        return None
    try:
        with open(_patent_cache_path(pn), encoding="utf-8") as fh:
            data = json.load(fh)
        basic = data.get("basic") if isinstance(data, dict) else None
        if not isinstance(basic, dict):
            return None
        returned = basic.get("patent_number")
        if not returned or not same_patent(validated_patent_number(pn),
                                            validated_patent_number(returned)):
            return None
        return data
    except (OSError, ValueError, TypeError):
        return None


def _save_patent_cache(pn, whole):
    if not _task_id or not pn:
        return
    try:
        basic = whole.get("basic") if isinstance(whole, dict) else None
        if not isinstance(basic, dict) or not same_patent(
                validated_patent_number(pn), validated_patent_number(basic.get("patent_number"))):
            return
        path = _patent_cache_path(pn)
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        # Resolve again after directory creation to reject an out-of-tree symlink.
        path = _patent_cache_path(pn)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(whole, fh, ensure_ascii=False)
    except (OSError, ValueError, TypeError):
        pass


def section_text(section, field):
    """权项 / 全文从 {code, patent: {<field>: "..."}, success} 里剥出纯文本。

    上游文本里的换行是字面的反斜杠 n，顺手还原成真换行，模型读起来、
    read --find 切段落都方便。结构认不出来时原样返回，不丢数据。
    """
    text = section
    if isinstance(section, dict):
        inner = section.get("patent") if isinstance(section.get("patent"), dict) else section
        text = inner.get(field, section)
    if isinstance(text, str):
        return text.replace("\\n", "\n")
    return text


def do_similar(args):
    payload = request("/api/similar", patent_number_of(args))
    rows = [normalize(r) for r in require_rows(payload, "相似专利")]
    # 上游把锚点专利自己排在第一位。留着它占一个名额，还容易让模型把"找到了自己"
    # 当成一条命中写进报告，所以按公开号剔掉。
    anchor = (args.patent or "").replace(" ", "").upper()
    if anchor:
        rows = [r for r in rows if (r.get("patent_number") or "").replace(" ", "").upper() != anchor]
    rows = rows[: args.limit]
    result = {
        "patent_number": args.patent,
        "similar": rows,
        "_note": "语义相似，不是关键词匹配；用词完全不同但方案接近的专利靠它捞回来。",
    }
    return with_ledger_summary(result, rows, f"similar: {anchor or args.id}")


def do_citation(args):
    payload = request("/api/citation", patent_number_of(args))
    return {
        "patent_number": args.patent,
        "citation": payload,
        "_note": "被引次数常被当作技术影响力的参考，但受公开时间影响，新专利天然偏低。",
    }


def do_figure(args):
    """摘要附图存到本地文件。返回的是图片，不适合直接塞给模型看。"""
    data = request("/api/img", patent_number_of(args), raw=True)
    path = args.out or f"{_pn(args.patent) or 'patent'}.png"
    try:
        with open(path, "wb") as fh:
            fh.write(data)
    except OSError as exc:
        die(f"图片写入失败：{exc}")
    return {"patent_number": args.patent, "saved_to": os.path.abspath(path),
            "bytes": len(data),
            "_note": "写报告要配图时引用这个路径；图片内容本身不用读进上下文。"}


#: /api/ration 支持的统计维度。每个维度最多返回前 20 项，不返回长尾。
DIMENSIONS = {
    "applicant": "申请人", "inventor": "发明人",
    "applicationYear": "申请年份", "documentYear": "公开年份",
    "ipc": "IPC 完整分类", "ipc1": "IPC 部", "ipc2": "IPC 大类",
    "ipc3": "IPC 小类", "ipc4": "IPC 大组",
    "countryCode": "国家/地区", "province": "省份", "city": "城市",
    "legalStatus": "法律状态", "type": "专利类型", "loc": "外观设计分类",
}


def do_stats(args):
    """按维度做 Top 20 统计。管理层看布局通常先看这个，不是逐篇读专利。"""
    if args.dimension not in DIMENSIONS:
        die(f"未知维度 {args.dimension}。可选：" + "、".join(f"{k}({v})" for k, v in DIMENSIONS.items()))

    payload = request("/api/ration", {"q": args.q, "c": args.dimension, "ds": "cn" if args.scope == "cn" else "all"})

    # analysis_total 有时是数组、有时是 JSON 字符串，两种都得认
    items = payload.get("analysis_total", payload) if isinstance(payload, dict) else payload
    if isinstance(items, str):
        try:
            items = json.loads(items)
        except json.JSONDecodeError:
            items = []
    if not isinstance(items, list):
        items = []

    return {
        "query": args.q,
        "dimension": args.dimension,
        "dimension_name": DIMENSIONS[args.dimension],
        "items": items,
        # 一次只回一个维度，四个维度就是四次调用。这是本客户端最贵的一档，
        # 先想清楚要哪个维度再调，不要逐个维度扫一遍。
        "_note": "只返回前 20 项，不含长尾；申请人未做集团归一化，同一企业可能分散在多行。",
    }


def do_company(args):
    """企业专利画像。名称必须用工商全称，简称匹配不到。"""
    payload = request("/api/a/portrait", {"en": args.name})
    return {
        "company": args.name,
        "portrait": payload,
        "_note": "名称匹配严格，需用工商全称。集团旗下不同主体需分别查询后合并。",
    }


# ── 两道闸门：金额闸 + 检索次数闸 ────────────────────────────
#
# 金额闸只拦钱，不拦命令类型。
#
# 第一版做成了"档位 + 命令白名单"（快速摸底只准 search 5 次），实测是灾难：
# 用户只想查一篇专利，被拦下来问要不要升档；而且上一轮任务用完的额度
# 会把一个全新对话拦死。**预算是用来防失控的，不是用来决定能用哪些功能的。**
#
#   · 没设预算       → 不拦金额
#   · 设了预算       → 每次调用前估价，装得下就放行，装不下才拒
#   · 闲置超 1 小时  → 视为上一个任务已结束，自动失效，绝不影响新任务
#
# ── 检索次数闸（2026-09-22 新增）──
#
# 实测教训：一次任务跑了 **49 次检索**，其中 2 分钟内连着 22 次。
# 起因是语义扩展接口当时有 bug 返回 0 条，agent 只好用同义词硬凑，
# 换了二十几个检索式——每一次都在花钱，而且越换越偏。
#
# 金额闸拦不住这个：单次检索才 ¥0.10，跑到 49 次也才 ¥4.9，多数预算都装得下。
# **失控的形式是"次数"，不是"单价"**，所以要单独数次数。
#
# 这一条是照着竞品的做法补的：他们同样翻过车（752 次调用），结论是
# 「没有执行前预估、没有预算上限、**没有中途检查点**」，三样里我们缺的正是检查点。
#
# 阈值 15：快速摸底规定 4-5 式，标准档 8-10 式，完整档 10-12 式。
# 到 15 次说明要么方向不对、要么该换策略了，继续换同义词是空转。
# 不是硬禁止——拦下来让 agent 去问用户，用户点头后放宽即可。
BUDGET_IDLE_TIMEOUT = 3600
BILLED_COMMANDS = ("search", "stats", "company", "brief", "similar", "citation", "figure")
DEFAULT_SEARCH_LIMIT = 15


def _session_path():
    root = os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")
    return os.path.join(root, "budget.json")


def _load_session():
    try:
        with open(_session_path(), encoding="utf-8") as fh:
            data = json.load(fh)
    except Exception:
        return None
    # 闲置太久就当上一个任务已经结束——陈旧预算拦住新任务是最糟的体验
    if time.time() - float(data.get("touched_at", 0)) > BUDGET_IDLE_TIMEOUT:
        return None
    return data


def _save_session(data):
    try:
        path = _session_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data["touched_at"] = time.time()
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False)
    except Exception:
        pass


def estimate_cost(args):
    """这条命令大概要花多少。**只用于放行判断，不打印**，实际以 _spent 为准。"""
    command = args.command
    if command not in BILLED_COMMANDS:
        return 0.0
    if command == "brief":
        # 整篇一口价，权项和全文都包含在内；只有法律事件是另一次调用
        return PRICES["patent"] + (PRICES["legal"] if getattr(args, "legal", False) else 0.0)
    return PRICES.get(
        {"stats": "ration", "company": "portrait", "figure": "img"}.get(command, command),
        PRICES["search"])


def _counter_session():
    """拿到用于计数的会话；没有就现造一个（不设金额上限）。

    次数闸必须**默认生效**，所以不能依赖用户先跑 `budget start`——
    真实场景里 agent 基本不会主动设预算，而失控恰恰发生在没人设闸的时候。
    """
    session = _load_session()
    if session is None:
        session = {"limit": 0.0, "spent": 0.0, "search_calls": 0,
                   "search_limit": DEFAULT_SEARCH_LIMIT, "started_at": time.time()}
    if not session.get("task_id"):
        session["task_id"] = uuid.uuid4().hex[:12]
    return session


def ensure_task():
    """付费命令开跑前确定任务 id 并**立刻落盘**。

    幂等键和候选台账都靠它。必须在发请求之前存下来：要是请求超时、进程退出，
    下一次重跑得拿到同一个 id，才能生成同一个幂等键让服务端重放而不是再扣一次。
    """
    session = _counter_session()
    _save_session(session)
    # 上一个任务的整篇缓存不再有用，顺手清掉，免得越积越多
    root = os.path.dirname(_patent_cache_dir(session["task_id"]))
    try:
        for name in os.listdir(root):
            if name != os.path.basename(_patent_cache_dir(session["task_id"])):
                shutil.rmtree(os.path.join(root, name), ignore_errors=True)
    except OSError:
        pass
    return session["task_id"]


def enforce_search_budget(args):
    """检索次数闸。退出码 3 = 该停下来问人了（不是故障）。"""
    if args.command != "search":
        return
    session = _load_session()
    if not session:
        return
    used = int(session.get("search_calls", 0))
    limit = int(session.get("search_limit", DEFAULT_SEARCH_LIMIT))
    if limit <= 0 or used < limit:
        return
    die(f"本次任务已经跑了 {used} 次检索，达到上限 {limit} 次。",
        hint="**停下来，先把已有结果交给用户。** 连着换同义词重检说明方向可能不对，"
             "继续跑多半是空转还要花钱。给他三个选择："
             "A 换个思路继续（说清楚打算怎么改检索式）、"
             "B 就用现有候选收尾出报告、"
             "C 到此为止。"
             f"用户同意继续后，跑 `budget start --limit <金额> --searches <更大的数> --force` 放宽。",
        exit_code=3,
        searches_used=used, searches_limit=limit)


def enforce_budget(args):
    """装不下才拒。退出码 3 = 预算不够（不是故障）。"""
    enforce_search_budget(args)
    session = _load_session()
    if not session or args.command not in BILLED_COMMANDS:
        return
    limit = float(session.get("limit", 0))
    spent = float(session.get("spent", 0))
    need = estimate_cost(args)
    if limit <= 0 or spent + need <= limit + 1e-9:
        return
    die(f"本次任务预算 ¥{limit:.2f} 不够了：已用 ¥{spent:.2f}，这一步还要约 ¥{need:.2f}。",
        hint="停下来告诉用户还差多少、继续大概要花多少，让他决定："
             "追加预算（budget start --limit <更大的数>）、缩小范围收尾、或就此结束。"
             "不要自行降级参数硬凑。",
        exit_code=3)


def record_usage(command):
    """记一笔：花了多少钱、跑了第几次检索。

    花费用服务端回的实扣，不用估价——估价和账单对不上时，预算会在错误的时点拦人。
    次数则**无条件记**，哪怕服务端没回计费头、哪怕这次走的是免费额度：
    免费的检索一样会把上下文塞满、一样说明 agent 在空转，次数闸管的是这个。
    """
    session = _counter_session()
    if _billing["saw_header"]:
        session["spent"] = round(
            float(session.get("spent", 0)) + _billing["charged_cents"] / 100, 2)
    if command == "search":
        session["search_calls"] = int(session.get("search_calls", 0)) + 1
    _save_session(session)


def do_budget(args):
    if args.action == "start":
        existing = _load_session()
        # 只有金额上限才算"已有预算"；自动建出来记次数的那种不算，不该挡住用户设预算
        if existing and float(existing.get("limit", 0)) > 0 and not args.force:
            return {"error": True,
                    "message": f"已有进行中的预算：上限 ¥{existing['limit']:.2f}，已用 ¥{existing.get('spent', 0):.2f}。",
                    "hint": "同一个任务继续跑就不用重设；换任务了加 --force 重开，或先 budget clear。"}
        _save_session({"limit": float(args.limit), "spent": 0.0,
                       "search_calls": 0, "search_limit": int(args.searches),
                       "started_at": time.time(), "task_id": uuid.uuid4().hex[:12]})
        return {"limit": f"¥{float(args.limit):.2f}", "spent": "¥0.00",
                "search_limit": int(args.searches),
                "_note": "两道闸：总花费超上限会拦，检索次数超上限也会拦（退出码都是 3）。"
                         "不限制用哪些命令。闲置 1 小时自动失效。"}
    if args.action == "status":
        session = _load_session()
        if not session:
            return {"limit": None, "_note": "当前没有进行中的任务，两道闸都没有计数。"}
        used = int(session.get("search_calls", 0))
        cap = int(session.get("search_limit", DEFAULT_SEARCH_LIMIT))
        out = {"searches": f"{used}/{cap} 次"}
        money = float(session.get("limit", 0))
        if money > 0:
            out["limit"] = f"¥{money:.2f}"
            out["spent"] = f"¥{session.get('spent', 0):.2f}"
            out["remaining"] = f"¥{money - session.get('spent', 0):.2f}"
        else:
            out["limit"] = None
            out["spent"] = f"¥{session.get('spent', 0):.2f}"
            out["_note"] = "没设金额上限，只在数检索次数。"
        return out
    for path in (_session_path(), _ledger_path()):
        try:
            os.remove(path)
        except Exception:
            pass
    return {"limit": None, "_note": "预算和候选台账已清除，下一条命令算新任务。"}


def _export_candidates(items, out):
    """候选台账导出成 CSV（UTF-8 带 BOM，Excel 直接打开不乱码）。纯本地，不花钱。"""
    import csv
    path = os.path.abspath(out or "候选专利.csv")
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["公开号", "标题", "申请人", "申请日", "法律状态", "取舍", "理由", "出现次数", "已取全文"])
        status_text = {"keep": "入选", "exclude": "排除", "pending": "待定"}
        for pn, item in items.items():
            writer.writerow([pn, item.get("title") or "", item.get("applicant") or "", item.get("application_date") or "",
                             item.get("legal_status") or "", status_text.get(item.get("status"), item.get("status") or ""),
                             item.get("reason") or "", item.get("hits") or 0, "是" if item.get("briefed") else ""])
    return {"saved_to": path, "rows": len(items), "_note": "用 Excel 打开即可；不花钱。"}


def do_candidates(args):
    """候选台账：列出本任务出现过的专利，或标注取舍。不调接口、不花钱。"""
    session = _load_session()
    if not session or not session.get("task_id"):
        return {"candidates": [], "_note": "当前没有进行中的任务（闲置超过 1 小时或还没检索过）。"}
    ledger = _load_ledger(session["task_id"])
    items = ledger["items"]

    if args.action == "export":
        return _export_candidates(items, getattr(args, "out", None))

    if args.action == "mark":
        if args.status == "exclude" and not (args.reason or "").strip():
            die("排除要写理由（--reason），报告里要交代为什么不算。")
        missing = [p for p in args.patent if _pn(p) not in items]
        if missing:
            die("台账里没有这些专利，先检索或 brief 过才能标注：" + "、".join(missing))
        for p in args.patent:
            items[_pn(p)]["status"] = args.status
            items[_pn(p)]["reason"] = (args.reason or "").strip() or None
        _save_ledger(ledger)
        return {"marked": [_pn(p) for p in args.patent], "status": args.status}

    rows = [{"patent_number": pn, **item} for pn, item in items.items()
            if args.status in (None, "all") or item.get("status") == args.status]
    counts = {s: sum(1 for i in items.values() if i.get("status") == s) for s in CANDIDATE_STATUSES}
    counts["briefed"] = sum(1 for i in items.values() if i.get("briefed"))
    return {"total": len(items), "counts": counts, "candidates": rows,
            "_note": "hits 是这篇在几次检索 / 相似结果里出现过；briefed 表示本任务已经取过全文，"
                     "再 brief 会直接用本地缓存不扣费，brief_file 是上次存的结果文件。"}


# ── read：只读已保存的结果文件 ─────────────────────────────────
#
# 一份 brief --fulltext 动辄几万字，整份读进上下文既慢又挤掉前面的证据。
# read 从 --json-out 存下的文件里只取要的那部分：检索结果给索引、单篇给全行、
# 全文按关键词给出所在段落（带 [0012] 这种段落号，报告引用直接用）。
# 纯本地操作，不调接口，不计次数。

PARAGRAPH = re.compile(r"\[(\d{4,5})\]")


def _load_result_file(path):
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        die(f"文件不存在：{path}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        die("文件不是完整的 JSON，可能写到一半就中断了。不能当作 0 条，回去看生成它的那条命令。")
    if not isinstance(data, dict):
        die("文件内容不是本工具的结果对象。")
    if data.get("status") == "incomplete":
        die("这是一个未完成的占位文件：生成它的命令没跑完。不能当作 0 条，回去看那条命令的报错。")
    if data.get("error"):
        die("这个文件里存的是一次失败：" + str(data.get("message", "")),
            hint="失败不等于没有结果。按原报错处理，或如实告诉用户这一步没跑成。")
    return data


def _windows(text, keywords, width, limit):
    hits = []
    lowered = text.lower()
    for word in keywords:
        start = 0
        while len(hits) < limit:
            at = lowered.find(word.lower(), start)
            if at < 0:
                break
            lo, hi = max(0, at - width), min(len(text), at + len(word) + width)
            paragraphs = PARAGRAPH.findall(text, 0, at + 1)
            hits.append({"keyword": word, "at": at,
                         "paragraph": f"[{paragraphs[-1]}]" if paragraphs else None,
                         "text": text[lo:hi]})
            start = hi
    return hits


def do_read(args):
    data = _load_result_file(args.file)
    rows = data.get("results") if isinstance(data.get("results"), list) else data.get("similar")

    if isinstance(rows, list):
        if args.patent:
            for row in rows:
                if _pn(row.get("patent_number")) == _pn(args.patent):
                    return {"file": args.file, "patent": row}
            die(f"文件里没有 {args.patent}。")
        keep = ("patent_number", "title", "applicant", "application_date",
                "legal_status", "ipc", "seen_before")
        return {"file": args.file, "query": data.get("query") or data.get("patent_number"),
                "total": data.get("total"), "returned": len(rows),
                "index": [{k: row.get(k) for k in keep} for row in rows],
                "_note": "索引不含摘要。要看某篇的摘要用 read --patent <号>。"}

    if "basic" not in data:
        die("认不出这是哪种结果文件。read 只读 search / similar / brief 用 --json-out 存下的文件。")
    field = args.field or "claims"
    if field == "abstract":
        text = (data.get("basic") or {}).get("abstract") if isinstance(data.get("basic"), dict) else None
    else:
        text = data.get(field)
    if text is None:
        die(f"文件里没有 {field}。" + ("取说明书要在 brief 时加 --fulltext。" if field == "description" else ""))
    if not isinstance(text, str):
        text = json.dumps(text, ensure_ascii=False)

    out = {"file": args.file, "patent_number": data.get("patent_number"),
           "field": field, "total_chars": len(text)}
    if args.find:
        keywords = [w for w in re.split(r"[|｜]", args.find) if w.strip()]
        out["hits"] = _windows(text, keywords, args.window, args.max)
        if not out["hits"]:
            out["_note"] = "全文里没有这些词。没出现不等于没公开，可能是换了说法，换个词再找。"
    else:
        out["start"] = args.start
        out["text"] = text[args.start: args.start + args.length]
        if args.start + args.length < len(text):
            out["_note"] = f"还有后文，下一段用 --start {args.start + args.length}。"
    return out


def add_patent_target(parser):
    """按篇取数的公共参数。公开号直接可用，不需要先检索换 id。"""
    parser.add_argument("--patent", default=None, help="公开号，如 CN109761224A")
    parser.add_argument("--id", default=None, help="内部 id（可选）。手上没有就用 --patent，价钱一样")


def emit(result, json_out):
    """把结果交出去。

    默认打到 stdout；给了 --json-out 就由**本进程**把 UTF-8 字节写进文件，
    stdout 只留一行纯 ASCII 的确认。

    为什么要有这个开关：stdout 捕获的解码方式**不归我们管**。
    Windows PowerShell 5.1 按 `[Console]::OutputEncoding` 解码外部程序输出，
    默认是 GBK；中文 JSON 会被解成乱码，而且是**不可逆的**——非法字节直接被替换掉，
    事后再怎么转码都救不回来。更糟的是：

      · 每条命令常常是一个新的 PowerShell 进程，上一条里设的编码带不过来；
      · `Out-String` 默认按 80 列折行，会往 JSON 里插换行，这跟编码无关。

    让 Python 自己写文件就绕开了整条链路：文件里一定是 UTF-8，调用方直接读文件。
    确认行用 ensure_ascii=True，保证它在任何代码页的控制台上都不会坏。
    """
    if not json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    try:
        directory = os.path.dirname(os.path.abspath(json_out))
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
    except OSError as exc:
        die(f"结果写入失败：{exc}")
    receipt = {"saved_to": os.path.abspath(json_out)}
    # 数字类的摘要也放进回执：命中多少、带来几篇新候选，不读文件就能决定下一步
    for key in ("total", "returned", "new_candidates", "seen_candidates",
                "_spent", "_balance", "_free_remaining", "_replayed"):
        if isinstance(result, dict) and key in result:
            receipt[key] = result[key]
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


def main():
    parser = argparse.ArgumentParser(description="PatentMax 专利检索与统计分析")
    sub = parser.add_subparsers(dest="command", required=True)

    # 所有子命令共用的输出开关。放在 parents 里而不是顶层，
    # 是为了让它能写在子命令**后面**（`search --q ... --json-out x.json`），
    # 顶层参数必须写在子命令前面，那个顺序很容易记错。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json-out", default=None, metavar="PATH",
                        help="把完整 JSON 写到这个文件（UTF-8），stdout 只回一行确认。"
                             "**Windows 上一律用它**——控制台捕获会按 GBK 解码中文，乱码且不可逆")

    p = sub.add_parser("search", parents=[common], help="检索专利（结果自带摘要，用于免费初筛）")
    p.add_argument("--q", required=True,
                   help="检索式。支持 AND/OR/NOT 与括号，也支持字段式："
                        "documentNumber:CN106328959A、t:区块链、legalStatus:有效专利、"
                        "type:发明授权、applicationYear:[2024 TO 2024]")
    p.add_argument("--scope", default="all", choices=["all", "cn"], help="all 全球，cn 仅中国")
    p.add_argument("--page", type=int, default=1, help="1-100")
    p.add_argument("--size", type=int, default=20, help="1-50")
    p.add_argument("--sort", default=None,
                   choices=["relation", "applicationDate", "!applicationDate",
                            "documentDate", "!documentDate", "rank"],
                   help="排序：relation 相关度、applicationDate 申请日升序、"
                        "!applicationDate 申请日降序、documentDate/!documentDate 公开日、rank 综合")
    p.add_argument("--highlight", action="store_true", help="返回关键词高亮标记")
    p.set_defaults(func=do_search)

    p = sub.add_parser("stats", parents=[common], help="按维度做 Top 20 统计（本工具最贵的一档）")
    p.add_argument("--q", required=True, help="检索式，圈定统计范围")
    p.add_argument("--dimension", required=True, help="统计维度，见 --help 列表")
    p.add_argument("--scope", default="all", choices=["all", "cn"])
    p.set_defaults(func=do_stats)

    p = sub.add_parser("company", parents=[common], help="企业专利画像")
    p.add_argument("--name", required=True, help="企业工商全称，简称匹配不到")
    p.set_defaults(func=do_company)

    p = sub.add_parser("brief", parents=[common], help="单篇速览：著录+权项+全文，一次调用一口价")
    add_patent_target(p)
    p.add_argument("--fulltext", action="store_true",
                   help="把说明书全文也回给模型。**不额外计费**（已随本次调用取回），"
                        "但全文很长会占满上下文，只在需要逐段分析时开")
    p.add_argument("--no-claims", action="store_true",
                   help="不回权利要求书。**不省钱**，只是少占上下文")
    p.add_argument("--legal", action="store_true",
                   help="额外取法律事件流水（这项走单独接口，确实另外收费）。"
                        "只想知道有没有失效的话不用开——检索结果里已经带法律状态")
    p.set_defaults(func=do_brief)

    p = sub.add_parser("similar", parents=[common], help="相似专利（语义近似，不是关键词匹配）")
    add_patent_target(p)
    p.add_argument("--limit", type=int, default=10)
    p.set_defaults(func=do_similar)

    p = sub.add_parser("citation", parents=[common], help="引证关系")
    add_patent_target(p)
    p.set_defaults(func=do_citation)

    p = sub.add_parser("figure", parents=[common], help="下载摘要附图到本地文件")
    add_patent_target(p)
    p.add_argument("--out", default=None, help="保存路径，默认 <公开号>.png")
    p.set_defaults(func=do_figure)

    p = sub.add_parser("budget", parents=[common], help="设置/查看本次任务的花费上限")
    p.add_argument("action", choices=["start", "status", "clear"])
    p.add_argument("--limit", type=float, default=5.0, help="本次任务的花费上限（元），默认 5")
    p.add_argument("--searches", type=int, default=DEFAULT_SEARCH_LIMIT,
                   help=f"本次任务的检索次数上限，默认 {DEFAULT_SEARCH_LIMIT}。"
                        "用户同意继续深挖时才调大")
    p.add_argument("--force", action="store_true", help="覆盖已有的进行中预算")
    p.set_defaults(func=do_budget)

    p = sub.add_parser("candidates", parents=[common], help="候选台账：本任务出现过的专利（不花钱）")
    p.add_argument("action", choices=["list", "mark", "export"])
    p.add_argument("--out", default=None, help="export 时的文件名，默认 候选专利.csv")
    p.add_argument("--patent", nargs="+", default=[], help="mark 时要标注的公开号，可以多个")
    p.add_argument("--status", default=None, choices=list(CANDIDATE_STATUSES) + ["all"],
                   help="list 时按状态过滤；mark 时必填：keep 入选 / exclude 排除 / pending 待定")
    p.add_argument("--reason", default=None, help="标注理由；exclude 必须写")
    p.set_defaults(func=do_candidates)

    p = sub.add_parser("read", parents=[common], help="从已保存的结果文件里只取需要的部分（不花钱）")
    p.add_argument("--file", required=True, help="search / similar / brief 用 --json-out 存下的文件")
    p.add_argument("--patent", default=None, help="检索结果文件：只看这一篇的完整行（含摘要）")
    p.add_argument("--field", default=None, choices=["claims", "description", "abstract"],
                   help="brief 文件：读哪一块，默认 claims")
    p.add_argument("--find", default=None, help="brief 文件：按关键词定位段落，多个词用 | 分隔")
    p.add_argument("--window", type=int, default=200, help="--find 时命中词前后各取多少字")
    p.add_argument("--max", type=int, default=8, help="--find 时最多返回几处")
    p.add_argument("--start", type=int, default=0, help="不用 --find 时从第几个字开始")
    p.add_argument("--length", type=int, default=3000, help="不用 --find 时取多少字")
    p.set_defaults(func=do_read)

    args = parser.parse_args()
    if args.command == "candidates" and args.action == "mark" and (not args.patent or not args.status
                                                                   or args.status == "all"):
        die("mark 要同时给 --patent 和 --status（keep / exclude / pending）。")

    global _json_out, _task_id
    _json_out = getattr(args, "json_out", None)
    if _json_out and args.command == "read" and os.path.abspath(_json_out) == os.path.abspath(args.file):
        _json_out = None
        die("--json-out 不能和 --file 是同一个文件，会把要读的结果覆盖掉。")
    if _json_out:
        # 先占位：命令中途失败或被杀掉时，文件里留下的是「未完成」，
        # 而不是上一次同名文件的成功结果。
        try:
            directory = os.path.dirname(os.path.abspath(_json_out))
            os.makedirs(directory, exist_ok=True)
            with open(_json_out, "w", encoding="utf-8") as fh:
                json.dump({"status": "incomplete", "command": args.command,
                           "_meaning": "命令还没跑完或中途退出。不是 0 条结果。"},
                          fh, ensure_ascii=False)
        except OSError as exc:
            _json_out = None
            die(f"结果文件写不进去：{exc}")

    # 预算不够才拦，且拦在调接口之前——被拦的请求不该打上游，更不该计费
    enforce_budget(args)
    if args.command in BILLED_COMMANDS:
        _task_id = ensure_task()
    result = args.func(args)
    if args.command in BILLED_COMMANDS:
        record_usage(args.command)
    # 每个命令的输出都带上权威余额与本次实扣，模型不用自己跨调用累加。
    # 只在返回的是字典时附加——二进制/原始输出不动。
    if isinstance(result, dict):
        result.update(billing_summary())
    emit(result, getattr(args, "json_out", None))


if __name__ == "__main__":
    main()
