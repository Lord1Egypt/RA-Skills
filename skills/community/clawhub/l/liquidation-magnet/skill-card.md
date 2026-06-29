## Description: <br>
Identifies price levels with dense liquidation clusters <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and users query this skill to identify high-risk price zones with dense liquidation clusters before setting stop losses or sizing positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM wallet private key to make x402 payments, which can expose funds if the key is mishandled. <br>
Mitigation: Use a dedicated low-balance wallet and avoid storing or pasting the private key in chat. <br>
Risk: Automated pay-per-call use can create unintended spend. <br>
Mitigation: Configure X402_POLICY_PATH with per-call and daily caps plus a recipient allowlist, and keep X402_AUTOPREFLIGHT enabled. <br>


## Reference(s): <br>
- [Liquidation Magnet signal endpoint](https://apexrunner.ai/signals/liquidation-magnet) <br>
- [Liquidation Magnet ClawHub listing](https://clawhub.ai/kynto2001-ctrl/skills/liquidation-magnet) <br>
- [kynto2001-ctrl publisher profile](https://clawhub.ai/user/kynto2001-ctrl) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with Python example code and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EVM wallet private key for x402-authenticated paid API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
