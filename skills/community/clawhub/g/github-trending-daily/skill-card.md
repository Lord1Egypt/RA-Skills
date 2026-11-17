## Description:

Fetches daily, weekly, or monthly GitHub Trending projects and prepares Markdown summaries for DingTalk delivery or preview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangzhiyu](https://clawhub.ai/user/jiangzhiyu)

### License/Terms of Use:


## Use Case:

Developers and team maintainers use this skill to monitor GitHub Trending repositories and share daily, weekly, or monthly Markdown summaries with a DingTalk group.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships with a live DingTalk webhook token and can send messages to a fixed external destination.

Mitigation: Rotate and replace the embedded webhook with a user-controlled secret, preferably loaded from an environment variable, before publication or use in a real workspace.

Risk: Default command and cron examples may send GitHub Trending summaries when executed.

Mitigation: Review the destination and run dry-run or no-push mode before enabling scheduled delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiangzhiyu/skills/github-trending-daily)
- [GitHub Trending](https://github.com/trending)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown summaries with command-line status text and cron examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports daily, weekly, monthly, dry-run, and no-push modes.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
