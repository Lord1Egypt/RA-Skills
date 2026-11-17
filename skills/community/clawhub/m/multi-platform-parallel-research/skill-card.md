## Description:

Auto Researcher researches a topic across X/Twitter, Reddit, YouTube, GitHub, Hacker News, Product Hunt, and news sites, then generates structured market, competitor, technical, and user-feedback reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yofoan](https://clawhub.ai/user/yofoan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and market researchers use this skill to gather public signals about a topic across multiple platforms and turn them into structured research reports. It supports market trend research, competitor analysis, technical research, and user feedback summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted research topics may trigger code execution.

Mitigation: Fix the heredoc topic-injection issue before normal use and review topic handling before installing or running the skill.

Risk: Research topics and queries are sent to third-party services.

Mitigation: Do not use sensitive internal project names, customer data, credentials, or confidential plans as research topics.

Risk: Reports and raw data are stored locally under /tmp or a user-selected output directory.

Mitigation: Run the scripts as an unprivileged user and prefer a fixed, trusted output directory with appropriate permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yofoan/skills/multi-platform-parallel-research)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON data files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports and raw research data to local output directories, normally under /tmp.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
