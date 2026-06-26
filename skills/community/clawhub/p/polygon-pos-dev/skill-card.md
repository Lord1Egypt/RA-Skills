## Description: <br>
Comprehensive guide for Polygon PoS blockchain development, including Foundry deployment, Amoy testnet testing, faucet use, and Polygonscan verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AkshatGada](https://clawhub.ai/user/AkshatGada) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-contract engineers use this skill to set up Foundry projects, test on Polygon Amoy, deploy to Polygon PoS, and verify contracts on Polygonscan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses private keys and .env files for deployment workflows. <br>
Mitigation: Use a dedicated low-balance deployment wallet and never commit or share .env files. <br>
Risk: Deployment commands with --broadcast or cast send can submit live blockchain transactions. <br>
Mitigation: Confirm the network, wallet address, gas cost, and transaction details before broadcasting; test on Amoy before mainnet. <br>
Risk: The workflow installs Foundry through a remote installer command. <br>
Mitigation: Install Foundry only from official sources before running the skill's deployment guidance. <br>


## Reference(s): <br>
- [Foundry Deployment Guide for Polygon PoS](references/foundry-deployment.md) <br>
- [Testing Strategies for Polygon PoS](references/testing-strategies.md) <br>
- [Contract Verification on Polygonscan](references/contract-verification.md) <br>
- [Foundry Book](https://book.getfoundry.sh/) <br>
- [Polygon Documentation](https://docs.polygon.technology/) <br>
- [Polygonscan API Documentation](https://docs.polygonscan.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Solidity, TOML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands requiring PRIVATE_KEY and POLYGONSCAN_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
