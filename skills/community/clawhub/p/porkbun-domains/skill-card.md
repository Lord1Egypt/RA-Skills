## Description:

Manage Porkbun domains and DNS through API-backed shell commands for domain listing, availability checks, DNS records, nameservers, URL forwarding, SSL retrieval, pricing, and auto-renew settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielgrobelny](https://clawhub.ai/user/danielgrobelny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Porkbun-hosted domains and DNS records from an agent workflow. It is useful for routine DNS changes, domain checks, forwarding setup, SSL bundle retrieval, and related domain administration tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can change live domain configuration, including DNS records, nameservers, URL forwarding, SSL retrieval, and auto-renew settings.

Mitigation: Preview planned changes, confirm the exact domain and record targets before execution, and restrict credential use to accounts authorized for the intended domains.

Risk: The workspace .env credential loader can execute shell code if the environment file is untrusted.

Mitigation: Pass Porkbun credentials through a secure environment or secret manager, remove the eval-based loader before deployment, and avoid running the skill in untrusted workspaces.

## Reference(s):

- [Porkbun API key settings](https://porkbun.com/account/api)
- [ClawHub skill page](https://clawhub.ai/danielgrobelny/skills/porkbun-domains)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Porkbun API credentials; command results depend on live Porkbun API responses and account permissions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
