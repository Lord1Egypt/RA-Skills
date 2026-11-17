## Description:

Lists Huawei Cloud OBS buckets through KooCLI with an SDK fallback and returns a table, JSON array, or bucket names.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use it to inventory the buckets in a Huawei Cloud account and obtain a table or structured list for follow-on work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found the advertised safeguards and query limits unreliable, and the installer source remains unverified.

Mitigation: Verify installation instructions independently; remove or tightly control executable overrides and fix fallback handling before relying on endpoint or count limits.

Risk: Cloud credentials and bucket names can expose private account information.

Mitigation: Keep credentials out of chat, use credentials restricted to bucket listing, and treat returned bucket names as private account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-obs-list)
- [Official KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credential guide](artifact/references/cli-installation-guide.md)
- [Least-privilege IAM policy](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Human-readable table, JSON array, or newline-delimited bucket names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-level bucket listings only; does not return objects inside buckets or bucket quota and usage.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
