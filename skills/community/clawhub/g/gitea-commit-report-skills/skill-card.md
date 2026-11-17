## Description:

Collects commit activity from visible Gitea repositories, uses AI to summarize project progress, and prepares HTML email reports for repository administrators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering team leads use this skill to collect recent Gitea repository activity, summarize member contributions and risks, and send periodic progress reports to repository administrators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect private repository activity across all visible repositories and email reports without clear confirmation.

Mitigation: Use a read-only Gitea token limited to the intended repositories and confirm repository scope and recipients before sending reports.

Risk: HTML report content may include repository data that has not been sufficiently escaped or reviewed.

Mitigation: Review and fix HTML escaping before use in shared or sensitive environments, and inspect generated reports before distribution.

Risk: Temporary report files, dependency ranges, fallback URLs, or environment file permissions may expose operational data or reduce deployment assurance.

Mitigation: Review temp-file handling, dependency pinning, the hard-coded fallback URL, and .env file permissions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/myd2002/skills/gitea-commit-report-skills)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON AI summary requirements, and generated HTML email content produced by scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GITEA_URL and a GITEA_TOKEN with repository read access; email sending depends on the separate imap-smtp-email skill.]

## Skill Version(s):

1.2.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
