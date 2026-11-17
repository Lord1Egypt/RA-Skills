## Description:

Opens the system map application and starts navigation to a user-provided destination or coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samkeke](https://clawhub.ai/user/samkeke)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent open the local map application and prepare navigation for a named destination or latitude/longitude coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Destination text or coordinates may be sent to Apple Maps or another registered URL handler.

Mitigation: Use the skill only on explicit user request and avoid sending sensitive locations unless that disclosure is intended.

Risk: Unencoded destination parameters may produce incorrect navigation targets or malformed map URLs.

Mitigation: Encode destination parameters safely before constructing map URLs.

Risk: The skill depends on a local GUI desktop session and the operating system's map URL handling.

Mitigation: Deploy it only in environments where opening a local map application is expected and supported.

## Reference(s):

- [open-map ClawHub skill page](https://clawhub.ai/samkeke/skills/open-map)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and map URL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-provided destination string or latitude/longitude coordinates for local map navigation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
