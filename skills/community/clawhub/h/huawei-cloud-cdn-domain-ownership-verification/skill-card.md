## Description:

Diagnoses Huawei Cloud CDN domain ownership verification failures by checking the required DNS TXT record or verification file against the expected value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CDN operators use this skill to diagnose why a domain ownership check fails and receive read-only findings and suggested fixes without changing CDN resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Huawei Cloud credentials allow the agent to query CDN ownership details.

Mitigation: Use least-privilege read-only credentials and never paste access keys into chat.

Risk: DNS and HTTP probes disclose the target domain to the queried resolver or web endpoint.

Mitigation: Diagnose only approved domains and use an approved DNS resolver when the domain is sensitive.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-domain-ownership-verification)
- [Verification method reference](references/verification-method.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured text diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports verification status, observed DNS or HTTP results, likely cause, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
