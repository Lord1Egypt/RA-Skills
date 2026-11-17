## Description:

Scans a user's logged-in social media accounts across Douyin, Xiaohongshu, Weibo, Douban, and Bilibili to compare public activity with likes, favorites, follows, ratings, and other activity, then generates a humorous Mirror Report about persona gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sophie-xin9](https://clawhub.ai/user/sophie-xin9)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for opt-in self-analysis of the user's own social media accounts. It gathers account activity from supported platforms, contrasts public presentation with private preference signals, and produces a shareable Markdown report with data-backed observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged-in browser automation can access private preference and social-graph data from connected social accounts.

Mitigation: Review the skill before installing and require explicit user consent for each platform and data type before collection.

Risk: Raw local exports may contain posts, likes, favorites, follows, ratings, comments, and activity history.

Mitigation: Save only the final report unless raw export is explicitly requested, keep files local, and delete raw data after use.

Risk: The dependency workflow may fetch ManoBrowser during setup without a pinned release.

Mitigation: Pin and review the browser automation dependency before enabling collection on logged-in accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sophie-xin9/skills/magic-mirror)
- [ManoBrowser dependency](https://github.com/ClawCap/ManoBrowser)

## Skill Output:

**Output Type(s):** [markdown, text, JSON, guidance]

**Output Format:** [Markdown Mirror Report with optional local JSON raw-data export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save report and raw collection data under mirror-reports/ during execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
