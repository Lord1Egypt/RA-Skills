<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Diff Strategy — Detecting What Changed in the Architecture Package

## Purpose

Defines how AI-DWG identifies what changed in the Architecture Package when operating in Mode 2 (Delta Reconciliation). The diff determines which workspace files need updating.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think of diff as architecture change detection — every AP modification cascades through the mapping rules to specific workspace files
- Classify changes by risk and reversibility — additions are safe, modifications need review, removals are potentially destructive
- Only diff AP-sourced sections — team content is invisible to the diff process and preserved unconditionally
- Trace every change back to its AP source — provenance markers are the boundary that defines what's diffable
- Consider cascading impacts — a changed ADR may ripple through multiple steering files via different mapping rules

### Anti-Patterns for This Activity
- Do NOT diff or propose changes to team-added content (anything outside AP markers) — it's sacred
- Do NOT auto-remove anything — all removals require explicit user confirmation
- Do NOT assume a "minor" change is low-risk — a single token expiry value change can require code modifications across the system

### Quality Check
A good output from this activity sounds like:
- "API Architecture changed → affects: api-standards.md (API-RATE-02 value change), error-handling.md (error format section), .github/pull_request_template.md (API checklist item)."
- "Change classified: MODIFY (medium risk) — API-RATE-02 global limit 1000→2000 req/min. Source: API Architecture rate limiting section updated."

---

## Trigger Scenarios

| Scenario | User Says | AI-DWG Response |
|----------|-----------|-----------------|
| Specific artifact changed | "I updated the API Architecture" / points to file | Read THAT file + compare against current steering |
| Specific ADR added/changed | "New ADR-005 changes the auth model" | Read ADR + identify affected steering files |
| Multiple changes | "Architecture changed — reconcile" / "Multiple updates" | Full AP re-read + diff against all steering files |
| Principle changed | "We added a new principle" / "P3 was updated" | Read Architecture Vision + diff workspace-rules + architecture-principles |
| Module added/removed | "We split the incident module into two" | Read Component Design + diff module-structure + CODEOWNERS + folder structure |

---

## Diff Process

```
STEP 1: IDENTIFY THE CHANGE SOURCE
──────────────────────────────────
• User points to specific artifact(s) → read those
• User says "reconcile" (broad) → re-read full AP, compare adlc-state.md timestamps

STEP 2: MAP CHANGE TO AFFECTED WORKSPACE FILES
───────────────────────────────────────────────
Use the mapping rules (mapping/*.md) to determine which workspace files
are downstream of the changed AP artifact.

Example:
  API Architecture changed → affects:
    • rules/api-standards.md
    • rules/api-versioning.md (if exists)
    • rules/error-handling.md (error format section)
    • .github/pull_request_template.md (API checklist item)

STEP 3: COMPARE AP CONTENT VS. CURRENT STEERING
────────────────────────────────────────────────
For each affected steering file:
  • Read current steering file
  • Identify AP-sourced sections (via provenance markers)
  • Extract new content from updated AP artifact (using extraction rules from mapping files)
  • DIFF: old AP-sourced content vs. new AP-derived content
  • Identify: additions, modifications, removals

STEP 4: CLASSIFY CHANGES
─────────────────────────
Each detected change is classified:
```

---

## Change Classification

| Type | Description | Risk | User Action Needed |
|------|-------------|:----:|:------------------:|
| **ADD** | New content to add (new principle, new rule, new module) | Low | Inform |
| **MODIFY** | Existing content changed (rule updated, value changed) | Medium | Review |
| **REMOVE** | Content no longer justified by AP (rule, module, constraint removed) | High | Confirm |
| **STRUCTURAL** | File structure change (new conditional file needed, or conditional no longer justified) | High | Confirm |

---

## AP Artifact → Workspace File Mapping (Quick Reference)

When this AP artifact changes, check these workspace files:

| Changed AP Artifact | Affected Workspace Files |
|--------------------|-------------------------|
| Architecture Vision | `workspace-rules.md`, `architecture-principles.md`, `scope-and-risks.md` |
| Technology Stack | `tech-stack.md`, `.gitignore`, `docker-compose.yml`, `.editorconfig`, `coding-standards.md`, `naming-conventions.md` |
| System Context (C4 L1) | `scope-and-risks.md` |
| Container Diagram (C4 L2) | `module-structure.md` (high-level), `docker-compose.yml`, possibly `frontend-standards.md` trigger |
| Component Design (C4 L3) | `module-structure.md`, `domain-context.md`, `CODEOWNERS`, folder structure, `naming-conventions.md` |
| Security Architecture | `security-rules.md`, `observability-sensitive.md` |
| API Architecture | `api-standards.md`, `api-versioning.md`, `error-handling.md` (error format) |
| Data Architecture | `database-rules.md` |
| Multi-Tenancy Architecture | `multi-tenancy.md`, `database-rules.md` (scoping), `security-rules.md` (TENANT rules) |
| Integration Architecture | `resilience-standards.md` (if exists) |
| Infrastructure & Deployment | `git-workflow.md`, `docker-compose.yml`, `observability-*.md` |
| New ADR | Depends on ADR topic → relevant steering file(s) |
| adlc-state.md (extensions changed) | Extension-enriched files per enrichment mapping |

---

## Full Re-Read Diff (When "Reconcile Everything")

When user requests full reconciliation:

```
1. Read adlc-state.md → compare timestamps of completed stages
   • If any stage has newer timestamp than last reconciliation → that artifact changed

2. For each changed artifact:
   • Load mapping rule for that artifact
   • Extract content per extraction rules
   • Compare against current workspace file content (AP-sourced sections only)
   • Record all differences

3. Aggregate all changes into a single proposal
   • Group by workspace file
   • Classify each change (ADD/MODIFY/REMOVE/STRUCTURAL)
   • Present consolidated proposal to user
```

---

## Detecting New vs. Removed Conditional Files

| Situation | Detection | Action |
|-----------|-----------|--------|
| AP now justifies a conditional file that wasn't generated before | Re-evaluate conditional triggers against updated AP | Propose: "Generate new file: {name} because {trigger now met}" |
| AP no longer justifies a conditional file that exists | Re-evaluate triggers — condition no longer true | Propose: "Remove {file}? AP no longer contains {justification}" — user confirms |
| Extension activated since last generation | adlc-state.md shows new extension | Propose enrichment additions + any forced conditionals |
| Extension deactivated | adlc-state.md no longer lists extension | Propose: remove extension-specific content (user confirms) |

---

## Diff Output Format (Internal — Feeds into Proposal)

For each affected file, produce:

```
FILE: rules/{filename}
CHANGE TYPE: {ADD | MODIFY | REMOVE | STRUCTURAL}
SECTIONS AFFECTED:
  - Section: "{section name}"
    Type: {added | modified | removed}
    Current: "{brief summary of current content}"
    Proposed: "{brief summary of new content}"
    Source: "{AP artifact + section that drove the change}"
    Risk: {low | medium | high}
```

This internal diff feeds into the merge-strategy.md process (Step 4: Propose Changes).

---

## Key Rules

1. **Only diff AP-sourced sections** — team-added content is invisible to diff (preserved unconditionally)
2. **Provenance markers are the boundary** — content between `<!-- begin: AP-sourced -->` and `<!-- end: AP-sourced -->` is what gets compared
3. **If no provenance markers exist** (file was manually created or markers stripped) → treat entire file as team-owned; propose adding new AP content as addendum only
4. **Removals require explicit user confirmation** — never auto-remove
5. **Structural changes (new/removed files) flagged prominently** — higher visibility than content changes
6. **ADR changes cascade** — a changed ADR may affect multiple steering files; trace all downstream
