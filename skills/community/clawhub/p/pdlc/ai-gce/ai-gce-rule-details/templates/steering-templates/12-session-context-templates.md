<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Session & Context Management Steering Templates

> **Purpose:** Used by the project-init-agent to generate session governance and context management
> steering files in the target project's `rules/` folder. These templates encode AI-DLC v1
> methodology rules, session discipline, context hygiene, and never-vibe-code enforcement
> derived from `session-governance.md` and the built-in AI-DLC v1 methodology baseline.

---

## session-governance.md (Always)

**Generates**: `rules/session-governance.md`
**Derived From**: session-governance.md + built-in AI-DLC v1 methodology baseline

```markdown
---
inclusion: always
---

# Session Governance

## Never Vibe Code
- NEVER edit AI-generated code directly during an AI-DLC v1 session
- All fixes flow: identify root cause → fix in {spec_docs_location} → regenerate
- Exception: production hotfixes (must be back-propagated within {hotfix_backprop_window})

## Session Discipline
- {session_scope_rule}: {session_scope_description}
- {session_planning_requirement}
- {session_completion_criteria}
- Commit {spec_docs_location} artifacts after every session
- Update {state_file} before ending

## Context Management
- Always front-load domain constraints in the initial prompt
- Reference existing files explicitly — AI cannot infer what it cannot see
- Keep steering files lean — they consume context in every session
- {context_budget_awareness}

## Question Answering
- Use {answer_format} for every AI-DLC v1 question
- Quantify constraints (volume, limits, thresholds)
- Reference related modules and integration points explicitly

## Session Types
{for_each_session_type}
- {session_type_name}: {session_type_description}
  - Scope: {session_type_scope}
  - Deliverable: {session_type_deliverable}
  - Gate: {session_type_gate}
{end_for_each}
```

---

## context-loading.md (FileMatch `{spec_docs_pattern}`)

**Generates**: `rules/context-loading.md`
**Condition**: Generated IF project has spec documentation structure
**Derived From**: session-governance.md + project structure

```markdown
---
inclusion: fileMatch
fileMatchPattern: "{spec_docs_pattern}"
---

# Context Loading Rules

## Spec-First Development
- EVERY code change MUST have a corresponding spec ({spec_format})
- Spec MUST be approved BEFORE implementation begins
- {spec_to_code_traceability}

## File Loading Order
- When starting a session on {module_name}:
  1. Load {primary_context_files}
  2. Load {module_specific_context}
  3. Load {cross_cutting_context}
- NEVER proceed without confirming context is loaded

## Context Budget
- Maximum always-inclusion steering: {max_always_lines} lines total
- {context_overflow_strategy}
- Priority order for context trimming: {context_priority_order}
```

---

## role-isolation.md (Always)

**Generates**: `rules/role-isolation.md`
**Derived From**: role-isolation.md + CODEOWNERS + TEAM_AGREEMENTS.md

```markdown
---
inclusion: always
---

# Role Isolation & Segregation of Duties

## Roles
{for_each_role}
- {role_name}: {role_description}
  - Permissions: {role_permissions}
  - Restrictions: {role_restrictions}
{end_for_each}

## Segregation Rules
- {author_approver_rule}
- {role_escalation_rules}
- ALL role violations MUST be logged as security events
- {override_authority}

## Code Ownership
- {code_ownership_enforcement}
- {cross_module_review_requirement}
- {ownership_change_process}
```
