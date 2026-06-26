## Description: <br>
Create and manage a custom DEX using Orderly One API - deployment, custom domains, graduation, and theming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tarnadas](https://clawhub.ai/user/Tarnadas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DEX operators use this skill to create, configure, deploy, update, and graduate white-label perpetuals DEXs with Orderly One. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides users through wallet signatures, token transfers, broker registration, and admin wallet finalization. <br>
Mitigation: Verify the official Orderly domain, inspect each signing payload, confirm chain IDs, recipient addresses, fees, and broker IDs, and prefer testnet or a limited-purpose wallet for setup. <br>
Risk: DEX configuration can include custom domains, uploaded assets, theme CSS, analytics scripts, IP allowlists, and region restrictions. <br>
Mitigation: Review configuration values before submission, validate CSS and encoded scripts, check file size limits, and confirm domain and regional settings match the intended deployment. <br>


## Reference(s): <br>
- [Orderly One DEX Skill Page](https://clawhub.ai/Tarnadas/orderly-one-dex) <br>
- [Orderly One Mainnet API](https://dex-api.orderly.network) <br>
- [Orderly One Testnet API](https://testnet-dex-api.orderly.network) <br>
- [Orderly Account Registration API](https://api.orderly.org/v1/register_account) <br>
- [Default DEX Theme CSS](https://raw.githubusercontent.com/OrderlyNetworkDexCreator/dex-creator-template/refs/heads/main/app/styles/theme.css) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions, Shell commands, Code] <br>
**Output Format:** [Markdown with endpoint references, JSON payload examples, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference an Orderly MCP tool for detailed endpoint information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
