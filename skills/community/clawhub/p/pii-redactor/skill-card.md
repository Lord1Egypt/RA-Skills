## Description: <br>
Redact sensitive information from text using a locally-hosted, zero-shot PII/PHI detection model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-newhauser](https://clawhub.ai/user/m-newhauser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route draft agent responses through a locally hosted PII/PHI redaction service before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft responses are sent to a configured redaction service, so an untrusted or public endpoint could expose sensitive text. <br>
Mitigation: Keep CLAWGUARD_URL pointed to localhost or an internal HTTPS service you operate, do not expose the service publicly, and validate the endpoint before sending data. <br>
Risk: PII/PHI detection is probabilistic and may miss sensitive information. <br>
Mitigation: Validate the detector on representative data, apply human review for high-stakes use, and use the documented manual-review fallback when automated scanning is unavailable. <br>
Risk: A leaked CLAWGUARD_TOKEN can allow unauthorized use of the redaction service. <br>
Mitigation: Store CLAWGUARD_TOKEN in a secret manager or protected environment variable and rotate it if compromised. <br>


## Reference(s): <br>
- [PII Redactor on ClawHub](https://clawhub.ai/m-newhauser/pii-redactor) <br>
- [clawguard-pii PyPI package](https://pypi.org/project/clawguard-pii/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires clawguard, CLAWGUARD_URL, and CLAWGUARD_TOKEN; sends draft text to the configured redaction service and returns redacted text or manual-review guidance.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
