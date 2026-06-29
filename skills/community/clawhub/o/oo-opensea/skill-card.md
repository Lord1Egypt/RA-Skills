## Description: <br>
OpenSea access for searching and reading NFT, collection, listing, and offer data through the OOMOL opensea connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve OpenSea NFT, collection, trait, rarity, listing, offer, ownership, and search data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive OpenSea credentials through an OOMOL-connected account. <br>
Mitigation: Use the intended OOMOL account and connection, and avoid exposing raw tokens because credentials are injected server-side. <br>
Risk: Connector actions can fail or behave unexpectedly if the live schema, authentication state, connection scope, or billing state has changed. <br>
Mitigation: Inspect the action schema before constructing payloads and use first-time setup or recovery steps only when the matching command failure occurs. <br>
Risk: Future connector actions tagged as write or destructive could affect OpenSea state. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running any action tagged write or destructive. <br>


## Reference(s): <br>
- [ClawHub OpenSea skill page](https://clawhub.ai/oomol/oo-opensea) <br>
- [OpenSea homepage](https://opensea.io) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before running OpenSea actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
