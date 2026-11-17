## Description:

Lists Huawei Cloud CDN accelerated domains through KooCLI, with an SDK fallback, filters, paging, and table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use the skill to inspect and filter a tenant's CDN accelerated-domain inventory before related operational work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency helper weakens download security.

Mitigation: Retain certificate verification and install verified, pinned packages in an isolated environment.

Risk: The CLI installer and external downloads were not verified in the supplied evidence.

Mitigation: Verify the CLI installer before running it.

Risk: Local executable settings can bypass the advertised read-only protection.

Mitigation: Keep executable overrides unset or tightly controlled, and use credentials limited to CDN listing.

## Reference(s):

- [Huawei KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [CLI installation and credential guide](references/cli-installation-guide.md)
- [Least-privilege IAM policy](references/iam-policies.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Full-field table, raw JSON array, or accelerated-domain names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports server-side filters and paged results.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
