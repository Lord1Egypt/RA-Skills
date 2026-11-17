## Description:

Audits merged GitCode pull requests across one or more repositories for review, labeling, test, size, issue-linking, and title/description quality, then outputs the findings as a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to sample or inspect merged GitCode pull requests across repositories and summarize quality/compliance concerns in Markdown or CSV tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The GitCode token can grant access to private pull request metadata visible to that token.

Mitigation: Use a read-only, least-privilege token scoped only to repositories intended for audit.

Risk: Optional file output writes results locally and may overwrite an existing Markdown or CSV file.

Mitigation: Choose output paths deliberately and review destination files before using --output.

Risk: Date ranges are interpreted using Asia/Shanghai time, which can differ from a user's local timezone.

Mitigation: State audit windows with explicit dates and account for the Asia/Shanghai interpretation when reviewing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoxj/skills/gitcode-pr-audit)
- [GitCode personal access token settings](https://gitcode.com/setting/token-classic)
- [GitCode API base endpoint](https://api.gitcode.com/api/v5)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, Shell commands, Guidance]

**Output Format:** [Markdown table on stdout, with optional Markdown or CSV file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GITCODE_TOKEN environment variable and at least one owner/repo target.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
