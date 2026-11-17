## Description:

Bridge OpenClaw with your n8n instance for Home Assistant automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to route Home Assistant, IoT, and calendar requests from OpenClaw to a local n8n workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real smart-home actions through a local n8n and Home Assistant setup.

Mitigation: Use it only with a trusted local n8n workflow and require confirmation for any device-changing action.

Risk: The documented curl pattern may be unsafe if raw user text is substituted directly into a shell string.

Mitigation: Avoid constructing shell commands from unsanitized user input; pass request data through safe JSON construction.

Risk: The connected workflow may expose Home Assistant or calendar data and actions beyond the intended use.

Mitigation: Limit the workflow's Home Assistant and calendar permissions to only the required devices, calendars, and operations.

## Reference(s):

- [n8n](https://n8n.io/)
- [ClawHub skill page](https://clawhub.ai/enchantedmotorcycle/skills/homeassistant-n8n-agent)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces curl POST examples that send chatInput, requestType, and sessionId fields to a local n8n webhook.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
