## Description: <br>
Alchemy (alchemy.com). Use this skill for ANY Alchemy request - searching and reading data. Whenever a task involves Alchemy, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query Alchemy data through an OOMOL-connected account and the oo CLI. It supports read-only Ethereum mainnet requests for asset transfers, NFT ownership, NFT metadata, token balances, and token metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires trust in OOMOL and uses an OOMOL-connected Alchemy account through the oo CLI. <br>
Mitigation: Install it only when OOMOL is trusted, review OOMOL sign-in and Alchemy connection setup before use, and rely on the server-side credential flow rather than handling raw API tokens. <br>
Risk: Wallet or contract addresses may be sensitive or unnecessary for some requests. <br>
Mitigation: Provide wallet or contract addresses only when they are relevant to the user's query. <br>
Risk: Alchemy connection, authentication, or billing state can prevent connector actions from completing. <br>
Mitigation: Use the documented setup fallbacks only after a command fails with the matching auth, connection, scope, credential, or billing error. <br>


## Reference(s): <br>
- [Alchemy skill page](https://clawhub.ai/oomol/oo-alchemy) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Alchemy homepage](https://www.alchemy.com) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
