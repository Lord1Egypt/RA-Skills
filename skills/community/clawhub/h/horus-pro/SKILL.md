---
name: horus-pro
description: "Horus Pro -- Full Meeting Intelligence Suite. Summary, decisions, action tracker, stakeholder-specific briefs, next meeting agenda, risk flags, and follow-up emails. The most powerful meeting tool on ClawHub."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [MEETING_NOTES, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: MEETING_NOTES
    emoji: "👁️⚡"
    homepage: https://clawhub.ai/occupythemilkyway/horus-pro
    tags: [meeting, notes, summary, action-items, decisions, stakeholders, agenda, risks, pro, horus]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Horus Pro license key. Get one at: ko-fi.com/occupythemilkyway"
      - name: MEETING_NOTES
        required: true
        description: "Raw meeting notes or full transcript"
      - name: MEETING_TITLE
        required: false
        description: "Meeting name or subject"
        default: ""
      - name: STAKEHOLDERS
        required: false
        description: "Comma-separated list of stakeholder names/roles for targeted briefs"
        default: ""
      - name: YOUR_NAME
        required: false
        description: "Your name for email sign-offs"
        default: ""
      - name: OUTPUT_DIR
        required: false
        description: "Output folder (default: ./horus_output)"
        default: "./horus_output"
---

# Horus Pro -- Full Meeting Intelligence Suite

The complete meeting processing tool. Delivers everything from a raw transcript: full brief, stakeholder-targeted summaries, action tracker, risk flags, next meeting agenda, and polished follow-up emails -- all saved to files.

**Bundle deal:** All 5 Egyptian skills for $29 -> ko-fi.com/s/7625accf3f (save $16)

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate and load

```python
import os, sys, re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY or not LICENSE_KEY.startswith("HORUS-PRO-"):
    console.print(Panel(
        "[red bold]Horus Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or try Horus Standard ($5): [dim]openclaw skills install horus[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

NOTES        = os.environ.get("MEETING_NOTES", "").strip()
TITLE        = os.environ.get("MEETING_TITLE", "").strip()
STAKEHOLDERS = [s.strip() for s in os.environ.get("STAKEHOLDERS", "").split(",") if s.strip()]
YOUR_NAME    = os.environ.get("YOUR_NAME", "").strip()
OUTPUT_DIR   = os.environ.get("OUTPUT_DIR", "./horus_output").strip()

if not NOTES:
    console.print(Panel("[red]MEETING_NOTES is required.[/red]", title="Error", border_style="red"))
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not TITLE:
    TITLE = NOTES.split("\n")[0].strip()[:60] or "Meeting"

date_str   = datetime.now().strftime("%Y-%m-%d")
safe_title = re.sub(r"[^a-z0-9]+", "_", TITLE.lower())[:30]
word_count = len(NOTES.split())

console.print()
console.print(Panel.fit(
    f"[bold yellow]👁️  Horus Pro -- Full Meeting Intelligence[/bold yellow]\n"
    f"Meeting:      [cyan]{TITLE}[/cyan]\n"
    f"Notes:        [white]{word_count} words[/white]\n"
    f"Stakeholders: [white]{', '.join(STAKEHOLDERS) or 'None specified'}[/white]\n"
    f"Output:       [green]{OUTPUT_DIR}/[/green]",
    border_style="yellow"
))
console.print(Rule("[yellow]Processing...[/yellow]"))
print(f"\n=== MEETING NOTES ===\n{NOTES}\n=== END NOTES ===")
if STAKEHOLDERS:
    print(f"\nStakeholders requiring targeted briefs: {', '.join(STAKEHOLDERS)}")
```

---

## Step 3 -- Generate full intelligence suite

Produce these documents from the meeting notes:

**1. MEETING_BRIEF.md** -- Complete master document:
- Executive Summary (4-5 sentences, what happened and what matters most)
- Attendees (extracted from notes)
- Decisions Made (table: Decision | Made By | Rationale)
- Action Items (table: # | Action | Owner | Due | Priority | Status=Open)
- Discussion Topics (organized, with key points under each topic)
- Open Questions (unresolved items)
- Risks & Blockers (anything that could prevent progress)

**2. ACTION_TRACKER.md** -- Standalone action item tracking file:
```
# Action Tracker -- [TITLE] -- [DATE]

| # | Action | Owner | Due Date | Priority | Status |
|---|--------|-------|----------|----------|--------|
[All action items, one per row]

## Completed (none yet)
```

**3. FOLLOW_UP_EMAIL.md** -- Professional follow-up email ready to send:
- Subject line
- Full email body (summary, decisions, action items)
- Signed by {YOUR_NAME} or "Best regards," if blank

**4. NEXT_AGENDA.md** -- Draft agenda for the next meeting based on this one:
- Open action items that need check-in
- Unresolved questions from this meeting
- Logical next topics based on what was discussed

**5. STAKEHOLDER_BRIEFS.md** -- If STAKEHOLDERS were provided, write a separate 3-5 sentence brief for each person named, focused only on what's relevant to them (their action items, decisions that affect them, info they need). If no stakeholders specified, write briefs for each person mentioned in the notes.

---

## Step 4 -- Save all files

```python
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
console = Console()

safe = re.sub(r"[^a-z0-9]+", "_", TITLE.lower())[:25]
d    = datetime.now().strftime("%Y%m%d")
outputs = [
    (os.path.join(OUTPUT_DIR, f"meeting_brief_{safe}_{d}.md"),    "Full meeting brief"),
    (os.path.join(OUTPUT_DIR, f"action_tracker_{safe}_{d}.md"),   "Action item tracker"),
    (os.path.join(OUTPUT_DIR, f"follow_up_email_{safe}_{d}.md"),  "Follow-up email"),
    (os.path.join(OUTPUT_DIR, f"next_agenda_{safe}_{d}.md"),      "Next meeting agenda"),
    (os.path.join(OUTPUT_DIR, f"stakeholder_briefs_{safe}_{d}.md"), "Stakeholder briefs"),
]

tbl = Table(title="Horus Pro -- Intelligence Suite Complete", box=box.SIMPLE, border_style="green")
tbl.add_column("File", style="cyan")
tbl.add_column("Contents", style="dim")
for path, desc in outputs:
    tbl.add_row(path, desc)
console.print()
console.print(tbl)
console.print(Panel(
    f"[bold green]Meeting intelligence complete.[/bold green]\n"
    f"[yellow]{len(outputs)} documents[/yellow] saved to [cyan]{OUTPUT_DIR}[/cyan]",
    border_style="green"
))
```

Save all 5 files to OUTPUT_DIR using your file writing tool.
