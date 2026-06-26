## Description: <br>
Returns a paid snapshot of the three largest absolute price movers among active Polymarket markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Web3 investors and agent workflows use this skill to request a paid Polymarket market-mover snapshot and receive payment status, checkout details, or the resulting top-three mover data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The payment flow is real and the artifact embeds a payment API secret. <br>
Mitigation: Review before installing, revoke the exposed key, remove secrets from source, and load payment credentials from a managed secret store. <br>
Risk: The release claims whale or on-chain intelligence that is not supported by the implemented market-mover behavior. <br>
Mitigation: Treat results as Polymarket price-mover data only unless the developer documents and implements the claimed data sources. <br>
Risk: Payment API and web hosts are configurable. <br>
Mitigation: Restrict payment hosts to trusted SkillPay endpoints before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/poly-hunter-pro) <br>
- [Publisher profile](https://clawhub.ai/user/xqw1377-prog) <br>
- [Polymarket CLOB markets endpoint](https://clob.polymarket.com/markets) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, API response] <br>
**Output Format:** [JSON response containing payment status, payment URL, charge ID, or market mover records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to three market records with title, current price, previous price, delta, absolute delta, volume, and status after payment confirmation.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact skill.yaml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
