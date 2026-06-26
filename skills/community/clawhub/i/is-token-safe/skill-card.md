## Description: <br>
Evaluates a crypto token contract for scam-risk signals and returns a safety indication with supporting reasons for trading and agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dokbawi80](https://clawhub.ai/user/dokbawi80) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to screen token addresses before routing them into automated trading bots, prediction-market agents, or token discovery pipelines. It is intended to provide a quick risk signal, not a substitute for independent contract review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The main entry point does not perform the promised token-safety check. <br>
Mitigation: Validate the entry point in a sandbox and fix it before using the skill for trading or automated decisions. <br>
Risk: Token addresses checked by the standalone scanner may be sent to public Base RPC and honeypot.is services. <br>
Mitigation: Avoid submitting sensitive token addresses to public services unless that data sharing is acceptable for the deployment. <br>
Risk: The standalone scanner needs dependency pinning and validation before its results are relied on. <br>
Mitigation: Pin runtime dependencies, review scanner behavior, and test known safe and unsafe token cases before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dokbawi80/is-token-safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object or concise text risk summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected output includes a token risk level and supporting reasons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
