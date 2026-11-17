## Description:

Lobster Fork Mode helps agents spawn subagents with selected parent-session context so the subagent can preserve task goals, relevant files, decisions, and preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a subagent needs parent-session context, including task goals, relevant file paths, code snippets, decisions, and selected preferences. It is most useful for project-aware or decision-aware subagent work rather than independent mechanical tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected parent-session context can include private file paths, code snippets, decisions, or memory-derived preferences.

Mitigation: Review and limit the context before spawning subagents, and avoid tasks involving secrets or private memory unless sharing is explicitly acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-fork-mode)
- [ClawHub publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with prompt templates and inline command-style blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested context-size limits and truncation strategies.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
