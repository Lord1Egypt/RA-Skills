## Description:

西柚-关键词洞察 helps agents query Xiyou Insights through LinkFox for Amazon ASIN and keyword traffic, ranking, BSR, ABA trend, competition, and suggested CPC analysis across supported marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers, marketplace analysts, and agent users use this skill to retrieve Xiyou ASIN and keyword analytics for product research, keyword discovery, trend review, and competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys, Xiyou client credentials, and phone-login flows.

Mitigation: Install only when the publisher is trusted; keep credentials in environment variables and avoid placing secrets in chats or source control.

Risk: The skill can invoke billing-related flows and API calls that may consume credits or require payment.

Mitigation: Confirm endpoint settings, plan selection, payment method, and repeated data requests before proceeding.

Risk: Full API responses may be stored locally without retention limits.

Mitigation: Review saved JSON files for sensitive marketplace data and delete or restrict access according to local retention needs.

Risk: Security evidence flags suspicious behavior involving credential handling, billing, feedback reporting, and persistent local storage.

Mitigation: Review the skill before deployment and disable or avoid automatic feedback reporting where local policy requires it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-xiyou-dongcha)
- [Xiyou API Reference](references/api.md)
- [Authentication and Billing Onboarding](references/onboarding.md)
- [LinkFox API Key Guide](https://skill.linkfox.com/linkfoxskills/guide.htm)
- [Xiyou OpenAPI Console](https://www.xydc.com/openapi?xiyou-insights-web=%2Fopenapi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON files]

**Output Format:** [Markdown guidance with shell commands and JSON response summaries; full API responses are persisted as JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses of 8 KB or less are printed inline; larger responses are summarized while the full JSON is saved under a LinkFox session data directory.]

## Skill Version(s):

0.0.8 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
