## Description:

Deep research across Reddit, X/Twitter, Hacker News, YouTube, Polymarket, and the web from the last 30 days that synthesizes findings into a grounded, cited briefing for trends, competitive analysis, latest-topic research, and tool or product comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ralph-oei](https://clawhub.ai/user/ralph-oei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users can use this skill to gather recent multi-source research on trends, news, competitive questions, recommendations, and product comparisons. It produces a cited briefing from public discussion, search, video, prediction-market, and web sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics are sent to external services used by the skill.

Mitigation: Avoid confidential, regulated, or sensitive topics unless the destination services are approved for that use.

Risk: X search uses session cookie values that are passed to a local command.

Mitigation: Enable X search only when needed, use low-sensitivity accounts where possible, and revoke or rotate session credentials after use.

Risk: Research reports are saved automatically under ~/Documents/Last30Days.

Mitigation: Review saved reports before sharing and choose an alternate save directory when local persistence is not appropriate.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ralph-oei/skills/last30)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown briefing with cited sections and optional JSON result payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Auto-saves a Markdown report under ~/Documents/Last30Days unless a different save directory is supplied.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
