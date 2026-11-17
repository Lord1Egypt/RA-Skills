## Description:

Lists Huawei Cloud VPCEP endpoints and endpoint services through read-only queries, with filters and concise, table, JSON, or Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inventory Huawei Cloud VPCEP endpoints and endpoint services, filter results for troubleshooting, and export reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner flagged an unverified downloaded installer that may make system changes.

Mitigation: Inspect the installer and its system changes, and verify it through a trusted source before running it.

Risk: The scanner flagged environment-controlled command execution and undeclared tool scope.

Mitigation: Review the active environment and command overrides before use, and confirm that the effective commands are the expected read-only VPCEP list operations.

Risk: Security analysis was partial because three local path-like references could not be resolved.

Mitigation: Resolve and review the referenced files before relying on the security assessment.

## Reference(s):

- [KooCLI official quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Verification method](artifact/references/verification-method.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Concise text, fixed-column table, JSON array, or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filtered and paginated VPCEP inventory; unavailable resources are grouped separately in text and table views.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
