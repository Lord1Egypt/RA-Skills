## Description:

Complete Juicebox V5 protocol skills collection. Build, deploy, and interact with Juicebox projects, revnets, hooks, and omnichain deployments. Includes API reference, implementation details, UI generation, and GraphQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mejango](https://clawhub.ai/user/mejango)

### License/Terms of Use:


## Use Case:

Developers and protocol integrators use this skill to research, configure, deploy, query, and build interfaces for Juicebox V5 projects, revnets, hooks, omnichain deployments, and related wallet flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated wallet UIs and transaction examples can trigger blockchain actions with real assets.

Mitigation: Review every generated transaction path, show explicit confirmation screens, and test with small amounts before production use.

Risk: Bendystraw API keys can be exposed if embedded in frontend code.

Mitigation: Keep API keys server-side, use environment variables, and call Bendystraw through a backend proxy.

Risk: Remote JavaScript dependencies or mutable Solidity imports can change after a template is generated.

Mitigation: Pin, vendor, or bundle dependencies and imports before deploying generated applications or contracts.

Risk: Unsanitized chain, address, calldata, and metadata inputs can misdirect wallet actions or produce misleading UI state.

Mitigation: Validate supported chain IDs, contract addresses, calldata, token metadata, and project identifiers before signing or displaying results.

Risk: Unlimited token approvals can expose users to excessive spending authority.

Mitigation: Prefer bounded approvals and require a clear user acknowledgement before any unlimited approval flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mejango/skills/juicy)
- [Juicebox documentation](https://docs.juicebox.money)
- [Juicebox V5 addresses](https://docs.juicebox.money/dev/v5/addresses)
- [Juicebox protocol GitHub](https://github.com/jbx-protocol)
- [nana-core-v5](https://github.com/Bananapus/nana-core-v5)
- [nana-721-hook-v5](https://github.com/Bananapus/nana-721-hook-v5)
- [revnet-core-v5](https://github.com/rev-net/revnet-core-v5)
- [Bendystraw GraphQL API](https://bendystraw.xyz)
- [Uniswap Permit2](https://github.com/Uniswap/permit2)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with code blocks, configuration snippets, GraphQL queries, shell commands, and standalone HTML, JavaScript, or Solidity examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some generated outputs are wallet-connected templates or blockchain transaction examples and require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
