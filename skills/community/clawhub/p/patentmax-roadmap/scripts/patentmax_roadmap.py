#!/usr/bin/env python3
"""PatentMax 技术路线与专利布局分析客户端（v1.2.1）。

给 AI 用的命令行工具，走 POST /api/v1/reports 的 report_type=roadmap_layout。

**每条命令最多跑 30 秒就返回。** WorkBuddy 这类宿主前台跑命令时，要等命令结束才显示输出，
AI 中途也插不了话；一条命令阻塞几十分钟，用户就几十分钟什么都看不到，宿主还可能把命令掐掉。
所以 create 提交后只等 15 秒就先返回，之后用 wait 接着等，每次最多 30 秒：

    退出码 0   完成了（Word 报告已自动下载到提交时的目录）
    退出码 10  还在生成：把输出里的「[进度]」行告诉用户，再运行一次 wait
    退出码 2   输入有误（少必填项、文件读不了、方案太短），什么都没提交
    退出码 3   同样的任务已经在跑（这次没有重复提交、没有重复扣费），用输出里的 operation_id 接着 wait
    退出码 1   出错，message 是给用户看的中文说明，原样转述即可

输出：先打若干行「[进度] ……」，最后打一份 JSON。报告在服务端生成，命令结束、被杀、
对话关掉都不影响，任何时候 wait --operation-id 都能接着看。

Idempotency-Key 默认按请求内容算稳定指纹——同样的输入重跑 create，拿回的是同一个任务，不会重复扣费。

依赖：只用标准库，不需要 pip install。
"""

import argparse
import calendar
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

BASE_URL = os.environ.get("PATENTMAX_BASE_URL", "https://api.ip930.com").rstrip("/")
API_KEY = os.environ.get("PATENTMAX_API_KEY", "").strip()
TIMEOUT = 60

REPORT_TYPE = "roadmap_layout"
REPORT_NAME = "技术路线与专利布局报告"

EXIT_DONE, EXIT_ERROR, EXIT_INPUT, EXIT_BUSY, EXIT_RUNNING = 0, 1, 2, 3, 10
# 每条命令最多等多久就返回（秒）。刚提交那一次只等 15 秒，让「已开始」早点报出去
WAIT_SECONDS = max(15, int(os.environ.get("PATENTMAX_WAIT_SECONDS") or 30))
FIRST_WAIT_SECONDS = min(15, WAIT_SECONDS)
POLL_SECONDS = 10

ME = os.path.basename(__file__)


def cache_root():
    return os.environ.get("PATENTMAX_CACHE_DIR") or os.path.join(os.path.expanduser("~"), ".patentmax")


# ─────────────────────── 输出 ───────────────────────

def emit(payload, code=EXIT_DONE):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.exit(code)


def die(message, code=EXIT_ERROR, **extra):
    """出错：message 是给用户看的中文说明，AI 原样转述，不猜原因、不自己换写法重试。"""
    payload = {"error": True, "message": message}
    payload.update(extra)
    emit(payload, code)


def say(line):
    """进度行打到 stdout（不用 stderr：PowerShell 会把 stderr 当成报错显示）。"""
    print(line, flush=True)


def clock(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60}分{seconds % 60:02d}秒" if seconds >= 60 else f"{seconds}秒"


# ─────────────────────── 免费试用密钥 ───────────────────────
#
# 免密钥版（TRIAL_SOURCE 非空）：没设 PATENTMAX_API_KEY 时，第一次调用自动领一把免费试用密钥（不用注册），
# 存在 ~/.patentmax/ 下，之后接着用。规则由服务端定：每把累计 ¥40、30 天有效、只开通这个 Skill 用到的功能。
# 设了 PATENTMAX_API_KEY 就一律用它，不会去领试用。
# 密钥版（TRIAL_SOURCE 为空）：必须设 PATENTMAX_API_KEY，不领试用。
TRIAL_SOURCE = ""
TRIAL_GROUP = "roadmap"
TRIAL_REGISTER_URL = "https://api.ip930.com/features/api-platform"
KEY_FROM_TRIAL = False


def _trial_key_path():
    return os.path.join(cache_root(), f"trial-key-{TRIAL_GROUP}.json")


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


def _server_error(detail):
    """取服务端返回的 error.code / error.message。"""
    try:
        body = json.loads(detail)
    except ValueError:
        return "", ""
    error = body.get("error") if isinstance(body, dict) else None
    if not isinstance(error, dict):
        return "", ""
    return str(error.get("code") or ""), str(error.get("message") or "")


def _claim_trial_key():
    url = f"{BASE_URL}/api/v1/trial-keys"
    data = json.dumps({"source": TRIAL_SOURCE}).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        _, message = _server_error(exc.read().decode("utf-8", "replace"))
        die(message or f"领取免费试用失败（HTTP {exc.code}）。可以注册 PatentMax 创建正式密钥：{TRIAL_REGISTER_URL}",
            free_trial=True)
    except (urllib.error.URLError, TimeoutError, ConnectionError, ValueError) as exc:
        die(f"领取免费试用失败，网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试。",
            free_trial=True)
    data = payload.get("data") if isinstance(payload, dict) else None
    key = data.get("api_key") if isinstance(data, dict) else None
    if not key:
        die("领取免费试用失败：服务端没有返回密钥，请稍后重试。", free_trial=True)
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
    say(f"[PatentMax] 已自动领取免费试用：{data.get('note') or ''}")
    return key


def ensure_api_key():
    """有 PATENTMAX_API_KEY 用它；没有就用本地存的试用密钥，再没有就领一把。"""
    global API_KEY, KEY_FROM_TRIAL
    if API_KEY:
        return API_KEY
    if not TRIAL_SOURCE:
        die("还没有设置 PatentMax 密钥。到 https://api.ip930.com/features/api-platform 注册（新用户送 ¥50 体验额度）"
            "并创建密钥，设成环境变量 PATENTMAX_API_KEY=pm_live_xxx 后，再运行同一条命令。", EXIT_INPUT)
    API_KEY = _load_trial_key() or _claim_trial_key()
    KEY_FROM_TRIAL = True
    return API_KEY


# ─────────────────────── 请求与报错 ───────────────────────

# 服务端个别报错只给了英文代码，这里翻成用户看得懂的话
CODE_MESSAGES = {
    "DAILY_LIMIT_EXCEEDED": "今天提交的报告数已达上限，北京时间明天 0 点恢复。这次没有提交，未扣费。",
    "CONCURRENT_LIMIT_EXCEEDED": "同时在生成的任务已达上限，等前面的任务完成后再提交。这次没有提交，未扣费。",
    "API_BALANCE_INSUFFICIENT": f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    # 防重复提交的编号冲突：同一份内容之前由同一账户下的另一把密钥提交过，或手动给的编号对应的是别的内容
    "IDEMPOTENCY_KEY_OWNED_BY_DIFFERENT_API_KEY": "这份内容之前用同一账户的另一把密钥提交过。这次没有提交、未扣费。"
                                                  "去 https://api.ip930.com 控制台的调用记录里找原来那份；要重新生成，换个说法补充一句材料再提交。",
    "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST": "这个任务编号已经用于另一份内容。这次没有提交、未扣费。不要手动指定 --idempotency-key，让脚本自动生成即可。",
    "REPORT_NOT_READY": "报告还没有生成完，用 wait 接着等。",
}
HTTP_MESSAGES = {
    400: "参数不正确：必填 --subject（技术主题，至少 3 字）；业务约束每项最长 2000 字（公开时点、申请偏好、预算、保密边界为 500 字）。这次没有提交，未扣费。",
    401: "密钥无效或已撤销。请到 https://api.ip930.com 控制台重新创建。",
    402: f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    403: "这把密钥没有开通这项功能。",
    404: "找不到这个任务或报告，请确认编号完整。",
    409: "同样的任务已经在生成，这次没有重复提交、没有重复扣费。",
    429: "提交太频繁，请稍后再试。这次没有提交，未扣费。",
}


def _has_cjk(text):
    return bool(re.search(r"[一-鿿]", text or ""))


def _open(path, method="GET", body=None, headers=None):
    ensure_api_key()
    url = path if path.startswith("http") else f"{BASE_URL}{path}"
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {API_KEY}")
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    return urllib.request.urlopen(req, timeout=TIMEOUT)


def request(path, method="GET", body=None, headers=None, raw=False):
    try:
        with _open(path, method, body, headers) as response:
            payload = response.read()
            return payload if raw else json.loads(payload.decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:600]
        code, message = _server_error(detail)
        if KEY_FROM_TRIAL and exc.code == 401:
            # 试用密钥过期或被停用：清掉本地缓存，下次运行自动领新的
            try:
                os.remove(_trial_key_path())
            except OSError:
                pass
            die("免费试用已过期或失效。重新运行同一条命令会自动领取新的试用；"
                f"也可以注册 PatentMax 换正式密钥：{TRIAL_REGISTER_URL}", free_trial=True)
        # 优先用服务端的中文说明（里面写着下一步怎么办）；只有英文代码时用本地翻译
        text = (message if _has_cjk(message) else "") \
            or CODE_MESSAGES.get(message) or CODE_MESSAGES.get(code) \
            or HTTP_MESSAGES.get(exc.code) \
            or f"PatentMax 服务暂时不可用（HTTP {exc.code}），请稍后重试。"
        extra = {"free_trial": True} if "免费试用" in text else {}
        busy = exc.code == 409 and not code.startswith("IDEMPOTENCY_") and not message.startswith("IDEMPOTENCY_")
        die(text, EXIT_BUSY if busy else EXIT_ERROR, http_status=exc.code, **extra)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        die(f"网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试；"
            "已提交的任务不受影响，稍后用 wait 接着看。")
    except json.JSONDecodeError:
        die("PatentMax 返回的内容不完整，请稍后重试。")


def try_download(path):
    """下载文件；失败不退出，返回 None（报告受限时可能没有 Word）。"""
    try:
        with _open(path) as response:
            return response.read()
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ConnectionError):
        return None


def unwrap(payload):
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def fingerprint(body):
    """同样的内容 + 同一把密钥 → 同一个编号：重跑拿回原任务，不重复扣费。

    带上密钥本身的指纹（不是密钥原文）：同一账户换了密钥再交同样的内容时，服务端会因为「编号属于另一把密钥」拒绝，
    用户卡在那里拿不到任务（2026-10-14 实测）。按密钥区分后，换密钥就是一个新任务。
    """
    ensure_api_key()
    raw = json.dumps(body, ensure_ascii=False, sort_keys=True) + "|" + hashlib.sha256(API_KEY.encode("utf-8")).hexdigest()[:12]
    return "pmr-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


def read_docx(path, label):
    """标准库取 .docx 正文（它就是个 zip，正文在 word/document.xml）。写好的交底书、初稿可以直接拿来用。"""
    import zipfile
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml").decode("utf-8", "replace")
    except (zipfile.BadZipFile, KeyError, OSError) as exc:
        die(f"读不了这个 Word 文件：{path}（{exc}）。只支持 .docx，老的 .doc 请先另存为 .docx。", EXIT_INPUT)
    xml = re.sub(r"</w:tc>", " | ", xml)
    xml = re.sub(r"</w:p>|</w:tr>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    xml = re.sub(r"<w:br[^>]*/>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", xml)
    for entity, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'"), ("&amp;", "&")):
        text = text.replace(entity, char)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        die(f"{label}文件是空的：{path}", EXIT_INPUT)
    return text


def read_text_file(path, label):
    if not os.path.isfile(path):
        die(f"找不到{label}文件：{path}", EXIT_INPUT)
    if path.lower().endswith(".docx"):
        return read_docx(path, label)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read().strip()
    except UnicodeDecodeError:
        die(f"{label}文件不是 UTF-8 文本：{path}。只支持 .md / .txt / .docx。", EXIT_INPUT)
    except OSError as exc:
        die(f"读不到{label}文件：{path}（{exc}）", EXIT_INPUT)
    if not text:
        die(f"{label}文件是空的：{path}", EXIT_INPUT)
    return text


def split_list(value):
    return [x.strip() for x in value.replace("，", ",").replace("、", ",").split(",") if x.strip()] if value else []


# ─────────────────────── 本地任务记录 ───────────────────────
#
# 记下每个任务从哪个目录提交、几点提交，wait 完成时把 Word 存回那个目录，
# 「已用时」也从提交时刻算起，命令断了再接上不会从 0 重新数。

def _task_path(operation):
    return os.path.join(cache_root(), "tasks", re.sub(r"[^\w.-]", "_", operation) + ".json")


def save_task(operation, **fields):
    record = load_task(operation)
    record.update({k: v for k, v in fields.items() if v is not None})
    try:
        os.makedirs(os.path.dirname(_task_path(operation)), exist_ok=True)
        with open(_task_path(operation), "w", encoding="utf-8") as fh:
            json.dump(record, fh, ensure_ascii=False, indent=2)
    except OSError:
        pass
    return record


def load_task(operation):
    try:
        with open(_task_path(operation), encoding="utf-8") as fh:
            saved = json.load(fh)
            return saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        return {}


# ─────────────────────── 本技能的输入 ───────────────────────

#: roadmap_context 的十个可选字段。每项都能留空，填了布局建议才贴合实际约束。
CONTEXT_FIELDS = {
    "future_plan": "未来规划：接下来一到三年打算做什么",
    "existing_assets": "现有资产：已有的专利、产线、技术积累",
    "own_advantages": "自身优势：相对竞争对手强在哪",
    "known_risks": "已知风险：担心撞上谁、哪些方向有雷",
    "evidence_data": "证据数据：实验数据、参数、验证结果",
    "disclosure_timing": "公开时点：什么时候要发布、参展、投标",
    "filing_preference": "申请偏好：发明为主还是实用新型、国内还是 PCT",
    "budget_and_volume": "预算与数量：今年打算申请几件、预算多少",
    "confidentiality_limits": "保密边界：哪些内容不能写进公开文件",
    "excluded_directions": "排除方向：明确不做的领域",
}

QUALITY_HINT = {
    "qualified": "报告通过质量校验，可作为布局决策依据。",
    "qualified_degraded": "报告已生成但存在数据短板，布局建议要保守使用，交付时须说明限制；这种情况本次费用已全额退回。",
    "review_required": "报告需要人工复核，不要直接当作布局方案交给决策层。",
}


def build_context(args):
    """roadmap_context 支持两种给法：--context-file 给 JSON，或逐个命令行参数。"""
    context = {}
    if args.context_file:
        raw = read_text_file(args.context_file, "业务约束")
        try:
            loaded = json.loads(raw)
        except ValueError as exc:
            die(f"业务约束文件不是合法的 JSON：{exc}", EXIT_INPUT)
        if not isinstance(loaded, dict):
            die("业务约束文件必须是一个 JSON 对象，字段见 fields 子命令。", EXIT_INPUT)
        unknown = [k for k in loaded if k not in CONTEXT_FIELDS]
        if unknown:
            die(f"业务约束里有不认识的字段：{', '.join(unknown)}。可用字段见 fields 子命令。", EXIT_INPUT)
        context.update({k: str(v).strip() for k, v in loaded.items() if str(v).strip()})
    for key in CONTEXT_FIELDS:
        value = getattr(args, key, None)
        if value and value.strip():
            context[key] = value.strip()
    return context


def do_create(args):
    subject = (args.subject or "").strip()
    if len(subject) < 3:
        die("缺少必填项 --subject（技术主题），只写技术名称，至少 3 个字，例如「钠离子电池正极材料」。", EXIT_INPUT)
    if not args.yes:
        die("专利布局规划是付费任务，取得用户同意后加 --yes 再运行。", EXIT_INPUT)
    materials = (read_text_file(args.materials_file, "素材") if args.materials_file else (args.materials or "").strip()) \
        or f"技术主题：{subject}"
    objective = (args.objective or "").strip() or "生成技术路线分析正式报告"
    context = build_context(args)
    body = {
        "report_type": REPORT_TYPE,
        "input": {
            "subject": subject,
            "materials": materials,
            "objective": objective,
            "target_markets": split_list(args.markets),
            "competitors": split_list(args.competitors),
        },
    }
    if context:
        body["input"]["roadmap_context"] = context
    submit(body, args, subject)


def do_fields(args):
    emit({"roadmap_context_fields": CONTEXT_FIELDS,
          "note": "写进一个 JSON 文件用 --context-file 传，或用同名命令行参数逐个给。全部可选，但填得越全建议越贴合实际。"})


def summarize(payload):
    """要讲的几项：标题、核心结论、建议、报告章节。完整结果另存文件。"""
    result = payload.get("result") or {}
    summary = result.get("executiveSummary") or result.get("executive_summary") or ""
    return {
        "title": result.get("title"),
        "executive_summary": summary[:800],
        "recommendations": [str(r)[:200] for r in (result.get("recommendations") or [])[:6]],
        "report_sections": [s.get("title") for s in result.get("sections") or []
                            if isinstance(s, dict) and s.get("title")][:12],
    }


# ─────────────────────────── 等待 ───────────────────────────

STATUS_TEXT = {"queued": "排队中", "accepting": "排队中", "running": "生成中"}
DONE_TEXT = {"succeeded": "已完成", "failed": "没有完成，预扣的费用已全额退回", "cancelled": "已取消，预扣的费用已全额退回"}


def progress_line(data, started_at):
    """「[进度 X%] 阶段，已用时 N」。服务端给了分步进度就带百分比，没给就只报状态和已用时，不编百分比。"""
    status = (data.get("status") or "").lower()
    if status in DONE_TEXT:
        return f"[进度] {DONE_TEXT[status]}"
    stage = str(data.get("stage") or "")
    percent = data.get("progress")
    elapsed = clock(time.time() - started_at)
    label = STATUS_TEXT.get(status, status or "处理中")
    detailed = _has_cjk(stage) and stage not in ("正在接收任务",)
    if detailed and isinstance(percent, (int, float)) and 0 < percent < 100:
        return f"[进度 {int(percent)}%] {stage}，已用时 {elapsed}"
    if status in ("queued", "accepting"):
        return f"[进度] 排队中，已等待 {elapsed}"
    return f"[进度] {stage if detailed else label}，已用时 {elapsed}"


def started_at_of(operation, data):
    record = load_task(operation)
    if record.get("started_at"):
        return float(record["started_at"])
    created = str(data.get("created_at") or "")
    try:
        return calendar.timegm(time.strptime(created[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return time.time()


def wait_for(operation, seconds, out_dir=None):
    """最多等 seconds 秒：完成就交付（退出码 0），还没完就报进度（退出码 10）。"""
    deadline = time.time() + seconds
    last_stage = None
    while True:
        data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(operation)}"))
        status = (data.get("status") or "").lower()
        if status == "succeeded":
            emit(deliver(operation, data, out_dir), EXIT_DONE)
        if status in ("failed", "cancelled"):
            error = data.get("error") or {}
            message = error.get("message") if _has_cjk(error.get("message")) else ""
            die(message or ("任务已取消。" if status == "cancelled" else f"{REPORT_NAME}没有生成成功。"),
                EXIT_ERROR, operation_id=operation, status=status,
                refund="预扣的费用已全额退回。")
        line = progress_line(data, started_at_of(operation, data))
        stage = line.split("，")[0]
        ending = time.time() + POLL_SECONDS > deadline
        # 一条命令只在返回前报一行最新进度；中途换了阶段再多报一行。不要每次轮询都刷一行
        if ending or (last_stage is not None and stage != last_stage):
            say(line)
        last_stage = stage
        if ending:
            emit({
                "status": "running",
                "operation_id": operation,
                "next": f"把上面的进度告诉用户，然后运行：python {ME} wait --operation-id {operation}",
            }, EXIT_RUNNING)
        time.sleep(POLL_SECONDS)


def safe_name(text):
    return re.sub(r'[\\/:*?"<>|\s]+', "", str(text))[:40] or REPORT_NAME


def deliver(operation, data, out_dir=None):
    """完成：Word 报告自动存到提交时的目录；完整结果存成文件，只返回要讲的几项。"""
    report_id = data.get("report_id")
    record = load_task(operation)
    target = out_dir or record.get("out_dir") or os.getcwd()
    payload = unwrap(request(f"/api/v1/reports/{urllib.parse.quote(report_id)}")) or {}
    quality = payload.get("quality_status") or data.get("quality_status")
    out = {
        "status": "succeeded",
        "operation_id": operation,
        "report_id": report_id,
        "elapsed": clock(time.time() - started_at_of(operation, data)),
        "amount_charged_yuan": data.get("amount_charged_yuan"),
        "quality_status": quality,
        "quality_hint": QUALITY_HINT.get(quality, ""),
    }
    summary = summarize(payload)
    stem = safe_name(summary.get("title") or record.get("title") or data.get("title") or REPORT_NAME)

    os.makedirs(target, exist_ok=True)
    files = {}
    docx = try_download(f"/api/v1/reports/{urllib.parse.quote(report_id)}/files/report.docx")
    if docx:
        path = os.path.abspath(os.path.join(target, f"{REPORT_NAME}_{stem}.docx"))
        with open(path, "wb") as handle:
            handle.write(docx)
        files[REPORT_NAME] = path
    else:
        out["docx_note"] = "这次没有生成 Word 报告，结论以下面的摘要和完整结果为准。"
    full = os.path.abspath(os.path.join(target, f"{REPORT_NAME}_{stem}_结果.json"))
    with open(full, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
    files["完整结果"] = full
    out["files"] = files
    out["summary"] = summary
    return out


# ─────────────────────────── 子命令 ───────────────────────────

def submit(body, args, title=None):
    key = args.idempotency_key or fingerprint(body)
    created = unwrap(request("/api/v1/reports", method="POST", body=body,
                             headers={"Idempotency-Key": key}))
    operation = created.get("operation_id")
    if not operation:
        die("PatentMax 没有返回任务编号，请稍后重试。")
    record = load_task(operation)
    resumed = bool(record)
    save_task(operation, started_at=record.get("started_at") or time.time(),
              out_dir=os.path.abspath(args.out_dir or os.getcwd()), title=title or created.get("title"))
    if not resumed:
        say(f"[进度] 已开始生成{REPORT_NAME}（预计费用 ¥{created.get('price_yuan')}）")
    else:
        say("[进度] 同样的内容已经提交过，这次没有重复提交、没有重复扣费，接着看原来的任务")
    if args.wait:
        # 老用法：一直等到出结果。宿主前台跑命令时用户全程看不到进度，SKILL.md 里不再用
        wait_for(operation, args.timeout, args.out_dir)
    wait_for(operation, FIRST_WAIT_SECONDS, args.out_dir)


def do_wait(args):
    wait_for(args.operation_id, WAIT_SECONDS, args.out_dir)


def do_status(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}"))
    emit({
        "operation_id": args.operation_id,
        "report_id": data.get("report_id"),
        "status": (data.get("status") or "").lower(),
        "progress": progress_line(data, started_at_of(args.operation_id, data)),
    })


def do_download(args):
    payload = request(f"/api/v1/reports/{urllib.parse.quote(args.report_id)}/files/report.docx", raw=True)
    out = args.out or f"{REPORT_NAME}.docx"
    with open(out, "wb") as handle:
        handle.write(payload)
    emit({"saved": os.path.abspath(out), "bytes": len(payload)})


def do_cancel(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/cancel",
                          method="POST"))
    emit({"operation_id": args.operation_id, "status": data.get("status"),
          "refund": "取消后预扣的费用全额退回。"})


def main():
    parser = argparse.ArgumentParser(description="PatentMax 技术路线与专利布局分析")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="提交技术路线与专利布局分析任务（约 15 秒后返回，之后用 wait 接着等）")
    p.add_argument("--subject", default=None, help="【必填】技术主题，只写技术名称，3-255 字。例：钠离子电池正极材料")
    p.add_argument("--materials", default=None, help="可选：技术方案与背景")
    p.add_argument("--materials-file", dest="materials_file", default=None, help="可选：素材文件路径（UTF-8）")
    p.add_argument("--objective", default=None, help="可选：这份报告要支持什么决策")
    p.add_argument("--markets", default=None, help="可选：目标市场，逗号分隔。例：CN,US,EP")
    p.add_argument("--competitors", default=None, help="可选：对标企业，逗号分隔，用全称")
    p.add_argument("--context-file", dest="context_file", default=None, help="可选：业务约束 JSON 文件，字段见 fields 子命令")
    for key, desc in CONTEXT_FIELDS.items():
        p.add_argument(f"--{key.replace('_', '-')}", dest=key, default=None, help=desc)
    p.add_argument("--force", action="store_true", help=argparse.SUPPRESS)  # 旧参数，保留以兼容
    p.add_argument("--out-dir", dest="out_dir", default=None, help="完成后 Word 存到哪个目录，默认当前目录")
    p.add_argument("--idempotency-key", dest="idempotency_key", default=None, help="幂等键，默认按请求内容自动生成")
    p.add_argument("--wait", action="store_true", help="（旧用法）一直等到出结果，不推荐")
    p.add_argument("--timeout", type=int, default=5400, help="配合 --wait 的等待上限（秒）")
    p.add_argument("--quiet", action="store_true", help=argparse.SUPPRESS)  # 旧参数，保留以兼容
    p.add_argument("--yes", action="store_true", help="确认扣费")
    p.set_defaults(func=do_create)

    p = sub.add_parser("wait", help="接着等：最多 30 秒，完成就自动下载 Word")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.set_defaults(func=do_wait)

    p = sub.add_parser("fields", help="列出业务约束的十个字段（不花钱）")
    p.set_defaults(func=do_fields)

    p = sub.add_parser("status", help="只查一次任务状态")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_status)

    p = sub.add_parser("download", help="重新下载 Word 报告（wait 完成时已自动下载过）")
    p.add_argument("--report-id", dest="report_id", required=True)
    p.add_argument("--out", default=None)
    p.set_defaults(func=do_download)

    p = sub.add_parser("cancel", help="取消任务，预扣费用全额退回")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
