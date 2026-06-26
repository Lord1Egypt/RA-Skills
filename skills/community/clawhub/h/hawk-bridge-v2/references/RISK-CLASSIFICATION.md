# Risk Classification v2

## Overview

Risk classification determines whether changes are auto-executed, flagged for review, or require a branch+PR flow.

## Risk Levels

### 🟢 Low Risk — Auto-Execute

**Characteristics:**
- No functional changes to code behavior
- Affects only documentation, comments, formatting
- No compatibility implications
- No user-facing changes

**Examples:**
- Fix typos in README or comments
- Update SKILL.md documentation
- Add/remove/fix code comments
- Lint fixes (format, import sorting)
- Add `.gitignore` entries
- Update changelog format
- Resolve TODO/FIXME annotations
- Extract duplicate string constants

**Action:** Auto-execute immediately, commit with prefix `auto:`, push to remote.

---

### 🟡 Medium Risk — Flag for Review

**Characteristics:**
- New features or enhancements
- Non-breaking additions
- Proactive optimizations found by scanner
- Changes to optional behavior
- Internal refactoring with preserved interfaces

**Examples:**
- Add new CLI command
- Add new optional flag to existing command
- Add new helper function
- Long function refactoring (>100 lines)
- Missing test coverage identified
- Enhance error messages
- Performance improvements

**Action:** Generate pending-review.json → User approves via `auto-evolve.py approve`

---

### 🔴 High Risk — Branch + PR Required

**Characteristics:**
- Breaking changes to existing interfaces
- Deletion of features
- Architectural changes
- Changes to core data models
- Changes affecting compatibility

**Examples:**
- Remove or rename existing CLI command
- Change API response format
- Delete existing configuration option
- Rename core functions/classes
- Change behavior of existing commands

**Action:** Create `auto-evolve/{description}` branch → commit → create GitHub PR

---

## Per-Repository Type Defaults

| Repo Type | Change Type | Default Risk |
|-----------|-------------|--------------|
| `skill` (public) | Code change | Medium |
| `skill` (public) | Doc change | Low |
| `norms` | Doc change | **Low** |
| `norms` | Code change | Medium |
| `project` | Test change | **Medium** |
| `project` | Doc change | Low |
| `closed` | Code change | **Medium** |
| `closed` | Doc change | Medium |

---

## Override Mechanism

Each repository can set `risk_override` to force a specific risk level:

```json
{
  "path": "~/my-conservative-repo",
  "type": "project",
  "risk_override": "low"
}
```

---

## Classification Algorithm

```
1. Get repo type and visibility
2. Apply type-based default risk
3. Check for high-risk patterns (remove, delete, deprecate, break...)
4. Check for low-risk patterns (README, SKILL.md, changelog...)
5. Apply risk_override if set
6. Return risk level
```
