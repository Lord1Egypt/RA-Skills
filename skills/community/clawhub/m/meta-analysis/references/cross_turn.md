# Cross-turn Continuity (mandatory)

> Extracted from SKILL.md §5.1 + §5 endpoint boundaries. Last sync: v2.17.1.

## 5.1 Cross-turn Continuity (mandatory)

> **Runtime is stateless.** coze R engine re-supplies `task`+`data`+`params` each call, never persists config/column mapping. Semantic drift (model/method silently changing) = highest-risk failure.

### Cross-turn spec (minimal unit maintained within the conversation thread)
```
{"task":"pairwise_meta","data_path":"<current-round csv>","measure":"OR","model":"random","method":"REML","subgroup":"—"}
```
(yi/sei/slab column mapping is already auto-derived by `build_request.py`; no explicit inheritance needed; `run_meta.py` is self-sufficient from query+data each time.)

### Three hard rules
1. **Echo a "当前分析设定 / Current analysis settings" block after every analysis (mandatory, after this round's numbers/figures):**
   `## 当前分析设定 / Current analysis settings: data=<csv> | measure=OR | model=random | method=REML | subgroup=— | task=pairwise_meta`
   Bilingual header (Chinese first, then English, separated by ` / `) is mandatory; field keys stay English (machine-readable for follow-up parsing). No field omitted (`—` placeholder) — lets LLM locate "most recent settings" on follow-up.
2. **On follow-up, change only the changed fields:** locate most recent `## 当前分析设定 / Current analysis settings:` block (match by either Chinese or English token), read all fields, override only what changed (e.g. `task←subgroup_analysis`, `subgroup←region`); yi/sei/slab + model/method/measure inherited verbatim — dropping column mapping = effect-size mismatch.
3. **Dataset supplied per round, not by magic pointer:** no auto `data_backup.csv`; carve subset into new csv + re-issue `run_meta.py` at it.

### Deterministic fallback
Worried about dropping config? `scripts/merge_spec.py` (prev+cur via stdin → merged spec):
```bash
echo '{"prev":{"task":"pairwise_meta","data_path":"<csv>","measure":"OR","model":"random","method":"REML","subgroup":"—"},"cur":{"task":"subgroup_analysis","subgroup":"region"},"required":["task","data_path","measure","model","method","subgroup"]}' | python scripts/merge_spec.py
```

### Endpoint capability boundaries (per coze `run_task.R` / `coze_contract.md` §3)
- `pairwise_meta` ✅ complete (I²/τ², Egger/Begg, funnel plot, quality gate)
- `subgroup_analysis` ✅ subgroup column **must** be passed as the param key `subgroup` (writing byvar/group/by silently fails)
- `metareg` ✅ requires effect-size columns te/sete + covariate column `params.cov` (passing only raw columns degrades to pairwise_meta)
- `nma` ✅ (≥2 arms per study); `nma_rank` ✅ (SUCRA/P-score); `survival_meta` ✅ (loghr/seloghr); `diagnostic_meta` ✅ (tp/fp/fn/tn, task name is not "diagnostic")
- **Network diagnostics + CINeMA (2026-09-14)** — `nma` / `nma_rank` / `cnma` additionally return network heterogeneity (`stats.heterogeneity`: `tau`/`tau2`/`I2`/`Q`/`df`/`p`; **previously `null`**), `stats.extra.network` (interventions / comparisons / studies / designs, plus `prop_direct` for **all three** network tasks) and `stats.extra.inconsistency` (design-by-treatment interaction test `Q`/`df`/`p` + per-comparison direct-vs-indirect differences for locating the source). ⚠️ `I2` is **always a percentage (0–100)** — netmeta's native 0–1 ratio is converted engine-side; do not convert again. ⚠️ `stats.k` / `extra.network.n_studies` / `extra.network.n_comparisons` count **unique** studies and **unique** comparison pairs (deduplicated by `studlab` / treat-pair) — **not** data rows; arm-based multi-arm studies expand to C(n,2) rows, so the old row-count reading over-reported both (self-audit fix, 2026-09-14). The interpretation layer routes network results to a dedicated branch and the quality layer assesses them with the **CINeMA six domains** (within-study bias / reporting bias / indirectness / imprecision / heterogeneity / incoherence) instead of plain GRADE — a domain short of data is reported `unclear`, **never silently treated as "no concern"**. Reading guide → `references/component_nma.md` §CINeMA.
- `rob2` ✅ (RoB2 / RoB traffic-light, self-drawn ggplot — no robvis dependency) and `rob_summary` ✅ (stacked-bar summary); `prisma_checklist` ✅ (PRISMA 2020, 27 items) and `prisma_flow` ✅ (four-stage diagram via `metagear::plot_PRISMA`); `grade` ✅ (GRADE certainty); `tsa` ✅ / `power` ✅ / `nnt` ✅ / `gosh` ✅ / `ipd_meta` ✅ / `metainc` ✅
- `cnma` ✅ **component network meta-analysis (additive model)** — built on `netmeta::netcomb()` / `discomb()`, **no extra dependency** (netmeta 3.6.1 on both local and cloud). Treatment labels encode components via `sep_comps` (single character, default `+`, e.g. `A+B`; inner spaces auto-trimmed); disconnected networks auto-route to `discomb()`. Returns component effects (`stats.extra.components`), combination effects (`stats.pooled`), the **additivity test** (`stats.extra.additivity`: `Q_diff`/`p_diff` — non-significant means the additive assumption is acceptable), the component design matrix (`stats.extra.design`) and the unidentifiable-components list (`stats.extra.unidentifiable`). **Unidentifiable components return `null`, never `0`**; degrees of freedom ≤ 0 (untestable) also yield `null` instead of a floating-point artefact. Params: `sep_comps` / `inactive` / `interaction` / `reference_group`; consumes `params.sm` (same as `nma`). Methodology, reading the additivity test, and pitfalls → `references/component_nma.md`.
- publication bias is embedded in pairwise_meta/funnel_plot; `sensitivity`/`pub_bias` are not registered tasks
- default figures adapt to the task (`build_request` requests per `figure.plots`; override via `params_extra.plots`)
> Few-shot samples → `references/interactive_menu.md` §6.
