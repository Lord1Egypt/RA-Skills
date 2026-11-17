## Description:

Integrate Stripe Identity safely through Pontx. Use for VerificationSessions, document, selfie, or ID-number checks, webhooks, retries, sensitive results, cancellation, or redaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pontjs](https://clawhub.ai/user/pontjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate Stripe Identity through Pontx for verification session lifecycle design, webhook handling, retries, sensitive result access, cancellation, and redaction while protecting credentials and identity data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stripe credentials, client secrets, webhooks, or identity data could be exposed through browser delivery, command arguments, logs, analytics, or error reporting.

Mitigation: Keep Stripe keys server-side, return only the client secret to the authenticated user over TLS, and avoid logging complete sessions, reports, raw events, or PII-bearing errors.

Risk: Webhook spoofing, duplicate delivery, or out-of-order events could cause incorrect verification state changes.

Mitigation: Verify Stripe-Signature against the untouched raw request body, deduplicate event IDs, make business actions idempotent, and retrieve the latest session when current state matters.

Risk: Cancellation and redaction can be irreversible or affect related reports, events, logs, metadata, and collected files.

Mitigation: Resolve mutations through the live contract, inspect current state and deletion scope, preview with dry-run, obtain explicit approval, and use a fresh preview when any API name, session, body, or option changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the current Pontx contract for API and SDK details; mutation workflows include dry-run previews and explicit confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
