# Migration Notes — AIPOCH medical-research-skills

> 中文摘要：对比 AIPOCH `meta-analysis` 及 5 个 meta 绘图技能与本技能的差异，列出"可考虑吸收的点"清单（8 条建议采纳 / 5 条建议不采纳），供主代理决策。**本文件仅供决策参考，不改动 SKILL.md。**
>
> **Adapted from**: `meta-analysis`, `meta-forest-binary-plot`, `meta-funnel-plot`, `meta-baujat-plot`, `meta-radial-plot`, `meta-rob2-plot` — AIPOCH, MIT License
> **Source**: https://github.com/aipoch/medical-research-skills
> **Migrated**: 2026-08-04 (into meta-analysis)

Scope: this is a **decision aid for the maintainer**, not an executable reference. Nothing here has been applied to `SKILL.md`.

---

## A. Baseline Comparison

The upstream `meta-analysis` skill is a single-file, Python-first skill (~260 lines) covering DL random-effects pooling, forest/funnel plots via matplotlib, Egger/Begg, and PRISMA reporting notes. This skill already supersedes it on statistical coverage (RevMan parity, Stata equivalents, NMA, Bayesian, TSA, RVE, diagnostic meta, dose-response).

Therefore **no statistical method from upstream is missing here.** The candidates below are about *engineering conventions, guardrails and scope framing*, plus one genuine capability gap (Python fallback).

---

## B. Candidates to Adopt

### B1. Python fallback path when R is unavailable — *recommend adopt*

Upstream ships a working pure-Python implementation (numpy/scipy/matplotlib) of DL random-effects pooling, forest plot, funnel plot, Egger and Begg. This skill declares `required_commands: [Rscript, python]` and hard-fails without R.

- **Value**: a user without an R installation currently gets nothing. A degraded Python path could still deliver a basic pairwise pooling + forest/funnel.
- **Where**: new `references/python_fallback.md` + `scripts/` entry; `SKILL.md` Initialization step 1 would branch instead of dead-ending.
- **Caveat**: must be clearly labelled *degraded mode* — no HK, no REML, no NMA, no prediction interval. Risk of users silently accepting the weaker path.

### B2. Every figure ships a companion data CSV — *recommend adopt*

All five upstream plot scripts write `<name>.png` **and** `<name>.csv` containing exactly the plotted coordinates (funnel x/y, baujat x/y/rank, radial precision/z/in-band, forest per-study effect/CI/weight).

- **Value**: reviewers and journals increasingly require the numbers behind every figure; also makes figures re-renderable without re-running the model.
- **Where**: `SKILL.md` §Output — currently promises `.svg`+`.png`+`results_summary.md`+`data_backup.csv`; extend to a per-figure CSV convention.

### B3. Deterministic output filename contract — *recommend adopt*

Upstream uses `{Type}_{plot}_{outcome}.{png|csv}`, e.g. `Binary_funnel_Mortality.png`, `Continuity_baujat_PainScore.csv`.

- **Value**: predictable artefacts across a multi-outcome review; trivially scriptable; avoids overwrite collisions when the same plot is produced for several outcomes.
- **Where**: `SKILL.md` §Output, or `references/units.md` as an output-unit convention.

### B4. Explicit "Zero-Hallucination Rule" on study-level data — *recommend adopt*

Upstream states plainly: all study-level data must come from tool results or user-provided data; never generate fictional study names, sample sizes or effect sizes; if data are insufficient, say so.

- **Value**: this skill's §Traceability covers *citing references*, but does not explicitly forbid **fabricating study rows**, which is the higher-severity failure mode for a meta-analysis agent.
- **Where**: `SKILL.md` §Traceability / Grounding, as an additional bullet.

### B5. "When NOT to Use" + sibling-skill routing — *recommend adopt (adapted)*

Upstream lists out-of-scope requests and routes them (protocol design, literature search, single-study stats, narrative review).

- **Value**: this skill has §Security & Scope and a "no literature DB search" note, but no consolidated negative-scope block. Useful for triage accuracy.
- **Adaptation**: route to the local ct-series equivalents (`ct-protocol`, `ct-literature`, `statsoft-cli`) rather than upstream's skill names, which do not exist here.

### B6. Minimum-k gating enforced in code, not just documented — *recommend adopt, with corrected thresholds*

Upstream scripts hard-stop below a minimum k (forest ≥ 2, funnel ≥ 2, baujat/radial ≥ 3, bias tests ≥ 3).

- **Value**: prevents meaningless output being produced silently.
- **Correction required**: upstream allows Egger/Begg at k = 3. The Cochrane Handbook threshold is **k ≥ 10**. Adopt the gating mechanism, but set funnel-asymmetry testing to k ≥ 10 with an explicit refusal message. This is already documented in the migrated `funnel-plot.md` §1.

### B7. Structured, fixed-field console summary — *recommend adopt (low priority)*

Every upstream script prints the same block: outcome · data type · k · output files · pooled effect · heterogeneity · conclusion.

- **Value**: predictable, parseable, and reduces the chance of omitting heterogeneity stats next to a pooled estimate.
- **Where**: `references/report_template.md` already covers report skeletons; this would be the *console/turn-level* analogue. Overlaps — check before adding.

### B8. Unified three-shape input contract across all plot types — *recommend adopt*

Upstream uses one CLI signature (`<csv> <type> [outcome] [outdir]`) with `type ∈ {Binary, Continuity, Survival}` and the same column names across forest/funnel/baujat/radial.

- **Value**: one data file drives every figure in the review; no re-shaping between plot types. The six migrated reference files already assume this contract.
- **Where**: `references/data_templates.md` — verify the existing templates are compatible before standardising.

---

## C. Explicitly Do NOT Adopt

| Item | Reason |
|---|---|
| `dpi = 150` in `ggsave()` (baujat, radial) | Below every journal minimum. The migrated files specify ≥ 300 / 600. |
| Egger/Begg at k ≥ 3 | Severely underpowered; produces false reassurance. Corrected to k ≥ 10. |
| Baujat axis labels | Upstream labels `bj$x` as "contribution to overall result" and `bj$y` as "contribution to Q" — **swapped**. Its manual fallback branch also assigns the axes opposite to its primary branch. Corrected in `baujat-plot.md` §3. |
| Egger's test for binary/OR outcomes | Known bias from the logOR–SE correlation. Harbord/Peters substituted in `funnel-plot.md` §3. |
| Upstream boilerplate sections ("Validation Shortcut", "Deterministic Output Rules", "Completion Checklist", "Quick Validation", auto-generated "Key Features") | Template filler, partly inaccurate (e.g. `python scripts/extract_criteria.py --help` as the validation path for a forest-plot skill). No value here. |

## D. Notes for the Maintainer

- Overlap check performed against: `revman_complete.md` (§IV forest, §V funnel, §IX bias, §X GRADE), `tsa_diagnostics.md` (§baujat), `svg_editing.md`, `data_templates.md`, `report_template.md`. Cross-references were added rather than duplicating content.
- `tsa_diagnostics.md` §baujat() is **correct** on axis orientation and does not need fixing; the new `baujat-plot.md` is its extended plotting/reporting companion and points back to it.
- The upstream repository ships **no** `meta-forest-continuous-plot` skill. `forest-continuous.md` was reconstructed from the `metacont()` configuration used consistently across the other AIPOCH scripts; this provenance is disclosed in that file's header.
- If B1 (Python fallback) is accepted, `required_commands` in the SKILL.md front matter must change from a hard `[Rscript, python]` requirement to a documented degraded mode.
- Licensing: all upstream material is MIT (author: AIPOCH). Attribution headers are present in all six migrated files; retain them on any further edit.
