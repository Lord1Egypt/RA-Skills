## Description:

Controls a local Clash for Windows proxy by changing proxy routing, checking status, and switching nodes through the Clash REST controller.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icenoodle](https://clawhub.ai/user/icenoodle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users who run Clash for Windows use this skill to manage local proxy routing and inspect the current proxy status from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill embeds a Clash controller secret that can authorize local proxy control if reused.

Mitigation: Replace or rotate the controller secret before use and keep the Clash REST controller bound to localhost.

Risk: Broad or ambiguous trigger phrases can unexpectedly change proxy routing.

Mitigation: Use explicit commands and review command handling before enabling the skill in shared or sensitive environments.

Risk: The skill can alter local network proxy behavior.

Mitigation: Install only where the Clash for Windows REST controller, ports, and proxy configuration are understood and intentionally configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icenoodle/skills/openclaw-clash-forwindows-controller)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text status, success, failure, and usage messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can change local proxy routing through the Clash REST controller when matching commands are issued.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
