## Description:

Manage Payhip coupons and license keys through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Payhip coupons and verify licenses, or to create and update coupons and manage license status or uses through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required oo CLI may automatically install or change agent skills, and this skill does not explain that behavior.

Mitigation: Review the CLI's automatic skill installation; consider setting OO_SKILLS_SYNC_DISABLED=1 for CLI calls and reviewing the installer separately.

Risk: Coupon and license actions can change Payhip data.

Mitigation: Keep the skill's approval step for write and destructive actions, confirming the exact target and effect before execution.

## Reference(s):

- [Payhip API documentation](https://payhip.com/api-reference)
- [Payhip](https://payhip.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve Payhip data; write and destructive actions require user approval.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
