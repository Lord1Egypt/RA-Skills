---
name: horus-lite
description: "Horus Lite -- Meeting Intelligence. Paste meeting notes or a transcript and get a clean action item list instantly. Free tier. The only meeting skill on ClawHub."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [MEETING_NOTES]
      bins: [python3, pip3]
    primaryEnv: MEETING_NOTES
    emoji: "👁️📋"
    homepage: https://clawhub.ai/occupythemilkyway/horus-lite
    tags: [meeting, notes, action-items, transcript, productivity, summary, free, lite, horus]
    envVars:
      - name: MEETING_NOTES
        required: true
        description: "Paste raw meeting notes, transcript, or bullet points here"
---

# Horus Lite -- Meeting Intelligence

Horus sees everything. Paste your messy meeting notes and get clean, assigned action items in seconds.

## Free vs Standard vs Pro

| Feature | Horus Lite (Free) | Horus Standard ($5) | Horus Pro ($9) |
|---------|------------------|--------------------|--------------------|
| Action items | Yes (list) | Yes (with owners + deadlines) | Yes (full tracker) |
| Meeting summary | No | Yes (full) | Yes + exec brief |
| Decisions log | No | Yes | Yes |
| Follow-up email | No | Yes (draft) | Yes (stakeholder-specific) |
| Next agenda | No | No | Yes |
| Risk/blocker flags | No | No | Yes |
| Save to file | No | Yes (.md) | Yes (.md) |

**Upgrade:** Horus Standard -> ko-fi.com/occupythemilkyway ($5)
**Bundle:** All 5 Egyptian skills for $29 -> ko-fi.com/occupythemilkyway

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Parse meeting notes

```python
import os, sys, re
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

NOTES = os.environ.get("MEETING_NOTES", "").strip()
if not NOTES:
    console.print(Panel(
        "[red]MEETING_NOTES is required.[/red]\n\nPaste the full text of your meeting notes or transcript.",
        title="Setup Error", border_style="red"
    ))
    sys.exit(1)

word_count = len(NOTES.split())
line_count = len(NOTES.splitlines())

console.print()
console.print(Panel.fit(
    f"[bold yellow]👁️  Horus Lite -- Meeting Intelligence[/bold yellow]\n"
    f"Notes: [cyan]{word_count} words[/cyan] / [cyan]{line_count} lines[/cyan]\n"
    f"[dim]Free tier -- action items extraction[/dim]",
    border_style="yellow"
))
console.print(Rule("[yellow]Analysing meeting...[/yellow]"))
print(f"\n=== MEETING NOTES ===\n{NOTES}\n=== END NOTES ===")
```

---

## Step 3 -- Extract action items

Read the meeting notes above and produce:

**Action Items List:**
Extract EVERY task, commitment, or follow-up mentioned. Format each as:
```
- [ ] [Action] — Owner: [Name or "TBD"] | Due: [Date or "TBD"]
```

Then add:

**Quick Summary (2-3 sentences):** What was the meeting about and what's the most important outcome?

Be thorough — catch every "I'll", "we need to", "someone should", "by next week", "action item" phrasing.

---

## Step 4 -- Upsell

```python
from rich.console import Console
from rich.panel import Panel
console = Console()
console.print()
console.print(Panel(
    "[bold yellow]Horus Standard ($5)[/bold yellow] adds a full meeting summary, decisions log, and a ready-to-send follow-up email.\n"
    "[bold magenta]Horus Pro ($9)[/bold magenta] adds stakeholder-specific briefs, next meeting agenda, risk flags, and saves to file.\n\n"
    "Upgrade: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]",
    title="[yellow]Want the full meeting brief?[/yellow]",
    border_style="yellow"
))
```
