## Description:

Interact with the Noya AI agent for crypto trading, prediction markets, token analysis, and DCA strategies via curl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ali-hajeh](https://clawhub.ai/user/ali-hajeh)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send authenticated Noya agent messages, inspect crypto portfolios, analyze tokens and markets, manage DCA strategies, and work with Polymarket or Rain prediction markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can send the Noya API key and financial prompts to an unvalidated override URL if NOYA_BASE_URL is set.

Mitigation: Do not set NOYA_BASE_URL unless the destination is fully trusted, and use a short-lived, low-privilege Noya API key.

Risk: Wallet, portfolio, market, and trading instructions are shared with the remote Noya service.

Mitigation: Avoid sending unnecessary sensitive details, confirm every transaction manually, and rotate the API key if it may have been exposed.

Risk: The release evidence reports a default-domain mismatch that users should review before installation.

Mitigation: Review the configured service URL and the skill documentation before enabling the skill in an agent environment.

## Reference(s):

- [Noya Agent API Reference](reference.md)
- [Noya Agent Homepage](https://agent.noya.ai)
- [Noya Agent ClawHub Listing](https://clawhub.ai/ali-hajeh/skills/noya-agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and parsed streaming API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOYA_API_KEY plus curl and jq; the helper script emits messages, tool results, progress updates, errors, and interrupt prompts.]

## Skill Version(s):

1.0.13 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
