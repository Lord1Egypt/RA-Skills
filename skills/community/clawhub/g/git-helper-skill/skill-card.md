## Description:

Git Helper provides Git command explanations, task-specific command guidance, troubleshooting help, and workflow best practices in English or Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunny0826](https://clawhub.ai/user/sunny0826)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand Git commands, plan repository workflows, recover from common Git mistakes, and receive safer command sequences for version-control tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested destructive or history-rewriting Git commands can lose local work or rewrite shared history when used in the wrong repository state.

Mitigation: Review command intent and repository state before execution, especially for reset --hard, clean, rebase, amend, and force-push operations.

Risk: The skill provides guidance but does not execute code or inspect the repository itself, so advice may depend on incomplete user-provided context.

Mitigation: Ask for or run verification commands such as git status and git log before applying complex recovery, reset, rebase, or force-push workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunny0826/skills/git-helper-skill)
- [README](artifact/README.md)
- [Evaluation prompts](artifact/evals/evals.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include English or Chinese explanations, verification commands, and safety warnings for destructive or history-rewriting Git operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
