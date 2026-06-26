## Description: <br>
Guides users through uploading an image and metadata, mining a vanity salt, and deploying a token on-chain through the Nad.fun BondingCurveRouter flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therealharpaljadeja](https://clawhub.ai/user/therealharpaljadeja) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to guide Nad.fun token creation, including image upload, metadata upload, vanity salt generation, and on-chain deployment with optional initial purchase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected images, token metadata, social links, wallet addresses, and token details to Nad.fun services. <br>
Mitigation: Require explicit user confirmation before each upload and review all submitted fields before sending them to the API. <br>
Risk: The skill can guide irreversible blockchain transactions involving funds. <br>
Mitigation: Verify contract addresses, network, fee estimates, initial purchase amount, and transaction parameters before any signature. <br>
Risk: The security summary notes no clear confirmation gate for uploads or blockchain transactions. <br>
Mitigation: Configure the agent to pause for user approval before upload, salt mining, and on-chain deployment steps. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/therealharpaljadeja/nadfun-token-creation) <br>
- [Nad.fun production API](https://api.nadapp.net) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, Solidity, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide API uploads and blockchain transaction preparation; confirmation should occur before uploads or signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
