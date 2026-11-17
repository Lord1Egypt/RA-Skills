## Description:

Verify Korean business registration numbers via the official NTS public API, including operating-status lookup, authenticity checks, local checksum validation, and bulk file processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to validate Korean B2B counterparties during onboarding, supplier audits, KYB checks, tax-invoice preparation, and payment review workflows. It supports single-record checks, bulk status sweeps, and local pre-validation before API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status and validation checks can send Korean business registration numbers, representative names, and opening dates to the NTS/data.go.kr API.

Mitigation: Use the skill only when that data sharing is approved for the workflow, and treat generated audit files as sensitive business records.

Risk: An inherited NTS_BASE value can change the endpoint used for API calls and expose API keys or KYB data outside the intended service.

Mitigation: Run the skill in a trusted environment and leave NTS_BASE unset or pin it to the official HTTPS NTS endpoint before use.

## Reference(s):

- [data.go.kr](https://www.data.go.kr)
- [NTS Businessman API Endpoint](https://api.odcloud.kr/api/nts-businessman/v1)
- [ClawHub Skill Page](https://clawhub.ai/chloepark85/skills/nts-bizno-cli)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSONL command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output is one JSON object per line for jq and downstream pipeline processing.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
