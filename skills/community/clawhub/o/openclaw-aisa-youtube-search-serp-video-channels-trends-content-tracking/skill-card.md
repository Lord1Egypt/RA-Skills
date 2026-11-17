## Description:

YouTube SERP Scout for agents. Search top-ranking videos, channels, and trends for content research and competitor tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xjordansg-yolo](https://clawhub.ai/user/0xjordansg-yolo)

### License/Terms of Use:


## Use Case:

External developers, marketers, and content researchers use this skill to query YouTube SERP results through AIsa for content planning, competitor monitoring, trend discovery, keyword research, and regional audience research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, country and language filters, and authenticated requests are sent to AIsa.

Mitigation: Avoid sending sensitive search terms, keep AISA_API_KEY private and scoped where possible, and review AIsa terms before use.

Risk: API usage may incur pay-as-you-go costs.

Mitigation: Monitor usage.cost and usage.credits_remaining in responses and apply account-level spending controls where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xjordansg-yolo/skills/openclaw-aisa-youtube-search-serp-video-channels-trends-content-tracking)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY; supports query, country, language, and filter-token parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
