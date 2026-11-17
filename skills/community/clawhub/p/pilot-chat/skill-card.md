## Description:

Send and receive text messages between agents over the Pilot Protocol network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to exchange direct one-to-one text messages between agents over the Pilot Protocol network for short questions and request-response workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell examples can become unsafe if untrusted hostnames or message text are interpolated directly into Bash commands.

Mitigation: Treat hostnames and message bodies as data, avoid sending secrets or internal state unless intended, and pass pilotctl arguments as separate process arguments where possible.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-chat)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
