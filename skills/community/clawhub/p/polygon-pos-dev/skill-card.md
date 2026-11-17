## Description:

Comprehensive guide for Polygon PoS blockchain development using Foundry, including contract deployment, Amoy testnet testing, faucet use, and Polygonscan verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshatgada](https://clawhub.ai/user/akshatgada)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, test, deploy, and verify smart contracts on Polygon PoS with Foundry, primarily on Amoy before mainnet deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install Foundry through a remote shell installer.

Mitigation: Review the installer source and use a verified, pinned installation method in an isolated development environment.

Risk: The skill includes workflows that pass wallet private keys to deployment commands.

Mitigation: Avoid machines or shells that hold valuable keys, prefer keystores or hardware/external signers, and use low-value test keys for Amoy.

Risk: Mainnet deployment commands with `--broadcast` can create irreversible real-funds transactions.

Mitigation: Complete testnet deployment and verification first, review every command and network target, and treat mainnet broadcast steps as final.

## Reference(s):

- [Foundry Deployment Guide for Polygon PoS](references/foundry-deployment.md)
- [Testing Strategies for Polygon PoS](references/testing-strategies.md)
- [Contract Verification on Polygonscan](references/contract-verification.md)
- [Foundry Book](https://book.getfoundry.sh/)
- [Foundry GitHub](https://github.com/foundry-rs/foundry)
- [Polygon Documentation](https://docs.polygon.technology/)
- [Polygon Gas Station](https://gasstation.polygon.technology/)
- [Polygon Faucet](https://faucet.polygon.technology/)
- [Polygonscan API Documentation](https://docs.polygonscan.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, TOML, and Solidity code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes external network, faucet, explorer, and API-key setup steps for Polygon PoS workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
