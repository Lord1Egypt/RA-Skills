---
name: javis-todo-spend-tracker
description: Keep the user's to-do list and spending ledger from what they say out loud. The javis-server dispatcher runs this skill once for every completed recording or keyboard unit; the skill reads the open to-dos, extracts the user's own to-dos, purchases and "done" statements, and writes them as PENDING cards the user confirms or discards. In chat it answers "what's on my list" and "what did I spend this month" by running its counting script. Triggers — "what's on my list", "my to-dos", "what did I spend this month", "spending this month", "待办", "这个月花了多少".
keywords: to-do, todo list, spending, expenses, what did I spend, 待办, 花了多少, todo-spend-tracker
metadata:
  openclaw:
    runtime:
      node: ">=18"
  routes:
    - route_id: ledger
      skill: javis-todo-spend-tracker
      matches: "to-dos the user commits to, purchases and money the user spent, a to-do the user says is done"
      args_template: null
      risk: low
---

# To-dos & Spending

> Turn the to-dos and purchases the user says out loud into pending cards, and answer
> "what's on my list?" and "what did I spend this month?" with exact numbers.

Rows live in `skill_data` (`skill=todo-spend-tracker`) with three types: `ledger_task`
(a to-do), `ledger_expense` (a purchase) and `ledger_done` (a to-do is finished). Every
row the skill writes is **pending**; the user taps Confirm (it counts) or Discard (it is
deleted) in the HiJavis app. Only confirmed rows count.

## When to run

1. **Dispatcher run (automatic).** After a recording or keyboard unit completes, the
   server runs this skill with a prompt like `Run /javis-todo-spend-tracker for <unit>.` (the
   unit is `audio:<id>` or `kbd:<id>`) plus a `UNIT CONTEXT` block (`transcript`, `reference_date`, `tz`, `source_ref`,
   `source_kind`). Do the extraction below. If the unit holds nothing to record, do
   nothing: no push, no reply.
2. **Chat question.** "What's on my list?", "what's still on my to-do list", "what did I
   spend this month?", "how much on food in October?", "我的待办", "这个月花了多少" — run
   the counting script (see "Answering in chat") and reply.

## Core commands

```bash
# Step 1 — the open to-dos a "done" may name, plus today's local date
node scripts/todo-spend-tracker.js fetch-open

# Step 3 — write the extracted rows (pending) to /api/skill/data.
# Save the extraction JSON to a file with your file tool, then:
node scripts/todo-spend-tracker.js push --file /tmp/ledger-extraction.json
# or pass it in a QUOTED heredoc (the quotes around the delimiter matter):
node scripts/todo-spend-tracker.js push <<'JAVIS_LEDGER_JSON'
{ ...extraction JSON... }
JAVIS_LEDGER_JSON

# Chat — the counting script (the agent copies its numbers)
node scripts/ledger.js todos
node scripts/ledger.js spending                     # this month
node scripts/ledger.js spending --month 2026-10     # a given month
# add --json for the raw numbers
```

## Dispatcher run: workflow

1. **Fetch the open to-dos.** Run `fetch-open`. It prints `{ reference_date, tz, open:
   [{ dedup_key, item, since }], source }`. A "done" may only name one of these
   `dedup_key`s. If `source` is `unavailable`, the server refused the read: `open` is
   empty, so record no "done" this run (to-dos and purchases still go in).
2. **Extract** from the `UNIT CONTEXT` transcript (the user's words; `reference_date` is
   the unit's local day). Produce one JSON object:

   ```json
   {
     "source_ref": "<UNIT CONTEXT source_ref, else the unit id>",
     "unit": "<the unit from the run prompt, e.g. audio:6f1c… or kbd:123>",
     "source_kind": "audio",
     "reference_date": "<UNIT CONTEXT reference_date>",
     "tasks":    [{ "item": "Call the bank about my card", "quote": "I need to call the bank tomorrow about my card" }],
     "expenses": [{ "item": "lunch", "amount": 12, "currency": "USD", "category": "Food & drink", "quote": "Just paid twelve dollars for lunch" }],
     "dones":    [{ "task_key": "<an open dedup_key from fetch-open, verbatim>", "quote": "OK, I finally called the bank" }]
   }
   ```

   Leave an array empty when there is nothing of that kind. If all three are empty, stop:
   do not push.
3. **Push.** Give the object to `push` with `--file <path>` or a quoted heredoc
   (`<<'JAVIS_LEDGER_JSON'`). Never use `echo '…' |`: the quotes are the user's own
   words, and an apostrophe ("I'll", "don't") would break the command. `unit` is
   required for a keyboard unit (its `source_ref` is shared by everything typed that
   day). `push` validates every row, builds the dedup keys
   (`task:<source_ref>:<hash>`, `exp:<source_ref>:<hash>`, `done:<task_key>:<source_ref>`),
   sets `start_at` to the local day at 00:00, and writes the rows as pending. It prints
   what it wrote and what it dropped. Running it again for the same unit adds no rows.

## Extraction rules

Record only things about the user's own life that the user states. When unsure, leave it
out: a missed card costs less than a wrong one.

- **Whose words.** Only statements in the first person count ("I need to…", "I paid…",
  "我得…", "我刚花了…"). Recordings label speakers `speaker_0`, `speaker_1`, …; no label is
  known to be the user, so treat every `speaker_N` label as unknown and rely on the
  first-person rule. A keyboard unit (`source_kind: keyboard`) is always the user.
- **Skip other people's items.** "Alex will order the rain barrel", "Sam paid forty
  dollars for the pizza", "you should call your mom" → nothing.
- **to-do (`tasks`)**: something the user commits to do ("I need to", "I have to", "I'll",
  "remind me to", "我要", "我得"). `item` = the task in a few words, in the user's
  language. Skip musing and maybes ("I should probably clean the garage someday, maybe").
- **Timed events are not to-dos.** Anything with a date and time to attend ("dentist
  Tuesday at 3pm", "dinner Saturday at 7") is left to `calendar-extractor`; record nothing
  for it here.
- **purchase (`expenses`)**: money the user spent. `item` = what it was for, as said
  ("lunch", "咖啡"); `amount` = a number; `currency` = an ISO code (`USD`, `CNY`, `EUR`…;
  "块"/"元"/"RMB" → `CNY`, "bucks"/"$" → `USD`). If the amount or currency is not clear,
  leave the purchase out. If the user names another day ("yesterday I paid…"), add
  `"date": "YYYY-MM-DD"` counted from `reference_date`. Only purchases from last month
  or this month are recorded; an older (or future) date is dropped by the script.
  Categories (exactly one): `Food & drink`, `Groceries`, `Transport`, `Shopping`, `Bills & subscriptions`, `Entertainment`, `Health`, `Travel`, `Other`
  Use these strings exactly; anything else is dropped. Pick `Other` when none fits.
- **done (`dones`)**: the user says an open to-do is finished ("I finally called the
  bank", "银行的电话打完了"). `task_key` must be one of the `dedup_key`s `fetch-open`
  printed, copied verbatim. If no open to-do matches, leave it out (the script drops it
  anyway).
- **Language.** English and Chinese both work; keep the user's language in `item` and
  `quote`.
- **quote**: the user's own words that state the fact, at most 25 words.

## Answering in chat

For "what's on my list?" and "what did I spend this month?" (or a given month, in any
language), **run the counting script and copy its numbers.** Never add amounts, count
items or work out totals yourself.

- To-dos: run `node scripts/ledger.js todos`. It lists the confirmed open to-dos with
  their since-dates and gives pending to-dos as a count only (do not list pending items).
- Spending: run `node scripts/ledger.js spending` (or `--month YYYY-MM`). It gives the
  month total and a table by category, largest first, confirmed purchases only. A second
  currency is reported on its own line; never add currencies together.
- Reply with the script's text (translate the wording into the user's language if
  needed, keeping every number and date). Keep its links: `[Open To-dos & Spending
  ›](javis://todos)` for to-dos and `[See by category ›](javis://todos/month)` for
  spending.
- If the script says the server refused the read, tell the user the numbers are on the
  To-dos & Spending screen and give the `javis://todos` link. Do not guess numbers.

## Notes

- **Counting rules** (`scripts/ledger.js`, mirrored by the iOS app and pinned by the
  shared `test/fixtures/ledger-cases.json`): a to-do is open when its `ledger_task` is
  confirmed and no confirmed `ledger_done` names its `dedup_key`; done recently = confirmed
  dones of the last 14 days; month spending = confirmed `ledger_expense` amounts by the
  local month of `start_at`, per category and per currency; pending rows are counted
  separately and never added in.
- **Ticks in the app** post a confirmed `ledger_done` with `source: "app"` and no
  `source_ref`; Undo discards it. The skill never writes those.
- **Server reads.** `fetch-open` and `ledger.js` read `GET /api/skill/data` with the
  container's gateway token. If the server refuses that token (401/403), `fetch-open`
  returns no open to-dos (`source: unavailable`, so no "done" is offered) and
  `ledger.js` prints a hint pointing to the app instead of numbers. The skill keeps no
  local copy of the user's to-dos.
- **Runtime**: Node 18+ built-ins only; no `npm install`.
