## Description: <br>
Provides an API-key authenticated proxy for ZhenInsure AI insurance consultations, including conversation creation, message calls, and human advisor handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and insurance advisors use this skill to start and continue ZhenInsure insurance-consultation chats, send customer questions to the hosted service, and request human advisor handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages may include sensitive insurance, health, or financial details sent to the ZhenInsure service. <br>
Mitigation: Install only from the trusted publisher profile, send only necessary personal information, and review the service destination before use. <br>
Risk: The skill requires a live ZhenInsure API key and message calls may incur charges. <br>
Mitigation: Use a limited API key where possible, monitor balance and billing, and confirm costs before high-volume use. <br>
Risk: A configurable base URL can redirect requests away from the default ZhenInsure host. <br>
Mitigation: Leave ZHENINSURE_BASE_URL unset or set it only to a trusted ZhenInsure-controlled host. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/zhenstaff/insurance-broker) <br>
- [ZhenInsure API documentation](https://www.zhenins.com/docs/api) <br>
- [ZhenInsure homepage](https://www.zhenins.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [Synchronous JSON responses with success or error fields, endpoint and method metadata, cost information, and service payloads.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include billing or API-key management URLs when balance or authentication errors occur.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence, package.json, skill.json, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
