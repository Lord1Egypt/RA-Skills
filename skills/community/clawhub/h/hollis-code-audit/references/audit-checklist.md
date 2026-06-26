# Code Audit Checklist

Load this only when the audit scope needs detailed prompts.

## Security and Privacy

- Protected routes require authentication.
- Authorization matches roles, tenants, project ownership, object scope, and unpublished/draft state.
- Path traversal, symlink traversal, archive extraction, reserved Windows names, and import-root bypasses are blocked.
- Upload parsing handles malformed, oversized, encrypted, nested, and unsupported files safely.
- Secrets are not logged, committed, returned by APIs, rendered in UI, or sent to external models.
- Network egress and LLM calls obey allowlists, admin settings, and redaction rules.
- Audit logs capture security-relevant changes without leaking sensitive payloads.

## Correctness and Data Integrity

- Writes are transactional where partial failure would corrupt state.
- Migrations/schema setup are compatible with supported deployments.
- State transitions cannot skip review, approval, publication, or provenance steps.
- Retries and duplicate submissions do not duplicate records, facts, jobs, or notifications.
- Derived facts trace back to evidence and are invalidated when sources change.
- Timezone, date parsing, currency, decimal precision, and locale assumptions are explicit.

## API and Integration Contracts

- Request validation rejects bad types, missing fields, long fields, and invalid enum values.
- Pagination, filters, sorting, and search behave for empty and large datasets.
- Error responses are stable and do not reveal internals.
- External dependency failures degrade predictably.
- Backward compatibility is preserved unless a breaking change was requested.

## Frontend and UX Risk

- Role-restricted UI actions have server-side enforcement.
- Empty, loading, error, slow-network, and permission-denied states are handled.
- UI state does not expose stale or unauthorized data after navigation, role changes, or failed saves.
- Forms prevent accidental destructive actions and preserve user edits on recoverable errors.

## Edge Cases

- Empty database, no configured settings, no search results.
- Very large inputs, many files, long paths, deep directories, mixed encodings.
- Malformed JSON/CSV/XLSX/PDF/DOCX/images.
- Concurrent requests, interrupted jobs, retries after timeout.
- Expired sessions, revoked tokens, role downgrade while a page is open.
- Cross-project or cross-tenant IDs, deleted objects, unpublished/draft objects.
- Offline mode, disabled network, blocked model provider, provider timeout.
- Midnight/month-end/year-end/leap-day/DST/timezone conversion.
- Database lock, disk full, missing archive file.
- Generated/vendor/demo/runtime files accidentally included in review scope.
