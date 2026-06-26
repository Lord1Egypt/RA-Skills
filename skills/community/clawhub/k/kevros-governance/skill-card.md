## Description: <br>
Kevros Governance helps agents verify proposed actions against policies and record signed, tamper-evident audit evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knuckles-stack](https://clawhub.ai/user/knuckles-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add policy checks, signed allow/clamp/deny decisions, and audit records around agent actions such as deployments, data access, trading, and payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Action payloads may be processed and logged by an external third-party governance service. <br>
Mitigation: Avoid sending secrets, PII, regulated data, or full business context unless that disclosure is intended and approved. <br>
Risk: Use depends on a protected Kevros API key and third-party SDKs or service domains. <br>
Mitigation: Protect the API key, verify SDK packages and domains before use, and review the provider's privacy, retention, and audit-access terms. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/knuckles-stack/kevros-governance) <br>
- [Kevros website](https://www.taskhawktech.com) <br>
- [Kevros API documentation](https://governance.taskhawktech.com/api) <br>
- [Kevros quickstart](https://www.taskhawktech.com/quickstart) <br>
- [Kevros playground](https://www.taskhawktech.com/playground) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK installation guidance, REST API examples, endpoint references, and integration options.] <br>

## Skill Version(s): <br>
0.3.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
