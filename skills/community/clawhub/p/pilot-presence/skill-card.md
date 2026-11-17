## Description:

Real-time online/offline/busy presence tracking for agent fleets using ping and pub/sub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to track agent availability, broadcast presence changes, and discover available agents for task routing in Pilot Protocol fleets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow example uses Bash commands that publish agent presence data.

Mitigation: Install only in Pilot Protocol environments where publishing presence data is expected, and avoid running the loop with elevated privileges.

Risk: The example loop uses a predictable /tmp status file path for continuous presence updates.

Mitigation: Replace the fixed status file with a private temporary directory or another authenticated status source, and validate status values before publishing.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-presence)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash command examples and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, the pilot-protocol skill, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
