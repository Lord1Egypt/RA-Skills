## Description:

Razorpay (razorpay.com). Use this skill for ANY Razorpay request — reading, creating, updating, and deleting data. Whenever a task involves Razorpay, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Razorpay orders and payments and, with approval, create orders or refunds through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, the setup instructions run a remote installer whose contents and local effects are unverified.

Mitigation: Install a verified CLI release yourself, and require approval before any fallback installation. Review the CLI's bundled-skill synchronization behavior and the Razorpay access it receives.

Risk: Creating orders or issuing refunds changes Razorpay account state.

Mitigation: Keep the skill's confirmation requirements: confirm the exact order payload before creating an order, and confirm the refund target and action before issuing a refund.

## Reference(s):

- [Razorpay API authentication documentation](https://razorpay.com/docs/api/authentication/)
- [Razorpay](https://razorpay.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions with oo CLI commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are fetched before calls; no fixed output size is stated.]

## Skill Version(s):

1.0.6 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
