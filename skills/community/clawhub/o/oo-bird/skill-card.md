## Description:

Bird (bird.com). Use this skill for ANY Bird request — reading, creating, updating, and deleting data. Whenever a task involves Bird, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Bird through an OOMOL-connected account can ask an agent to inspect Bird channels, contacts, messages, and interactions, or to create, update, delete, and send Bird data. The skill covers both read actions and state-changing actions, with confirmation guidance for writes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI's remote installer was unavailable for inspection, and automatic setup may execute unverified code or make broader local changes.

Mitigation: Review and install the CLI separately, and examine its automatic skill synchronization settings before use.

Risk: Bird contact data and message payloads pass through OOMOL, and broad account permissions could expose more data than needed.

Mitigation: Grant only the account permissions needed for the task.

Risk: Creating, updating, sending, or deleting Bird data can change external state.

Mitigation: Keep the skill's confirmation requirement for write actions and confirm the target and effect before destructive actions.

## Reference(s):

- [Bird](https://bird.com)
- [Bird API documentation](https://docs.bird.com/)
- [oo CLI project (linked by the skill)](https://github.com/oomol-lab/oo-cli)
- [Bird skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-bird)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [JSON action payloads and Bird response data, with concise text guidance or summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads should follow the live connector schema; write and destructive actions require confirmation of the intended effect or target.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
