# Mode: discover — find roles worth considering

Loaded unconditionally on entering discover mode. Read it in full before the first
adapter call.

**What this mode does:** turn a search intent into a shortlist of real, retrieved
job listings with a provisional verdict on each. **What it does not do:** it never
chains into `apply`. Thirty rows do not become thirty CVs; the whole point of
ranking a shortlist is to let a person choose.

**Write the shortlist in the user's language, one language end to end** (CVs follow the
target market; shortlists, assessments and debriefs follow the user). English and Chinese
literals are below, and the gate accepts all five report languages. **Writing the
shortlist in Japanese, Korean or Spanish: read `references/report-localization.md`
first** — it holds those languages' provisional stamps and disclosure templates. Fill
them with real answers; never an invented retrieval or login state.

## A complete job-search consultation

When the user requests a broad search and recommendations, a single application
example is not a complete delivery. Agree or infer a practical collection target
from the request and retain it separately from each round's safety caps. A target
of dozens of jobs may require multiple bounded rounds; never increase a site's
read budget or invent listings to reach that target.

Keep a collection manifest with the requested count, maximum rounds, completed
round workspaces, deduplicated posting URLs/IDs, and shortfall reasons. Continue
independent sources while a site awaits login or recovery. Refusal locks and
per-consultation limits survive round changes; a new folder never resets them.
Reaching the collection target does not end lead gathering: every registered
source and direction still needs its result and every observed lead a
disposition (`references/search-coverage.md`). Before
final delivery, read the full description for every retained posting, including
each city/ID under a grouped title. Continue within the existing source caps;
never reset a stop lock or raise a cap to finish. If agreed rounds are exhausted,
report that the work is incomplete rather than calling unread leads complete.

Each round still passes its own shortlist and evidence gates. The final client
report combines unique roles across those verified rounds, explains priorities
and tradeoffs, gives concrete application actions and role-specific interview
preparation. A complete report contains detail-reviewed postings; a genuinely
unavailable detail can remain only as an explicitly unresolved lead with a
captured access failure and a visible reason. Unattempted cards belong in the
research workspace, not a finished report. An explicitly requested preliminary
shortlist may include them; record the user request as described below.
Undisclosed or overlapping salary ranges are confirmation items, not proof that
a pay floor is satisfied. Do not create a tailored CV for every lead by default.

### Final detail coverage and collection delivery

`brief.report_scope` defaults to `complete`. Use `preliminary` only when the user
explicitly asks for an initial/partial list or chooses to publish the current
partial report; record their request in `brief.preliminary_request` and explain
which requirements remain unchecked. Do not choose this mode to avoid more work.

Read every retained description before completing the report. The 1–5
`max_match_reviews` cap limits **requirement-by-requirement CV mappings**, not the
number of retained descriptions to read. Once a full description is read, a row
outside that mapping batch uses `basis: detail_unmapped`, `recommendation: review`,
empty `requirements`, no `alignment`, and `job_evidence` quoting its duties and
requirements from the journaled detail. It does not count against the mapping cap
and cannot become a default recommendation. Use later bounded rounds for more
CV mappings when the request requires them. Never infer that an unmapped row is
unsuitable; say what has and has not been checked.

If a genuine access failure prevents a read, preserve the failed capture and add
`shortlist.yaml.detail_unavailable: [{id: site-id, reason: <reader-facing reason>,
capture: raw/<failed-capture>}]`. Show that exact reason beside the job in the
report. A site-level login or risk-control stop can explain affected rows without
retrying each one. Time spent, a reached job count or the mapping cap is not an
access failure. Do not recommend an unresolved row. Closed roles stay out of the
client report as required by `references/discover/multi-posting-report.md`.

For one round, `deliver.py` checks every row in its shortlist. For a consultation
spanning several rounds, put `report.md` and this manifest in a delivery workspace:

```yaml
# collection.yaml — private delivery inputs; not a client artifact
report_scope: complete
rounds:
  - workspace: ../round-01
    ids: [site-123, site-456]  # only final retained rows; omit ids to include all
  - workspace: ../round-02
    ids: [site-789]
```

Use existing round workspaces with passing, current shortlist checks. The manifest
selects the final set without deleting earlier search evidence. `deliver.py`
checks each selected ID, its full-description evidence (or captured failure), and
its link in the aggregate report. It refuses an unread card even if every search
round previously passed. The collection's report scope governs all its rounds;
a preliminary collection also needs its own `preliminary_request`.

Mock interview remains opt-in: include preparation in the report, then enter the
interview mode and its interactive coaching workflow only when the user asks to
practise. Never invent an interview transcript or start a mock on their behalf.

## Supplementary public research

Use `references/supplementary-sources.md` when official web/news, GitHub,
WeChat articles or relevant role discussions can fill a concrete
career evidence gap. It defines provider availability checks, source quality and
source-selection records. These sources supplement
formal posting evidence; they do not replace it or run automatically on every task.

## On entering this mode — before anything else

```bash
python3 scripts/enter_mode.py --workspace <ws> --mode discover \
    --because "<why discover, in one line, from what the user asked>"
```

This writes a `mode_entry` with this file's content hash to `journal.jsonl`.
`check_shortlist.py` fails with `NO_MODE_ENTRY` when it is absent and
`MODE_FILE_CHANGED` when this file changed afterwards (re-enter and re-read).
Then read this file in full: the `shortlist.yaml` fields the gate requires are
defined only here.

## Entry conditions (any one)

1. The user wants to find or compare roles.
2. `assess` returned `likely_screen_out` or `blocked`.
3. The honest-gap early-stop fired.
4. `assess` returned `stretch` and the user has not said they want that specific job.
5. The user supplied two or more postings (ranking mode).

Discover is **never** triggered as a side effect of another mode; no implicit calls.

## Ownership

| Reads | Writes |
|---|---|
| `profile.yaml` (never modified by any mode) | `searches/<YYYY-MM-DD>-<slug>/`, plus `search-preferences.yaml` — the one spine file discover owns |


Workspace layout — **the path shape is load-bearing**, the resume-an-unfinished-run
feature finds work by this shape:

```text
~/.claude/job-profiles/<name>/searches/<YYYY-MM-DD>-<slug>/
  brief.yaml                 this round's reproducible search basis
  shortlist.yaml             the structured shortlist
  candidate-profile.yaml     frozen profile used for this round's match evidence
  candidate-match.yaml       per-row JD ↔ frozen-profile evidence mapping
  shortlist.md               readable: §0 来源与读取质量, §0.1 触发原因, §0.2 披露
                             (English round: §0 Sources and read quality,
                              §0.1 Trigger, §0.2 Disclosure)
  raw/<site>-<n>.json        adapter stdout, VERBATIM, never edited (run_tool.py names
                             it raw/<site>-<32-hex id>.json; <n> is that id)
  raw/<site>-<n>.stderr.txt  adapter stderr for the same call
  raw/opencli-help/<site>.yaml   the adapter's own metadata for this run
  raw/auth-status.json       the auth probe output
  journal.jsonl              mode_entry + adapter_call records + gate receipts
```

**Resolve both spine paths through `scripts/paths.py`, never by hand:**
`paths.search_dir(<name>, "<YYYY-MM-DD>-<slug>")` for the workspace above and
`paths.search_prefs(<name>)` for the preferences file below. A hand-joined path
silently orphans the previous workspace.

Never edit `raw/*`: every downstream claim's provenance chain terminates there.

## The shared search preferences — asked once, reused, confirmed

`paths.search_prefs(<name>)` → `~/.claude/job-profiles/<name>/search-preferences.yaml`.
Discover **owns** this file: it is the only mode that writes it, and `assess` reads
it to avoid asking for the target market once per posting.

```yaml
updated: "2026-08-09"
target_market: cn                    # cn / nl / de / uk / us / other
locations: ["上海", "西安"]           # cities or regions, in the market's own language
seniority: mid                       # new_grad|junior|mid|senior|unknown
work_models: ["onsite", "hybrid"]    # remote|hybrid|onsite
languages: ["Chinese", "English"]    # languages the user can work in
salary_floor: {currency: CNY, amount: 30000, period: month}   # or null
avoid: ["外包", "销售导向岗位"]
experience_track: "medical imaging / MRI reconstruction"
employer_types: ["国企", "外企"]     # cn only — see below; omit for other markets
```

**`employer_types` is asked for a `cn` round only** (大型私企 / 中小型私企 / 国企 / 外企;
51job returns `companyType` and `companySize` on every card) and omitted elsewhere.
Ask it as a multi-select; "no preference" is a valid answer, not all four. It is a preference, not a filter: rank a
row outside the chosen types lower and say its type in `why_matched`.

**Every field here is asked, never inferred** — not from a payslip, a CV, or the
language the user happens to type in. The file is reused across later rounds.

- **First run** (the file does not exist): ask the questions above, in the
  user's language, in one pass. `salary_floor: null` is a legitimate answer and the
  only correct one if the user declines — never substitute a market median.
  `target_market: other` is likewise legitimate: markets outside `cn/nl/de/uk/us`
  have no convention data, and saying so beats borrowing a neighbour's.
- **Later runs:** read it, show the user what it says, and **confirm once per
  session** — not once per posting. Re-ask whenever this round's locations sit in a
  different market than `target_market`.
- Rewriting it is an explicit act with the user watching. Bump `updated` when you do.
- `brief.yaml` below is this round's *narrowing* of these preferences, not a copy of
  them: preferences are durable, a brief is one round.

A weekly-digest round runs this mode from the digest's standing brief, with the user
present, as described in `references/weekly-digest.md` (the brief and preferences are
not asked again).

## Before Step 0 — region, then platforms, then the login hand-off

Run these three in order, before the trigger reason and before `brief.yaml`.

### 1. Ask the region, as options, on its own

Never infer it. Not from the language the user is typing in, not from their
profile's `meta.target_market`, and not from a stored preference file — a stored
`target_market` is shown for confirmation, and the region for THIS round is asked
whether or not one exists. `brief.locations` is the round's own narrowing;
`search-preferences.target_market` is the durable setting, and the two can
legitimately differ.

Offer concrete regions rather than a blank question — United States, United
Kingdom, Netherlands / Europe, China, Middle East, and whatever else fits what
you know about them. Then ask cities inside it, because an adapter's location
parameter takes a city, not a country.

**If the round's region is a different market than the stored `target_market`,
re-ask the whole preferences file**, not just the market: a salary floor in EUR
and an avoid-list entry reading "roles requiring fluent Dutch" mean nothing in
Shanghai. Back the old file up before rewriting it: the user may be exploring,
not switching.

### 2. Say which platforms that region actually has

Before any search, tell the user which adapters serve their region and which need
a login. This is what lets them fix a missing session BEFORE the round runs
rather than after it.

This table is about ONE thing: which adapters return **job listings**, i.e. rows
that can become `shortlist.yaml` entries. Everything else about any adapter —
flags, pagination, measured login state, identity field — lives in
`references/discovery-sources.md`, which is the source of truth and must be read
before calling a discovery adapter.

| region | job listings, no login | job listings, needs a login | do not use for listings |
|---|---|---|---|
| United States | `indeed` (its native site) | `linkedin` | — |
| China | `51job` | `boss` | — |
| Netherlands · Germany · UK · rest of Europe | Indeed's **country site** (`nl.indeed.com`, `de.indeed.com`, `uk.indeed.com`) through the diagnosed browser route — see below | `linkedin` | the **`indeed` adapter** — it resolves locations against a US gazetteer, so a European city returns US rows |
| Middle East · anywhere with no convention table | Indeed's country site **if the official country directory lists one**, through the same browser route | `linkedin` | the **`indeed` adapter**, same reason; `target_market: other`, and say plainly there is no convention data for this market |

The ban in the last two rows belongs to the installed **`indeed` adapter** (origin
hardcoded to `www.indeed.com`), not to Indeed's country sites. Read a country site
through the built-in browser route (fallback reason `unsupported_extraction`, see
`references/browser-fallback.md`). Expect a bot-block there: a 403 or a challenge is
a **site refusal** — stop that site for the round and say so; it is never evidence
that the country has no matching jobs.

**No adapter covers a market's own boards, and that does not put them out of
reach.** Employer career pages and market-native boards are readable through the
same browser route, using the site's own search box — for research and academic
roles in the Netherlands, `academictransfer.com` is the canonical one. None of
them were measured here, so treat a named board as a place to look rather than a
verified adapter, and record what was actually read.

**A site being absent from the "job listings" columns does not make it useless, and
saying it has "no search command" is wrong.** `nowcoder` has a search command, but it
returns 面经; a forum thread is not a posting with a `source_id` a row can be traced to.
`nowcoder` (面经/内推 threads), `maimai` (recruiter-side `search-talents` only) and
`upwork` (freelance) produce no shortlist rows. For a Chinese campus round
(`seniority: new_grad`), point to Nowcoder 面经 and 内推 threads in the report — a
pointer, not a row.

### 3. Hand the login to the user, then wait

`opencli <site> login` is a **write** command. `references/source-policy.md` puts
it on the Red list: it is never run here. Ask the user to click Login/登录 on the
page kept open in their daily browser, not to run a terminal command. Follow
[user recovery](../references/user-recovery.md) and wait for their explicit reply.

So say it plainly and wait:

> `boss` needs a browser session. Click Login/登录 on the page already open in
> your daily browser, finish login, and tell me when it's done — then I can search there.
> It is a logged-in adapter, which `source-policy.md` puts in the yellow tier:
> the search runs inside your own session, and account risk is not zero.

**A quick `opencli auth status` probe can report `not_logged_in` for a live session.**
Before asking the user to log into a site the quick probe called `not_logged_in`,
re-probe it with `opencli auth status --site <site> --full`.

Only once the region is fixed, the platforms are named, and the sessions the
round needs are actually live, go on to the trigger reason and `brief.yaml`.

## Step 0 — state the trigger reason BEFORE searching

Say why this search is happening, then write it into `brief.yaml` as
`trigger_reason` and into `shortlist.md` under `## §0.1 触发原因` (English round:
`## §0.1 Trigger`; the gate keys on the language-agnostic `§0.1`). Stating it
afterwards is a rationalisation; `check_shortlist.py` fires `NO_TRIGGER_REASON` and
`NO_TRIGGER_SECTION` if either is missing.

If the original JD was judged unsuitable: **this round's candidates must be visibly
more solid than it, not merely similarly titled.** Write how, per row, in
`why_matched`.

### brief.yaml — this round's reproducible basis

```yaml
slug: 2026-08-09-suanfa-shanghai       # <YYYY-MM-DD>-<short-slug>
created: "2026-08-09"
trigger_reason: "上一份 JD 被 assess 判为 likely_screen_out（缺 C++ 生产经验）…"
target_titles: ["算法工程师", "algorithm engineer"]
report_label: "算法岗"                 # optional: the direction in the reader's words, used in
                                       # the report filename; default: first target title
markets: ["cn"]                        # cn / nl / de / uk / us / other
locations: ["上海", "西安"]
seniority: mid                         # new_grad|junior|mid|senior|unknown
employment_types: ["full_time"]
work_models: ["onsite", "hybrid"]      # remote|hybrid|onsite
languages: ["Chinese", "English"]
must_have_constraints: ["work authorization: …"]
nice_to_have: ["计算机视觉"]
avoid: ["外包", "销售导向岗位"]
target_count: 12                       # how many rows the user wants
max_rows_per_round: 25                 # yellow-layer cap, per site per round
max_pages_per_site: 2                  # yellow-layer cap
max_match_reviews: 5                   # 1-5 full JDs eligible for CV matching
max_age_days: 30                       # older than this ⇒ verification: stale_possible
```

**`target_count` is a collection target, not the size of the labour market.**
Use an explicit requested count. Otherwise, for a broad search, state a practical
working target and continue; do not silently limit the search to three or five
examples. Ask only when the number or scope materially changes the desired
result. Keep this consistent with “A complete job-search consultation” above.

Before accepting a shortfall, inspect the source coverage: how many distinct
leads were observed, how many obtained complete descriptions, and how many were
actually excluded for candidate fit or eligibility. Unread details are an access
or extraction backlog, not evidence that the market has no jobs. For a named
industry, cover relevant employers and role synonyms (for investment banking,
股权/债券/并购/保荐承销/财务顾问/ABS/REITs, including graduate and campus labels).
Do not count unrelated trading, asset management or investment-research roles
as investment banking merely to reach a number.

A written `shortfall_reason` explains a remaining limitation; it is **not a stop
condition by itself**. Resolve known catalog-to-detail gaps using supported
navigation, continue already authorized bounded rounds/independent sources,
and only then report any remaining shortfall. Preserve source caps and refusal
locks. Distinguish “found N verified postings in the sources checked” from
“only N postings exist”, and do not imply exhaustive market coverage.

`target_count` and `max_rows_per_round` are different things: the first is the goal,
the second is the politeness cap from `references/source-policy.md`. Falling short of
`target_count` requires a written `shortfall_reason` in `shortlist.yaml`
(`SHORTFALL_NO_REASON`). **Never pad the count.**

### Freeze the profile before reading job details

First run the online-presence step (`references/online-presence.md`,
`scripts/online_presence.py status --name "<name>" --workspace <ws>`): confirmed
findings written into the master before the snapshot become this round's evidence.

The recommendation is about the CV supplied for **this** round, not a master
profile that might change tomorrow. Before the first detail fetch, create the
round-local snapshot once:

```bash
python3 scripts/snapshot_profile.py --workspace <ws> --profile <master-profile.yaml>
```

This writes `candidate-profile.yaml` without changing the master. If the source CV
changes, start a new round rather than replacing the snapshot: changing it would
silently alter the evidence behind an already-ranked shortlist. Read
`references/candidate-matching.md` for the mapping rules and schema.

`max_match_reviews` is a separate, bounded decision cap: ask for it with the brief
and set an integer from 1 to 5. It is the maximum number of fetched full descriptions
that can receive a CV-to-JD mapping in this round. It does not raise the source-policy
page or row caps, and it is not a target count.

## Retrieval backend — OpenCLI first; one-way built-in CDP fallback

Before using OpenCLI for the first BOSS, Indeed, 51job, LinkedIn or Nowcoder read, follow `references/opencli-compat.md`:
check and automatically apply only the known version/hash-matched local repairs
with `scripts/opencli_compat.py`. Do not overwrite custom edits or force a patch
onto another version. This local preparation performs no site reads and cannot
reset a site's refusal. Browser fallback can use the site's own search box;
it is not limited to Google or other search engines.

Before Step 1, run `python3 scripts/doctor.py` and inspect the adapter's
read help and actual transport. **OpenCLI is the initial backend, in CDP mode
only.** The diagnostic probes the installed website browser factory offline;
it never connects to an extension. Verify the selected live CDP endpoint and
adapter path separately before reading a site. Do not run an extension-backed
adapter merely to obtain a failure first.

Never use browser extensions, including already-connected ones. The presence of
a CDP class, an endpoint environment variable, or a successful generic health
check does not prove the website adapter uses CDP. When the installed website
factory still selects Browser Bridge, record `unsupported_extraction` with the
version and routing evidence, then use built-in CDP.

Only a diagnosed `cli_missing`, `bridge_disconnected` (a failed CDP connection),
or `unsupported_extraction` permits the one-way fallback in
`references/browser-fallback.md`. On that path skip OpenCLI-only auth/help
commands and retain source selection, query, page, row, detail and disclosure
rules. There is no built-in-CDP-to-OpenCLI fallback for the same round: if that
CDP fallback is unavailable too, disclose the gap. Do not stop merely because
an optional adapter executable is absent.

### Local CDP connection versus a sandbox boundary

An `EPERM`, timeout or connection refusal at a local CDP endpoint can come from
the agent runner. Preserve the error and verify the already-selected CDP
connection through an available approved host-local or unsandboxed path, only
when the platform requires it. Existing authorization is sufficient; do not
request permissions that the host does not support. Never use a daemon's
extension connectivity as this check.

If that same CDP route is verified, repeat the single bounded read on it. If it
still fails, retain `bridge_disconnected` and try the one-way browser CDP
fallback. `EADDRINUSE` does not authorize killing a shared process, changing its
port, reinstalling tools or restarting the user's browser. This is only local
connection recovery before a site refusal, never a way around a site stop.

For an unexplained page failure, follow `references/network-recovery.md` before
choosing a fallback reason. Use `references/daily-browser.md` after the OpenCLI
CDP diagnosis permits built-in CDP; keep the same source, query, page, row, detail
and disclosure rules. Site login remains a user action.

Browser captures use `scripts/record_browser_capture.py`, `browser_call` journal
records and `extraction_method: browser_page`. They are not adapter responses.
Both `check_no_write.py` and `check_shortlist.py` consume these records. A captcha,
403, login wall or platform limit is a **site refusal**, not a backend-capability
failure: it stops the site across tools for this round. Never try built-in CDP to
route around an OpenCLI site refusal, or vice versa.
A stop is a pause for [user recovery](../references/user-recovery.md), not a
reason to abandon the requested search. Explain the actual obstacle and wait for
the user's explicit completion/continue reply before a new linked round.

## Step 1 — probe the login state (three states, not two)

Every live OpenCLI or browser read goes through one persistent browser session, so
start it once for the task (`run_tool.py` refuses a live read without it). The auth
probe is not a planned source, so run it **without** `--workspace` and save it into
the round yourself:

```bash
python3 scripts/run_tool.py browser-session start
python3 scripts/run_tool.py opencli auth status -f json > <ws>/raw/auth-status.json
```

- `status: "logged_in"` — usable.
- `status: "not_logged_in"` — usable only for adapters that do not need a session.
- `status: "unknown"` — **not the same as logged out.** Its `logged_in` field is an
  **EMPTY STRING**, not `false`, so `if (!row.logged_in)` misreads it. Re-probe:
  `opencli auth status --site <sites> --full --timeout 40 -f json`, which runs the
  read-only `whoami` and returns `checked: "full"`.
- **Site absent from the list entirely** — `no_auth_adapter`. `indeed` and `51job`
  are not in the list and neither exposes a `login` or `whoami` command. This is
  not an error and not a missing adapter: it means the adapter has no auth command. The website can still require login or
  verification; classify the actual page. Never run `opencli 51job login`; it does
  not exist.

Each adapter's own contract lands in `<ws>/raw/opencli-help/<site>.yaml`, which
`check_no_write.py` reads. `run_tool.py --workspace <ws> opencli <site> …` saves it
automatically before every recorded read; save it yourself only for a capture made
by another runner.

## Step 2 — choose sources

For domestic job discovery, read the WeChat coverage procedure in
`references/supplementary-sources.md` now and include it in the source plan.
Carry relevant leads from targeted queries through original-article reading and
recruitment-condition checks. Preserve the distinction between search snippets
and verified openings; follow the existing read budgets and site-stop rules.

Prefer sources that need no login. `51job` is the only adapter measured to return
every documented column populated. `indeed` also works without login but returns
empty titles (Step 4). Use the command pairs and adapter metadata in
`references/discovery-sources.md`; read the relevant source entry first.

**The `indeed` adapter serves the US site only** and resolves `--location` against a
US gazetteer, so a non-US city silently returns US rows with exit 0 and
`classification: ok`. For `cn`, `uk`, `nl` or `de`, do not
use the adapter: read the country site (`https://cn.indeed.com/`, `nl.`, `de.`, `uk.`;
others from Indeed's [country directory](https://www.indeed.com/countries)) through
the browser route in the region table, with this round's `brief.locations`, or use
the region's other sources. Keep country-domain URLs for search and detail. Read
every returned `location` against the requested country and city
(`WARN_ROW_OUTSIDE_BRIEF_MARKET` only catches rows, not an empty result), and never
turn a wrong-country or unreadable result into "no jobs in this market".

## Step 3 — generate queries in BOTH languages

Generate the keyword set in English **and** in the market's local language, and run
both. **English-only keywords miss local-language postings**: a Dutch employer
posting "Onderzoeker beeldreconstructie" or a Chinese one posting "图像重建算法工程师"
is invisible to an English-only query, and the empty result looks like "there are no
such jobs".

Record every query string in `brief.yaml.target_titles` so the round is reproducible.

**Split the row budget across the query set BEFORE the first call — the cap is per site per round, not per query.**
With N queries and a cap of R rows, run each at about `R // N`, rounding up for the
tracks the user named first. Two or three queries at 8-12 rows beat one at 25. More
coverage than one round allows is a second round with its own slug, never a raised cap.

**Then order them: most specific first, broadest last** (`MRI reconstruction` → `medical imaging AI` →
`machine learning engineer`) and give leftover rows to the broad query last. Write
`brief.target_titles` in that run order. A declared query that no adapter call ran is
reported as `QUERIES_DECLARED_NOT_RUN`, but only at the end.

## Step 4 — run the search, read the exit code first

Before the first retrieval, follow [Search completion coverage](../references/search-coverage.md):
write `search-coverage.yaml` with the planned sources and directions and run
`python3 scripts/check_search_coverage.py --workspace <ws> --record-plan`.
Use a direction's `query_by_source` when a source needs more specific terms,
such as employer, city and recruitment year for WeChat; keep the ordinary
job-board query as its default. Preregister the actual terms before reading.
For a multi-round consultation, register at the collection owner before any
round reads; register every round path there before using it. Scope can grow,
but cannot shrink after reading begins. Keep the owner and its journal across
rounds. State this scope to the user before searching.

Row/page budgets, elapsed time, target counts (including 18 or 20), and a
`shortfall` explanation never establish search completion. Continue remaining
sources and directions in linked rounds within the existing access rules.
Every observed lead needs a retained, evidence-backed excluded, or genuinely
blocked disposition, including rows omitted from a collection's selected ids.
Record unstructured catalog leads in the browser capture's rows as well.

Use the prepared wrapper with the **owning round's absolute workspace** for each
OpenCLI discovery read. It verifies the registered source plan before network
access, records the actual stdout/stderr inside that round, and classifies the
result before returning. Keep `-f json` and the agreed per-source budgets. Do not
store shared captures in a coordinator folder and later copy them into six
unrelated rounds; use a declared collection or give each read one owning round.

```bash
python3 scripts/run_tool.py --workspace /absolute/path/to/round opencli \
    51job search "算法工程师" --area 上海 --page 1 --limit 5 \
    --window background -f json
```

The wrapper returns nonzero when the read fails. It saves classification in the
journal and prints it on stderr; stdout retains the original adapter output.
Do not run `check_opencli_result.py` again for this already-recorded read. That
script remains the explicit import path for captures made by another supported
runner; pass absolute raw paths and the actual exit code, never a reconstructed
success. Import before the next dependent read.

Public-web searches use `run_tool.py --workspace /absolute/path/to/round
anysearch search "the exact query" --max_results 5`. Register `site: anysearch`
in the source plan first. This route records native HTTP `search_call` evidence;
its snippets are leads only. Read the original posting through its own planned
source and capture before adding a shortlist row. See
[search-coverage.md](../references/search-coverage.md) for lead dispositions.
Do not use an unrecorded `batch_search` in a discovery round.

**Read the exit code before interpreting empty output.** A login wall gives exit 1, EMPTY stdout and a YAML
error body on stderr *even under `-f json`*, so `JSON.parse(stdout || '[]')` silently
converts a 403 into a zero-result success. Only `exit == 0` **and** stdout parsed to
an array is "no results".

The wrapper returns one of five classifications, each with an action:

| classification | what happened | what to do |
|---|---|---|
| `ok` | exit 0, JSON array parsed | continue to Step 5 |
| `not_logged_in` | login wall, and auth says the session is absent or unknown | cross-check auth; ask the user to click Login/登录 on the page kept open in their daily browser. Pause for [user recovery](../references/user-recovery.md); no read retry while logged out. **Do not treat `strategy: public` as evidence that no login is needed**; classify the actual response. |
| `no_auth_adapter` | login wall from an adapter without an auth command | no CLI login command is available. Pause and ask the user to inspect the browser page and complete login if it asks for it; do not invent a login command or infer a missing session from absent adapter metadata. |
| `platform_limit` | a stop-signal from `references/risk-control-signals.yaml`, or a refusal while auth says logged in | **Stop immediately: no retry, parameter changes or bypass.** Pause this source, not the whole task. Explain whether it is verification, rate limiting or an unknown refusal; follow [user recovery](../references/user-recovery.md) before offering degraded output. |
| `transport` | unrecognised failure, or exit 0 with unparsable stdout | Check the actual selected CDP connection and offline routing diagnostic, then follow [bounded network recovery](../references/network-recovery.md). Distinguish a disconnected browser from a site loading or route failure; a timeout alone is not evidence that a VPN caused it. |

## Step 5 — row integrity, before anything else

Assert the identity field is non-empty on every returned row: `title` for every
adapter except `boss`, where it is `name`. The wrapper reports this as
`empty_identity_rows` / `needs_detail_recovery`.

`indeed` is measured to return exit 0, valid JSON, and empty `title`/`salary`/`tags`
while `id`/`company`/`location`/`url` are populated. Recover each row with
`opencli indeed job <id>` and report the gap in `§0`. **Never** infer "this site has
no such jobs" from blank fields — the rows existed.

## Step 6 — normalise, then de-duplicate

Every row becomes one `JobListingEvidence` entry plus this skill's four additions
(`why_matched`, `verdict`, `provisional`, `effort`). This schema is defined here and
nowhere else; `check_shortlist.py` requires all seventeen fields.

```yaml
- id: 51job-173198362              # <site>-<source_id>, stable within the search
  title: 高级算法工程师（视觉调试智能化、AI方向）   # non-empty, or recover it
  company: 比亚迪汽车工业
  location: 西安 · 高新技术产业开发区
  salary: 3-6万                     # verbatim display string from the adapter
  url: https://jobs.51job.com/xian-gxjs/173198362.html   # non-empty direct posting URL returned by the source; tracking params stripped
  source_site: 51job
  source_id: "173198362"           # MUST appear verbatim in raw/51job-*.json
  extraction_method: adapter_search # adapter_search|adapter_detail|user_paste|public_page
  retrieved_at: "2026-08-09T14:02:11Z"
  quality: card_only               # complete|partial|card_only
  verification: collected_unverified # fresh_verified|collected_unverified|stale_possible
  raw_text: "…the card text the evaluator actually saw…"
  why_matched: "…"                 # see the rule below
  verdict: stretch                 # the five levels, nothing else; a card_only row
                                   # never carries strong_apply/worth_applying (Step 8)
  provisional: true                # always true in discover
  effort: evening                  # quick|evening|multi_day|not_closable
```

- `quality`: `card_only` = search row only; `partial` = search row with fields
  recovered by a detail call; `complete` = the detail page was fetched.
- `effort`: how much work the row's *closable* gaps would take, from the card you
  actually have — `quick` (rewording and reordering what is already true),
  `evening` (one focused session: a small demo, a short write-up),
  `multi_day`, `not_closable` (the gap is a hard disqualifier or years of
  experience). It is what makes the within-band ordering in Step 7 a rule rather
  than a sentiment, so it is a closed vocabulary the gate checks (`BAD_ENUM`), not
  free text. Estimate it from the card and say so; do not pretend a card told you
  more than it did.
- `verification`: `fresh_verified` only when a detail call in **this** session
  returned the posting; `collected_unverified` for a card; `stale_possible` when the
  source's own posting date is older than `brief.max_age_days`.
- De-duplicate across platforms on company + normalised title + location; keep the
  row with the higher `quality`.

**`check_shortlist.py` anchors each row to its capture.** `raw_text` is the card text
**copied** — not summarised or translated — and most of it must be found in
`raw/<site>-*.json` (`RAW_TEXT_NOT_IN_RAW`). `id` is exactly `<site>-<source_id>`
(`BAD_ROW_ID`). Your own words go in `why_matched`; normalising `title` is expected, which
is why the title is not the anchored field.

**`why_matched` is one of exactly three places where the no-fabrication fence is
restated, and this is that restatement.** Cite the brief field and the raw field
that made the match — "brief.target_titles 命中「算法工程师」；raw salaryMin 30000
在 brief 区间内". **Never** write a reason that the card does not support, and never
borrow a requirement from a JD you have not fetched. An invented `why_matched` is
the most persuasive part of a fabricated row.

## Step 7 — provisional triage and evidence-backed defaults

First scan cards for hard disqualifiers (work authorisation, licence, mandatory
language, hard location) — a supported hit is `blocked` immediately. Cards can tell
the user which leads are worth reading, but they cannot establish all job requirements.
Therefore a card-only row is **never** a default recommendation: keep it as `stretch`,
`likely_screen_out`, or `blocked` and write `recommendation: review` in
`candidate-match.yaml`.

The shared verdict vocabulary remains:

`strong_apply` · `worth_applying` · `stretch` · `likely_screen_out` · `blocked`

Promote a row to `worth_applying` or `strong_apply` only after its complete detail
was fetched and its requirements were mapped to the frozen CV as described in
`references/candidate-matching.md`. The gate enforces these practical conditions:

- Every stated knockout has strong CV evidence, and every weighted core requirement
  has documented CV support; no core row is `gap` or `no_evidence`. A partial weighted
  item is permitted only when it is genuinely small (`quick` or `evening`) and closable.
- At least half of core requirements have strong evidence not marked `dated`, with at
  least one strongly evidenced core must-have and one strongly evidenced core
  responsibility when the posting states either category. Evidence that is only dated
  is treated as partial.
- Role domain is the same or adjacent and the level is assessed. `strong_apply`
  additionally needs the same domain, no step-up, and strong evidence for every
  core row.
- Missing `nice_to_have` items are allowed. Do not force a candidate to meet every
  preference, and never use a title keyword, skill inventory, or inference as a
  substitute for quoted CV evidence.

This is a conservative investment rule, not an estimate of an interview outcome.
The top of `shortlist.yaml` and `shortlist.md` is ordered by an evidence-backed
default recommendation first, then verdict, then effort (`quick`, `evening`,
`multi_day`, `not_closable`). Within a band, **order by effort** for the next action.

**Every discover verdict carries `provisional: true` and may not be rendered without
the matching disclosure.** That is two obligations, and both are checked:

- in `shortlist.yaml`, the field itself (`MISSING_PROVISIONAL`);
- in `shortlist.md`, the stamp on the row section (`MD_MISSING_PROVISIONAL_STAMP`).
  For an all-card round it is **「基于卡片信息的初判」** — English:
  **"provisional, from card data only"**;
- when any row has a complete detail, use **「已获取职位信息后的初判，尚非完整投递评估」** —
  English: **"provisional; not a full application assessment"** — instead. Japanese,
  Korean and Spanish use the exact matching stamps in
  `references/report-localization.md`.

A YAML boolean is not a disclosure. **规则：discover 的档位永不被带进 assess——assess 一律重算。**

A card that cannot support any level is **dropped from the shortlist** and named in `shortfall_reason`;
it never becomes an `insufficient_evidence` row (`BAD_VERDICT`).

## Step 8 — detail fetch and CV mapping, bounded

For initial triage, fetch detail pages **only** for rows in the top three verdict bands
(`strong_apply`, `worth_applying`, `stretch`), and no more than
`brief.max_match_reviews` rows may enter CV matching. Select the most promising card
leads first; a `stretch` card is a valid detail candidate precisely because its
requirements are still unknown. `likely_screen_out` and `blocked` rows stay card-level
and are labelled **未取详情** (English round: **no detail fetched**) in an initial `shortlist.md`.
Before complete-report delivery, either exclude such a row or read its description
if it is still useful to retain. A final-report completeness read, like a user-named
fetch, is recorded in
`shortlist.yaml.detail_fetch_exceptions` with a reason, but it does not bypass source limits or the
matching-review cap. Unmapped reads use `detail_unmapped` as described above.

Each detail call goes through the same `run_tool.py --workspace <ws> opencli …`
wrapper, which records and classifies it (do not run `check_opencli_result.py` again
for it); its stdout lands in `raw/<site>-<n>.json` like any other read. For every fetched detail selected for mapping,
write one `candidate-match.yaml` row with exact quoted job evidence, JSON-pointer CV
evidence into `candidate-profile.yaml`, requirement type, screening role, match,
recency, effort and role alignment. Do not create requirement rows from card text.
Run the renderer before authoring the reader-facing summary:

```bash
python3 scripts/check_candidate_match.py --workspace <ws> --render --lang <zh|en|ja|ko|es>
```

Copy each rendered line beside that posting's direct link in `shortlist.md`; do not
paraphrase the count. A fetch that reveals a blocker or a material gap normally demotes
the row. Record a below-band final row in `detail_fetch_exceptions` with the reason
that the in-band fetch revealed it.

## Step 9 — write the outputs

`shortlist.yaml`:

```yaml
search_slug: 2026-08-09-suanfa-shanghai
brief: brief.yaml
shortfall_reason: null          # required (a written sentence) when rows < target_count
detail_fetch_exceptions: []     # [{id: …, reason: 用户点名要求补取}]
sources:                        # one entry per site used
  - site: 51job
    command: search
    access: read
    login_state: no_auth_adapter
    classification: ok          # MUST match what journal.jsonl recorded
    invocations: 1
    rows_returned: 25
    identity_field: title
    identity_field_empty_rows: 0
    detail_command: "opencli 51job detail <jobId> --url <captured-url>"
    raw_files: ["raw/51job-0d4e9a7c2b1f4e3a8c6d5b2a1f0e9d8c.json"]
rows: [...]
```

`candidate-match.yaml` is the separate recommendation-evidence file. It names every
shortlist row: a card entry is a `review`, while a default recommendation requires a
complete detail entry and its evidence map. Keep requirement wording and both evidence
quotes verbatim; the schema is deliberately compact so it can be audited:

```yaml
profile_snapshot: candidate-profile.yaml
rows:
  - id: 51job-173199597
    basis: detail                    # detail | detail_unmapped | card
    recommendation: recommend        # recommend | review
    requirements:
      - id: M1
        text: "熟悉 Python/C++"       # verbatim requirement text
        kind: must_have               # must_have | responsibility
        screening: weighted           # knockout | weighted | nice_to_have
        match: strong                 # strong | partial | gap | no_evidence
        recency: current              # current | recent | dated | undated
        effort: quick                 # quick | evening | multi_day | not_closable
        job_evidence:
          - file: raw/51job-7b3c1e9f0a2d4c5e8f6a1b0c9d2e3f4a.json
            quote: "熟悉 Python/C++"
        cv_evidence:
          - path: /skills/Technical/0
            quote: Python
    alignment:
      level_direction: lateral        # step_up | lateral | step_down | unclear
      domain_fit: same_domain         # same_domain | adjacent | cross_over | unclear
      job_evidence: [{file: raw/51job-7b3c1e9f0a2d4c5e8f6a1b0c9d2e3f4a.json, quote: "算法工程师"}]
      cv_evidence: [{path: /experience/0/title, quote: "算法工程师"}]
  - id: 51job-173198362
    basis: card
    recommendation: review
    requirements: []
```

For `no_evidence`, use `cv_evidence: []`; every other match requires an exact pointer
and quote. The quotation in `job_evidence` must come from a successful, journaled
detail capture for that exact row. `candidate-match.yaml` never changes the source
row's original `raw_text` or direct URL.

`identity_field` and `detail_command` for every adapter come from
`references/discovery-sources.md`. There is no other source for
them, which is why `SOURCE_REPORT_MISSING` is that file's backstop.

`raw_files` entries are **workspace-relative and keep the `raw/` prefix** —
`raw/51job-0d4e9a7c2b1f4e3a8c6d5b2a1f0e9d8c.json`, never the bare basename
(`SOURCE_REPORT_RAW_PATH`). One spelling, so a name that resolves is a name that was captured.

`shortlist.md` carries `## §0 来源与读取质量`, `## §0.1 触发原因`, and — when the run
is degraded — `## §0.2 披露`. Its row section uses the matching conditional stamp:
`## §1 候选（全部为基于卡片信息的初判 · provisional）` for all-card output, or
`## §1 候选（已获取职位信息后的初判，尚非完整投递评估 · provisional）` when a detail
was read. Each row shows its band, effort, the exact localized CV-match summary from
the renderer, and a Markdown link using that row's direct `url` (e.g.
`[打开职位](https://...)`). A category, search, company, or source page is not a
replacement for the posting link. Rows below the top three are labelled **未取详情**.

An English round writes the same document with the same numbering: `## §0 Sources
and read quality`, `## §0.1 Trigger`, `## §0.2 Disclosure`, a row section headed
e.g. `## §1 Candidates (all provisional, from card data only)` for all-card output
or `## §1 Candidates (provisional; not a full application assessment)` when a detail
was read, and rows below the top three labelled **no detail fetched**. The `§n`
markers are the same in both — they are what the gate keys on, so they are never
translated away.

## Degraded output — when no real postings could be retrieved

First offer the recovery hand-off above. While waiting, preserve partial results
and say the search is paused; do not present this fallback as the completed task.
Use it when the user declines recovery, cannot regain access, or asks to proceed
with the remaining sources. A user saying “done, continue” after the hand-off
requests a new linked round; follow the recovery reference rather than retrying
inside this stopped round.

Emit a **direction-level shortlist** (3-5 directions), each with: 目标方向 ·
检索词 · 建议筛选条件 · 为何比原 JD 更稳 · 要避开的标题与信号 · 手动收集优先序 —
in English: direction · search terms · suggested filters · why it is steadier than
the original JD · titles and signals to avoid · manual-collection priority.
It contains no posting entries. Keep `rows: []` in `shortlist.yaml` and
`candidate-match.yaml` so both schemas remain valid; write the directions only
in `shortlist.md`. An empty list never claims that a posting exists.

Then the disclosure block, verbatim, in `shortlist.md` — one language, all six
lines, in whichever language the rest of the document is in (Japanese, Korean and
Spanish templates: `references/report-localization.md`):

```text
本次会话已登录：        <是|否|不适用—无 auth adapter>
Adapter 返回：          <逐字错误信息>
收到限制信号后重试：    否
绕过任何平台控制：      否
取得真实岗位：          否
降级输出类型：          方向级 shortlist
```

```text
Logged in this session:         <yes|no|n/a — no auth adapter>
Adapter returned:               <verbatim error message>
Retried after a stop signal:    no
Bypassed any platform control:  no
Obtained real postings:         no
Degraded output type:           direction-level shortlist
```

The last four answers ship pre-filled 否 / no; change one only if a retry or bypass
actually happened. `check_shortlist.py` fires `DEGRADED_WITHOUT_DISCLOSURE` when no
supported-language block is present and `DISCLOSURE_INCOMPLETE` when a line or
answer is missing. **"没有匹配" needs a receipt:** `EMPTY_RESULT_UNSUPPORTED` fires
unless at least one adapter exited 0. If every adapter failed, say that.

## Step 10 — gates, and cite the receipts

```bash
python3 scripts/check_no_write.py       --workspace <ws>
python3 scripts/check_candidate_match.py --workspace <ws>
python3 scripts/lint_no_prediction.py   --workspace <ws>
python3 scripts/check_shortlist.py      --workspace <ws>
```

All four must exit 0. **This mode may not claim success without a passing receipt for
each in `journal.jsonl`** — a skipped script produces no output, and that looks
exactly like a clean one.

Those four gates validate a round. Before a **complete consultation delivery**,
also run `python3 scripts/check_search_coverage.py --workspace <ws>` at the report
owner and require its passing receipt. `deliver.py` independently rechecks the
current coverage file, all declared rounds, raw captures and unresolved leads
before copying files. A prior pass or changing modes cannot bypass that check.
A real source access failure requires captured evidence and a visible limitation
in the report; it does not complete other sources. Only the user's explicit
request permits `report_scope: preliminary` with `preliminary_request` recorded.

**Repair rules — know these before a gate fires.** The receipts in `journal.jsonl`
and the captures in `raw/` are the record: never edit either to reconcile a finding,
and when the source report disagrees with the receipts, the receipts are right. A row
the gate cannot trace to a capture was not retrieved; delete it rather than
"fixing" its provenance. Copy company, salary, URL and capture file names from what
the adapter returned, or leave the field empty; never assemble or invent them.
**Deleting a row means deleting it from both files.** `shortlist.yaml` and `shortlist.md`
(`MD_ROW_NOT_IN_SHORTLIST` reports the half you forgot).

**When a gate reports a finding, read `references/discover/finding-codes.md`** for
what the code means and its exact repair.

## Hand the artifacts over

After the artifacts, you may mention once that an optional weekly email of new
matching roles exists, with what it needs (`references/weekly-digest.md`, "Before
offering it"). Set it up only on the user's yes.

Follow SKILL.md "Client deliverables" (write `report.md` after reading
`references/report-writing.md`, render and review it, run `lint_no_prediction.py`,
then `python3 scripts/deliver.py --workspace <ws>` last (client files go to `~/Downloads/<workspace-name>/`)).
**Discover reports also read `references/discover/multi-posting-report.md`** before
drafting: the job directory, city/ID grouping, company grouping and job identities
across sections. An existing CV is source material and is not redelivered unless the
user asks (`--include-applications`). For several rounds of one
consultation pass the same `--to <consultation-folder>`; a later round lands in its own
subfolder there instead of overwriting the first. If `deliver.py` refuses
incomplete evidence, keep the draft and say what is missing; never copy files into
the delivery by hand. A preliminary report needs `brief.preliminary_request`. Do not
start a mock interview or another mode automatically.

## Self-check before reporting the round

- [ ] `scripts/enter_mode.py --mode discover` run **first**, and this file read in full.
- [ ] `search-preferences.yaml` read via `paths.search_prefs(<name>)`; written on
      first run from answers the user gave, never from inference; confirmed once
      this session.
- [ ] `brief.yaml` written **before** the first adapter call, with `trigger_reason`
      and all three round caps; `candidate-profile.yaml` frozen before any detail fetch.
- [ ] `raw/opencli-help/<site>.yaml` saved for every site called.
- [ ] `raw/auth-status.json` saved; `unknown` re-probed with `--full`.
- [ ] Every adapter call recorded and classified (by `run_tool.py --workspace`, or by `scripts/check_opencli_result.py` for another runner's capture).
- [ ] Queries generated in both languages of the market.
- [ ] For domestic discovery, the WeChat source plan has been reconciled with
      actual query/article captures and unresolved gaps under
      `references/supplementary-sources.md`; snippets alone are not coverage.
- [ ] Identity field asserted non-empty on every row; `indeed` rows recovered.
- [ ] Every row's `raw_text` is the card text **copied** from the capture, and its
      `id` is `<site>-<source_id>`.
- [ ] The `indeed` adapter not used for a non-US market (country sites go through the browser route), and if it was
      used, every returned `location` read against `brief.markets` before the row
      was kept.
- [ ] Every row carries `provisional: true` **and** `shortlist.md` carries the
      card-only or detail-reviewed native stamp from
      [report-localization.md](../references/report-localization.md); no verdict copied
      into an assessment.
- [ ] `shortlist.md` is in **one** language — the user's — end to end: section
      names, the stamp, the 未取详情 / no detail fetched labels and the disclosure
      block, with no furniture left in the other one.
- [ ] Every rendered candidate has a clickable direct posting link copied from
      its `url` field. A search/category/source page is not a job link.
- [ ] Every row carries an `effort` value; evidence-backed defaults are first, then
      verdict and effort within the remaining order.
- [ ] Cards that could not support any level were dropped and named in
      `shortfall_reason` — not listed as `insufficient_evidence` rows.
- [ ] Detail reads outside `strong_apply` / `worth_applying` / `stretch` have a
      documented user-named or final-report completeness exception, and no more
      than `max_match_reviews` entries have CV mappings.
- [ ] Every high verdict has a complete `candidate-match.yaml` entry, raw-detail
      quotes, frozen-profile pointers, and its exact localized summary beside the link.
- [ ] `references/source-policy.md` re-read if any action felt like it might be
      yellow or red; `references/risk-control-signals.yaml` consulted on any failure.
- [ ] `references/discovery-sources.md` read before calling a discovery adapter.
- [ ] `scripts/check_no_write.py`, `scripts/check_candidate_match.py`,
      `scripts/lint_no_prediction.py`, and `scripts/check_shortlist.py` all exited 0,
      and the completion message cites their `journal.jsonl` receipts.
- [ ] Every final retained posting has a full description or a captured access-failure
      exception with its reason visible; `deliver.py` checked all collection rounds.
      Preliminary delivery is based on an explicit user request, not a reached cap.
- [ ] No chaining into `apply`. The shortlist is handed back for a person to choose.

**Voice.** Follow `references/report-writing.md` for the client report: make each role's source visible, explain what was not searched, and end with concrete actions. Keep raw evidence IDs and tool diagnostics in the internal shortlist records.

## When a platform says stop, stop

A platform limit is any refusal the platform put up: a risk-control or captcha body,
a rate limit, or a refusal on a site `opencli auth status` says you are logged into.
Follow [user recovery](../references/user-recovery.md); "done, continue" starts one
new bounded round linked to the old workspace, never an erased journal. For the
stopped round:

1. **Stop that site for that round.**
2. Do not retry.
3. Do not change parameters and retry — a smaller `--limit`, a different city or a
   fresh `--window` is still a retry.
4. Do not route around it — no other adapter, no public mirror, no logged-in
   session standing in for a logged-out one.
5. Continue independent sources; use the direction-level degraded output only if
   the user chooses it or recovery is unavailable.
6. Fill in the disclosure table (six lines, pre-filled "no") above, in the document's one language.

Trigger strings are data in `references/risk-control-signals.yaml`. Always `-f json`,
always `--window background`, and **always branch on the exit code before you read stdout**.
Never run a command whose published `access:` is `write`.

Begin every discovery round with OpenCLI's offline CDP routing check (`scripts/doctor.py`).
If the one-way browser fallback is unavailable too, disclose the gap; do not switch back to
OpenCLI for the same round.
**READ `references/source-policy.md` before the first live retrieval of any run** and
`references/discovery-sources.md` before calling a discovery adapter.
<!-- END discover-inserts (plan 3) -->
