## Description:

Operate Nodit Web3 Data API reads through UXC with a curated OpenAPI schema, API-key auth, and overlap-aware guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure UXC access to Nodit and perform read-only multichain entity, account, native balance, transaction history, token metadata, and token price lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wallet addresses, contract addresses, chain and network names, and lookup inputs to the third-party Nodit API.

Mitigation: Use the skill only when sharing those lookup inputs with Nodit is acceptable for the task and environment.

Risk: Local UXC authentication or host binding mistakes can cause failed or unintended API requests.

Mitigation: Configure the Nodit API key through the documented X-API-KEY credential flow and validate the active binding before use.

Risk: Hosted schema changes can reduce reproducibility.

Mitigation: Prefer the packaged curated OpenAPI schema or a pinned schema source for reproducible operation coverage.

Risk: Nodit plan limits can return HTTP 429 responses, especially for lookupEntities.

Mitigation: Back off on rate-limit responses, avoid hot-loop retries, and use chain-specific reads when the target network is already known.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/nodit-web3.openapi.json)
- [Nodit Introduction](https://developer.nodit.io/en/guides/overview/introduction)
- [Nodit Entity Lookup Docs](https://developer.nodit.io/reference/multichain_lookupentities)
- [Nodit Web3 Data Docs](https://developer.nodit.io/reference/gettransactionsbyaccount)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/nodit-openapi-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Nodit Web3 Data API operations through UXC using X-API-KEY authentication.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
