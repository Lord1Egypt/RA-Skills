## Description:

Run an autonomous Open Ralph Wiggum coding loop using OpenCode Zen with free models and automatic fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bderiel](https://clawhub.ai/user/bderiel)

### License/Terms of Use:


## Use Case:

Developers use open-ralph to run a bounded autonomous coding loop for fixing tests, implementing scoped changes, refactoring, and resolving build, lint, or type errors inside a git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The autonomous coding loop can repeatedly modify files in the current repository.

Mitigation: Run it on a clean git branch, keep iteration limits modest, and inspect the final diff before merging or committing changes.

Risk: Broad or unverifiable prompts can produce changes that do not satisfy the intended task.

Mitigation: Provide precise task scope, verifiable success criteria, and a completion promise before starting the loop.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bderiel/skills/open-ralph)
- [Project homepage](https://github.com/Th0rgal/open-ralph-wiggum)
- [OpenCode Zen models](https://opencode.ai/zen/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires git, ralph, and opencode binaries; autonomous loops should use explicit success criteria, completion promises, and iteration limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
