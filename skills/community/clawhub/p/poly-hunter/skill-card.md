## Description: <br>
庄家异动探测器 monitors active Polymarket markets and returns the three topics with the largest recent absolute price moves after SkillPay payment confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Web3 traders and developers can use this skill to request a paid snapshot of active Polymarket markets with the largest recent price changes for market monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact embeds a SkillPay API key. <br>
Mitigation: Remove the hardcoded key, rotate it before any deployment, and load payment credentials from managed secrets. <br>
Risk: Payment account ownership and SkillPay host trust are not fully established in the evidence. <br>
Mitigation: Confirm the receiving payment account and pin or allowlist approved SkillPay hosts before installation. <br>
Risk: The public description overstates the behavior as broader whale intelligence. <br>
Mitigation: Describe the skill as returning public Polymarket price-mover data unless additional verified whale-analysis evidence is added. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/poly-hunter) <br>
- [Polymarket CLOB markets endpoint](https://clob.polymarket.com/markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON API response containing payment status, optional payment URL, and Polymarket mover records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SkillPay payment confirmation before returning market mover data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
