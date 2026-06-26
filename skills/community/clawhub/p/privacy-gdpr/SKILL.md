---
name: privacy-gdpr
description: Deep privacy/GDPR-oriented workflow—lawful basis, data inventory, minimization, DSAR process, DPIA triggers, subprocessors, and breach notification mindset. Use when designing data practices, vendor review, or user rights operations. Not legal advice.
---

# Privacy & GDPR (Deep Workflow)

This skill supports **structured thinking** about personal data. **Legal and compliance teams** must approve binding interpretations—this is **not** legal advice.

## When to Offer This Workflow

**Trigger conditions:**

- New collection of PII; analytics or ML on user data
- Vendor processing agreements; international transfers
- DSAR volume; breach response planning

**Initial offer:**

Use **six stages**: (1) scope & roles, (2) inventory & purposes, (3) lawful basis & notices, (4) rights & DSAR, (5) security & subprocessors, (6) DPIA & transfers). Confirm jurisdiction (EU/UK vs broader).

---

## Stage 1: Scope & Roles

**Goal:** Identify controller vs processor roles and whose data is involved (employees, customers, minors).

### Output

Simple RACI for privacy decisions.

**Exit condition:** Data subjects and systems in scope are listed.

---

## Stage 2: Inventory & Purposes

**Goal:** Record of processing activities (ROPA-style): what data, why, where stored, retention, who accesses.

### Practices

- Data minimization: collect and retain only what is needed

---

## Stage 3: Lawful Basis & Notices

**Goal:** Map processing to lawful basis (consent, contract, legitimate interests, etc.)—**lawyers validate** per jurisdiction.

### UX

- Consent granular and withdrawable where required

---

## Stage 4: Rights & DSAR

**Goal:** Operational playbook for access, erasure, portability, restriction—with SLAs and identity verification.

### Practices

- Log requests and responses for audit
- Plan how erasure interacts with backups and logs

---

## Stage 5: Security & Subprocessors

**Goal:** DPAs, SCCs or adequacy for transfers; subprocessor list public where required.

### Security

- Encryption, access controls, and logging aligned with risk

---

## Stage 6: DPIA & Transfers

**Goal:** Recognize when DPIA is likely required (high-risk processing)—escalate to DPO/legal.

### Transfers

- Document mechanisms for non-adequate countries

---

## Final Review Checklist

- [ ] Roles (controller/processor) and scope clear
- [ ] RoPA or equivalent inventory maintained
- [ ] Lawful basis and notices reviewed by legal where needed
- [ ] DSAR process with SLAs and verification
- [ ] Subprocessors and transfers documented

## Tips for Effective Guidance

- Engineering detail (backups, logs) is where GDPR meets reality.
- Privacy by design is cheaper than retrofit.
- Never invent legal conclusions—flag for professional review.

## Handling Deviations

- US-only: still map PII and consider state laws (e.g., CPRA).
- B2B vs B2C: different notice and rights patterns.
