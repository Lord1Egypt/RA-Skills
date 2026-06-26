## Description: <br>
NTS BizNo CLI helps agents verify Korean business registration numbers through official NTS API status and authenticity checks, local checksum validation, and bulk JSONL processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, finance operations teams, and KYB onboarding teams use this skill to check Korean business-registration status, validate representative and opening-date details, pre-filter invalid numbers locally, and audit supplier lists before contracts, payments, or tax-invoice workflows. <br>

### Deployment Geography for Use: <br>
South Korea <br>

## Known Risks and Mitigations: <br>
Risk: API-backed checks send selected Korean business-registration details to the official NTS/data.go.kr endpoint. <br>
Mitigation: Use the skill only when that disclosure is acceptable for the onboarding or audit workflow, and avoid sending unnecessary records. <br>
Risk: The NTS_API_KEY credential is required for status, validate, and bulk API calls. <br>
Mitigation: Keep NTS_API_KEY private, store it outside shared files and logs, and rotate it if exposure is suspected. <br>
Risk: JSONL outputs can contain sensitive supplier or onboarding records. <br>
Mitigation: Store outputs in access-controlled locations and redact or delete them when they are no longer needed. <br>
Risk: Overriding NTS_BASE could route business-registration data and credentials to an untrusted endpoint. <br>
Mitigation: Do not override NTS_BASE unless the replacement endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/nts-bizno-cli) <br>
- [data.go.kr](https://www.data.go.kr) <br>
- [NTS businessman API base endpoint](https://api.odcloud.kr/api/nts-businessman/v1) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown instructions with bash examples and JSONL command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NTS_API_KEY for API-backed commands; local checksum formatting runs without network.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
