## Description:

Monitor GitHub Trending daily and use AI to summarize notable projects with topic tags, innovation scoring, star-growth signals, and formatted digest output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nima54851](https://clawhub.ai/user/nima54851)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, investors, and technology enthusiasts use this skill to monitor GitHub Trending, classify notable open-source projects, and produce a daily markdown digest for trend tracking and watch-list decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled use can create daily markdown files in ~/github-digest.

Mitigation: Confirm the output directory and retention expectations before enabling a recurring schedule.

Risk: Setting GITHUB_TOKEN gives the workflow access to the user's GitHub API quota.

Mitigation: Use a token with the minimal needed scope, or omit the token when public Trending data is sufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nima54851/skills/lingxi-github-daily-digest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown digest with ranked projects, topic summaries, insights, and recommended projects to watch.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save a dated daily digest under ~/github-digest when scheduled.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
