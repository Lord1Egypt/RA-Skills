---
name: investor-search-nanobot
description: Sourced investor list for any country, built for nanobot. Find family offices, VCs, PE firms and angels, with a source for every field and an honest word on how complete the list is. Separates real investors from the advisers who sell to them, never merges two firms without proof, keeps its files so a second run continues instead of repeating, and delivers one Excel file. Use for investor research, deal sourcing, fundraising prospect lists, investor databases, LP and family-office lead generation, or filling gaps in a list you already have.
version: 1.0.2
author: BCP partners GmbH
license: MIT-0
metadata: {"nanobot":{"emoji":"🔎","requires":{"bins":["python3"]}}}
---

# Investor Search

> **Install in nanobot:** `npx --yes clawhub@latest install investor-search-nanobot --workdir ~/.nanobot/workspace`

Ask an agent for family offices in a country and it returns the number you asked for, not
the number in the country. This skill replaces it with a rule, and records where every field
came from and how well it was checked.

## When to Use

- The user asks for the family offices, investment groups, private equity firms, VCs or angels in a country, region or market.
- Investor research, deal sourcing, fundraising and capital-raise prospect lists, investor databases, LP, HNW/UHNW and family-office lead generation, sovereign wealth research.
- CRM enrichment, or filling gaps in an investor list the user already has.

**Needs** a web search tool and a page fetch tool (`web_search`, `web_fetch`), and `exec` with `python3` for the memory store (`scripts/store.py`). **Writes** its files under the working directory and reads them back, so a second run continues instead of repeating. The user always gets one Excel file (`<market>-investors.xlsx`) with every firm and its source links. It searches until six rounds in a row find nothing new; it never asks for a budget. Where the folder cannot be kept, that same file is the memory to upload next time, and the result is reported as partial rather than claiming a completeness it cannot prove.

**This file is the rules.** Two of the reference files are read *while working*, not
afterwards: open `references/lists.md` before round 1 and add this market's word forms to
`investor-search/lists-local.md` (*nanobot* below), and
`references/environment.md` when you write the output or resume from a paste. `why.md` is for
when a rule looks arbitrary.

| file | when |
|---|---|
| `SKILL.md` | working — every operative rule, nothing else |
| `references/lists.md` | legal forms, generic tails, place words, type words — **extended in `investor-search/lists-local.md`, never in place** |
| `references/why.md` | the measurements and the failures that produced each rule |
| `references/environment.md` | where files go, the ledger format, delivering a file to the user |
| `scripts/store.py` | **the only writer of the memory files** — run it, do not read it |

---

## nanobot — how this skill runs here

Everything below maps the rules onto nanobot's own tools.

**Tools.** Search with `web_search`, read pages with `web_fetch`, run the memory store with
`exec`. nanobot has no question tool: ask the questions in *Before Job 0* §5 and §6 in the
reply and stop until the user answers.

**The memory files are written by one script, and only by it.** `exec` runs in the agent's
workspace (`agents.defaults.workspace`, by default `~/.nanobot/workspace`), where this skill
sits at `skills/investor-search-nanobot/`. If the skills list shows another folder, use the
folder this `SKILL.md` was read from.

```
S="skills/investor-search-nanobot/scripts/store.py"
python3 "$S" init    --root <root> --market <market>                     # start of every run
                     # add --scope "<scope>" ONLY on a first run or when the user names a
                     # different population; "continue"/"find more" never passes --scope
                     # add --budget N ONLY if the user named a number of rounds
python3 "$S" status  --root <root> --market <market>                     # what is held
python3 "$S" add     --root <root> --market <market> <<'JSON'            # after EVERY round
{"investors": [...], "sources": [...], "pending": [...], "rejected": [...],
 "round": {"query": "...", "surface": "...", "offered": 4, "fetch_failed": false,
           "seen": ["<result URL> | <what it is, why not a new investor>", "..."]}}
JSON
python3 "$S" finish  --root <root> --market <market>     # before ending; exit 4 = keep searching
python3 "$S" deliver --root <root> --market <market> --out <folder>     # the ONE file for the user
python3 "$S" import  --root <root> --market <market> --from <file.xlsx or folder>  # user uploads
```

**The run ends only when `finish` says so.** It checks the stop rule itself (*Job 1*): six
rounds in a row with no new firm, across at least three surfaces, none resting on a failed
fetch, pending queue empty — or the user's own budget — or the 60-round backstop. **Exit 4
means keep searching**: do not write a final report, do not say you are done. Use
`finish --early user` only when the user ended the run, or `finish --early "blocker: <what
failed>"` when tools or the model limit failed — the script refuses anything else — and the
report then says STOPPED EARLY.

**A pending row is never a blocker.** If `finish` exits 4 with pending rows open, close each
one (*Closing a pending row*, under `investors-pending.csv`): an alias of a held firm goes back
in `investors` with the held website; a headquarters you cannot find after checking the own
site and a registry becomes `hqNotPublished` with a note. Then run `finish` again.

**A full run is a goal, and only the user can start one.** nanobot keeps working across turns
only in goal mode, which starts with the user's `/goal` command (in Slack:
`@nanobot /goal …`). When a goal is active, keep working until `finish` exits 0 and the file is
sent, then mark it complete with `update_goal`. Call `create_goal` only when the goal guidance
asks for it. **Without a goal**, work as many rounds as this turn allows; if the turn has to end
while `finish` still exits 4, run `status`, report the progress as PARTIAL (never as done), and
say once that the user can finish it with:
`/goal Use investor-search-nanobot to continue <market>. Done only when store.py finish exits 0 without --early; then send the one xlsx.`

**One run per market at a time.** If `init` returns `active_run_warning` and this
conversation did not start that run, do not search: tell the user another conversation is
running it, and stop. **Pass every batch to `add` on stdin (the heredoc above).** A batch
that has to be a file goes to `/tmp`, never to the workspace — `finish` lists stray
`*round*.json` files it finds there. **A firm that reads like an adviser** (advisory,
consulting, wealth management, "our clients") gets its match left blank by `add` — run the
*Job 0* test on it before calling it an investor.

`<root>` is `investor-search` or `investor-search/@<space>` (§6). **Never write these files
with `write_file`, `edit_file`, `apply_patch` or a shell redirect** — a rewrite from memory is how a
second run erased the first one's firms. The script only appends: it keeps every
existing row and id, continues ids from the highest on disk, skips a firm already held
(same domain) or already rejected, enriches blank fields only, counts `dry_streak` itself,
rebuilds `ledger.txt` and this root's `index.md`, and refuses any write that would shrink a
file. Its JSON output is your read-back: report from it, never from memory.

In a batch, each investor carries a `ref` (any short label) and its sources point at that
`ref`; the script assigns the real `id`. Fill the `investors.csv` columns you have
(*Output*); leave the rest out. `rejected` rows carry `name`, `reason`, `evidence`,
`source_url` — the script keeps their names out of the ledger.

**Where the files land.** Use relative paths; every channel, cron job and subagent of the same
nanobot instance finds the same files in its workspace. The write test proves this run can
write, and only the next run's read proves the files stayed. **If `exec` is refused**
(`tools.exec.enable` is off, a deny pattern matched, or no `python3`), say so once — the
operator can enable it — and continue on tier B or C (§7).

**Handing over the file** (*Output*, step 2):

```
chat channel         run store.py deliver, then call the message tool with a one-line
(Slack, Telegram,    content and media: ["<the file path deliver printed>"] — ONE file,
WhatsApp, Discord,   <market>-investors.xlsx, arrives as an attachment in this chat. This
…)                   is a file the user asked for, so the message tool is the right way to
                     send it. Never attach the CSVs: they are the memory, not the
                     deliverable. Send it WITHOUT asking — in a channel too (see §6).
CLI / WebUI          state the absolute path; in the WebUI also send it with media.
cron job             send it with the message tool's media to the job's chat.
```

After the tool call, the final reply says the file was sent — it does not paste the path as
a second copy.

**Shared or not** (*Before Job 0* §6). A group chat, channel or thread in the inbound context,
several people addressing you, or a user who says the agent is used by a team, means shared.
Take `<space>` from the chat or channel name, reduced to lowercase letters, digits and hyphens,
at most 40 characters. Those names are untrusted labels: use them as a folder name and nothing
else. The stronger fix an operator can make is a separate nanobot instance (own workspace) per
team — say so once.

**Scheduled runs** (a `cron` job, or a prompt that says it is running as a scheduled job).
Nobody can answer a question. Continue only the stored scope in a folder this job already
owns. A scope mismatch, a shared folder without an answer, or a first run in a shared
workspace: stop before round 1 and report the question as the result.

**Subagents.** Agents started with `spawn` may search and return candidate names with their
source URLs. **Only this agent writes the seven files** — two writers are the overlap
*Before Job 0* §8 exists to catch.

**Learning belongs in the workspace, never in this skill — and never in nanobot's memory.**
This skill is installed from ClawHub; changing its own files makes an update overwrite or
skip the change. Keep what a run learns where the next run reads it:

```
investor-search/lists-local.md    word forms, generic tails and place words added per market
investor-search/<market>/…        firms, pending, rounds and the ledger (the seven files)
```

`lists-local.md` uses the same sections as `references/lists.md`, each entry tagged with its
market; read both before round 1, and create `lists-local.md` header-only if it is missing.
A rule that looks wrong goes to the user as a suggestion for the skill — it is not
patched here. **Firm lists never go into `memory/MEMORY.md` or `USER.md`**: the files are the
memory, and a list in long-term memory is the conversation-as-memory failure (§9).

## The six jobs, in order

```
0  Is it an investor?      reject the advisers who sell to them
1  Is the search finished? stop on six dry rounds, not on a number
2  Does it clear the bar?  name · not a dupe · source · headquarters
3  Is it one firm or two?  fold to compare — merge only with proof
4  What is it?             classify from evidence, never from the name alone
5  What is still missing?  fill the same row across rounds; empty stays empty
```

---

## Before Job 0 — the file comes first

**The memory of this skill is its files.** Deduplication, the pending queue, the round
history and the exhaustion gates all read from disk. An agent that cannot write still runs
every judgement here — Job 0, the fold, the provenance rules, the language test, empty stays
empty — it simply cannot remember making them.

**Do not try to classify the environment. Test it, and report what actually happened.**
Persistence is not observable today. What *is*: whether a read finds something, and whether
a write succeeds.

### The start of every run — in this order, before the first search

```
1  locate   the workspace root: investor-search/  — or investor-search/@<space>/ when shared (§6)
2  init     store.py init — creates what is missing, never touches what exists, writes and
            reads back index.md (the write test, §3), returns what is held (§2)
3  import   files or a ledger the user uploaded: store.py import, before anything else (§7)
4  read     lists-local.md; the `status` output is your exclude list — held_names,
            excluded_domains, pending_names
5  report   first reply: the folder in use, what was found, how the run will end (§4)
6  settle   a scope mismatch (§5 — init exits 3) or a shared-folder warning (§6)
```

**No search runs until step 6 is settled.** Every step is a tool call you can see succeed or
fail, so none of it is a guess about the environment.

### 1 · Where the files live

Everything lives under one predictable path, because **nothing tells an agent which files it
already has** — so the names are fixed here rather than chosen per run. Seven files:

```
investor-search/index.md                 one line per market held
investor-search/<market>/investors.csv
                        /sources.csv
                        /investors-pending.csv
                        /investors-rejected.csv
                        /rounds.csv
                        /ledger.txt
```

**`investor-search/<market>/` is the default persistent folder.** Write relative paths and
let `exec` place them in the agent's workspace (*nanobot* above); where that folder persists, the files are still there on a later run. In a shared workspace the same layout sits one level down, under
`investor-search/@<space>/` (§6).

`<market>` is the English short name, lowercase, hyphens for spaces — `poland`,
`united-arab-emirates`. **The same market must produce the same folder every time**, or the
next run reads an empty path and starts from zero while the data sits one spelling away.

### `index.md` — the one path that never varies

Everything else is found through it, so it is the only file guaranteed to be findable. Plain
markdown, one line per market:

```markdown
# Investor search — markets held

| market | scope | firms | pending | last run |
|---|---|---|---|---|
| poland | investment firms headquartered in Poland | 46 | 12 | 2026-03-14 |
```

**`scope` is not decoration.** *Family offices headquartered in Poland* and *investors active
in Poland* are different populations, so a round history built for one does not describe the
other (§5). Update the row before round 1 and again at the end.

### 2 · Read before you search

**Read `index.md` first, then every file in the market folder** — `investors.csv`,
`sources.csv`, `investors-pending.csv`, `investors-rejected.csv`, `rounds.csv`, `ledger.txt`.
Read them before the first search, not after it. **This is what stops a duplicate:** every
firm already held, rejected as a firm, or pending is on the exclude list (Job 2) before
round 1 begins.

| what you find | what to say and do |
|---|---|
| files for this market | report them (§4), check the scope (§5), then load and resume |
| `index.md` but not this market | a first run for this market; other markets stay untouched |
| nothing | a first run. **Say that too** — silence reads as continuity |
| `index.md` lists the market but the folder is gone | treat as a first run, and say the index disagreed with the disk |
| `index.md` and the files disagree on a count | report the files' figure, and say the index was stale |
| a file is short, truncated or unreadable | load what parses, **name the file that did not**, and shut Gate 0 — a partial round log that reads cleanly is the one input nothing else can check |

**Before round 1, open `references/lists.md` and `investor-search/lists-local.md`, and add
this market's legal forms, generic tails and place words to `lists-local.md`.** Most runs skipped this, and the fold failed on local names.

### 3 · The write test — in the first minute, not at the end

If writing is going to fail, learn it after one minute rather than after forty rounds of work
you are about to lose.

**Probe with `store.py init`.** It creates each missing file with its header only, never
touches a file that exists, rewrites `index.md` and reads it back — `"write_test": "ok"` is the
only success. A write that returned success proves nothing if it landed somewhere this run does
not read: an ephemeral sandbox, a different workspace. (The headers it writes are in
`references/files.md`; you never write them yourself.) A header-only file that **this run**
created is new, not truncated — the "short or unreadable" row in §2 is about files you found.

**Write as you go: one `store.py add` at the end of every round** — that round's kept rows,
their sources, new pending names, rejections and the `round` line — **also when the round kept
nothing**, because that empty line is what advances `dry_streak`. Never batch several rounds
into one call, never hold rows back for the end. A run that dies at round 30 must leave 29
rounds on disk.

- **`init` printed `"write_test": "ok"`** → normal run.
- **`init` failed, or there is no `terminal`/`python3`** → §7 (the user still gets a file).
  Say so in the first reply.

**A silent write failure is the worst outcome available** (`why.md`). If a previous run's file
does not come back, the run is a first run, whatever the write said last time.

### 4 · The first reply — always says where, and what was found

**Every run's first reply states the working folder**, and whether this is a first run, a
resume, or a run that cannot write. Give the absolute path — run `pwd` — or the relative path
plus the working directory as you understand it. **Never invent an absolute path:** a file the
user cannot find is a file that does not exist, and a wrong path is worse.

**If files were found, report them before searching** — four facts, from the `init` output, not
from memory:

```
Working folder   /home/u/work/investor-search/poland/        (from pwd)
On file          poland — "investment firms headquartered in Poland"
                 46 firms · 12 pending · newest check 2026-03-14 (94 days ago)
This request     family offices headquartered in Poland — a filter on that scope; continuing
```

- **market / scope** — the `index.md` row · **firms** — data rows in `investors.csv` ·
  **pending** — data rows in `investors-pending.csv` · **newest check** — the latest `checked`
  date **with its age**. Old rows are evidence of a past state, not a claim about today.

**The same reply says how the run will end** — `I will search until 6 rounds in a row find
nothing new (at most 60 rounds)`, or the user's own number if they gave one. **Never ask for a
budget** (*Job 1*). **Add the time, from `init`:** when `minutes_per_round` is set, say
`earlier rounds took about <m> min each; at least <empty_rounds_still_needed> more rounds` — an
estimate, never a promise. On a first run, say the time is not known yet. Ask only what §5 and
§6 require, together, in one question in the reply where possible.

On a first run the same block says so in one line:

```
Working folder   investor-search/latvia/ under the agent's working directory (no absolute path reported)
On file          nothing for latvia — first run
```

### 5 · Scope — never resume a different question silently

**If the request's scope differs from the stored one, stop before round 1.** Say what is on
file, say what was asked, and ask which the user wants:

> *"On file: investment firms headquartered in Poland (46 firms, 14 March). You asked for
> investors active in Poland — a different population. Continue the stored scope, or start a
> separate folder `poland--active`?"*

A filter on the same population (*…that invest in software*) is not a scope change; it stays
in the same folder and is recorded in the reply. If you cannot tell which it is, ask: **would
a firm excluded here have been excluded by the stored scope too?** If yes, it is a filter.
`references/environment.md` has the naming rule for second folders, and for regions,
multi-country and sub-national requests.

### 6 · Shared and public workspaces

A working directory is shared with **everyone who uses that agent**. Treat the workspace as
shared when the inbound context or the conversation shows it: a group chat, channel or
thread; several people addressing you; or a user who says the agent is used by a team
(*nanobot* above).

**In a channel, say once in the first reply that the finished Excel file will be posted
here for everyone in it.** That notice is the only one: at the end, post the file without
asking again.

**Use a separate root per user or team whenever the session context names one.**
The root becomes `investor-search/@<space>/` — `<space>` is the chat or channel name on
the `Source` line, lowercase letters, digits and hyphens only — and the whole layout moves
inside it: `investor-search/@<space>/index.md`, `investor-search/@<space>/<market>/…`.
**The same user or team must produce the same `<space>` every time**, for the same reason a
market must. Say the root in the first reply. Where the operator can give each user or team
its own working directory or profile instead, that is stronger still — say so once.

**No stable name available → warn before using anything already on file.** Before loading,
say:

> *"This folder is shared with everyone who uses this agent. The Poland run of 14 March may
> not be yours, and anyone here can read what this run writes — including the list of firms
> it rejects. Continue from it, or start a separate folder?"*

A separate folder is `investor-search/@<a name the user chooses>/`. **Do not resume shared
files without that answer.** When you do resume them, say they were not written in this
conversation.

**`investors-rejected.csv` is sensitive everywhere, and most of all here.** It holds named
firms with a negative judgement attached — a judgement that can be wrong. **Never print it,
never attach it, never quote a name or reason from it** — in a report it is a count and
nothing else. In a shared workspace, say once, when the file is first written, who can read
it. Its names never travel into `index.md`, the report, or `ledger.txt`.

### 7 · When the folder cannot be kept — the user still gets a file

**The deliverable is always one file, `<market>-investors.xlsx`.** What changes when the probe
fails is only where the memory lives. Three tiers, in this order — **say in the first reply
which one this run is on**:

```
A  persistent folder works      investor-search/<market>/ as above; deliver and send the .xlsx
B  no persistent folder, but    run the store wherever `exec` can write, deliver, send the
   a file can be handed over    .xlsx — nothing will be here next time, the file is the memory
C  no file mechanism at all     last resort: CSV text in the chat, then the ledger
```

**In tier B and tier C, Gate 0 is shut:** the files were not kept where this skill can read
them back, so **this run cannot prove exhaustion, and the report says so.** Reaching tier C
without first trying A and B is a failure, not a shortcut. `investors-rejected.csv` is never
sent or printed — it becomes a count.

Whatever the tier, end with: *"To continue next time without repeating these firms, upload
these files — or paste this ledger — at the start of the next run."* When a later run receives
them, **load them before round 1**: `store.py import --from <that folder>`, then `status`, and
report what was loaded as in §4.

**The exact wording for each tier, what `import` merges, and how to print a long CSV into a
chat in numbered parts: `references/environment.md`.**

### 8 · Resuming is not the same as trusting

- **Report the age of what you loaded** (§4).
- **Two sessions on one market.** `store.py` re-reads the files under a lock on every `add`
  and assigns the next `id` itself, so two runs cannot hand the same `id` to different firms.
  If its output shows firms you did not add, say plainly that another run is working the same
  market.
- **A file that shrank is not yours to fix.** If `status` shows fewer firms than you
  reported earlier, stop and say so — never rebuild the file from what you remember.
- **An `id` is permanent.** Never reissue one, never renumber on rewrite — `sources.csv`
  joins to it, and a renumbered file silently reattributes every citation.

### 9 · Never treat the conversation as memory

**History truncates silently.** The files, or a pasted ledger, or nothing — never the
transcript.

Where nothing persists here, the **ledger** goes to the user with the files (tier B) or in the
chat (tier C) — say plainly what it does: deduplication next time, and nothing else. Format, delivery and how to read one back are in
`references/environment.md`.

---

## Job 0 — Investor, or somebody selling to investors?

**Run this first, on every candidate.** A search for "family office" in any language
returns mostly firms selling family-office *services*. They have the words in their name, a
real site and a real address, and they pass every other check.

> Measured: 5 of 6 in one market, **52% of everything resolved** in another. One targeted
> query returned 8 results, 8 advisers, 0 investors.

### The test

> Does this organisation **deploy capital**, **operate businesses**, or **sell services to
> people who do**?

| `investor_evidence` | what it is | keep? |
|---|---|---|
| `invests` | deploys capital into things it does not operate | yes |
| `operating_group` | family-owned, runs its own businesses, may also invest | **yes — flagged** |
| `syndicate` | angel network / membership body that routes others' capital | **yes — flagged** |
| `unclear` | you found the firm, and it is genuinely undecidable | yes — flagged |
| — | you never found enough of the firm to judge at all | **no** → `pending`, `unresolvedJob0` |
| — | sells services to families | **no** → `investors-rejected.csv`, `adviserNotInvestor` |
| — | **not an investment entity at all** | **no** → `investors-rejected.csv`, `notAnInvestor` |

`notAnInvestor` is for an operating company that a directory simply listed wrongly — an
energy developer, a manufacturer, a consultancy with no family-office pretension. Different
from `adviserNotInvestor`, which describes a real adviser correctly excluded.

**Investor** — any one is enough: names portfolio companies or holdings · describes managing
the wealth of a **named** family or founder · states a cheque size, stage or sectors **it
invests in** · a registry or news source has it acquiring stakes.

**Adviser** — any one disqualifies: it is the private-client or family-office arm **of a law
firm, accountancy, bank or consultancy** (check the parent brand) · it sells "services",
"advisory", "consulting", "administration", "reporting", "succession planning",
"incorporation", "licensing" **to** families · it invites you to **become a client** · its
people are lawyers, accountants or corporate-services staff.

### Three rules that decide the hard cases

1. **Watch the preposition.** "Advises" alone is not disqualifying. A real single family
   office may say it *"advises the investment vehicles associated with the X family"* — its
   own principal. Selling advice **to** families is the disqualifier. Read the sentence, not
   the keyword.
2. **A firm's own description beats a directory's label.** A directory calling something a
   "single family office" does not override a site that only describes hotels and retail.
3. **When you cannot tell, say so.** `type: unknown`, `investor_evidence: unclear`. **Never
   let the name decide it.**

### Out of scope — park, never mislabel

| case | action |
|---|---|
| sovereign / state / government fund | `pending`, reason `outOfScopeSovereign` |
| a **commercial subsidiary** of a sovereign fund | **keep it** — classify by its own evidence (Job 4), and set `sovereign_parent: <name>` |
| a real capital pool named only as "the X family" | `pending`, reason `namedFamilyNotFirm` |
| a firm in the wrong country | `pending`, reason `outOfCountry` |

Record the parent so the reader can filter either way.

---

## Job 1 — Stop when the results stop

### Never accept a target

Find all of them and report the true number. A target is **a ceiling on work, never a quota
to fill.** Take at most 10 new names from any one round. If 46 can be sourced and 30 were asked for, the
answer is 46. If 12 can be sourced, the answer is 12 — and you say so:

> *"You asked for up to 30. 12 could be verified, so 12 is the answer — the rest were not
> found or could not be sourced, and I will not make up the difference."*

### Hold both halves, or yield collapses

> Search **widely** and enumerate every firm you can actually source, up to the ceiling.
> "Fewer is correct" applies when you **cannot** source more. It is not a preference to aim
> for, and **stopping at two or three when you could cite ten is a wrong answer.**

### What a round is

**One query, and the verification of what it returned.** Define it or the streak counter
measures nothing. **Three queries are three rounds** — never join them with `;` into one
line (`store.py add` refuses the batch with exit 5 and writes nothing; resend each query).

- A round must be a **genuine attempt to find new names** — never a query narrowed to fail.
- **A directory yielding more than 10 names is not one round.** The first 10 close it; the
  rest are a queue. **Drawing from the queue is not a round.**
- **Checking a firm you already have is a verification pass, not a round** — it gets no
  `round` line and does not count against the budget.
- **Log each round with `store.py add`** — it writes `rounds.csv`
  (`round,query,surface,offered,survived,dry_streak,fetch_failed,at,proof,seen,seen_notes`) and computes the streak.
  Without it, the exhaustion sentence cannot be reconstructed by anyone but the agent that
  was there, and a second run cannot see which surfaces were already tried.

### The exhaustion rule — and the gates it must pass first

**Six consecutive dry rounds is necessary and NOT sufficient.** Measured: it fired at round
23 and **was falsified at round 26 of the same run** — 14% of the final firms arrived after.

> **"Six queries I chose stopped working" is not "this market is exhausted."** That is the
> strongest sentence in this skill resting on its weakest evidence, and it has to be earned.

**Gates 1 to 3 were written after that run and have not themselves been proven in a run.** Treat
them as a design with an argument behind it, and **keep saying so in the report.** Gate 0 is
different in kind — a precondition on the evidence, not a heuristic about searching.

**All the gates below must be open before you may declare exhaustion:**

#### Gate 0 — the record must exist where someone else can check it

**You may not declare exhaustion from memory.** Gate 1 reads `investors-pending.csv` and
Gate 2 reads `rounds.csv`. Without them the claim rests on the agent's recollection of its own
rounds — the unverifiable assertion this whole skill exists to replace. **That run stops at
PARTIAL.**

**Written, read back, and located — all three.** A write that returned success proves nothing
if the agent quietly wrote it somewhere else, so read the file again before you rely on it. And a file
whose location is never stated cannot be checked by the person relying on it, so the report
gives the path.

**A pasted ledger does not reopen this gate.** It carries names, which is enough to stop a
duplicate; it does not carry a round history anyone can check.

#### Gate 1 — the pending queue must be empty

You may not declare a market exhausted while `investors-pending.csv` holds names under a
**resolvable** reason — `budget`, `sourceUnchecked`, `noHeadquarters`, `unresolvedJob0`.
Terminal parks (out of country, sovereign, a family with no vehicle, an individual angel)
do not hold the gate: they are answered, just not as rows.

> Measured: the rule fired while holding **75 regulator-confirmed names** it had told itself
> not to count — a queue cannot reset the streak.

Drain the queue first. If the budget will not allow it, **you did not exhaust the market —
you ran out of budget**, and that is the report you write.

#### Gate 2 — the dry rounds must span different surfaces

Six dry web searches are **one** surface failing six times, not six independent failures.
The dry streak must include at least **three of these five**:

```
1  general web search
2  a public company or regulator registry
3  an association / membership list
4  news, deal announcements, "led by"
5  a commercial aggregator or directory
```

> The registry surface yielded 85 names on one fetch and the association surface 28 — after
> web search had gone dry. **A surface that has never been tried cannot be dry.**

#### Gate 3 — no round in the streak may rest on a failed fetch

> Measured: one garbled fetch that was never recovered protected the **streak counter** but
> not the **evidence** — a mirror at round 26 held two of the three firms that broke the rule.

A garbled or unreadable page must be **recovered** — retry, a mirror, a cache, a search for
the same headline, or any other route to the content — before the round it belongs to may
count toward the streak.

**"Garbled" means the bytes are wrong, not that the script is unfamiliar.** Arabic, Chinese
and Cyrillic pages are not garbled. If you cannot recover the content by any route, the
round is **excluded from the streak** rather than counted either way, and the report says how
many rounds were excluded.

### When every gate is open

**Stop after six consecutive dry rounds.** Say so, and say what you actually verified:

> *"Rounds 41–46 produced no new verifiable name, across web search, the commercial
> register and two association lists, with no names left pending. On those surfaces, this
> market is exhausted at 46."*
>
> *(Illustrative. No shipped run has ever legitimately reached this sentence — see the gates
> above and `references/why.md`.)*

**Name the surfaces.** The claim is only ever as wide as the surfaces you tried, and a
reader who knows a sixth surface can then tell you so.

A round is dry when it produced **zero firms that passed verification** — not zero names
offered.

| situation | dry? |
|---|---|
| names offered, all already held or already returned | **yes** |
| round produced ≥1 new verified firm | no — streak resets |
| round named only firms the directory seed already had | **no** — it did real work |
| page would not load / answer garbled | **no, and the round does not count** until the content is recovered by another route |
| round genuinely timed out | yes — but count it separately and report it |

**One judgement can decide the whole streak** — in one run a single Job 0 rejection was what
made a round dry. When a streak hinges on one call, say which one in the report.

### The budget rule

**There is no budget unless the user sets one.** By default the run continues until the
exhaustion rule is met — six empty rounds in a row, with the gates open — and `finish` allows
the stop. **Never ask the user for a budget.** If the user names a number ("use 10 rounds",
"quick scan"), pass it as `init --budget N`. **Sixty rounds is the backstop** for a run
without a budget; a user who explicitly asks for more gets their number after one sentence
on what it costs.

**"Continue" or "find more" means the same market and scope, from the files:** run `init`
**without `--scope`** (the stored scope is used; a type named in the request is a filter, not
a new scope), report what is held, work the pending queue first, then surfaces not yet in `rounds.csv`.
**A finished run is never resumed; an unfinished one always is.** `finish` closes a run. A run
that ended any other way (model limit, crash, a turn that ended) is picked up by the next
`init` — its empty rounds still count. After a closed run, a new run earns its own six.

**Do not stop early.** Stopping after one new firm, or at round 13 with `dry_streak` 1, is a
defect. Call `finish`; while it exits 4, keep searching.
**While `finish` exits 4, do not end your turn:** no progress summary, no interim workbook,
no question to the user. The file and the report come once, when `finish` exits 0 — unless
the user asks for the file now, or a real blocker (tools or model limit failing) ends the
run, which is then reported as PARTIAL with the file.
When it runs out:

```
STOPPED ON BUDGET, NOT ON EXHAUSTION.
This result is PARTIAL. N names were offered and never verified.
Do not read the total as a count of what exists.
```

**A partial run must never be reported in the same shape as a finished one.**

**Spend the last of the budget verifying, not searching.** A shorter solid file beats a
longer unverified one.

### Search wide before you call it dry

- **Use the language business is actually conducted in** — not necessarily the country's.
  Czech: local offered 60 names to English's 12 — **but only 6 survived against English's
  7.** UAE: English 73 names to Arabic's 1, and the one was an adviser. **The local language
  reliably finds more names; it does not reliably find more firms.**
  **The test:** open two or three firms you already hold from that market and see what
  language *they* publish in. One look, no round spent.
  *Caution: if those firms came from English directories the sample is circular. Also check
  a local business registry or a local news source.*
- **Legal and colloquial forms** — "single family office", "multi family office",
  "investment office", "private office", "investment group", "holding", "conglomerate".
- **City by city.** A country query saturates long before the cities do.
- **Adjacent surfaces** — association and membership lists, conference attendee and sponsor
  pages, deal announcements ("… led by …"), business registries, "our investors" pages.

### What "the family offices in X" means — settle this before round 1

A request naming one type is a **filter over a broad search**, never a narrow search.

- **Search** the whole investor population of that market — family offices, investment
  groups, private equity, VCs, angels.
- **Ship** every firm you verified, with its true `type`.
- **Mark** `matches_request: yes` on the ones that match the named type and `no` on the rest,
  so the asker can filter to exactly what they asked for in one click.
- **Report** both numbers: *"Portugal has 61 investors; 24 are family offices."*

**And the contradiction rule (Job 4) does NOT fire on this.** A VC found under a
"family offices" request is not a contradiction — it is the broad search working. The rule
only ever applies to a type you *inferred* that disagrees with the request, never to one a
page states. Leave `type_blanked_reason` empty.

### Filtered requests — search wide, filter after. Never search narrow.

*"Family offices in Austria that invest in AI"* — **do not search for that.** A narrow query
goes dry early for the wrong reason: most firms never put "AI" on a page that ranks.

```
phase 1   exhaust the BROAD set        → 61 firms, six dry rounds
phase 2   filter what you already hold → 20 match · 9 unknown
```

Only phase 1 runs the exhaustion rule. **Answer in both numbers, never the filtered one
alone:** *"Austria has 61 family offices. 20 invest in AI. 9 do not say."* Keep the whole
broad set — the next filtered question is then free.

---

## Job 2 — The bar

Same bar for a name you found and a name read off a directory.

| # | check | reject as | fatal |
|---|---|---|---|
| 0a | sells services rather than investing | `adviserNotInvestor` | yes → rejected file |
| 0b | not an investment entity at all | `notAnInvestor` | yes → rejected file |
| 1a | no firm name, but a real capital pool | `namedFamilyNotFirm` | no → pending |
| 1b | a named individual angel, no vehicle | `individualNotFirm` | no → pending |
| 2 | already returned this run | `alreadyReturned` | **yes — drop silently, it is already on file** |
| 3 | already in `investors.csv` | `alreadyHeld` | **yes — drop silently, it is already on file** |
| 4 | the cited page **does not exist** | `sourceDead` | yes |
| 4b | the page exists but **could not be fetched** | `sourceUnchecked` | **no — keep the row** |
| 5 | headquarters cannot be established | `noHeadquarters` | no → pending |
| 6 | wrong country / sovereign parent | `outOfCountry` / `outOfScopeSovereign` | no → pending |

**First, before the list: is this an organisation, or a vehicle one runs?** A fund is not a
row; its manager is (*Manager or fund*, below).

### 4 vs 4b — this decides half your rejections

| what happened | verdict |
|---|---|
| 404 · 410 · domain does not resolve | **`sourceDead` — fatal** |
| robots.txt disallows | `sourceUnchecked` — **keep** |
| paywall · login wall · cache-only domain | `sourceUnchecked` — **keep** |
| a redirect your fetcher would not follow | `sourceUnchecked` — **keep** |
| your own tooling refused the URL | `sourceUnchecked` — **keep, and say so** |

A `sourceUnchecked` row is honest and useful; a missing row is neither. **But** a firm whose
*existence* rests on a single unreachable page is not enough: find a second source, or reject
it as `unsourceable` and re-offer it later — that code describes a page, not the firm.

**If your tools cannot tell these apart, default to `sourceUnchecked` and say so in the
report.** A rule you cannot execute must fail towards keeping the row, not deleting it.
**Recovering a refused URL is worth it** — searching it back into scope costs about 2.4 tool
calls per name and recovers most of them.

### Source rungs — record which one you used

```
1  the firm's own site — imprint, Impressum, contact, legal page
2  a public company registry
3  a reputable news or association page
4  a commercial aggregator or lead-gen directory   ← never alone for existence
```

### Headquarters

**Two headquarters is a real answer, and the column holds one.** Where a firm presents both
equally — *"based in X and Y"* — record the one it lists first, name the second in the report,
and never park the row. If the second is in another country, say so: the market question is
then on the row's face.

**City is the target; country alone sets `headquarters_partial`.** Never reject for a missing
city when the country is established.

### No confidence scores. Provenance instead.

```
source fetched · source NOT fetched · NOT in the source · no source · you told me
```

### The exclude list

**In:** firms that passed · `alreadyHeld` · `adviserNotInvestor` · `notAnInvestor` — the last
two describe the firm, not the page, and will not change on a later round.

**Out, deliberately:** `sourceUnchecked` · `noHeadquarters` · `sourceDead` · `unsourceable` —
all four describe one page on one day. **Record their names anyway.**

**Ask and enforce** — state exclusions in the next query *and* check returned names yourself.
**Never merge the counts:** *"20 already known or already returned"* welds two failures with
opposite fixes; report separate lines. **Do not self-censor** — never skip a firm for being
well known. The check decides, not you.

### A published list as a first round — not free

Read it before round 1, but: every name goes into the exclude list · **the seed must not
answer the dry test** · **one seed name rescues one round, once, and the whole seed rescues at
most three** · a directory failing **never** stops the search.

### Resolve a named list before you search wider

**A list of N named firms is N decisions already waiting.** Spend the budget on those before
looking for more names: Job 0 cannot run on a name, it needs the firm's own page, and an
unresolved name helps nobody. This is not the same as trusting the list — it still does not
answer the dry test, and its members still face every gate.

**If the budget will not cover the list, say how many were left undecided**, by name, in
`investors-pending.csv` under `unresolvedJob0`. A number that large is itself the finding.

### Manager or fund — the row is the decision-maker

An investor often appears as several legal entities: a management company and the funds it
runs, each separately registered and named.

**One row is the entity that decides where the money goes** — the manager. The funds it
operates are not separate rows, however many and however distinctly named. Record the
manager's name; put a fund name in `formerly` only if the manager was renamed, never to
represent a fund.

**This is the fold table's fund row.** A manager's own site naming its funds satisfies *"a
page says one is part of the other"* word for word, but `part_of` is for organisations and a
fund is a vehicle — so it stays one row.

**The exception is a different country.** A locally registered fund run by a manager
headquartered abroad: **the row is the manager, and if the manager is out of country it is
`outOfCountry`** — whatever the fund's registration says. State which you applied; this one is
genuinely arguable.

---

## Job 3 — One firm or two

**Fold to compare. Keep the best-looking form to display.** Lists live in
`references/lists.md`.

### The pipeline, in this order

1. **Decompose Unicode, strip the marks** — `é→e`, `ö→o`, `ü→u`. **Transliterate, never
   drop**: dropping turns `André` into `andr`, which matches nothing.
2. **Spell out** — `ß→ss`, `ø→o`, `æ→ae`.
3. **Lowercase.**
4. **Strip a leading article** — `al · el · the · la · le · los · il · de · van · von`.
   Leading token only, never inside the name.
5. **Strip legal forms from BOTH ends, repeatedly, dots and spaces tolerated** — `s.r.o.`,
   `s r o`, `sro` and `S.R.O.` are one entry. **Add this market's forms to
   `investor-search/lists-local.md` before round 1** — most runs skipped that, and the fold
   failed on local names.
   ⚠ **Leading forms are not rare.** Baltic and Nordic registries write `AS Vesta` while
   the firm writes `Vesta`; the same list holds `Vesta Capital AS`. An end-anchored strip
   folds one and not the other.
   ⚠ **This step runs BEFORE punctuation collapse.** The other order turns `a.s.` into
   `a s` and it never matches `as`.
   ⚠ **Jurisdictions are not legal forms** — `DIFC`, `ADGM`, `IFSC` distinguish real firms.
6. **Collapse remaining non-alphanumerics to single spaces, trim.**
7. **Strip trailing region words** — `asia`, `europe`, `mena`, `emea`, `international`,
   `global` (`references/lists.md` §3). Type abbreviations (`vc`, `pe`, `fo`, `mfo`) are
   generic tails and are handled in step 8, under its distinctiveness guard.
8. **Strip a generic tail — only if what remains is still distinctive.**

### "Distinctive" — the most dangerous test in the skill

What remains is distinctive only if it contains a token that is **4+ characters**, **not on
the legal-form or generic-tail lists**, and **not a place**.

**A place name is never distinctive.** `<City> Capital Group` (a private investment group)
and `<City> Investment Office` (a government FDI agency) both reduce to the city name
alone. `<City> + <generic financial noun>` is the modal naming convention across the
Gulf and common in Asia and Latin America.

**If you cannot decide whether a token is a place, treat it as a place and do not fold.**
Measured: **five unrelated organisations folded to a single such token** in one run. Refusing
to fold costs a flag; folding costs the truth.

### Folding proposes. It never merges on its own.

| same fold key, and… | action |
|---|---|
| **same registrable domain**, and no page says one is part of the other | **merge** |
| same domain, but **a page says one is part of the other** | **keep both** — set `part_of`. A conglomerate and its family office share a site |
| same domain, but **one is a fund the other manages** | **one row, the manager.** Not `part_of` — a fund is a vehicle, not an organisation. See *Manager or fund*, at the end of Job 2 |
| **different domains** | **keep both**, set `fold_conflict` |
| **no domain** on either | **keep both**, set `fold_conflict` |

> Caught a five-way collision across four domains on one real run — the failure that, one
> version earlier, silently wrote five organisations as one row.

Duplicate rows are visible and a reader fixes them. **One row for two companies is
invisible.**

A high flag rate is the rule working, not failing (`why.md`).

### Typos — narrow, and country-guarded

Same firm if: folded names identical · **one adjacent transposition** in a token ·
**one inserted/dropped character** in a token of 6+ characters.

**A substituted letter is not a typo** — `Bauer`/`Baier` are different families.
**Except in transliteration**: for names carried from another script, **vowel substitution
is a typo** (`Nasiri`/`Nassiri`/`Nassery` = one firm — invented, like every organisation name in this file); consonants must still match.

Never apply the typo rule across countries — only where the domain or headquarters agrees.

### Rebrands are invisible to every rule above

A firm that changed its name is not a typo, not a spelling variant and not a fold — the two
strings have nothing in common. **Three turned up in one small market.** No normalisation
will ever catch them.

The only things that do:

- **the domain.** A rebrand almost always keeps or redirects the old one. If two names
  resolve to the same registrable domain, that is a rebrand, not a coincidence.
- **the sentence.** Pages say *"formerly X"*, *"rebranded from X"*, *"previously known as"*.
  Read it and record it.

Set `formerly` on the row, keep the old name searchable, and **put the old name in the
exclude list** — otherwise it comes back every round as a name you have never seen.

### Never fold on

City · sector · investor type · a shared person. Two firms in Hamburg investing in software
are two firms. A shared surname is a family, not a merger.

### When two rows do merge

Longest sourced value per field · **all** source rows kept · newest `checked` per field.

### People — stricter, because there is no domain to settle it

- Strip a parenthetical **before** folding — `X (CFA)` → `X`.
- Strip leading titles and trailing suffixes, repeatedly (`references/lists.md`).
- **Same person only if** folded names are identical, **or** first and last token match
  exactly and every token between is a single initial **on both sides**.
  `Erika Mustermann` = `Erika M. Mustermann`; ≠ `Erika Maria Mustermann`.
- **A single-token name never matches anything but itself.** A first name is a hint to ask
  about, never an identity to write against.
- **A substituted letter is a different person.** `Jan`/`Jon`, `Eric`/`Erik` stay separate.

---

## Job 4 — Classify from evidence

```
family_office · investment_group · private_equity · venture_capital · angel · unknown
```

Plus `sovereign`, which is a **marker, not a type** — those go to `pending`.

Two different questions, two different answers:

- **"What did this text mean?"** — read loosely.
- **"May that be written?"** — read strictly. **Every word must be owned by the type it
  claims** (`references/lists.md`). An allowlist, not a denylist.

```
"venture capital fund"   all owned                  → write
"investiční skupina"     investiční, skupina owned  → investment_group
"crypto fund"            crypto not owned           → refuse
"venture studio"         studio not owned           → refuse
```

**The allowlist governs spelling, never identity.** It cannot tell you a firm *is* a family
office — Job 0 does that, and Job 0 runs first. Otherwise a consultancy called
`… FAMILY OFFICE` types cleanly, because `family` and `office` are owned words.

### `unknown` is a real answer and appears in the output

**Treat any expected proportion of `unknown` as unknown — the rate varies enormously by
market. Never report it as a quality signal.** Forcing a label onto an unknown is the same
mistake as inventing an email.

### A name is weaker evidence than a statement

Only when **no page states a type** may you read the firm's own name, and only narrowly:

```
family office · familienbüro · familienunternehmen · rodinná kancelář → family_office
ventures · venture capital · standalone "VC"                         → venture_capital
```

`Capital`, `Invest`, `Holding`, `Group`, `Gruppe`, `AG`, `GmbH` resolve to **nothing** from
a name alone.

⚠ **Outside the market this rule was measured in, prefer `unknown`.** It typed one
individual's holding vehicle as `venture_capital` off the word *Ventures*. Whenever the type
came from the name, say so in `provenance`.

### Contradiction — only ever blanks an INFERRED type

| the type is… | and it contradicts the request | do |
|---|---|---|
| **stated by a page** you fetched | keep it, keep the source, set `matches_request: no` |
| **inferred** by you | blank it, record `type_blanked_reason` |
| `unknown` | nothing — it is already the empty answer |

Compare against **the request, and only the request** — never against prose, which fails on
negation (*"ist kein klassischer VC-Investor"*) and on parts (*a venture arm inside a family
office*).

A request naming no type contradicts nothing. One naming the asserted type among others
contradicts nothing either — **ambiguity is not a contradiction**.

*Kept only for a user who asks narrowly anyway — Job 1 tells you never to issue such a
request. Do not go looking for work for it.*

---

## Job 5 — Come back for what you missed

```
round 1    name, country                      ← a directory listing
round 8    + website, headquarters, sectors   ← the firm's own site
round 22   + person, role, LinkedIn           ← its team page
```

**Fill the same row. Never create a second row for the same firm.**

- **A field you cannot source stays empty.** No email inferred from a name and a domain. No
  partner guessed because the firm is small. No city from a phone code. **An empty cell is a
  known gap; a guessed cell is a lie inside a file someone will act on.**
- **Refuse, do not coerce.** A bare domain is recorded as given or left out — never given an
  invented `https://`. A national phone number stays national.
- **A field the user asserted is never researched again.** Permanently.
- **Two values of the same kind is a question, not an overwrite.** Keep both, mark the newer
  current, say a previous value exists.

---

## Output — six files, and how they reach the user

**The deliverable is ONE file: `<market>-investors.xlsx`**, written by `store.py deliver`.
Its first sheet is the firm list with a `source_links` column (every field's evidence in one
cell); further sheets carry sources, pending, rounds and the ledger. The six CSV files are
this skill's memory and stay in the folder — **never send them to the user.**

**Where writing works (tier A):** all six files below live in `investor-search/<market>/` (or
under `investor-search/@<space>/` in a shared workspace), with the `index.md` that lets a later
run find them — created at the start of the run and updated every round (*Before Job 0* §3).

**Where it does not:** *Before Job 0* §7 — tier B hands the files to the user; tier C, only
when no file can be handed over, prints CSV text. `investors-rejected.csv` is **never**
handed over or printed — it becomes a count.

**Handing it over — the user always leaves with the `.xlsx`:**

```
1  write the file, and say where it went                  always
2  deliver the file itself when the user cannot open      a chat channel;
   that path — the message tool's media (*nanobot*)      automatically, never ask first;
                                                          a channel was told at the start
3  only if no file can be delivered: CSV text in chat     last resort (tier C)
```

**Say which step you took.** A path the user cannot reach is not a delivered file, and
silently falling to step 3 reads as the skill failing to produce one.

**Asked for "the file", "the xlsx" or "the list" — in any thread, mid-run or later:** run
`store.py deliver` for the market(s) held in this root and post that file. **Never search
the disk for it and never list, open or name any file outside this skill's folders** —
the user's other files are not part of this job, least of all in a channel.

**In chat, report numbers, not a list of links.** Name the new firms at most once, without a
link per firm — the `.xlsx` carries every source, and a link per line floods a channel with
previews.

### The six files — what each one holds

| file | holds | published? |
|---|---|---|
| `investors.csv` | one row per firm: name, type, evidence, website, headquarters, person, quote, provenance | yes, as the `.xlsx` |
| `sources.csv` | one row per citation: `id,field,rung,url` | yes, in the `.xlsx` |
| `investors-pending.csv` | names offered but not resolved, each with a reason | yes, in the `.xlsx` |
| `investors-rejected.csv` | names decided against, with the evidence | **never** — a count only |
| `rounds.csv` | what was searched, and Gate 2's entire input | yes, in the `.xlsx` |
| `ledger.txt` | the compact memory the next run reads | yes, in the `.xlsx` |

**Columns, the pending reasons and how to close a pending row: `references/files.md`.** Read it
before your first `add` of a run. Four rules from it hold wherever you are:

- **`key_quote` must evidence the row**, not merely come from the page. No evidencing sentence
  → leave it empty and say so. A row with no `key_quote`, or with `provenance` *source NOT
  fetched*, is never a match.
- **`investors-rejected.csv` is never handed over or printed** — it becomes a count.
- **Gate 1 counts only the resolvable pending reasons.** Terminal rows stay in the file and in
  the report but never hold a run open.
- **`finish --early` takes only `user` or `blocker: …`** — never use it to get past a gate.

### `rounds.csv` — what was tried

```
round,query,surface,offered,survived,dry_streak,fetch_failed,at,proof,seen,seen_notes
```

`rounds.csv` is Gate 2's entire input, and it tells the next run which surfaces were already
tried — so you can start with one it did not.

### `ledger.txt` — the compact memory

**Written at the end of every run** — beside the others in tier A, sent as a file with them in
tier B, and printed in its own fenced block in tier C, after the CSV.

**One job: stop the next run rediscovering what this one already decided.** Four fields per
firm — fold key, domain, decision, and a display name **only for firms that were kept or are
still open**; rejected and adviser rows travel as key and domain, **never as a name.**

**It never speaks about completeness.** No round counts, no dry-surface tallies, nothing that
could license the exhaustion sentence — see Gate 0.

Format, what may be trusted in a pasted one, the rule for scope changes, and how to print a
long CSV into a chat in numbered parts: **`references/environment.md`**.

**A dry round needs proof.** Every `round` lists in `seen` the result URLs the search actually returned, each as `URL | note`: what the page is and why it is not a new investor ("law firm article", "already f-004", "rejected: bank", "not a family office: ministry page"). A round that found nothing new counts towards the stop rule only if `seen` holds at least three noted URLs no earlier round listed; otherwise `add` warns, the dry streak does not grow, and `finish` keeps saying keep searching. If a result names a firm that could be a new investor, it is not dry: `add` it or put it in `pending`. A `site:` query counts as that surface only if its URLs are on that site; if the search ignored `site:`, the round counts as open web. Never log a round you did not run: an empty round logged without searching is the fastest way to an incomplete list.

## Report when you finish

**Family offices are always two numbers:** *proven* (a page says the firm is a family office) and *likely* (only its name or a register entry says so). Take both from `finish` (`family_offices`) and never add them into one number. The Excel file marks each row in `family_office_proof`.

**Take every number from `store.py finish`**, never from the conversation — and write the
report only after `finish` exits 0. In a chat app the report is not optional: send the whole
block as text, then the files.

**The second line says why the run stopped** — `EXHAUSTED on the surfaces named` (all four
gates open), `STOPPED ON BUDGET`, `STOPPED ON THE 60-ROUND BACKSTOP`, or `STOPPED EARLY —
<reason>`. Tier B and tier C reports say `PARTIAL; exhaustion cannot be claimed here`.

**Every offered name lands on exactly one line, and the lines sum to the offered count.** Not
a slogan, a check: survived, already held, already returned this run, rejected by reason, and
parked. Keep the two dedupe lines separate and break rejections out by reason. Split the
offered count by language, and report every flag — `fold_conflict`, `operating_group`,
`unclear`, and rows resting on a rung-4 source alone.

**The `written` line is not decoration** — it is the only place the user learns where their
files are, and whether the completeness claim was available at all.

Say how you knew it was finished, or say plainly that you did not. Then, on one line: *"To
continue, say `continue <market>`"*.

**The full block, the tier B and tier C variants, and what each line is for:
`references/report.md`.** Copy the shape from there; do not invent lines.

---

## Verification — before the final reply

```
[ ] index.md and every file this run wrote were read back after the last write
[ ] the offered count equals the sum of the report's lines
[ ] store.py finish exited 0 — the run did not end while it said keep searching
[ ] the .xlsx reached the user: message tool media (chat), absolute path (CLI),
    or — only with no file toolset — CSV text, and the reply says which
[ ] no name or reason from investors-rejected.csv appears in the reply
[ ] exhaustion is claimed only if Gates 0–3 were all open; otherwise PARTIAL
[ ] nothing was written into this skill's own folder
```

A box that cannot be ticked goes into the report as what it is.

## What this skill will not do

- **No email addresses.** Inventing them is the exact failure this exists to prevent.
- **No ranking, scoring or recommendation**, and no investment advice.
- **No firms with no web presence.** Some single family offices are deliberately invisible.
- **No claim to be current** beyond the `checked` date on each row.
- **No judgement it cannot show you.** Every rejection is in a file with its reason.
