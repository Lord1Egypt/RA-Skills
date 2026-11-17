---
name: literature-review-paper-screener
version: 1.5.0
description: >-
  Literature Review Paper Screener V1.5.0. The local agent (internet-enabled, free) searches for literature,
  collects evidence, builds per-paper Evidence Records with Evidence Availability Levels A-D, submits ONE
  paper per workbook row to the private LoomLoom Cloud template (rows run as independent parallel tasks, so
  screening never exceeds the platform per-activity timeout), then audits and merges the returned screening
  results and renders Excel Paper Sheet + Reading List. Cloud has no internet access; you gather the evidence
  and it evaluates it. Use it for Literature Review tasks in the Medical Science focus only;
  do not use it as a general citation manager, for other task types, or for disciplines it is
  not configured for.
  The bundled files are local helpers only — a pre-flight checker, a result validator, and an
  Excel renderer. All searching, downloading, and cloud submission is performed by the agent
  through the loomloom CLI, which this skill requires.
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - loomloom
    homepage: https://github.com/ez-hq/literature-review-paper-screener/releases
permissions:
  # Declared tool scope (least privilege): research + local helpers + user-confirmed cloud.
  network: public literature search / metadata services (PubMed, Crossref) — local research only
  web: WebSearch, WebFetch (literature search, retrieval, metadata lookup)
  files: bundled scripts + run output directory only (validator, renderer, Excel output)
  shell: python3 (bundled helper scripts), loomloom CLI (cloud run, only after explicit user confirmation)
  allowed-tools: [WebSearch, WebFetch, python3, loomloom]
---

# Literature Review Paper Screener — Local Agent Skill (V1.4.6)

The **Local Agent** is the internet research layer of the Literature Review Paper Screener. You have
internet access and do **all** research and evidence gathering. The **Cloud** (a private LoomLoom
template) has no internet access; it screens and organizes only the evidence you send it.

> **Core principle:** Local Agent gathers the evidence. Cloud evaluates and organizes the evidence.
> (Full product rules live in the project documentation set; this Skill is the executable guide.)

## What one task means and how it executes (V1.1)

One task = **one full literature review** for one student topic, delivered as:

- **Paper Sheet** — the complete screened pool, one row per retained paper (evidence level, screening verdicts, priority, reading role, evidence-bound notes/summary)
- **Reading List** — the same pool organized by Priority and Primary Reading Role

**Execution model (per-paper rows):** the Cloud template's screening step has a platform-fixed
per-activity timeout. Screening all N papers inside **one** activity times out for larger sets
(observed: 20 papers → `StartToClose timeout` failure, twice). V1.1 therefore submits **one paper
per workbook row**: N papers = N rows = N independent parallel cloud tasks, each screening a single
paper in seconds. The results are **merged locally** back into one Paper Sheet + Reading List.

- Never put more than one paper's evidence into a single workbook row.
- Total cloud tasks = total papers = total per-task fee units (Market: USD 0.10/task).
- Merging is local-only: no cloud aggregation step, no re-derivation.

## Prerequisites

- Python 3.9+ (validator/render scripts)
- `loomloom` Skill + CLI installed — install with `npm install -g @cogfoundry/loomloom`
  (or let the agent install it), then verify with `loomloom doctor --output json` (`healthy=true`)
- A LoomLoom account on the platform you run on (CogFoundry or Shengsuanyun) with balance for cloud runs
- The workflow begins with a **mandatory cloud onboarding** — see "0. Cloud onboarding" below

## Bundled files and what each one does

This package ships documentation and three local helper scripts. None of them opens a network
connection, calls the cloud, or screens anything:

| Path | What it is | Network |
|---|---|---|
| `README.md`, `NOTICE`, `LICENSE` | Package provenance and licensing | none |
| `references/architecture.md` | Search and evidence-collection rules | none |
| `references/evidence-package-schema.md` | The per-paper Evidence Record shape handed to the cloud | none |
| `references/metadata-validation-gate.md` | The bibliographic-identity check run before handoff | none |
| `agents/openai.yaml` | Descriptor metadata for platforms that read one | none |
| `scripts/check_evidence.py` | Local pre-flight: validates one Evidence Record's JSON and fields before pasting | none |
| `scripts/validate_results.py` | Local audit of returned results: merges the per-paper rows, checks the product contract | none |
| `scripts/render_excel.py` | Local renderer: writes the Excel Paper Sheet and Reading List | none |

Searching, evidence collection, the metadata gate, workbook filling, and cloud submission are
performed by **the agent** using its own tools plus the `loomloom` CLI declared in this skill's
frontmatter. They are not implemented in the bundled scripts.

**Files these scripts read and write.** Read: the cloud result export passed to `--input`
(`result-rows.json`) and, for the pre-flight checker, one Evidence Record JSON. Written: the audit
outputs `review/local-audit.json` and `review/validation-report.json`, plus the deliverables
`PaperSheet.xlsx` and `ReadingList.xlsx` under `--out-dir`. Nothing else is read or written, no
network request is made, and any other path is out of scope for this skill.

## Before you start: pick language & payment channel

1. **Cloud output language — confirm it with the user.** The package only sets the default: this is the English package, so the default is **English**; the `-zh` package is the Simplified-Chinese counterpart. Ask the user which language they want for the delivered comments and summaries before the run. If the assignment requires another language, keep this package and write those fields in the required language (see the language rule in step 5); if the user wants a Chinese default throughout, point them at the `-zh` package.
2. **Which Cloud to pay** (run cost is charged where you execute):
   - Domestic / RMB: Shengsuanyun, CNY 0.7 / task
   - Overseas / USD: CogFoundry, USD 0.10 / task
3. **Input is required.** The cloud has NO internet; it evaluates ONLY the evidence text you paste. No input, no output.
4. Full local packages (scripts/references/agents; `-zh` and `-en`) live on GitHub: https://github.com/ez-hq/literature-review-paper-screener/releases

## Workflow

### 0. Cloud onboarding (MANDATORY — before anything else)

**This Skill requires LoomLoom Cloud to screen papers — there is no fully-local mode.**
Before starting any work, you MUST tell the user this, and confirm they are willing to
proceed on the paid cloud path. Do not skip this even if they seem ready.

Tell the user (in their own language), ALL of this:

1. **Cloud is required.** This Skill's local part only searches and gathers evidence; the
   actual screening runs on LoomLoom Cloud, which is a **paid** service.
2. **LoomLoom must be installed locally — the user installs it themselves (prerequisite).**
   It is NOT installed automatically with this Skill, and the agent does NOT run global
   installations. Tell the user to install it in their own terminal:
   ```bash
   npm install -g @cogfoundry/loomloom
   ```
   For production, prefer pinning a reviewed release version. Do not proceed until the user
   confirms installation is complete.
3. **Verify the install works:**
   ```bash
   loomloom doctor --output json
   ```
4. **The user needs a LoomLoom account on the platform they will run on** (CogFoundry or
   Shengsuanyun — see step 1.5). They should follow that platform's own account/sign-up flow.
5. **The user logs in interactively with `loomloom login`** — the agent never sees or handles
   their credentials.
6. **Cloud runs are paid** (CogFoundry USD 0.10 / task; Shengsuanyun CNY 0.70 / task).
   Billing and balance follow the platform's own payment flow. Confirm the estimated cost
   with the user before running.

> If the user does not want to install LoomLoom, has no account, or does not accept the paid
> cloud path, stop and explain that this Skill cannot complete screening without Cloud. Do not
> silently substitute another method.

### 1. Install/verify LoomLoom

```bash
loomloom doctor --output json
```

If `healthy=false`, complete authentication first (browser login preferred: `loomloom login`;
follow the platform's own sign-in flow if a token is needed). Do not proceed to cloud steps
without a healthy Doctor.

### 1.5 Ask the user which Cloud platform to run on

The SkillBot is published on **two platforms**. You **must ask the user before any cloud run**
which platform to use — never decide on their behalf. Payment method is the decision guide:

| Platform | Profile | Evidence input mode | Market fee | When to pick |
|---|---|---|---|---|
| CogFoundry | `cogfoundry` | Paste the single-paper record JSON into the cell (v2 platform: upload port removed) | USD 0.10 / task | Credit-card / international payment (USD) — **English output** |
| ShengSuanYun | `shengsuanyun` | Paste the single-paper record JSON into the cell (no upload port on v2) | CNY 0.70 / task | China payment (WeChat/Alipay/RMB) — **Chinese-language listing; outputs in Simplified Chinese** |

Ask in plain language, e.g.: *"Which platform should I run on? CogFoundry (USD — credit card,
English output) or ShengSuanYun (CNY — Chinese output)?"*

Then switch the active profile and verify health before proceeding:

```bash
loomloom server list
loomloom server use <cogfoundry|shengsuanyun>
loomloom doctor --output json
```

The screening logic is identical; only the evidence-entry mechanics and fee differ. The platform
choice is confirmed **again at submission time** (step 8) together with the cost — if the user
changes platform after evidence entry, redo the platform-specific evidence-entry step (6) for the
new platform.

### 2. Understand your template binding

This Skill runs through the **Market Listing** on each platform (buyer path — the listing,
not a private template, is what the user pays through). Current listing bindings
(do not invent IDs; verify with `loomloom market workbook download <listing-id>`):

| Platform | Listing ID | Market fee |
|---|---|---|
| CogFoundry | `01a0423e-fdcd-7428-b388-4711b67b0e03` | USD 0.10 / task |
| ShengSuanYun | `01a0465b-5d0e-7279-bcea-f206544521b0` | CNY 0.70 / task |

If the binding changes, ask the owner; never guess IDs.

### 3. Gather user input (conversational)

Ask, one question at a time, in plain language (all optional except the topic):

1. **Research Question / Topic** — required
2. Required Citation Count — optional (guidance only)
3. Assignment Requirements (brief, rubric, word count, population, etc.) — optional
4. Research Restrictions (population, country/region, time period, source type, years) — optional
5. Deadline — optional (reading recommendation only)
6. Available Reading Time — optional

Never block on missing optional inputs; skipped fields use default rules. If the topic is too
unclear, ask **one** clarification question, then proceed with what you have.

### 4. Search the literature (you, local, internet-enabled)

Per the search workflow rules (see references/architecture.md):

- Build a search profile from available input; never invent restrictions the user did not provide.
- Decompose the question into core concepts, research focus, population, context.
- Build a keyword map (synonyms, alternative terminology, academic terms).
- Generate multiple search queries (direct, relationship, terminology expansion, population/context).
- Run them; maximize recall; do NOT screen for quality during search.
- Run a coverage check (all core concepts, synonyms, population, context, direct evidence,
  alternative perspectives, foundational + recent research). Expand only when new searches still
  add new literature; stop when new searches produce mainly duplicates/covered/low-relevance.
- Combine everything into a **Master Candidate Pool**, then **deduplicate** (DOI, accession, title)
  into the **Unique Candidate Pool**.

### 5. Collect evidence and build one Evidence Record per paper

For every unique candidate, collect as much as is reasonably available:

- Bibliographic metadata (title, authors, year, journal/publisher, source type, DOI, ISBN, stable URL, database record)
- Abstract
- Available content: full text where possible; otherwise sections (intro/methods/results/discussion/conclusion) or structured info (methods info, key findings, results info, conclusion info, database record detail)
- Stable links (paper link, DOI link, database record, publisher page)

Then assign **one Evidence Availability Level** per paper:

| Level | Record contains |
|---|---|
| A | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| B | Abstract + substantial structured information (methods info, key findings, results, conclusions, detailed database record) |
| C | Title + metadata + Abstract |
| D | Title, authors, year, journal/publisher only |

Record per paper: Available Evidence, Missing Evidence, Assessment Limitations. Do **not** fabricate
evidence; do **not** require full text for every paper; failed retrieval only lowers the level.

**Output = one standalone JSON/text file per paper** (the per-paper Evidence Record, see
references/evidence-package-schema.md for the exact shape), named like `handoff_p001.json`…
`handoff_pNNN.json`. **One file must contain exactly one paper's record** — this is what keeps a
single cloud task small enough to finish inside the platform activity timeout. Do not bundle all
papers into one file.

**Language rule: the Evidence Record defaults to English.**

- **Default.** English is the default for every field the local agent writes:
  `available_content`, `available_evidence`, `missing_evidence`, `assessment_limitations`,
  `abstract_or_available_content`, `metadata_gate_notes`, and any notes. The default comes from
  the cloud template bound to this package, which is configured for English output, so English
  input keeps the cloud summary/notes, Paper Sheet, and Reading List consistent end-to-end.
- **Override.** Assignment requirements take precedence over the default. If the user's assignment
  requires the delivered comments and summaries in another language, write those fields in that
  language and say so in the handoff notes. If the user simply asks for a different output
  language, honour the request and record which language was used.
- Literature content (abstract, full-text excerpts, structured info) is never translated: keep the
  paper's original language as-is (keep an English paper's English).
- Want a different package default? The `-zh` package is the Simplified-Chinese counterpart of
  this one, and installing it makes Chinese the package default.

### 5.5 Metadata Validation Gate (mandatory, before handoff)

Before any per-paper record may be written into its `handoff_p<record_id>.json`, run the
**Metadata Validation Gate** (see references/metadata-validation-gate.md) against authoritative
sources (PubMed / Crossref). This gate validates **bibliographic identity only** — it never
touches search logic, screening logic, CRAAP, Topic Relevance, Reading Role, Priority, the Cloud
DAG, or workbook batching.

- Every unique candidate receives exactly one outcome:
  `VERIFIED` | `PARTIALLY VERIFIED` | `MISMATCH` | `INVALID`.
- **VERIFIED / PARTIALLY VERIFIED** → record may proceed; write
  `"metadata_status": "VERIFIED"|"PARTIALLY VERIFIED"` into the handoff record and mark any
  unverifiable identifier explicitly (`"doi": "NOT VERIFIED"`).
- **MISMATCH / INVALID** → the record is **blocked** before `handoff_p<record_id>.json`, cloud
  upload, screening, and final delivery. Return it to evidence collection (step 5) for
  re-verification; never guess, infer, or repair identity with semantic similarity. If
  re-verification cannot resolve identity, surface the conflicting values to the owner and let
  the owner decide keep/drop.
- **No DOI/PMID and no authoritative confirmation** (not indexed by PubMed/Crossref): keep the
  record as `PARTIALLY VERIFIED` with identifiers marked `NOT VERIFIED` — never silently drop
  valid literature; flag it in the gate ledger and delivery summary for owner awareness.
- Keep a short per-run gate ledger (record_id → status → what was checked) for the delivery
  summary.
- Core principle: **a correct summary does not prove that the citation metadata is correct.**
  Evidence content and bibliographic identity are validated separately.

Optional pre-flight: run `python3 scripts/check_evidence.py <evidence.json>` before pasting to catch JSON/field errors locally (no cloud, no cost).

### 5.6 What leaves your machine — cloud handoff, privacy, and data minimization

Steps 1–5.5 (search, evidence collection, the metadata gate, the pre-flight check) run on this
machine as local artifacts. **Two kinds of outbound request exist and both must be disclosed:**
(a) `WebSearch`/`WebFetch` and metadata lookups (PubMed / Crossref) send the **research queries and
identifiers** you derive from the topic to external services **during research, before step 6** —
minimize what you put into queries (avoid names, student numbers, or other personal detail), and
tell the user which external services the research will contact; and (b) the **cloud handoff at step
6**, which sends the Evidence Records to the selected LoomLoom platform. Declining (b) does **not**
undo requests already made in (a) — say so plainly. Before you paste or upload anything for (b):

1. **Disclose before you send.** Tell the user, in plain language, which platform will receive the
   data, that it is a third-party cloud service, and what the run will cost. A confirmation about
   *platform and fee* alone is not consent to transfer data — ask for the data transfer explicitly.
2. **Minimize what you send.** Send only what screening needs: the per-paper Evidence Record fields
   defined in `references/evidence-package-schema.md`. Strip anything else from the payload —
   student names, student numbers, email addresses, phone numbers, home addresses, ID numbers,
   grades, and any other personal or identifying detail. If the research question or the assignment
   brief itself contains such detail, replace it with a neutral placeholder before it reaches the
   cloud and tell the user you did so.
3. **Local alternative (cloud handoff only).** The Evidence Records, the metadata gate ledger, and
   the pre-flight check are local artifacts, and skipping the step-6 handoff avoids **cloud** transfer
   only — it does **not** mean "no third-party disclosure at all", because the research queries in (a)
   already contacted external search/metadata services. If the user does not consent to the cloud
   handoff, stop here and deliver the local artifacts (per-paper Evidence Records plus the gate
   ledger), stating plainly that no cloud screening was run and therefore no Paper Sheet or Reading
   List was produced. Never send the data anyway, and never substitute a local guess for a screening
   result.
4. **No credentials in the payload.** Never include API tokens, keys, or account identifiers in any
   handoff payload.

### 6. Prepare the cloud workbook (one row per paper) — Market buyer path

Run through the **Listing** (not a private template). Download the listing's input workbook:

```bash
# CogFoundry (international, USD):
loomloom market workbook download 01a0423e-fdcd-7428-b388-4711b67b0e03 --output-file lit_input.xlsx -s https://loomloom.cogfoundry.ai/loom/v1
# ShengSuanYun (China mainland, CNY):
loomloom market workbook download 01a0465b-5d0e-7279-bcea-f206544521b0 --output-file lit_input.xlsx -s https://loomloom.shengsuanyun.com/loom/v1
```

Fill **one row per paper** (N papers → N rows):

- `Research Question / Topic` — the same required topic text on every row
- `Assignment Requirements`, `Research Restrictions` — optional; same values on every row when provided
- `Required Citation Count`, `Deadline`, `Available Reading Time` — optional (collected for context only)
- `Screening Model` — select from the approved list once; leave default if fine
- `Literature Evidence Package (paste)` — paste the single-paper record as **compact single-line
  JSON** directly into the cell (see references/evidence-package-schema.md). Keep it under ~25,000
  chars per cell (Excel cell limit is 32,767). One record = one paper; every row carries a
  **different** single-paper record. Reusing one multi-paper bundle on every row is forbidden
  (it reintroduces the timeout).

Do not modify the workbook's meta sheet (the `__template_id` / `__template_version` keys are
managed by the platform).

### 7. Validate and precheck (read-only)

```bash
loomloom market workbook validate <listing-id> --file lit_input.xlsx -s <selected-server>
loomloom market workbook quote    <listing-id> --file lit_input.xlsx -s <selected-server>
```

Show the owner, before any submission:

- task count = **paper count N** (rows in the workbook)
- per-task fee (Market: USD 0.10 / CNY 0.70) and **total fee = 0.10 × N (USD) or 0.70 × N (CNY)**
  from the quote, plus estimated model/API cost and balance/sufficiency
- the selected platform's listing id and server

Do **not** submit yet.

### 8. Confirmed run (platform + fee + count lock)

Before anything else, **re-confirm the platform with the owner** (even if chosen in step 1.5):

- **ShengSuanYun** — CNY ¥0.70/task, China payment (WeChat/Alipay/RMB)
- **CogFoundry** — USD $0.10/task, credit-card payment

Then present the full numbers and get an explicit confirmation, phrased as: **"Platform: <X>.
N papers → N cloud tasks → total fee ≈ <0.70 CNY × N | 0.10 USD × N> + model cost. Confirm?"**
The row count is the paper-count lock: the number of tasks (and fee units) is fixed before
submission and cannot change mid-run. Also verify the active profile matches the confirmed
platform (`loomloom doctor`). If the owner changes platform at this point, go back to step 6
(evidence entry) for the new platform. Then:

```bash
# CogFoundry:
loomloom market workbook run 01a0423e-fdcd-7428-b388-4711b67b0e03 --file lit_input.xlsx --confirm --client-request-id <new-uuid> -s https://loomloom.cogfoundry.ai/loom/v1
# ShengSuanYun:
loomloom market workbook run 01a0465b-5d0e-7279-bcea-f206544521b0 --file lit_input.xlsx --confirm --client-request-id <new-uuid> -s https://loomloom.shengsuanyun.com/loom/v1
```

Preserve the returned `run_id`. Watch and retrieve **all** task results:

```bash
loomloom run watch <run-id>
loomloom run result-rows <run-id> --output result-rows.json
loomloom run result-workbook <run-id> --output-file results.xlsx
```

Every run needs its own confirmation and its own client-request-id. If input changes after
confirmation, re-validate, re-precheck, show a new estimate, and obtain a new confirmation.

### 9. Local audit (mandatory — merged)

Run the validator on the returned results (it merges all per-paper task outputs into one global
screened pool automatically):

```bash
python3 scripts/validate_results.py --input result-rows.json --manifest ../store-manifest.json --out-dir ../review
```

It must PASS before you render or claim success. The validator checks: parseable structured
output for every task row, evidence availability levels, content-credibility decision rule,
excluded papers never in the Paper Sheet, same pool across Paper Sheet and Reading List, one
Primary Reading Role per paper, no duplicate record IDs across batches, citations present,
explicit failures/partial results, and reproducible rerun conditions. If it reports issues, do not
fabricate fixes — record them and report to the owner.

### 10. Render and deliver (merged)

Run the Excel renderer over the audited result set (it merges every task row's output into one
Paper Sheet + one Reading List):

```bash
python3 scripts/render_excel.py --input result-rows.json --out-dir <deliverables>
```

Deliver: Paper Sheet (complete screened pool, one row per retained paper) + Reading List (same
pool by Priority and Reading Role) as Excel files, plus a short plain-language summary: how many
papers searched, screened, included, excluded (with reasons), the evidence-level breakdown
(A/B/C/D), and how many cloud tasks ran. Point out evidence-limited papers (Levels C/D) and
preliminary classifications.

**Before delivery, verify the outputs are in the agreed language** (English by default, or the
assignment-required language when one was specified) — scan the rendered data and the handoff for
text in a different language; if any is found, return to step 5 (evidence collection), rewrite the
offending fields, and re-run the affected stages:

```bash
# quick check: prints any records containing CJK characters in the rendered output
python3 -c "
import sys, json, re
for f in sys.argv[1:]:
    d = json.load(open(f, encoding='utf-8'))
    hits = [k for k, v in (d.items() if isinstance(d, dict) else []) if isinstance(v, str) and re.search(r'[\u4e00-\u9fff]', v)]
    print(f, 'CJK fields:', hits if hits else 'none')
" result-rows.json handoff_p*.json
```

## Operating rules

- **Human-in-the-loop (global, mandatory — covers every high-impact action).** This Skill never
  auto-executes actions that spend money, send data to a third party, or irreversibly change
  files. Every cloud submission, every data handoff, and every file overwrite requires an
  explicit confirmation from the user in the current conversation, after the relevant numbers
  (platform, fee, paper count) have been shown. Silence, a previous approval, or an earlier
  choice is NOT a confirmation.
- **Ask the user which platform before every cloud run — including test and verification runs.**
  Never default to the currently active profile without asking (step 1.5), and never skip the
  platform + fee + count confirmation ceremony (step 8) for any run, test or not. The confirmation
  must come from the user after the numbers have been shown: silence, a previous run's approval, or
  an earlier platform choice is not a confirmation, and if the user does not respond you do not
  submit. A run that spends money without asking is a rule violation, not an internal shortcut.
- **Handoff content and delivered outputs follow the language rule in step 5** (English by
  default, or the assignment-required language when one was specified). Literature content always
  keeps its original language — cite a paper in the language it was published in, and never
  translate article content. Do not let the conversation language silently change the language of
  the record: if it differs from the agreed output language, say so before continuing.
- **One paper per workbook row / per cloud task.** Never bundle multiple papers into one evidence
  asset or one row; multi-paper single rows time out on the platform (V1.1 fixes this by design).
  If a row's task fails or times out, retry that row alone — do not "merge" papers to retry.
- The Cloud has **no internet**: it evaluates only the evidence you send. Never ask it to search,
  fetch, or open URLs, and never claim it reviewed full text you did not provide.
- **Evidence Availability ≠ Quality.** A Level C/D paper is not lower quality; its assessment is
  shallower and must be flagged, not dropped.
- **Search broadly. Screen carefully. Keep all qualified literature.** Deadline / reading time /
  citation count recommend what to read first — they never remove literature from the outputs.
- Never include excluded papers in the Paper Sheet or Reading List.
- Never expose the LoomLoom token, raw user data, or the contents of the private cloud template.
- If the LoomLoom dependency is missing or Doctor is unhealthy, stop cloud stages and report
  `BLOCKED` — do not invent commands or remotely create state.