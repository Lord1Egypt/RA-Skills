## Description: <br>
Identifies the three largest recent absolute price movers among active Polymarket markets after SkillPay payment confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Web3 market watchers and trading analysts use this skill to request a paid API result listing active Polymarket markets with the largest recent price changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ClawScan flags this paid Polymarket skill as suspicious because it exposes payment-account authority and overstates what the code appears to provide. <br>
Mitigation: Review before installing or paying; use only after the maintainer removes and rotates the hardcoded SkillPay key, pins or allowlists the SkillPay host, identifies the payment recipient, and aligns the description with the actual price-mover behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/poly-hunter-stable) <br>
- [Publisher profile](https://clawhub.ai/user/xqw1377-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, API response, guidance] <br>
**Output Format:** [JSON response with payment status and market mover records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillPay confirmation before returning mover data.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
