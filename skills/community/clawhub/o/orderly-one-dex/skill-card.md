## Description:

Create and manage a custom DEX using Orderly One API - deployment, custom domains, graduation, and theming.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers and DEX operators use this skill to create, configure, deploy, update, and graduate white-label perpetuals DEXs through Orderly One.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet signatures, token transfers, receiver addresses, and DEX updates can affect funds or deployed sites.

Mitigation: Confirm every signature request, transaction hash, receiver address, transfer amount, and DEX update before submission.

Risk: Analytics script configuration can affect end-user privacy.

Mitigation: Review any analyticsScript content and privacy implications before adding it to a deployed DEX.

## Reference(s):

- [Orderly One API mainnet base URL](https://dex-api.orderly.network)
- [Orderly One API testnet base URL](https://testnet-dex-api.orderly.network)
- [Orderly DEX creator default theme](https://raw.githubusercontent.com/OrderlyNetworkDexCreator/dex-creator-template/refs/heads/main/app/styles/theme.css)
- [Orderly registration nonce endpoint](https://api.orderly.org/v1/registration_nonce)
- [Orderly register account endpoint](https://api.orderly.org/v1/register_account)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with endpoint references, workflow steps, and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multipart form fields, wallet-signature steps, token-transfer checks, deployment polling, and DEX customization guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
