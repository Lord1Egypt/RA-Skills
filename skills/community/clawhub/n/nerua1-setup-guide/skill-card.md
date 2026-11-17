## Description:

Battle-tested setup guide for a multi-agent AI system on Apple Silicon, covering install order, RAM tradeoffs, shared memory, inter-agent communication, operational pitfalls, and WhatsApp monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerua1](https://clawhub.ai/user/nerua1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent operators use this skill to set up or onboard a multi-agent AI system on Apple Silicon, including Claude Code and OpenClaw installation order, memory sharing, local and cloud model placement, backup practices, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide may influence agents to reduce sandbox isolation.

Mitigation: Keep explicit human approval around sandbox changes and review whether reduced isolation is acceptable for the target system.

Risk: The guide includes external install guidance for pip, npx, and git-installed components.

Mitigation: Pin package versions and verify package sources before installing or running components.

Risk: Console or monitoring guidance may expose sensitive information through WhatsApp.

Mitigation: Avoid forwarding sensitive console logs, tokens, credentials, personal data, or operational secrets to messaging channels.

Risk: Guidance touches crons, ports, and configuration edits that can change system behavior.

Mitigation: Require explicit user approval before changing schedules, opening ports, or editing persistent configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerua1/skills/nerua1-setup-guide)
- [Artifact README](artifact/README.md)
- [Project story](artifact/STORY.md)
- [Published locations](artifact/PUBLISHED.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
