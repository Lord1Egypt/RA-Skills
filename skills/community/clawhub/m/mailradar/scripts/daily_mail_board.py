# -*- coding: utf-8 -*-
"""
每日邮件工作看板管道：
  1) 拉取飞书邮件（flagged / inbox / sent）
  2) 复用 extract4.py + gen_dashboard3.py 生成 mail_workboard2.html
  3) 组装飞书每日摘要（markdown）并推送 + 附件 HTML
可单独运行做一次性生成；自动化每天调用本脚本即可。
"""
import json, re, os, sys, subprocess, datetime, shutil, shlex

WS = os.path.dirname(os.path.abspath(__file__))
os.chdir(WS)
LARK = "lark-cli"

def load_config():
    """读取同目录 config.json（同事部署时填入自己的邮箱 / 飞书 open_id / 姓名）。
    未配置时回退到环境变量 MAILBOARD_ME / MAILBOARD_OPEN_ID / MAILBOARD_NAME，
    再回退到下方默认值。"""
    cfg_path = os.path.join(WS, "config.json")
    if os.path.exists(cfg_path):
        try:
            return json.load(open(cfg_path, encoding="utf-8")) or {}
        except Exception:
            pass
    return {}

CFG = load_config()
# 同事部署：改 config.json 或设置环境变量即可，无需改代码
ME = CFG.get("mailbox") or os.environ.get("MAILBOARD_ME") or "your-name@company.com"
OPEN_ID = CFG.get("feishu_open_id") or os.environ.get("MAILBOARD_OPEN_ID") or ""
AT_NAME = CFG.get("feishu_name") or os.environ.get("MAILBOARD_NAME") or "同事"
# 让子进程（extract4.py / gen_dashboard3.py）继承 mailbox 地址
os.environ["MAILBOARD_ME"] = ME

TODAY = datetime.date.today()
GEN_AT = TODAY.strftime("%Y-%m-%d %H:%M")

# ---------------- lark-cli helpers ----------------
def find_bash():
    import glob
    cands = glob.glob(os.path.expanduser("~/.workbuddy/binaries/PortableGit/versions/*/usr/bin/bash.exe"))
    if cands:
        return cands[0]
    return "bash"

BASH_EXE = find_bash()

def lark(args, timeout=120):
    cmd = "lark-cli " + " ".join(shlex.quote(a) for a in args)
    r = subprocess.run([BASH_EXE, "-lc", cmd], capture_output=True, text=True, cwd=WS, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError("lark-cli failed [%s]: %s" % (" ".join(args[:3]), r.stderr.strip()[:300]))
    return r.stdout

def pull_triage(folder, maxn=400, start_days=None, timeout=180):
    out = []
    page = None
    while True:
        args = ["mail", "+triage", "--folder", folder, "--max", str(maxn), "--json", "--labels"]
        if start_days:
            st = (TODAY - datetime.timedelta(days=start_days)).strftime("%Y-%m-%dT00:00:00+00:00")
            flt = json.dumps({"time_range": {"start_time": st}})
            args += ["--filter", flt]
        if page:
            args += ["--page-token", page]
        data = json.loads(lark(args, timeout=timeout))
        msgs = data.get("messages", []) or []
        out.extend(msgs)
        if not data.get("has_more") or not data.get("page_token"):
            break
        page = data.get("page_token")
    return out

def pull_bodies(ids):
    bodies = {}
    if not ids:
        return bodies
    batch = [ids[i:i+20] for i in range(0, len(ids), 20)]
    for b in batch:
        try:
            data = json.loads(lark(["mail", "+messages", "--html=false", "--message-ids", ",".join(b)], timeout=180))
        except Exception as e:
            sys.stderr.write("bodies batch err: %s\n" % e)
            continue
        for m in data.get("data", {}).get("messages", []):
            bodies[m.get("message_id")] = m
    return bodies

# ---------------- extraction logic (from extract3.py) ----------------
def norm(d):
    d = (d or "").replace("T", " ").replace("Z", "")
    return d[:10]

# 引文/邮件头剥离（含 MAIL/From/To/Cc/Sent/Subject 等内联或换行形式），避免引用邮件头泄漏
# 跨语言引用头：Am/Il/Le/El/Dňa/Dne ... schrieb/ha scritto/a écrit/escribió/napísal/napsal；英文 On ... wrote:（冒号/换行收尾）
WROTE_PATTERN = re.compile(
    r'(?m)(?:^|[>\s]*)(?:Am|Il|Le|El|Dňa|Dne)\b'
    r'.{0,200}?\b(?:schrieb|ha scritto|a écrit|escribió|napísal|napsal)\b(?=\s*[:\n])',
    re.I)
EN_WROTE = re.compile(r'(?m)^[>\s]*On\b.{0,200}?\bwrote\b(?=\s*[:\n])', re.I)
def fresh_part(body):
    b = body or ""
    marks = ["\nFrom: ", "\nOn ", "-----原始邮件-----", "\n> ",
             " MAIL:", " From:", " To:", " Cc:", " Sent:", " Subject:",
             "\n发件人：", "\n收件人：", "\n抄送：", "\n主题：", "\n发送时间："]
    positions = [b.find(mk) for mk in marks if b.find(mk) > 0]
    for pat in (WROTE_PATTERN, EN_WROTE):
        m = pat.search(b)
        if m and m.start() > 0:
            positions.append(m.start())
    if positions:
        b = b[:min(positions)]
    return b.strip()

def responsible(body):
    fp = fresh_part(body)
    m = re.search(r"(?:Hi|Dear|Hello)\s+([A-Za-z][\w\x27.-]+)", fp)
    if m:
        return m.group(1)
    m2 = re.search(r"(?:Hi|Dear|Hello)\s+([A-Za-z][\w\x27.-]+)", body or "")
    return m2.group(1) if m2 else ""

MONTHS = r"(?:january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec)"
DDL_PATTERNS = [
    r"end of (?:" + MONTHS + r")",
    r"by (?:the )?(?:end of |beginning of |middle of )?" + MONTHS + r"(?: \d{1,2})?",
    r"week of " + MONTHS + r"(?: \d{1,2})?",
    r"\d{1,2}(?:st|nd|rd|th)? (?:of )?" + MONTHS,
    r"\d{1,2}[/.]\d{1,2}(?:[/.]\d{2,4})?",
    r"\d{1,2} ?\w+ (?:at the latest|at latest)",
    r"最晚|截止日期|截止至|before \w+ \d{1,2}",
]
MON2NUM = {m: i+1 for i, m in enumerate(["january","february","march","april","may","june","july","august","september","october","november","december"])}
MON2NUM.update({m: i+1 for i, m in enumerate(["jan","feb","mar","apr","jun","jul","aug","sep","sept","oct","nov","dec"])})

def parse_ddl_date(phrase):
    ph = phrase.lower()
    m = re.search(r"(\d{1,2})[/.](\d{1,2})(?:[/.](\d{2,4}))?", ph)
    if m:
        d, mo = int(m.group(1)), int(m.group(2))
        yr = int(m.group(3)) if m.group(3) else 2026
        if yr < 100:
            yr += 2000
        if 1 <= mo <= 12 and 1 <= d <= 31:
            return "%04d-%02d-%02d" % (yr, mo, d)
    mm = re.search(MONTHS, ph)
    if mm:
        mon = MON2NUM.get(mm.group(0).lower())
        dm = re.search(r"(\d{1,2})(?:st|nd|rd|th)?", ph)
        day = int(dm.group(1)) if dm else 28
        if mon:
            return "2026-%02d-%02d" % (mon, min(day, 28))
    return None

ACTION_RE = re.compile(r"\b(please|kindly|could you|can you|we need|need to|must|should|confirm|arrange|provide|send|review|submit|complete|finalize|follow up|by when|let (?:me|us) know|reply|schedule|book|prepare|update)\b", re.IGNORECASE)

def ddl_text(body):
    fp = fresh_part(body)
    found = []
    for p in DDL_PATTERNS:
        for m in re.finditer(p, fp, re.IGNORECASE):
            s = max(0, m.start() - 20); e = min(len(fp), m.end() + 20)
            frag = fp[s:e].replace("\n", " ").strip()
            dt = parse_ddl_date(frag)
            if not dt:
                continue
            window = fp[max(0, m.start() - 60):min(len(fp), m.end() + 40)]
            hard = re.search(r"\b(by|before|end of|until|最晚|截止|at the latest|at latest|deadline|due)\b", window, re.IGNORECASE)
            if hard or ACTION_RE.search(window):
                found.append({"text": frag, "date": dt})
    out = {}
    for f in found:
        if f["date"] not in out:
            out[f["date"]] = f["text"]
    return [{"date": k, "text": out[k]} for k in sorted(out.keys())][:2]

def snippet(body, n=200):
    fp = re.sub(r"\s+", " ", fresh_part(body)).strip()
    return fp[:n] + ("…" if len(fp) > n else "")

def direction_of(meta_from, body_msg):
    st = (body_msg or {}).get("message_state_text")
    if st == "sent":
        return "发出"
    if st == "received":
        return "收到"
    frm = (meta_from or "").lower()
    return "发出" if ME in frm else "收到"

# 系统退信（投递失败）识别：覆盖英文主流模板 + 中文模板（邮件退信/退信/投递失败…）+ 退信发件人（mailer-daemon/postmaster…）
BOUNCE_RE = re.compile(
    r'(undeliverable|returned mail|returned to sender|delivery status notification|failure notice|'
    r'delivery failure|delivery has failed|mail delivery failed|unable to deliver|'
    r'permanent delivery failure|nondelivery report|undelivered mail|message not delivered|'
    r'delivery report \(failure\)|邮件退信|退信|投递失败|无法送达|邮件退回|发送失败|退回的邮件|投递状态通知)',
    re.I)
BOUNCE_SENDER_RE = re.compile(r'(mailer-daemon|postmaster|mail delivery system|microsoft outlook|no.?reply|don?ot?reply|do-not-reply|系统退信|投递系统|daemon)', re.I)

def is_bounce(subj, body="", sender=""):
    s = (subj or "").strip()
    if BOUNCE_RE.search(s):
        return True
    if sender and BOUNCE_SENDER_RE.search(sender):
        return True
    b = body or ""
    if "Delivery has failed to these recipients or groups" in b:
        return True
    if "邮件退信" in b or "投递失败" in b or "无法送达" in b:
        return True
    return False

# ---------------- build email_detail + bodies ----------------
ODL_SUBJ = re.compile(r"\b(order|purchase order|p\.o\.|procurement|采购|下单|订货|deliver|delivery|shipment|ship|dispatch|发货|交付|送货|到货|物流|lead time|lead-time|生产周期|货期|交期|eta|etd|production time|工期|tender|quote|quotation|boq|invoice|payment)\b", re.I)
STORE_SUBJ = re.compile(r"cologne|köln|koeln|rome|roma|düsseldorf|dusseldorf|duesseldorf|zurich|zürich|glatt", re.I)
DDL_SUBJ = re.compile(r"\b(by|before|end of|due|deadline|最晚|截止|at the latest)\b", re.I)
# 西葡地区非建店业务：西班牙/葡萄牙 + Brandzone/Endcap/Table-Top/POSM（模块③）
IBERIA_SUBJ = re.compile(r"\b(spain|portugal|españa|ibé?ria|brandzone|endcap|table[\s-]?top|posm|retail project|monica avila)\b", re.I)
def needs_body(subj):
    return bool(ODL_SUBJ.search(subj or "") or STORE_SUBJ.search(subj or "") or DDL_SUBJ.search(subj or "") or IBERIA_SUBJ.search(subj or ""))

def build():
    print("[1/5] pulling triage (flagged / inbox) ...")
    # 用户最新规则：只抓取 7 天内邮件；超出 7 天的邮件不再进入任何统计/展示
    flagged_raw = pull_triage("flagged", start_days=7)
    inbox_raw = pull_triage("inbox", start_days=7)
    # 系统退信（投递失败）直接忽略，不进入任何信息范围
    nb0 = len(flagged_raw) + len(inbox_raw)
    flagged_raw = [m for m in flagged_raw if not is_bounce(m.get("subject", ""), sender=m.get("from", ""))]
    inbox_raw = [m for m in inbox_raw if not is_bounce(m.get("subject", ""), sender=m.get("from", ""))]
    print("  bounce filtered: %d removed, flagged=%d inbox=%d" % (nb0 - len(flagged_raw) - len(inbox_raw), len(flagged_raw), len(inbox_raw)))
    flagged_ids = set(m["message_id"] for m in flagged_raw)

    print("[2/5] pulling bodies (focused) ...")
    focus_inbox = [m for m in inbox_raw if (m["message_id"] not in flagged_ids) and needs_body(m.get("subject", ""))]
    all_ids = list({m["message_id"] for m in flagged_raw + focus_inbox})
    bodies = pull_bodies(all_ids)
    json.dump({"data": {"messages": list(bodies.values())}}, open("_all_bodies.json", "w", encoding="utf-8"), ensure_ascii=False)

    def meta_of(m):
        b = bodies.get(m["message_id"], {})
        return {
            "id": m["message_id"],
            "date": norm(m.get("date") or b.get("internal_date")),
            "subject": m.get("subject") or b.get("subject", ""),
            "from": m.get("from", ""),
            "labels": m.get("labels", ""),
            "direction": direction_of(m.get("from", ""), b),
            "body": b.get("body_plain_text", ""),
        }

    flagged = []
    for m in flagged_raw:
        x = meta_of(m)
        flagged.append({
            "id": x["id"], "date": x["date"], "subject": x["subject"], "from": x["from"],
            "direction": x["direction"], "labels": x["labels"],
            "responsible": responsible(x["body"]), "ddl": ddl_text(x["body"]), "content": snippet(x["body"]),
        })
    other = []
    for m in focus_inbox:
        x = meta_of(m)
        other.append({
            "id": x["id"], "date": x["date"], "subject": x["subject"], "from": x["from"],
            "direction": x["direction"], "labels": x["labels"],
            "responsible": responsible(x["body"]), "ddl": ddl_text(x["body"]), "content": snippet(x["body"]),
        })

    json.dump({"flagged": flagged, "other": other}, open("email_detail.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # split bodies for extract4 expected filenames
    fbg = [b for mid, b in bodies.items() if mid in flagged_ids]
    obg = [b for mid, b in bodies.items() if mid not in flagged_ids]
    json.dump({"data": {"messages": fbg}}, open("flagged_bodies.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({"data": {"messages": obg}}, open("other_bodies.json", "w", encoding="utf-8"), ensure_ascii=False)
    print("  flagged=%d other=%d bodies=%d" % (len(flagged), len(other), len(bodies)))
    return len(flagged), len(other)

# ---------------- generate + send ----------------
def generate():
    print("[3/5] extract4 -> workboard2_data.json")
    subprocess.run([sys.executable, "extract4.py"], cwd=WS, check=True)
    print("[4/5] gen_dashboard3 -> mail_workboard2.html")
    subprocess.run([sys.executable, "gen_dashboard3.py"], cwd=WS, check=True)
    # 生成待翻译清单（供 agent 在自动化里做 LLM 中文翻译/归纳）
    if os.path.exists("prep_cn.py"):
        try:
            subprocess.run([sys.executable, "prep_cn.py"], cwd=WS, check=True)
        except Exception as e:
            sys.stderr.write("prep_cn warn: %s\n" % e)

def upcoming_ddls(data, days=7):
    res = []
    cutoff = (TODAY + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    for sk, sv in data["stores"].items():
        for sec in sv["sections"]:
            for t in sec["items"]:
                for d in t.get("ddl", []):
                    if d.get("date") and TODAY.strftime("%Y-%m-%d") <= d["date"] <= cutoff:
                        res.append((d["date"], sv["label"], t["subject"][:40], d.get("text", "")))
    for o in data["other_todos"]:
        for d in o.get("ddl", []):
            if d.get("date") and TODAY.strftime("%Y-%m-%d") <= d["date"] <= cutoff:
                res.append((d["date"], "其他·" + o["type"], o["subject"][:40], d.get("text", "")))
    res.sort()
    return res

# 与 gen_dashboard3.py 中 urgencyOf 同步：逾期/临期(2天内)/关注(5天内)，窗口 ±7 天
def _lvl(d):
    try:
        dd = datetime.datetime.strptime(d, "%Y-%m-%d").date()
    except Exception:
        return None
    days = (dd - TODAY).days
    if days < -7 or days > 7:
        return None
    if days < 0:
        return "overdue"
    if days <= 2:
        return "high"
    if days <= 5:
        return "mid"
    return None

# 简易主题中文翻译（Python 兜底版，与 JS 的 trSubj 对齐；
# pick_summary 在 CN 缺失时调用，确保飞书 message 也能给点中文提示）
_RE_R = __import__('re').compile(r'^\s*(RE|Re|FW|Fw|FYI|AW|Aw|SV|VS|TR|FS|FBL|R)(\s*[：:.\-]\s*)', __import__('re').I)
_TR_PAIRS = [
    (r'DE[\s_]+POSM\b', '德国 POSM'),
    (r'FR[\s_]+POSM\b', '法国 POSM'),
    (r'\bPOSM\b', '物料'),
    (r'\bRFQ\b', '询价'),
    (r'\bendcap(s)?\b', '端架'),
    (r'\btiered pricing\b', '分级报价'),
    (r'\bquotation\b', '报价'),
    (r'\bnew quotation\b', '新报价'),
    (r'\brevised quotation\b', '修订报价'),
    (r'\bTender Invitation\b', '招标邀请'),
    (r'\bQ&A Period\b', '答疑期'),
    (r'\bseparate deliveries\b', '分批交付'),
    (r'\bpreparation(s)?\b', '备货'),
    (r'\bworking days?\b', '工作日'),
    (r'\bshipping time\b', '运输周期'),
    (r'\bproduction time\b', '生产周期'),
    (r'\blightboxes?\b', '灯箱'),
    (r'\bdisplays?\b', '陈列道具'),
    (r'\bprint data\b', '印刷数据'),
    (r'\bFinal Delivery Date\b', '最终交付日期'),
    (r'\bholiday\b', '休假'),
    # 兼容 "11_MOVA_DE_COLOGNE_BOUTIQUE_MM_"：连同首部编号(11_)与尾部标记(_MM)一并吞掉，与 JS trSubj 对齐
    (r'(?<![A-Za-z])\d*[\s_]*MOVA[\s_]+DE[\s_]+COLOGNE[\s_]+BOUTIQUE[\s_]*MM?[\s_]*', 'MOVA 科隆店中店'),
    (r'\bMOVA[\s_]+Italy\b', 'MOVA 意大利'),
    (r'\bDreame[\s_]+Italy\b', 'DREAME 意大利'),
    (r'\bItaly\b', '意大利'),
    (r'\bGermany\b', '德国'),
    (r'\bD[uü]sseldorf\b', '杜塞'),
    (r'\bZurich\b', '苏黎世'),
    (r'\bCologne\b', '科隆'),
    (r'\bRome\b', '罗马'),
]
def _tr_subj_py(s):
    if not s:
        return ""
    import re
    prev=None
    while prev != s and s:
        prev=s
        s=_RE_R.sub('',s).strip()
    for pat, rep in _TR_PAIRS:
        s = re.sub(pat, rep, s, flags=re.I)
    s = re.sub(r'\s+&\s+', ' · ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s[:100]

def collect_ddl_items(data, cn=None):
    """汇总所有 DDL 项目（含中文摘要），按状态严重程度排序：逾期 > 临期 > 关注。"""
    cn = cn or load_cn()
    cn_stores = cn.get("stores", {})
    cn_iberia = cn.get("iberia", {})
    cn_todos = cn.get("other_todos", {})
    items = []

    def pick_summary(c, fallback=""):
        # 用户最新规则：CN 词典完全缺失时，也用 trSubj 对 fallback 主题做兜底中文
        if not c:
            if not fallback:
                return ""
            ts = _tr_subj_py(fallback)
            if ts and any('\u4e00' <= c2 <= '\u9fa5' for c2 in ts):
                return ts
            return ""
        if isinstance(c.get("summary"), str) and c["summary"].strip():
            return c["summary"]
        arr = []
        if c.get("todos"): arr = c["todos"]
        elif c.get("needs_action"): arr = c["needs_action"]
        elif c.get("items"): arr = c["items"]
        if arr:
            return "；".join(arr[:2])
        # CN 存在但无 summary/todos/items: 仍兜底翻译 fallback
        if fallback:
            ts = _tr_subj_py(fallback)
            if ts and any('\u4e00' <= c2 <= '\u9fa5' for c2 in ts):
                return ts
        return ""

    for sk in ["Cologne", "Rome", "Dusseldorf", "Zurich"]:
        cn_sk = cn_stores.get(sk, {})
        for sec in data["stores"][sk].get("sections", []):
            for t in sec.get("items", []):
                # 无明确待办的邮件不计入提醒
                if not (t.get("todos") and t["todos"]):
                    continue
                c = cn_sk.get(t.get("thread_id")) if isinstance(cn_sk, dict) else None
                summary = pick_summary(c, t.get("subject", "")[:60])
                for d in t.get("ddl", []):
                    lvl = _lvl(d["date"])
                    if not lvl:
                        continue
                    items.append({
                        "lvl": lvl,
                        "date": d["date"],
                        "label": data["stores"][sk]["label"],
                        "summary": summary,
                        "city": sk,
                        "tid": t.get("thread_id"),
                        "mod": "store",
                    })
    for sec in data.get("iberia_view", {}).get("sections", []):
        for t in sec.get("items", []):
            if not (t.get("todos") and t["todos"]):
                continue
            c = cn_iberia.get(t.get("thread_id")) if isinstance(cn_iberia, dict) else None
            summary = pick_summary(c, t.get("subject", "")[:60])
            for d in t.get("ddl", []):
                lvl = _lvl(d["date"])
                if not lvl:
                    continue
                items.append({
                    "lvl": lvl,
                    "date": d["date"],
                    "label": t.get("country") or "西葡业务",
                    "summary": summary,
                    "tid": t.get("thread_id"),
                    "mod": "iberia",
                })
    for o in data.get("other_todos", []):
        c = cn_todos.get(o.get("id")) if isinstance(cn_todos, dict) else None
        summary = pick_summary(c, o.get("subject", "")[:60])
        for d in o.get("ddl", []):
            lvl = _lvl(d["date"])
            if not lvl:
                continue
            items.append({
                "lvl": lvl,
                "date": d["date"],
                "label": "其他·" + (o.get("type") or ""),
                "summary": summary,
                "tid": o.get("id"),
                "mod": "todo",
            })
    # 排序：逾期 > 临期 > 关注，然后按日期升序
    order = {"overdue": 0, "high": 1, "mid": 2}
    items.sort(key=lambda x: (order.get(x["lvl"], 9), x["date"]))
    return items


def build_digest(data, cn=None):
    """重构后的飞书 message（用户最新规则）：
       ① 顶部简要统计（含三档计数：已逾期X条 / 临期Y条 / 关注Z条）
       ② 待办事项按 1/2/3... 编号列出，3~5 条（按状态严重程度排序）
       ③ 超出条目数提示跳转看板
       ④ 明日截止催反馈（如有）
    """
    cn = cn or load_cn()
    vol = data["volume"]
    lines = []

    # ① 顶部简要统计
    lines.append("**📬 每日邮件工作看板 · %s**（窗口近 7 天）" % GEN_AT)
    lines.append("")
    lines.append("总往来 **%d 封** ｜ 收到 %d ｜ 发出 %d ｜ 旗标 %d ｜ 含明确 DDL %d ｜ 重点门店相关 %d" % (
        vol["total"], vol["received"], vol["sent"], vol["flagged"], vol["with_ddl"], vol["key_store_emails"]))
    lines.append("西葡非建店业务：%d 个线程（Monica 涉及 %d 个）" % (
        data["stats"].get("iberia", 0), data["stats"].get("iberia_monica", 0)))
    lines.append("")

    # ② 三档计数（用户最新格式："X 条"）
    items = collect_ddl_items(data, cn)
    cnt = {"overdue": 0, "high": 0, "mid": 0}
    for it in items:
        cnt[it["lvl"]] += 1
    lines.append("**⏰ 临期三档**：🔴 已逾期 **%d 条** / 🟡 临期 **%d 条** / 🔵 关注 **%d 条**（共 %d 条）" % (
        cnt["overdue"], cnt["high"], cnt["mid"], len(items)))
    lines.append("")

    # ③ 1/2/3 编号待办列表（限 3~5 条）
    cap = 5
    show = items[:cap]
    if show:
        lines.append("**📋 待办事项列表**（按状态分组 · 展示前 %d 条）" % len(show))
        lines.append("")
        lvl_emoji = {"overdue": "🔴", "high": "🟡", "mid": "🔵"}
        for i, it in enumerate(show, 1):
            emoji = lvl_emoji.get(it["lvl"], "🔹")
            summary = it["summary"] or "（无中文摘要，请在看板查看）"
            lines.append("**%d.** %s **%s** · 截止 **%s** · %s" % (
                i, emoji, it["label"], it["date"], summary))
        lines.append("")
        if len(items) > cap:
            lines.append("> 📎 完整 **%d 条** 待办见附件 HTML 看板（含每条详情、跳转邮件卡片按钮）。" % len(items))
            lines.append("")
    else:
        lines.append("**📋 待办事项列表**：（暂无临期 7 天内待办）")
        lines.append("")

    # ④ 明日截止催反馈（如有；保持原有 @陈哲 行为）
    chase = chase_items(data)
    if chase:
        lines.append("---")
        lines.append("**⏰ 明日（%s）截止 · 需催反馈**" % (TODAY + datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        at = '<at user_id="%s">%s</at>' % (OPEN_ID, AT_NAME)
        lines.append("%s 以下待办明天截止且仍需对方反馈，请跟进催办：" % at)
        for o in chase:
            who = o.get("responsible") or "对方"
            lines.append("- 需催 **%s** ｜ %s ｜ %s" % (who, o.get("type"), o.get("subject", "")[:50]))
        lines.append("（多数对方为外部供应商、不在飞书通讯录，请在其邮件 / 原有沟通渠道催办；本条为提醒，不直接 @ 外部方。）")
        lines.append("")
    else:
        lines.append("⏰ 明日无「需反馈」截止项。")
        lines.append("")

    # ⑤ 模块导览 + 看板说明
    lines.append("---")
    lines.append("📂 **看板 4 模块**：① 往来邮件Summary（KPI+图表，含临期三档提醒卡片）｜ ② 西南欧建店管理（4 城：科隆/罗马/杜塞/苏黎世）｜ ③ 西葡地区非建店业务跟踪（西/葡）｜ ④ 其他事项（下单/交付/交期）。")
    lines.append("")
    lines.append("每条邮件卡片均含：**🇨🇳 邮件摘要翻译** + **📌 主要内容（中英文对照）** + **✅ 待办事项（中英文对照）** + 已回复/待回复/无需回复按钮（localStorage 持久化）。")
    lines.append("")
    lines.append("📎 完整看板见附件 `mail_workboard2.html`（自包含、可离线打开）。")

    return "\n".join(lines)

def _metric(num, label):
    """指标卡（P1 焦点 / P3 结构）：大数字 + 灰标签，居中。"""
    return {
        "tag": "column", "width": "weighted", "weight": 1,
        "background_style": "grey-50",
        "padding": "12px", "vertical_spacing": "2px",
        "elements": [
            {"tag": "markdown", "content": "## <font color=\"blue\">%s</font>" % num, "text_align": "center"},
            {"tag": "markdown", "content": "<font color=\"grey\">%s</font>" % label, "text_align": "center", "text_size": "notation"},
        ],
    }

def build_card(data, cn=None):
    """飞书原生交互卡片（Card 2.0）：三栏看板式布局（已逾期 / 临期 / 关注），美观直观。
    结构：header(蓝+状态标签) → 指标卡 row → 三档看板 column_set → 附件说明。
    遵循 lark-im-card-style P0–P7：单焦点(stats)、分组(三栏)、复杂度适中(3 块)、语义色(红=警/黄=待处理/蓝=信息)。"""
    cn = cn or load_cn()
    vol = data["volume"]
    items = collect_ddl_items(data, cn)
    cnt = {"overdue": 0, "high": 0, "mid": 0}
    for it in items:
        cnt[it["lvl"]] += 1

    def trunc(s, n=24):
        s = (s or "").strip()
        return s if len(s) <= n else s[:n] + "…"

    # 三档分组（语义色：red=警 / yellow=待处理 / blue=信息）
    tiers = [
        ("overdue", "🔴", "已逾期", "red",    cnt["overdue"]),
        ("high",    "🟡", "临期",   "yellow", cnt["high"]),
        ("mid",     "🔵", "关注",   "blue",   cnt["mid"]),
    ]
    per_col_cap = 4
    columns = []
    for lvl, emoji, name, color, n in tiers:
        grp = [it for it in items if it["lvl"] == lvl]
        col_elems = [
            {"tag": "markdown",
             "content": "%s **<font color=\"%s\">%s</font>**  <font color=\"grey\">%d 条</font>" % (emoji, color, name, n)},
        ]
        if not grp:
            col_elems.append({"tag": "markdown", "content": "<font color=\"grey\">暂无</font>"})
        else:
            for it in grp[:per_col_cap]:
                label = it["label"] or ""
                date = (it["date"] or "")[5:]  # MM-DD
                summ = trunc(it["summary"] or "（无摘要，看板查看）", 22)
                col_elems.append({
                    "tag": "markdown",
                    "content": "**%s**\n<font color=\"grey\">截止 %s · %s</font>" % (label, date, summ),
                    "text_size": "normal",
                })
            if len(grp) > per_col_cap:
                col_elems.append({"tag": "markdown",
                                   "content": "<font color=\"grey\">…等 %d 条，见附件</font>" % len(grp),
                                   "text_size": "notation"})
        columns.append({
            "tag": "column", "width": "weighted", "weight": 1,
            "background_style": color + "-50",
            "padding": "12px", "vertical_spacing": "4px",
            "elements": col_elems,
        })

    card = {
        "schema": "2.0",
        "config": {"width_mode": "default"},
        "header": {
            "title": {"tag": "plain_text", "content": "每日邮件工作看板"},
            "subtitle": {"tag": "plain_text", "content": "%s · 近 7 天窗口" % GEN_AT},
            "template": "blue",
            "icon": {"tag": "standard_icon", "token": "todo_colorful"},
            "text_tag_list": [
                {"tag": "text_tag", "text": {"tag": "plain_text", "content": "已逾期 %d" % cnt["overdue"]}, "color": "red"},
                {"tag": "text_tag", "text": {"tag": "plain_text", "content": "临期 %d" % cnt["high"]}, "color": "yellow"},
                {"tag": "text_tag", "text": {"tag": "plain_text", "content": "关注 %d" % cnt["mid"]}, "color": "blue"},
            ],
        },
        "body": {
            "direction": "vertical",
            "padding": "12px 12px 20px 12px",
            "vertical_spacing": "12px",
            "elements": [
                {"tag": "column_set", "flex_mode": "none", "horizontal_spacing": "8px", "columns": [
                    _metric(vol["total"], "总往来"),
                    _metric(vol["flagged"], "旗标"),
                    _metric(vol["with_ddl"], "含 DDL"),
                    _metric(vol["key_store_emails"], "重点门店"),
                ]},
                {"tag": "column_set", "flex_mode": "none", "horizontal_spacing": "8px", "columns": columns},
                {"tag": "markdown", "content": (
                    "📎 **完整看板见下方附件** `mail_workboard2.html`（含每条详情、跳转邮件卡片按钮）。\n"
                    "📂 4 模块：① 往来邮件Summary ② 西南欧建店 ③ 西葡非建店 ④ 其他事项。")},
            ],
        },
    }
    return json.dumps(card, ensure_ascii=False)

def chase_items(data):
    """需反馈 且 DDL 落在明天 的待办（用于截止前1天催办提醒）。"""
    tom = (TODAY + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    out = []
    for o in data.get("other_todos", []):
        if not o.get("needs_feedback"):
            continue
        if o.get("ddl_earliest") == tom:
            out.append(o)
    return out

def chase_message(items):
    tom = (TODAY + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    at = '<at user_id="%s">%s</at>' % (OPEN_ID, AT_NAME)
    lines = []
    lines.append("%s ⏰ **明日截止 · 需催反馈提醒**" % at)
    lines.append("")
    lines.append("以下待办**明天（%s）截止**且仍需对方反馈，请跟进催办：" % tom)
    for o in items:
        who = o.get("responsible") or "对方"
        lines.append("- 需催 **%s** ｜ 截止 %s ｜ %s ｜ %s" % (
            who, o.get("ddl_earliest"), o.get("type"), o.get("subject", "")[:50]))
    lines.append("")
    lines.append("（多数对方为外部供应商、不在飞书通讯录，请在其邮件 / 原有沟通渠道催办；本条为提醒，不直接 @ 外部方。）")
    return "\n".join(lines)

def load_cn():
    try:
        return json.load(open("workboard2_cn.json", encoding="utf-8"))
    except Exception:
        return {}

def send(data, dry=False, no_push=False):
    card = build_card(data)
    # 防御：确保是合法 JSON
    json.loads(card)
    print("==== CARD PREVIEW (first 1200 chars) ====")
    print(card[:1200])
    print("==== END CARD ====")
    if no_push or not OPEN_ID:
        print("[5/5] skip Feishu send (no_push=%s, OPEN_ID configured=%s)" % (no_push, bool(OPEN_ID)))
        return
    print("[5/5] sending Feishu interactive card (dry=%s, as bot) ..." % dry)
    tag = os.environ.get("PUSH_TAG", "")
    idek = "mailboard-" + TODAY.strftime("%Y-%m-%d") + "-cn" + tag
    send_args = ["im", "+messages-send", "--as", "bot", "--user-id", OPEN_ID,
                 "--content", card, "--msg-type", "interactive", "--idempotency-key", idek]
    if dry:
        send_args.append("--dry-run")
    out = lark(send_args, timeout=60)
    print("  send card:", out.strip()[:200])
    # attach HTML file
    fpath = "mail_workboard2.html"
    if os.path.exists(fpath):
        f_args = ["im", "+messages-send", "--as", "bot", "--user-id", OPEN_ID,
                  "--file", fpath, "--idempotency-key", idek + "-file"]
        if dry:
            f_args.append("--dry-run")
        out2 = lark(f_args, timeout=60)
        print("  send file:", out2.strip()[:200])
    # 截止前1天：需反馈待办 飞书催办提醒（@陈哲）
    items = chase_items(data)
    if items:
        cm = chase_message(items)
        cidek = "chase-" + (TODAY + datetime.timedelta(days=1)).strftime("%Y-%m-%d") + tag
        c_args = ["im", "+messages-send", "--as", "bot", "--user-id", OPEN_ID,
                  "--markdown", cm, "--idempotency-key", cidek]
        if dry:
            c_args.append("--dry-run")
        out3 = lark(c_args, timeout=60)
        print("  send chase:", out3.strip()[:200])
    else:
        print("  chase: 明日无「需反馈」截止项")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="dry-run send (no real push)")
    ap.add_argument("--no-push", action="store_true", help="generate data+HTML only, do NOT push to Feishu")
    ap.add_argument("--skip-pull", action="store_true", help="reuse existing email_detail.json/bodies")
    args = ap.parse_args()

    if args.skip_pull and os.path.exists("email_detail.json"):
        print("[skip] reuse existing data")
    else:
        build()
    generate()
    data = json.load(open("workboard2_data.json", encoding="utf-8"))
    data["generated_at"] = GEN_AT
    json.dump(data, open("workboard2_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    send(data, dry=args.dry, no_push=args.no_push)
    print("DONE")

if __name__ == "__main__":
    main()
