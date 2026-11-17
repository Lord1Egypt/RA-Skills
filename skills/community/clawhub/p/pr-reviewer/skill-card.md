## Description:

Automated GitHub PR code review with diff analysis, lint integration, and structured reports for security issues, error handling gaps, test coverage, and code style in Go, Python, and JavaScript/TypeScript repositories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briancolinger](https://clawhub.ai/user/briancolinger)

### License/Terms of Use:


## Use Case:

Developers and code reviewers use this skill to inspect GitHub pull requests, summarize changed files, flag common security and quality issues, run optional local linters, and create structured review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted pull-request filename can trigger local Python code execution during review.

Mitigation: Do not run the skill on untrusted pull requests until PR file data is passed through stdin, argv, or JSON rather than embedded in Python source.

Risk: The skill uses GitHub repository access and can post review comments when run with write-capable credentials.

Mitigation: Run it with a low-privilege GitHub account or token and avoid environments that contain unrelated secrets.

Risk: Automated or scheduled review could repeatedly process unsafe pull-request data before human inspection.

Mitigation: Avoid cron or unattended automation until the filename-to-Python injection issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briancolinger/skills/pr-reviewer)
- [ClawHub publisher profile](https://clawhub.ai/user/briancolinger)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown reports, JSON status summaries, and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes review state JSON and Markdown reports to configured local paths; can post a saved report as a GitHub PR comment.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
