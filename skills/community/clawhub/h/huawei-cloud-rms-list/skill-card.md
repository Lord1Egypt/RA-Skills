## Description:

Queries Huawei Cloud Resource Management Service to list tenant resources or provider and region catalogs, filter results, and export them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and engineers use this skill to review a tenant's Huawei Cloud resource inventory for asset tracking, compliance pre-checks, and resource lookups. It can filter and export read-only inventory results or list RMS provider and region catalogs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags installer commands that weaken download security.

Mitigation: Replace mirror installation commands with certificate-verified package installation in an isolated environment before using cloud credentials.

Risk: The SDK fallback does not honor --domain-id, so the effective account may differ from the selected account.

Mitigation: Use read-only credentials and verify the effective account; do not rely on --domain-id when the SDK fallback is active.

Risk: The downloaded quality reporter's data handling has not been reviewed.

Mitigation: Set SKILL_QUALITY_REPORT=0 unless you have reviewed the external reporter's data handling.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-rms-list)
- [IAM Policies](references/iam-policies.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV]

**Output Format:** [Aligned table, JSON, GitHub-flavored Markdown, or CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports filters and automatic paging; JSON, Markdown, and CSV results can be written to a local file.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
