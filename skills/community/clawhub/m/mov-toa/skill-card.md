## Description:

Real-time crypto news API guidance for fetching market updates, searching by keyword, filtering by coin, and paginating 6551-compatible responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyboundyi](https://clawhub.ai/user/skyboundyi)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agent builders use this skill to query a third-party crypto-news API for recent market events, keyword searches, coin-specific news, and structured response fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and coin filters are sent to a documented third-party API.

Mitigation: Avoid sending private account data, API keys, wallet information, or other sensitive text in API searches.

Risk: Crypto-news results may affect market interpretation or trading decisions.

Mitigation: Review returned sources and timestamps before using the information in decision-making workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skyboundyi/skills/mov-toa)
- [Publisher profile](https://clawhub.ai/user/skyboundyi)
- [Documented API base URL](https://web-production-666f44.up.railway.app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with inline curl commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes GET and POST requests for health checks, latest news, advanced search, coin filters, and pagination.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
