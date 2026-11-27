---
name: procurement-admission-copilot
slug: procurement-admission-copilot-skill
displayName: Procurement Admission Copilot
version: "1.0.9"
description: Shadow-mode copilot for B2B procurement admission. Given a
  supplier's raw qualification inputs, it checks material-package completeness
  and internal consistency; given a set of approval cases, it tracks status,
  stalls, and gaps. It never drafts contract terms or makes the admission
  decision — only structures and flags for a human to decide.
description_zh: 采购准入影子助手
description_en: Procurement Admission Copilot
not_for:
  - Drafting contract terms or negotiating with suppliers
  - Making the admission or award decision (results are flags for a human decider)
  - Financial audits or procurement policy design
  - Consumer purchasing decisions
agent_created: true
---

# Procurement Admission Copilot

A shadow-mode, review-only copilot for the two repeatable, high-friction parts of B2B supplier / vendor procurement admission:

1. **Supplier material package readiness** — given a supplier's scattered qualification inputs (business license, certificates, product catalog, case studies, financials summary, compliance docs), check that the package is complete and internally consistent before it is submitted for admission review.
2. **Approval case management** — given a set of admission approval cases (each a supplier's request with submitted materials, reviewer, stage, due date, and decision), track status, stalls, and gaps so a human reviewer can act.

It structures and flags. It does **not** draft contract clauses and does **not** make the admission / sourcing decision. Responsibility stays with the procurement committee or buyer.

## When to use

- A supplier is preparing the document package for procurement admission / vendor onboarding and you want a readiness pass before submission.
- You receive a supplier's materials and need to know, fast, whether company identity, certificates, and figures are consistent across documents.
- You manage a queue of admission approval cases and need a status dashboard: what is stalled, what is blocked by missing documents, what needs a decision.
- You want a reviewable, one-pass readiness or case report to hand to a human reviewer or committee.

## Do not use

- Drafting contract terms, pricing clauses, or the legal/sourcing conclusion of admission → out of scope by design ("不碰合同结论").
- A single-document fact-check of an article or report → use `claim-to-source-auditor`.
- Negotiation or scorecard weighting of suppliers → this skill tracks and flags, it does not rank or decide.
- Directly modifying supplier documents.

## Input

```yaml
mode: material_package | approval_cases
# Mode A — material_package
supplier_inputs:        # folder or list of files
  - path:
    label: 营业执照 | 资质证书 | 产品册 | 案例 | 财报摘要 | 合规材料
checklist:              # optional industry qualification list
  - item:
    mandatory: true
reference_source:       # doc authoritative for company identity (default: 营业执照)
# Mode B — approval_cases
cases:                  # CSV / JSON / folder of case files
  - supplier:
    submitted_materials:
    reviewer:
    stage:
    due_date:
    decision:           # pending | approved | rejected | needs-info
    notes:
review_only: true       # never rewrite; output structured findings
```

## Workflow

### Mode A — Material Package Readiness (供应商材料包)

#### Step 1: [Deterministic] Load + extract structured fields

For each supplied document, extract:

- Company legal name **as written in that document** (capture per-doc wording — differences are the signal).
- Unified Social Credit Code (USCC) if present.
- Certificate names with issue / expiry dates.
- The document's submission deadline / validity window (needed to satisfy the deadline-integrity rule in Hard Rule 5).
- Revenue / scale figures and their stated source.
- Product / service categories and declared scope.
- Contact and registration details.

Record the extraction into a material manifest (the deterministic script consumes this).

#### Step 2: [Deterministic] Run the readiness check

Run `scripts/check_material_package.py` on the manifest. It performs:

- **Identity consistency**: compare legal names across documents after normalization; flag any divergence as a potential P0.
- **USCC presence**: flag missing USCC when mandatory.
- **Certificate validity**: expired mandatory cert → P0; expiry within 90 days → P1.
- **Required-document completeness**: any missing mandatory document → P0.
- **Financial consistency**: when two revenue figures differ beyond a tolerance band, flag P1 (inconsistency to reconcile).

Output `01-readiness-check.json`.

#### Step 3: [LLM] Consistency & quality review

Explain and extend the deterministic findings, and add judgments the script cannot:

- Name mismatch across documents (营业执照 vs 产品册 vs 案例).
- Expired or near-expiry certificates.
- Revenue inconsistency between financials, tax summary, and case-study scale.
- Weak or boilerplate case studies (no measurable outcome).
- Missing recommended (non-mandatory) qualification (ISO / industry cert / security clearance).
- Declared scope vs product categories mismatch.

Severity:

- **P0**: identity conflict (same supplier under different legal names / USCC); expired mandatory certificate; missing mandatory document; required USCC absent.
- **P1**: near-expiry certificate; revenue inconsistency; weak case study; missing recommended qualification.
- **P2**: cosmetic / formatting issues that do not affect admission readiness.

#### Step 4: [LLM] Produce the structured package + readiness report

Render a standardized **supplier material package** (from `templates/supplier-material-package.md`) and a **readiness report** (from `templates/readiness-report.template.md`) with the P0/P1/P2 list and recommended actions. Recommended fixes must cite an existing supplied document — never invent.

#### Step 5: [Deterministic] Human confirmation

Pause. Confirm P0/P1 disposition. The human (or the supplier's BD) revises the package. This skill is review-only.

### Mode B — Approval Case Management (审批案件管理)

#### Step 1: [Deterministic] Load + normalize

Read the cases (CSV / JSON / folder). Normalize each to the case schema: supplier, submitted materials, reviewer, stage, due date, decision, notes. Output `01-cases-normalized.json`.

#### Step 2: [LLM] Status analysis

- **Stalled**: past due with no decision → P0 if a compliance deadline is at risk, else P1.
- **Inconsistent decisions**: same supplier approved by one reviewer and rejected by another without rationale → P0.
- **Doc-gap blocked**: decision pending because a mandatory document is missing → P1.
- **Reviewer bottleneck**: one reviewer holds an outsized share of open cases → P1.
- **Labeling / format drift**: P2.

#### Step 3: [LLM] Produce the case dashboard

Render a status dashboard (from `templates/case-dashboard.template.md`): status distribution, risk-flag list, pending-decision list, and recommended actions for human reviewers. The dashboard surfaces what a human needs to decide; it does **not** decide.

#### Step 4: [Deterministic] Human confirmation

Pause. A human reviewer acts on the flagged cases. This skill never emits the approval/rejection decision.

## Hard Rules

1. **Review-only.** Never modify supplier documents or case files. Output structured findings; hands-off after delivery.
2. **No contract conclusions.** Never draft contract clauses, pricing, or the admission/sourcing decision. Structure and flag; the human decides.
3. **Identity is anchored to the official registration.** The business license / official registration is authoritative for legal name and USCC; every other document must agree with it.
4. **P0 blocks readiness / decision-readiness.** A package with a P0 is not admission-ready; a case with a P0 needs human attention before any decision.
5. **Deadline integrity.** Every readiness flag carries the source document's submission deadline; a case past its deadline is reported as expired, never as pending.
6. **No fabricated content.** Recommended fixes must reference an existing supplied document.
7. **Deterministic checks are the baseline.** `scripts/check_material_package.py` owns the numbers; the LLM layer explains and extends, never overrides a deterministic result.

## Failure Handling

| Scenario | Action |
|---|---|
| No supplier inputs provided (Mode A) | Stop; at least one document is required |
| Document unreadable / non-text | Mark it and check only the readable ones |
| Manifest missing required fields | Ask for the missing field; do not guess identity |
| All checks pass | Report "package ready" / "no case risk found" |
| P0 found in an already-submitted package | Flag with extra severity; recommend resubmission |
| Cases provided without due dates | Compute stall only where dates exist; note coverage gap |

## Output Format

```text
<run-dir>/
├── (Mode A) 01-readiness-check.json   # deterministic script output
├── (Mode A) 02-material-package.md    # structured supplier package
├── (Mode A) 03-readiness-report.md    # P0/P1/P2 + actions
├── (Mode B) 01-cases-normalized.json
└── (Mode B) 02-case-dashboard.md
```

## Verification

- [ ] Every supplied document's legal name compared for identity consistency.
- [ ] Certificate expiry checked against a reference date; P0/P1 assigned correctly.
- [ ] Required-document completeness checked against the checklist.
- [ ] Financial inconsistencies flagged when figure divergence exceeds tolerance.
- [ ] No contract clause or admission decision appears in any output.
- [ ] Human confirmation documented before the task is marked complete.
- [ ] Each readiness flag states whether its source document's submission deadline is still open; an expired document is not counted as valid evidence of readiness.

## Pitfalls

- Treating a near-expiry certificate as fine — 90 days is the warning line, not a pass.
- Reconciling revenue by picking the "nicer" number — flag the divergence, let the supplier explain.
- Letting the dashboard imply a decision ("approve supplier X") — it surfaces, it does not decide.
- Assuming the product catalog's scope equals the declared business scope — mismatch is a real admission risk.
- Running Mode A on a single document and calling it "ready" — completeness needs the whole set.

---

## 中文摘要（Chinese Summary）

本 Skill 是**采购准入**的影子助手，只覆盖两个高重复、高摩擦的环节，且**不碰合同结论**：

- **供应商材料包就绪度审查**：给定供应商散落的资质材料（营业执照、资质证书、产品册、案例、财报摘要、合规材料），在提交准入评审前检查材料包是否**完整、内部一致**。
- **审批案件管理**：给定一批准入审批案件（每家供应商的请求 + 提交材料 + 评审人 + 阶段 + 截止日 + 结论），跟踪状态、卡点、缺口，供评审人行动。

**关键约束（双语要点 / Bilingual key points）：**

- **只审阅不决策 Review-only, no decision**：绝不撰写合同条款，绝不下准入/采购结论；只结构化、标记，责任留在采购委员会/采购方。
- **身份锚定官方登记 Identity anchored to registration**：营业执照/官方登记的名称与统一社会信用代码为权威；其他材料必须与之对齐。
- **P0 阻断就绪 P0 blocks readiness**：材料包有 P0 即未就绪；案件有 P0 须人工介入方可决策。
- **确定件检查是基线 Deterministic baseline**：`scripts/check_material_package.py` 负责数字与一致性，LLM 层只解释与扩展，不推翻确定件结论。
- **不编造 No fabrication**：修复建议必须引用已提交材料，不得凭空生成。

**何时用（场景引导 / When to reach for it）：** 供应商准备准入/入库材料包、想提交前过一遍就绪度；你收到供应商材料想快速判断名称/证书/数字是否跨文档一致；你管一批准入审批案件想要状态看板（卡在哪、缺什么、谁该决策）；想给评审人/委员会一份可一键审阅的报告。它专门抓"名字对不上、证书快过期、数字前后矛盾、案件超时无结论"这类问题。
