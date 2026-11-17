# Environment — where the files go, and what to do when they cannot

`SKILL.md` carries the rules that change a decision mid-run. This file carries the formats
and the mechanics: read it when you are about to write the output, hand it over, or resume
from something the user pasted.

---

## 1 · Why the paths are fixed

An agent is not shown what is in its own working directory. A session typically receives the
*contents* of a short list of named files and nothing else — no directory listing, no index
of what exists. Anything not named in advance is invisible.

That single fact decides the design. The skill cannot discover last week's run; it can only
**look in a place it already knows**. So the layout is fixed rather than chosen, and the
market folder is derived by a stated rule rather than by taste:

```
investor-search/index.md
investor-search/<market>/investors.csv
                        /sources.csv
                        /investors-pending.csv
                        /investors-rejected.csv
                        /rounds.csv
                        /ledger.txt
```

**`<market>`** — the English short name, lowercase, spaces to hyphens, nothing else:
`poland`, `estonia`, `united-arab-emirates`, `south-korea`. Not `UAE`, not `Poland (PL)`,
not the local-language name, not an abbreviation the user happened to type. A market whose
folder is spelled two ways is two markets, and the second run starts from zero with the
answer sitting one directory away.

**Not every request is a country.** Use the same rule one level out, and **write the folder
name into your first reply** so the user can see which drawer their work went into:

| the request | the folder |
|---|---|
| a region — the Gulf, the Nordics, DACH, Benelux | `the-gulf`, `the-nordics`, `dach` — one folder, and `scope` says which countries |
| several countries at once | one folder per country. A run over three countries writes three folders and three `index.md` rows |
| a sub-national area — Bavaria, Silicon Valley | `bavaria`, `silicon-valley`, with `scope` naming the parent country |
| a filter on a country — Poland, software only | **the country's folder.** A filter is a `scope`, never a second folder — see below |

**A firm can belong to two markets** — headquartered in one, active in another. It gets its
own `id` in each folder and the two are not linked. Say so once when it happens rather than
implying a single global list exists.

**All writes go through `scripts/store.py`** (`SKILL.md`, *OpenClaw*); this file describes what
it produces. **Relative, not absolute.** Write `investor-search/poland/investors.csv` and let the agent
resolve it against the agent's workspace. Run `pwd` when the first reply needs the absolute folder.

**Shared workspaces move the whole layout one level down** — `investor-search/@<space>/index.md`,
`investor-search/@<space>/poland/…` — where `<space>` is the chat or channel name from the inbound context's
session context, reduced to lowercase letters, digits and hyphens. The `@` marks a workspace, so it can never collide with a market folder. The rule
for when to do this, and what to say when no such name exists, is in `SKILL.md`
(*Before Job 0* §6).

### `index.md`

Plain markdown, human-readable, one line per market. It exists so a single known read can
answer *what do I already have* — including for a user who asks vaguely.

```markdown
# Investor search — markets held

| market | scope | firms | pending | last run |
|---|---|---|---|---|
| poland | investment firms headquartered in Poland | 46 | 12 | 2026-03-14 |
| estonia | investment firms headquartered in Estonia | 28 | 139 | 2026-02-02 |
```

Update it at the start of a run and again at the end. It is the only file whose path never
varies, so it is the only file guaranteed to be findable.

### Scope belongs in the index

Two runs can name the same market and mean different questions — *family offices
headquartered in Poland* is not *investors active in Poland*. The stored `scope` line is
what makes that visible on resume.

**If the request's scope differs from the stored one, do not silently continue.** Say what
is on file, say what was asked, and let the user choose: continue the old scope, or start a
second folder. A round history describes the question it was asked, and reusing it under a
different question is how a completeness claim becomes false without anyone lying.

**A second folder for the same country is named `<market>--<scope-slug>`** — `poland--active`
— with the double hyphen marking it as a scope split rather than a market. The plain
`<market>` folder always means the broadest scope run so far.

**This is for a different question, never for a filter.** *Investors active in Poland* is a
different population from *investors headquartered in Poland*, so it gets its own folder and
its own round history. *Family offices in Poland that invest in software* is the same
population with a filter applied — it stays in `poland`, and the filter is recorded in the
reply, not in the tree. If you cannot tell which you are looking at, ask: **would a firm
excluded here have been excluded by the stored scope too?** If yes, it is a filter.

### When the user names their own folder

Honour it — but say what it costs, once: **a folder outside the fixed layout cannot be found
again by a later run**, because nothing tells an agent what directories exist. Offer to keep
the canonical copy as well, and record the chosen path in `index.md` so a person can follow
it even though the skill cannot. Never relocate a run mid-flight.

---

## 2 · `ledger.txt`

### What it is for

One job: **stop the next run rediscovering what this one already decided.** Nothing else.

It is not the deliverable. `investors.csv` is what the user asked for — twenty-two columns
and its citations. A fallback that asks the user to paste that back is a fallback that dies
at the second run and takes the context window with it.

### What it must never do

**It carries no round history, no dry-surface counts, no claim about completeness.** An
earlier draft of this design put those in the header so a pasted ledger could reopen the
exhaustion gates. That was wrong twice over:

- A per-surface dry *total* is not a *streak*. Gate 2 asks whether six consecutive dry rounds
  spanned three different surfaces; `web=6 registry=2` cannot answer that, because it does
  not say which rounds were adjacent or which belonged to the streak.
- A pasted count cannot be verified against anything. Counting the body lines proves the body
  is intact; it says nothing about whether the header was accurate when written or edited
  since. The one number whose error costs a false *"this market is finished"* would have been
  the one number with no check on it.

So Gate 0 is absolute: **a ledger makes a run cheaper, never finished.**

### Format

```
#LEDGER v2 market=<market> date=<ISO>
#SCOPE <the scope line from index.md>
key|name|domain|status
sigmacap|Sigma Capital Partners|sigmacap.example|ok
nordadv|—|nordadv.example|adviser
qrsgroup|QRS Group|—|pending
#END rows=3
```

| field | notes |
|---|---|
| `key` | the fold key from Job 3, so the next run deduplicates with the same instrument |
| `name` | the display name — **only for `ok` and `pending`**; `—` for `adviser` and `rejected` |
| `domain` | registrable domain, or `—` |
| `status` | `ok` · `adviser` · `rejected` · `pending` — four values, no reasons |

- **`|` is the separator** because it does not occur in firm names or bare domains. `,` does.
  One line per firm, never wrapped.
- **`status` carries no reason strings.** The reason vocabularies live in the CSVs; repeating
  them here would invite a reader to treat the ledger as the record, which it is not.
- **`rejected` and `adviser` rows carry no name at all** — key and domain only, enough to
  recognise the firm if it is offered again and not enough to publish a judgement about it.
  `investors-rejected.csv` is a local working file precisely because a named firm with a
  negative claim attached should not travel; the ledger is an object built to travel, so the
  name comes off. Never attach the evidence, the quote or the rejection reason either.
  A key with no domain and no name is a weak match — accept that it will occasionally fail to
  suppress a re-offer, because the alternative is publishing the list.
- **No person, email or phone number. Ever.**
- `rows=` counts firm lines only.

### Where files work, the ledger is for people, not for the next run

Nothing in this skill ever reads `ledger.txt` back when the CSVs exist — the CSVs hold
everything it holds and more. It is still written, because it is the one artefact small enough
to hand to a colleague, paste into a ticket, or carry to a different agent.

**If the two ever disagree, the CSVs win.** Regenerate the ledger from them rather than
reconciling it.

### Reading a pasted one

**Count the firm lines against `#END rows=N`, and say what you found.** A mismatch, or a
missing `#END` (the usual shape of a truncated paste), does not stop you — a half-pasted
ledger still prevents half the duplicates. It is simply reported: *"The ledger says 46 rows;
I can see 31. I will deduplicate against those 31 and treat the rest as unseen."*

**Trust it for identity and nothing more.** Names, keys, domains and `status` decide whether
a firm is new. A wrong one costs a single duplicate row. That is the whole of what a pasted
file may decide.

**A `#LEDGER` version that is not this skill's still deduplicates.** Identity is stable
across versions; that is why the format holds nothing else.

**`#SCOPE` is binding** — same rule as the index above.

**Rows from a ledger never enter `investors.csv`.** They carry no source, no headquarters,
no `checked` date. Writing them into the deliverable would put unsourced rows in the file
this skill exists to keep clean. They suppress rediscovery; they do not become results. If
the user wants the earlier firms in the new output, they have the earlier output — say so.

### When a fold key changes underneath you

`references/lists.md` is extended per market — in `investor-search/lists-local.md`, never in
the installed skill — and the fold key is a function of those lists. Add a legal form between two runs and the same firm can key differently.

So **when a ledger line's `key` does not match but its `domain` does, it is the same firm.**
Match on domain first, key second, display name last. Never merge two ledger lines on a fold
key alone — the merge rules in Job 3 apply here exactly as they do to live rows.

---

## 3 · Handing the result to the user

The three steps are stated in `SKILL.md` (*Output — six files*). What each one costs:

**Step 1 is not optional and not sufficient.** The agent is the only party that knows where
its working directory resolves to. Naming `investors.csv` without the directory has delivered
nothing.

**Step 2 is how a user who cannot open the path still gets the file.** In OpenClaw that is a
`MEDIA:/absolute/path` line in the reply, and it works only through the messaging gateway —
in the CLI and TUI it prints as plain text (`SKILL.md`, *OpenClaw*). Check which one this
session is before relying on it, and if a delivery cannot be confirmed, say so and give the
path as well. In a shared channel, ask first — a file sent there reaches everyone in it.

**The same mechanism is tier B** (`SKILL.md`, *Before Job 0* §7): when no folder can be kept,
the files are written wherever the agent can write and handed over, and the user brings them back
next time.

**Step 3 is the floor, not the output.** CSV text in a chat is for a session with no way
to hand over a file at all — no file toolset. Nobody ends a run with nothing.

**Say which step you took.** Silently falling to step 3 reads as the skill failing to produce
a file at all.

### Printing a CSV into a chat — tier C only

- **One fenced block, nothing else inside it.** Outside a fence, markdown eats the commas and
  quotes and the user pastes a broken file.
- **If it will not fit one message, number the parts** — `# part 2/3` as the first line —
  repeat the column header in every part, and put `#END rows=N` at the end of the last.
  An unnumbered continuation cannot be reassembled by anyone.
- **Never print a truncated CSV without saying it is truncated.** A file that silently stops
  at row 40 of 130 is this skill's founding failure, reintroduced at the last step.
- **`investors-rejected.csv` is never printed and never attached** — only counted.

---

## 4 · What to tell the user about their own setup

Two situations are worth one sentence each, because the user can fix them and the agent
cannot.

**Writing silently goes somewhere else.** In OpenClaw this is a sandboxed agent whose sandbox is not kept, or two
agents (or a CLI and a gateway) with different workspaces: the write succeeds and the next run looks somewhere else. The symptom is
specific and recognisable: **every run behaves like a first run.** If a user says they have
run this before and nothing was found, that is the thing to describe — not as a diagnosis of
their configuration, which you cannot see, but as the one cause worth checking.

**The working directory is shared.** Where several people use the same agent, they share its
files. Anything written here is visible to all of them — which matters most for
`investors-rejected.csv`. Say it once, when that file is first written. Use a per-user or
per-team root when the inbound context names the chat or channel, and warn before resuming shared files when it
does not (`SKILL.md`, *Before Job 0* §6). The fix the user can make is on the OpenClaw side: a
separate agent with its own workspace for each user or team.
