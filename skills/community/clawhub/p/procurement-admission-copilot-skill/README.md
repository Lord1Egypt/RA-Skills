# Procurement Admission Copilot

> Shadow-mode, review-only copilot for the two repeatable, high-friction parts of B2B supplier / vendor procurement admission: supplier material-package readiness, and approval-case management. It structures and flags — it never drafts contract terms or makes the admission decision.


---

## What it does

- **Supplier material package readiness** — given a supplier's scattered qualification inputs (business license, certificates, product catalog, case studies, financials summary, compliance docs), check the package is complete and internally consistent before submission.
- **Approval case management** — given a set of admission approval cases (each a supplier's request with materials, reviewer, stage, due date, decision), track status, stalls, and gaps so a human reviewer can act.

## When to use

- A supplier is preparing the document package for procurement admission / vendor onboarding and wants a readiness pass before submission.
- You receive a supplier's materials and need to know, fast, whether company identity, certificates, and figures are consistent across documents.
- You manage a queue of admission approval cases and need a status dashboard: what is stalled, what is blocked by missing documents, what needs a decision.

## When not to use

- Drafting contract terms, pricing, or the admission/sourcing conclusion → out of scope by design.
- A single-document fact-check of an article → `claim-to-source-auditor`.
- Supplier negotiation or scorecard ranking → this skill tracks and flags, it does not rank or decide.
- Directly modifying supplier documents.

## Hard rules (key)

- Review-only: never modify supplier documents or case files; hands-off after delivery.
- No contract conclusions: never draft contract clauses or the admission decision; the human decides.
- Identity anchored to the official registration (business license / USCC is authoritative).
- P0 blocks readiness / decision-readiness.
- Deterministic checks (`scripts/check_material_package.py`) own the numbers; the LLM layer explains, never overrides.

## File structure

```
procurement-admission-copilot/
├── SKILL.md
├── SKILL_zh.md
├── README.md
├── README_zh.md
├── _meta.json
├── references/
│   └── qualification-checklist.md
├── scripts/
│   └── check_material_package.py
└── templates/
    ├── supplier-material-package.md
    ├── readiness-report.template.md
    └── case-dashboard.template.md
```

## License

MIT
