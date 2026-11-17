<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 15: AI-DWG / AI-GCE Handoff

## Purpose

Package the design system, tokens, component standards, and accessibility baseline for consumption by AI-DWG (workspace generation) and AI-GCE (compliance enforcement). This handoff turns UX design decisions into enforceable development standards.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During this stage, layer the Workspace Architect lens on top of the UX Designer primary:

**Behavioral Shifts:**
- Think about how design decisions translate into steering files and compliance rules
- Ensure token format is machine-parseable (not just human-readable)
- Map design system concepts to the workspace structure AI-DWG generates
- Consider what AI-GCE can enforce automatically vs. what requires human judgment

**Anti-Patterns for This Stage:**
- DO NOT hand off aspirational guidelines — hand off enforceable specifications
- DO NOT expect AI-DWG to interpret design intent — give it explicit token values and rules
- DO NOT duplicate what AI-DWG already generates from AP — only ADD the UX layer
- DO NOT hand off subjective criteria as compliance rules (e.g., "looks good" is not enforceable)

**Quality Check:**
- [ ] Token specification is in a parseable, structured format
- [ ] Every handoff item maps to a specific AI-DWG or AI-GCE output
- [ ] Enforceable rules are distinct from aspirational guidelines
- [ ] Handoff is ADDITIVE to what AI-DWG already produces from AP

---

## Steps

### Step 1: Package for AI-DWG

AI-DWG generates steering files for the development workspace. AI-UXD's handoff ADDS to what AI-DWG already derives from the Architecture Package:

```markdown
## AI-DWG Handoff: Design System → Steering

### New Steering File: `design-system.md`
AI-DWG generates this new steering file from the UXP:

Content source:
- Design principles → Section 1 (principles that affect code decisions)
- Token specification → Section 2 (all tokens in consumable format)
- Component inventory → Section 3 (component names, where they live, how to extend)
- Responsive rules → Section 4 (breakpoints, grid, reflow expectations)

### Enrichment to: `frontend-standards.md`
AI-DWG already generates `frontend-standards.md` from AP. UXP ADDS:
- Component state requirements (all states must be implemented)
- Interaction patterns (keyboard, hover, focus behavior specifications)
- Voice & tone integration (copy patterns for frontend components)
- Icon usage rules

### Enrichment to: `coding-standards.md`
UXP ADDS:
- Token usage enforcement (reference tokens, never hardcode values)
- Component composition rules (atoms → molecules → organisms hierarchy)
- Accessibility coding patterns (ARIA, focus management, live regions)

### New File: `design-tokens.json` (or equivalent)
Machine-readable token export:
- All tiers (global, semantic, component)
- W3C Design Tokens Format aligned
- Ready for Style Dictionary / Tokens Studio consumption
```

### Step 2: Package for AI-GCE

AI-GCE derives compliance rules and hooks. AI-UXD's handoff enables new enforcement:

```markdown
## AI-GCE Handoff: Accessibility + Design → Compliance

### New Rule Category: `accessibility-compliance`
AI-GCE generates this from the accessibility baseline (Stage 11):
- Contrast ratio rules (enforceable via color token values)
- Keyboard accessibility rules (every interactive component)
- ARIA requirements (per component type)
- Focus management rules
- Motion accessibility (prefers-reduced-motion respect)

### New Rule Category: `design-system-compliance`
AI-GCE generates this from the design system (Stage 8-9):
- Token usage enforcement (no hardcoded color/spacing values)
- Component state completeness (all states implemented)
- Responsive behavior compliance (breakpoint handling)
- Content/copy patterns (error messages follow format)

### Potential Hooks (for AI-GCE to generate)
| Hook | Trigger | Checks |
|------|---------|--------|
| `design-token-check` | fileEdited (UI files) | No hardcoded values; tokens referenced |
| `accessibility-check` | fileEdited (component files) | ARIA present; keyboard handler exists |
| `component-state-check` | fileCreated (new component) | All required states defined |
```

### Step 3: Define What's Enforceable vs. Advisory

Not everything in the design system can be automatically enforced. Clarify:

| Category | Enforceable (AI-GCE can check) | Advisory (human judgment) |
|----------|-------------------------------|--------------------------|
| Color | Token usage; contrast ratio | Color appropriateness for context |
| Typography | Token usage; hierarchy | Readability in context |
| Spacing | Token usage; minimum values | Visual balance |
| Components | State presence; ARIA; keyboard | Interaction feel |
| Voice & tone | Format patterns (error structure) | Tone appropriateness |
| Accessibility | Contrast; ARIA; focus; keyboard | Cognitive load; clarity |
| Layout | Grid alignment; breakpoint handling | Visual hierarchy effectiveness |

### Step 4: Produce Handoff Documents

Produce two handoff packages:

**For AI-DWG:**
```markdown
## AI-DWG Consumption Contract

### Files I Produce That You Consume:
1. `07_Design_System/*.md` → generates `design-system.md` steering
2. `07_Design_System/Design_Tokens.md` → generates `design-tokens.json`
3. `08_Component_Library/Component_Inventory.md` → enriches `frontend-standards.md`
4. Responsive/Grid spec → enriches `frontend-standards.md`

### Detection:
AI-DWG detects UXP by scanning for `uxd-state.md` marker.
If found: load design system and generate/enrich the above steering files.
If not found: generate `frontend-standards.md` from AP only (current behavior unchanged).

### The UXP is ADDITIVE — never replaces what AI-DWG derives from AP.
```

**For AI-GCE:**
```markdown
## AI-GCE Consumption Contract

### Files I Produce That You Consume:
1. `10_Accessibility_Baseline.md` → derives `accessibility-compliance` rules
2. `07_Design_System/Design_Tokens.md` → derives `design-system-compliance` rules
3. `08_Component_Library/Component_Inventory.md` → derives component state enforcement

### Detection:
AI-GCE detects UXP by scanning for `uxd-state.md` marker.
If found: derive accessibility + design system compliance rules.
If not found: skip these rule categories (no UXP = no design enforcement).

### Enforceable rules only — never derive subjective judgment as a compliance check.
```

### Step 5: Update State File

Update `uxd-state.md`:
- Downstream Signals → AI-DWG: "Handed Off"
- Downstream Signals → AI-GCE: "Handed Off"

### Step 6: Present for Approval

Present:
- What AI-DWG receives and what it generates from it
- What AI-GCE receives and what rules it derives
- Enforceable vs. advisory distinction
- Consumption contracts (clear enough for downstream packages?)

---

## Gate

**Approval required before proceeding to Stage 16.**

User must confirm:
- Handoff contracts are clear for both consumers
- Token format is consumable
- Enforceable vs. advisory distinction is correct
- ADDITIVE nature is clear (doesn't replace existing AI-DWG/GCE behavior)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 15 with date
- Downstream Signals: AI-DWG = "Handed Off", AI-GCE = "Handed Off"
- Current Stage: 16

---

## Transition

After gate approval:
```
Stage 15 complete. Design system and accessibility baseline handed
off to AI-DWG and AI-GCE.

Moving to Stage 16: Package Assembly. I'll now assemble the complete
UX Design Package with a reading guide and final state update.
```

Load `assemble/package-assembly.md`.
