## Workflow

1. Clarify the listing intent and selector using only non-secret details:
   listing title, category, price, description text, image readiness, and
   whether the target is all ads, new ads, changed ads, due ads, or specific ad
   IDs.
2. Run `kleinanzeigen_status` first when checking installation, plugin config,
   runtime availability, or supported miniclaw commands.
3. Run `kleinanzeigen_verify` before any account-changing operation when
   practical.
4. For publish, update, delete, download, or extend, summarize the exact
   non-secret action, scope, and live listing impact, then wait for explicit
   user confirmation.
5. If the Kleinanzeigen plugin tools are unavailable, stop and tell the user the
   `kleinclaw` OpenClaw plugin is required.
6. Call the matching optional plugin tool only after confirmation:
   `kleinanzeigen_publish`, `kleinanzeigen_update`, `kleinanzeigen_delete`,
   `kleinanzeigen_download`, or `kleinanzeigen_extend`.
7. Report only the sanitized result returned by the tool. If the result has
   `needsUserAction`, tell the user to handle the account step outside chat in
   a terminal/browser, then retry `kleinanzeigen_status` or
   `kleinanzeigen_verify`. If the result says configuration or credentials need
   attention, ask the user to fix that outside the chat and rerun verification.
