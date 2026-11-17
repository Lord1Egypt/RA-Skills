## Description:

Guides users through beginner-friendly OpenClaw multi-agent setup, including Feishu onboarding, routing choices, starter profile generation, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[majiabin2020](https://clawhub.ai/user/majiabin2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create multi-agent setups with safe defaults, small-step Feishu onboarding, group-based routing, and final verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to paste Feishu App Secrets into chat.

Mitigation: Collect secrets only through a local masked prompt, environment variable, or trusted secret store.

Risk: The Feishu permission setup may request broader access than a deployment needs.

Mitigation: Reduce Feishu permissions to the minimum required for message receive/send and routing before production use.

Risk: Starter-profile writers may persist files into agent workspaces.

Mitigation: Run profile writers only on new empty workspaces or after backing up existing agent files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/majiabin2020/skills/openclaw-multi-agent-wizard)
- [Quick Start](references/quick-start.md)
- [Modes](references/modes.md)
- [Preflight](references/preflight.md)
- [Feishu Setup](references/feishu-setup.md)
- [Routing Basics](references/routing-basic.md)
- [A2A Collaboration Mode](references/a2a-mode.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline commands and generated configuration/profile files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate starter agent profile files and concise setup summaries when used in an OpenClaw workspace.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
