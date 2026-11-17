## Description:

Human-in-the-loop: A free, extensible framework for intercepting tool calls via the OmniPersona mobile app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiasyouki](https://clawhub.ai/user/tobiasyouki)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use OmniPermission to add human approval gates to selected OpenClaw tool calls before an agent can proceed with sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OmniPersona key may be exposed by the status command or unsafe local handling.

Mitigation: Rotate the key if it may have been displayed, avoid sharing status output, and require masked or safer secret storage before relying on the plugin in sensitive environments.

Risk: Approval policy storage can fail open if malformed, allowing protected tools to run without the intended gate.

Mitigation: Validate policy storage and fail closed on invalid policy before treating the plugin as a security boundary.

Risk: An agent with access to the OpenClaw CLI may be able to change or clear the approval configuration.

Mitigation: Run the agent in isolated mode without access to the OpenClaw CLI when approval rules must not be modified by the agent.

Risk: Sensitive tool context may be sent through the mobile approval channel.

Mitigation: Do not route highly sensitive tools or prompts through the mobile approval flow unless the external data flow is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobiasyouki/skills/omnipermission)
- [Project homepage from ClawHub metadata](https://github.com/youkinetwork/OmniPermission)
- [OmniPersona on the App Store](https://apps.apple.com/us/app/omnipersona/id6553972082)
- [OmniPersona on Google Play](https://play.google.com/store/apps/details?id=ai.youki.omni.persona)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces setup and operating guidance for configuring mobile approval gates around selected OpenClaw tools.]

## Skill Version(s):

1.0.2 (source: package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
