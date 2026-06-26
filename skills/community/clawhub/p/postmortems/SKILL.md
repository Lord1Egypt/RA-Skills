---
name: postmortems
description: Deep blameless postmortem workflow—timeline, impact, root cause vs contributing factors, what went well/poorly, action items with owners, and follow-through. Use after incidents, outages, or near-misses to improve reliability culture.
---

# Postmortems (Deep Workflow)

A good postmortem **learns** without **blaming individuals**. It produces **owned** **actions** that **reduce recurrence** or **improve detection**—not a generic “we will communicate better.”

## When to Offer This Workflow

**Trigger conditions:**

- **SEV** incidents, customer-visible outages, data loss scares
- **Near-miss** worth documenting (luck prevented impact)
- **Blame** culture risk—need **facilitation** structure

**Initial offer:**

Use **six stages**: (1) scope & audience, (2) timeline & impact, (3) root cause analysis, (4) what worked / didn’t, (5) action items, (6) communication & follow-up). Confirm **internal-only** vs **customer-facing** summary.

---

## Stage 1: Scope & Audience

**Goal:** **Readers** (exec, eng, CS) and **sensitivity** (PII, security details redacted).

### Practices

- **Blameless** framing in invite and template

**Exit condition:** Template chosen; owner for final doc.

---

## Stage 2: Timeline & Impact

**Goal:** **Minute-resolution** timeline with **UTC**; **detection** vs **start** vs **mitigation** vs **resolution**.

### Impact

- **Users** affected, **duration**, **data** **integrity** if relevant, **SLA** **breach**

**Exit condition:** **Customer** **communication** **aligned** **with** **facts** **here**.

---

## Stage 3: Root Cause Analysis

**Goal:** **Five whys** or **fishbone** as **tool**, not **ritual**—**root** **cause** **and** **contributing** **factors** **separate**.

### Practices

- **Root**: **fix** **that** **stops** **recurrence** **class** **(with** **evidence)**
- **Contributors**: **process**, **missing** **tests**, **alert** **gaps**

**Exit condition:** **No** **single** **person** **named** **as** **“root** **cause.”**

---

## Stage 4: What Worked / Didn’t

**Goal:** **Reinforce** **good** **(runbooks,** **heroes** **who** **followed** **process)** **and** **fix** **bad** **(missing** **dashboards).**

---

## Stage 5: Action Items

**Goal:** **Specific**, **tracked** **tickets** **with** **owners** **and** **dates**; **types**: **prevent**, **detect**, **recover**, **process**.

### Practices

- **Avoid** **vague** **“add** **monitoring”** **without** **metric** **names**

**Exit condition:** **Action** **items** **in** **issue** **tracker** **linked**.

---

## Stage 6: Communication & Follow-Up

**Goal:** **Share** **summary** **with** **org**; **review** **completion** **in** **30/60** **days**.

### Practices

- **External** **postmortem** **if** **customer** **promise** **requires**

---

## Final Review Checklist

- [ ] Blameless tone; facts and timeline clear
- [ ] Impact quantified where possible
- [ ] Root cause and contributing factors distinguished
- [ ] Action items owned, dated, and tracked
- [ ] Follow-up review scheduled

## Tips for Effective Guidance

- **Severity** **should** **match** **depth** **of** **postmortem** **(lightweight** **for** **small** **incidents).**
- **Link** **to** **metrics** **and** **traces** **in** **appendix** **for** **engineers.**
- **Psychological** **safety** **enables** **honesty**—**leadership** **must** **model** **it.**

## Handling Deviations

- **Security** **incident**: **coordinate** **with** **legal** **before** **public** **detail**.
- **Repeated** **same** **failure**: **escalate** **to** **architecture** **or** **SLO** **review**.
