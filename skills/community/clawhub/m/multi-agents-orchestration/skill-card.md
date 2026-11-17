## Description:

Defines OpenClaw multi-agent orchestration patterns for backend spawning, Discord mentions, bot-to-bot mentions, configuration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cchaojiejes](https://clawhub.ai/user/cchaojiejes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to design and adjust multi-agent team collaboration, including when to use backend spawn, Discord-visible agents, or skill-only workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples use broad agent-delegation authority that could allow agents to call more roles than intended.

Mitigation: Replace wildcard delegation with explicit allowlists for each role before applying the configuration.

Risk: Discord setup requires bot tokens and channel permissions that can expose persistent access if handled loosely.

Mitigation: Keep bot tokens private and scoped, restrict guild and channel access, and enable only the Discord features required for the deployment.

Risk: The guide changes persistent OpenClaw agent and gateway configuration.

Mitigation: Review each configuration change before restarting the gateway and test with a minimal spawn task before using the workflow for real work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cchaojiejes/skills/multi-agents-orchestration)
- [Source skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and JavaScript configuration examples plus shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes OpenClaw and Discord configuration examples that should be adapted with explicit agent IDs, scoped tokens, and allowlists before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
