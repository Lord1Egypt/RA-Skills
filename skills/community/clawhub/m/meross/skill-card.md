## Description:

Control Meross cloud plugs via local CLI commands for discovery, state checks, and switch on/off actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[powtac](https://clawhub.ai/user/powtac)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Meross cloud plugs, read their switch state, and turn supported plugs on or off through the local CLI after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls cloud-connected power devices using Meross account credentials.

Mitigation: Use least-privilege or test Meross credentials where possible, keep credentials out of project files, and require exact user confirmation before switch writes.

Risk: The authoritative security review flags a concerning npm dependency chain.

Mitigation: Review or update the dependency chain before installation, especially request, form-data, ip-address, and ws, and run the skill in an isolated environment where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/powtac/skills/meross)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI success and failure responses are JSON; switch writes require an exact confirmation object.]

## Skill Version(s):

1.0.27 (source: package.json, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
