## Description:

GitHub Smart Code Digest monitors GitHub repositories for commits and pull requests, runs AI-assisted code review, creates visual review cards, and publishes summarized reports to Feishu Wiki.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering teams, technical leads, and open source maintainers use this skill to aggregate GitHub PR activity, review findings, visual digest cards, and daily or weekly Feishu Wiki reports for code quality tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses GitHub and Feishu credentials while collecting repository data and publishing review results.

Mitigation: Use trusted, pinned dependencies; scope GitHub and Feishu credentials to the intended repositories and Wiki space; and confirm Feishu Wiki reader access before enabling publishing.

Risk: The skill uses shell commands, scheduled execution, and Feishu Wiki writes in ways the security summary says are not tightly scoped.

Mitigation: Review the skill before installation, avoid sensitive repositories until shell input validation and private per-run temporary files are added, and enable cron only after the target scope is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/github-smart-code-digest)
- [README.md](artifact/README.md)
- [workflow.json](artifact/workflow.json)
- [Provenance unavailable](evidence.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, structured JSON review summaries, shell command guidance, and PNG digest card artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters lower-confidence review findings and can publish scheduled daily or weekly Feishu Wiki reports.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, workflow.json, and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
