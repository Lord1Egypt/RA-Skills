# Investor Search for PicoClaw

> **Install in PicoClaw:** `picoclaw skills install --registry clawhub investor-search-picoclaw` (the command shown above it on ClawHub is for another agent)

**Build a sourced list of the investors in a market — and say honestly how complete it is.**

Ask an AI agent for family offices in a country and you get the number you asked for. Ask
again tomorrow and you get an overlapping but different set, with no way to tell which firms
are new and no way to know what is missing.

This skill replaces the number with a rule, separates real investors from the advisers who
sell to them, and writes files where every claim carries the page it came from.

## Install and use

```
picoclaw skills install --registry clawhub investor-search-picoclaw
```

Do not edit the
installed copy — the skill keeps what it learns (extra legal forms for a new market, for
example) in its working folder (`investor-search/lists-local.md`), not in its own files.

**It runs a small Python script** (`scripts/store.py`, standard library only) through the
`exec` tool. From a chat channel that needs `tools.exec.allow_remote` (on by default); without
exec the skill still answers, but cannot keep its memory between runs.

Then ask in plain language — or name it (`investor-search-picoclaw`) in your message:

```
find the family offices in Austria
who are the private investment groups in Poland
enrich my investors.csv — fill in the missing websites and people
family offices in Germany that invest in software
```

**It needs a web search tool and a fetch tool.** No CRM, no database, no account, no API key,
no configuration. (Your web search provider may need a key of its own — that is the agent's
setup, not this skill's.)

**It writes files, and reads them back.** The memory of this skill *is* those CSVs —
deduplication, the pending queue, the round history and the exhaustion gates all read from
disk. So it puts them somewhere predictable — in the agent's workspace (by
default `~/.picoclaw/workspace`) — and looks there first:

```
investor-search/index.md
investor-search/poland/investors.csv · sources.csv · pending · rejected · rounds · ledger
```

Run it again next month and it finds that folder, tells you how old the newest check is, and
continues instead of repeating. Ask for a market it has never seen and it says that too —
because silence reads as continuity.

**You get one file: `<market>-investors.xlsx`.** The first sheet is the firm list with a
`source_links` column; the other sheets hold the evidence, the open queue, the round history
and the ledger. In Slack, Telegram, WhatsApp, Discord or Signal it arrives as an attachment; in the
terminal you get the full path.

**It searches until the results stop** — six rounds in a row with no new firm, across
different kinds of source — and never asks you for a budget. Say "use 10 rounds" if you want
a quick scan. Sixty rounds is the ceiling unless you ask for more.

It does not guess whether it can keep a folder; it tries in the first minute. If it cannot,
you hear it then, and the same Excel file becomes the memory: upload it next time and the
run continues from it. Only a session with no way to send a file at all gets CSV text in the
chat.

**What it will not do in that case is claim a market is finished.** The completeness check
reads the pending queue and the round log; with no folder there is nothing it can read back,
so the answer is PARTIAL and says so. The files it hands you include a **ledger** — one line
per firm; upload the file (or paste the ledger) next time and the next run skips what this
one already decided. The ledger makes a run
cheaper. It never makes one finished.

**Say `continue Austria` (any market) to carry on** — the next run reads the files, skips
every firm already decided, and works the pending queue first. A run that was cut off
(model limit, crash) resumes where it stopped; its empty rounds still count.

**A full run can take more than one turn.** PicoClaw ends a turn after
`max_tool_iterations` tool calls (50 by default). The skill then reports PARTIAL progress;
say `continue Austria` and it picks up from the files. Raise the limit in
`agents.defaults.max_tool_iterations` for longer runs.

**Two PicoClaw notes.** A message sent to the same chat while a run is working stops that run;
say `continue Austria` to resume. PicoClaw 0.3.1 cannot upload files to Slack ("file size
cannot be 0"); the skill then tells you the path of the Excel file in the workspace.

**Every run starts the same way, before any search:** it reads what is on file, writes
`index.md` and reads it back, creates any missing file with its header, and says in its first
reply which folder it is using and what it found — market, scope, firm count, pending count,
and the date of the newest check. If you ask a different question of a market already on file
(*investors active in* rather than *headquartered in*), it asks before mixing the two.

**Shared and public bots.** Everyone who uses one agent shares its workspace.
In a group chat or channel the skill keeps that channel's files under
`investor-search/@<channel>/`; where it cannot tell, it warns before using files already there.
`investors-rejected.csv` names firms with a negative judgement, so it is never printed or
attached — only counted. If you run a bot for several people, the safest setup is one agent
per team, each with its own workspace.

**Scheduled runs** (cron jobs) continue a stored market without asking; anything that
would need a question — a different scope, a shared folder — stops before the first search
and reports the question instead.

**It will never use the conversation as memory.** Chat history truncates silently, and an
agent reading it believes it has seen every firm when it holds only the last few — which
produces confident duplicates, worse than an admitted blank slate.

## What it does differently

**It knows an investor from an adviser.** A search for "family office" in any language
returns mostly law firms, accountancies, private banks and company-formation agents selling
family-office *services*. They have the words in their name, a real site and a real address —
and they pass every check most tools apply.

> Measured: in one market, **five of the six** firms verified through local-language search
> were advisers rather than investors. In another, **52% of everything resolved**. One
> targeted query returned eight results, eight advisers, zero investors.

This runs first, rejects them to their own file, and reports the count.

**It refuses to merge two firms into one row without proof.** Accents transliterated, legal
forms stripped in every written form and at both ends of the name, leading articles handled,
transliteration variants treated as one firm. But two names that fold to the same key are
only merged when a shared domain agrees — otherwise both are kept and the pair is flagged.

> On one run a single fold key collided **five ways across four domains**. An earlier version
> would have written them as one row with all five sets of sources pooled and nothing marking
> it. A place name never counts as distinctive, because `<City> Capital Group` and
> `<City> Investment Office` are not the same organisation.

**Empty stays empty.** A field it cannot source is blank. It will not infer an email from a
name and a domain, or a city from a phone code. A guessed cell is a lie inside a file
someone is about to act on.

**It searches the language business is actually conducted in** — which is not always the
country's. One market offered five times more names in the local language; another offered
73 names in English against 1 in the local language. The skill carries a test for which, and
reports both rates so you can see when it chose wrong.

## The stopping rule — and what it can and cannot claim

The rule is six consecutive rounds producing no new verifiable name, behind four gates: a
record that exists on disk, nothing resolvable left unverified, dryness across at least three
different kinds of source, and no round in the streak resting on a page that failed to load.

**The gates exist because the rule was tested and failed.** On a small market it declared
exhaustion at round 23 and was falsified at round 26 by one query shape that had not been
tried. Four of the final 29 firms — 14% — arrived after the rule said "finished".

So the claim is now the narrower true one: **exhausted on the surfaces named**, and it names
them, so a reader who knows a further surface can say so.

**Be clear about what is proven.** Gates 1 to 3 were written after that test and **have not
themselves been proven in a run.** Every run behind this package stopped on budget, not
on exhaustion. What this skill reliably produces today is a **defensible partial list** —
sourced, deduplicated, adviser-filtered, and explicit about what it did not reach. The
completeness claim is a design with an argument behind it, not a measured result.

## What you get

**Delivered:** one `<market>-investors.xlsx`. **Kept in the folder** (the memory, never
sent):

| file | what it holds |
|---|---|
| `investors.csv` | the firms — one row each, with a dated check and a stable `id` |
| `sources.csv` | one row per citation: `id, field, rung, url` |
| `investors-pending.csv` | offered but unresolved, with a reason — makes the next run cheaper |
| `investors-rejected.csv` | refused, with the reason — **a local working file, not for sharing** |
| `rounds.csv` | what was queried, on what surface, and what it yielded |
| `ledger.txt` | one line per firm — identity only, so a later run can skip what this one decided |

All six live in `investor-search/<market>/`. A later run reads them before it searches, so it
fills in what it holds rather than doubling it. Where nothing can be written, the ledger
carries identity forward and the skill says plainly that that is all it carries.

## What it will not do

- **No email addresses.** Almost no family office publishes one, and inventing them is the
  exact failure this exists to prevent.
- **No ranking, scoring or recommendation.** It is not investment advice.
- **No firms with no web presence.** Some single family offices are deliberately invisible.
- **No confidence scores.** On one corpus, only 5% of claims carried one at all and those
  clustered at 0.99 — a number that distinguished nothing while inviting more trust.
  Provenance labels replace them.
- **No judgement it cannot show you.** Every rejection is in a file with its reason.

## What's in the box

```
SKILL.md                     the rules — read this while working
README.md                    this file
references/lists.md          legal forms, generic tails, place words, type words
references/why.md            what was measured and what broke, rule by rule
references/environment.md    where files go, the ledger format, delivering a file to the user
scripts/store.py             the only writer of the memory files — append-only (Python 3, stdlib)
```

**The memory is protected by code, not only by rules.** A second run once rewrote the
first run's files from memory. Since 1.2.0 every write goes through
`scripts/store.py`, which never removes a row, never renumbers an id, skips firms already held
or rejected, and counts the empty rounds itself. It needs `python3` and the `exec`
tool.

**Three reference files in the skill, and the split is deliberate.** An earlier single file put every rule next to
its justification, and a review found the predictable result: *"every defect I found is a
rule that exists but is unreachable at the moment of decision."* The reasoning is still
shipped — it is just not in the way.

**Be aware of one number before you read `SKILL.md`:** it is about 45KB, which is the size a
reviewer was looking at when they said *"at 45KB the justifications win."* The split
moved that file's justification out and then later runs put new rules in, and it arrived
back at the same figure by a different route. What is in it now is mostly rules — but nobody
has measured the ratio, so this package does not claim one, and the reachability of a rule at
the moment it is needed remains the thing to check first if you extend this.

## Where the rules come from

The core came from a production investor-research system run over several months and
hundreds of pages. It was then run in five markets as a standalone skill, and each run
rewrote it:

| market | what it found |
|---|---|
| **Czech Republic** | 13 defects. No adviser test at all. A fold whose step order silently broke every dotted legal form. A classification rule that blanked the types it got *right* |
| **United Arab Emirates** | The fold **merging two different companies into one row**. Nine of ten local legal forms not folding. The language rule inverting |
| **Singapore** | The fold rewrite vindicated — one key collided five ways and none were merged. 14 more defects, and the finding that the file had grown too long to follow |
| **Estonia** | The stopping rule fired for the first time — **and was wrong, falsified inside the same run.** Legal forms written in front of the name. Rebrands invisible to every rule there is |
| **Latvia** | Run under the current rules. **Job 0 barely fired** — 16 of 31 association members went undecided because the rules forbid judging from a name and the budget went on searching wider. One firm ran three funds; another listed two headquarters |

**No sample output ships with this package, and that is deliberate.** Five runs produced real
files, and each one was a snapshot of the rules as they stood on the day — which made every
shipped sample a set of claims about itself that had to be kept true as the rules moved. Four
successive audits found more defects in the sample and in the sentences describing it than in
the rules themselves; the last one found a sample that broke a rule the same run had just
produced.

So the package ships the schema, the column meanings and the citation format, and no data. If
you want to see the output, run it — that is one prompt, and the result will be built by the
rules as they are today rather than as they were when someone last exported a file.

## Licence

**MIT-0.** Use it, change it, redistribute it, sell work built with it. **Attribution is not
required.**

If you extend the lists for a market we have not covered, open an issue or a pull request
here — the rules get better for everyone.
