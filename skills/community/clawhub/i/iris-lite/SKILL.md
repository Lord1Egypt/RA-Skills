---
name: iris-lite
description: "Iris Lite — Inbox Intelligence (Free). Scans your last 25 Gmail emails, shows urgency scores and a priority list, and drafts 2 quick replies. A free taste of what Iris Pro does for your full inbox every day."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [GMAIL_ADDRESS, GMAIL_APP_PASSWORD]
      bins: [python3, pip3]
    primaryEnv: GMAIL_ADDRESS
    emoji: "🌈"
    homepage: https://clawhub.ai/occupythemilkyway/iris-lite
    tags: [email, gmail, inbox, triage, productivity, free, lite, iris]
    envVars:
      - name: GMAIL_ADDRESS
        required: true
        description: Your Gmail address
      - name: GMAIL_APP_PASSWORD
        required: true
        description: "Gmail app password from myaccount.google.com/apppasswords"
      - name: YOUR_NAME
        required: false
        description: Your name for draft replies
        default: ""
---

# Iris Lite — Free Inbox Triage

Scan your last 25 emails and get a quick priority list with 2 draft replies.

## Free vs Pro

| Feature | Iris Lite (Free) | Iris Pro |
|---------|-----------------|----------|
| Emails scanned | **25** | Up to 200 |
| Draft replies | **2** | Every actionable email |
| Email categories | ❌ | ✅ Sales, HR, Legal, Finance |
| Reply tones | ❌ | Professional / Friendly / Brief |
| Weekly analytics | ❌ | ✅ |
| JSON export | ❌ | ✅ |

👉 **Upgrade:** `openclaw skills install iris-pro` — get your key at **ko-fi.com/s/f75940a0ce**

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 — Quick inbox scan (Lite)

```python
import os, imaplib, email, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

GMAIL_ADDR = os.environ.get("GMAIL_ADDRESS", "").strip()
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
YOUR_NAME  = os.environ.get("YOUR_NAME", "").strip()

# Lite hard limits
SCAN_LIMIT   = 25
DRAFT_LIMIT  = 2

if not GMAIL_ADDR or not GMAIL_PASS:
    console.print(Panel(
        "[red]GMAIL_ADDRESS and GMAIL_APP_PASSWORD are required.[/red]\n\n"
        "App password: myaccount.google.com/apppasswords",
        title="Setup Required", border_style="red"))
    raise SystemExit(1)

URGENT_KEYWORDS = ["urgent","asap","deadline","immediately","overdue","payment","invoice","emergency"]
NOISE_PATTERNS  = [r"unsubscribe",r"newsletter",r"no-reply@",r"noreply@",r"marketing@"]

def decode_str(s):
    if not s: return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(str(part))
    return " ".join(result)

def is_noise(sender, subject):
    return any(re.search(p, (sender+subject).lower()) for p in NOISE_PATTERNS)

def score_email(subject, snippet, sender, age_hours, has_replied):
    score = 50
    text  = (subject + " " + snippet).lower()
    if any(k in text for k in URGENT_KEYWORDS): score += 20
    if "?" in text: score += 10
    if age_hours > 48: score -= 10
    if has_replied: score -= 15
    return max(0, min(score, 100))

console.print(Panel.fit(
    f"[bold cyan]🌈 Iris Lite — Quick Inbox Scan[/bold cyan]\n"
    f"Scanning last [yellow]{SCAN_LIMIT}[/yellow] emails from [green]{GMAIL_ADDR}[/green]\n"
    f"[dim]Lite: 25 emails, 2 drafts — upgrade to Pro for full inbox coverage[/dim]",
    border_style="cyan"
))

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(GMAIL_ADDR, GMAIL_PASS)
    mail.select("INBOX", readonly=True)
except Exception as e:
    console.print(f"[red]❌ Login failed: {e}\nCheck GMAIL_ADDRESS and GMAIL_APP_PASSWORD.[/red]")
    raise SystemExit(1)

_, msg_ids = mail.search(None, "ALL")
all_ids    = msg_ids[0].split() if msg_ids and msg_ids[0] else []
recent_ids = list(reversed(all_ids[-SCAN_LIMIT:])) if len(all_ids) > SCAN_LIMIT else list(reversed(all_ids))

emails_data = []
now = datetime.now(timezone.utc)
for uid in recent_ids:
    try:
        _, raw = mail.fetch(uid, "(RFC822.HEADER FLAGS)")
        if not raw or not raw[0]: continue
        raw_header  = raw[0][1] if isinstance(raw[0], tuple) else raw[0]
        msg         = email.message_from_bytes(raw_header)
        subject     = decode_str(msg.get("Subject","(no subject)"))
        sender      = decode_str(msg.get("From",""))
        flags_raw   = raw[0][0] if isinstance(raw[0], tuple) else b""
        has_replied = b"\\Answered" in flags_raw
        try:
            sent_dt   = parsedate_to_datetime(msg.get("Date",""))
            if sent_dt.tzinfo is None: sent_dt = sent_dt.replace(tzinfo=timezone.utc)
            age_hours = (now - sent_dt).total_seconds() / 3600
        except Exception:
            age_hours = 0
        body_snippet = ""
        try:
            _, rb = mail.fetch(uid, "(BODY[TEXT]<0.150>)")
            if rb and rb[0] and isinstance(rb[0], tuple) and rb[0][1]:
                body_snippet = rb[0][1].decode("utf-8", errors="replace").strip()[:100]
        except Exception:
            pass
        m = re.search(r'"?([^"<]+)"?\s*<([^>]+)>', sender)
        sender_name = m.group(1).strip() if m else sender
        noise   = is_noise(sender, subject)
        urgency = score_email(subject, body_snippet, sender, age_hours, has_replied)
        emails_data.append({
            "subject": subject, "sender": sender_name, "age_hours": age_hours,
            "urgency": urgency, "is_noise": noise, "replied": has_replied, "snippet": body_snippet,
        })
    except Exception:
        continue

mail.logout()

actionable = sorted([e for e in emails_data if not e["is_noise"]], key=lambda e: -e["urgency"])
noise_count = sum(1 for e in emails_data if e["is_noise"])

console.print()
tbl = Table(title=f"📬 Priority Inbox — Top {min(len(actionable), 15)} of {len(actionable)}",
            box=box.ROUNDED, border_style="cyan")
tbl.add_column("Score", width=7, justify="right")
tbl.add_column("From",  width=22, style="yellow")
tbl.add_column("Subject", width=42)
tbl.add_column("Age",   width=6, style="dim")

for e in actionable[:15]:
    sc  = "red" if e["urgency"] >= 70 else "yellow" if e["urgency"] >= 50 else "dim"
    age = f"{int(e['age_hours'])}h" if e["age_hours"] < 48 else f"{int(e['age_hours']//24)}d"
    tbl.add_row(f"[{sc}]{e['urgency']}[/{sc}]", e["sender"][:20], e["subject"][:40], age)
console.print(tbl)

# 2 draft replies (Lite limit)
unreplied = [e for e in actionable if not e["replied"]]
console.print()
for e in unreplied[:DRAFT_LIMIT]:
    name   = e["sender"].split()[0]
    text   = (e["subject"] + " " + e["snippet"]).lower()
    if any(k in text for k in ["urgent","deadline","asap"]):
        body = "Thank you for flagging this — I'll look into it and get back to you shortly."
    elif "?" in text:
        body = "Thanks for your question. To answer: [your answer here]\n\nLet me know if you need more."
    else:
        body = "Thanks for reaching out. [Your response here]."
    sig  = f"\n\n— {YOUR_NAME}" if YOUR_NAME else ""
    console.print(Panel(
        f"Hi {name},\n\n{body}{sig}",
        title=f"[bold]📝 Draft — Re: {e['subject'][:45]}[/bold]",
        border_style="yellow"
    ))

console.print()
console.print(Panel(
    f"Scanned: [yellow]{len(emails_data)}[/yellow]  "
    f"Actionable: [cyan]{len(actionable)}[/cyan]  "
    f"Noise: [dim]{noise_count}[/dim]  "
    f"Drafts: [yellow]{min(len(unreplied), DRAFT_LIMIT)}/{DRAFT_LIMIT}[/yellow] (Lite limit)\n\n"
    f"[bold yellow]🔓 Want more?[/bold yellow]\n"
    f"Iris Pro scans [bold]200 emails[/bold], drafts [bold]every reply[/bold], classifies by category, "
    f"and gives you weekly analytics.\n\n"
    f"[bold cyan]openclaw skills install iris-pro[/bold cyan]\n"
    f"Get your key → [bold]ko-fi.com/s/f75940a0ce[/bold]",
    title="Summary + Upgrade",
    border_style="cyan"
))
```
