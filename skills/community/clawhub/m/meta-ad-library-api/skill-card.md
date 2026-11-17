## Description:

Search the Meta Ad Library by keyword or Facebook Page id and walk full cursor pagination through every ad, with creative, run dates, platforms and political spend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and research agents use this skill to search public Facebook and Instagram ad data, retrieve ads for a specific Facebook Page, inspect one ad by archive id, and collect structured creative, platform, run-date, and political disclosure data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ad research queries, page IDs, ad archive IDs, and the Scavio API key are sent to Scavio.

Mitigation: Use an approved Scavio account, keep SCAVIO_API_KEY in a secret store or environment variable, and avoid submitting data that should not be shared with the third-party API provider.

Risk: Deep cursor pagination consumes one credit per page and can exceed the user's intended budget.

Mitigation: Set a page or credit budget before crawling, cap pagination loops, and stop when has_next_page is false.

Risk: Meta-reported totals and political disclosure fields can be misread; capped totals are not exact and commercial ads generally do not publish spend or reach.

Mitigation: Present capped totals as capped estimates, never treat null spend or reach as zero, and request political_and_issue_ads when spend and reach disclosures are required.

Risk: Ad creative may be copyrighted third-party content.

Mitigation: Quote creative only for analysis and do not present copied ad creative as the user's own work.

## Reference(s):

- [Scavio Meta Ads Search documentation](https://scavio.dev/docs/meta-ads-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=meta-ad-library-api)
- [Scavio rate limits](https://scavio.dev/docs/rate-limits?utm_source=agent-skills&utm_medium=skill&utm_campaign=meta-ad-library-api)
- [ClawHub skill page](https://clawhub.ai/scavio-ai/skills/meta-ad-library-api)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with bash, Python, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; API calls return structured JSON envelopes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
