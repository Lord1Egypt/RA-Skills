# Household-aware Grocery

**Local surface only.** Grocery has no tools and no authorization scopes on the
remote hosted surface. If your tool list has no `heyfood_*` tools, none of this
applies — tell the user Grocery requires the local hey.food client rather than
attempting an equivalent with remote tools.

## Reads

Use `heyfood_get_grocery_list` when available. Preserve:

- list ID and version;
- stable item IDs;
- requested and canonical names;
- quantity, unit, state, and intended member;
- aggregate and per-member safety status;
- safety reasons, substitutions, and label guidance;
- context hash/version when present;
- source type, reference, and detail; and
- created/updated freshness.

Use `heyfood_get_grocery_exclusions` for the canonical never-buy list.

Never simplify `risky`, `avoid`, or `unable_to_evaluate` into “safe.”

## Requested changes

If the current tool list contains no Grocery prepare/cancel/confirm tools, say
that Grocery mutation is not supported through the agent integration. Hand the
user to the human TUI or documented human CLI without invoking it yourself.

If qualified mutation tools are present, preserve the exact proposal
presentation and use only the heyfood-controlled out-of-band approval flow.
Never expose or reconstruct the production proposal, confirmation token,
idempotency key, or commit credential.

Stale list version, household context, account, session, or approval state is
a rejection. Do not automatically prepare or commit a replacement.
