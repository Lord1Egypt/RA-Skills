# Bases and review views

Use Bases or equivalent review lists as the control plane for curation.

Views that group by `topic` depend on consistent topic slugs. Use the `topic` rule in `references/status-schema.md` before creating or changing topic-based views.

## Recommended views

### Vault Inbox
Show notes missing `status` or `doc_kind`.

### Needs Review
Show notes where:

- `status = needs-review`, or
- `review_state = conflict`

### Canonical Pages
Show notes where:

- `canonical = true`

group by `topic`.

### Historical but linked
Show notes where:

- `status = historical`
- and the note still has meaningful inbound links

### Concept / future state
Show notes where:

- `status = concept`

### Reactivatable
Show notes where:

- `status = reactivatable`

### Supersession gaps
Show notes where:

- `status = historical`
- and `superseded_by` is empty

### Stale current docs
Show notes where:

- `status = current`
- and `last_verified` is older than 90 days or missing

### Research not integrated
Show notes where:

- `doc_kind = research`
- and no canonical page links to them

## Practical guidance

- Keep the first dashboard small and obvious.
- Start with visibility, not automation.
- Prefer a handful of high-signal views over a huge taxonomy.
- If Bases is not available, propose manual indexes or search-driven lists as equivalent queues.
