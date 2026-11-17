## Description:

This skill helps agents extract structured Google Maps review data for local businesses, brands, venues, competitors, and other place-based research tasks through BrowserAct's Google Maps Reviews API template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phheng](https://clawhub.ai/user/phheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect public Google Maps review fields for local business analysis, reputation monitoring, competitive benchmarking, sentiment analysis, market research, and service quality audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation may lead users to share BROWSERACT_API_KEY conversationally.

Mitigation: Configure BROWSERACT_API_KEY through a protected environment or secret manager and rotate the key if it has already been shared in chat.

Risk: Review search terms are sent to BrowserAct and results may include public reviewer profile data.

Mitigation: Use the skill only when the user accepts sending business or review queries to BrowserAct and receiving public reviewer profile fields.

Risk: The security verdict is suspicious despite no listed risk findings.

Mitigation: Review before installing and scan the skill before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phheng/skills/google-maps-reviews-api-skill)
- [Publisher Profile](https://clawhub.ai/user/phheng)
- [BrowserAct API Key Console](https://www.browseract.com/reception/integrations)
- [BrowserAct Workflow API Endpoint](https://api.browseract.com/v2/workflow)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Text, JSON, Guidance]

**Output Format:** [Terminal status logs followed by structured review data or JSON returned by the BrowserAct workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python and BROWSERACT_API_KEY; accepts keywords, language, and country arguments; automatic retry is limited to one retry for non-authorization failures.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
