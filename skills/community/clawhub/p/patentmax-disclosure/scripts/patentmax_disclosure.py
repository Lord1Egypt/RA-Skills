#!/usr/bin/env python3
"""PatentMax 技术交底书客户端（v1.1.0）。

给 AI 用的命令行工具。走 POST /api/v1/reports 的两种报告：

    idea_upgrade          只有一个想法时，先出几个可申请的升级方向
    technical_disclosure  材料够了，直接出技术交底书 Word（外加一份核对说明）

**每条命令最多跑 30 秒就返回。** WorkBuddy 这类宿主前台跑命令时，要等命令结束才显示输出，
AI 中途也插不了话；一条命令阻塞十几分钟，用户就十几分钟什么都看不到，宿主还可能把命令掐掉。
所以 create / ideas 提交后只等 15 秒就先返回，之后用 wait 接着等，每次最多 30 秒：

    退出码 0   这一步有结果了（wait 完成时已自动下载好 Word）
    退出码 10  还在生成：把输出里的「[进度]」行告诉用户，再运行一次 wait
    退出码 2   输入有误（材料太短、文件读不了、少参数），什么都没提交
    退出码 3   同样的任务已经在跑（这次没有重复提交、没有重复扣费），用输出里的 operation_id 接着 wait
    退出码 1   出错，message 是给用户看的中文说明，原样转述即可

输出：先打若干行「[进度] ……」，最后打一份 JSON。生成在服务端跑，命令结束、被杀、
对话关掉都不影响，任何时候 wait --operation-id 都能接着看。

其余几件事：

1. **Idempotency-Key 必填**。默认按请求内容算稳定指纹——同样的材料重跑同一条 create，
   拿回的是同一个任务，不会重复扣费。
2. **材料护栏**。太短的材料直接拦下来，别花钱买一份全是推断的技术交底书。
3. **多文件拼装**。--file 可以给多次，.md / .txt 直接读，.docx 用标准库解压取正文。
4. **方向接力**。--from-ideas 直接取上一步创新升级的某个方向当材料。

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
import zipfile

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

BASE_URL = os.environ.get("PATENTMAX_BASE_URL", "https://api.ip930.com").rstrip("/")
API_KEY = os.environ.get("PATENTMAX_API_KEY", "").strip()
TIMEOUT = 60

DOC_NAME = "技术交底书"
NOTES_NAME = "核对说明"

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
# 存在 ~/.patentmax/ 下，之后接着用。规则由服务端定：每把累计 ¥40、30 天有效、
# 只开通这个 Skill 用到的功能。用完或过期后，注册 PatentMax 换正式密钥即可。
# 设了 PATENTMAX_API_KEY 就一律用它，不会去领试用。
# 密钥版（TRIAL_SOURCE 为空）：必须设 PATENTMAX_API_KEY，不领试用。
TRIAL_SOURCE = ""
TRIAL_GROUP = "disclosure"
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
}
HTTP_MESSAGES = {
    400: "参数不正确：材料要在 20 字到 10 万字之间，方向数只能是 1 到 5。这次没有提交，未扣费。",
    401: "密钥无效或已撤销。请到 https://api.ip930.com 控制台重新创建。",
    402: f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    403: "这把密钥没有开通这项功能。",
    404: "找不到这个任务或文件，请确认编号完整。",
    409: "同样的任务已经在生成，这次没有重复提交、没有重复扣费。",
    429: "提交太频繁，请稍后再试。这次没有提交，未扣费。",
}


def _has_cjk(text):
    return bool(re.search(r"[一-鿿]", text or ""))


def request(path, method="GET", body=None, headers=None, raw=False):
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

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
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
    return "pmd-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


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


# ─────────────────────────── 材料 ───────────────────────────

def read_docx(path):
    """标准库取 .docx 正文：它就是个 zip，正文在 word/document.xml。

    表格按行拼成「单元格 | 单元格」，段落之间空行。图片、公式取不到，
    这一点要在 SKILL.md 里交代：附图内容得用文字补。
    """
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
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def read_pptx(path):
    """标准库取 .pptx 里的文字：每页一段，按页码顺序。图片和图表取不到，要用文字补。"""
    try:
        with zipfile.ZipFile(path) as archive:
            names = [n for n in archive.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
            names.sort(key=lambda n: int(re.search(r"(\d+)", n.rsplit("/", 1)[-1]).group(1)))
            pages = []
            for i, name in enumerate(names, 1):
                xml = archive.read(name).decode("utf-8", "replace")
                xml = re.sub(r"</a:p>", "\n", xml)
                text = re.sub(r"<[^>]+>", "", xml)
                for entity, char in (("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&apos;", "'"), ("&amp;", "&")):
                    text = text.replace(entity, char)
                text = re.sub(r"\n{2,}", "\n", text).strip()
                if text:
                    pages.append(f"[第 {i} 页]\n{text}")
    except (zipfile.BadZipFile, KeyError, OSError) as exc:
        die(f"读不了这个 PPT 文件：{path}（{exc}）。只支持 .pptx，老的 .ppt 请先另存为 .pptx。", EXIT_INPUT)
    return "\n\n".join(pages)


def read_file(path):
    if not os.path.isfile(path):
        die(f"找不到文件：{path}", EXIT_INPUT)
    if path.lower().endswith(".docx"):
        return read_docx(path)
    if path.lower().endswith(".pptx"):
        return read_pptx(path)
    if path.lower().endswith((".pdf", ".doc", ".ppt", ".xls", ".xlsx")):
        die(f"不支持直接读 {os.path.splitext(path)[1]}：{path}", EXIT_INPUT,
            hint="由你读完后把要点写进 --supplement，或先转成 .md / .txt / .docx。")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except UnicodeDecodeError:
        die(f"{path} 不是 UTF-8 文本。只支持 .md / .txt / .docx。", EXIT_INPUT)


def collect_materials(files, text):
    """把多份材料拼成一段。每份前面标出处，服务端检查材料冲突时要靠它指认来源。"""
    parts = []
    for path in files or []:
        body = read_file(path)
        if body:
            parts.append(f"【材料：{os.path.basename(path)}】\n{body}")
    if text and text.strip():
        parts.append(f"【补充说明】\n{text.strip()}" if parts else text.strip())
    return "\n\n".join(parts)


def direction_to_material(direction, idea_text=None):
    """把创新升级的一个方向转成交底材料。字段为空就跳过，不写「无」占位。"""
    lines = []
    if idea_text:
        lines.append(f"【原始想法】\n{idea_text.strip()}")
    head = direction.get("title") or direction.get("direction_label") or "选定方向"
    lines.append(f"【选定方向】{head}")
    for key, label in (
        ("plain_summary", "方向概述"),
        ("technical_field", "技术领域"),
        ("background", "背景技术"),
        ("triz_contradiction", "要解决的技术矛盾"),
        ("core_idea", "核心技术方案"),
        ("existing_tech_description", "与现有技术的关系"),
    ):
        value = direction.get(key)
        if value:
            lines.append(f"【{label}】\n{value}")
    points = [p for p in direction.get("innovation_points") or [] if p]
    if points:
        lines.append("【创新点】\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(points, 1)))
    return "\n\n".join(lines)


MAX_CHARS = 100_000
# 低于这个长度，服务端会发起提问，而 API 模式下没人回答，全部按推荐值继续
RICH_CHARS = 800
MIN_DISCLOSURE_CHARS = 200
MIN_IDEA_CHARS = 40


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
            die(error.get("message") or ("任务已取消。" if status == "cancelled" else "任务没有完成。"),
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


def deliver(operation, data, out_dir=None):
    """完成：交底书类自动把两份 Word 存到提交时的目录；结果摘要只给要讲的几项，完整结果存成文件。"""
    report_id = data.get("report_id")
    record = load_task(operation)
    target = out_dir or record.get("out_dir") or os.getcwd()
    result = (unwrap(request(f"/api/v1/reports/{urllib.parse.quote(report_id)}")) or {}).get("result") or {}
    out = {
        "status": "succeeded",
        "operation_id": operation,
        "report_id": report_id,
        "report_type": data.get("report_type"),
        "elapsed": clock(time.time() - started_at_of(operation, data)),
        "amount_charged_yuan": data.get("amount_charged_yuan"),
    }

    if data.get("report_type") == "idea_upgrade":
        out["directions"] = [{
            "direction": d.get("direction_index"),
            "title": d.get("title"),
            "summary": d.get("plain_summary"),
            "innovation_points": d.get("innovation_points"),
            "existing_tech": d.get("existing_tech_description"),
            "scores": d.get("scores"),
        } for d in result.get("directions") or []]
        out["next"] = f"把方向列给用户挑；挑定后运行：python {ME} create --from-ideas {report_id} --direction <序号> --yes"
        return out

    os.makedirs(target, exist_ok=True)
    stem = safe_name(result.get("title") or record.get("title") or DOC_NAME)
    files = {}
    for kind, name in (("disclosure", f"{DOC_NAME}_{stem}.docx"), ("notes", f"{NOTES_NAME}_{stem}.docx")):
        path = f"/api/v1/reports/{urllib.parse.quote(report_id)}/files/report.docx"
        if kind == "notes":
            path += "?kind=notes"
        payload = request(path, raw=True)
        saved = unique_path(os.path.join(target, name))
        with open(saved, "wb") as handle:
            handle.write(payload)
        files[kind] = saved
    full = unique_path(os.path.join(target, f"{DOC_NAME}_{stem}_结果.json"))
    with open(full, "w", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)

    figures = result.get("figures") or []
    rows = (result.get("novelty") or {}).get("rows") or []
    out.update({
        "title": result.get("title"),
        "files": {DOC_NAME: files["disclosure"], NOTES_NAME: files["notes"], "完整结果": full},
        "pending_count": result.get("pending_count"),
        "missing_sections": result.get("missing_sections") or [],
        "figures": {"total": len(figures), "auto": sum(1 for f in figures if f.get("auto")),
                    "need_drawing": [f.get("name") for f in figures if not f.get("auto")]},
        "novelty": {"features": len(rows), "found": sum(1 for r in rows if r.get("found")),
                    "hits": sorted({h.get("doc") for r in rows for h in r.get("hits") or [] if h.get("doc")})[:10]},
        "conflicts": len(result.get("conflicts") or []),
    })
    return out


def unique_path(path):
    """同名文件已存在时在文件名后加生成时间，新稿不覆盖旧稿（改了材料再出一版时两版都在）。"""
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    stamped = f"{base}_{time.strftime('%Y%m%d-%H%M')}{ext}"
    n = 2
    while os.path.exists(stamped):
        stamped = f"{base}_{time.strftime('%Y%m%d-%H%M')}_{n}{ext}"
        n += 1
    return stamped


def safe_name(text):
    return re.sub(r'[\\/:*?"<>|\s]+', "", str(text))[:40] or DOC_NAME


# ─────────────────────────── 子命令 ───────────────────────────

def submit(body, args, title=None):
    key = args.idempotency_key or fingerprint(body)
    created = unwrap(request("/api/v1/reports", method="POST", body=body,
                             headers={"Idempotency-Key": key}))
    operation = created.get("operation_id")
    if not operation:
        die("PatentMax 没有返回任务编号，请稍后重试。", raw=created)
    record = load_task(operation)
    resumed = bool(record)
    save_task(operation, started_at=record.get("started_at") or time.time(),
              out_dir=os.path.abspath(args.out_dir or os.getcwd()),
              report_type=body["report_type"], title=title)
    if not resumed:
        what = "方向分析" if body["report_type"] == "idea_upgrade" else DOC_NAME
        say(f"[进度] 已开始生成{what}（预计费用 ¥{created.get('price_yuan')}）")
    else:
        say("[进度] 同样的材料已经提交过，这次没有重复提交、没有重复扣费，接着看原来的任务")
    if args.wait:
        # 老用法：一直等到出结果。宿主前台跑命令时用户全程看不到进度，SKILL.md 里不再用
        wait_for(operation, args.timeout, args.out_dir)
    wait_for(operation, FIRST_WAIT_SECONDS, args.out_dir)


def do_ideas(args):
    if not args.yes:
        die("这是付费任务，取得用户同意后加 --yes 再运行。", EXIT_INPUT)
    idea = collect_materials(args.file, args.idea)
    if not idea:
        die("必须提供想法：--idea 给文本，或 --file 给文件。", EXIT_INPUT)
    if len(idea) < MIN_IDEA_CHARS and not args.force:
        die(f"想法只有 {len(idea)} 字，太短了。至少说清：想解决什么问题、现在打算怎么做。", EXIT_INPUT)
    if len(idea) > MAX_CHARS:
        die(f"材料 {len(idea)} 字，超过上限 {MAX_CHARS} 字。删掉与方案无关的部分再试。", EXIT_INPUT)

    body = {"report_type": "idea_upgrade",
            "input": {"idea_text": idea, "direction_count": args.count}}
    if args.title:
        body["input"]["title_hint"] = args.title
    submit(body, args, args.title)


def do_create(args):
    if not args.yes:
        die("这是付费任务，取得用户同意后加 --yes 再运行。", EXIT_INPUT)

    if args.from_ideas:
        report = unwrap(request(f"/api/v1/reports/{urllib.parse.quote(args.from_ideas)}"))
        directions = ((report or {}).get("result") or {}).get("directions") or []
        if not directions:
            die(f"报告 {args.from_ideas} 里没有方向清单，请确认它是方向分析的 report_id 且已经完成。", EXIT_INPUT)
        if args.direction is None:
            die("用 --from-ideas 时必须用 --direction 指定选第几个方向。", EXIT_INPUT,
                directions=[{"direction": d.get("direction_index"), "title": d.get("title")} for d in directions])
        picked = next((d for d in directions if d.get("direction_index") == args.direction), None)
        if not picked:
            die(f"没有第 {args.direction} 个方向。可选：" +
                "、".join(str(d.get("direction_index")) for d in directions), EXIT_INPUT)
        extra = collect_materials(args.file, args.supplement)
        supplement = direction_to_material(picked, args.idea)
        if extra:
            supplement += "\n\n" + extra
        title = args.title or picked.get("title")
    else:
        supplement = collect_materials(args.file, args.supplement)
        title = args.title
        if not supplement:
            die("必须提供材料：--supplement 给文本，--file 给文件（可多次），"
                "或 --from-ideas 接上一步的方向。", EXIT_INPUT)

    length = len(supplement)
    if length < MIN_DISCLOSURE_CHARS and not args.force:
        die(f"材料只有 {length} 字，写出来几乎全是推断。至少讲清：解决什么问题、具体怎么做（结构/步骤/参数）、"
            "达到什么效果；只有一个模糊想法的话，先用 ideas 出方向。", EXIT_INPUT)
    if length > MAX_CHARS:
        die(f"材料 {length} 字，超过上限 {MAX_CHARS} 字。删掉与方案无关的部分再试。", EXIT_INPUT)

    body = {"report_type": "technical_disclosure", "input": {"supplement": supplement}}
    if title:
        body["input"]["title_hint"] = title[:255]
    if length < RICH_CHARS:
        say(f"[提示] 材料 {length} 字，偏薄。缺的信息会按推荐值自动补，交付时提醒用户看核对说明里的待确认条目。")
    submit(body, args, title)


def do_wait(args):
    wait_for(args.operation_id, WAIT_SECONDS, args.out_dir)


def do_status(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}"))
    emit({
        "operation_id": args.operation_id,
        "report_id": data.get("report_id"),
        "report_type": data.get("report_type"),
        "status": (data.get("status") or "").lower(),
        "progress": progress_line(data, started_at_of(args.operation_id, data)),
        "error": data.get("error"),
    })


def do_download(args):
    path = f"/api/v1/reports/{urllib.parse.quote(args.report_id)}/files/report.docx"
    if args.kind == "notes":
        path += "?kind=notes"
    out = args.out or (f"{NOTES_NAME}.docx" if args.kind == "notes" else f"{DOC_NAME}.docx")
    payload = request(path, raw=True)
    with open(out, "wb") as handle:
        handle.write(payload)
    emit({"saved": os.path.abspath(out), "bytes": len(payload), "kind": args.kind})


def do_cancel(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/cancel",
                          method="POST"))
    emit({"operation_id": args.operation_id, "status": data.get("status"),
          "refund": "取消后预扣的费用全额退回。"})


def do_preview(args):
    """不花钱：看看拼好的材料长什么样、多少字，确认无误再 create。"""
    text = collect_materials(args.file, args.supplement)
    if not text:
        die("没有材料可预览。", EXIT_INPUT)
    emit({"chars": len(text),
          "level": "充分" if len(text) >= RICH_CHARS else ("偏薄" if len(text) >= MIN_DISCLOSURE_CHARS else "太短"),
          "head": text[:1500],
          "tail": text[-500:] if len(text) > 2000 else None})


def main():
    parser = argparse.ArgumentParser(description=f"PatentMax {DOC_NAME}")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p):
        p.add_argument("--title", default=None, help="案件名称，可选")
        p.add_argument("--file", action="append", default=[], help="材料文件，可多次：.md / .txt / .docx")
        p.add_argument("--out-dir", dest="out_dir", default=None, help="完成后 Word 存到哪个目录，默认当前目录")
        p.add_argument("--idempotency-key", dest="idempotency_key", default=None,
                       help="幂等键，默认按请求内容自动生成")
        p.add_argument("--wait", action="store_true", help="（旧用法）一直等到出结果，不推荐")
        p.add_argument("--timeout", type=int, default=5400, help="配合 --wait 的等待上限（秒）")
        p.add_argument("--force", action="store_true", help="材料过短时强制执行")
        p.add_argument("--yes", action="store_true", help="确认扣费")

    p = sub.add_parser("ideas", help="方向分析：一个想法 → 几个可申请的方向")
    p.add_argument("--idea", default=None, help="想法描述")
    p.add_argument("--count", type=int, default=3, choices=range(1, 6), metavar="1-5",
                   help="要几个方向，默认 3")
    common(p)
    p.set_defaults(func=do_ideas)

    p = sub.add_parser("create", help=f"生成{DOC_NAME}")
    p.add_argument("--supplement", default=None, help="材料正文或补充说明")
    p.add_argument("--from-ideas", dest="from_ideas", default=None, help="方向分析的 report_id")
    p.add_argument("--direction", type=int, default=None, help="选第几个方向（配合 --from-ideas）")
    p.add_argument("--idea", default=None, help="配合 --from-ideas：把原始想法也带上")
    common(p)
    p.set_defaults(func=do_create)

    p = sub.add_parser("wait", help="接着等：最多 30 秒，完成就自动下载 Word")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.set_defaults(func=do_wait)

    p = sub.add_parser("preview", help="不花钱：预览拼好的材料和字数")
    p.add_argument("--supplement", default=None)
    p.add_argument("--file", action="append", default=[])
    p.set_defaults(func=do_preview)

    p = sub.add_parser("status", help="只查一次任务状态")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_status)

    p = sub.add_parser("download", help="重新下载 Word（wait 完成时已自动下载过）")
    p.add_argument("--report-id", dest="report_id", required=True)
    p.add_argument("--kind", default="disclosure", choices=["disclosure", "notes"],
                   help=f"disclosure = {DOC_NAME}正文；notes = {NOTES_NAME}")
    p.add_argument("--out", default=None)
    p.set_defaults(func=do_download)

    p = sub.add_parser("cancel", help="取消任务，预扣费用全额退回")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
