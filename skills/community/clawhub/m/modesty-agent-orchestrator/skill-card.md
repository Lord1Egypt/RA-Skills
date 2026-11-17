## Description:

Meta-agent skill for orchestrating complex tasks through autonomous sub-agents by decomposing macro tasks, spawning specialized agents, coordinating file-based communication, consolidating results, and dissolving agents when work is complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to break complex work into parallel or dependent subtasks, generate specialized sub-agent workspaces, coordinate their file-based handoffs, and consolidate their results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task files, datasets, source code, or internal documents may be shared with the third-party SkillBoss API when sub-agents use AI capabilities.

Mitigation: Require explicit approval before external API use, redact confidential inputs and secrets, scope the SKILLBOSS_API_KEY, and use local-only controls for sensitive work.

Risk: Autonomous sub-agents can create workspaces, generate skill files, and perform delegated work with broad file and tool access.

Mitigation: Run agents in isolated workspaces with least-privilege credentials, review generated SKILL.md files and task instructions before dispatch, and scan outputs before integration.

Risk: Parallel sub-agent outputs may conflict or contain incorrect conclusions that could be merged into the final deliverable.

Mitigation: Validate each deliverable against its success criteria, document conflicts during consolidation, and require human review for merged results.

## Reference(s):

- [File-Based Communication Protocol](references/communication-protocol.md)
- [Sub-Agent Templates](references/sub-agent-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/modestyrichards/skills/modesty-agent-orchestrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with inline shell, Python, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration guidance and file/workspace specifications for generated sub-agents, including inbox, outbox, workspace, status, summary, and error-report conventions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
