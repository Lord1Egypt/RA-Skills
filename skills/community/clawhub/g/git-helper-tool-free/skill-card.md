## Description:

Git Assistant Free helps developers with common Git operations, merge conflict guidance, commit message checks, and safe-operation checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to request step-by-step Git help, resolve merge conflicts, check Conventional Commit messages, and review safety steps before Git operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential persistence guidance may store Git credentials in plaintext when using credential.helper store.

Mitigation: Use credential storage only when the user accepts the plaintext-storage tradeoff, and prefer an operating-system credential manager where available.

Risk: Destructive Git recovery examples such as hard resets can discard local work.

Mitigation: Inspect repository state, save or back up important changes, and confirm the target commit before running destructive commands.

Risk: Generated file overwrite examples can replace existing project files such as .gitignore.

Mitigation: Review the proposed file content and preserve existing files before applying overwrite commands.

Risk: Broad command execution can affect the current repository or shell environment.

Mitigation: Use the skill only for explicit Git tasks and review proposed commands before execution.

## Reference(s):

- [Detailed Git helper examples](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-helper-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable Git or shell examples that should be reviewed before running.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
