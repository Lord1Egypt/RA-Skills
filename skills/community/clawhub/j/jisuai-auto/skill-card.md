## Description:

jisuai-auto configures OpenClaw to use the aicodee.com MiniMax relay by extracting API details and updating the local OpenClaw model settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[outrice](https://clawhub.ai/user/outrice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure an aicodee.com MiniMax API relay as an OpenClaw provider and make it the default model route.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles API credentials while configuring OpenClaw.

Mitigation: Use only intended HTTPS aicodee.com endpoints, avoid pasting real keys into chat or shell history when possible, and rotate keys if they are exposed.

Risk: The skill makes persistent model-routing changes with too little scoping and user control.

Mitigation: Back up openclaw.json first, then verify the provider, endpoint, API key, and default model before continuing to use OpenClaw.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/outrice/skills/jisuai-auto)
- [aicodee.com MiniMax relay endpoint](https://v2.aicodee.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown instructions with inline shell commands and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make persistent OpenClaw provider and default model changes when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
