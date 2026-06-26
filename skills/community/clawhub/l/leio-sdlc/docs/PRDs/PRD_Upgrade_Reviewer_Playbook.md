---
Affected_Projects: [leio-sdlc]
status: closed
---

# PRD: Upgrade_Reviewer_Playbook

## 1. Context & Problem (业务背景与核心痛点)
Currently, the `leio-sdlc` Reviewer agent uses a free-form text format in the "Details" and "Action Items" sections of the `Review_Report.md`. This lack of structure causes the Coder to sometimes miss specific fixes or misunderstand the exact line/file where the error occurred. The Boss requested merging the highly structured "7 Key Focus Areas" and JSON-like Findings array from the IADF-ADE Code Review Agent. However, natively injecting JSON output would break the Orchestrator's Regex parsing and hundreds of E2E tests. We need a "Zero-Blast-Radius" upgrade to enforce structure via Markdown instead of modifying the Python parsing logic.

## 2. Requirements & User Stories (需求定义)
- The Reviewer must evaluate code against 7 Key Focus Areas (Plan Alignment, Correctness, Test Coverage, Readability, Architecture, Efficiency, Security).
- The Reviewer must output feedback in a rigid, highly structured Markdown list format that mimics the strictness of a JSON array (including File path, Line approximation, Category, Severity, Issue description, and Recommendation).
- The Orchestrator Python regex logic and all existing E2E tests MUST NOT break. The top-level `{"status": "..."}` JSON block must remain intact at the top of the report.

## 3. Architecture & Technical Strategy (架构设计与技术路线)
**Technical Strategy:** Zero-Blast-Radius Template Update.
We will NOT modify any python scripts (`orchestrator.py`).
Instead, we will target two static configuration files:
1. `TEMPLATES/Review_Report.md.template`: Replace the vague `## Details` section with a highly structured `## Structured Findings` markdown template that enforces the `<Severity> | <Category> | <File> | <Issue> | <Recommendation>` syntax.
2. `playbooks/reviewer_playbook.md`: Inject the "7 Key Focus Areas" text directly into the reviewer's system prompt instructions.

## 4. Acceptance Criteria (BDD 黑盒验收标准)

- **Scenario 1:** Generating the new Review Report format
  - **Given** the new `Review_Report.md.template` and `reviewer_playbook.md` are deployed
  - **When** the Reviewer agent generates a review
  - **Then** the report must contain the exact `## Structured Findings` headers and the 7 Key Focus Areas, while keeping the `{"status": "APPROVED|ACTION_REQUIRED"}` JSON block safely at the top.

- **Scenario 2:** Ensuring SDLC backward compatibility
  - **Given** the modified templates
  - **When** running the SDLC preflight script (`./preflight.sh`)
  - **Then** all 60+ tests, including `test_orchestrator_cli.py` and `test_triad_reviewer.sh`, must pass without modification.

## 5. Overall Test Strategy & Quality Goal (测试策略与质量目标)
- **Core Quality Risk:** The regex parser in `orchestrator.py` failing to find the JSON status block because of template changes.
- **Testing Approach:** This is a pure template/prompt change. The existing E2E and Unit test suite in `./preflight.sh` is already designed to catch regex/parsing failures. The Coder merely needs to update the templates and run the existing test suite. No new tests are strictly required, but the Coder MUST verify 100% test pass rate.

## 6. Framework Modifications (框架防篡改声明)
- `TEMPLATES/Review_Report.md.template`
- `playbooks/reviewer_playbook.md`
- *(STRICTLY FORBIDDEN: Modifying `scripts/orchestrator.py` or `tests/*` for this PRD).*

---

## Appendix: Architecture Evolution Trace (架构演进与审查追踪)
> **[CRITICAL INSTRUCTION FOR PLANNER & CODER]** 
> IGNORING THIS SECTION IS MANDATORY. This section is strictly for historical tracking of the PM-Auditor-Boss discussion loop. Do NOT read, reference, or implement any logic from this appendix into the SDLC pipeline.

- **v1.0**: Initial draft to implement Zero-Blast-Radius reviewer prompt injection.