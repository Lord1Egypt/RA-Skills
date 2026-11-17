## Description:

Gives AI agents persistent BlueColumn memory for storing and recalling health and fitness goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to store, recall, and search health and fitness context so responses can reflect ongoing goals and habit history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive health and fitness information may be sent to and persistently stored by BlueColumn's external service.

Mitigation: Require explicit user confirmation before each store or recall operation, show the exact text being saved, and avoid storing unnecessary sensitive details.

Risk: Stored memories may persist beyond the user's immediate session.

Mitigation: Use a dedicated scoped API key and confirm the deletion process before deployment or routine use.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/health-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with bash curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends health-related text to an external persistent memory service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
