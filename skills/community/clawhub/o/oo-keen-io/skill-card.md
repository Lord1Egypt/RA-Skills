## Description:

Keen IO (keen.io). Use this skill for ANY Keen IO request — reading, creating, and updating data. Whenever a task involves Keen IO, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use the skill to query Keen IO event collections, count or sum event data, and publish events through an OOMOL-connected Keen IO account. It requires checking each action's input schema first and confirming the exact payload and effect before event writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute remote installer code that was not inspected and whose future contents are not fixed.

Mitigation: Review the setup first and prefer a verified release installed under your control.

Risk: The CLI may synchronize and install persistent agent skills at startup.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 before invoking the CLI to prevent the documented startup synchronization.

Risk: Publishing an event changes Keen IO data.

Mitigation: Keep the required confirmation and confirm the exact payload and effect before running an event write.

## Reference(s):

- [Keen IO](https://keen.io/)
- [Keen IO API documentation](https://keen.io/docs/api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs are checked against the live connector schema; event writes require confirmation of the payload and effect.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
