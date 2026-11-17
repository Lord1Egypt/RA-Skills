## Description:

Build and operate a metered public API endpoint for OpenClaw skills or agents with API-key authentication, per-request usage logging and pricing, prepaid balances, and BTC/ETH top-ups through payment-processor webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arshingleton](https://clawhub.ai/user/arshingleton)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to package an OpenClaw capability as a public metered API with signed requests, usage accounting, prepaid balances, and payment webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External routing and billing flows may send sensitive lead, contract, or business data to an endpoint the operator does not control.

Mitigation: Replace the hardcoded api.vms0.com endpoint with a confirmed deployment or deliberately approve that hosted service before use.

Risk: Payment, credential, and admin flows require hardening before production use.

Mitigation: Use strong webhook secrets, disable or guard demo payment behavior, protect admin routes, and review idempotency and failed-charge handling.

Risk: Unpinned JavaScript dependencies can change during installation.

Mitigation: Pin dependencies with lockfiles and review package updates before deploying the service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arshingleton/skills/metered-api-marketplace)
- [API Reference](references/api_reference.md)
- [Billing and Ledger Notes](references/billing_ledger.md)
- [Payment Provider Adapters](references/providers.md)
- [Agent Integration Prompt](references/integration_prompt.md)
- [VMS0 API Base URL](https://api.vms0.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JavaScript server code, JSON API examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and starter files for a metered API service; runtime responses are structured JSON.]

## Skill Version(s):

0.1.3 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
