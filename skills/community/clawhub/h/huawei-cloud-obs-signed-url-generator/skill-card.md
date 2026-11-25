## Description:

Create time-limited signed URLs for Huawei Cloud OBS requests, with optional headers, query parameters, temporary credentials, and image processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to create temporary OBS object access or image-processing links, allowing recipients to retrieve content without receiving permanent credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious with medium confidence. It reports quality-tool installation and telemetry concerns, and that signed requests may allow object changes or deletion depending on credential permissions. The review was incomplete.

Mitigation: Review installation scripts before installing the quality tool and disable telemetry with SKILL_QUALITY_REPORT=0 if installed. Use narrowly scoped OBS credentials, set a short expiration, and check the signed method and parameters before sharing a URL.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-signed-url-generator)
- [IAM policies and permissions](artifact/references/iam-policies.md)
- [Image processing guide](artifact/references/image-processing-guide.md)
- [Huawei Cloud OBS image processing overview](https://support.huaweicloud.com/intl/zh-cn/usermanual-obs/obs_01_0001.html)
- [Huawei Cloud OBS Python SDK signed URL guide](https://support.huaweicloud.com/intl/zh-cn/sdk-python-devg-obs/obs_22_1301.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Signed URL text with optional command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [URLs grant temporary access according to their signed method, parameters, expiration, and the permissions of the credentials used.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
