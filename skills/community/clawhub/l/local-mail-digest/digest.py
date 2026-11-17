#!/usr/bin/env python3
# 本地邮件摘要生成器（技能组件版）：零依赖，数据不出电脑
# 定位：本技能供 Python / Codex / Claude / WorkBuddy / Hermes / OpenClaw 等宿主调用，
#       调度与自动化由宿主负责；本技能只做"本地拉邮件→结构化摘要"。
# 入口：--imap 服务器,邮箱(或仅邮箱自动推断) / --txt 文件 / --input JSON|.eml|.mbox
# 输出：HTML(人看) + Markdown + JSON(给 Agent 框架消费)
# 可选增强：--llm 本地端点(Ollama/Hermes 兼容 OpenAI 格式)做真 AI 理解，不传则降级关键词规则
import json, sys, re, html, os, argparse, mailbox, imaplib, getpass, smtplib, ssl, urllib.request, urllib.error
from email import message_from_bytes
from email.header import decode_header, make_header

HIGH = ["紧急", "urgent", "asap", "截止", "请确认", "请处理", "请审批", "请回复",
        "审批", "review", "尽快", "马上", "务必", "deadline", "ddl", "action required"]
MID = ["会议", "周报", "月报", "更新", "进度", "同步", "通知", "提醒"]
TODO_PAT = re.compile(r'(?:请|需要|待|行动项|action|todo)[^。\n]{2,40}', re.I)
DDL_PAT = re.compile(
    r'(?:'
    r'(截止|deadline|ddl|due(?:\s+by)?|到期|前完成|前提交)[^。\n]{0,12}?'
    r'(\d{1,2}\s*[月./\-]\s*\d{1,2}\s*日?|\d{4}\s*[年./\-]\s*\d{1,2}\s*[月./\-]\s*\d{1,2}\s*日?)'
    r'|'
    r'(\d{1,2}\s*[月./\-]\s*\d{1,2}\s*日?)[前之]?\s*(?:提交|完成|截止|到期|前)'
    r')',
    re.I)
DEFAULT_PROJECTS = ["OpenClaw", "年度汇报", "官网改版", "客户", "招聘", "项目"]

IMAP_PRESETS = {
    "qq.com": ("imap.qq.com", 993, "ssl"),
    "foxmail.com": ("imap.qq.com", 993, "ssl"),
    "163.com": ("imap.163.com", 993, "ssl"),
    "126.com": ("imap.126.com", 993, "ssl"),
    "outlook.com": ("outlook.office365.com", 993, "ssl"),
    "hotmail.com": ("outlook.office365.com", 993, "ssl"),
    "live.com": ("outlook.office365.com", 993, "ssl"),
    "gmail.com": ("imap.gmail.com", 993, "ssl"),
}


def decode_mime(s):
    try:
        return str(make_header(decode_header(s or "")))
    except Exception:
        return s or ""


def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_payload(decode=True).decode("utf-8", "ignore")
                except Exception:
                    return part.get_payload(decode=True).decode("gbk", "ignore")
        return ""
    try:
        return msg.get_payload(decode=True).decode("utf-8", "ignore")
    except Exception:
        return msg.get_payload(decode=True).decode("gbk", "ignore")


def eml_to_dict(msg):
    return {
        "from": decode_mime(msg.get("From", "")),
        "subject": decode_mime(msg.get("Subject", "")),
        "date": decode_mime(msg.get("Date", "")),
        "body": get_body(msg),
        "read": False,
    }


def _decode_folder_name(raw_bytes):
    try:
        return imaplib.utf7.decode(raw_bytes).strip('"')
    except Exception:
        try:
            return raw_bytes.decode("utf-8", "ignore").strip('"')
        except Exception:
            return str(raw_bytes)


def _pick_inbox(conn):
    try:
        typ, raw = conn.list()
    except Exception:
        return "INBOX"
    if not raw:
        return "INBOX"
    for r in raw:
        if not r:
            continue
        m = re.search(rb'\)\s+\S+\s+"?([^"]+)"?\s*$', r) or re.search(rb'"([^"]+)"\s*$', r)
        if not m:
            continue
        name = _decode_folder_name(m.group(1))
        if name.upper() == "INBOX" or name.lower() == "inbox" or "收件箱" in name:
            return name
    return "INBOX"


def _connect(server, user, pwd):
    last_err = None
    for port, use_ssl in [(993, True), (143, False)]:
        try:
            if use_ssl:
                conn = imaplib.IMAP4_SSL(server, port, timeout=15)
            else:
                conn = imaplib.IMAP4(server, port, timeout=15)
                ctx = ssl.create_default_context()
                conn.starttls(ctx)
            conn.login(user, pwd)
            return conn
        except imaplib.IMAP4.error as ex:
            raise SystemExit(
                f"[IMAP] 认证失败：{ex}\n"
                f"       多数邮箱需用授权码/应用专用密码而非登录密码(QQ/163 在邮箱设置生成)。")
        except Exception as ex:
            last_err = ex
            continue
    raise SystemExit(
        f"[IMAP] 连接失败：{last_err}\n"
        f"       检查服务器地址、网络、端口是否被防火墙拦截。")


def load_imap(server_user, limit=50):
    if "," in server_user:
        server, user = server_user.split(",", 1)
    else:
        user = server_user
        domain = user.split("@")[-1].lower() if "@" in user else ""
        preset = IMAP_PRESETS.get(domain)
        if not preset:
            raise SystemExit(
                f"[IMAP] 无法推断 {domain} 的服务器，请用 服务器,邮箱 格式，"
                f"例：imap.qq.com,{user}")
        server = preset[0]
    pwd = getpass.getpass(f"请输入 {user} 的授权码(应用专用密码,不会显示): ")
    conn = _connect(server, user, pwd)
    inbox = _pick_inbox(conn)
    try:
        conn.select(inbox)
    except Exception:
        conn.select("INBOX")
    typ, data = conn.search(None, "ALL")
    ids = data[0].split() if data and data[0] else []
    ids = ids[-limit:]
    out = []
    for i in ids:
        try:
            typ, d = conn.fetch(i, "(RFC822)")
            msg = message_from_bytes(d[0][1])
            out.append(eml_to_dict(msg))
        except Exception:
            continue
    try:
        conn.logout()
    except Exception:
        pass
    if not out:
        print(f"[IMAP] 已从 {inbox} 拉取，但最近 {limit} 封为空。")
    return out


def load_text(path):
    raw = open(path, encoding="utf-8").read()
    blocks = re.split(r'\n={3,}\n|\n-{3,}\n', raw)
    out = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        m = re.search(r'(?:发件人|From)\s*[:：]\s*(.+)', b)
        s = re.search(r'(?:主题|标题|Subject)\s*[:：]\s*(.+)', b)
        body = re.sub(r'(?:发件人|From)\s*[:：].*\n(?:主题|标题|Subject)\s*[:：].*\n?', '', b, flags=re.I).strip()
        out.append({
            "from": m.group(1).strip() if m else "",
            "subject": s.group(1).strip() if s else "",
            "body": body,
            "read": False,
            "date": "",
        })
    return out


def load_json(path):
    data = json.load(open(path, encoding="utf-8"))
    for e in data:
        e.setdefault("read", True)
        e.setdefault("date", "")
        e.setdefault("from", "")
        e.setdefault("subject", "")
        e.setdefault("body", "")
    return data


def load_eml(path):
    with open(path, "rb") as f:
        return eml_to_dict(message_from_bytes(f.read()))


def load_eml_dir(d):
    out = []
    for fn in sorted(os.listdir(d)):
        if fn.lower().endswith(".eml"):
            out.append(load_eml(os.path.join(d, fn)))
    return out


def load_mbox(path):
    out = []
    for m in mailbox.mbox(path):
        out.append(eml_to_dict(m))
    return out


def load_input(src):
    if os.path.isdir(src):
        return load_eml_dir(src)
    low = src.lower()
    if low.endswith(".json"):
        return load_json(src)
    if low.endswith(".eml"):
        return [load_eml(src)]
    if low.endswith(".mbox"):
        return load_mbox(src)
    raise SystemExit(f"不支持的输入格式: {src}")


def score(em):
    s = 0
    text = (em.get("subject", "") + " " + em.get("body", "")).lower()
    # 未读≠重要，不加权；高优由"是否含紧急/截止/需行动"类词决定，而非靠分数累加
    has_high = False
    for k in HIGH:
        if k.lower() in text:
            s += 3
            has_high = True
    for k in MID:
        if k.lower() in text:
            s += 1
    em["_has_high"] = has_high
    return s


def project(em, projects):
    m = re.search(r"\[([^\]]+)\]", em.get("subject", ""))
    if m:
        return m.group(1)
    body = em.get("body", "").lower()
    for kw in projects:
        if kw.lower() in body or kw.lower() in em.get("subject", "").lower():
            return kw
    return "其他"


def todos(em):
    return [t.strip() for t in TODO_PAT.findall(em.get("body", ""))][:3]


def ddls(em):
    text = em.get("body", "") + " " + em.get("subject", "")
    out = []
    for m in DDL_PAT.finditer(text):
        d = m.group(2) or m.group(3)
        if d:
            out.append(d.strip())
    return list(dict.fromkeys(out))[:2]


def annotate_rules(data, projects):
    for em in data:
        em["_score"] = score(em)
        em["_proj"] = project(em, projects)
        em["_todos"] = todos(em)
        em["_ddl"] = ddls(em)
        em.setdefault("_summary", "")


def classify(data):
    data.sort(key=lambda e: -e.get("_score", 0))
    # 高优=含紧急/行动类信号；中=含普通信号(会议/周报/进度等)；低=无信号
    high = [e for e in data if e.get("_has_high")]
    mid = [e for e in data if not e.get("_has_high") and e.get("_score", 0) > 0]
    low = [e for e in data if not e.get("_has_high") and e.get("_score", 0) <= 0]
    return high, mid, low


def _extract_json(text):
    text = text.strip()
    text = re.sub(r'^```(?:json)?', '', text).strip()
    text = re.sub(r'```$', '', text).strip()
    for a, b in [('[', ']'), ('{', '}')]:
        s, e = text.find(a), text.rfind(b)
        if s != -1 and e != -1:
            try:
                return json.loads(text[s:e + 1])
            except Exception:
                continue
    return None


def llm_enhance(data, endpoint, model="hermes3"):
    sys_p = (
        "你是邮件助理。对每封邮件判断：优先级(high/mid/low)、项目归类、待办事项、"
        "截止日期、一句话中文摘要。只返回 JSON 数组，元素字段："
        "from, subject, priority, project, todos(数组), ddl(数组), summary(字符串)。"
    )
    batch = [{
        "from": e.get("from", ""),
        "subject": e.get("subject", ""),
        "body": e.get("body", "")[:1500]
    } for e in data]
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_p},
            {"role": "user", "content": json.dumps(batch, ensure_ascii=False)}
        ],
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        endpoint, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            resp = json.loads(r.read().decode("utf-8"))
        content = resp["choices"][0]["message"]["content"]
        result = _extract_json(content)
        if not isinstance(result, list):
            print("[LLM] 返回非数组，降级关键词规则")
            return False
        by_key = {(e.get("from", ""), e.get("subject", "")): e for e in data}
        for item in result:
            key = (item.get("from", ""), item.get("subject", ""))
            e = by_key.get(key)
            if not e:
                continue
            e["_proj"] = item.get("project", "其他")
            e["_todos"] = (item.get("todos") or [])[:3]
            e["_ddl"] = (item.get("ddl") or [])[:2]
            e["_summary"] = item.get("summary", "")
            pr = (item.get("priority") or "mid").lower()
            e["_score"] = {"high": 5, "mid": 2, "low": 0}.get(pr, 2)
        print(f"[LLM] 已用本地模型增强 {len(result)} 封")
        return True
    except Exception as ex:
        print(f"[LLM] 增强失败，降级关键词规则: {ex}")
        return False


def clean_html(s):
    """把 HTML 邮件正文清洗成纯文本（零依赖）。真实邮件大量是 HTML，避免标签污染分类/抽取。"""
    if not s:
        return ""
    if "<" not in s:
        return s.strip()
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"(?is)<!--.*?-->", " ", s)
    s = re.sub(r"(?is)<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\r]+", " ", s)
    s = re.sub(r"\n[ \t]*\n+", "\n", s)
    return s.strip()


def esc(s):
    return html.escape(str(s))


def card_html(e):
    t = "".join(f'<li class="todo">▸ {esc(x)}</li>' for x in e["_todos"])
    d = "".join(f'<span class="ddl">⏰ {esc(x)}</span>' for x in e["_ddl"])
    summ = f'<div class="sum">{esc(e["_summary"])}</div>' if e.get("_summary") else ""
    return f'''<div class="card">
  <div class="ch"><span class="from">{esc(e.get("from",""))}</span>
  <span class="sub">{esc(e.get("subject",""))}</span></div>
  <div class="bd">{esc(e.get("body","")[:160])}</div>
  {summ}
  {f'<div class="ddls">{d}</div>' if d else ''}
  {f'<ul class="todos">{t}</ul>' if t else ''}
</div>'''


def render_html(data, high, mid, low, out):
    proj = {}
    for e in high:
        proj.setdefault(e["_proj"], []).append(e)
    all_todos = [(e.get("subject", ""), t) for e in data for t in e["_todos"]]
    proj_html = "".join(
        f'<h3 class="pg">▣ {esc(p)}</h3>' + "".join(card_html(e) for e in lst)
        for p, lst in proj.items())
    h = f'''<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>邮件摘要 {len(data)} 封</title><style>
*{{box-sizing:border-box}} body{{font-family:-apple-system,"Microsoft YaHei",sans-serif;margin:0;background:#f5f6f8;color:#1a1a1a}}
.wrap{{max-width:820px;margin:24px auto;padding:0 16px}}
.hd{{background:linear-gradient(135deg,#1e3a8a,#0ea5e9);color:#fff;padding:20px 24px;border-radius:14px}}
.hd h1{{margin:0;font-size:22px}} .hd p{{margin:6px 0 0;opacity:.85}}
.sec{{margin:22px 0}} .sec h2{{font-size:16px;border-left:4px solid #1e3a8a;padding-left:10px;margin:0 0 12px}}
.card{{background:#fff;border-radius:10px;padding:14px 16px;margin:10px 0;box-shadow:0 1px 3px rgba(0,0,0,.08)}}
.ch{{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}}
.from{{font-weight:700;color:#1e3a8a}} .sub{{color:#333}}
.bd{{color:#555;font-size:13px;margin-top:6px;line-height:1.5}}
.sum{{color:#0f766e;font-size:13px;margin-top:6px;font-style:italic}}
.todos{{margin:8px 0 0;padding-left:2px;list-style:none}} .todo{{color:#b91c1c;font-size:13px;padding:2px 0}}
.ddl{{color:#d97706;font-size:12px;margin-right:10px}} .ddls{{margin-top:6px}}
.pg{{color:#0ea5e9;margin:16px 0 4px}}
@media print{{body{{background:#fff}}.hd{{background:#1e3a8a!important;-webkit-print-color-adjust:exact}}}}
</style></head><body><div class="wrap">
<div class="hd"><h1>📥 本地邮件摘要</h1>
<p>共 {len(data)} 封 · 高优 {len(high)} · 中 {len(mid)} · 低 {len(low)} · 数据未出电脑</p></div>
<div class="sec"><h2>🔴 今日重点（高优先级）</h2>{proj_html or "<p>无</p>"}</div>
<div class="sec"><h2>✅ 待办清单（共 {len(all_todos)} 条）</h2>
<ul class="todos">''' + "".join(
        f'<li class="todo">▸ [{esc(s)}] {esc(t)}</li>' for s, t in all_todos) + f'''</ul></div>
<div class="sec"><h2>🟡 普通（{len(mid)}）</h2>{''.join(card_html(e) for e in mid) or "<p>无</p>"}</div>
<div class="sec"><h2>⚪ 可稍后（{len(low)}）</h2>{''.join(card_html(e) for e in low) or "<p>无</p>"}</div>
</div></body></html>'''
    open(out, "w", encoding="utf-8").write(h)
    return len(all_todos)


def render_md(data, high, mid, low, out):
    lines = [f"# 本地邮件摘要（共 {len(data)} 封）\n"]
    lines.append(f"> 高优 {len(high)} · 中 {len(mid)} · 低 {len(low)} · 数据未出电脑\n")
    proj = {}
    for e in high:
        proj.setdefault(e["_proj"], []).append(e)
    lines.append("## 🔴 今日重点\n")
    for p, lst in proj.items():
        lines.append(f"### ▣ {p}\n")
        for e in lst:
            lines.append(f"- **{e.get('from','')}**：{e.get('subject','')}")
            if e.get("_summary"):
                lines.append(f"  - 摘要：{e['_summary']}")
            if e["_ddl"]:
                lines.append(f"  - ⏰ 截止：{', '.join(e['_ddl'])}")
            for t in e["_todos"]:
                lines.append(f"  - [ ] {t}")
    todos_all = [(e.get("subject", ""), t) for e in data for t in e["_todos"]]
    lines.append(f"\n## ✅ 待办清单（{len(todos_all)} 条）\n")
    for s, t in todos_all:
        lines.append(f"- [ ] {t} （{s}）")
    lines.append(f"\n## 🟡 普通（{len(mid)}）\n")
    for e in mid:
        lines.append(f"- {e.get('from','')}：{e.get('subject','')}")
    lines.append(f"\n## ⚪ 可稍后（{len(low)}）\n")
    for e in low:
        lines.append(f"- {e.get('from','')}：{e.get('subject','')}")
    open(out, "w", encoding="utf-8").write("\n".join(lines))


def render_json(data, high, mid, low, out):
    def prio(e):
        return "high" if e in high else "mid" if e in mid else "low"
    obj = {
        "total": len(data),
        "high": len(high), "mid": len(mid), "low": len(low),
        "emails": [{
            "from": e.get("from", ""),
            "subject": e.get("subject", ""),
            "date": e.get("date", ""),
            "priority": prio(e),
            "project": e.get("_proj", ""),
            "todos": e.get("_todos", []),
            "ddl": e.get("_ddl", []),
            "summary": e.get("_summary", ""),
            "body_excerpt": e.get("body", "")[:300],
        } for e in data]
    }
    json.dump(obj, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def build_push_text(data, high, mid, low):
    lines = [f"📥 今日邮件摘要（共{len(data)}封·高优{len(high)}）", ""]
    if high:
        lines.append("🔴 今日重点：")
        for e in high[:6]:
            ddl = f" ⏰{','.join(e['_ddl'])}" if e["_ddl"] else ""
            lines.append(f"· [{e['_proj']}] {e.get('from','')}：{e.get('subject','')}{ddl}")
        lines.append("")
    todos_all = [(e.get("subject", ""), t) for e in data for t in e["_todos"]]
    if todos_all:
        lines.append(f"✅ 待办（共{len(todos_all)}条，节选前8）：")
        for s, t in todos_all[:8]:
            lines.append(f"· {t}")
        lines.append("")
    lines.append("（完整版见电脑本地 HTML）")
    return "\n".join(lines)


def push_email(server_user, text, html_body):
    if "," not in server_user:
        raise SystemExit("SMTP 格式: --smtp 服务器,邮箱  例: smtp.qq.com,me@qq.com")
    server, user = server_user.split(",", 1)
    pwd = getpass.getpass(f"请输入 {user} 的 SMTP 授权码(不会显示): ")
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    m = MIMEMultipart("alternative")
    m["From"] = user
    m["To"] = user
    m["Subject"] = Header("📥 今日邮件摘要", "utf-8")
    m.attach(MIMEText(text, "plain", "utf-8"))
    if html_body:
        m.attach(MIMEText(html_body, "html", "utf-8"))
    try:
        if "office365" in server:
            with smtplib.SMTP(server, 587, timeout=15) as s:
                s.starttls(context=ssl.create_default_context())
                s.login(user, pwd)
                s.sendmail(user, [user], m.as_string())
        else:
            with smtplib.SMTP_SSL(server, 465, timeout=15) as s:
                s.login(user, pwd)
                s.sendmail(user, [user], m.as_string())
    except Exception as ex:
        print(f"[推送] 邮件发送失败: {ex}")
        return False
    print(f"[推送] 已发邮件到 {user}")
    return True


def push_webhook(url, text, wh_type="auto"):
    if wh_type == "auto":
        wh_type = "wecom" if "qyapi.weixin" in url else ("feishu" if "feishu" in url else "wecom")
    if wh_type == "wecom":
        payload = {"msgtype": "text", "text": {"content": text}}
    else:
        payload = {"msg_type": "text", "content": {"text": text}}
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = r.read().decode("utf-8")
        print(f"[推送] Webhook({wh_type}) 响应: {resp[:80]}")
        return True
    except Exception as ex:
        print(f"[推送] Webhook 失败: {ex}")
        return False


def main():
    ap = argparse.ArgumentParser(description="本地邮件摘要生成器（技能组件，零依赖）")
    ap.add_argument("--out", help="输出 HTML 路径", default="邮件摘要.html")
    ap.add_argument("--imap", help="IMAP 直连: 服务器,邮箱  或仅 邮箱(自动推断)")
    ap.add_argument("--txt", help="纯文本粘贴文件 (发件人:/主题:/正文, 多封用 --- 分隔)")
    ap.add_argument("--input", help="文件导入: JSON/.eml/.mbox/目录")
    ap.add_argument("--md", help="同时输出 Markdown 路径", default=None)
    ap.add_argument("--json", help="输出结构化 JSON（给 Agent 框架消费）", default=None)
    ap.add_argument("--projects", help="项目关键词，逗号分隔", default=None)
    ap.add_argument("--limit", help="IMAP 拉取最近 N 封", type=int, default=50)
    ap.add_argument("--llm", help="可选本地 LLM 端点(OpenAI 兼容, Ollama/Hermes), 如 http://localhost:11434/v1/chat/completions")
    ap.add_argument("--model", help="LLM 模型名", default="hermes3")
    ap.add_argument("--smtp", help="SMTP 发邮件给自己(手机收): 服务器,邮箱")
    ap.add_argument("--webhook", help="企业微信/飞书机器人 webhook URL(手机弹通知)")
    ap.add_argument("--wh-type", help="webhook 类型: auto/wecom/feishu", default="auto")
    a = ap.parse_args()
    projects = a.projects.split(",") if a.projects else DEFAULT_PROJECTS

    if a.imap:
        data = load_imap(a.imap, a.limit)
    elif a.txt:
        data = load_text(a.txt)
    elif a.input:
        data = load_input(a.input)
    else:
        ap.print_help()
        raise SystemExit("\n需指定 --imap / --txt / --input")

    # 真实邮件大量是 HTML，统一清洗正文，避免标签污染分类/抽取
    for e in data:
        if e.get("body"):
            e["body"] = clean_html(e["body"])

    annotate_rules(data, projects)
    if a.llm:
        llm_enhance(data, a.llm, a.model)
    high, mid, low = classify(data)

    n = render_html(data, high, mid, low, a.out)
    if a.md:
        render_md(data, high, mid, low, a.md)
    if a.json:
        render_json(data, high, mid, low, a.json)
    print(f"生成完成 | 导入{len(data)}封 高优{len(high)} 中{len(mid)} 低{len(low)} 待办{n} | {a.out}"
          + (f" MD:{a.md}" if a.md else "")
          + (f" JSON:{a.json}" if a.json else ""))


if __name__ == "__main__":
    main()
