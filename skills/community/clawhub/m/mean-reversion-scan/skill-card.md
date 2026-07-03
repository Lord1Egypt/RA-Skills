## Description: <br>
Mean-reversion opportunity scan across RANGING and CHOPPY regimes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to request paid APEX Runner mean-reversion signals before considering entries in ranging or choppy crypto market regimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses EVM_PRIVATE_KEY, which can authorize spending from the configured wallet. <br>
Mitigation: Use a dedicated low-balance payment wallet, set strict funding limits, and avoid primary trading or custody wallets. <br>
Risk: x402-authenticated requests can initiate paid calls automatically. <br>
Mitigation: Require clear confirmation before paid requests and monitor wallet call history and balance. <br>
Risk: Crypto trading signals may be incorrect, incomplete, or unsuitable for a user's strategy. <br>
Mitigation: Review returned signals before acting and do not rely on them as the sole basis for trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/mean-reversion-scan) <br>
- [APEX Runner mean-reversion scan](https://apexrunner.ai/signals/mean-reversion-scan) <br>
- [APEX Runner pricing tiers](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner](https://apexrunner.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, JSON] <br>
**Output Format:** [Markdown instructions with a Python example and JSON API response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
