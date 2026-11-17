## Description:

Diagnoses Huawei Cloud CDN domain DNS resolution by checking the expected CNAME, probing resolved IP addresses, and verifying their CDN attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CDN operators use this skill to diagnose DNS failures, CNAME mismatches, timeouts, and IP attribution for their Huawei Cloud CDN domains without changing account settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Huawei Cloud access credentials could be exposed in chat or logs.

Mitigation: Use dedicated read-only IAM credentials; never paste access keys or secrets into chat or logs.

Risk: Applying remediation as a configuration change could affect production traffic.

Mitigation: Keep this skill read-only and perform any DNS or CDN changes separately after review.

Risk: A local A-record probe or a result with more than 20 IPs may not reflect all resolution paths.

Mitigation: Disclose incomplete coverage in the report and verify across resolvers or regions when results are mixed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-cdn-dns-resolution-diagnosis)
- [DNS resolution probe](artifact/references/task-dns-resolve.md)
- [IP attribution check](artifact/references/task-ip-attribution.md)
- [Diagnosis report format](artifact/references/task-report-generation.md)
- [IAM permissions](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Structured text diagnosis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes expected CNAME, resolved IPs, CDN attribution, diagnosis status, and remediation suggestions; checks at most 20 IPs.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
