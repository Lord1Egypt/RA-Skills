## Description:

Lists Huawei Cloud CBR backups for a selected region and returns a filtered inventory as a table, JSON array, or compact name-and-ID list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use the skill to inventory and filter Huawei Cloud CBR backups by region, status, resource, or vault. The resulting list supports routine backup checks, capacity accounting, and locating backup IDs for follow-up work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guide downloads and executes a remote KooCLI installer whose contents were not verified.

Mitigation: Use a verified KooCLI download from Huawei's official documentation instead of running the supplied installer command.

Risk: Credential-handling assurances conflict, and the SDK fallback reads access keys into process memory.

Mitigation: Use credentials with backup-listing-only IAM permission, configure them outside chat, and account for the SDK fallback when choosing the runtime.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI Installation and Credential Guide](references/cli-installation-guide.md)
- [Least-Privilege IAM Policy](references/iam-policies.md)
- [Verification Method and API Scope](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Aligned text table, JSON array, or compact backup name-and-ID list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Region-scoped inventory with optional filters and automatic pagination.]

## Skill Version(s):

1.0.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
