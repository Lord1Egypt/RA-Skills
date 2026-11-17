# Search completion coverage

The number of matching postings does not establish that a search is finished.
A shortlist gate validates one round. Complete delivery additionally checks the
declared sources, directions and every structured lead actually captured.
This is a check of recorded scope, not a claim to have exhausted the market.

Before retrieval, explain the intended sources and directions and write
`search-coverage.yaml` in the report workspace. Register with:

```bash
python3 scripts/check_search_coverage.py --workspace <ws> --record-plan
```

The script stores a tamper-evident plan in `journal.jsonl`. The first registration
must precede retrieval. Add sources/directions by extending the plan and running
the same command before reading the additions. Do not remove or rewrite existing
entries. Never backdate a plan to make a historical search pass. Start a properly
registered consultation or describe the historical result as incomplete.

```yaml
plan:
  sources:
    - id: employer_a
      site: employer_a
      label: Employer A official careers
      method: search
  directions:
    - id: ib
      label: Investment banking analyst
      query: Investment Banking Analyst
checks:
  - source: employer_a
    direction: ib
    status: pending
leads: []
```

For live discovery, use `scripts/run_tool.py --workspace /absolute/round`
before the `opencli`, `anysearch` or direct `browser` tool name. The wrapper
rejects an unregistered source before opening it and records OpenCLI/AnySearch
results in that same round. Browser snapshots still require verbatim row
extraction and `record_browser_capture.py`; an unimported snapshot blocks the
next wrapped read. Budgeted browser navigation retains its documented
`browser --workspace ... --site ... --budget-plan ...` syntax and applies the
same source-plan preflight. Complete its import before scheduling another read.

AnySearch is `site: anysearch`, `method: search`. The wrapper supports one
quoted query per call, `--max_results` at most 10 and the remaining round row
budget, and owns `--format json`. It preserves the original API envelope, exit
code and stderr in signed `search_call` records. Do not describe these as
browser or OpenCLI captures, and do not put their snippets directly in a
shortlist. A search lead can use `status: retained` and `row_id` only when the
selected original-posting row has the **same exact URL**, under its real source.
Other leads need their normal exclusion or blocked disposition.

`method: search` requires the direction's actual query in the recorded search.
Use separate directions for required translations and synonyms. `method: catalog`
is for a reviewed careers catalog: record the catalog as a search capture,
extract its candidate titles/links into rows, and give a concrete review reason
for each direction. A detail page alone cannot close a source search.

When the same direction needs different search terms on different sources, keep
the ordinary `query` as the default and preregister overrides by **source id**:

```yaml
directions:
  - id: frontend_zh
    label: Chinese frontend roles
    query: 前端工程师
    query_by_source:
      weixin: 上海 React 前端工程师 招聘 2026
```

Here `weixin` must be the id of a registered `method: search` source. Its capture
must match the override exactly; other search sources still match `query`.
Unknown source ids, blank queries and catalog overrides are rejected. Register
these terms before retrieval; an existing direction's query or overrides cannot
be rewritten after registration. Targeted WeChat terms should come from the
brief, not be reduced to generic job-board terms to satisfy a coverage check.

Every source × direction pair requires one check. After reviewing a result:

```yaml
checks:
  - source: employer_a
    direction: ib
    status: done
    reason: Reviewed the returned analyst openings and recorded every candidate.
    evidence:
      workspace: .
      file: raw/employer_a-search.json
      sha256: REPLACE_WITH_ACTUAL_FILE_SHA256
      quote: COPY_AN_ACTUAL_CAPTURE_EXCERPT
```

Evidence must be a raw file named by an actual same-source retrieval record.
The hash and quoted excerpt are checked; browser snapshot records additionally
retain their existing signature, metadata and raw-file validation. These records
are tamper evidence, not independent proof of web origin. Catalog interpretation
and exclusion reasoning still require honest review of the captured content.

The built-in browser keeps `requested_url` alongside the final page `url`.
This binds a redirected article's unavailable-content result to its original
search lead. Preserve both addresses; never edit an old raw capture to add a
missing request address or substitute an unrelated failed page.

`blocked` requires an actual captured login/access refusal or transport failure,
a reason, and that exact reason visible in `report.md`. It can close the affected
source's directions without retrying a stopped site. Other sources still need
their own results. A successful capture, time budget, row limit, target count or
shortfall cannot justify a blocked status. Pending work prevents full delivery.

Leads in structured captures are matched by `site` and `source_id`. A row is a
lead when it has the adapter's title field (`name` for `boss`; `title` otherwise,
even when empty as on `indeed`) and an identity: an explicit id field, else the
posting id in its URL (`currentJobId`/`jk` query values, else the last path
segment without `.html`). A posting selected for delivery is retained
automatically when its `source_id` is any of those spellings. Journal paths may
be workspace-relative or absolute inside the workspace. Otherwise use `leads`:

```yaml
leads:
  - site: employer_a
    source_id: actual-captured-id
    status: excluded
    reason_code: eligibility
    reason: The posting requires a qualification the candidate does not hold.
    evidence:
      workspace: .
      file: raw/employer_a-search.json
      sha256: REPLACE_WITH_ACTUAL_FILE_SHA256
      quote: COPY_THE_REQUIREMENT_FROM_THIS_LEAD
```

Allowed exclusion codes: `wrong_year`, `closed`, `wrong_location`, `wrong_role`,
`wrong_level`, `eligibility`, `duplicate`, `not_a_posting` (an article, news item
or company page returned by the search, e.g. a WeChat industry commentary) and
`not_selected` (a relevant posting left out of the detailed selection). A
`not_selected` lead must stay visible to the client: list its posting link in
`report.md`, for example under other relevant roles not yet read in full. Never
use another code for a relevant posting merely to shorten the report. Quotes must
belong to the specified lead, not another row in the same file. Blocked leads require the same captured
failure and report visibility as blocked checks. When a catalog title identity
resolves to a different detail id, use `status: retained` and `row_id` of a selected
shortlist row with the same site and title. Unprocessed or unknown leads fail.

For collections, create the owner and register **before any round reads**.
Each round also registers its own source plan before its first wrapped read;
the collection registration does not replace that local preflight.
Include `plan.rounds` listing every workspace path from `collection.yaml.rounds`.
Keep previously registered rounds when adding another, and use an evidence
`workspace` pointing to one of those rounds. Selecting `ids` in a collection
does not erase other captured leads. Each retained round still needs its own
shortlist and description checks; a preliminary round cannot downgrade a complete
collection. Run the completion gate at the owner:

```bash
python3 scripts/check_search_coverage.py --workspace /path/to/collection
python3 scripts/deliver.py --workspace /path/to/collection
```

Complete delivery re-runs coverage against current inputs before copying files;
it cannot reuse an old passing receipt. Existing explicitly requested preliminary
delivery remains available through `report_scope: preliminary` and a nonempty
`preliminary_request`. Never use it merely because the search is taking longer.
