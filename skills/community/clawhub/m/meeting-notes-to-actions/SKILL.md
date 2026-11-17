---
name: meeting-notes-to-actions
description: Turns raw US meeting notes into a decision log and an owned action list with due dates, left as a draft for the organizer to send. Use when the user asks for meeting notes to actions, action item list template, meeting notes summarizer. For US project managers, chief of staff and team leads running recurring internal meetings.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Meeting Notes to Actions

**Turns raw US meeting notes into a decision log and an owned action list with due dates, left as a draft for the organizer to send.** Written for US project managers, chief of staff and team leads running recurring internal meetings.

Use this skill when someone asks for:

- meeting notes to actions
- action item list template
- meeting notes summarizer
- decision log template
- meeting follow up draft

---

## The job

Notes go into a document nobody opens again, so decisions get relitigated and the same follow-up ends up assigned to three people.

## What you get

1. Collect the raw notes, the attendee roles and the meeting type so nothing depends on a name being present.
2. Pull the decisions out with the decision, the role that made it and the date it was made.
3. Turn the open threads into actions with one owner role, one due date and a checkable definition of done.
4. Mark the items that need a date the group never set, so the organizer can fill them in.
5. Draft the follow-up message and leave it as a draft for the organizer to send.

Output contract:

- decisions - each decision with the deciding role and the date
- actions - one row per action with owner role, task, due date and definition of done
- open_items - the threads still needing a decision, with the question to ask
- follow_up_draft - a short message for the organizer to send, left as a draft
- needs_dates - the actions that have no agreed due date

## US specifics that matter

- Under the FLSA, time spent in a meeting the employer requires counts as hours worked, so a required meeting outside work hours has to be paid for covered nonexempt employees, while voluntary social or morale meetings generally do not (29 CFR part 785).
- The FLSA requires employers to keep payroll records for three years and to make them available to the employee or their representative on written request within 15 days (29 USC 211(c) and 29 CFR part 516), so minutes are not the record of time worked.
- FMLA records have to be kept for three years, including the dates of leave and the hours taken (29 CFR 825.400).
- Where an employer has a written policy, most courts expect it to be applied consistently, so a dated record of what was decided is the evidence that the process was followed.
- Minutes, task lists and policy documents are separate records, and a meeting summary does not satisfy a requirement to deliver or post a policy.
- Accommodation and medical details should stay out of a shared notes document, because the ADA limits how an employer may use health information about a current employee.

## Guardrails (hard rules)

- Never send the follow-up message, post it to a channel or distribute the action list; the organizer sends it.
- Never include attendees' home addresses, personal phone numbers, medical details or compensation in the notes.
- Never treat the action list as a timekeeping or payroll record; hours worked come from the timekeeping system.
- Never assign a task to a named person when the notes only name a role; list it as an open item for the organizer to confirm.

## Quickstart

### 1. Fill in the brief

`templates/action-item.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/render_action_item.py --input action-item.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/meeting-record-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Meetings and hours worked**

- 29 CFR part 785: attendance at a meeting the employer requires counts as hours worked.
- Lectures, training and voluntary meetings are handled under the same part.
- Voluntary social or morale meetings are generally not hours worked.
- If a meeting is mandatory only by written policy, the policy language is what the employee will rely on.

**Records and retention**

- Payroll records are kept for three years and are produced on written request within 15 days.
- FMLA records, including leave dates and hours, are kept for three years (29 CFR 825.400).
- Personnel file retention periods differ by state, so the minutes should not carry a promise about retention.
- Keep minutes with the dated records of the project, not in one person's inbox.

**Decisions and policy**

- A written policy has to be applied consistently, so the dated record of a decision is evidence.
- Minutes do not replace the policy document and cannot amend it.
- Where a state requires a written notice, the meeting record is not that notice.
- Record who decided, not only what was decided, when the decision is a judgment call.

**Language to keep out**

- No speculation about a person's performance, intent or health in a shared notes file.
- No legal conclusions about liability or blame for an incident.
- No customer or candidate personal data, because the notes travel to people who do not need it.
- No pay figures; keep compensation decisions out of a broadly shared document.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/meeting-record-rules.md` - US rules for meeting records and follow-ups
- `templates/action-item.md` - the brief to fill in
- `scripts/render_action_item.py` - the working script

## Verify the bundle

```bash
python3 scripts/render_action_item.py --input action-item.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
