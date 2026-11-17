## Description:

Implement Google Pay for web and Android with tokenization safety, gateway alignment, and production-ready checkout operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to implement Google Pay checkout, subscription, and PSP-mediated payment flows with safe token handling, environment validation, rollout checks, and incident response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw payment tokens, private keys, or PSP secrets could be exposed through chat, logs, screenshots, or local notes.

Mitigation: Keep token handling minimal, never ask for secrets in chat, and store only short validation evidence and non-sensitive metadata in local notes.

Risk: Client-side totals, currency, or gateway configuration could diverge from server and PSP records.

Mitigation: Use the server as the source of truth for charge amount and currency, align gateway identifiers by environment, and validate PSP mapping before rollout.

Risk: Retries or timeout recovery could create duplicate authorizations.

Mitigation: Require stable idempotency keys for authorization, capture, refund, and void operations, then verify retry behavior in the validation checklist.

Risk: A production release could fail if merchant readiness, fallback checkout, observability, or rollback gates are incomplete.

Mitigation: Keep integrations in test mode until validation passes, use a staged rollout, monitor payment metrics, and pause launch when hard-stop conditions occur.

## Reference(s):

- [Google Pay skill page](https://clawhub.ai/ivangdavila/skills/google-pay)
- [Google Pay](https://pay.google.com)
- [Google Pay JavaScript client](https://pay.google.com/gp/p/js/pay.js)
- [Google Pay developer documentation](https://payments.developers.google.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with checklists, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, GOOGLE_PAY_MERCHANT_ID, and access to the relevant Google Pay business console and PSP account.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
