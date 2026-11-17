## Description:

Full access to Moon Banking API endpoints for data about every bank on Earth, including stories, votes, scores, search, country overviews, world overview, crypto-friendliness, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanwall](https://clawhub.ai/user/juanwall)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to query Moon Banking data about banks, countries, stories, votes, rankings, scores, search results, and global banking overviews through the Moon Banking API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid, sensitive Moon Banking API key to query an external banking data API.

Mitigation: Review the skill before installation, use a dedicated low-privilege API key when available, and avoid sending personal account details or confidential banking questions.

Risk: The examples place the bearer token in curl command-line arguments.

Mitigation: Rewrite commands to avoid exposing the token in shell history, process listings, logs, or shared transcripts.

Risk: The broad auto-use guidance could cause unintended API calls for general banking questions.

Mitigation: Require explicit confirmation before the agent queries the external API, especially for sensitive or paid-key workflows.

## Reference(s):

- [Moon Banking OpenClaw Skill Documentation](https://docs.moonbanking.com/openclaw-skill)
- [Moon Banking API Base URL](https://api.moonbanking.com/v1)
- [Moon Banking Pro Plan](https://moonbanking.com/pro)
- [Moon Banking API Key Management](https://moonbanking.com/settings/api/manage-api-keys)
- [ClawHub Skill Page](https://clawhub.ai/juanwall/skills/moonbanking)
- [ClawHub Publisher Profile](https://clawhub.ai/user/juanwall)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline bash commands and summarized API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and the MOON_BANKING_API_KEY environment variable.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
