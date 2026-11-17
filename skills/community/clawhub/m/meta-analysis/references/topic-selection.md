# Topic Selection Assessment Framework（选题评估框架）

> Reference design inspired by the public `meta-analysis-topic-selector` skill
> (ClawHub @wenhan9739) and adapted to this skill's local-first, R-engine
> architecture. Registered as a ct-update competitor (2026-08-15).
> Grounding: PRISMA 2020 (Page MJ et al., BMJ 2021;372:n71), AMSTAR-2
> (Shea BJ et al., BMJ 2017;358:j4008), Cochrane Handbook v6.x, GRADE.
> ⚠️ Any claim without a source here → `⚠️ official verify` + ask user.

## Purpose

Turn "I want to do a meta-analysis but have no topic" (or a candidate topic)
into an **auditable, output-driven decision**: should this topic be done, and
in which meta-analysis type — **before** any R analysis runs.

This module is the **upstream gate** of the skill. It does NOT compute pooled
estimates; it decides whether a topic deserves a full analysis, and pre-checks
methodological compliance.

## When to trigger

- "我想做 Meta 分析但没选题" / "I want a meta-analysis but have no topic"
- User offers a direction and asks whether it is feasible
- Reviewer rejected a topic as "duplicate / no increment" — need re-evaluation
- Before PROSPERO registration — methodological pre-audit
- User asks for a structured topic-selection report

**Not applicable**: user is already at data-extraction / pooling stage →
route to the normal analysis pipeline (Core Functions in SKILL.md).

## Topic Gating (选题门控) — ct-literature routing

> **First action on the topic track (before any probe).** The topic track must
> NOT silently run the in-skill probe. It must first run the deterministic gate
> `python scripts/topic_gate.py --topic "<topic>"` and route on its decision.
> The gate is **zero-LLM, zero-network**: it only checks whether ct-literature
> is installed and assembles the right command. The install-vs-simple *question*
> is asked by the agent (AskUserQuestion), not by the script.

### Decision tree

```
python scripts/topic_gate.py --topic "<topic>"
        │
        ├─ ct_literature_installed = true  →  recommended_path = "ct_literature"
        │     ▸ Directly invoke ct-literature for full retrieval (no prompt):
        │         cd <ct_literature_dir> && python scripts/ct_literature.py \
        │           --topic "<topic>" --review-type meta-analysis \
        │           --with-europepmc --with-semantic-scholar --year-from <y-5> \
        │           --safety --prisma --run --out-dir ./lit
        │     ▸ Use its .merged.json / Excel / HTML as the Stage-4 novelty evidence.
        │
        └─ ct_literature_installed = false →  recommended_path = "ct_search_prompt"
              ▸ AskUserQuestion to the user:
                  A) Install ct-literature then continue  (recommended; full retrieval)
                     → show install hint, pause until installed, then run as above.
                  B) Do a simple analysis now  (no install)
                     → directly call the ct-search remote service:
                         python adapters/ctsearch_client.py search \
                           --source europepmc --keyword "<topic>" --year-from <y-5> --run
                     → use its real hit counts + top titles as Stage-4 dedup evidence.
              ▸ Absolute fallback (ct-search unreachable even in branch B):
                run the in-skill `adapters/literature_probe.py` (direct Europe PMC,
                fully coze-independent). Never leave topic selection without a
                real-hit-count probe.
```

### Why this path
- **ct-literature is the best evidence base** (6-source retrieval + dedup + PRISMA + anti-hallucination), so when installed it is used directly — no degraded default.
- **ct-search remote is the lightweight equivalent** of the in-skill probe but richer (OpenAlex/Europe PMC/bioRxiv/…, same backend ct-literature uses) and **needs no ct-literature install** — the correct "simple analysis" branch when the user declines to install.
- The in-skill `literature_probe.py` (direct Europe PMC) remains only as the **offline ultimate fallback**, not the default.

⛔ **Red line preserved**: regardless of which path supplied them, candidate ranking MUST be grounded in the probe's real `hit_count` + the 4-dim score card (R7). The LLM never free-forms "which direction is good".

## Dual path entry（双路径入口）

| User signal | Path | Output |
|---|---|---|
| "5 分钟告诉我能不能做" / "quick feasibility" | **Quick Assessment** | 1-page decision card: rough 4-dim scores + verdict + **live real-gap evidence** (Cochrane/PubMed probe + broad-direction ratio) + top risks (≤30 min) |
| "给我一份选题报告" / "PROSPERO 预审计" | **Full Assessment** | 5-stage workflow → 11-section report (`generate_topic_report.py`) |
| "被拒为重复了" | **Dedup re-review** | Increment re-review report (subset of Full: Stage 4 only + verdict) |

> Quick Assessment must NOT give a final go/no-go — it is a screen.
> If Quick returns ⚠️ or ❌ on any dimension → recommend Full Assessment.
>
> **Quick 卡必须携带真实缺口证据（2026-09-08 融合）**：仅给四维评分而不给缺口依据，会让"新颖性"变成空中楼阁（旧版曾因缺失此层被质疑）。Quick 路径须**实时跑探针**两次——① 窄方向主题，② 其宽泛父方向（如「PD-1 NSCLC 二线」→「NSCLC 免疫治疗」），用 `literature_probe.py` 取 `cochrane.hit_count` / `pubmed_meta.hit_count`，算 `ratio = 窄.PubMed / 宽.PubMed`，落到 `gap` 字段并渲染进卡片（见 Output contract）。探针不可用时 `verdict="unverified"`，卡片显示"未验证"，**不得**用模板数字硬填。可用 `adapters/build_gap_probe.py` 一键跑窄方向+宽泛父方向双探针并产出 `gap` 字段（`--out gap.json` 单独输出，或 `--merge-into input.json` 合并进选题 input 直接喂给 `generate_topic_report.py`）。
>
> **真实缺口判定阈值**：`ratio < 0.3` 且 `Cochrane < 10` → `real_gap`（真实缺口，✅）；`ratio ≥ 0.5` 或 `Cochrane ≥ 20` → `saturated`（已饱和，🔴，须明确增量）；介于之间 → `caution`（⚠️，须差异化）。该 Verdict 与四维"新颖性"互校：新颖性给 4–5 但缺口判定 `saturated` 时，触发 R3 复核。

## Four-dimension scoring model（四维评估模型）

Each dimension scored 0–5 with a **mandatory anchor reason** ("should be 4"
alone is NOT acceptable). Total 0–20.

| Dimension | 0–1 (fatal gap) | 2–3 (weak) | 4–5 (strong) |
|---|---|---|---|
| **临床价值 Clinical Value** | No clinical question / already answered | Marginal relevance | Answers a real decision (drug, dose, population) |
| **方法学可行性 Methodological Feasibility** | No estimable effect measure / impossible design | Loose PICO, few comparisons | Clean PICO, standard effect measures, feasible design |
| **数据可得性 Data Availability** | No realistic data source | Partial data, heavy reconstruction | Published summary data or IPD obtainable |
| **新颖性 Novelty** | Known duplicate | Incremental only | Fills a genuine evidence gap (verified by dedup search) |

### Score rules
- 总分 ≥17 → 强烈建议（strongly recommend）
- ≥14 → 建议（recommend）
- ≥10 → 暂缓（hold, fix gaps first）
- <10 → 不建议（not recommended at this time）
- **任一维 ≤2 → 一票否决（veto）**：无论总分多少，先解决该维缺陷再谈选题。

## Cross-check rules R1–R6（交叉检查规则）

Run after scoring; any rule **triggered** → force re-review of the flagged
dimension(s), output must state which rule fired and what was re-examined.

| Rule | Check | Trigger example |
|---|---|---|
| **R1** | Clinical value says high but PICO is coarse ("实体瘤患者" + "PD-1 抑制剂" whole class) | Score ≥4 clinical but PICO not decomposable to a drug/dose |
| **R2** | ≥3 interventions compared but meta type chosen is pairwise, not NMA | Multi-arm design + "pairwise" in report |
| **R3** | Novelty ≥4 but no dedup search evidence recorded | High novelty without PROSPERO/Cochrane/PubMed hits logged |
| **R4** | Methodological feasibility ≥4 but no pre-specified heterogeneity threshold / subgroup plan | Feasibility high, I² trigger (e.g. >50%) not pre-set |
| **R5** | Data availability ≥4 but effect measure inconsistent with outcome type (e.g. survival outcome → OR) | Availability high + mismatched effect measure |
| **R6** | Full assessment claims "recommend/proceed" but PROSPERO registration not mentioned | Verdict proceed + no PROSPERO step in next actions |
| **R7** | Candidate directions ranked by meta *type* (pairwise/NMA/regression) or by raw feasibility, **without** a real dedup screen — and a saturated/generic direction is listed as the top pick | Top candidate is "SGLT2i vs placebo on CKD composite endpoints" (a direction already covered by ≥5–6 large meta-analyses in 2024) with no evidence-gap justification |

## Meta type decision tree（Meta 类型决策树）

```
Compare interventions (≥3 arms, same outcome)?
 ├─ yes → NMA (netmeta / gemtc；multinma 可选)
 ├─ no → individual patient data available?
 │    ├─ yes → IPD meta (one-stage / two-stage)
 │    └─ no → dose-response relationship in scope?
 │         ├─ yes → dose-response meta (dosresmeta)
 │         └─ no → diagnostic accuracy question?
 │              ├─ yes → DTA meta (mada bivariate + SROC)
 │              └─ no → outcome type:
 │                   ├─ binary / continuous / survival / rate → standard pairwise
 │                   ├─ single proportion / prevalence → single-group meta
 │                   └─ genetic association / multivariate → specialized (esc / mvmeta)
```

Mapping to this skill's engines: see `advanced_analysis.md` (IPD /
multilevel / dose-resp / power), `bayesian_nma.md` (Stan/JAGS),
`diagnosis_meta.md` (mada), `single_group_meta.md` (metaprop et al.).

## Five-stage full workflow（完整评估 5 阶段）

Each stage has a **decision gate**; do NOT pass to the next stage until the
gate is cleared.

### Stage 1 — Research interest clarification
Ask: core interest, meta goal (thesis / journal / grant / learning), method
capability boundary, resource constraints.
- **Gate 1**: output 1–3 candidate directions. 0 → ask another round;
  ≥4 → ask user to shortlist 3.

### Stage 2 — PICO/PECO operational decomposition
See `pico-guide.md`. Every element must be expressible as a search term.
- **Gate 2**: self-check list all pass → Stage 3.

### Stage 3 — Four-dimension scoring + meta type selection
Score with anchors, run R1–R6, choose meta type via decision tree.
- **Gate 3**: total + veto rules applied; type chosen → Stage 4.

### Stage 4 — Dedup search + PRISMA/AMSTAR-2 pre-check
See `dedup-search.md` and `compliance-precheck.md`.
**Which dedup source to use is decided by the Topic Gating (见上文「选题门控」)**:
- **ct-literature installed** → use its `.merged.json` (full 6-source retrieval + dedup) as the dedup evidence.
- **ct-literature NOT installed, user chose simple analysis** → use the **ct-search remote** probe `python adapters/ctsearch_client.py search --source europepmc --keyword "<topic>" --run` (real `hit_count` + top titles).
- **Absolute fallback** (ct-search unreachable) → run the in-skill Europe PMC probe `adapters/literature_probe.py` (`dedup_probe`) for the **Cochrane (CDSR)** and **PubMed/MEDLINE** layers — live, no other skill required.

All three paths return real `hit_count` + top titles that directly feed the novelty
dimension and the R7 ranking. PROSPERO and non-English DBs remain guided manual
steps (no clean public API). Templates are only a fallback when the network is
unavailable.
- **Gate 4**: dedup evidence (live `hit_count` from the chosen probe) + compliance risk 🟢/🟡/🔴 recorded → Stage 5. If `any_error` (network down), mark dedup **"unverified"** and state so in the report.

### Stage 5 — Topic report generation
Mode A (recommended): `python scripts/generate_topic_report.py input.json output.md|html`.
Mode B: fill `references/topic-report-template.md` by hand.
If PROSPERO registration intended → include `prospero-mapping.md`.

## Output contract (JSON for report generator)

```json
{
  "slug": "pd1-nsclc-2ndline",
  "title": "PD-1 inhibitors vs docetaxel in 2nd-line NSCLC",
  "date": "2026-08-15",
  "path": "full",
  "background": "…",
  "pico": {"P": "...", "I": "...", "C": "...", "O": "...", "search_terms": {...}},
  "meta_type": "pairwise",
  "scores": {"clinical": 4, "feasibility": 4, "data": 3, "novelty": 4, "total": 15},
  "score_anchors": {"clinical": "…", "feasibility": "…", "data": "…", "novelty": "…"},
  "cross_checks": [{"rule": "R1", "triggered": false, "note": ""}],
  "gap": {"probe_used": true, "narrow": {"cochrane": 4, "pubmed": 224}, "broad": {"topic": "NSCLC 免疫治疗", "pubmed": 2240}, "ratio_narrow_over_broad": 0.1, "verdict": "real_gap", "label": "真实缺口", "summary": "该窄方向 PubMed 224，约为宽泛方向(2240)的 1/10 → 真实缺口"},
  "dedup": {"prospero": "...", "cochrane": "...", "pubmed": "...", "non_english": "...", "near_duplicate": "no", "increment": "..."},
  "search_strategy": "…", "expected_studies": "…",
  "compliance": {"prisma": [{"item": "1", "status": "ok"}], "amstar2": [...], "overall_risk": "green"},
  "outcomes": ["ORR", "PFS", "OS"],
  "subgroups": ["histology", "PD-L1 TPS"],
  "sensitivity": ["leave-one-out", "quality filter"],
  "risks": [{"risk": "…", "mitigation": "…"}],
  "next_actions": ["PROSPERO registration", "…"],
  "verdict": "recommend"
}
```

Verdict mapping: `strongly_recommend | recommend | hold | not_recommended`
(+ `veto:<dimension>` suffix when a veto fired).

## Traps to avoid (13, distilled from reference skill + Cochrane guidance)

1. Never skip the dedup search in a Full assessment.
2. PICO must not be coarse; complex interventions decomposed to the drug/dose.
3. ≥3 interventions → NMA, not pairwise.
4. Pre-specify ≥3 subgroup analyses.
5. Pre-set heterogeneity threshold (e.g. I²>50% → subgroup/regression).
6. No unanchored optimistic scores — every score needs an anchor.
7. Run R1–R6 always in Full mode.
8. PRISMA 2020 item #16 (equity, PROGRESS-Plus) must be considered.
9. Verdict "proceed" must mention PROSPERO registration.
10. Distinguish near-duplicate vs exact duplicate (see `dedup-search.md`).
11. Non-English population → extend non-English DB search.
12. Quick assessment must not give a final verdict.
13. Outcome ↔ effect measure mismatch → block (see R5).
14. Candidate directions must be ranked by **evidence gap + novelty verified by dedup search** (R7), not by meta *type* or raw feasibility. Never list a saturated/generic direction (e.g. a broad "SGLT2i vs placebo on CKD composite endpoints" pairwise meta already covered by ≥5 large 2024 meta-analyses) as the top pick without an evidence-gap justification.
