## Description:

Guides agents in retrieving public Google Play app data through ReplyNodes' read-only API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search Android apps and inspect public app details, reviews, permissions, data safety, availability, categories, and developer listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: App lookup terms and package IDs are sent to ReplyNodes.

Mitigation: Confirm this data sharing is acceptable before making requests.

Risk: An optional ReplyNodes API key could be exposed in commands, logs, or reports.

Mitigation: Keep any key in an environment variable and do not include it in URLs or shared output.

Risk: Batch requests may encounter rate limits or metered costs.

Mitigation: Check the live capabilities endpoint before a batch and bound pagination and request volume.

## Reference(s):

- [Googleplay Public Data Api on ClawHub](https://clawhub.ai/replynodes-ai/skills/googleplay-public-data-api)
- [ReplyNodes Google Play API capabilities](https://api.replynodes.com/v1/googleplay/capabilities)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with API request examples and public-data summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public app data; live responses are normalized JSON.]

## Skill Version(s):

1.1.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
