## Description:

Deploys an OpenClaw self-evolution workspace with a constitution, evolving SOUL.md, heartbeat workflow, PARA-style memory, goal tracking, EvoClaw governance, and self-improving agent support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kianzzz](https://clawhub.ai/user/kianzzz)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to initialize a persistent agent workspace that can manage identity, memory, goals, heartbeats, and governed self-improvement. It is intended for users who explicitly want a persistent self-evolving agent environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a persistent self-evolving agent workspace with broad memory and governance authority.

Mitigation: Install only when that behavior is intentional, and review generated AGENTS.md, HEARTBEAT.md, SOUL.md, EvoClaw, and self-improving files before activation.

Risk: Persistent memory and self-improvement files can retain sensitive information if users paste secrets into the agent context.

Mitigation: Avoid pasting raw API tokens or credentials, and inspect memory files before sharing or syncing the workspace.

Risk: Source polling and visualizer behavior can expose workspace information if enabled broadly.

Mitigation: Keep source polling opt-in and do not run the visualizer server on an untrusted network.

Risk: Heartbeat, default-agent, and governance changes can alter future agent behavior.

Mitigation: Require explicit user approval for heartbeat, default-agent, and governance changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/kianzzz/skills/openclaw-soul-publish)
- [Publisher profile](https://clawhub.ai/user/kianzzz)
- [README](artifact/README.md)
- [Bootstrap guide](artifact/references/bootstrap-guide.md)
- [Agent constitution template](artifact/references/agents-template.md)
- [Soul template](artifact/references/soul-template.md)
- [Heartbeat template](artifact/references/heartbeat-template.md)
- [EvoClaw schema reference](artifact/fallback/evoclaw/references/schema.md)
- [Self-improving security boundaries](artifact/fallback/self-improving/boundaries.md)
- [Self-Improving Agent page](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands, generated workspace files, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a persistent OpenClaw workspace after user confirmation and preflight checks.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
