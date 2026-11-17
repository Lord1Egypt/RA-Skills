## Description:

Query read-only CES and EPS management-plane information in Huawei Cloud using natural-language prompts or explicit query categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and engineers use this skill to retrieve alarm, dashboard, resource group, and enterprise project metadata across 12 supported read-only query categories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted inputs may expose cloud tokens.

Mitigation: Keep credentials out of chat and command arguments, use narrowly scoped read-only IAM credentials, and validate cloud endpoints before production use.

Risk: Dependency installation may weaken download security.

Mitigation: Require validated cloud endpoints and certificate verification for dependency installation; skip quality-tool installation until its data handling is reviewed.

Risk: A generic live-test helper may bypass read-only safeguards.

Mitigation: Avoid that helper until operation restrictions are enforced, and use narrowly scoped read-only IAM credentials.

Risk: The downloaded telemetry implementation remains unverified.

Mitigation: Disable reporting with SKILL_QUALITY_REPORT=0 and skip quality-tool installation until its data handling is reviewed.

## Reference(s):

- [Least-privilege IAM policies](references/iam-policies.md)
- [CLI, SDK, and credential guide](references/cli-installation-guide.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Verification method](references/verification-method.md)
- [Huawei Cloud KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text tables or JSON query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized CES and EPS management-plane results; output is limited to supported read-only categories.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
