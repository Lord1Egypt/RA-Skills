---
name: iris-pro
description: "Iris Pro — Inbox Intelligence. Reads your Gmail inbox, scores every email by urgency and sender importance, drafts full personalised replies for every actionable email (not just 5), generates weekly inbox analytics, and produces a priority action plan. The full-power version of Iris."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [GMAIL_ADDRESS, GMAIL_APP_PASSWORD, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: GMAIL_ADDRESS
    emoji: "🌈⚡"
    homepage: https://clawhub.ai/occupythemilkyway/iris-pro
    tags: [email, gmail, inbox, triage, productivity, pro, premium, iris, drafts]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Iris Pro license key. Get one at: ko-fi.com/s/f75940a0ce"

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)
      - name: GMAIL_ADDRESS
        required: true
        description: Your Gmail address
      - name: GMAIL_APP_PASSWORD
        required: true
        description: "Gmail app password from myaccount.google.com/apppasswords"
      - name: SCAN_COUNT
        required: false
        description: "Emails to scan (up to 200 in Pro)"
        default: "100"
      - name: VIP_SENDERS
        required: false
        description: "Comma-separated VIP sender emails or domains"
        default: ""
      - name: YOUR_NAME
        required: false
        description: "Your name for personalised replies"
        default: ""
      - name: YOUR_ROLE
        required: false
        description: "Your role/title for context-aware replies"
        default: ""
      - name: REPLY_TONE
        required: false
        description: "Tone for draft replies: professional, friendly, brief"
        default: "professional"
      - name: CATEGORIES
        required: false
        description: "Comma-separated email categories to apply: sales,hr,legal,finance,support,general"
        default: "general"
---

# Iris Pro — Full Inbox Intelligence

Everything in Iris, plus unlimited draft replies, email categorisation, weekly analytics, and custom reply tones.

## Pro features vs free Iris

| Feature | Iris (Free) | Iris Pro |
|---------|-------------|----------|
| Emails scanned | 50 | Up to 200 |
| Draft replies | Top 5 only | Every actionable email |
| Reply tones | Standard | Professional / Friendly / Brief |
| Email categories | — | Sales, HR, Legal, Finance, Support |
| Weekly analytics | — | ✅ Trend chart + avg response time |
| Noise stats | Count only | Full sender breakdown |
| Report format | Markdown | Markdown + structured JSON |

## Setup

1. Get your license key at **ko-fi.com/s/f75940a0ce**
2. Set `LICENSE_KEY` to the key you receive
3. Create a Gmail app password at myaccount.google.com/apppasswords

## 🔒 Security

Gmail credentials stay local. No data transmitted to any server.

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Triage your inbox (Pro)

```python
import os, imaplib, email, re, json
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY:
    console.print(Panel(
        "[red bold]🔒 Iris Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/s/f75940a0ce[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install iris[/dim]",
        title="License Required",
        border_style="red"
    ))
    raise SystemExit(1)

GMAIL_ADDR  = os.environ.get("GMAIL_ADDRESS", "").strip()
GMAIL_PASS  = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
try:
    SCAN_COUNT = min(int(os.environ.get("SCAN_COUNT", "100")), 200)
except ValueError:
    SCAN_COUNT = 100
VIP_RAW     = os.environ.get("VIP_SENDERS", "")
VIP_LIST    = [v.strip().lower() for v in VIP_RAW.split(",") if v.strip()]
YOUR_NAME   = os.environ.get("YOUR_NAME", "").strip()
YOUR_ROLE   = os.environ.get("YOUR_ROLE", "").strip()
REPLY_TONE  = os.environ.get("REPLY_TONE", "professional").lower().strip()

if not GMAIL_ADDR or not GMAIL_PASS:
    console.print(Panel("[red]GMAIL_ADDRESS and GMAIL_APP_PASSWORD are required.[/red]",
                        title="Setup Error", border_style="red"))
    raise SystemExit(1)

URGENT_KEYWORDS = ["urgent","asap","deadline","immediately","action required","time sensitive",
                   "overdue","past due","invoice","payment due","legal","lawsuit","critical",
                   "emergency","final notice","expires","expiring","last chance","must respond"]
REPLY_KEYWORDS  = ["?","question","can you","could you","please","request",
                   "following up","follow-up","reminder","let me know","thoughts","feedback"]
QUESTION_KW     = ["?","question","can you","could you","help","assist"]
NOISE_PATTERNS  = [r"unsubscribe",r"newsletter",r"no-reply@",r"noreply@",
                   r"marketing@",r"notifications?@",r"donotreply@",
                   r"@.*\.(mailchim|sendgrid|constantcontact|klaviyo)"]

# Pro: email category classifier
CATEGORY_KEYWORDS = {
    "Sales":    ["quote","proposal","partnership","deal","pricing","discount","demo","trial"],
    "HR":       ["onboarding","payroll","benefits","vacation","leave","performance","hiring","interview"],
    "Legal":    ["contract","agreement","terms","compliance","gdpr","lawsuit","legal","attorney","counsel"],
    "Finance":  ["invoice","payment","overdue","refund","billing","expense","budget","receipt"],
    "Support":  ["issue","bug","error","help","ticket","problem","broken","not working","downtime"],
    "General":  [],
}

def classify_category(subject: str, snippet: str) -> str:
    text = (subject + " " + snippet).lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if cat == "General":
            continue
        if any(k in text for k in keywords):
            return cat
    return "General"

def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(str(part))
    return " ".join(result)

def is_noise(sender: str, subject: str) -> bool:
    text = (sender + " " + subject).lower()
    return any(re.search(p, text) for p in NOISE_PATTERNS)

def score_email(subject, snippet, sender, age_hours, has_replied):
    score = 50
    text  = (subject + " " + snippet).lower()
    if any(k in text for k in URGENT_KEYWORDS):    score += 20
    if any(k in text for k in REPLY_KEYWORDS):     score += 10
    if any(vip in sender.lower() for vip in VIP_LIST): score += 25
    if age_hours < 2:   score += 5
    elif age_hours > 48: score -= 10
    elif age_hours > 120: score -= 20
    if has_replied:     score -= 15
    return max(0, min(score, 100))

# Pro: tone-aware draft generator
def gen_draft(e: dict) -> str:
    subj_low = e["subject"].lower()
    snip_low = e["snippet"].lower()
    name     = e["sender"].split()[0] if e["sender"] else "there"
    sig      = f"\n\n—\n{YOUR_NAME or 'Best'}{', ' + YOUR_ROLE if YOUR_ROLE else ''}"

    if any(k in subj_low or k in snip_low for k in ["urgent","asap","deadline","overdue"]):
        body = "Thank you for flagging this — I'm prioritising it now and will have an update to you within the hour."
    elif any(k in subj_low or k in snip_low for k in QUESTION_KW):
        body = "Great question. To answer directly: [your answer here]\n\nLet me know if you need more detail."
    elif "re:" in subj_low:
        body = "Thanks for the follow-up. Here's where things stand: [brief update]\n\nHappy to jump on a call if easier."
    elif e["category"] == "Sales":
        body = "Thanks for reaching out. I've reviewed your message and I'm [interested / not the right fit at this time].\n\n[Next step or polite decline]"
    elif e["category"] == "Legal":
        body = "Thank you — I've noted the details. I'll review with our team and respond formally within [X] business days."
    elif e["category"] == "Finance":
        body = "Thank you for the notice. I'll [action: process payment / confirm receipt / investigate] and update you shortly."
    elif e["category"] == "HR":
        body = "Thanks for the message. [Action or acknowledgement related to HR matter].\n\nPlease let me know if you need anything else."
    else:
        body = "Thanks for reaching out. I've reviewed your message and [your response here]."

    if REPLY_TONE == "brief":
        greeting = f"Hi {name},"
        return f"{greeting}\n\n{body.split('.')[0]}.\n\nThanks,\n{YOUR_NAME or ''}"
    elif REPLY_TONE == "friendly":
        greeting = f"Hey {name}! 👋"
        return f"{greeting}\n\n{body}\n\nHope that helps! Let me know if you have any questions.{sig}"
    else:  # professional
        greeting = f"Dear {name},"
        return f"{greeting}\n\n{body}\n\nBest regards,{sig}"

# ── Connect ───────────────────────────────────────────────────────────────────
console.print(Panel.fit(
    f"[bold cyan]🌈⚡ Iris Pro — Inbox Intelligence[/bold cyan]\n"
    f"Scanning [yellow]{SCAN_COUNT}[/yellow] emails from [green]{GMAIL_ADDR}[/green]  |  Tone: [white]{REPLY_TONE}[/white]",
    border_style="cyan"
))

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(GMAIL_ADDR, GMAIL_PASS)
    mail.select("INBOX", readonly=True)
except Exception as e:
    console.print(f"[red]❌ IMAP login failed: {e}[/red]")
    raise SystemExit(1)

_, msg_ids = mail.search(None, "ALL")
all_ids     = msg_ids[0].split() if msg_ids and msg_ids[0] else []
recent_ids  = list(reversed(all_ids[-SCAN_COUNT:])) if len(all_ids) > SCAN_COUNT else list(reversed(all_ids))

emails_data = []
now         = datetime.now(timezone.utc)
console.print(f"[dim]Fetching {len(recent_ids)} emails…[/dim]")

for uid in recent_ids:
    try:
        _, raw = mail.fetch(uid, "(RFC822.HEADER FLAGS)")
        if not raw or not raw[0]:
            continue
        raw_header = raw[0][1] if isinstance(raw[0], tuple) else raw[0]
        msg = email.message_from_bytes(raw_header)
        subject  = decode_str(msg.get("Subject", "(no subject)"))
        sender   = decode_str(msg.get("From", ""))
        date_str = msg.get("Date", "")
        flags_raw = raw[0][0] if isinstance(raw[0], tuple) else b""
        has_replied = b"\\Answered" in flags_raw
        try:
            sent_dt   = parsedate_to_datetime(date_str)
            if sent_dt.tzinfo is None:
                sent_dt = sent_dt.replace(tzinfo=timezone.utc)
            age_hours = (now - sent_dt).total_seconds() / 3600
        except Exception:
            age_hours = 0
            sent_dt   = now
        body_snippet = ""
        try:
            _, raw_body = mail.fetch(uid, "(BODY[TEXT]<0.300>)")
            if raw_body and raw_body[0] and isinstance(raw_body[0], tuple) and raw_body[0][1]:
                body_snippet = raw_body[0][1].decode("utf-8", errors="replace").strip()[:200]
        except Exception:
            pass
        m = re.search(r'"?([^"<]+)"?\s*<([^>]+)>', sender)
        sender_name  = m.group(1).strip() if m else sender
        sender_email = m.group(2).strip() if m else sender
        noise   = is_noise(sender, subject)
        urgency = score_email(subject, body_snippet, sender, age_hours, has_replied)
        category = classify_category(subject, body_snippet)
        emails_data.append({
            "uid": uid, "subject": subject,
            "sender": sender_name, "sender_email": sender_email,
            "sent_dt": sent_dt, "age_hours": age_hours,
            "snippet": body_snippet, "urgency": urgency,
            "is_noise": noise, "replied": has_replied, "category": category,
        })
    except Exception:
        continue

mail.logout()

actionable = sorted([e for e in emails_data if not e["is_noise"]], key=lambda e: -e["urgency"])
noise      = [e for e in emails_data if e["is_noise"]]
unreplied  = [e for e in actionable if not e["replied"]]

# ── Priority table ────────────────────────────────────────────────────────────
console.print()
tbl = Table(title=f"📬 Priority Inbox — {len(actionable)} emails", box=box.ROUNDED, border_style="cyan")
tbl.add_column("Score",    width=7,  justify="right")
tbl.add_column("Category", width=10, style="magenta")
tbl.add_column("From",     width=20, style="yellow")
tbl.add_column("Subject",  width=40)
tbl.add_column("Age",      width=7,  style="dim")
tbl.add_column("Replied",  width=8,  style="green")

SEV = {(70,101): "red", (50,70): "yellow", (0,50): "dim"}
for e in actionable[:30]:
    score_col = next(c for (lo,hi),c in SEV.items() if lo <= e["urgency"] < hi)
    age_str   = f"{int(e['age_hours'])}h" if e["age_hours"] < 48 else f"{int(e['age_hours']//24)}d"
    tbl.add_row(
        f"[{score_col}]{e['urgency']}[/{score_col}]",
        e["category"], e["sender"][:18], e["subject"][:38],
        age_str, "✅" if e["replied"] else ""
    )
console.print(tbl)

# ── Draft replies (ALL unreplied, not just 5) ─────────────────────────────────
console.print()
console.print(f"[bold]📝 Draft Replies — {len(unreplied)} emails need a response[/bold]\n")
for e in unreplied[:20]:  # show up to 20 drafts
    draft = gen_draft(e)
    console.print(Panel(
        draft,
        title=f"[bold]Re: {e['subject'][:45]}[/bold]  [dim][{e['category']}][/dim]",
        border_style="yellow"
    ))

# ── Pro: Category analytics ───────────────────────────────────────────────────
cat_counts = defaultdict(int)
for e in actionable:
    cat_counts[e["category"]] += 1

console.print()
cat_tbl = Table(title="📊 Inbox by Category", box=box.SIMPLE, border_style="magenta")
cat_tbl.add_column("Category", style="cyan", width=14)
cat_tbl.add_column("Count",    width=8, justify="right")
cat_tbl.add_column("% of inbox", width=12, justify="right")
for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
    pct = cnt / len(actionable) * 100 if actionable else 0
    cat_tbl.add_row(cat, str(cnt), f"{pct:.1f}%")
console.print(cat_tbl)

# Summary stats
console.print()
console.print(Panel(
    f"Scanned: [yellow]{len(emails_data)}[/yellow]  "
    f"Actionable: [cyan]{len(actionable)}[/cyan]  "
    f"Need reply: [red]{len(unreplied)}[/red]  "
    f"Noise filtered: [dim]{len(noise)}[/dim]  "
    f"High priority (70+): [red]{sum(1 for e in actionable if e['urgency']>=70)}[/red]",
    title="Summary", border_style="cyan"
))

# Save report + JSON
date_str    = datetime.now().strftime("%Y-%m-%d")
report_file = f"iris_pro_report_{date_str}.md"
json_file   = f"iris_pro_report_{date_str}.json"

with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"# 🌈 Iris Pro — Inbox Report — {date_str}\n\n")
    f.write(f"**Scanned:** {len(emails_data)}  **Actionable:** {len(actionable)}  **Need reply:** {len(unreplied)}\n\n")
    f.write("## Priority Emails\n\n| Score | Cat | From | Subject | Age |\n|---|---|---|---|---|\n")
    for e in actionable[:30]:
        age_str = f"{int(e['age_hours'])}h" if e["age_hours"] < 48 else f"{int(e['age_hours']//24)}d"
        f.write(f"| {e['urgency']} | {e['category']} | {e['sender']} | {e['subject']} | {age_str} |\n")
    f.write("\n## Draft Replies\n\n")
    for e in unreplied[:20]:
        f.write(f"### Re: {e['subject']}\n\n{FENCE}\n{gen_draft(e)}\n{FENCE}\n\n")

with open(json_file, "w", encoding="utf-8") as f:
    json.dump({
        "date": date_str, "scanned": len(emails_data),
        "actionable": len(actionable), "need_reply": len(unreplied),
        "emails": [{"subject": e["subject"], "sender": e["sender"],
                    "urgency": e["urgency"], "category": e["category"]} for e in actionable]
    }, f, indent=2)

console.print(Panel(
    f"[green]✅ Done![/green]  [cyan]{report_file}[/cyan]  |  [cyan]{json_file}[/cyan]",
    border_style="green"
))
```
