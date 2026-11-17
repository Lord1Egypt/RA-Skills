## Description:

Sauce Labs (saucelabs.com). Use this skill for ANY Sauce Labs request — reading, creating, and updating data. Whenever a task involves Sauce Labs, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test teams use this skill to inspect Sauce Labs builds, virtual-device jobs, and job assets, and to update job names, tags, visibility, or pass status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Required software may make broader changes to the agent environment than the skill explains.

Mitigation: Review OOMOL account access and install a verified oo CLI release before use; disable startup synchronization with OO_SKILLS_SYNC_DISABLED=1 if additional skills should not be installed or refreshed.

Risk: Updating a Sauce Labs job can change its visibility.

Mitigation: Confirm job edits, especially visibility changes, before applying them.

Risk: The downloaded installer and hosted service implementation are outside the inspected package.

Mitigation: Review and verify the CLI release before installation, and account for the hosted service being outside the package review.

## Reference(s):

- [Sauce Labs](https://saucelabs.com)
- [Sauce Labs API documentation](https://docs.saucelabs.com/dev/api/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON connector responses and textual guidance, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read Sauce Labs data or update job metadata and status.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
