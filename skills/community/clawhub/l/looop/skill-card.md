## Description:

Claude Automated Development Toolkit decomposes requirements from documents, files, or inline text into task lists and can execute those tasks through Claude CLI until project completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caesargattuso](https://clawhub.ai/user/caesargattuso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use looop to turn requirements into a tracked implementation plan and optionally have Claude CLI execute the tasks inside a source directory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates Claude CLI to modify code and commit changes with broad authority.

Mitigation: Install only for trusted, disposable or well-backed-up repositories and inspect every diff before sharing or pushing.

Risk: Optional git push can publish unintended automated changes.

Mitigation: Avoid --push unless the repository and remote are intentionally prepared for automated updates.

Risk: .looop logs may contain sensitive Claude output.

Mitigation: Ignore, clean, or review .looop logs before committing or sharing project contents.

Risk: Unbounded task execution can make many changes before human review.

Mitigation: Review tasks.json before execution and set --max-tasks for staged runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caesargattuso/skills/looop)
- [Publisher profile](https://clawhub.ai/user/caesargattuso)
- [Claude Code](https://claude.ai/code)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Console text, JSON task files, logs, Markdown-style progress summaries, code changes, and git commits.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes task state, progress, and logs under <src_dir>/.looop; can optionally commit and push changes.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
