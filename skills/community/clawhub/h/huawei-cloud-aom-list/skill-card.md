## Description:

Lists names for 12 read-only Huawei Cloud AOM resource categories from natural-language or explicit category queries, with table, JSON, or names-only output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to retrieve names of Huawei Cloud AOM monitoring resources for an account and region.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication tokens could be misdirected by unapproved endpoints or unsafe redirects.

Mitigation: Keep the release in review until authenticated requests enforce approved endpoints and safe redirects; do not wrap credential checks.

Risk: Package installation may weaken download security.

Mitigation: Preserve TLS verification during package installation.

Risk: Telemetry behavior is poorly documented, and the remote telemetry executable was not bundled for review.

Mitigation: Make telemetry optional and clearly disclose data handling; treat its collection behavior as unverified until reviewed.

Risk: Cloud credentials and resource or access-code output may be sensitive.

Mitigation: Use narrowly scoped cloud credentials and treat returned resource and access-code data as private.

## Reference(s):

- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [KooCLI and SDK installation guide](artifact/references/cli-installation-guide.md)
- [AOM query data flow](artifact/references/dataflow-diagram.md)
- [Verification method](artifact/references/verification-method.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Name-first text table, JSON, or newline-separated names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes results to stdout; names-only mode omits other fields.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
