## Description:

Generate machine-actionable Product Requirements Documents for AI coding agents, using a discovery interview before drafting phased requirements, acceptance criteria, file structures, API contracts, and build order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idcesares](https://clawhub.ai/user/idcesares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and AI-agent users use this skill to turn feature ideas or raw notes into executable PRDs for Claude Code, Codex, Cursor, Gemini CLI, or similar coding agents. It is best suited for structured implementation planning before an agent starts changing code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PRDs or companion agent guidance may encode incorrect assumptions if discovery answers are incomplete.

Mitigation: Review the PRD and any generated CLAUDE.md or AGENTS.md before allowing another agent to rely on them.

Risk: Generated planning files can influence later agent behavior and may steer implementation toward outdated or misunderstood requirements.

Mitigation: Validate acceptance criteria, protected behaviors, file paths, and API contracts against the current project before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/idcesares/skills/prd-for-ai-agents)
- [Discovery Interview Question Bank](artifact/discovery-questions.md)
- [PRD Template for AI Coding Agents](artifact/prd-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a PRD Markdown file and, when requested, companion CLAUDE.md, AGENTS.md, TASKS.md, or PLANNING.md files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
