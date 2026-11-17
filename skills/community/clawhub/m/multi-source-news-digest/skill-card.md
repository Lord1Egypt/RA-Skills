## Description:

Aggregates and scores technology news daily from RSS feeds, GitHub releases, and web sources, producing customizable filtered digests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyh-pan](https://clawhub.ai/user/pyh-pan)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to fetch, score, filter, and format technology news from configured RSS, GitHub, and web sources into daily digests or item lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches remote news data through generated python -c subprocess execution.

Mitigation: Replace generated subprocess fetchers with direct safe HTTP and RSS library calls, and validate or allowlist source URLs before fetching.

Risk: The packaged trigger configuration enables an auto-start daily cron action with Telegram notifications.

Mitigation: Disable auto-start scheduling and notifications by default unless the installer explicitly opts in and reviews the destination channel.

Risk: Dependencies are not pinned consistently across the packaged Python and package metadata.

Mitigation: Pin dependencies with the correct package manager and review updates before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pyh-pan/skills/multi-source-news-digest)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown digest text or JSON status and news item data from command-line actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports digest, list, and refresh actions; output depends on configured sources, scoring threshold, and network availability.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/config.json, artifact/package.json, and artifact/skill.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
