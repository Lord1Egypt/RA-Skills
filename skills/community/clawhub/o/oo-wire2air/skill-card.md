## Description:

Wire2Air (wire2air.com). Use this skill for ANY Wire2Air request — reading, creating, and updating data. Whenever a task involves Wire2Air, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read inbound SMS and MMS messages and queue SMS messages through a connected Wire2Air account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to run online CLI installers whose contents and installed runtime were not verified.

Mitigation: Review and approve the CLI installation separately, and check whether the documented synchronization-disable setting is appropriate.

Risk: Sending messages can reach unintended recipients or incur costs.

Mitigation: Connect only the intended Wire2Air account and review recipients, message content, and costs before sending.

## Reference(s):

- [Wire2Air](https://www.wire2air.com)
- [Wire2Air REST API documentation](https://www.wire2air.com/docs/rest-api/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read and message-queueing actions; write actions require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
