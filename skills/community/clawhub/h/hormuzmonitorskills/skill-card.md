## Description:

Monitors Strait of Hormuz shipping traffic, market indicators, Iranian sources, and news aggregation, then writes Mandarin-formatted updates to MONITOR_LOG.md and updates website data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xingpt88](https://clawhub.ai/user/xingpt88)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators can use this skill to collect current Strait of Hormuz maritime, geopolitical, insurance, and market signals and maintain a structured monitoring log for a website. It is intended for recurring situational updates rather than authoritative maritime or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run a local deployment script that pushes website data to GitHub and triggers Vercel without a clear approval step.

Mitigation: Use it only in a controlled repository where the deployment script is reviewed and trusted, and require manual review before push or deployment.

Risk: The skill modifies MONITOR_LOG.md and deletes entries older than seven days.

Mitigation: Keep source control history or backups for the log and review generated entries before allowing downstream website updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xingpt88/skills/hormuzmonitorskills)
- [UKMTO JMIC products](https://www.ukmto.org/partner-products/jmic-products)
- [Windward maritime intelligence blog](https://windward.ai/blog/)
- [Tasnim News English](https://www.tasnimnews.ir/en/)
- [Fars News English](https://www.farsnews.ir/en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown log entries and brief alert summaries, with shell command execution guidance for website data updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mandarin summary fields, strict MONITOR_LOG.md formatting, seven-day log trimming, and flash alert checks for oil, vessel-count, ceasefire, breakthrough, or attack signals]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
