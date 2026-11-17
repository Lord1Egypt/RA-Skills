## Description:

Lists and filters Huawei Cloud BSS vouchers using KooCLI or the Huawei SDK, returning a table, JSON, or a compact voucher-name list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud account administrators and developers use this skill to review and filter voucher inventory for Huawei Cloud BSS billing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says executable overrides may bypass the intended read-only guard.

Mitigation: Remove or constrain executable overrides, use a trusted CLI installation, and run with an isolated account limited to read-only BSS access.

Risk: Credential-handling documentation conflicts about where the skill obtains credentials.

Mitigation: Correct the credential guidance and explicitly select credentials for a dedicated account; do not use an environment containing several Huawei accounts.

## Reference(s):

- [KooCLI Installation & Credential Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown table, JSON array, or plain-text voucher-name list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The user can select JSON or name-list output; a full-field table is the default.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
