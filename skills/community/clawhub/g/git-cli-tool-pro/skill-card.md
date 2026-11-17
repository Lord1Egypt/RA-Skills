## Description:

Git命令行助手专业版 helps enterprise development teams automate Git CLI workflows, diagnose repository health, standardize branch workflows, troubleshoot issues, and manage multiple repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to automate routine Git work, run repository diagnostics, standardize feature, hotfix, and release workflows, and manage multiple repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated Git-changing operations can stage, commit, push, rebase, tag, or delete branches in the wrong repository.

Mitigation: Require explicit confirmation and review git status, diffs, target repository, and target branch before commits, pushes, rebases, tags, branch deletion, or multi-repo cleanup.

Risk: Broad staging and persistent credential storage can expose unintended files or credentials.

Mitigation: Avoid git add -A defaults, review staged files before committing, and do not use the persistent Git credential store unless it matches the deployment security policy.

## Reference(s):

- [Detailed reference](references/detail.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/git-cli-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Git-changing operations; review the target repository, branch, and diff before execution.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
