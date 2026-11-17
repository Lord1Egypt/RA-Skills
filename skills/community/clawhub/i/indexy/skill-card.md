## Description:

Indexy helps agents manage, create, update, and analyze custom cryptocurrency indices through Indexy API and Web3 authentication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsantana](https://clawhub.ai/user/hsantana)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to create and rebalance public crypto indices, inspect agent-owned indices, and analyze public index, KPI, and mindshare data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Create and update requests can publish or change public crypto index portfolios.

Mitigation: Require review of the intended index composition, methodology, and rebalance details before authenticated create or update requests are sent.

Risk: API keys and Web3 signatures can authorize account-specific actions.

Mitigation: Store credentials securely, avoid exposing them in logs or user-facing content, and send API requests only to the documented Indexy API domain.

Risk: A full rebalance update replaces the complete asset composition.

Mitigation: Provide the complete asset list with weights summing to 100 and confirm that omitted assets are intended to be removed.

## Reference(s):

- [Indexy Skill Page](https://clawhub.ai/hsantana/skills/indexy)
- [Indexy API Documentation](https://docs.indexy.xyz/api)
- [CoinGecko Networks API](https://docs.coingecko.com/reference/networks-list)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to make authenticated state-changing API requests for public crypto index creation and updates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
