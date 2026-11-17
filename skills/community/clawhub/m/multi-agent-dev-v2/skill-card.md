## Description:

Coordinates multi-agent coding work by decomposing implementation plans, assigning fresh subagents, and applying staged specification and code-quality reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate multi-step coding plans through task decomposition, subagent implementation, staged reviews, and final integration review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can coordinate broad code-changing work, including command execution, file edits, tests, Git operations, and subagents.

Mitigation: Require explicit confirmation before writes, commits, branch or worktree changes, deployments, or credential use.

Risk: The security evidence flags inconsistent generic API-key, callback_url, CRUD, and API-connection sections.

Mitigation: Review or remove those generic sections before installation and use platform-managed credentials only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/multi-agent-dev-v2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with examples, command-oriented guidance, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to read files, execute shell commands, edit files, run tests, use Git workflows, and coordinate subagents.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
