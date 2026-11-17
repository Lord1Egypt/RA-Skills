# meeting-notes-to-action 📋

**Turn raw meeting notes into decisions, owners, and deadlines — before they evaporate.**

The universal post-meeting ritual: someone scrolls back through 40 minutes of
chat-log notes trying to figure out what was actually decided and who promised
what. Action items live in five people's heads and evaporate. This skill
converts messy notes into a decisions log, action items with owner + deadline,
open questions, and a ready-to-send summary email — deterministically, offline.

## The real-world problem

- **Action items evaporate.** Studies of meeting effectiveness consistently find
  a large share of agreed actions are never tracked; notes live in one person's
  notebook or a chat scroll nobody re-reads.
- **"Who said they'd do what by when?"** is the most expensive question in
  knowledge work — it requires re-reading the whole transcript to answer.
- **Minutes take longer than the meeting.** Writing structured minutes by hand
  from unstructured notes is pure formatting labor.
- **Recurring meetings lose continuity.** Without carryover tracking, the same
  unfinished item is re-raised from scratch every week.

## What it does

```bash
python3 scripts/meeting_extractor.py notes.txt --meeting-date 2026-08-12 \
  --title "Product sync" --minutes minutes.md --email email.md
```

- **Action items** from commitment patterns ("Sarah will send the report by
  Friday", "assigned to Priya", "@tom can you review?", checkboxes,
  "Action items:" sections) with owner, deadline, and confidence
- **Natural-language dates** — "by Friday", "next Tuesday", "end of month",
  "in 2 weeks" — resolved against the meeting date, never the run date
- **Decisions** ("we agreed to", "going with", "postponed") kept separate from
  mere discussion ("we discussed")
- **Open questions** (TBD, explicit questions, question forms outside lists)
- **Deduplication** — the same commitment phrased twice merges with a duplicate count
- **Carryover** — feed last week's JSON via `--previous`; unfinished items roll
  forward with age and stale warnings (3+ meetings = blocked or dead)
- **Outputs**: terminal digest, JSON, Markdown minutes table, summary email
  draft with per-owner task lists

## Example

Notes:

```
10:01 Sarah: I'll send the revised deck to leadership by Friday.
We decided to postpone the launch to Q4.
- Action items:
- set up Stripe payment sandbox, assigned to Priya by end of week
- [ ] call the datacenter about cooling
Question: who owns the runbook?
```

Output (excerpt):

```
 DECISIONS
  1. We decided to postpone the launch to Q4.  (line 2)

 ACTION ITEMS
  1. send the revised deck to leadership by Friday.
     owner: Sarah   due: 2026-08-14   conf: 0.95
  2. set up Stripe payment sandbox, by end of week
     owner: Priya   due: 2026-08-14   conf: 0.95
  ...
```

## Who needs this

Anyone who runs or attends meetings and takes notes: team leads, PMs, project
coordinators, executive assistants, consultants. Works with any text notes —
typed minutes, chat exports, or transcription output (use a transcription tool
first, then feed the text here).

## License

MIT — see [LICENSE](LICENSE)
