<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Merge Strategy — Applying Changes While Preserving Customizations

## Purpose

Defines how AI-DWG applies approved changes to workspace files without destroying team customizations. The core principle: AP-sourced content is updated; team-added content is preserved untouched.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Treat team-added content as sacred — anything outside `<!-- begin/end: AP-sourced -->` markers is untouchable by reconciliation
- Present conflicts transparently — when team edited inside AP markers, show both versions and let the user decide
- Think about merge as a conversation, not an overwrite — propose changes, user approves; never auto-apply removals
- Maintain provenance marker integrity — they are the contract that enables all future reconciliation
- Consider ordering stability — don't reorder sections; maintain the generation sequence to minimize confusion

### Anti-Patterns for This Activity
- Do NOT auto-resolve conflicts — present both versions (AP-derived vs. team-modified) and let the user pick
- Do NOT silently delete AP-sourced sections that are no longer justified — always ask for confirmation
- Do NOT break, nest, or duplicate provenance marker pairs — they are the structural integrity of the reconciliation system

### Quality Check
A good output from this activity sounds like:
- "Conflict detected in security-rules.md AUTH-02: AP says 10min, team changed to 30min, new AP says 10min. Options: (a) Use AP, (b) Keep team's, (c) Edit manually."
- "Merge complete: 3 additions applied (within markers), 1 modification approved, 1 removal confirmed by user. Team-added sections preserved untouched."

---

## The Merge Model

```
┌──────────────────────────────────────────────────────────────┐
│  STEERING FILE ANATOMY                                        │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  <!-- AI-DWG generated | source: {AP} | date: {date} -->      │  ← Provenance header
│                                                                │
│  # File Title                                                  │
│                                                                │
│  <!-- begin: AP-sourced -->                                    │  ← AP section START
│  {Content derived from Architecture Package}                   │  ← CAN be updated by reconciliation
│  {Rules, tables, patterns}                                     │
│  <!-- end: AP-sourced -->                                      │  ← AP section END
│                                                                │
│  ## Team Additions                                             │  ← Team content
│  {Content added by the team after generation}                  │  ← NEVER touched by reconciliation
│  {Custom rules, notes, extensions}                             │
│                                                                │
│  <!-- begin: AP-sourced -->                                    │  ← Another AP section
│  {More AP-derived content}                                     │
│  <!-- end: AP-sourced -->                                      │
│                                                                │
│  {More team content...}                                        │  ← NEVER touched
│                                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## Merge Rules

| # | Rule | Description |
|---|------|-------------|
| 1 | **AP-sourced sections are mutable** | Content between `<!-- begin: AP-sourced -->` and `<!-- end: AP-sourced -->` can be updated |
| 2 | **Everything else is immutable** | Content outside AP markers is team-owned — NEVER modify, move, or delete |
| 3 | **Additions are safe** | Adding new AP-sourced sections at the end of a file is always allowed |
| 4 | **Modifications require review** | Changing existing AP-sourced content is proposed, not auto-applied |
| 5 | **Removals require confirmation** | Removing AP-sourced sections requires explicit user approval |
| 6 | **No markers = fully team-owned** | If a file has no provenance markers, treat it as 100% team content — append only |
| 7 | **Marker integrity** | Never break, nest, or duplicate marker pairs |
| 8 | **Order preserved** | Don't reorder sections — maintain the sequence from original generation |

---

## Merge Scenarios

### Scenario A: Content Addition (Low Risk)

AP now contains something new that wasn't there before (new principle, new rule, new module).

**Action:**
1. Identify the correct section in the steering file
2. Add new content within the appropriate `<!-- begin/end: AP-sourced -->` block
3. If no appropriate block exists → add new block at logical position
4. Present to user: "Adding: {description}"

**Example:**
```
Architecture Vision added Principle P8: "Observability-First"
→ Add P8 row to workspace-rules.md Principles table (within AP-sourced markers)
→ Add P8 section to architecture-principles.md (within AP-sourced markers)
→ Derive new golden rule from P8
```

---

### Scenario B: Content Modification (Medium Risk)

AP content changed (principle reworded, technology version bumped, rule threshold updated).

**Action:**
1. Identify the AP-sourced section containing the changed content
2. Show BOTH versions (current vs. proposed)
3. User approves → replace within markers
4. User rejects → keep current

**Presentation format:**
```
📝 MODIFICATION PROPOSED

File: rules/api-standards.md
Section: Rate Limiting (API-RATE-02)

Current:  "Global limit: 1000 req/min per tenant"
Proposed: "Global limit: 2000 req/min per tenant"
Source:   API Architecture (Rate Limiting section updated)

Apply? [Yes / No / Edit manually]
```

---

### Scenario C: Content Removal (High Risk)

AP no longer contains something that was previously there (principle removed, module deleted, constraint lifted).

**Action:**
1. Identify the AP-sourced section that's no longer justified
2. Flag prominently — removals are significant
3. NEVER auto-remove — always ask
4. If user confirms → remove the AP-sourced section (preserve surrounding team content)
5. If user declines → keep it; add comment: `<!-- retained by team despite AP removal -->`

**Presentation format:**
```
⚠️ REMOVAL PROPOSED

File: rules/workspace-rules.md
Section: Constraint C4 (within AP-sourced Constraints section)

Current:  "DO NOT use cloud services — on-premises only"
Reason:   This constraint no longer appears in Architecture Vision Constraints table
Impact:   Removes a restriction — more technology options become available

Remove? [Yes / No / Keep with note]
```

---

### Scenario D: Structural Change (High Risk)

A new conditional file needs to be generated, or an existing conditional file is no longer justified.

**Action for new file:**
1. Explain why: "{trigger} is now met because AP added {content}"
2. Propose generating the file
3. User approves → generate using appropriate mapping rules

**Action for file removal:**
1. Explain why: "{trigger} is no longer met because AP removed {content}"
2. Propose removing or archiving the file
3. NEVER auto-delete — user confirms
4. If user keeps it → mark as team-maintained: update provenance header

---

### Scenario E: Conflict (Team Edited AP Section)

Team modified content inside AP-sourced markers (technically breaking the contract — but it happens).

**Detection:** Content between markers doesn't match what the PREVIOUS AP would have generated.

**Action:**
1. Present both versions: AP-derived (new) vs. team-modified (current)
2. Options:
   - (a) Use AP version (overwrite team edit)
   - (b) Keep team version (ignore AP update)
   - (c) Merge manually (user provides combined version)
3. Recommend: if team intentionally deviated, move their content OUTSIDE markers (make it team-owned)

**Presentation format:**
```
⚡ CONFLICT DETECTED

File: rules/security-rules.md
Section: AUTH-02 (within AP-sourced Authentication Rules)

AP says:      "Access tokens MUST expire after 15 minutes"
Team changed: "Access tokens MUST expire after 30 minutes"
New AP says:  "Access tokens MUST expire after 10 minutes"

Options:
(a) Use new AP value (10 minutes)
(b) Keep team's value (30 minutes)
(c) I'll edit manually

💡 Suggestion: If your team intentionally chose 30min, move this rule 
   outside AP markers to protect it from future reconciliation.
```

---

## Merge Process (Step by Step)

```
FOR EACH affected file:
  1. Read current file content
  2. Identify all AP-sourced sections (via markers)
  3. Identify all team-added content (everything else)
  4. For each AP-sourced section:
     a. Generate what the NEW AP would produce for this section
     b. Compare against current AP-sourced content
     c. If different → record change (ADD/MODIFY/REMOVE)
     d. Check for conflicts (team edited inside markers)
  5. Compile change list for this file
  6. Present to user (per approval mode: all-at-once or per-file)
  7. Apply approved changes:
     - Replace AP-sourced section content with new content
     - Preserve all team content exactly as-is
     - Maintain section order
  8. Update provenance header date
```

---

## Approval Modes

When presenting changes, user chose one of:

| Mode | Behavior |
|------|----------|
| **(a) Apply all** | Apply every proposed change without individual review — trust the diff |
| **(b) Review each** | Present each change individually — user approves/rejects per change |
| **(c) Skip** | Apply nothing — user handles manually |

For mode (b), group by file and present in file order.

---

## Post-Merge Actions

After approved changes are applied:

1. **Update provenance header date** — `<!-- AI-DWG generated | source: {AP} | date: {NEW date} -->`
2. **Log reconciliation** — record what changed, why, and what was approved/rejected (see provenance-tracking.md)
3. **Validate consistency** — run V3 (consistency check) on affected files
4. **Signal downstream** — notify AI-GCE if steering files changed (see downstream-signaling.md)

---

## Key Principles

1. **Non-destructive by default** — when in doubt, preserve; never silently delete
2. **Team content is sacred** — anything outside AP markers is untouchable
3. **User always decides on removals** — AI proposes, human disposes
4. **Conflicts are presented, not auto-resolved** — user picks the winner
5. **Provenance markers are the contract** — maintain them; they enable all reconciliation
6. **Small, focused diffs** — show the minimum context needed to understand each change
