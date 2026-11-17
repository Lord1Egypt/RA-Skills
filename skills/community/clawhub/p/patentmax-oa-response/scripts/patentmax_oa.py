#!/usr/bin/env python3
"""PatentMax OA答复（审查意见答复）客户端（v1.0.1）。

给 AI 用的命令行工具，走 POST /api/v1/reports 的 report_type=oa_response（仅中国专利申请）。

流程：提交 → 分析（约 2～3 分钟）→ 停下等用户选答复策略 → 改权利要求（约 1 分钟）
      → 停下等用户确认权利要求 → 写意见陈述书（约 1 分钟）→ 交付。用户说「按推荐来」时 --auto 一次跑完。

**每条命令最多跑 30 秒就返回**（学竞品：WorkBuddy 这类宿主前台跑命令时要等命令结束才显示输出，
一条命令阻塞几分钟，用户就几分钟什么都看不到）：

    退出码 0   完成了：意见陈述书全文在输出里，Word 已自动下载到提交时的目录
    退出码 10  还在生成：把输出里的「[进度]」行告诉用户，再运行一次 wait
    退出码 20  停下来等用户拿主意（选策略 / 确认权利要求）：把选项讲给用户，按他的决定运行 strategy / claims
    退出码 2   输入有误（材料缺、文件读不了），什么都没提交
    退出码 3   同样的任务已经在跑（没有重复提交、没有重复扣费），用输出里的 operation_id 接着 wait
    退出码 1   出错，message 是给用户看的中文说明，原样转述即可

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
REPORT_NAME = "OA答复"

EXIT_DONE, EXIT_ERROR, EXIT_INPUT, EXIT_BUSY, EXIT_RUNNING, EXIT_ACTION = 0, 1, 2, 3, 10, 20
WAIT_SECONDS = max(15, int(os.environ.get("PATENTMAX_WAIT_SECONDS") or 30))
FIRST_WAIT_SECONDS = min(15, WAIT_SECONDS)
POLL_SECONDS = 10
MIN_TEXT = 20

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
    print(line, flush=True)


def clock(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60}分{seconds % 60:02d}秒" if seconds >= 60 else f"{seconds}秒"


# ─────────────────────── 免费试用密钥 ───────────────────────
#
# 免密钥版（TRIAL_SOURCE 非空）：没设 PATENTMAX_API_KEY 时，第一次调用自动领一把免费试用密钥，
# 存在 ~/.patentmax/ 下，之后接着用（每把累计 ¥40、30 天有效、只开通 OA答复）。
# 密钥版（TRIAL_SOURCE 为空）：必须设 PATENTMAX_API_KEY。
TRIAL_SOURCE = ""
TRIAL_GROUP = "oa-response"
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
    if expires and expires <= time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()):
        return None
    return saved.get("api_key") or None


def _server_error(detail):
    try:
        body = json.loads(detail)
    except ValueError:
        return "", ""
    error = body.get("error") if isinstance(body, dict) else None
    if not isinstance(error, dict):
        return "", ""
    return str(error.get("code") or ""), str(error.get("message") or "")


def _claim_trial_key():
    req = urllib.request.Request(f"{BASE_URL}/api/v1/trial-keys", data=json.dumps({"source": TRIAL_SOURCE}).encode("utf-8"),
                                 method="POST")
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
        die(f"领取免费试用失败，网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试。", free_trial=True)
    data = payload.get("data") if isinstance(payload, dict) else None
    key = data.get("api_key") if isinstance(data, dict) else None
    if not key:
        die("领取免费试用失败：服务端没有返回密钥，请稍后重试。", free_trial=True)
    try:
        os.makedirs(cache_root(), exist_ok=True)
        with open(_trial_key_path(), "w", encoding="utf-8") as fh:
            json.dump({"api_key": key, "expires_at": data.get("expires_at"), "source": TRIAL_SOURCE, "base_url": BASE_URL},
                      fh, ensure_ascii=False, indent=2)
        os.chmod(_trial_key_path(), 0o600)
    except OSError:
        pass
    say(f"[PatentMax] 已自动领取免费试用：{data.get('note') or ''}")
    return key


def ensure_api_key():
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

CODE_MESSAGES = {
    "DAILY_LIMIT_EXCEEDED": "今天提交的报告数已达上限，北京时间明天 0 点恢复。这次没有提交，未扣费。",
    "CONCURRENT_LIMIT_EXCEEDED": "同时在生成的任务已达上限，等前面的任务完成后再提交。这次没有提交，未扣费。",
    "API_BALANCE_INSUFFICIENT": f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    "IDEMPOTENCY_KEY_OWNED_BY_DIFFERENT_API_KEY": "这份材料之前用同一账户的另一把密钥提交过。这次没有提交、未扣费。"
                                                  "去 https://api.ip930.com 控制台的调用记录里找原来那份。",
    "IDEMPOTENCY_KEY_REUSED_WITH_DIFFERENT_REQUEST": "这个任务编号已经用于另一份材料。这次没有提交、未扣费。不要手动指定 --idempotency-key。",
    "REPORT_NOT_READY": "答复还没有生成完，用 wait 接着等。",
}
HTTP_MESSAGES = {
    400: "参数不正确：审查意见通知书和申请文件都要给全文（各至少 20 字），对比文件最多 10 篇。这次没有提交，未扣费。",
    401: "密钥无效或已撤销。请到 https://api.ip930.com 控制台重新创建。",
    402: f"余额不足，这次没有提交，未扣费。充值或换正式密钥：{TRIAL_REGISTER_URL}",
    403: "这把密钥没有开通 OA答复。",
    404: "找不到这个任务或文件，请确认编号完整。",
    409: "任务不在这一步（可能已经继续过了），先运行 wait 看现在走到哪一步。",
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
        detail = exc.read().decode("utf-8", "replace")[:800]
        code, message = _server_error(detail)
        if KEY_FROM_TRIAL and exc.code == 401:
            try:
                os.remove(_trial_key_path())
            except OSError:
                pass
            die("免费试用已过期或失效。重新运行同一条命令会自动领取新的试用；"
                f"也可以注册 PatentMax 换正式密钥：{TRIAL_REGISTER_URL}", free_trial=True)
        text = (message if _has_cjk(message) else "") \
            or CODE_MESSAGES.get(message) or CODE_MESSAGES.get(code) \
            or HTTP_MESSAGES.get(exc.code) \
            or f"PatentMax 服务暂时不可用（HTTP {exc.code}），请稍后重试。"
        extra = {"free_trial": True} if "免费试用" in text else {}
        busy = exc.code == 409 and method == "POST" and path.endswith("/reports") \
            and not code.startswith("IDEMPOTENCY_") and not message.startswith("IDEMPOTENCY_")
        die(text, EXIT_BUSY if busy else EXIT_ERROR, http_status=exc.code, **extra)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        die(f"网络连不上 PatentMax（{getattr(exc, 'reason', exc)}）。请检查网络后重试；"
            "已提交的任务不受影响，稍后用 wait 接着看。")
    except json.JSONDecodeError:
        die("PatentMax 返回的内容不完整，请稍后重试。")


def try_download(path):
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
    """同样的材料 + 同一把密钥 → 同一个编号：重跑拿回原任务，不重复扣费。带密钥指纹，换密钥不会卡住。"""
    ensure_api_key()
    raw = json.dumps(body, ensure_ascii=False, sort_keys=True) + "|" + hashlib.sha256(API_KEY.encode("utf-8")).hexdigest()[:12]
    return "pmo-" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


# ─────────────────────── 材料 ───────────────────────

def read_docx(path):
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


def read_file(path, label):
    if not os.path.isfile(path):
        die(f"找不到{label}文件：{path}", EXIT_INPUT)
    lower = path.lower()
    if lower.endswith(".docx"):
        text = read_docx(path)
    elif lower.endswith((".pdf", ".doc", ".tif", ".tiff", ".jpg", ".png")):
        die(f"脚本读不了 {os.path.splitext(path)[1]}：{path}", EXIT_INPUT,
            hint="由你（AI）先把这份文件的全文读出来，存成 .txt 再交给脚本；通知书和申请文件要全文，不要摘要。")
    else:
        try:
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
        except UnicodeDecodeError:
            die(f"{label}文件不是 UTF-8 文本：{path}。只支持 .txt / .md / .docx。", EXIT_INPUT)
    text = text.strip()
    if len(text) < MIN_TEXT:
        die(f"{label}只有 {len(text)} 字，要给全文。", EXIT_INPUT)
    return text


def gather(files, text, label):
    parts = [read_file(p, label) for p in files or []]
    if text and text.strip():
        parts.append(text.strip())
    return "\n\n".join(parts)


def cited_entry(path):
    """对比文件：文件名里有公开号（如 CN109761224A.docx）就带上，没有也行。"""
    match = re.search(r"([A-Z]{2}\d{5,}[A-Z]\d?)", os.path.basename(path).upper())
    entry = {"text": read_file(path, "对比文件")}
    if match:
        entry["reference_number"] = match.group(1)
    return entry


# ─────────────────────── 本地任务记录 ───────────────────────

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


def out_dir_of(operation, override=None):
    target = override or load_task(operation).get("out_dir") or os.getcwd()
    os.makedirs(target, exist_ok=True)
    return target


def unique_path(path):
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
    return re.sub(r'[\\/:*?"<>|\s]+', "", str(text))[:40] or REPORT_NAME


# ─────────────────────── 等待 ───────────────────────

STATUS_TEXT = {"queued": "排队中", "accepting": "排队中", "running": "生成中"}


def progress_line(data, started_at):
    status = (data.get("status") or "").lower()
    stage = str(data.get("stage") or "")
    percent = data.get("progress")
    elapsed = clock(time.time() - started_at)
    detailed = _has_cjk(stage)
    if detailed and isinstance(percent, (int, float)) and 0 < percent < 100:
        return f"[进度 {int(percent)}%] {stage}，已用时 {elapsed}"
    if status in ("queued", "accepting"):
        return f"[进度] 排队中，已等待 {elapsed}"
    return f"[进度] {stage if detailed else STATUS_TEXT.get(status, '处理中')}，已用时 {elapsed}"


def started_at_of(operation, data):
    record = load_task(operation)
    if record.get("stage_started_at"):
        return float(record["stage_started_at"])
    created = str(data.get("created_at") or "")
    try:
        return calendar.timegm(time.strptime(created[:19], "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return time.time()


def decision(operation, data, out_dir=None):
    """停下来等用户拿主意：选项讲给用户，完整内容另存文件（用户想细看时再读）。"""
    action = data.get("required_action") or {}
    kind = action.get("type")
    target = out_dir_of(operation, out_dir)
    full = unique_path(os.path.join(target, f"{REPORT_NAME}_待确认_{kind or '下一步'}.json"))
    with open(full, "w", encoding="utf-8") as fh:
        json.dump(action, fh, ensure_ascii=False, indent=2)
    out = {"status": "requires_action", "operation_id": operation, "type": kind, "details_file": full,
           "expires_at": action.get("expires_at"),
           "expires_note": "超过这个时间不回复，任务会自动取消并全额退款。"}
    if kind == "select_strategy":
        out.update({
            "recommended": action.get("recommended_strategy_id"),
            "recommendation_reason": action.get("recommendation_reason"),
            "strategies": [{
                "id": s.get("id"), "title": s.get("title"), "amendment_level": s.get("amendment_level"),
                "amendment_summary": s.get("amendment_summary"),
                "core_arguments": (s.get("core_arguments") or [])[:4],
                "weaknesses": (s.get("weaknesses") or [])[:3],
                "evidence_needed": s.get("evidence_needed"),
            } for s in action.get("strategies") or []],
            "distinguishing_features": [{"feature": f.get("feature"), "claims": f.get("claims"), "assessment": f.get("assessment")}
                                        for f in (action.get("distinguishing_features") or [])[:6]],
            "examiner_flaws": action.get("examiner_flaws"),
            "divisional_suggestion": action.get("divisional_suggestion"),
            "next": f"把策略讲给用户，由他选；选定后运行：python {ME} strategy --operation-id {operation} --choose <编号>",
        })
    elif kind == "confirm_claims":
        claims_file = unique_path(os.path.join(target, f"{REPORT_NAME}_修改后的权利要求.txt"))
        with open(claims_file, "w", encoding="utf-8") as fh:
            fh.write(action.get("claims_text") or "")
        out.update({
            "selected_strategy": action.get("selected_strategy_id"),
            "amendment_summary": action.get("amendment_summary"),
            "claims_text": action.get("claims_text"),
            "claims_file": claims_file,
            "amendment_rows": [{"claim": r.get("amended_number"), "from": r.get("original_numbers"),
                                "operation": r.get("operation"), "basis": r.get("basis")}
                               for r in action.get("amendment_rows") or []],
            "checks": action.get("checks"),
            "next": (f"把修改后的权利要求全文贴给用户核对。原样确认：python {ME} claims --operation-id {operation}；"
                     f"用户改了文字：把改后的全文写进文件，先 python {ME} claims --operation-id {operation} --file <文件> --check 校验，"
                     f"用户同意后去掉 --check 再运行一次确认"),
        })
    emit(out, EXIT_ACTION)


def wait_for(operation, seconds, out_dir=None):
    deadline = time.time() + seconds
    last_stage = None
    while True:
        data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(operation)}"))
        status = (data.get("status") or "").lower()
        if status == "succeeded":
            emit(deliver(operation, data, out_dir), EXIT_DONE)
        if status == "requires_action":
            decision(operation, data, out_dir)
        if status in ("failed", "cancelled"):
            error = data.get("error") or {}
            message = error.get("message") if _has_cjk(error.get("message")) else ""
            die(message or ("任务已取消。" if status == "cancelled" else "OA答复没有生成成功。"),
                EXIT_ERROR, operation_id=operation, status=status, refund="预扣的费用已全额退回。")
        line = progress_line(data, started_at_of(operation, data))
        stage = line.split("，")[0]
        ending = time.time() + POLL_SECONDS > deadline
        if ending or (last_stage is not None and stage != last_stage):
            say(line)
        last_stage = stage
        if ending:
            emit({"status": "running", "operation_id": operation,
                  "next": f"把上面的进度告诉用户，然后运行：python {ME} wait --operation-id {operation}"}, EXIT_RUNNING)
        time.sleep(POLL_SECONDS)


def deliver(operation, data, out_dir=None):
    """完成：意见陈述书全文放进输出（要原样贴给用户），各份 Word 自动下载。"""
    report_id = data.get("report_id")
    payload = unwrap(request(f"/api/v1/reports/{urllib.parse.quote(report_id)}")) or {}
    result = payload.get("result") or {}
    target = out_dir_of(operation, out_dir)
    stem = safe_name(result.get("case_name") or result.get("title") or load_task(operation).get("title") or REPORT_NAME)

    files, internal = {}, {}
    for doc in result.get("documents") or [{"key": "statement", "title": "意见陈述书", "formal": True, "file": "statement.docx"}]:
        content = try_download(f"/api/v1/reports/{urllib.parse.quote(report_id)}/files/{urllib.parse.quote(doc.get('file') or '')}")
        if not content:
            continue
        path = unique_path(os.path.join(target, f"{doc.get('title') or doc.get('key')}_{stem}.docx"))
        with open(path, "wb") as fh:
            fh.write(content)
        (files if doc.get("formal", True) else internal)[doc.get("title") or doc.get("key")] = path
    statement = result.get("statement_text") or ""
    statement_file = unique_path(os.path.join(target, f"意见陈述书_{stem}.md"))
    with open(statement_file, "w", encoding="utf-8") as fh:
        fh.write(statement)
    full = unique_path(os.path.join(target, f"{REPORT_NAME}_{stem}_完整结果.json"))
    with open(full, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
    return {
        "status": "succeeded",
        "operation_id": operation,
        "report_id": report_id,
        "amount_charged_yuan": data.get("amount_charged_yuan"),
        "case_name": result.get("case_name"),
        "selected_strategy": result.get("selected_strategy"),
        "statement_text": statement,
        "claims_text": result.get("claims_text"),
        "evidence_needed": result.get("evidence_needed"),
        "files": files,
        "internal_files": internal,
        "statement_file": statement_file,
        "full_result": full,
    }


# ─────────────────────────── 子命令 ───────────────────────────

def do_create(args):
    if not args.yes:
        die("OA答复是付费任务（¥15），取得用户同意后加 --yes 再运行。", EXIT_INPUT)
    office_action = gather(args.office_action, args.office_action_text, "审查意见通知书")
    application = gather(args.application, args.application_text, "申请文件")
    if not office_action:
        die("缺审查意见通知书：用 --office-action 给文件（.docx / .txt / .md），要全文。", EXIT_INPUT)
    if not application:
        die("缺申请文件：用 --application 给文件，要包含权利要求书和说明书全文。", EXIT_INPUT)
    body = {"report_type": "oa_response", "input": {"office_action_text": office_action, "application_text": application}}
    specification = gather(args.specification, None, "说明书")
    if specification:
        body["input"]["specification_text"] = specification
    if args.cited:
        if len(args.cited) > 10:
            die("对比文件最多给 10 篇；没给的系统会按通知书里的公开号自己去取。", EXIT_INPUT)
        body["input"]["cited_references"] = [cited_entry(p) for p in args.cited]
    if args.auto:
        body["input"]["auto_confirm"] = True
    if args.title:
        body["input"]["title_hint"] = args.title[:255]

    key = args.idempotency_key or fingerprint(body)
    created = unwrap(request("/api/v1/reports", method="POST", body=body, headers={"Idempotency-Key": key}))
    operation = created.get("operation_id")
    if not operation:
        die("PatentMax 没有返回任务编号，请稍后重试。")
    record = load_task(operation)
    save_task(operation, stage_started_at=record.get("stage_started_at") or time.time(),
              out_dir=os.path.abspath(args.out_dir or os.getcwd()), title=args.title)
    if record:
        say("[进度] 同样的材料已经提交过，这次没有重复提交、没有重复扣费，接着看原来的任务")
    else:
        say(f"[进度] 已开始分析审查意见（预计费用 ¥{created.get('price_yuan')}）")
    wait_for(operation, FIRST_WAIT_SECONDS, args.out_dir)


def do_wait(args):
    wait_for(args.operation_id, WAIT_SECONDS, args.out_dir)


def do_strategy(args):
    body = {"strategy_id": args.choose}
    if args.note:
        body["note"] = args.note
    if args.no_divisional:
        body["include_divisional"] = False
    request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/strategy", method="POST", body=body)
    save_task(args.operation_id, stage_started_at=time.time())
    say(f"[进度] 已按策略 {args.choose} 开始修改权利要求")
    wait_for(args.operation_id, FIRST_WAIT_SECONDS)


def do_claims(args):
    body = {"action": "check" if args.check else "confirm"}
    if args.file:
        body["claims_text"] = read_file(args.file, "权利要求")
    path = f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/claims"
    if args.check:
        checked = unwrap(request(path, method="POST", body=body)) or {}
        emit({"status": "checked", "operation_id": args.operation_id, "checks": checked.get("checks"),
              "claims": checked.get("claims"),
              "next": f"把校验结果讲给用户；用户同意后运行：python {ME} claims --operation-id {args.operation_id} --file {args.file}"},
             EXIT_ACTION)
    request(path, method="POST", body=body)
    save_task(args.operation_id, stage_started_at=time.time())
    say("[进度] 权利要求已确认，开始写意见陈述书")
    wait_for(args.operation_id, FIRST_WAIT_SECONDS)


def do_status(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}"))
    emit({"operation_id": args.operation_id, "status": (data.get("status") or "").lower(),
          "progress": progress_line(data, started_at_of(args.operation_id, data)),
          "required_action": (data.get("required_action") or {}).get("type")})


def do_cancel(args):
    data = unwrap(request(f"/api/v1/operations/{urllib.parse.quote(args.operation_id)}/cancel", method="POST"))
    emit({"operation_id": args.operation_id, "status": data.get("status"), "refund": "取消后预扣的费用全额退回。"})


def main():
    parser = argparse.ArgumentParser(description="PatentMax OA答复（中国专利审查意见答复）")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("create", help="提交 OA答复（约 15 秒后返回，之后用 wait 接着等）")
    p.add_argument("--office-action", dest="office_action", action="append", default=[], help="审查意见通知书文件（.docx / .txt / .md）")
    p.add_argument("--office-action-text", dest="office_action_text", default=None, help="审查意见通知书全文（不方便给文件时）")
    p.add_argument("--application", action="append", default=[], help="申请文件（权利要求书 + 说明书），可多次")
    p.add_argument("--application-text", dest="application_text", default=None, help="申请文件全文")
    p.add_argument("--specification", action="append", default=[], help="说明书单独一份时用（可选）")
    p.add_argument("--cited", action="append", default=[], help="对比文件全文（可选，最多 10 篇；文件名带公开号更好）")
    p.add_argument("--auto", action="store_true", help="用户说「不用问我、按推荐来」时才加：自动选推荐策略、原样确认权利要求")
    p.add_argument("--title", default=None, help="案件简称，可选")
    p.add_argument("--out-dir", dest="out_dir", default=None, help="Word 存到哪个目录，默认当前目录")
    p.add_argument("--idempotency-key", dest="idempotency_key", default=None, help=argparse.SUPPRESS)
    p.add_argument("--yes", action="store_true", help="确认扣费（¥15）")
    p.set_defaults(func=do_create)

    p = sub.add_parser("wait", help="接着等：最多 30 秒")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--out-dir", dest="out_dir", default=None)
    p.set_defaults(func=do_wait)

    p = sub.add_parser("strategy", help="用户选定答复策略后继续（不另收费）")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--choose", required=True, help="策略编号，如 A")
    p.add_argument("--note", default=None, help="用户对这个策略的调整意见（原话）")
    p.add_argument("--no-divisional", dest="no_divisional", action="store_true", help="有分案建议但用户不采纳时加")
    p.set_defaults(func=do_strategy)

    p = sub.add_parser("claims", help="确认修改后的权利要求后继续（不另收费）")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.add_argument("--file", default=None, help="用户改过的权利要求全文文件（按「1. ……」逐项一行）；不给表示原样确认")
    p.add_argument("--check", action="store_true", help="只校验改过的文字，不继续")
    p.set_defaults(func=do_claims)

    p = sub.add_parser("status", help="只查一次状态")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_status)

    p = sub.add_parser("cancel", help="取消任务，预扣费用全额退回")
    p.add_argument("--operation-id", dest="operation_id", required=True)
    p.set_defaults(func=do_cancel)

    args = parser.parse_args()
    if args.command == "claims" and args.check and not args.file:
        die("--check 要和 --file 一起用（校验用户改过的权利要求）。", EXIT_INPUT)
    args.func(args)


if __name__ == "__main__":
    main()
