## Description: <br>
Active grid levels, spacing, and next buy/sell prices per pair. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve real-time grid trading levels, grid spacing, and next buy or sell prices for supported cryptocurrency pairs. It supports manual grid inventory management, dashboards, and reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM wallet private key for paid x402 requests. <br>
Mitigation: Use a dedicated wallet with limited USDC, store EVM_PRIVATE_KEY only in secure secret storage, and avoid logging or hardcoding it. <br>
Risk: Automatic payment authorization can spend funds without enough user control. <br>
Mitigation: Require explicit approval and a maximum amount before each paid call. <br>
Risk: The security verdict is suspicious because key-safety and user-control warnings are insufficient. <br>
Mitigation: Review the skill carefully before installation and confirm the wallet, payment, and approval behavior before deployment. <br>


## Reference(s): <br>
- [Grid Levels signal homepage](https://apexrunner.ai/signals/grid-levels) <br>
- [Pricing tier lookup](https://apexrunner.ai/signals/my-pricing) <br>
- [grid-health related signal](https://apexrunner.ai/signals/grid-health) <br>
- [grid-health-score related signal](https://apexrunner.ai/signals/grid-health-score) <br>
- [live-fill-rate related signal](https://apexrunner.ai/signals/live-fill-rate) <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/grid-levels) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response data with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests using an EVM wallet with USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
