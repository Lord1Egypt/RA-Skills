## Description: <br>
庄家异动探测器 requires SkillPay payment, fetches active Polymarket markets, and returns the three detected markets with the largest recent price changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xqw1377-prog](https://clawhub.ai/user/xqw1377-prog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Web3 market watchers can use this skill to request a paid Polymarket mover snapshot from an agent. The output is useful for triage and market monitoring, but it should not be treated as verified whale or investment intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports an embedded SkillPay API key. <br>
Mitigation: Remove the hardcoded key, rotate the exposed credential, and load payment credentials only from a managed secret. <br>
Risk: The payment flow is real and can create SkillPay charges. <br>
Mitigation: Review payment settings before deployment and restrict payment endpoints to trusted hosts. <br>
Risk: The security evidence says the release advertises stronger whale analysis than the code performs. <br>
Mitigation: Describe the output as Polymarket price-mover data unless verified whale or on-chain analysis is added and independently validated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xqw1377-prog/poly-hunter-final) <br>
- [Publisher profile](https://clawhub.ai/user/xqw1377-prog) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Guidance] <br>
**Output Format:** [JSON response containing payment status, optional payment URL, and up to three Polymarket mover records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SkillPay charge before data is returned; mover records can include market id, title, current price, previous price, delta, absolute delta, volume, and status.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata; artifact skill.yaml reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
