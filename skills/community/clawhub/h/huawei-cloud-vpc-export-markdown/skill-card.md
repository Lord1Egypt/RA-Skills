## Description:

Lists VPCs in a Huawei Cloud region and exports the read-only inventory as Markdown, a table, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use it to inspect regional VPC inventory and create a local report for operations reviews or record keeping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled SDK installer may not preserve certificate verification.

Mitigation: Avoid the bundled installer; install dependencies from a verified source in an isolated environment.

Risk: The quality CLI wrapper's telemetry behavior is not fully verified.

Mitigation: Skip its installers and set SKILL_QUALITY_REPORT=0 until you have reviewed the wrapper and telemetry policy.

Risk: Exported VPC inventory can expose infrastructure details, and credentials grant cloud access.

Mitigation: Use read-only VPC credentials and protect the generated inventory file.

## Reference(s):

- [CLI installation and credential guide](references/cli-installation-guide.md)
- [Read-only IAM policy guidance](references/iam-policies.md)
- [Verification method and API details](references/verification-method.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files]

**Output Format:** [Local Markdown report, plain-text table, or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-specific VPC inventory with optional filters and output path.]

## Skill Version(s):

1.0.9 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
