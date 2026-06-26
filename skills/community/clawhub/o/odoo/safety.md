# Odoo Safety Ladder

Use this file for any task that could change business state, financial truth, or inventory traceability.

## Preview

- Identify target model, record count, required filters, and fields to change.
- Show a sample set of records or a dry-run summary before a write or import.
- Call out side effects: followers, activities, recomputations, stock reservations, taxes, or accounting entries.

## Protect

- Define who must confirm and what rollback path exists.
- For bulk imports, keep the source file reviewable and versioned.
- For accounting and stock operations, preserve an auditable correction path.
- For automations, define trigger, frequency, idempotency, and failure handling before enabling them.

## Apply

- Use the smallest reversible action first.
- Prefer batch segmentation for large changes by date, warehouse, company, or external ID.
- Re-check counts and a sample of resulting records immediately after the change.
- Record the incident or new safe default if the task revealed a repeatable risk.

## Hard Stops

- No `unlink` on live business data without explicit confirmation and a recovery story.
- No direct edits to posted accounting, closed periods, or finalized stock history as a casual shortcut.
- No mass import without deduplication keys or clear update-vs-create rules.
- No direct database writes unless the user is intentionally doing backend repair and accepts the blast radius.

## Safer Alternatives

| Risky request | Safer move |
|---------------|------------|
| "Just rewrite the invoice" | reverse, credit, or correct through supported accounting flow |
| "Delete the stock moves" | return, scrap, or inventory adjustment with traceability |
| "Upload this CSV and see what happens" | dry-run on staging or review key mappings first |
| "Fix all customers at once" | preview duplicates and batch by rule |
