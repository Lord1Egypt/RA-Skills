## Description:

Lists Huawei Cloud Cloud Connect instances by region, with optional filters and table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and operators use this skill to inspect and filter Cloud Connect instance inventories for a selected Huawei Cloud region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's read-only and credential-handling promises need review; the SDK fallback reads keys directly, and live cloud behavior is unverified.

Mitigation: Use a dedicated read-only cloud identity, expose only its intended credentials, and verify the installer through Huawei's official documentation. Restrict or remove executable overrides.

## Reference(s):

- [IAM Policies (least privilege, read-only)](references/iam-policies.md)
- [KooCLI Installation & Credential Guide](references/cli-installation-guide.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Tabular text, JSON array, or newline-separated instance names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports region selection and optional name, status, and ID filters.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
