<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Drift Intake Digest — AI-UXD (UX Domain)

## Purpose

Defines how AI-UXD **receives, digests, and resolves** drift routed to the UX domain. AI-UXD implements the `drift-intake@1.0` interface (see `contracts/DRIFT_INTAKE_CONTRACT.md`); this file carries ONLY the UX-specific decision logic. The interface shape, authority matrix, and communication model are the contract's — not repeated here.

**Domain owned:** `ux` (design tokens, design system, components/UI patterns, accessibility baseline, information architecture & navigation) — from the `driftRouting` table AI-FLO owns.

**Grounding:** `contracts/DRIFT_INTAKE_CONTRACT.md` (`drift-intake@1.0`) + `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §7 under the baseline-brokered pull model (INV-L4-006).

---

## MANDATORY: Sub-Role — Brand Designer / Audit Specialist (as the drift dictates)

Digest under the UX Designer primary + the sub-role matching the drifted element: `#persona-subrole-brand-designer` (design system / tokens / theming), `#persona-subrole-audit-specialist` (accessibility baseline), `#persona-subrole-ux-designer` (IA / navigation / flows). ADDS a lens — never replaces the primary.

### Anti-Patterns
- Do NOT write the drift register or the baseline — disposition goes to UXD's OWN artifacts, then DWG re-baselines (INV-L4-006).
- Do NOT read FLO's routing-log — learn of drift ONLY by querying FLO (address) + reading GCE's register.
- Do NOT hardcode "ux is mine" — ask FLO; it returns only what belongs to AI-UXD.
- Do NOT Waive an accessibility-baseline drift casually — accessibility is non-negotiable (Rule 4); a Waive here needs an owner, a short expiry, and an explicit risk note.

---

## Step 1 — Pull (Contract §3, Direction 1)

```
1. Ask AI-FLO: "Any drift for AI-UXD?"
2. FLO returns ADDRESS(es) only: { driftId, address: "<register>#DRF-NNN" }
3. FOR EACH address: read the drift body DIRECTLY from GCE's register (READ-ONLY):
     driftId · elementId · classification · domainTag · evidence · baselineVersion · elementDescription
4. Confirm domainTag == ux (sanity — FLO already resolved ownership)
```

No push arrives; UXD pulls. The body is read from GCE, never relayed by FLO.

---

## Step 2 — Digest: UX-Domain Decision Guidance

Map the drifted element to its UX intent, then choose ONE disposition. Guidance by element type:

| Drifted element (`domainTag: ux`) | Source of truth (UXP) | Decision lens |
|-----------------------------------|------------------------|---------------|
| `design-token` | design system / design tokens (W3C) | Did the token taxonomy/value deliberately evolve, or did the implementation hardcode off-token values? |
| `component` / UI pattern | component inventory (states/ARIA/responsive) | Is the component variation an intended addition, or an off-system one-off? |
| `accessibility` | accessibility baseline (WCAG target + POUR) | Did the a11y target change (rare), or did the build fall below the approved baseline? |
| `navigation` / IA | information architecture, user flows | Did the IA/nav model change, or did the implementation diverge from the approved structure? |
| `theming` (multi-brand) | multi-brand token spec | Is the theme/brand variation adopted, or accidental? |

### Choosing the disposition (authority per contract §5)

- **Conform** — the approved design system / baseline is still correct; the implementation must match the tokens / components / a11y baseline. UXD records the expectation; no design-system change. *Low ceremony.*
- **Amend** — the design intent genuinely evolved. Update the source UXP artifact (design tokens, component inventory, IA, or theming spec), then let DWG re-baseline. *High ceremony — a design-system change is a decision; gate/approval required.*
- **Waive** — a tolerated legacy-component or transitional exception, with a named owner and mandatory future expiry. *Highest ceremony — time-boxed; auto-reopens. For `accessibility` elements, a Waive additionally requires an explicit risk note (Rule 4).*

> Accessibility drift defaults toward **Conform** (bring the build up to the baseline). Amend an accessibility baseline only when the WCAG target itself is deliberately re-set — a rare, gated decision.

---

## Step 3 — Emit (Contract §4.3–4.5)

Write the disposition to AI-UXD's OWN artifacts, then signal readiness:

| Disposition | UXD writes (own artifacts) | Then |
|-------------|-----------------------------|------|
| Conform | Note the restore expectation against the token/component/baseline (element unchanged) | emit `digest-ready` (type: conform) |
| Amend | Update the design system / design tokens / component inventory / IA / theming spec + note the change in `uxd-state.md` | emit `digest-ready` (type: amend, `changedElement` + rationale) |
| Waive | Record the waiver (owner + future expiry + scope [+ a11y risk note]) in `uxd-state.md` | emit `digest-ready` (type: waive, owner+expiry+scope) |

```yaml
digest-ready:                 # in uxd-state.md (UXD's own state)
  - driftId: DRF-021
    dispositionType: amend
    outputAddress: "uxd-state.md#DRF-021"   # where DWG reads the disposition payload
    readyAt: {ISO}
```

DWG later pulls this via FLO (Contract §3, Direction 2), reads the payload from `outputAddress`, and bakes it into baseline `vN+1`. GCE then reads `vN+1` and closes the register entry. **AI-UXD never writes the register or the baseline.**

---

## Step 4 — Examples

**Example A — `design-token` drift → Conform.**
`DRF-021`: components use hardcoded `#3366FF` instead of the `color.primary` token, with no decision to change the palette. → **Conform**: the token stands; record the restore expectation; emit `digest-ready(conform)`. DWG carries a ledger entry (design system unchanged); GCE re-measures vs the token and closes when the hardcode is replaced.

**Example B — `component` drift → Amend.**
`DRF-024`: the build introduces a new "toast" component variant the team decides to adopt system-wide. → **Amend**: add the variant (states/ARIA/responsive) to the component inventory, note it in `uxd-state.md`; emit `digest-ready(amend)`. DWG re-baselines; the new governed element matches reality; GCE closes.

**Example C — `accessibility` drift → Conform (default).**
`DRF-027`: a form field lacks a label / fails the WCAG AA target in the baseline. → **Conform** (a11y is non-negotiable, Rule 4): the baseline stands; record the restore expectation; emit `digest-ready(conform)`. GCE re-measures against the baseline and closes when the field is fixed. A Waive here would require an owner, a short expiry, and an explicit risk note.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `contracts/DRIFT_INTAKE_CONTRACT.md` | The `drift-intake@1.0` interface + authority matrix this file implements |
| (AI-FLO `route/drift-routing.md`) | Answers UXD's inbox query with drift addresses; polls UXD's `digest-ready` for DWG |
| (AI-GCE `drift/drift-register.md`) | The register UXD reads (read-only) for the drift body; GCE closes entries from the baseline |
| (AI-DWG `reconciliation/re-baseline.md`) | Pulls UXD's disposition via FLO; bakes into `vN+1` |
| `design/design-system-foundation.md` · `design/component-library.md` · `define/information-architecture.md` · `validate/accessibility-baseline.md` | The UXP artifacts an Amend updates |

---

## Output Validation

- [ ] Drift pulled by querying FLO (address) + reading GCE register (read-only) — never scanned/pushed
- [ ] Disposition written to UXD's OWN artifacts (design system / tokens / components / `uxd-state.md`) — never the register or baseline
- [ ] Accessibility drift defaults to Conform; a Waive carries owner + short expiry + explicit risk note (Rule 4)
- [ ] Waivers carry named owner + mandatory future expiry
- [ ] `digest-ready` signal emitted in `uxd-state.md` with `driftId` + `dispositionType` + `outputAddress`
- [ ] No read of FLO's routing-log; drift state learned only from GCE register + own digest
