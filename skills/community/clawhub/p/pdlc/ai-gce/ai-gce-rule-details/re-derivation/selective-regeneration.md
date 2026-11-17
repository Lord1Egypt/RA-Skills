<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Selective Regeneration — Re-Derivation Logic

## Purpose

Defines HOW AI-GCE regenerates ONLY the affected rules and hooks when steering files change, while preserving manual customizations. This is the execution step of Mode 2 after change detection.

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (Compliance Officer + Platform Engineer + AI-DLC v1 Engineer) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think in surgical precision: touch ONLY what's affected, leave everything else exactly as-is
- Preserve all custom markers (`<!-- custom -->` rules, `## Custom Instructions` in hooks) — team additions survive re-derivation
- Apply merge strategy correctly: re-derived content first, then preserved custom rules appended after separator
- Increment hook version on re-derivation (1.0.0 → 1.1.0) to signal that the hook changed
- Validate after regeneration: run V2 (traceability), V3 (consistency), V5 (hook integrity) on affected artifacts only

### Anti-Patterns for This Activity
- Do NOT overwrite custom-tagged rules during re-derivation (team additions are sacred)
- Do NOT touch unaffected rule files or hooks (selective means selective)
- Do NOT reset compliance tier, score, or lastAudit timestamp (re-derivation ≠ audit)

### Quality Check
A good output from this activity sounds like:
- "Selective regeneration complete: api-first-compliance.md re-derived (5 rules updated, 1 custom rule preserved). api-contract-check.json patterns unchanged (module paths didn't change). V2/V3/V5 validation PASS."
- "Hook version incremented: coverage-check.json 1.0.0 → 1.1.0. Prompt updated with new threshold (80% → 85% per updated testing-strategy.md). Custom Instructions section preserved."

---

## The Selective Update Principle

```
ONLY touch what's affected. Leave everything else exactly as-is.

Changed steering: api-standards.md
  → Re-derive: .governance/rules/api-first-compliance.md
  → Re-derive: .governance/hooks/api-contract-check.json (if patterns changed)
  → DO NOT TOUCH: security-compliance.md, naming-conventions.md, all other rules/hooks
```

---

## Step 1: Identify Sections to Update (Within Affected Files)

Each rule file has two types of content:

| Content Type | Marker | Re-Derivation Behavior |
|-------------|--------|------------------------|
| **Steering-derived** | No special marker (default) | RE-GENERATE from updated steering |
| **Manually customized** | `<!-- custom -->` tag on rule | PRESERVE — never overwrite |

### How to Detect Custom Rules

A rule added manually by the team after initial generation is marked:

```markdown
<!-- custom -->
### CUSTOM-SEC-99: Project-Specific Security Rule

This rule was added by the team for project-specific requirements.
Not derived from any steering file.
```

**Rule:** If a rule block starts with `<!-- custom -->`, it survives re-derivation unchanged.

---

## Step 2: Re-Generate Affected Rule Files

For each affected rule file:

1. **Read current file** — identify all custom-marked rules
2. **Extract custom rules** — store them temporarily
3. **Re-derive from updated steering** — generate fresh rules from the changed steering file using the appropriate generator (e.g., `generators/api-compliance-generator.md`)
4. **Merge custom rules back** — append custom rules after the re-derived content
5. **Write updated file** — preserving custom additions

### Merge Strategy

```
REGENERATED FILE = [
  Header (updated metadata + derivation date)
  + Re-derived rules (from updated steering)
  + Separator: "---\n## Custom Rules (Team-Added)\n"
  + Custom rules (preserved unchanged)
]
```

---

## Step 3: Re-Generate Affected Hooks

For hooks affected by the change:

### When to Update a Hook

| Change Type | Hook Update Needed |
|------------|:------------------:|
| Steering file content changed (new rules, modified thresholds) | ✅ Update prompt (rule IDs may change) |
| Module paths changed (module-structure.md) | ✅ Update `patterns` field |
| Technology changed (tech-stack.md) | ✅ Update `patterns` field (file extensions change) |
| Severity changed on a rule | ❌ Hook prompt doesn't embed severity (references rule file) |
| New conditional file appeared | ✅ Generate NEW hook (see change-detection.md) |

### What to Preserve in Hooks

| Hook Field | Re-Derive? |
|-----------|:----------:|
| `name` | Keep current (team may have renamed) |
| `version` | Increment minor version (1.0.0 → 1.1.0) |
| `description` | Re-derive from updated rules |
| `when.type` | Keep current (debounce tier is stable) |
| `when.patterns` | RE-DERIVE from updated module-structure/tech-stack |
| `then.type` | Keep current (always askAgent unless team changed to runCommand) |
| `then.prompt` | RE-DERIVE rule references + phase check; PRESERVE any team-added instructions marked with `## Custom Instructions` |

### Hook Prompt Custom Preservation

If a team added custom instructions to a hook prompt:

```json
{
  "then": {
    "prompt": "...standard AI-GCE prompt...\n\n## Custom Instructions\nAlso check for XYZ because our team decided..."
  }
}
```

The `## Custom Instructions` section is PRESERVED during re-derivation. Everything above it is re-generated.

---

## Step 4: Update Supporting Artifacts

After rule/hook regeneration, update:

| Artifact | What Changes |
|----------|-------------|
| `knowledge-map.md` (in docs/) | Updated source references for re-derived rules |
| `COMPLIANCE_README.md` | Updated rule list if categories added/removed |
| `ENFORCEMENT-GUIDE.md` | Updated if hooks added/removed/renamed |
| `.compliance-state.json` | Updated `lastAudit` field is NOT changed (re-derivation ≠ audit) |

---

## Step 5: Validate Regenerated Output

Run validation checks V2, V3, V5 from `common/validation-rules.md`:
- V2 (Traceability): All re-derived rules still trace to a source
- V3 (Consistency): Re-derived rules don't contradict preserved custom rules
- V5 (Hook Integrity): Updated patterns still match real filesystem

---

## What Selective Regeneration Does NOT Do

- ❌ Touch rule files that aren't affected by the change
- ❌ Overwrite custom rules (tagged `<!-- custom -->`)
- ❌ Overwrite custom hook instructions (tagged `## Custom Instructions`)
- ❌ Change hook event types (debounce tier is stable)
- ❌ Remove hooks (even if a conditional is removed — see change-detection.md for removal flow)
- ❌ Reset the compliance tier or score
- ❌ Re-run the audit (that's a separate action)
- ❌ Modify `.compliance-state.json` score fields (only audit updates scores)
