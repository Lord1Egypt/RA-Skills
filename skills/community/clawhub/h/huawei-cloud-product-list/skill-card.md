## Description:

Lists Huawei Cloud product and service types with filters and table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Huawei Cloud users can browse the product and service catalog, filter entries by name or code, and export the results for product selection or catalog review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags weakened download security during setup and environment settings that may bypass the advertised read-only guard.

Mitigation: Use a corrected release that preserves certificate verification and removes arbitrary executable overrides; install pinned dependencies in an isolated environment, use narrowly scoped read-only credentials, and invoke the skill explicitly for Huawei Cloud.

## Reference(s):

- [KooCLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Verification method](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [Official Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text catalog table, JSON array, or newline-separated product names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results go to stdout; errors go to stderr.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
