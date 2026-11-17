## Description:

Notcrawl helps agents search Notion archives, check freshness, inspect pages and databases, export Markdown, run read-only SQL counts, and work with the Notcrawl repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Notcrawl to answer questions from local or API-backed Notion archives, check data freshness, refresh stale archives, and report source gaps before relying on live browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The notcrawl tool can access local Notion archive data and may use a Notion token in API mode.

Mitigation: Install only when that access is intended, keep any NOTION_TOKEN scoped and private, and do not assume API credentials are available.

Risk: SQL access could change local archive data if used outside the documented read-only posture.

Mitigation: Use SQL only for read-only inspection, such as counts, and avoid mutation statements.

Risk: Installing the Go module at latest can change the installed tool over time.

Mitigation: Review the external Go module source or pin a version when reproducible installs are required.

## Reference(s):

- [Notcrawl GitHub Repository](https://github.com/openclaw/notcrawl)
- [Notcrawl ClawHub Skill Page](https://clawhub.ai/openclaw/skills/notcrawl)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and concise source-gap reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report Notion workspace or teamspace names, page and database titles, absolute date spans, counts, and known gaps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
