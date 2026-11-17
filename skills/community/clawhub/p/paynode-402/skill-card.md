## Description:

Dynamic Premium API Marketplace for AI Agents. Grants access to an ever-expanding registry of real-time external tools (e.g., web search, crypto oracles, web scraping, and more) via USDC micro-payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paynodelabs](https://clawhub.ai/user/paynodelabs)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to discover and invoke paid API marketplace services for live data, external API interactions, and HTTP 402-protected resources using USDC micro-payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses wallet-backed mainnet payment flows that can spend real USDC through third-party CLI operations.

Mitigation: Use a dedicated burner wallet with minimal funds and require explicit user approval for every outbound marketplace lookup and paid API call.

Risk: Unpinned bunx execution can fetch a CLI version that has not been locally reviewed.

Mitigation: Prefer a pinned or locally audited CLI build for production or high-value workflows.

Risk: Private keys may be supplied through CLIENT_PRIVATE_KEY or the documented local config file.

Mitigation: Avoid high-value keys, review local config contents before use, and keep secret material out of logs and shared environments.

## Reference(s):

- [PayNode 402 CLI](https://github.com/PayNodeLabs/paynode-402-cli)
- [ClawHub skill page](https://clawhub.ai/paynodelabs/skills/paynode-402)
- [Publisher profile](https://clawhub.ai/user/paynodelabs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents through wallet configuration, marketplace discovery, paid API execution, and task management workflows.]

## Skill Version(s):

2.7.5 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
