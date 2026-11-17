# Sources for career consultations

Choose sources that answer the current career question. Start with the employer's
careers page and current JD for vacancy status, requirements and pay. Add a source
when it can change the application decision or help the user prepare. The table
below is a selection guide, not a checklist to run in full.

## Fixed tool routes

Source selection and tool routing are separate decisions. The user has assigned
these routes; do not reconsider the provider when one of these sources is used:

| Source | Required initial route |
|---|---|
| WeChat public accounts (Sogou WeChat) | OpenCLI |
| Xiaohongshu | OpenCLI |
| Douyin | OpenCLI |
| Toutiao | OpenCLI |
| Public web, news, employer websites, specialist verticals and specified domains | AnySearch HTTP API for search |
| GitHub repositories, code, issues and PRs | `gh search` |

For the four named platforms, diagnose only whether the installed OpenCLI read
adapter can execute through CDP; do not treat the tool choice as optional or send
the search to AnySearch instead. If CDP is unsupported or the selected connection
fails, retain the actual reason and follow the one-way daily-browser CDP fallback
in [browser-fallback.md](browser-fallback.md). Never use an extension.
Use the customer's daily browser unless they explicitly request a separate one.
Xiaohongshu and Douyin retain per-consultation authorization and site read limits.
These routes do not require running every platform in every consultation.

## Useful sources

| Need | Source and route | What to verify |
|---|---|---|
| Current openings and requirements | Employer careers pages and recruitment platforms; diagnose OpenCLI first, use its verified CDP read adapter, or fall back to daily-browser CDP for the diagnosed reason | Original posting, location, requirements, pay and posting date. |
| Employer or industry background | AnySearch public search through its HTTP API, then the original website or news article | Publisher, date and the claim supported; a snippet is not a full-page read. |
| Recruitment announcements, referral leads and industry analysis | WeChat public accounts; anonymous Sogou WeChat search through OpenCLI after verifying its CDP adapter, or diagnosed daily-browser CDP fallback | Account name, article date and original article. Follow recruitment links to confirm the job; reposts and old announcements do not establish a current opening. |
| A candidate's public work or an employer's technical projects | GitHub public repositories, code, issues or PRs through `gh search` | Read the relevant original material; distinguish project activity from the candidate's personal contribution. |

For China-related hiring, use WeChat when recruitment announcements or industry
context are relevant;
consider it explicitly during source selection rather than silently omitting it.
A generic web search is not a substitute for an actual WeChat search. If Sogou or
an article cannot be accessed, record that result and the scope actually read.

### WeChat coverage for domestic job discovery

Include WeChat in the source plan for a domestic job search, especially campus
and state-owned enterprise recruitment. A user-limited source list takes
precedence; a CV-only edit or an assessment of a supplied JD does not require
unrelated searches. Use the fixed route above and the existing access boundaries.

Derive targeted queries from the actual brief: target employers or employer
type, graduation year/recruitment season, role family and city. Adapt queries to
the unresolved parts of the search rather than running every combination.
Prioritize employer recruitment accounts, state-owned enterprise accounts and
university career offices; check the publisher before treating it as official.
One employer query does not cover a multi-employer or multi-role request.

Open relevant original articles and retain their account, title, publication
date, original URL and captured text. Check the applicable graduating class,
location, role requirements, application window and route. Follow linked job
descriptions when the article only summarizes them. An employer's official
recruitment article can itself be the original posting when it supplies those
details; capture it through the supported posting-evidence workflow. An old
article or an unspecified deadline does not prove recruitment is still open.

Keep a private coverage table in the existing research notes: search question,
actual query, captured result, article reading scope, linked-posting status and
remaining gap. Separate search snippets, full article reads and verified hiring
conditions. Reconcile the table before calling research complete: resolve
relevant unread leads within the agreed scope and read budget, or record the
actual access failure or exclusion reason. Do not prescribe a fixed article
quota, count a few snippets as coverage, or bypass site stops to fill the table.
Missing coverage remains a research gap; report only limitations that affect the
client's decision and keep tool diagnostics in the private record.

Use AnySearch vertical search for a relevant specialist question, and its
`site:` search for public pages on a specified domain. Discover the supported
vertical domains before using them. Neither route replaces original-job evidence.

Other channels are outside the default search plan. Add one only for a concrete
information gap or an explicit user request, after checking that it serves the
question. Do not expand into unrelated social, video or podcast research to make
a report look comprehensive.

## Availability and execution

Apply [daily-browser.md](daily-browser.md) to independent reads: separate browser
tabs, shared site budgets and serial journal imports. Prepare OpenCLI and AnySearch, and verify the bundled CDP reader using [agent-setup.md](agent-setup.md). AnySearch is an HTTP API
search provider; it does not use the browser CDP route. Browser reads use CDP
only, with OpenCLI diagnosed first and fallback governed by
[browser-fallback.md](browser-fallback.md). Use the daily browser unless the user
explicitly requests a separate one.
Inspect current help before calling a tool. For discover rounds, use `run_tool.py --workspace /absolute/round anysearch search
"query" --max_results 5` so native HTTP evidence is recorded. Use separate
recorded calls for separate queries. Outside discover, AnySearch `batch_search`
can group independent background queries; use its documented schema. If a provider is unavailable,
use an available public source with the same access boundary and record the gap.

Before retrieval, briefly record the selected sources and the question each one
will answer in the workspace. For each source selected, record whether it was
read, unavailable or no longer needed, and why. Do not count a source as searched
just because this reference names it. Do not install unrelated providers or
request additional social accounts to complete setup.

Employer or industry context remains background research. A hiring lead may become a
shortlist candidate only after its original posting has been read through the
supported evidence workflow. Use [browser-fallback.md](browser-fallback.md) for
browser posting captures and keep the recruitment gates and refusal locks.

## Evidence and client report

For every source used, retain the original URL, publisher/account, publication
date when available, read date, claim supported and reading scope (snippet, full
text or metadata). Save actual captured evidence in the workspace. Distinguish
company statements, independent reporting and individual experience. Confirm
important hiring conditions with primary sources.

Use relevant findings in `report.md` and place source links beside the claims or
in a short source list. WeChat findings should name the account and article, with
the reading scope clear. Do not add a link merely to show platform coverage.
For a job-search report with a job directory, that directory is the source list;
do not add another “来源与信息范围” section. Keep supplemental verification detail
in the research notes. Include a supplementary finding beside a job only when
it changes the client's choice or preparation, with a direct link if needed.
Tool diagnostics and the full source-selection audit stay in internal records.
If a missing source limits a career conclusion, explain the fact that remains
unverified. Deliver the verified report PDF with any requested CV in the same
consultation folder.

## Supplementary public research

Use `references/supplementary-sources.md` when official web/news, WeChat
public accounts or relevant GitHub projects can fill a concrete career evidence
gap. It defines source selection, availability checks and evidence quality.
These sources supplement formal posting evidence; select only what the current
question needs.

For China recruitment, WeChat public accounts are a priority research source.
Use the prescribed OpenCLI/Sogou WeChat route for targeted employer, graduation
year and role queries, prioritizing official recruitment, state-owned enterprise
and university career accounts. Read relevant original articles and follow their
application links. One broad query or a few search snippets do not establish
source coverage; record unread articles as leads, not verified opportunities.

For domestic job discovery, read `references/supplementary-sources.md` before
selecting sources and apply its WeChat coverage procedure. A CV-only edit or a
single supplied posting does not automatically start a new search.

When a source requests human verification, immediately tell the user which site
and page needs attention, ask them to complete it in the connected browser, and
wait for an explicit completion reply before resuming that source. Follow
`references/user-recovery.md`; announcing a site stop alone is not a hand-off.
