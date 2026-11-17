# Systematic Review Full-Flow Mode / 系统综述全流程模式

> **This is the `@skill` entry point for an end-to-end systematic review.** When the user
> invokes meta-analysis with a full-flow intent (see §0 triggers), follow this playbook
> instead of jumping straight to the compute track.
>
> **Positioning**: meta-analysis is the *orchestrator* of the Meta-analysis pipeline.
> Upstream stages (topic judgment / retrieval / screening) reuse existing modules + the
> **ct-literature** skill; the only net-new capability is the **data-extraction assistant**
> (LLM draft + human-verification gate). Command chains and seam traps →
> `references/upstream_orchestration.md`.

---

## 0. Trigger & scope / 触发与定位

**Trigger phrases** (already in SKILL.md `triggers`):

- `系统综述全流程` / `系统综述全流程模式` / `系统综述流程` / `系统综述一站式`
- `meta 全流程` / `全流程meta` / `meta 全流程模式`
- `从检索到meta分析` / `从选题到meta分析` / `从选题到合并效应量`
- `文献检索后做meta` / `检索→筛选→提取→合并` / `数据提取 meta`
- English: `systematic review workflow` / `systematic review full pipeline` / `full meta pipeline`

** relationship to §0 two-track gating**: a full-flow trigger is an *explicit* user intent to
run the whole pipeline. It is NOT a new compute task class (no `classify.py` change needed).
Internally it sequences the existing **topic track** (Stage 1) + **compute track** (Stage 5),
with three human-in-the-loop stages in between.

**Hard rule**: every upstream stage ends at a **checkpoint** where the agent MUST pause and let
the human confirm before proceeding. Never auto-advance across a human gate.

---

## 1. Stage 0 — Launch gate (do this FIRST, run no commands yet)

On full-flow trigger, present a short orientation (≤8 lines) + a 5-stage map, then ask only
what is still missing. Do not start Stage 1 until the gate clears.

```
① 方向判断  → topic-selection + literature_probe（如需全面证据则委托 ct-literature）
② 检索整理  → 委托 ct-literature（跨库检索+去重），产出 .merged.json / Excel / HTML
③ 初筛+PRISMA → ct-literature 规则筛 + agent 逐条判定（需你最终拍板纳入数）→ PRISMA 图
④ 数据提取  → extract_assist 草稿 + 你逐行核验 + stamp --confirm（红线：不可无人值守）
⑤ 合并分析  → run_meta.py（守卫自动放行已核验 CSV）→ HTML 报告
```

**Confirm before proceeding** (ask 1–3 at a time):
- PICO 是否明确？有没有预设的纳入/排除标准？
- 检索范围：哪些数据库 / 时间窗 / 语言 / 研究类型（RCT？队列？）？
- 效应量类型（二分类 OR？连续型 MD/SMD？预计算 HR/RR？）？→ 决定 Stage 4 的 `--type`
- 全文来源：是否由你上传 PDF / 提供 DOI（opt-in 取 OA）？付费墙文献能否提供？

**Human gates are non-negotiable at**: Stage 3 (final included count) and Stage 4 (extraction
verification). State this explicitly so the user knows where they must act.

---

## 2. Stage 1 — Topic-direction judgment / 方向判断

Goal: decide whether the topic is feasible & novel enough to run a review.

- Quick (≤30 min): 4-dim score card (clinical / feasibility / data / novelty, 0–5, any ≤2 = veto)
  via `references/topic-selection.md`.
- Full (5 stages + gates): PICO → scoring + R1–R7 cross-checks → dedup probe
  (`adapters/literature_probe.py`, Cochrane CDSR + PubMed/MEDLINE) → PRISMA 2020 / AMSTAR-2
  precheck → 11-section report via
  `python scripts/generate_topic_report.py input.json output.md|html`.
- **Delegated comprehensive retrieval** (when the topic report needs a full evidence base):
  call **ct-literature** for cross-DB retrieval (see Stage 2 command) and fold its
  `lit_report.*` into the novelty evidence of the topic report.

**Checkpoint**: present the topic verdict (`recommend` / `hold` / `not_recommended`).
If `hold` / `not_recommended`, STOP and let the user decide — do not auto-proceed to retrieval.

---

## 3. Stage 2 — Retrieval & dedup / 文献检索整理（委托 ct-literature）

Goal: pull the candidate set, normalized + deduped, ready for screening.

```bash
python <ct-literature>/scripts/ct_literature.py \
    --topic "<PICO-driven query>" --review-type meta-analysis \
    --with-europepmc --with-semantic-scholar --year-from <YYYY> --safety --prisma --run \
    --out-dir ./lit
```

- Outputs: `./lit/.merged.json` (with `prisma` block: `identified` / `excluded` /
  `included_records` / `duplicates_removed`), `lit_report.html`, `lit_report.xlsx`.
- meta-analysis only **orchestrates** here — no in-skill re-implementation of retrieval.
- Boundary: PROSPERO / non-English DBs are "guide-human" steps (`--with-prospero` is a reserved
  interface; silently skipped when no token — never claim it worked).

**Checkpoint**: report `identified` count + top titles; let user sanity-check the query before
screening. (No human gate blocks here, but surface the number.)

---

## 4. Stage 3 — Screening + PRISMA bridge / 初筛与 PRISMA 桥接

Goal: turn the candidate set into a *human-confirmed* final included list + PRISMA diagram.

1. **Machine pre-screen**: `ct-literature screen_prisma.py` (title/abstract rules).
2. **Human judgment — via file hand-off (2026-09-10 decision)**: the agent **does not walk the
   list entry-by-entry in conversation**. Instead it exports the decision table, the human edits
   it, and the table comes back:
   ```bash
   # export: ct-literature template + 规则裁决(预填) + 文献类型确认(规则预填)
   #         + DOI 列（回传匹配键）
   #   block_a.export_screening_xlsx(session_path, out_path)
   # human edits in Excel → upload back
   #   block_a.parse_screening_xlsx(xlsx_path, current_decisions)
   ```
   The uploaded table is the **authoritative included list AND the authoritative document type**.
   Rejection rules (do not advance on failure): missing columns / non-alignable rows / illegal
   `decision` value / `exclude` without `reason` / unexpected new rows / **zero rows matched**.
   The merged node (A2「文献集」, the former A3 folded in on 2026-09-10) has **no in-conversation
   per-record edit path** — editing happens in the spreadsheet.
3. **PRISMA bridge**:
   ```bash
   python scripts/prisma_bridge.py \
       --merged ./lit/.merged.json \
       --set assessed=<N> --set excluded_elig=<N> --set included=<N> --set other_sources=<N> \
       --out prisma_flow_request.json
   ```
   then "generate the PRISMA flow diagram from this request". The bridge prints a per-field
   source table and forces a ` [MANUAL]` declaration on `included` / `assessed` / `excluded_elig`.

> ⚠️ **Seam trap (do not bypass)**: `included_records` (machine pre-screen pass) ≠ `included`
> (human final). Mapping the former onto the PRISMA `included` field silently produces a
> methodologically wrong diagram. The `included` number MUST come from the human screen.

- **Persist the confirmed included list** (so Stage 4 can auto-prefill — no manual re-typing of
  study names). Write it the moment the human confirms the final set:
  ```bash
  # 人工确认最终纳入研究名后，写入纳入清单文件
  # 支持格式：JSON 数组 / {"included":[...]} / {"studies":[...]}；也支持 .txt / .csv 每行一个
  python - <<'PY'
  import json
  included = ["StudyA", "StudyB", "StudyC"]   # ← 人工确认的最终纳入研究名
  json.dump({"included": included}, open("included_studies.json", "w", encoding="utf-8"),
            ensure_ascii=False, indent=2)
  PY
  ```

**Checkpoint (HUMAN GATE #1)**: user confirms the final `included` count **and the included
study list** + the PRISMA diagram before any extraction. Do not advance on `included_records`.

> **Document type is confirmed here (2026-09-10).** The uploaded decision table carries a
> 「文献类型确认」column: rule-prefilled by `ct-literature classify_record()` (single source of
> truth), then confirmed / overridden / left blank by the human. On upload it becomes the
> **authoritative `doc_type`** for that record, with audit fields `doc_type_source`
> (`human`/`rule`), `doc_type_changed`, `doc_type_rule`.
> **After this point, no layer judges type again** — see Stage 4. To change a type, re-upload
> the A2「文献集」merged table; there is no in-pipeline override path.

---

## 5. Stage 4 — Data extraction / 数据提取（抽取助手，红线）

Goal: build the Type 1/2/3 CSV that feeds the compute track — with a human verification gate.

> **A4 downloads by the A2 list, 100% (2026-09-10).** Every record in the confirmed A2「文献集」node's list is
> downloaded; **no pre-download type screening**, no re-classification, no silent skipping.
> `pdf_extractor.extract()`'s former "rule R1" short-circuit is removed and
> `review_summary.excluded` is always `False`.
>
> **Type is read-only here.** A4 reads the human-confirmed `doc_type` from the A2 decision row
> (formerly the A3 decision table; A3 was merged into A2 on 2026-09-10).
> The extractor's own detection is demoted to `doc_type_detected` and **only raises a notice when
> it disagrees** with the confirmed value — it never changes the verdict. `type_notice` /
> `review_note` are advisory text only (e.g. "looks like a review; 0 extracted rows is normal"),
> surfaced at the 🔴 gate for a human to act on.
> To change a type → go back to ③ and re-upload the decision table.

```bash
# 1) scaffold blank extraction table + companion provenance (verified_by_human=NO)
#    自动预填 Stage 3 确认的最终纳入清单（included_studies.json），无需手动重列研究名
python scripts/extract_assist.py scaffold --type <binary|continuous|precomputed|rate|correlation|single_proportion|single_mean> \
    --out extracted.csv --studies-file included_studies.json
#    若未生成清单文件，可退化为手动 --studies "StudyA,StudyB"

# 2) agent/LLM reads OA full text or user-uploaded PDF (convert to md/text first, see §7 of
#    upstream_orchestration.md), fills effect sizes into extracted.csv.
#    Columns by type:
#      binary:       study,n_exp,event_exp,n_ctrl,event_ctrl,year
#      continuous:   study,n_exp,mean_exp,sd_exp,n_ctrl,mean_ctrl,sd_ctrl,year
#      precomputed:  study,effect_type,effect_size,lower95,upper95,year
#    Any value not locatable in the source → fill `NR` (never fabricate).

# 3) validate structure + numeric sanity + missing markers
python scripts/extract_assist.py validate --csv extracted.csv

# 4) HUMAN verifies each row against source page/table → stamp (requires --confirm)
python scripts/extract_assist.py stamp --csv extracted.csv --confirm

# 5) compute (extraction_guard auto-passes the verified CSV)
python scripts/run_meta.py --query "pool <measure> from extracted studies" \
    --data extracted.csv --out-dir <workspace>/meta_analysis
```

`extract_assist.py types` lists all supported schemas (mirrors `references/data_templates.md`).

> ⚠️ **Red line — no unattended feed**: extraction accuracy is clinically critical and full-text
> access is paywalled; systematic reviews require dual independent extraction + arbitration.
> Any CSV produced by `extract_assist.py` stays `verified_by_human=NO` until a human runs
> `stamp --confirm`. `run_meta.py` (via `scripts/extraction_guard.py`) **blocks** unverified
> extraction CSVs with `META_STATUS=unverified_extraction` (exit 3). `--trust-data` is the
> only override (explicit user responsibility, for trusted hand-built CSVs only).

**Checkpoint (HUMAN GATE #2)**: user reviews extracted rows (source page/table citations) and
runs / confirms `stamp --confirm`. Do not run Stage 5 on an unstamped CSV.

---

## 6. Stage 5 — Meta-computation / 合并分析

Goal: run the pooled analysis on the verified extraction CSV.

- Use `python scripts/run_meta.py --query "..." --data extracted.csv --out-dir <workspace>/meta_analysis`.
- `extraction_guard` auto-checks `verified_by_human`; if already stamped, it passes silently.
- Follow §0 speed discipline + §5.1 cross-turn continuity for the compute track.
- Present the single-file HTML report via `present_files` (the HTML report is the sole
  presentation surface; figures appear only inside it).

---

## 7. Wrap-up / 收尾

Deliverables for a completed full-flow run:

| Artifact | Source |
|---|---|
| Topic report (`output.md`/`html`) | Stage 1 |
| `lit_report.*` + `.merged.json` | Stage 2 (ct-literature) |
| PRISMA flow diagram | Stage 3 (`prisma_bridge.py` → `prisma_flow` task) |
| `extracted.csv` + `extracted.csv.provenance.json` | Stage 4 |
| `meta_analysis/` HTML report + `analysis_complete.R` | Stage 5 |

Cross-turn continuity: echo the `## 当前分析设定 / Current analysis settings:` block after
Stage 5 (per §5.1); re-issue `run_meta.py` against the same verified CSV for follow-up analyses
(subgroup / metareg / sensitivity) — do not re-extract.

---

## 8. Failure & boundary handling / 失败与边界

- **ct-literature silently skips a DB** (no token): state it explicitly; never imply full coverage.
- **PDF paywalled**: only fetch OA full text via `adapters/pdf_fetch.py` on explicit user opt-in
  (DOI/PMID provided); otherwise require user-uploaded PDF → convert to md → extract.
- **`validate` reports hard errors** (e.g. `event_exp > n_exp`): bounce back to fill, do not stamp.
- **`run_meta` returns `unverified_extraction`**: means the CSV was not stamped — route back to
  Stage 4 checkpoint, never use `--trust-data` to bypass a real extraction.
- **Coze unreachable** at Stage 5: per §6, ask before auto-diagnosing; never fall back to local R.
