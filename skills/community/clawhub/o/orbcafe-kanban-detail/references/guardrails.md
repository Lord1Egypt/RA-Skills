# Kanban + Detail Guardrails

## Board constraints

- Prefer controlled state via `useKanbanBoard`; otherwise drag will appear to work and then snap back.
- `bucket.id` and `card.id` must be stable and unique.
- Empty buckets still need to render through `CKanbanBoard`; do not short-circuit them away.

## Card / bucket constraints

- Keep visual customization in `CKanbanBucket` / `CKanbanCard`, not in ad-hoc wrappers, so styling stays consistent.
- Use `priority`, `progress`, `assignee`, `tags`, and `metrics` as optional enrichments; do not require all of them.

## Detail chaining constraints

- `onCardClick` belongs in a Client Component because it performs routing.
- If detail page should return to Kanban, pass `backHref` explicitly in the query string and consume it in the detail example.

## Tool constraints

- `moveKanbanCard` is pure; use it in reducers or optimistic updates.
- Do not mutate nested `model.buckets[].cards[]` arrays in place when using React state.
