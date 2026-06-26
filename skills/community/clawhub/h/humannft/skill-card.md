## Description: <br>
Browse, mint, buy, sell, and trade human NFTs on the HumanNFT marketplace (humannft.ai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSmartApe](https://clawhub.ai/user/TheSmartApe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to browse HumanNFT marketplace data and prepare minting, listing, buying, selling, transfer, portfolio, sync, and webhook operations for HumanNFT assets on Base mainnet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real-money NFT trading and wallet transactions on Base mainnet. <br>
Mitigation: Use a dedicated low-balance wallet and require explicit approval before each signature, mint, buy, list, cancel, price update, transfer, or webhook registration. <br>
Risk: The required HumanNFT API key can authorize marketplace actions if exposed or misused. <br>
Mitigation: Keep HUMANNFT_API_KEY revocable, store it only in the agent runtime environment, and rotate it if exposure is suspected. <br>
Risk: The artifact references an external MCP package for 21 tools. <br>
Mitigation: Verify the external MCP package before running it in an agent environment. <br>


## Reference(s): <br>
- [HumanNFT Marketplace](https://humannft.ai) <br>
- [HumanNFT API](https://humannft.ai/api) <br>
- [HumanNFT Agent Registration API](https://humannft.ai/api/agents/register) <br>
- [ClawHub Skill Page](https://clawhub.ai/TheSmartApe/humannft) <br>
- [TheSmartApe Publisher Profile](https://clawhub.ai/user/TheSmartApe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, code, markdown] <br>
**Output Format:** [Markdown with inline code blocks, API request examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require HUMANNFT_API_KEY and explicit wallet approval for real on-chain actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
