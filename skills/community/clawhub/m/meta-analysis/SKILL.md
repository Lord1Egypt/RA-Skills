---
name: meta-analysis
cn_name: 医学Meta分析
slug: meta-analysis
displayName: Meta Analysis / 医学Meta分析
version: 2.20.1
license: MIT
summary: 基于 R 的全方位 Meta 分析技能，覆盖 RevMan + Stata 等价 + esc + RVE + 贝叶斯 NMA + 生存 Meta + TSA + 单组率 Meta + 诊断 Meta + 系统评价流程；输出森林图、漏斗图、异质性(I²)、发表偏倚、亚组分析、元回归、网络 Meta等共 23 种分析图形。所有分析提供可复现 R 代码。还可提供Meta选题方向判断 + 文献检索整理 + 筛选 + 数据提取功能。
description: "Comprehensive R-based meta-analysis skill covering RevMan + Stata equivalents + esc + RVE + Bayesian NMA + survival meta + TSA + single-group meta + diagnostic meta + systematic review workflow; produces forest plots, funnel plots, heterogeneity (I²), publication bias, subgroup analysis, meta-regression, network meta, for a total of 23 analysis figures. All analyses ship reproducible R code. Can also provide meta topic-direction judgment + literature retrieval and organization + screening + data-extraction functionality. / 基于 R 的全方位 Meta 分析技能，覆盖 RevMan + Stata 等价 + esc + RVE + 贝叶斯 NMA + 生存 Meta + TSA + 单组率 Meta + 诊断 Meta + 系统评价流程；输出森林图、漏斗图、异质性(I²)、发表偏倚、亚组分析、元回归、网络 Meta等共 23 种分析图形。所有分析提供可复现 R 代码。还可提供Meta选题方向判断 + 文献检索整理 + 筛选 + 数据提取功能。"

required_commands: [python]
invocable: true

triggers:
  - "meta分析"
  - "meta-analysis"
  - "系统评价"
  - "森林图"
  - "漏斗图"
  - "异质性"
  - "发表偏倚"
  - "元回归"
  - "network meta"
  - "贝叶斯meta"
  - "效应量转换"
  - "TSA"
  - "诊断meta"
  - "full meta pipeline"
  - "上下文菜单"
  - "对话菜单"
  - "全流程菜单"
  - "flow menu"
  - "论文撰写"
  - "写稿"
  - "初稿"
  - "投稿建议"
  - "发表建议"
  - "writing advisor"
  - "manuscript"
permissions:
  scope: "user-space-only"
  network: required
  network_note: "All numerical computation runs on the coze cloud R engine; analysis params/summary stats are POSTed to coze. No local-R fallback (paid-only feature); IPD only if the user explicitly opts in."
  filesystem: "writes only to the current working directory (meta_analysis/ and output/ report artifacts: generated .R scripts, .svg/.png figures, .csv tables); otherwise read-only"
metadata:
  {
    "openclaw": { "emoji": "📊", "icon": "assets/icon.svg" },
    "authors": ["medstatstar", "phoe-zip"],
    "homepage": "https://github.com/medstatstar/meta-analysis",
    "workbench_url": "https://meta.app.workbuddy.host/",
    "workbench_url_alias": "https://meta.app.workbuddy.link/",
    "workbench_domain_prefix": "meta",
    "workbench_domain_note": "Registered exception to the ct-base iron rule (2026-09-16): simplified prefix 'meta' instead of the skill name. Whitelisted, do not extend.",
    "workbench_app_id": "wbapp_hNZl928SI6wByvJt2COtcC",
    "workbench_owner_workspace": "2026-09-17-09-54-01",
    "workbench_sandbox": "a3c70e48be8f45019845b76383334bfc",
    "tags": ["meta-analysis", "systematic-review", "clinical-trials", "R", "biostatistics", "evidence-based-medicine", "forest-plot", "network-meta-analysis", "bayesian", "metafor", "meta", "netmeta", "gemtc", "revman", "robumeta", "clubSandwich", "esc", "dosresmeta", "mada", "metagear", "forestploter"],
  }
---

# Meta-Analysis

> R-based comprehensive meta-analysis. Every module ships reproducible R code.

## Language

- **English guide** → [README.md](https://github.com/medstatstar/meta-analysis/blob/main/README.md) · **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/meta-analysis/blob/main/README_zh-CN.md)
- Bilingual auto-switch: the answer language follows the user's question language (English question → English answer, Chinese question → Chinese answer).

## 0. Execution discipline (speed-first)

> 🚀 **Top-level red line — higher priority than any "thinking/polishing" impulse. Violation = wasting the user's time.** Full boundaries/exceptions/anti-patterns in `references/speed-discipline.md`.

### Two-track gating (code-driven routing, no LLM decision)
The first message goes through `python scripts/classify.py` for **deterministic triage** (zero LLM decision):
- **Compute track (compute)**: clear Simple / Complex → describe and immediately run `run_meta.py --query --data`; three steps to completion, fully bound by this discipline.
- **Topic track (topic)**: vague / topic selection / feasibility → **first run `scripts/topic_gate.py`** to route on ct-literature install status (installed → call ct-literature directly; not installed → AskUserQuestion install-vs-simple, simple = ct-search remote `adapters/ctsearch_client.py search`), then `generate_topic_report.py`; code-grounded, zero free-form improvisation.
- Both tracks forbid reading source via Read/Grep/Bash to "confirm how to tune / which task to use" — that is `classify.py`'s job.

### Agent operation card (copy verbatim, no variations)
```bash
# Compute track one-shot: report lands in --out-dir (user workspace); in-conversation data uses --data-json to skip file writes.
# If data comes from a file, pass --data <csv|json absolute path> (csv auto-converts to JSON before sending to coze).
python scripts/run_meta.py --query "<user original request>" --data-json '<[{"study":"S1",...}]>' --out-dir "<user workspace>/meta_analysis"
```
Read `META_HTML_REPORT=<path>` from stdout and pass directly to `present_files`; across turns, carve a subset into a new csv/json and re-issue the same command (always include `--out-dir`). Do NOT use this card for the topic track. Fallback `META_STATUS=build_failed` → re-run with `--colmap` per the hint.

### Six iron rules
1. **Execute, don't think**: when running the skill, only perform the workflow; no reasoning/trade-off/review/self-explanation; if a field is missing, ask only about that field.
2. **Zero number rewriting**: cite `stats`/`pooled`/`heterogeneity`/`bias` verbatim; no rounding/conversion/re-formatting.
3. **HTML report is the sole presentation surface**: `out['html_report']` is the final deliverable; no further processing; inline `show_widget` is deprecated, figures only appear in the HTML.
4. **Coze is the sole source of truth for computation**: all numerical analysis/computation runs on the coze R engine; the local side keeps only orchestration + send/receive and retains no compute engine. If coze is unreachable/unauthorized, raise a structured error per §6 — never fall back to local. (Consequence: without coze authorization the skill cannot compute — this is intended, as it supports paid-only features.)
5. **Call-count invariant**: compute track ≤1 call before fire (only `build_request`), ≤1 call after fire (only `present_files`); topic track ≤2; no retry loops. Cross-turn `--data-json` refill is input construction and does not count.
6. **No duplicate fire**: once `run_meta.py` is in-flight (the Bash call has been issued), **wait for the result** — do NOT re-issue the same or equivalent command. If `META_STATUS=error`, follow the structured guidance; do NOT silently retry. If `META_HTML_REPORT=...`, pass to `present_files` — done. One command, one wait, one result.

### Already automated / anti-patterns
Subgroup columns auto-pass-through, column-name aliases auto-matched, artifact completeness guaranteed by `run_analysis` — the agent must not read source to verify, must not hand-assemble subgroup into request.json, must not declare "missing Q_between" each round.

**❌ Impatient duplicate fire (2026-09-17 field incident):** re-issuing `run_meta.py` before the previous call returns wastes coze compute and burns rate limits. Full anti-pattern list → `references/speed-discipline.md`.

## 1. Triage — First step: classify the user's intent

> **Routing is already done in code (§0 two-track gating)**: track / task judgment is delegated to `build_request.py` (which calls `classify.py`); the LLM no longer makes routing decisions and does not hand-write request.json. The table below is for understanding only — the LLM calls `run_analysis` directly from the generated `request.json` and `present_files(html)`.

| Classification | Condition | Action |
|---|---|---|
| **Simple** | Single, specific intent (e.g., "pool OR from these 5 studies") | Reply directly, no menu |
| **Complex** | Multi-decision / multi-parameter (e.g., "network meta with 3 interventions, subgroup, check inconsistency") | Present level-1 routing menu incl. "③ Can't decide? → explain the differences"; full menu → `references/interactive_menu.md` |
| **Vague** | Unclear what user wants (e.g., "I need meta-analysis help") | Grill-me branch questions, 1–3 per round; "no topic / feasibility" → **Topic Selection** (§2.2) |

If unsure between Simple and Complex → give short reply + optional expansion hint.

## 2. Conversation guide

### 2.1 Interactive menu
Vague → Level 1 menu (7 categories). Select → Level 2 with data-format hints. Sufficient info → skip menu, run directly. Full menu tree + data formats → `references/interactive_menu.md`.
> **Other formats?** Install `@skill:statdata-transfer` for 50+ format conversion.

### 2.2 Topic Selection (upstream gate, self-contained)
Trigger: no topic / feasibility check / "rejected as duplicate" / pre-PROSPERO audit → `references/topic-selection.md`. Two paths:
- **Quick** (≤30 min): 1-page decision card — 4-dim scores (clinical/feasibility/data/novelty, 0–5, any ≤2 = veto) + screen verdict.
- **Full** (5 stages + gates): PICO (`pico-guide.md`) → scoring + cross-checks R1–R6 → dedup (`dedup-search.md`) → PRISMA 2020/AMSTAR-2 (`compliance-precheck.md`) → 11-section report via `python scripts/generate_topic_report.py input.json output.md|html` (templates → `topic-report-template.md` / `prospero-mapping.md`).
- **Dedup source is gate-driven (see Topic Gating in `topic-selection.md`)**: first run `scripts/topic_gate.py`; if **ct-literature** is installed, call it directly for full 6-source retrieval (`.merged.json` as Stage-4 evidence); if not installed, AskUserQuestion → simple-analysis branch calls the **ct-search remote** (`adapters/ctsearch_client.py search --source europepmc`, no install needed); in-skill `adapters/literature_probe.py` (direct Europe PMC) is only the offline ultimate fallback. All paths return real `hit_count` + titles; novelty ranking grounded in actual literature.
  - ⛔ **Topic-track red line**: candidate ranking **must** be based on the probe's real hit counts + 4-dim score card; the LLM only paraphrases, strictly no free-form "which direction is good". Quick is ranked by the probe card; Full is reported by `generate_topic_report.py`, the LLM does not rewrite.

### 2.3 Upstream orchestration (retrieval → screening → extraction → analysis)

> **Repositioning (2026-08-30):** meta-analysis evolved from "pooling effect sizes only" into a "full-chain Meta orchestrator".
> The upstream three stages reuse existing modules and `ct-literature`; the only new capability is the **data-extraction assistant** (LLM draft + human-verification gate).

Full-chain orchestration, command list, seam pitfalls (incl. `included_records` ≠ `included`), and guard semantics → `references/upstream_orchestration.md`.
Writing-advisor (④′), evidence-upload (④″), and detailed A-stage contract / type-confirmation model → `references/chat_orchestration.md`.

- ⛔ **Automatic PDF value extraction is SUSPENDED (2026-09-27, user-decided)**: `features.a4_extraction=False` gates off A4 auto 2×2 extraction; three backend bypasses (`/api/upload_pdf`, `/api/upload_pdf_auto`, fastpath `data_mode="pdf"`) return 409. Do NOT offer "auto-extract numbers from PDFs" as an available capability in chat. Unfreeze = set `a4_extraction: True` in `adapters/features.py`.

> ⚠️ **The human-verification gate is a red line:** any CSV from `extract_assist.py` not `stamp --confirm`ed is blocked by `run_meta.py` (`META_STATUS=unverified_extraction`).

### 2.4 Systematic-review full-flow mode (@skill entry)

> **Trigger:** "systematic review full flow" / "from retrieval to meta-analysis" / "systematic review workflow" → end-to-end orchestration, not a direct jump to compute track.
> The agent executes the full playbook → `references/systematic_review_fullflow.md`. CCM (Conversation Context Menu) is **DISABLED** for agent use (2026-09-27) — two execution surfaces remain: ① the **published web app** and  **plain conversation** (agent narrates + asks open questions in prose). Do NOT render `flow_menu.py` menus in chat.
> Archived CCM details (menu design, A1/A2 sub-menus, pre-flight checks, contract gaps) → `references/chat_orchestration.md`.
### 2.5 Workbench — published app & local launch

> **Trigger:** "工作台" / "workbench" / "meta 全流程" etc.
> Published app metadata, share link, appId, publish toolchain, local-launch commands → `references/workbench.md`.

## 3. Initialization & execution backend

**Execution model**: coze-only, absolute. Startup: probe `coze_client.health()`, create `meta_analysis/` + `output/`, read R config from `~/.workbuddy/MEMORY.md`. Details → `references/ADVANCED.md`.

## 4. Core functions & API

Module → R-package/function matrix → `references/advanced_api.md` · `references/ADVANCED.md`.
**Rule (mandatory)**: any analysis MUST call existing functions — never rewrite inline. Unified entry `adapters/run_analysis.py` (default: coze).

## 5. Output specification

**Artifacts**: `analysis_complete.R` + forest/funnel (`.svg`, inlined in HTML) + `results_summary.md` + `last_run.json`. Per-round dataset CSV is an *input* the agent carves; `run_analysis.py` does NOT auto-write `data_backup.csv`.

**Rendering**: `figures[].svg` embedded into single-file HTML report → `present_files`. Inline `show_widget` cancelled. SVG keeps natural width. Quality Gate: R-side `run_quality_gate()` → red (k<3 / I²>75% / missing bias check) **blocks** presentation.

**Cross-turn continuity (mandatory)**: stateless runtime → echo `## 当前分析设定 / Current analysis settings` after every analysis; follow-up changes only changed fields; dataset supplied per round (no `data_backup.csv`). Full spec + merge_spec + endpoint capability boundaries → `references/cross_turn.md`.

## 6. Security & scope

**Execution model**: numeric computation via coze. **Data-exfiltration decision belongs to the user**.

**Outbound disclosure**: analysis data (no PII) POSTed to coze, sanitized by `sanitize_payload()`. Default endpoint pre-approved; custom `COZE_META_ENDPOINT` asks AUTH-BLOCK on first call. First outbound notice each session (once, bilingual). Attribution never empty (`query_origin` hostname SHA-256 + `request_id` UUID). Coze failure needs consent before diagnose+retry.

**Other boundaries**: PDF download ONLY on explicit user instruction (`adapters/pdf_fetch.py`). Data-extraction guard (red line): `extract_assist.py` CSV blocked until `stamp --confirm`.

Full security details → `references/ADVANCED.md` · `references/pdf-download-portals.md` · `references/bug_report_endpoint.md`.

## 7. User-uploaded files

1. **Structured data (`.csv`/`.xlsx`/`.xls`)** → Type 4 template (`references/data_templates.md`).
2. **Document/template (`.docx`/`.pptx`/`.pdf`/`.doc`)** → convert to md first: `.docx`/`.pptx` via `scripts/office_to_md.py`; `.pdf` via `pdf` skill.

**🔔 Pre-conversion notice**: `⚠️ All uploaded documents will be converted to md. PPT conversion can lose images/layout/animations/charts.`

Full upload spec → `references/data_templates.md`.

## 8. Bug Reporting

Agent behavior only; implementation → `adapters/bug_report.py`, protocol → `references/bug_report_endpoint.md`. Trigger ≤1 proposal/session. Two-stage confirmation (propose-with-preview → consent → send). 11-key whitelist, never raw data.

## 8.5 Deploy Retest Gate (mandatory before publish / deploy)

**Freeze check FIRST**: before any publish attempt to GitHub → SkillHub → ClawHub, run `python adapters/publish_guard.py` — exit code 2 means a dev-period publish freeze is active (`adapters/DEV_POLICY.json`) and publishing is blocked; do NOT proceed and do NOT bypass it. This check is part of the gate, not optional advice.

**Mandatory before publishing / deploying** to GitHub → SkillHub → ClawHub: run `python tests/deploy_retest.py` (`--live` to actually hit the network; publish allowed only on all-green). This gate strictly verifies that the coze response is **genuinely valid** (HTTP 200 ≠ success; it rejects `status=ok` empty shells / `NaN` / no-figure (svg/url) false greens — coze externalizes SVG to S3 `url`, so a present+reachable `url` counts as a valid figure), writes `tests/deploy_retest_report.json`, and exits non-zero on any failure to block publishing. Use `--mock` for local logic self-check (no network) and `--offline` for envelope-contract validation. Full rules and red lines → `outputs/deploy_retest_gate.md`.
## 9. Meta information

**Traceability**: all factual claims cite a `ref-*.md` section or official guideline; unverifiable → mark `⚠️ official verify`.
**References**: full index → `references/references.md`. Key: `interactive_menu.md`, `ADVANCED.md`/`ADVANCED_zh-CN.md`, `advanced_api.md`, `topic-selection.md`, `data_templates.md`, `svg_editing.md`. Units → `references/units.md`.
**Project Files**: `README.md` | `README_zh-CN.md` | `CHANGELOG.md` | `AGENTS.md` | `LICENSE` (MIT © 2025 medstatstar) | `requirements.txt` | `assets/icon.svg`.
**Changelog**: → `CHANGELOG.md`.
