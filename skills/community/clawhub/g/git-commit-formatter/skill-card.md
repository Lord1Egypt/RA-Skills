## Description:

Formats Conventional Commits messages from Git diffs, file lists, or written change descriptions, including type, optional scope, subject, and body.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wipal](https://clawhub.ai/user/wipal)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to turn Git diffs, file lists, or written change descriptions into consistent Conventional Commits messages for review, changelog generation, and CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes unrelated whitelist and gateway auto-add instructions that could allow skill additions without user confirmation.

Mitigation: Review before installing, remove or isolate the whitelist/gateway section, and do not let the formatter modify gateway configuration or add skills automatically.

Risk: Generated commit messages may misclassify change type, scope, or impact when input is ambiguous or incomplete.

Mitigation: Review the proposed commit message against the diff and ask for clarification when file paths or the change type are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wipal/skills/git-commit-formatter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown commit message with an optional body and issue references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commit subjects are constrained to 50 characters; optional body lines are constrained to 72 characters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
