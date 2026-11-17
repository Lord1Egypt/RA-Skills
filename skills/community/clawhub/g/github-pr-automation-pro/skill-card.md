## Description:

Automate GitHub pull request workflows for creating templated PRs, applying branch-based labels, and monitoring review, merge, and CI status through the GitHub CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create GitHub pull requests from templates, add labels based on branch naming, and check whether a pull request is ready to merge. Review unsupported advertised workflows before relying on auto-merge, approval, batch, or metrics behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports unvalidated user input in shell-string command execution while using an authenticated GitHub CLI session.

Mitigation: Review and fix scripts before use by replacing shell-string execution with argument-array execution, validating PR numbers and branch, template, and label inputs, and using least-privileged GitHub credentials.

Risk: The artifact advertises auto-merge, approval, batch processing, and metrics workflows that are not supported by the bundled scripts.

Mitigation: Treat those workflows as unavailable unless corresponding reviewed scripts or integrations are added and validated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dagangtj/skills/github-pr-automation-pro)
- [automation_rules.json](references/automation_rules.json)
- [feature.md](references/pr_templates/feature.md)
- [bugfix.md](references/pr_templates/bugfix.md)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub CLI commands and local PR templates; authenticated GitHub access is required for script execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
