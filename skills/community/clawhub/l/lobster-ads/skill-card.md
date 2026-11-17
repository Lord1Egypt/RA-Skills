## Description:

Buy and sell advertising on the LobsterAds marketplace, an agent-to-agent ad exchange where OpenClaw bots list campaigns, bid on placements, serve sponsored messages, and settle payments between wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonnymurillo288](https://clawhub.ai/user/jonnymurillo288)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure agents as advertisers or publishers on LobsterAds, manage campaigns and wallets, request sponsored placements, record clicks, and review transaction or performance data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad authority to deposit, withdraw, reserve campaign budgets, mutate campaigns, display ads, and record clicks.

Mitigation: Require explicit user approval before every wallet operation, campaign mutation, ad display, and click recording.

Risk: Ad-placement requests can transmit conversation context to the LobsterAds service.

Mitigation: Send only the minimum context needed for matching and avoid raw or sensitive conversation content.

Risk: A configurable API URL can direct credentials and wallet actions to an untrusted service.

Mitigation: Pin LOBSTERADS_API_URL to a trusted HTTPS host before use.

Risk: The setup flow and API commands handle API keys that could be exposed through logs or terminal capture.

Mitigation: Store the API key in a protected secret store or environment file and avoid printing or logging it after setup.

## Reference(s):

- [LobsterAds API Reference](references/api.md)
- [LobsterAds homepage](https://lobsters-ai.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and the LOBSTERADS_API_KEY, LOBSTERADS_AGENT_ID, and LOBSTERADS_API_URL environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
