## Description:

Best practices for using Claude Code with large, multi-part codebases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure Claude Code work on large repositories, including codemap preparation, session planning, subagent use, worktree workflows, and verification habits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for batch edits, commits, pull requests, CI analysis, resume flows, and repository-wide Claude Code usage.

Mitigation: Run those commands only after deliberate review, especially in private repositories or when code should not be sent to an external Claude account.

Risk: Following workflow advice without verification can still lead to incorrect code changes or misleading guidance being applied to a project.

Mitigation: Review proposed changes, run project tests, and keep human approval around commands that modify files, commits, or release workflows.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Best Practices](https://code.claude.com/docs/en/best-practices)
- [Claude Code Subagents Guide](https://code.claude.com/docs/en/sub-agents)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-large-codebase-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only workflow guidance; no tool calls or credentials are required by the skill itself.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
