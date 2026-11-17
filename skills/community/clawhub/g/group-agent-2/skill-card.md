## Description:

智能体 is a minimal multi-agent group skill for AI conversation, agent orchestration, workflow automation, and non-critical decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and agent users use this skill to coordinate multiple AI agents for LLM conversations, agent orchestration, workflow automation, and decision-support tasks that do not require deterministic outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local read, write, search, and command-execution authority for a loosely defined agent helper.

Mitigation: Install only in trusted workspaces where file changes and command execution are acceptable, and constrain allowed commands, file paths, and approval requirements at the host-agent level.

Risk: The security verdict is suspicious because operational boundaries are not clearly defined.

Mitigation: Review the skill before installation and prefer a release that documents exact data, API, command, and permission boundaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/group-agent-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON, depending on the agent task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file edits and commands; execution depends on host agent permissions.]

## Skill Version(s):

1.0.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
