## Description:

Recharge (getrecharge.com). Use this skill for ANY Recharge request — searching and reading data. Whenever a task involves Recharge, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to search and read Recharge charges, customers, orders, products, and subscriptions through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions use remote installer scripts whose contents remain unverified.

Mitigation: Review CLI setup separately and use a verified release before allowing installation.

Risk: Startup may automatically install additional skills without disclosing the full scope.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED=1 before running oo.

Risk: OOMOL mediates access to the connected Recharge account.

Mitigation: Use a read-only Recharge connection and account for OOMOL's role in access.

## Reference(s):

- [Recharge API documentation](https://developer.rechargepayments.com/2021-11)
- [oo CLI documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI command controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Recharge homepage](https://getrecharge.com/)
- [Recharge skill release page](https://clawhub.ai/oomol/skills/oo-recharge)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with shell command examples and JSON payloads; Recharge responses are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Recharge records returned through the connected account.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
