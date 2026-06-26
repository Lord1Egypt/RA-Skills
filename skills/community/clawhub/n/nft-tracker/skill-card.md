## Description: <br>
Track NFT collection prices, floor prices, and sales data for Ethereum collections including BAYC, MAYC, CryptoPunks, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ianalloway](https://clawhub.ai/user/ianalloway) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to get shell commands for checking NFT collection floor prices, volumes, owner counts, floor history, recent sales, and token details from Reservoir and optional OpenSea APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collection slugs, contract addresses, token IDs, and OpenSea authenticated requests may be visible to the relevant API provider. <br>
Mitigation: Review commands before running them and send only NFT identifiers intended for those API providers. <br>
Risk: The OPENSEA_API_KEY value can be exposed if pasted into chat, command history, or logs. <br>
Mitigation: Keep OPENSEA_API_KEY in an environment variable and do not paste the key itself into prompts, scripts, or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ianalloway/nft-tracker) <br>
- [OpenSea API overview](https://docs.opensea.io/reference/api-overview) <br>
- [OpenSea API keys](https://docs.opensea.io/reference/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash code blocks, curl commands, and jq filters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; OpenSea requests optionally use OPENSEA_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
