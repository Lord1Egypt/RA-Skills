# 📋 Multi-Agent UX Audit Pipeline (Tasks Example)

This file demonstrates how to orchestrate a thorough, multi-agent `/product-ux-audit` pipeline. 

> [!IMPORTANT]
> **Core Concept:** To achieve maximum depth and avoid confirmation bias, the codebase is split into distinct **User Flows** or **Module Scopes**. Instead of a human doing this, the LLM agent itself should scan the repository first, identify these scopes, and generate this task list.
> 
> The pipeline executes two independent runs (`runA` and `runB`) for each scope using fresh agent contexts (no shared memory), merges their findings to keep the highest severity, and compiles everything into a master audit report.

---

## 🛠️ Execution Strategy & Rules (CRITICAL — read before starting)

### Phase 1: Parallel Auditing (Subagents)
- **Run in parallel:** Spawn and run ALL `runA` and `runB` subagent tasks (e.g., `01a` to `04b` below) concurrently in a single batch.
- **Subagent Role:** Each subagent operates in an isolated context, reads its scope-specific files, runs the `/product-ux-audit` skill, and writes its final report (e.g., `FINAL.md`).

### Phase 2: Pipelined Merging (Orchestrator)
- **Do not wait for all subagents:** As soon as both `runA` and `runB` for a single scope are completed, the orchestrator must immediately merge them into `MERGED.md`.
- **Merge logically:** Combine shared findings (keep the higher severity of the two), and keep unique findings marked as `[Run A only]` or `[Run B only]`.
- **Do not delegate merges:** Merging requires comparing two files and context; the orchestrator should do this directly instead of delegating to a subagent.

### Phase 3: Final Cross-Scope Merge (Orchestrator)
- **Deduplicate and group:** Once all `MERGED.md` files are ready, the orchestrator reads them all, performs cross-scope deduplication, and compiles the master report (e.g., `AUDIT_FINAL.md`).
- **Include ALL findings:** 
  - **CRITICAL & HIGH:** Each must include its file path, line number (`file:line`), and a detailed description.
  - **MEDIUM & LOW:** Group these as bulleted lists organized by scope. Do not omit any findings.
- **Cross-Scope Deduplication:** If the exact same issue pattern occurs across multiple scopes, combine them into a single `CRITICAL` or `HIGH` finding and list all affected files/scopes.
- **Sort by severity:** Order the consolidated findings strictly from `CRITICAL` ➔ `HIGH` ➔ `MEDIUM` ➔ `LOW`.
- **Do not delegate the final merge:** This requires full repository context of all scopes, which only the orchestrator possesses.

### Progress & Context Rules
- **Progress Log:** After completing each task (subagent run or merge), append a line in `00_PROGRESS.md`:
  `[Task ID] | [Scope Name] | CRITICAL: X | HIGH: Y | MEDIUM: Z | DONE`
- **Context Preservation:** Do not output the entire contents of generated `FINAL.md` or `MERGED.md` reports into the chat context. Only confirm the generated file path and proceed to the next task to prevent token limit issues.
- **Directory Isolation:** Create a separate subfolder for each task scope (e.g., `01_auth-onboarding/runA/`, `01_auth-onboarding/runB/`).

### Why the Orchestrator Handles Merges Directly
- **Merge (2 inputs):** The orchestrator processes this faster than spinning up a new subagent.
- **Final (N inputs):** Cross-scope deduplication requires full context of all scopes — only the orchestrator has this.

### Prompt Template for Subagents
For each `runA`/`runB` task, instruct the subagent:
`"/product-ux-audit. Scope: [scope name]. App: [app tag]. Relevant files (read these first, then discover more via skill's pre-flight if needed): [file list]. READ-ONLY. Save all phase reports + FINAL to: [output path]. Focus: find UX gaps, logic issues, edge cases in this scope only. Severity: CRITICAL=user-blocking / HIGH=likely issue / MEDIUM=gap / LOW=doc gap."`

---

## 🎯 Example Pipeline Tasks

*Replace these placeholders with the actual flows identified by the LLM during the initial project scan.*

### Output Directory
`Output path: C:\Users\Username\Desktop\_Reports\product-audit_run1\`

### Checklist

- [ ] **01a_auth-onboarding** | App: `web-client` | Files: `src/app/(auth)/*`, `src/api/auth.ts` ➔ `01_auth-onboarding/runA/`
- [ ] **01b_auth-onboarding** | (Same scope as 01a) ➔ `01_auth-onboarding/runB/`
- [ ] **01m_auth-onboarding-merge** | Merge 01a and 01b ➔ `01_auth-onboarding/MERGED.md`

- [ ] **02a_core-feed** | App: `web-client` | Files: `src/components/Feed/*`, `src/hooks/useFeed.ts` ➔ `02_core-feed/runA/`
- [ ] **02b_core-feed** | (Same scope as 02a) ➔ `02_core-feed/runB/`
- [ ] **02m_core-feed-merge** | Merge 02a and 02b ➔ `02_core-feed/MERGED.md`

- [ ] **03a_checkout-billing** | App: `web-client` | Files: `src/app/checkout/*`, `src/api/stripe/*` ➔ `03_checkout-billing/runA/`
- [ ] **03b_checkout-billing** | (Same scope as 03a) ➔ `03_checkout-billing/runB/`
- [ ] **03m_checkout-billing-merge** | Merge 03a and 03b ➔ `03_checkout-billing/MERGED.md`

- [ ] **04a_admin-panel** | App: `admin-dashboard` | Files: `src/app/admin/*` ➔ `04_admin-panel/runA/`
- [ ] **04b_admin-panel** | (Same scope as 04a) ➔ `04_admin-panel/runB/`
- [ ] **04m_admin-panel-merge** | Merge 04a and 04b ➔ `04_admin-panel/MERGED.md`

- [ ] **99_final-merge** | Consolidate and sort all `MERGED.md` findings ➔ `AUDIT_FINAL.md`
