## Description:

Monitors TikTok for brand mentions and product discussions using apidojo's TikTok scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Brand managers, community teams, crisis communications teams, and product marketing teams use this skill to collect TikTok brand mentions, classify sentiment and content type, and flag high-reach praise or criticism.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify credentials can be exposed when tokens are passed in URLs or stored in shared environment files.

Mitigation: Prefer Apify MCP or API calls that send the token in an Authorization header, use a least-privilege Apify token, and avoid shared .env files.

Risk: Submitted keywords and collected TikTok results may be visible to Apify or Apidojo under their policies.

Mitigation: Review the skill before use with sensitive brands, unreleased products, incident terms, or regulated data, and assume third-party processing applies.

Risk: Lexical sentiment, virality, and crisis classifications can mislabel TikTok content or overstate urgency.

Mitigation: Treat crisis alerts as triage signals and review sampled posts, creator context, and engagement patterns before taking external action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/monitoring-tiktok-mentions-of-brand)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Analysis, Files, Guidance]

**Output Format:** [Markdown report with tables, inline shell commands, and optional JSON or CSV result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Apify inputs such as keywords, start URLs, location, sort order, and max item count; produces sentiment, content type, virality, and crisis-alert summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
