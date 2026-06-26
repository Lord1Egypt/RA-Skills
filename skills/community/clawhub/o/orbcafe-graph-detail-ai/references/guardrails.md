# Graph + Detail + Agent Guardrails

## Graph constraints

- `CGraphReport` requires `open`, `onClose`, `model`, `tableContent`.
- Use interactive filtering only when filter state wiring is present.
- Map provider keys (Google/AMap) must stay in business app config, not hardcoded in UI layer.

## Detail constraints

- `CDetailInfoPage` requires `title` and `sections`.
- Search should target `sections/tabs` field label/value/searchableText.
- `ai.onSubmit` may return Markdown string; keep rendering deterministic.

## Agent settings constraints

- `CCustomizeAgent` requires `open`, `onClose`, `value`.
- `onSaveAll` should persist both setting values and selected template IDs in one transaction.
- Do not leak API keys into logs or client-visible debug panels.

## Cross-module constraints

- Prefer table-integrated graph entry for list pages.
- Use standalone `CGraphReport` only when open/close and model need external orchestration.
