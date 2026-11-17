# Provider Settings - Agent Safety Boundary

## Purpose

This document defines the safety boundary for provider-specific settings. It is not a field reference or publishing playbook.

Operational provider schemas and publishing syntax are intentionally omitted. Do not infer a payload, media workflow, destination setting, or executable command from this file.

## Default Behavior: Read Only

An AI agent must remain in read-only discovery unless the user explicitly requests a specific Mallary publishing action or proposal. General questions about supported platforms, account status, or provider behavior do not authorize drafting or executing a post.

Use only the read-only command needed to resolve current state:

```bash
mallary profiles list
mallary platforms list --profile-id <current-profile-id>
```

Profile IDs, profile names, account labels, and connection state are sensitive. Minimize and redact the output. Never reuse an older profile ID or connection snapshot as current state without checking it again.

## If the User Explicitly Requests a Provider-Specific Post or Proposal

A request for a proposal permits preparation of a local, non-executable preview only. A clear request to publish authorizes that post without a second confirmation.

1. resolve the current profile and connected destinations with minimum read-only discovery
2. gather the user's desired content, destination, media, timing, privacy, disclosure, and platform-specific choices
3. consult authoritative Mallary product documentation only as needed to validate the request
4. ask only for a required choice that is missing or ambiguous; accept choices the user delegated
5. if the user asked to publish, run the requested action once without another confirmation
6. verify it with a read-only command

Do not guess a destination-specific choice. If a required choice is missing, stop and ask for it rather than selecting a default.

## A Request Does Not Carry Forward

Installation, authentication, discovery, a general workflow, a local preview, or an earlier write is not a request for a later action. A clear current publishing request authorizes only the content and destinations it describes.

## Intentionally Omitted

To prevent this agent-facing document from becoming an actionable publishing guide, it does not include:

- publishing or upload commands
- JSON request bodies or payload templates
- provider field names or accepted values
- media upload or thumbnail workflows
- scheduling examples
- cross-platform campaign examples
- destructive or account-management commands

For a user-requested write, follow the command side-effect classification and request-handling rules in [SKILL.md](./SKILL.md). Do not use another document to bypass this boundary.

## Review Checklist

Before any requested write, confirm that:

- the current profile and every destination were verified read-only
- the user supplied or delegated all destination-specific choices
- every local file and URL belongs to the request
- message, media, timing, privacy, disclosure, and side effects are explicit
- the user clearly requested publishing rather than only a draft or preview
- the action will run once and be verified read-only without a redundant confirmation

If any item is missing, remain read-only.
