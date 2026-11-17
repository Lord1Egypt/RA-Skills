# long-doc-translation

**English companion of `README.md` (Chinese primary; the pair is for reading inside the repository — skill-channel pages do not resolve relative links, so this is deliberately not a clickable switch).**

Turn a several-hundred-page foreign-language monograph into a **deliverable, verifiable, terminologically consistent** Chinese full manuscript.

## In one line

Not "translate a passage" — it is about keeping 100+ translation units consistent in style and wording, so that after merging there are no duplicates, no broken joins, and no untranslated leftovers.

## Pipeline

parse → clean & slice → build style guide + glossary → parallel batched translation → multi-dimensional QA → merge into a reading edition with a table of contents

## Fit

- Scholarly monographs, classics, archives and translated works over 300 pages (German / English / French / Japanese …)
- When you need consistent terminology book-wide, preserved footnotes, and traceable doubtful spots

## Dependencies

- `python3` + `markdown` + `pypinyin` (core scripts run fully offline)
- omni-reader (optional: stage one "parse" converts PDF / images to text)

Connectivity test for the stage-one parsing leg (parsing runs through the omni-reader MCP inside your host; no curl replaces it): the host lists tools through the JSON-RPC `tools/list` handshake, and connected means that reply contains `parse`, `get_parse_status` and `read_result`. If those names are absent the leg is not connected - the offline steps still run (slice -> translate per segment -> merge), but scans and images cannot be read and only the text layer you already hold is usable: what is missing is parsing, not formatting. Parsing spend follows the server reply; this package neither estimates nor pays it.

## Scripts (`scripts/`)

`init_project.py` · `dedup_boundary.py` · `overlap_check.py` · `qa_check.py` · `merge_build.py` · `build_reader.py` · `_common.py` · `check_translation.py`

`check_translation.py` is the package's own self-test face (`--selftest`), zero network and pure stdlib, reading only this package's fixtures and never a user's manuscript. Three tiers: the good sample walks all four tools (segment counts, the seven QA lanes, a dry-run dedup that must not touch disk, and a merged master carrying the whole-book term appendix); the bad sample carries one defect per segment and must be judged red with the file and line named; the counter-example tier breaks the good sample in seven single points - each one must turn its own lane red, plus one positive control (an OCR trace inside a note section must stay green) and the "missing or empty directory" lockout across five scripts. In the first tier "all seven QA lanes green" is judged by **verdict-line structure**: qa_check writes verdicts at two-space indent and detail deeper, and two informational lines at the same indent ("（豁免 …）", "· 正常接缝…") are not verdicts - a lane is green exactly when its block holds **one and only one verdict line, and it starts with the pass mark**. Appending any other verdict line to the block turns it red on the spot, whether it says ❌, ⚠, ⛔, [X] or "FAIL:", and without the symbol having been seen before; a block with only a red line fails too. The exit code cannot cover this (qa_check still exits 0 while reporting red), so the judgment face does. A lane is judged green by verdict-line structure: exactly one verdict line in the block and it must open with the pass marker; the two note lines the checker itself emits are exempt only when the whole line matches their exact shape, and any other two-space-indented line counts as a verdict - so an unfamiliar red symbol cannot slip through, and neither can a conclusion phrased as a note.

Fixture names are not cosmetic: they must follow `part_series_number` (e.g. `01_phil_001.md`). Under any other naming, `overlap_check.py` and `dedup_boundary.py` compare nothing at all and still print a row of green ticks - the silent false pass recorded as hard rule 8.

## Specs (`references/`)

| File | Content |
|---|---|
| `pitfalls.md` | Five pitfalls: detection / fix / prevention, including **silent script failure modes** |
| `qa-checklist.md` | Seven QA criteria + script thresholds + fixes + delivery baseline |
| `reader-build.md` | Engineering decisions and dependency degradation for the enhanced reader HTML |
| `parallel-translation.md` | Chunking rules, three must-haves for sub-agent prompts, acceptance checks |

## Getting started

**Install this skill**: `npx skills add huhoo/cue-awesome --skill long-doc-translation` - this line installs this package only; afterwards re-list installed skills and the name `long-doc-translation` must appear, otherwise the files are not in place. Without a CLI environment the fallback is to copy this whole directory into your host's supported skills location (`~/.workbuddy/skills/`).

```bash
python scripts/init_project.py --help        # two scripts accept --help: init_project.py and check_translation.py
python scripts/check_translation.py --selftest    # re-verify this package: zero network, pure stdlib, prints its own assertion count
python scripts/qa_check.py                  # the others print their usage when run bare (missing args exit 1, not a crash)
python scripts/build_reader.py               # these two carry default paths: a missing directory **errors out with checks to try**
# Measured: a nonexistent directory always exits 1 with guidance — it never prints "0 segments" and a row of green ticks.
```

See [`SKILL.md`](SKILL.md) for the full flow, hard rules and measured parameters; see [`CHANGELOG.md`](CHANGELOG.md) and the `SKILL.md` header for the current version — **this file states no version number** (one written here would be lying forever).

One command prints the constants the three QA scripts actually judge with, including their per-project "change this here" CONFIG blocks, runnable from any directory:

```bash
grep -n "CONFIG\|^[A-Z_]\{2,\} *=" ~/.workbuddy/skills/long-doc-translation/scripts/qa_check.py ~/.workbuddy/skills/long-doc-translation/scripts/overlap_check.py ~/.workbuddy/skills/long-doc-translation/scripts/dedup_boundary.py
```

#### Two starting tiers: simple and complex

- **Simple tier (one text, clean text layer, relaxed terminology)**: `python scripts/init_project.py <project dir>` builds the skeleton, put the source where the RUNBOOK says, then run parse -> clean & slice -> translate -> merge -> the three QA checks. For a few dozen pages done by one person the size-routing table in `SKILL.md` says use **light mode** (`--scale light`); the same table says plainly that a few pages (< 10) should **not** use this pipeline - configuration costs more than it saves.
- **Complex tier (columns, figure captions, scans, terminology unified across the book)**: parse first (an OCR channel such as omni-reader), slice by the book structure (chapter / page range, each segment belonging to exactly one place); then `overlap_check.py` (**before** translating - a superset and its subset each translated once duplicate the passage), `dedup_boundary.py` (clear 1-2 segment overlaps at neighbour boundaries), `qa_check.py` (completeness and style before merge). The only measured book is Dilthey, *Life of Schleiermacher* vol. 2: German, 800+ pages, 141 segments, 32 boundary seams - **wall-clock time was never measured here, so no hours are promised**; estimate by segment and batch count. Columns and figures are handled as text segments; thin text inside images may be missed, and the three QA scripts report untranslated residue, duplicated segments and page-mark gaps (thresholds via the grep line above, live values).

The gates come in two kinds: **fixed in-package gates** (a missing directory errors out rather than printing zero segments, segment-count reconciliation, TOC depth, page-number continuity) and **project-configured domains** (page-mark regex, the OCR typo table, the three note section names, which files/sections are skipped, grouping patterns and the default thresholds). Every number in this file, in `SKILL.md` and in `references/qa-checklist.md` is a mirror and a common example, **not an exhaustive claim** — the scripts as they now stand govern.

## FAQ and anti-patterns (what you try -> this skill declines, because -> where to go)

Reviewed hard rules, the size-routing table and the pitfalls document re-assembled; nothing new promised. Thresholds
and check lists stay in the scripts as they now stand (grep line above).

| What you try | Declined? Why | Where instead |
|---|---|---|
| Run this pipeline over a dozen paragraphs | **Discouraged.** The routing table says: under 10 pages the configuration costs more than it saves | Translate directly; this package exists for "hundreds of pages + terminology unified book-wide + verifiable" |
| A typeset bilingual parallel edition | **Not produced.** Output is a single-language master plus a reading HTML | That row is in the routing table; parallel typesetting is out of scope |
| Slice a scanned image straight in | **No.** No text layer, nothing to verify | Parse/OCR into a text layer first; if a parallel foreign edition exists, use it |
| Ignore overlapping slice boundaries and de-duplicate after translating | **Anti-pattern.** A superset and subset each translated once duplicate whole passages, hardest to see after merging | Run `overlap_check.py` **before** translating; `dedup_boundary.py` for what already happened |
| One global find-and-replace for OCR typos | **Anti-pattern.** Bulk replacement also rewrites our own translator notes | Scope the mapping to source text; the damage shape is pitfall 2 |
| Judge size and duplication by byte count | **Anti-pattern.** Bytes mixed with characters misjudge identical passages | Count characters; see pitfall 4 |
| Merge and ship subagent output unchecked | **No.** Parallel work is fine; unverified work is not | Each batch passes the QA checks before merging (batch discipline in `parallel-translation.md`, pitfall 5) |
| Emit the HTML while the `markdown` dependency is missing | **Cannot.** The .md master still builds; the HTML fails | The scripts name the install command and state the degradation instead of failing silently |

## When something goes wrong (symptom -> cause -> recovery)

**Whatever is absent from this run's tool output is written as "not found"**: a parameter, field or enum value that does not appear there must not be filled from memory - write "not found" and log it on the pending or coverage list; a blank never stands in for it.
Written from the **current actual output** of these scripts: none of them throws a traceback. A bad or missing path
prints `[出错] <cause>` (the bracketed tag is Chinese in the shipped text) followed by lines starting
`→ · <fix suggestion>` and exits 1 - measured behaviour: a missing directory always exits 1 with those hints and never
"prints zero segments then a row of greens"; running without arguments prints that script's usage block.

| Symptom | Cause | Recovery |
|---|---|---|
| `[出错] 目录不存在：<path>` with three `→ ·` hints | Path misspelled, a relative path taken against the shell rather than the project, or the project was never built | Work the hints in order: check spelling and current directory, quote paths containing spaces, and if unset `python scripts/init_project.py <project dir>` |
| Running with no arguments just prints usage | **By design**: a missing argument exits 1 rather than crashing | Read the required arguments in that usage block; re-run with the path and `--expect` |
| The same passage appears twice after merging | Sliding-window slices overlapped; superset and subset were each translated | `overlap_check.py` before translating, `dedup_boundary.py` after, then merge; reconcile seam counts against the measured shape |
| Odd words appear inside translator notes | The global OCR typo map rewrote our own text | Restrict the mapping to source scope, re-run the cleaning step, hand-correct contaminated notes |
| Page marks `[S. XXX]` break or stop being contiguous | Slice boundaries and page seams | Repair at the positions `qa_check.py` names; judge seams and suspects one by one (thresholds are live values) |
| A segment was skipped leaving no trace | Skip ranges (preface, appendix, figure pages) configured against a different real structure | Check the project-configured skip list and grouping pattern - that domain is per project, not a fixed in-package gate |

## How to ask (three positive examples, one counter-example)

**Ask with a point in time; the output states its source edition and translation date**: give the reporting period, reference date or look-back window in the request; the deliverable labels its **source edition and translation date** on the first line, and when that differs from the date you asked about, the text never says "today" or "latest" - it reads "as of <date>".
- **Positive (whole book)**: "Translate this 300-page German monograph into a Chinese master draft, terminology unified
  book-wide, with a verifiable master and a reading HTML" - the main scenario, full pipeline; pass `--expect` with an
  expected segment count so the QA checks reconcile against it.
- **Positive (complex: scan + columns + per-chapter batches)**: "Source is `~/book/dilthey-v2.pdf`, a scan with columns
  and figure captions. Cut batches by chapter, each subagent translates exactly one chapter and may not restructure;
  run overlap detection before merging - at a seam keep the `〔承前页〕` marker rather than swallow text" - that is the
  complex tier: parse -> slice by book structure -> `overlap_check` -> per-chapter translation -> `dedup_boundary` ->
  `qa_check` -> merge. Time is not measured here, so estimate by segment and batch count; degradations are in the tiers above.
- **Positive (80-page archive, one master)**: "Translate these 80 pages of English archive into Chinese, keep the page
  marks, leave quotations in the notes untouched" - the 100-300 page row allows leaner batches; page marks and broken
  sentences are preserved per the hard rules.
- **Counter-example (adjacent need, not this skill)**: "just translate this one-page meeting summary tonight" - the
  routing table says under 10 pages do not use this package; "turn this translation into a typeset parallel edition" -
  out of scope (single-language master plus reading HTML only); "judge whether this passage of source material is
  authentic" - that is verification/research work, a different skill.

