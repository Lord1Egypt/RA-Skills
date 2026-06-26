## Description: <br>
Trade Hyperliquid perpetuals through CAI tools for market lookup, preflight checks, order placement, order status, closes, and cancels without Hyperliquid website signup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bernardtai](https://clawhub.ai/user/bernardtai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide CAI-enabled Hyperliquid perpetuals onboarding, preflight validation, live order placement, order monitoring, closes, and cancels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live perpetuals trading and deposits can cause financial loss if asset, size, price, direction, or account balance is wrong. <br>
Mitigation: Require explicit user confirmation before deposits, order placement, closes, and cancels; verify preflight results, asset, size, price, direction, and balances before acting. <br>
Risk: The skill requires a CAI_API_KEY with platform or full API scope. <br>
Mitigation: Use the least CAI API scope that supports the workflow, store the key as a secret, and avoid exposing it in prompts, logs, or generated files. <br>
Risk: Security evidence flags the release as suspicious because live trading and deposits need stronger risk disclosure and confirmation guidance. <br>
Mitigation: Review the skill carefully before installing and only use it when the operator understands CAI and Hyperliquid perpetuals trading risks. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bernardtai/skills/hyperliquid-with-cai) <br>
- [CAI Skill Reference](https://cai.com/skill.md) <br>
- [CAI Tools Manifest](https://cai.com/specs/cai-tools.manifest.json) <br>
- [CAI Developers](https://cai.com/developers.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and CAI tool names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CAI_API_KEY with platform or full API scope; recommends explicit confirmation before deposits, order placement, closes, and cancels.] <br>

## Skill Version(s): <br>
1.0.17 (source: evidence release, artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
