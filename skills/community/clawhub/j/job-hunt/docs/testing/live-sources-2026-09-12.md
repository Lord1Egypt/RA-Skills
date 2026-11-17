# Live source acceptance — 2026-09-12

All seven original job and interview-information sources were exercised in the
user's daily Chrome with OpenCLI 1.8.7 and the project compatibility patches.
The user subsequently removed 1point3acres; the six retained sources have now
returned search results and complete selected detail text through the routes below. This is
bounded source acceptance, not a candidate recommendation or a complete
discover/apply/interview workflow test. No applications or messages were sent.

| Source | Search evidence | Detail evidence | Status |
| --- | --- | --- | --- |
| 51job | OpenCLI returned three Beijing AI product roles | After user-completed slider verification, OpenCLI returned the selected role's full description, company metadata and address | Passed for this sample |
| BOSS | OpenCLI returned three Beijing roles | OpenCLI returned full responsibilities and requirements, salary, employer and address | Passed for this sample |
| Indeed | US OpenCLI search and China/UK/Germany/Netherlands browser searches returned usable rows | One independent full description in each of the five country cases | Passed for these cases; the CLI adapter remains US-only |
| LinkedIn | Adapter returned HTTP 400; browser search rendered results | All three sampled descriptions are now complete: one after waiting, two after revealing the lazy-loaded description | Browser route passed; adapter remains incompatible |
| Upwork | After user recovery, the adapter could not read its expected state structure; the browser returned three selected rows | An independent browser detail returned the full description, requirements and closing paragraph | Browser route passed; adapter remains incompatible |
| 1point3acres | Actual search returned HTTP 403 | Not attempted after the refusal | Removed from product scope at the user's request after the retry also returned 403 |
| Nowcoder | A narrow query returned no rows; a broader product-manager query returned three posts | Selected post text returned successfully | Text read passed; embedded images were not inspected |

Maimai is a recruiter-only people-search adapter, so it was excluded from this
job/interview-content scope. Its presence in the historical adapter catalogue
does not establish job-discovery support.

## Country and completeness checks

Indeed cases were Beijing (`cn.indeed.com`), London (`uk.indeed.com`), Berlin
(`de.indeed.com`), Amsterdam (`nl.indeed.com`) and the earlier same-day New York
area test (`www.indeed.com`). Each non-US search retained three rows and followed
one original regional result URL to an independent detail. Region, employer,
role, duties and requirements were checked. Missing salary was left undisclosed.
The US result is earlier same-day evidence, not a new capture in this round.

The 51job repair was verified against the real page: company type, size and
industry no longer shift columns; the address is present; the 1,018-character
description has 38 line breaks and is unchanged after whitespace normalization.

The first successful LinkedIn sample took about 53 seconds. Two other pages
initially exhausted 15/30/60-second waits with only a header. DOM diagnosis then
showed an empty description skeleton inside a lazy-loaded component, despite
HTTP 200 and logged-in navigation. Activating the task-owned tab, briefly letting
it settle and scrolling the observed description node into view recovered both
bodies. The final bundled reader returned them in **18.925** and **22.320**
seconds. The latter description exactly matches the linked employer's original
after whitespace normalization. Waiting alone and scrolling immediately after
activation had failed in earlier retained captures; these are bounded observed
results, not a claim about every LinkedIn page.

Upwork's browser page rendered usable public job content after user recovery.
That proves content access, not the account's login status. Its search page used
Relevance sorting; recency sorting was not validated.

## Fixes and regression evidence

- The browser reader waits through three increasing rendering budgets in one
  owned tab, can wait for an observed description heading, and preserves the
  final DOM and timeout state. An optional observed-selector reveal activates
  only the task tab and scrolls once after a brief settling wait; default
  captures stay in the background. A timed-out capture with no rows is a transport
  result, never a successful empty search.
- Explicit guest-group denial requests login even when a cached auth flag says
  logged in. Stalled human verification requests user intervention. Site refusal
  still stops all reads from that source until explicit user confirmation.
- The 51job compatibility patch recognizes the observed slider wording and
  repairs company fields, address extraction and paragraph breaks. Only exact
  known earlier patches upgrade automatically; custom edits remain protected.
- `make check eval-lint`: **4,193 passed, 8 skipped**; lossless accounting
  **1,317/1,317**, conventions and eval lint passed. Five dependency deprecation
  warnings remain.
- **17** browser-capture checks cover loading, reveal, refusal, selector handling
  and task-tab cleanup. **29** offline DOM checks execute the actual patched Indeed and 51job
  extraction code. Synthetic guest/verification and slow-rendering regressions
  are code checks, not successful live reads of blocked sources.

Raw page snapshots, original URLs, command timestamps, stopped journals and
linked recovery rounds remain in private local evidence. Historical failures
were retained. 1point3acres is no longer a pending acceptance item: the user removed it from
product scope. Upwork recovery and LinkedIn diagnosis remain separately recorded.
This report does not validate every native adapter, fresh-machine installation,
all countries, all postings, later pages or long-term access stability.
