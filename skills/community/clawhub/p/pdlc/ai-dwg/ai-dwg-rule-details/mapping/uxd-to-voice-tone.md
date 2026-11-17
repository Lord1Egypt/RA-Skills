<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → content-guidelines.md (UXD CLUSTER)

## Purpose

Transforms the **voice & tone guidelines** produced by AI-UXD (`design/design-system-foundation.md` → voice & tone section, or a dedicated voice-tone artefact) into a prescriptive `content-guidelines.md` steering file. This governs all user-facing copy — labels, microcopy, error messages, empty states, notifications — so AI-DLC v1 writes interface text in the product's designed voice instead of generic developer phrasing.

**Output:** `rules/content-guidelines.md`

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains voice & tone guidelines.

**Cluster:** UX — belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — UX Designer

During THIS activity, ALSO adopt the mindset of a **UX Designer** (brand/content lens). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Microcopy is interface, not decoration — error and empty-state text are designed surfaces
- Voice is consistent; tone flexes by context (error vs success vs onboarding) — preserve both axes
- Examples are the spec — the do/don't pairs are the most enforceable part; carry them verbatim
- Terminology consistency is governance — the approved/avoid word list is a hard rule

### Anti-Patterns for This Activity
- Do NOT rewrite the UXP's example copy in your own words
- Do NOT drop the "avoid" list — what NOT to say is as binding as what to say
- Do NOT generalize tone into "be friendly" — keep the contextual tone matrix

---

## Source Inputs

**Primary source:** AI-UXD → UXP, via `uxd-state.md` marker.

| UXP Document | What to Extract | Maps to Section |
|---|---|---|
| Voice & Tone guidelines | Voice attributes, tone-by-context matrix | Voice & Tone |
| Microcopy patterns | Button labels, errors, empty states, confirmations, notifications | Microcopy Rules |
| Terminology / glossary | Approved terms, terms to avoid, capitalization | Terminology Rules |
| Localization notes (if present) | Tone constraints across locales | Cross-ref to `i18n-standards.md` |

---

## Target Structure: content-guidelines.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — design-system-foundation (voice & tone)"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-UXD Voice & Tone | date: {generation-date} -->

# Content & Microcopy Guidelines

## Voice & Tone
<!-- begin: UXP-sourced -->
**Voice (constant):** {attributes — e.g. clear, confident, human}

| Context | Tone | Example |
|---------|------|---------|
| Error | {tone} | "{example copy}" |
| Success | {tone} | "{example copy}" |
| Onboarding | {tone} | "{example copy}" |
<!-- end: UXP-sourced -->

## Microcopy Rules
| Rule ID | Surface | Rule | Do | Don't |
|---------|---------|------|----|----|
| CNT-01 | Buttons | Use verb-first action labels | "Save changes" | "OK" |
| CNT-02 | Errors | State cause + recovery | "Email already in use — try signing in" | "Error 409" |
| CNT-03 | Empty states | Explain + offer next action | … | … |

## Terminology Rules
| Rule ID | Use | Avoid | Note |
|---------|-----|-------|------|
| CNT-TERM-01 | {approved term} | {avoid term} | {capitalization / usage} |

## Localization Note
- If `i18n-standards.md` is generated, tone constraints per locale are honored there.
```

---

## Transformation Rules

### Rule 1: Example Copy Is VERBATIM
Do/don't example pairs are copied exactly — they are the operative spec.

### Rule 2: Voice Constant, Tone Contextual
Preserve both: one voice, multiple tones by context. Do not collapse into a single adjective.

### Rule 3: Terminology List Is Binding
Approved/avoid terms become MUST-use / MUST-NOT-use rules.

### Rule 4: Prescriptive Microcopy
Each microcopy rule pairs a Do with a Don't and a target surface — not abstract advice.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-design-system.md` | `design-system.md` identity header carries a 1-line brand-voice summary; full voice rules live here. |
| `uxd-to-i18n.md` | Localization tone constraints reconcile with i18n rules. |
| `uxd-to-information-architecture.md` | Nav labels must obey terminology rules here. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP present, no voice & tone section | Skip; flag: "UXP defines no voice & tone — content guidelines not generated" |
| Voice defined but no examples | Carry voice/tone matrix; mark examples `<!-- UXP gave no example copy -->` |
| Backend-only project | Skip (no user-facing copy) |
| Voice conflicts with marketing brand voice | Out of DWG scope — note for product owner; do not reconcile here |

---

## Output Validation

- [ ] Do/don't example copy verbatim
- [ ] Voice (constant) + tone (contextual matrix) both present
- [ ] Terminology rules are MUST/MUST-NOT
- [ ] Microcopy rules pair Do + Don't + surface
- [ ] Provenance front-matter + projectId present
