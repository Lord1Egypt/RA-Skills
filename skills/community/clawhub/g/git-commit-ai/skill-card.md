## Description:

Generates Angular-style commit messages from staged Git diffs with automatic or user-selected Chinese and English output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenoleee](https://clawhub.ai/user/zenoleee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to analyze staged Git changes and draft concise conventional commit messages with an inferred scope, change type, and language. It can also install a Git prepare-commit-msg hook that reminds users to generate a message during commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Staged diffs may contain secrets or other sensitive code that would be included in the generated prompt.

Mitigation: Review staged changes for secrets before running the skill and remove sensitive content before asking the agent to generate a commit message.

Risk: The optional Git hook is persistent, and forced installation can overwrite an existing prepare-commit-msg hook.

Mitigation: Install the hook only after checking existing hook behavior and avoid --install --force unless the existing hook has been reviewed and backed up.

Risk: Very large diffs can reduce commit-message accuracy.

Mitigation: Split large staged changes into smaller commits before generating a message.

## Reference(s):

- [Angular Commit Convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit)
- [Git diff Documentation](https://git-scm.com/docs/git-diff)
- [ClawHub Skill Page](https://clawhub.ai/zenoleee/skills/git-commit-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prompt text containing a staged diff and instructions, or plain text status/help output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports language selection with auto, zh, or en; optional hook installation writes or updates prepare-commit-msg.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
