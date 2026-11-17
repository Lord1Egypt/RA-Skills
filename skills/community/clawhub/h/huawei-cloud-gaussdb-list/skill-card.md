## Description:

Lists Huawei Cloud GaussDB for MySQL instances in a selected region and presents the results as a table, JSON, or Markdown, with filters and a read-only guard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use the skill to inspect GaussDB for MySQL inventory and instance status in a Huawei Cloud region, including as a read-only check before related work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence: setup downloads and runs an external installer, and environment settings may redirect command execution beyond the read-only inventory task. The scan was incomplete.

Mitigation: Review the installer and environment configuration before use, and avoid running where untrusted parties can influence environment settings or cloud credentials.

## Reference(s):

- [KooCLI installation guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies and least-privilege access](references/iam-policies.md)
- [Verification method and API details](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Aligned instance table, JSON array, or Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region and instance filters with automatic pagination.]

## Skill Version(s):

1.0.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
