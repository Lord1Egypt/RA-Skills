<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 12: Product Documentation

**Phase:** Stakeholders & Communication
**Purpose:** Establish governance for product-facing documentation — release notes, changelogs, and (optionally) PRDs/feature briefs — so stakeholders know what was built, customers know what changed, and marketing can communicate.

---

## Purpose

AI-DLC v1 produces implementation docs (specs, tests, code docs). AI-POLC governs product-facing documentation: the external/stakeholder record. Without it, stakeholders don't know what was built; customers don't know what changed; marketing can't communicate new capabilities.

---

## Depth Adaptation

| Depth | Behavior |
|-------|----------|
| **Minimal** | Release notes template + changelog governance rules. |
| **Standard** | Release notes + changelog + communication template for stakeholders. |
| **Comprehensive** | Full documentation governance: PRD templates, feature briefs, product wiki, API change communication. Extension: Full Product Docs. |

---

## Steps

### Step 12.1: Define Release Notes Governance

Every release needs a customer/stakeholder-facing summary of what changed:

**Release Notes Template:**
```markdown
# Release {version} — {date}

## What's New
- {Feature 1}: {one-line user-facing description}
- {Feature 2}: {one-line user-facing description}

## Improvements
- {Improvement 1}: {what changed and why it matters}

## Bug Fixes
- {Fix 1}: {what was wrong and what's now correct}

## Known Issues
- {Issue 1}: {description + workaround if available}

## Breaking Changes (if any)
- {Change}: {what was before → what is now → migration path}
```

**Governance rules:**
- Release notes are written by the PO (or delegated with PO review)
- Written in user language, not developer language
- One release note per release (not per sprint)
- Published at release time, not after

### Step 12.2: Define Changelog Governance

The changelog is the running historical record:

**Format:** Follow [Keep a Changelog](https://keepachangelog.com/) convention:
- Added, Changed, Deprecated, Removed, Fixed, Security

**Governance rules:**
- Updated per sprint/iteration (append new entries at top)
- Each entry links to the epic or story it relates to (traceability)
- Version numbering follows semantic versioning (if applicable)

### Step 12.3: Context-Adapted Documentation

| Context Factor | Documentation Adaptation |
|---|---|
| Market = B2C | Release notes critical (users see them); simple language |
| Market = B2B | Contractual change notices; formal impact assessment |
| Market = Internal | Lighter; focus on "what can you now do?" |
| Compliance = Heavy | Change documentation mandatory; audit trail required |
| Stakeholder Density = High | Multiple communication formats (exec summary + detailed) |

### Step 12.4: Persist Documentation Governance

Write `release-notes-governance.md` with:
- Release notes template
- Changelog format and update rules
- Ownership (who writes, who reviews, who publishes)
- Timing (when relative to release)
- Distribution (where published, who receives)

---

## Extension: Full Product Docs

If triggered ("PRD" / "feature brief"), load `extensions/full-product-docs.md` and additionally produce:
- PRD template (problem, solution, scope, success metrics, timeline)
- Feature brief template (for communicating upcoming work to stakeholders)
- Product wiki governance (structure, ownership, update cadence)
- API change communication template (for developer-facing products)

---

## Gate

**Gate 12 — Documentation Governance Confirmed:**

Present to user:
```
Product documentation governance established:
• Release notes: template defined, ownership assigned
• Changelog: format and update rules defined
• Communication: adapted to {market type} context

Approve to proceed to PBP Assembly (final phase before handoff).
```

User must confirm. This is also the **Phase 4 gate** — Stakeholders complete.

---

## Transition

→ **Phase 5, Stage 13: PBP Assembly & Handoff** (Assembly begins)

---

*Detail file for AI-POLC Stage 12 | Phase: Stakeholders & Communication*
