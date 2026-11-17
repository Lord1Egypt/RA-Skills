---
name: pontx-pinhere
description: Integrate Pinhere safely through Pontx for private issue collaboration, browser-extension capture, project setup, Webhooks, PATs, OAuth, and explicitly approved state changes.
---

# Pinhere

Use this Skill for Pinhere-specific privacy, authorization, issue-lifecycle,
browser-extension, and Webhook delivery decisions. Resolve current Endpoint,
Schema, credential, and package details before writing code:

```bash
pontx-hub search "Pinhere <capability>" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk pinhere
```

Use `@pontx/pinhere` for application integration. Use `pontx-pinhere` only for
an explicitly requested local script. Hub discovery is not an execution path:
all Pinhere requests originate from the caller-controlled SDK or CLI process.

## Establish the privacy and authorization boundary

Pinhere API responses can include private project data, issue content, DOM
context, screenshots, token metadata, or Webhook delivery diagnostics. Minimize
what your application fetches and returns. Do not send any of that data, a PAT,
a website session cookie, OAuth value, one-time secret, or screenshot to Hub,
logs, analytics, support tickets, or chat.

Use a PAT for the smallest required service-to-service read or write scope.
Keep it in a caller-owned secret store or process environment. Reserve website
session credentials for the user-owned same-origin workflow. For a Chrome
extension, preserve OAuth 2.0 Authorization Code + PKCE values only in the
extension and its trusted backend; never substitute a copied browser session.

Read the active project, Origin, and issue identity before proposing a change.
Treat every requested create, claim, completion, reopen, delete, token action,
or Webhook action as a persistent or security-sensitive operation. If names are
ambiguous, stop and ask the user to select the exact target.

## Preview every direct call

Inspect the current local surface and create a redacted request preview first:

```bash
pnpm exec pontx-pinhere list apis
pnpm exec pontx-pinhere call issues getIssue --issueId iss_example --dry-run
```

For any state-changing request, present the exact target, method, path,
redacted input, and expected effect. Obtain explicit approval, then invoke the
unchanged request with its generated confirmation token. A changed target,
body, credential context, or operation requires a new preview.

Do not automatically retry an ambiguous write or Webhook delivery action.
Inspect the current resource and delivery state first. Treat one-time token or
secret responses as non-recoverable sensitive output: return only the minimum
needed to the intended local recipient and do not persist them.

## Few-shot workflows

### Scenario 1: Read project issues

**User:** "Show open issues for this project, but do not expose any private
details outside our tool."

**Approach:** Resolve the live read contract and exact project identity, use a
local preview, request approval before any direct call, and return only the
minimum allowed result with credentials and private context redacted.

### Scenario 2: Capture a browser issue

**User:** "Let our Chrome extension create an issue from a page screenshot."

**Approach:** Apply the extension authorization and privacy boundary, inspect
the live capture and attachment contract, preserve PKCE isolation, and preview
the exact creation before requesting approval. Do not transmit page context or
screenshots through Hub.

### Scenario 3: Rotate a Webhook secret

**User:** "Rotate the deployment Webhook secret now."

**Approach:** Resolve the exact Webhook and downstream rotation plan, explain
that the value is sensitive, preview the local action, and stop for explicit
approval. Deliver a returned one-time value only to the authorized caller and
never log it.
