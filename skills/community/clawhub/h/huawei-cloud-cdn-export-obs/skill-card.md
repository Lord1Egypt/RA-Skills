## Description:

Queries a Huawei Cloud CDN tenant’s accelerated-domain list, exports it locally as JSON, CSV, or Markdown, and can upload the file to Huawei OBS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers can use this skill to create an inventory snapshot of accelerated domains for a Huawei Cloud CDN tenant, save it locally, and optionally archive it in OBS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dependency helper may install packages without certificate verification, and downloaded code has not been verified in a live environment.

Mitigation: Avoid the helper until certificate verification is restored; install reviewed, pinned dependencies in an isolated environment.

Risk: Upload verification can be skipped, so an uploaded object may not be checked against the local export.

Mitigation: Independently compare the uploaded object size with the local file size.

Risk: Cloud credentials or the OBS destination may grant or expose more access than intended, and overwrites can replace existing data.

Mitigation: Use narrowly scoped credentials and a trusted bucket, and explicitly approve overwrites.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/wlc-dev/skills/huawei-cloud-cdn-export-obs)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [Least-privilege IAM policies](artifact/references/iam-policies.md)
- [Verification method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Files, JSON, CSV, Markdown]

**Output Format:** [A local JSON, CSV, or Markdown export, with an optional JSON run summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OBS upload is optional; existing objects are refused by default.]

## Skill Version(s):

1.0.5 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
