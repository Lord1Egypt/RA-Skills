## Description:

Coupontools (coupontools.com). Use this skill for any Coupontools request involving reading, creating, or updating data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to list and retrieve Coupontools coupon campaigns and create single-use coupon URLs through a connected Coupontools account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote CLI installer and CLI implementation have not been verified, and the installer may synchronize other agent skills.

Mitigation: Use an already reviewed CLI installation; require approval before running the remote installer, and review or disable its automatic skill synchronization.

Risk: Connecting Coupontools gives OOMOL access to the selected account, and creating a single-use URL changes account state.

Mitigation: Retain confirmation of the exact coupon change payload and effect before running the write action.

## Reference(s):

- [Coupontools API documentation](https://docs.coupontools.com/api/overview)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Coupontools](https://www.coupontools.com)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON input and JSON responses, plus concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations retrieve coupon data; the create_single_use_url action changes account state and requires confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
