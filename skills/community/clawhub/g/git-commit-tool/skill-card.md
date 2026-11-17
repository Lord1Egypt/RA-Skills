## Description:

Execute git commits with Conventional Commit analysis, intelligent staging, and commit message generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangchencheng](https://clawhub.ai/user/wangchencheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect git changes, stage logical groups of files, and create Conventional Commit messages, including Simplified Chinese descriptions and an AI-GEN footer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can stage files and create git commits, which can permanently record unintended changes if the diff is not reviewed.

Mitigation: Review git status, diffs, and staged files before committing; stage only the intended logical change.

Risk: Generated commit conventions may not match every repository, especially Simplified Chinese messages or AI-GEN footers.

Mitigation: Override the generated message, language, or footer to match the repository policy before running git commit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangchencheng/skills/git-commit-tool)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with git shell commands and Conventional Commit message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commit messages are expected in Simplified Chinese and may include an AI-GEN footer.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
