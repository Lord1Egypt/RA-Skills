## Description:

Lists Huawei Cloud Elastic IP bandwidths, inspects individual bandwidth details, and exports results as tables, JSON, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory Huawei Cloud EIP bandwidth resources in a tenant region and inspect the public IPs and rules associated with a bandwidth. It can also produce a report for review or archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence because installation runs a downloaded script and environment settings may redirect a subprocess to another program.

Mitigation: Review the installer before running it and verify it through a trusted source where possible. Check environment overrides and use only credentials and permissions you are comfortable exposing to the invoked program.

Risk: The security scan was partial because five local references were unresolved, so its evidence is incomplete.

Mitigation: Review the skill and its referenced files before use, and reassess the security evidence when the unresolved references are available.

## Reference(s):

- [Huawei Cloud KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Terminal table, JSON array or object, or Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists bandwidth records or returns details for one bandwidth, including associated public IPs and bandwidth rules. Markdown reports can be written to a file.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
