## Description:

Helps users read and manage Stripe customers, products, and prices through their connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to retrieve Stripe account, customer, product, and price information and to make approved customer or catalog changes through their connected Stripe account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified downloads and silently install other agent skills; installer contents and hosted service behavior are unverified.

Mitigation: Review CLI installation and automatic skill synchronization, independently verify downloaded software, and set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent startup skill synchronization.

Risk: Stripe changes and deletions can affect account records.

Mitigation: Use a restricted Stripe key and retain explicit approval for changes and deletions.

## Reference(s):

- [Stripe API documentation](https://docs.stripe.com/api)
- [Stripe](https://stripe.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON action results and concise guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that change or delete Stripe records require user approval.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
