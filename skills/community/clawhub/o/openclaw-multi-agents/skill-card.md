## Description:

Openclaw Multi Agents helps an OpenClaw user set up a persistent multi-agent team with a Manager agent, specialized Worker agents, persona templates, task routing guidance, and quality checks before results are returned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porkapple](https://clawhub.ai/user/porkapple)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to plan, create, and maintain a persistent agent team for parallel work such as planning, implementation, review, documentation, and coordination. It is most relevant when a user wants a Main agent to delegate through a Manager agent instead of handling every task directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad persistent changes to OpenClaw agent behavior and local workspaces.

Mitigation: Back up ~/.openclaw first and review generated SOUL.md, AGENTS.md, and openclaw.json diffs before using the changes.

Risk: The security scan flags unsafe installation and data-handling patterns.

Mitigation: Install only on trusted machines, tighten workspace permissions, and manually review any added skills or installation steps.

Risk: Live prompt enrichment or external skill installation may introduce unreviewed content.

Mitigation: Avoid live prompts.chat enrichment and pin or manually approve any skills installed through ClawHub.

Risk: The skill may read user context, memory, and session history while planning or verifying agents.

Mitigation: Use it only when that local context access is acceptable, especially on shared machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/porkapple/skills/openclaw-multi-agents)
- [Project Homepage](https://github.com/porkapple/openclaw-multi-agent)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Architecture Guide](artifact/references/architecture_guide.md)
- [Planning Guide](artifact/references/planning_guide.md)
- [Task Categories and Model Matching](artifact/references/task_categories_and_model_matching.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, and generated SOUL.md and AGENTS.md content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local OpenClaw setup guidance and configuration artifacts; users should review generated files and diffs before applying them.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
