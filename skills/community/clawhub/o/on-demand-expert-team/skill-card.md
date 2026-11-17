## Description:

Instantly designs and runs a temporary expert team to complete a task end-to-end, generating role prompts inline rather than as standalone prompt files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill when a task benefits from a temporary multi-role expert team, structured SOP stages, progress updates, quality gates, and an integrated final deliverable. It can also fall back to single-session execution when team or sub-agent tools are unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can progress from task analysis into multi-agent execution, file writes, and Bash validation without a clear consent checkpoint.

Mitigation: Invoke it intentionally, prefer read-only mode for exploratory work, and require explicit confirmation before it writes files, runs Bash validation, creates subagents, or converts a temporary team design into reusable assets.

Risk: Temporary team outputs may contain incorrect or unverified facts when the task requires external evidence or data.

Mitigation: Require source checks for factual claims, preserve uncertainty markers such as "to be verified", and review final deliverables before relying on them.

Risk: Automatically generated team roles and prompts may over-scope execution or duplicate responsibilities.

Mitigation: Review the displayed team-design rationale, enforce minimal-team and role-boundary checks, and use the bundled team-design validation before execution when files are produced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/on-demand-expert-team)
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng)
- [on-demand-expert-team-catalog.md](references/on-demand-expert-team-catalog.md)
- [on-demand-expert-team-requirements.md](references/on-demand-expert-team-requirements.md)
- [on-demand-expert-team-exemplars.md](references/on-demand-expert-team-exemplars.md)
- [team-design-template.md](templates/team-design-template.md)
- [lead-prompt-template.md](templates/lead-prompt-template.md)
- [member-prompt-template.md](templates/member-prompt-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task outputs with possible inline code, shell commands, configuration snippets, execution summaries, validation notes, and reusable-team guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role prompts are generated inline for the active run and are not intended to be delivered as standalone prompt files unless the user separately asks for reusable material.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
