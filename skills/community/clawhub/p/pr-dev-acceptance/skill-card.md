## Description:

Tests already-deployed development changes from human-approved Bitbucket pull requests against Jira requirements through fresh browser logins and independent final visits, then provides screenshots and a local acceptance report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvolutionor](https://clawhub.ai/user/alvolutionor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA teams use this skill to check approved changes on an existing dev deployment against Jira acceptance criteria and document observed results without deploying or running pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser testing can modify dev test records or expose sensitive information in screenshots.

Mitigation: Use scoped test accounts and permitted records, restore changed data where possible, and keep credentials and reports outside the public repository.

Risk: Optional Jira posting can upload screenshots, publish comments, or transition an issue.

Mitigation: Use least-privilege Jira credentials, review the preview before applying writes, and request a transition only when explicitly authorized.

## Reference(s):

- [Deployed Dev Acceptance on ClawHub](https://clawhub.ai/alvolutionor/skills/pr-dev-acceptance)
- [Jira acceptance comment example](artifact/references/jira-comment-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Local Markdown acceptance report with saved browser screenshots; optional Jira comment draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS, FAIL, or BLOCKED with case evidence and screenshot links; Jira posting or issue transitions require an explicit request.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
