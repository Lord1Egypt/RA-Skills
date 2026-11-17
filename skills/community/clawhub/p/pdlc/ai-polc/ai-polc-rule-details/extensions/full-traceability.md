<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension: Full Traceability (Full Rules)

**Stage:** 10 (Traceability Spine)
**Adds:** Audit-grade matrix, compliance evidence, change impact, outcome tracking

---

## Additional Steps (replace minimal traceability in Stage 10)

### Step 10.E1: Build Audit-Grade Matrix

Full chain from intent to outcome:

| PIP Objective | Product Goal | Epic | Stories | AC Count | Release | Increment | Outcome | Status |
|---|---|---|---|:---:|---|---|---|:---:|
| Revenue +20% | Payment <2s | EPIC-001 | 3 stories | 12 | R1 | Sprint 3 | P95: 1.8s ✅ | Achieved |
| Revenue +20% | 3 Providers | EPIC-002 | 4 stories | 8 | R2 | — | — | Planned |

### Step 10.E2: Compliance Evidence Mapping

For regulated products, link regulatory requirements to AC:

| Regulation | Requirement | Epic | Specific AC | Evidence |
|---|---|---|---|---|
| PCI-DSS 3.4 | Encrypt cardholder data at rest | EPIC-006 | AC3: data encrypted AES-256 | Test report |
| GDPR Art.17 | Right to erasure | EPIC-008 | AC2: user can delete all data | Acceptance test |

### Step 10.E3: Change Impact Tracing

When a goal/requirement changes, trace the downstream impact:

```
CHANGE: Goal "Payment <2s" revised to "Payment <1s"
IMPACT:
├── EPIC-001: AC1 target changes (2s → 1s) — AFFECTED
├── EPIC-003: No change (abstraction layer is latency-agnostic)
├── Release R1: May need additional performance epic — RISK
└── DoD: Performance criterion needs updating — ACTION
```

### Step 10.E4: Outcome Tracking

After each release, record whether the traceability chain delivered value:

| Goal | Target Metric | Actual After Release | Gap | Action |
|------|---|---|---|---|
| Payment <2s | P95 < 2s | P95 = 1.8s | None ✅ | Continue |
| 10K MAU | 10,000 | 7,200 | -2,800 ⚠️ | Add growth epic to R3 |

---

## Additional Output

When this extension is active, `traceability-matrix.md` is the full audit-grade version with all columns populated. Additionally produces:
- Compliance evidence map (if regulated)
- Change impact template (for future changes)
- Outcome tracking table (populated during Operations)
