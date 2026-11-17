# OpenCLI-first read-only browser fallback

First inspect OpenCLI's version, read-adapter help and offline website CDP routing
with `python3 scripts/doctor.py`. Do not run OpenCLI's extension-oriented health
probe or instantiate Browser Bridge. The selection order is fixed:

1. Use **OpenCLI** when the required read adapter actually uses CDP and the
   selected browser/profile connection is verified.
2. Use **built-in CDP** only when that probe diagnoses `cli_missing`,
   `bridge_disconnected` (the selected CDP connection failed), or
   `unsupported_extraction` (including a website factory that selects Browser Bridge).
3. If built-in CDP is unavailable after the diagnosis, disclose the gap;
   do not switch back to OpenCLI for the same round. The built-in reader is a one-way
   fallback, not a second route for re-reading the site.

Never use browser extensions, including ones already installed or connected.
A successful extension health check or an endpoint variable alone is not proof
that a website command uses CDP. Preserve the actual offline probe output and
version; do not execute a disallowed backend to manufacture a fallback reason.

Use job-hunt's bundled `scripts/browser_cdp.mjs` with the selected daily browser.
It needs Node 22+ and no separate browser skill. Do not assume a localhost port, restart the user's browser or
change its settings. A browser tool policy denial remains a denial.

## Check a local CDP boundary before falling back

A sandbox can reject a local CDP connection. Retain the actual error and, when
available and authorized, verify the same selected connection through the
platform's approved host-local or unsandboxed path. Ask only for a permission the
platform actually requires; existing authorization is sufficient.

- If that route works, repeat the single bounded read using the same CDP path.
- If it still fails, `bridge_disconnected` permits the one-way browser CDP fallback.
- `EADDRINUSE` does not authorize killing a shared process, changing its port,
  reinstalling tools or restarting the user's browser. Extension daemon status
  is not evidence for this CDP check.

This applies only before a site refusal. A captcha, login wall, 401/403/429 or
platform limit stops the site across every execution path and backend.

Only these reasons are accepted by the recorder:

- `cli_missing`: executable unavailable.
- `bridge_disconnected`: diagnostic confirms the selected CDP connection is unavailable.
- `unsupported_extraction`: no suitable documented read extraction, including an
  adapter that cannot serve the requested market or a diagnosed adapter
  incompatibility while the requested browser search demonstrably works.
  Preserve the help/diagnostic evidence under `raw/` and explain the reason in
  shortlist §0. Known optional repairs are in [opencli-compat.md](opencli-compat.md);
  patching is not required before using a supported browser fallback.

A generic timeout, blank fields or unclassified transport error does not establish
one of these reasons. Diagnose first using [network recovery](network-recovery.md);
existing detail recovery still applies. A site refusal (captcha, login wall,
401/403/429, platform limit) is different from a backend capability failure: it
stops this site for this round across both allowed retrieval backends. Use the
same stable `site` name for both backends, e.g. `51job`.

The stop is keyed on three things, so a rename does not quietly reset it: the
declared name, the host actually read, and the hosts that name was already seen
using in this journal. `51job`, `51job.com` and `www.51job` are one site; so is a
differently-named read whose URL resolves to a host the refused site had already
used, which is how `boss` and `zhipin.com` are joined without anyone maintaining
a table of adapters to domains. **A rename that shares no text with the refused
name and no host the run has actually seen cannot be joined to it** — the check
says so rather than pretending otherwise, and the stable name is what keeps that
edge from mattering. Pause and follow [user recovery](user-recovery.md): explain
what happened, ask the user to resolve login/verification themselves, and wait.
Their explicit confirmation that they completed the action and want to continue
is the request for a new bounded round; they need not restate the search brief.
The new round keeps the same source/backend and preserves the old evidence.
Never switch backends after a refusal. If no approved browser capability exists,
request a pasted JD/export and disclose that live discovery was unavailable.

## Capture, then import

Use the selected read-only browser tool to open/read the page. Navigation and the user's requested job
search are allowed; login submission, applications, recruiter messages and any
other account mutation are not. Record every retrieved search/detail page,
including empty results and refusal pages, immediately and before another read of the same site. Independent sites may
be in flight; one coordinator imports captures serially.
Save the actual tool output; do not ask a model to recreate a snapshot from memory.
Use the bundled reader's `SNAPSHOT_EXPRESSION` for rendered text. Do not use
`body.innerText` alone: an unrendered body can fall back to script/style source
and falsely report a captcha. Hidden and non-content nodes are excluded; a
textless page is a transport failure, not a successful empty search. Actual
visible verification text and HTTP 401/403/429 still stop the source and require
[user recovery](user-recovery.md).

For the bundled reader, capture directly to a new workspace file:

```sh
node scripts/browser_cdp.mjs --browser chrome --url '<original-page-url>' \
  --output '<ws>/raw/<site>-browser-1.json'
```

The helper creates its own background tab, captures the rendered DOM,
and records a main-document HTTP status when CDP reports it. It never selects an
existing tab. Completed task tabs are closed; login or verification pages are
kept open and brought forward for the user, including after session shutdown.
Read/classify and import this file before the next read of the same
site. Navigation failures return an error, not an empty success. The reader
supports known HTTP(S) URLs and explicit read-only navigation to an observed
job title, detail control or pagination label. It never submits forms or clicks
application, contact or account controls (投递/申请, BOSS's 立即沟通 which messages
the recruiter, 关注/收藏, Follow/Connect, Solliciteer/Bewerben/Postuler, login).
The helper refuses these labels in code as a backstop; never pass one. A rendered catalog without hrefs is not evidence
that no job details exist. Inspect the observed label, then navigate within the
same task-owned tab:

```sh
python3 scripts/run_tool.py --browser chrome browser \
  --workspace '<ws>' --site '<site>' --budget-plan '<ws>/catalog-budget.json' \
  --url '<catalog-url>' \
  --click-text '<exact visible job title>' --wait-for-text '任职资格' \
  --output '<ws>/raw/<site>-detail.json'
```

For a filter that requires opening a menu before choosing an option, use
`--steps-file <plan.json>` with an array such as
`[{"text":"Location"},{"text":"Mainland China","selector":"label[for=location-mainland-china]"}]`.
Use only controls observed on the source page. A plan allows at most eight
read-only clicks within the same owned tab; each step preserves before/after
snapshots under `navigation_steps` and stops on a refusal before proceeding.
Do not combine it with `--click-text`. A visible `Apply filters` / `Apply all filters` button may be selected with
an observed selector only when it is outside a form. Form and
account/application controls remain forbidden. Single-click navigation uses the
same accounting requirement as a multi-step plan.

Every successful browser `search`, including a direct initial search page with
no clicks, needs this complete DOM catalog accounting. A hand-selected rows file
is not the page count. Unaccounted captures remain preserved but cannot pass;
stop that source rather than treating missing accounting as a network retry.

Before navigation, supply `--workspace`, `--site` and `--budget-plan`. The JSON
plan contains one `stages` entry for the initial page and each click destination:
`{"stages":[{"row_selector":".observed-job-card","page":1,"max_rows":10},
{"row_selector":".observed-job-card","page":1,"max_rows":0}]}`.
The second entry in this example is a detail page with no catalog cards. These
are examples only: inspect the actual DOM before choosing a selector. Match all
visible catalog cards, never a selected subset. `max_rows` reserves the expected
maximum; it is not an instruction to truncate the DOM. Use zero only for a stage
that exposes no catalog, and retain the page evidence establishing that.

For an already observed home/detail page without any catalog, use
`"row_selector": null, "max_rows": 0`. When the first catalog's DOM structure
is unknown, a final inspection stage may instead use `row_selector: null` and
reserve the brief's full row allowance (`max_rows: 25` by default), but only
with zero prior consumption and zero-row preceding
stages. Pair it with `--inspect-text` for an observed role label. The capture
includes up to three ancestor containers to establish the actual card selector.
It stops there with `catalog_accounting_pending: true` and an unknown row count;
it is never a completed or empty search. Import the diagnostic, inspect its
actual rows and selector, then preserve it and make a new bounded verification
round using the observed selector. The pending diagnostic cannot pass gates or
authorize another read in its original round. Do not use this inspection path
to repeat an over-budget read or to recover after a source refusal.

The wrapper derives consumed rows/pages from the round's journal, using its
prepared Python runtime. The reader rejects plans above the remaining allowance
before creating a tab. It saves every stage's full DOM and all matching cards,
counts a previous result/source checkpoint once, and stops further clicks if a
page unexpectedly exceeds its reservation. Repeated catalog visits consume the
allowance again; distinct page numbers determine the page cap. This accounting
is deliberately conservative for catalog context used on a detail journey: it
does not infer that repeated cards can be ignored. Prefer an already observed
detail URL when available. Narrow the route before a read that cannot fit;
never split or relabel evidence after reading it to erase a violation.

Import the snapshot before another same-source read. A pending capture, invalid
prior accounting, unexpected overflow or incomplete journey blocks continuation.
If a later click fails, the reader keeps the earlier stages with
`navigation_error`; import this evidence, diagnose it, and do not call it a
completed search. Intermediate cards also enter source-coverage checks, even
when the final page is empty or a login wall. Historical navigation captures
without stage accounting remain preserved but cannot pass current gates.

If the label is ambiguous or not the actual clickable control, first capture
`--inspect-text '<observed label>'`. The snapshot includes that node's parent
HTML; use an observed `--click-selector` plus the exact control's `--click-text`
(e.g. a specific card's “详情”), never a guessed selector. Missing or duplicate
matches fail instead of clicking an arbitrary element. A click is attempted
once; the final snapshot retains its source URL/text/links under `navigation`,
the original label and timestamp, and the resulting page. The final expected
text must be the detail's actual heading; a timeout or unchanged catalog is not
a complete JD. Import/classify before further same-site work. Reopening a known
catalog solely to follow an already observed title is navigation, not a new
search query; its visible cards still need the conservative accounting above.

Links which normally open a new window are directed into the capture's own tab;
no unrelated browser tab is selected. Refusal checks apply before interaction
and while waiting for the destination. If the site needs interaction beyond
this supported navigation, retain the concrete limitation and continue other
sources. Do not install another browser skill to fill it.

Rendering waits use three increasing budgets: 15, 30 and 60 seconds in the same
tab. For a job page whose shell loads first, add `--wait-for-text "About the job"`
(or its observed local-language heading). A timeout retains the actual DOM for
diagnosis; `load_timed_out: true` with no extracted rows is recorded as transport,
not zero matches. Login and human-verification pages stop the wait and require
the user hand-off below, including a verification screen that keeps spinning.

If DOM diagnosis shows that the intended description node is present but still
contains a lazy-loading skeleton, use its **observed selector**, together with
the expected text, to reveal that node:

```sh
python3 scripts/run_tool.py --browser chrome browser \
  --url '<original-page-url>' \
  --wait-for-text 'About the job' --reveal-selector '<observed-description-selector>' \
  --output '<ws>/raw/<site>-browser-revealed.json'
```

After the first 15-second wait and the refusal check, this option activates only
the capture's own tab, lets it settle for 1.5 seconds, and scrolls the specified
node into view once. The remaining
30- and 60-second waits still require the requested text; scrolling alone does
not establish a complete JD. A missing or invalid selector returns an error and
closes the task tab instead of scrolling elsewhere. The snapshot's `reveal`
field records whether the action occurred. No application button is clicked and
no website private API is called. Without this option, captures stay in the
background. Do not guess selectors or enable it routinely: retain the observed
lazy-loading evidence and obey the same capture/import and refusal-stop rules.

Save the JSON string's contents as `raw/<site>-browser-<n>.json`, without rewriting
its text or URLs. If a tool reports a refusal outside the DOM (HTTP 403, for
example), retain that output and set `http_status: 403` or `blocked: true` on the
snapshot; never record it as an empty successful page. Bare navbar links labelled
Login do not establish a login wall. Explicit wall language does.

If a tool returns richer link objects, preserve its original output and make a
separate deterministic projection to the snapshot shape above: retain `text`
unchanged and extract only original HTTP(S) link URLs. Do not pass link objects
or `javascript:` links to the importer, and never reconstruct text from memory.
Workers must return that shape to the coordinator and wait for import/classification
before their next read of the same site. A late bulk import does not establish
that this ordering was followed; retain the deviation and rerun a bounded sample.

Separately extract a JSON array into `raw/<site>-browser-<n>-rows.json`:

```json
[{"source_id":"job-1234","url":"https://careers.example.org/jobs/job-1234",
  "title":"Python Engineer","raw_text":"Python Engineer\nExample Ltd\nLondon"}]
```

Each card's `raw_text` is a contiguous verbatim piece of snapshot text; title must
occur in that piece, and URL/identifier must exist in the snapshot. For missing
IDs, use the original job URL as `source_id`. Company-only links are not job URLs.
Missing fields stay empty; a card is not a complete JD. Refusal and genuine empty
pages have `[]` rows, distinguished by the snapshot's status/text.

```bash
python3 scripts/record_browser_capture.py --workspace <ws> --site 51job \
  --snapshot-file <ws>/raw/51job-browser-1.json \
  --rows-file <ws>/raw/51job-browser-1-rows.json \
  --backend builtin-cdp --fallback-reason unsupported_extraction --command search \
  --query 'Python' --page 1
```

This importer performs no network operation. Exit 0 means **recorded**, even for
`classification: platform_limit`; inspect that result and stop the site. Exit 2
means invalid input; repair the evidence/reporting error before any further read.
Select the actual `--backend`: `builtin-cdp` (default). Older backend identifiers remain readable only for
historical capture verification. Use the actual diagnosed fallback reason; the example assumes
`unsupported_extraction`. The recorder retains `preferred_browser` for older
captures, but it is not a capability diagnosis for a new OpenCLI-first round.
It appends `browser_call` with that backend, `operation: snapshot`, query,
page, row count, classification, source URL/time and both file hashes. It does not
fabricate an `adapter_call`, shell command or OpenCLI access metadata.

In `shortlist.yaml`, browser rows use `extraction_method: browser_page`, copied
`source_id`, `url`, `title`, `raw_text`, `retrieved_at`, and the usual quality and
verification fields. `sources` uses the same site, `command: search` (or `detail`),
actual classification, counts and both `raw_files`. If a site used multiple
commands, omit `sources.command` to aggregate them; do not hide failed calls.
All existing page, query, count, detail and disclosure rules apply. The row
budget counts search rows returned across both backends per site, before
shortlisting or de-duplication; discarding a row does not undo the read. Browser
`--page` is the page actually visited, not a counter reset on every query.

Run `check_no_write.py` and `check_shortlist.py` normally. They read both types of
retrieval, reject altered/missing captures, unknown browser operations, invented
browser rows, missing queries, excess pages and reads after a refusal. Mark any
browser detail fetch `quality: complete` only when the full JD was obtained;
partial detail fetches also need `detail_fetch_exceptions` if their final verdict
is outside the top three. Follow the detail cap before fetching, not after.

These checks establish consistency of recorded evidence. They cannot prove a
snapshot's browser origin or detect operations absent from the journal. Keep the
actual tool trace and never claim that a hash proves an unlogged action was safe.

HTTP 404/5xx captures with no extracted rows are recorded as `transport` with
their status and original evidence. They are never successful empty searches;
malformed captures and rows attributed to failed HTTP pages are rejected.


### Capture ownership during discovery

Register the original site's source before its first read, including a detail
page reached from AnySearch. For a direct detail capture, use
`run_tool.py --workspace /absolute/round browser --site employer --url URL
--output /absolute/round/raw/employer-detail.json`. Keep the existing DOM,
read-budget and fallback rules. Extract and import the actual rows into that
same round immediately. Do not assign a shared capture to another candidate by
copying its JSON or backdating a plan; a collection must declare its rounds
before they read. A pending snapshot prevents the next wrapped retrieval until
its real capture is imported.
