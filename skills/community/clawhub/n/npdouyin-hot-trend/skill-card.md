## Description:

Fetches Douyin hot-search and trending-list data, including ranked titles, popularity values, detail links, tags, content types, and cover image URLs when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezi1985201](https://clawhub.ai/user/yezi1985201)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media operators use this skill to retrieve current Douyin trend rankings for hotspot tracking, content trend analysis, marketing planning, and social media operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled automation can write output files and run helper scripts with unvalidated input.

Mitigation: Review cron and helper scripts before execution, use the basic Douyin fetch path when only public trend data is needed, and avoid passing untrusted arguments to helper scripts.

Risk: The included Telegram automation prepares messages for a fixed chat_id.

Mitigation: Do not connect the generated messaging output to downstream automation unless the configured recipient is intentionally yours.

Risk: Douyin public web response formats and access controls may change or rate-limit frequent requests.

Mitigation: Treat fetched trend data as time-sensitive external data, handle empty or failed responses, and keep request frequency reasonable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezi1985201/skills/npdouyin-hot-trend)
- [Douyin web data source](https://www.douyin.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files]

**Output Format:** [Plain text trend listings, Markdown messages, and JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trend records may include rank, title, popularity, link, cover, label, type, timestamp, timezone, and messaging fields.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
