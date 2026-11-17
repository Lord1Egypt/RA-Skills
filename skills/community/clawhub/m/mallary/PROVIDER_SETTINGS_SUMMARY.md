# Provider Settings - Read-Only Boundary Summary

This summary is not publishing guidance. Operational provider schemas and publishing syntax are intentionally omitted.

## Default

- remain in read-only discovery
- use only the minimum current profile and connection lookup needed
- minimize and redact profile IDs, account labels, and connection details
- do not infer publishing intent from a platform or provider question

```bash
mallary profiles list
mallary platforms list --profile-id <current-profile-id>
```

## After an Explicit User Request

An explicit request for a provider-specific proposal permits only a local, non-executable preview. A clear request to publish authorizes that post without a second confirmation.

- resolve the current profile and connected destinations read-only
- collect all content, media, timing, privacy, disclosure, and destination-specific choices
- ask only for a required choice that is missing or ambiguous; accept choices the user delegated
- if the user asked to publish, run the requested action once without another confirmation
- verify the result read-only

Installation, authentication, discovery, a general workflow, a preview, or an earlier write is not a request for a later action.

## Omitted from This Agent-Facing Summary

- publishing and upload commands
- payload shapes and templates
- provider field names and accepted values
- media and scheduling workflows
- cross-platform examples
- destructive and account-management commands

Use [SKILL.md](./SKILL.md) for the request-handling rules. Do not use another document to bypass this boundary.
