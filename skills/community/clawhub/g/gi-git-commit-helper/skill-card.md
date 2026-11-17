## Description:

Generate descriptive commit messages by analyzing git diffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laimiaohua](https://clawhub.ai/user/laimiaohua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect staged or unstaged git diffs and draft concise Conventional Commits messages for commit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git diffs may include sensitive implementation details or accidental secrets.

Mitigation: Review the diff before invoking the skill and remove or redact sensitive changes when necessary.

Risk: Generated commit messages may use an undesired language or omit nuance from complex changes.

Mitigation: Specify the preferred language and review the proposed subject and body before committing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with Conventional Commits examples and optional git diff commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Chinese or English commit subjects depending on the user's request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
