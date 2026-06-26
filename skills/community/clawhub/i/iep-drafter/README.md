# IEP Drafter

**Domain:** Special Education · IDEA Compliance
**Platforms:** Claude · Codex

## Purpose

Turns evaluation reports, present-levels evidence, and IEP-team inputs into a DRAFT Individualized Education Program aligned with IDEA 34 C.F.R. Part 300: Present Levels (PLAAFP), measurable annual goals, special-education and related services, supplementary aids and accommodations, assistive technology, state-assessment participation, Extended School Year consideration, Least Restrictive Environment justification, transition services where age-eligible, and an edit log. The output is always a DRAFT for IEP team review — never a final or signed IEP.

## When to Use

- Drafting an initial IEP after eligibility has been determined
- Drafting an annual review IEP from prior-IEP progress data and current evaluations
- Drafting a 3-year reevaluation IEP from a fresh comprehensive evaluation
- Drafting a transfer-in IEP from another LEA or state
- Drafting a transition IEP (age 16 or younger per state) with postsecondary goals and transition services
- Drafting an amendment for a single-element IEP change between annual reviews

## What It Does

1. Collects role, student reference (no direct identifiers), grade, IDEA disability category, IEP type, state, IEP team composition, and source documents through one-question-at-a-time intake
2. Builds an evidence-cited Present Levels (PLAAFP) across academic, communication, social/emotional, functional, motor, sensory, health, adaptive, and transition domains, and names prioritized needs from the data
3. Drafts measurable annual goals (six SMART-IEP elements) each traced to a PLAAFP-named need, with baselines, measurement methods, and parent-reporting cadence; adds short-term objectives or benchmarks when alternate assessment is selected
4. Drafts services (frequency / duration / location / start / end / source of need), transition content for age-eligible students, supplementary aids and accommodations, assistive technology, state-assessment participation, LRE narrative with rejected alternatives, ESY determination per goal, and behavior / FBA-BIP context
5. Runs a 12-item mass-IEP and compliance self-check (boilerplate scan, SMART-elements scan, citation scan, accommodation-alignment scan, identifier scan) and maintains an edit log per CIDDL ethical-use framework
6. Outputs the full IEP as a DRAFT with a verbatim IEP-team-review banner

## Notes

This skill produces a **DRAFT IEP**, not a final, signed, or filed document. IDEA requires an IEP team — including the parent, the LEA representative, the general education teacher, the special education teacher, and (when appropriate) the student — to determine eligibility, services, placement, and goals. The skill never drafts eligibility determinations, Prior Written Notice, or consent forms. The drafting agent is never listed as an IEP team member. Direct identifiers (full name, DOB, address, SSN, photo) must remain redacted in the working draft — the skill uses a non-identifying student code throughout.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
