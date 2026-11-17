# Production-plan, sample, and revision gates

## Initial approval sequence

1. Resolve configuration and EXIF-order sources.
2. Complete every rich `production_brief` and the project `sample_style_contract`.
3. Build `render-plan.json` and the mandatory `production-plan.md`.
4. Render only the first EXIF page, record and validate its renderer receipt, normalize its clean plate, compose it deterministically, and register the plate, composed sample, and receipt.
5. Communicate the plan decisions and discuss them together with the sample.
6. Record the discussion mode and evidence.
7. Copy the user's exact explicit approval into the gate.
8. Render only pages 2..N from the batch scope.

The Markdown file must always exist. It need not always be sent as a file: `mark-shown` accepts either `artifact` or `faithful-summary`, but both modes require confirmation that the plan decisions were communicated and the sample was discussed.

```bash
python3 bin/review_gate.py register-sample \
  --state work/approval-state.json \
  --sample-plate work/sample/01-plate.png \
  --sample work/sample/01.png \
  --renderer-record work/sample-renderer-receipt.json

python3 bin/review_gate.py mark-shown \
  --state work/approval-state.json \
  --presentation-mode faithful-summary \
  --discussion-note 'All page decisions and the sample were reviewed in chat' \
  --plan-decisions-communicated \
  --sample-discussed \
  --decision-coverage ordered-page-briefs \
  --decision-coverage sample-style-contract \
  --decision-coverage sample-scope \
  --decision-coverage finish-qa-delivery

python3 bin/review_gate.py approve \
  --state work/approval-state.json \
  --approval-text '<exact user message>' \
  --explicit-user-approval
```

The gate locks the resolved config, render plan, Markdown plan, approved reference image/metadata hashes, normalized sample plate, composed sample, validated renderer receipt, and structured sample style contract. The receipt records model/version/seed/settings and source/reference/output hashes; a `not-configured` receipt is an explicit blocker. For an external renderer, permission to store a private reference locally remains separate from explicit, service-scoped permission to transmit it. The generated sample is never a style reference.

## What is not approval

Silence, reactions, unrelated feedback, partial plan approval, partial sample approval, or a request to revise are not batch permission.

## Post-approval revision decision rule

Use a typed page-local revision only when all changes concern approved non-sample pages and do not change style, references, sources, order, shared composition/system rules, or the sample style contract.

```json
{
  "changes": [
    {"page": 4, "domain": "page-content", "operation": "retain_but_simplify", "target": "major roads", "instruction": "keep fewer, wider directional lines"},
    {"page": 3, "domain": "page-content", "operation": "add_as_secondary", "target": "trees", "instruction": "frame the glass facade without competing with it"},
    {"page": 2, "domain": "page-content", "operation": "preserve_unchanged", "target": "courtyard depth", "instruction": "do not flatten the surrounding context"}
  ]
}
```

Each change also has a structured `domain`. Only `page-content` and `page-overlay` are local. `sample`, `style-reference`, `shared-system`, and `source-order` automatically invalidate the batch gate even if the caller mistakenly asks for a local impact.

Operations are literal:

- `remove`: delete only the named target.
- `retain_but_simplify`: keep the target while reducing detail or quantity.
- `add_as_secondary`: add without displacing the established primary hierarchy.
- `preserve_unchanged`: lock the named target against collateral changes.

Create the scope with `revision_scope.py`. It records the exact request, marks only actionable pages stale, hash-locks unchanged approved pages, and emits only affected pages.

If the revision touches the first/sample page, style/reference, source, order, shared layout, or system plan, `revision_scope.py` invalidates batch approval and returns to the plan+sample gate. Do not force a local scope.
