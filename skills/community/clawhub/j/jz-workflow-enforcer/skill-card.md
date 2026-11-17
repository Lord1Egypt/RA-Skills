## Description:

Agent Workflow Enforcer helps agents follow mandatory workflow checkpoints through gate scripts, required output formats, and persisted style context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add mandatory pre-task and post-task checklists for content, code, deployment, and staged work so agents keep workflow constraints visible during execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent instruction rules can influence future agent sessions outside the intended workflow.

Mitigation: Install only in narrowly scoped projects and remove copied workflow rules when the workflow is no longer needed.

Risk: The documented installer uses an unpinned latest package reference.

Mitigation: Prefer a pinned, verified installer and review the skill before installation.

Risk: Workflow context files may contain sensitive task or style details.

Mitigation: Inspect or delete generated style-context.yaml or learnings.jsonl files before sharing or reusing the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzocb/skills/jz-workflow-enforcer)
- [Declared homepage](https://github.com/example/agent-workflow-enforcer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, checklist text, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask agents to create or read local workflow context files such as style-context.yaml.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
