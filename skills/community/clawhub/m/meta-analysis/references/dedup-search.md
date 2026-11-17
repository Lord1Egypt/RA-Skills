# Dedup Search Workflow（去重检索流程）

> Grounding: PROSPERO (NIHR), Cochrane Library, PubMed/MEDLINE;
> PRISMA-S (Rethlefsen ML et al., 2021) search reporting guidance.
> **Self-contained dedup (default: live, in-skill)**. The two primary layers —
> Cochrane (CDSR) and PubMed/MEDLINE — are probed **live and by default** via the
> in-skill `adapters/literature_probe.py` (Europe PMC REST, no key, no other skill
> required). It returns real hit counts + top titles, so the novelty ranking (R7
> in `topic-selection.md`) is grounded in actual literature — not templates.
> Templates below are only a **fallback** when the network is unavailable, and for
> the two layers with no clean public API (PROSPERO, non-English DBs).

## Purpose

Verify novelty (dimension 4 of topic-selection) and avoid the #1 reviewer
rejection reason: "duplicate / no increment". Run in **Stage 4** of the Full
assessment (and in Dedup re-review path).

## Three-layer dedup（三层去重）

Layer order is deliberate — registered protocols first, then ongoing, then
published. **Layers 1–2 run live in-skill** (default); Layer 3 + non-English are
guided manual steps (no clean public API).

| Layer | Database | How | What to check | Time window |
|---|---|---|---|---|
| 1 | **Cochrane Library** (CDSR) | **In-skill probe** (`literature_probe.py`, `layer="cochrane"`) — live, default | Cochrane Reviews / protocols on the same question | any (Cochrane has priority) |
| 2 | **PubMed / MEDLINE** | **In-skill probe** (`literature_probe.py`, `layer="pubmed"`) — live, default | Published meta-analyses / systematic reviews on the same question | last 5 years (extend if the field is slow-moving) |
| 3 | **PROSPERO** (NIHR register) | Manual / template (no clean public API) | Registered/recently completed systematic reviews on the same question | active + completed ≤24 months |
| — | **Non-English DBs** (CNKI / 万方 / 维普 / SinoMed) | Manual / template (opt-in) | Chinese-herb / regional questions where English DBs under-cover | any |

### Run the in-skill probe（默认路径，真实结果）

```bash
# Two-layer dedup (Cochrane + PubMed SR/MA), last 5 years:
python adapters/literature_probe.py --topic "PD-1 inhibitors NSCLC second line" --layer both --max 8

# Cochrane only:
python adapters/literature_probe.py --topic "<P> <I> <C>" --layer cochrane
```

Output (real, from Europe PMC):
```json
{
  "topic": "PD-1 inhibitors NSCLC second line",
  "layers": {
    "cochrane": {"hit_count": 36, "cochrane_count": 36, "works": [{"title": "...", "journal": "The Cochrane database of systematic reviews", "year": 2026, "pmid": "..."}]},
    "pubmed_meta": {"hit_count": 5358, "works": [{"title": "...", "journal": "...", "year": 2026}]}
  },
  "summary": "Cochrane: 36 review(s) on this topic; PubMed SR/MA (last 5 y): 5358",
  "any_error": false
}
```

Interpretation: `hit_count` is the **live total** for that layer. A high Cochrane
count → the topic is likely saturated (discount novelty); a high PubMed count with
few/zero Cochrane → a gap may still exist but weigh competition. Feed `hit_count`
into the novelty dimension and the R7 ranking. If `any_error` is true (network
down), fall back to the templates below and mark dedup as **"unverified"**.

## 快速检查 vs 全面检索（何时用 ct-literature）

> ⚠️ **本探针只是「快速去重检查」，不是全面文献检索**：它给出真实命中数 + 前几篇标题，
> 用于选题阶段的新颖性判断（R7 排名）。它**不**产出完整题录、**不**做反幻觉验证、
> **不**合并去重、**不**生成 Excel/HTML 报告、**不**做 PRISMA 筛选。

**需要全面检索时，先使用 `ct-literature` 技能**——与本研究探针用**同一 Europe PMC 期刊过滤串**
`(JOURNAL:"The Cochrane database of systematic reviews")`，Cochrane 层计数完全一致，可无缝衔接。
两种典型用法：

```bash
# 1) Cochrane 全面检索（确认“该方向是否已被 Cochrane 系统评价覆盖”）
cd <ct-literature 技能目录> && python scripts/ct_literature.py \
    --topic "PD-1 inhibitors NSCLC second line" --cochrane --with-europepmc --run --out-dir ./cochrane_out

# 2) PubMed SR/MA 全面检索（近 5 年系统评价 / Meta 分析）
cd <ct-literature 技能目录> && python scripts/ct_literature.py \
    --topic "PD-1 inhibitors NSCLC second line" --review-type systematic-review \
    --year-from 2021 --with-europepmc --run --out-dir ./pubmed_out
```

探针的 JSON 输出已自带 `ct_handoff` 块（含上述命令 + 原始 Europe PMC 查询串），可直接复制执行。

## Fallback search-query templates (PROSPERO + non-English; or when probe unavailable)

Use when the in-skill probe cannot run (network down) or for Layer 3 (PROSPERO) /
non-English DBs that have no clean public API. Replace placeholders from the PICO
block (`pico-guide.md`):

```
# PubMed (E-utilities URL, opt-in only)
https://pubmed.ncbi.nlm.nih.gov/?term=(<P>)+AND+(<I>)+AND+(<C>)+AND+(meta-analysis[pt] OR systematic-review[pt])+AND+("2021/01/01"[dp]:"2026/12/31"[dp])

# PROSPERO (browser)
https://www.crd.york.ac.uk/prospero/#searchadvanced
  Query: <P> AND <I> AND <C>, filter = systematic review / meta-analysis, status = all

# Cochrane Library (browser)
https://www.cochranelibrary.com/search
  Query: <P> AND <I> AND <C>, content type = Cochrane Review, trials
```

## Near-duplicate judgment matrix（近似重复判断矩阵）

Not every same-question review is a duplicate. Classify each hit:

| Situation | Verdict | Reason |
|---|---|---|
| Same PICO, same type, similar time window | **Exact duplicate** → block | No increment; reviewer will reject |
| Same PICO, but substantially newer data / larger evidence base | **Near-duplicate, conditional** | Allowed only with documented increment (new trials, updated search, added subgroup) |
| Same population, different intervention (or vice versa) | **Class-substitution** → usually NOT duplicate | Different clinical question; say so explicitly in report |
| Same question, different meta type (pairwise → NMA / IPD) | **Not duplicate if type adds evidence** | Type upgrade can be an increment |
| Same question, only database/time window changed | **Usually duplicate** | Cosmetic change is not an increment |

## Increment assessment（创新增量判断）

For any existing review, assess **increment type** and **sufficiency**:

| Increment type | Sufficient? |
|---|---|
| New RCTs / IPD since last search (≥2 meaningful trials or major trial) | ✅ usually |
| Added outcome / subgroup / NMA / dose-response not in prior review | ✅ if clinically meaningful |
| Updated methods (e.g. 2015 review → PRISMA 2020 + RoB 2) | ⚠️ weak alone |
| Only re-run of same search | ❌ no |

**Increment statement** (mandatory in report): one paragraph saying what exists
and what THIS review adds — reviewers require this verbatim.

## Report fields (into JSON `dedup`)

```json
"dedup": {
  "prospero": "2 registered reviews found (CRD4202xxxxxx): same PICO — exact-dup risk",
  "cochrane": "1 Cochrane review in progress on PD-1 2nd-line NSCLC",
  "pubmed": "4 meta-analyses 2021-2026; 3 use older drug set, 1 includes all PD-1s (2024, 18 trials)",
  "non_english": "not applicable (English-language trial literature)",
  "near_duplicate": "near-dup vs 2024 meta (18 trials); increment = 3 new trials + PD-L1 subgroup not in prior review",
  "increment": "Adds 3 post-2024 trials and PD-L1 TPS subgroup analysis absent from the 2024 review"
}
```

## When dedup re-review is requested（被拒重复后复审）

Run **Stage 4 only**: re-run dedup layers, re-judge near/exact duplicate,
produce increment statement + verdict on whether re-submission is defensible.
Output = short re-review report (not the full 11 sections).
