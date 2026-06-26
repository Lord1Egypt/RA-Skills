## Description: <br>
Fetch, filter, dedup, and deliver curated news briefings to Telegram. Benzinga for finance, AI News RSS for tech. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hohobohan](https://clawhub.ai/user/hohobohan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run scheduled finance and AI/tech news curation workflows that fetch public news, filter low-quality items, format concise briefings, and deliver them to Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled delivery can post generated briefings to an unintended Telegram chat or channel. <br>
Mitigation: Confirm the Telegram destination before enabling recurring runs, and use manual review if automatic posting is not desired. <br>
Risk: Live public-news curation can summarize incomplete, stale, or low-quality sources. <br>
Mitigation: Keep the source links in each briefing, filter low-quality categories as documented, and review important items before relying on them. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown news briefing with source names and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scheduled Telegram delivery; each run selects 6-8 finance and AI/tech items.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
