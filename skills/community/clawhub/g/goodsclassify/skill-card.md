## Description: <br>
Classifies product queries and returns commodity, customs, HS, or tax-code lookup results using the configured FastGPT workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orangeboo](https://clawhub.ai/user/orangeboo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to answer Chinese-language product classification requests, including commodity codes, customs codes, HS codes, and tax numbers. It may first request a mobile number before returning product-code results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects mobile numbers, stores them locally, and sends them with product queries to an external FastGPT service. <br>
Mitigation: Use only with informed user consent and an approved data-retention process; prefer a version that documents retention and deletion behavior. <br>
Risk: The security review reports bundled service credentials and plain HTTP communication with the configured FastGPT service. <br>
Mitigation: Replace bundled keys with operator-managed secrets, rotate exposed credentials, and prefer HTTPS before using the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orangeboo/goodsclassify) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt for a mobile number before returning product-code lookup results.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
