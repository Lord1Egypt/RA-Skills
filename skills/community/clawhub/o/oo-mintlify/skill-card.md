## Description:

Mintlify (mintlify.com). Use this skill for ANY Mintlify request — reading, creating, and updating data. Whenever a task involves Mintlify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers with an OOMOL-connected Mintlify account use this skill to check deployment status and trigger production or preview deployments through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes unverified installers, and the required CLI can silently install persistent agent skills.

Mitigation: Review the installer before use, use a verified release, and consider disabling automatic skill synchronization before running commands.

Risk: The hosted connector implementation is outside the supplied artifact and was not verified.

Mitigation: Review which Mintlify access is connected through OOMOL, and keep deployment confirmation enabled.

## Reference(s):

- [Mintlify documentation](https://www.mintlify.com/docs)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-mintlify)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [JSON action results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the connected Mintlify account and selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
