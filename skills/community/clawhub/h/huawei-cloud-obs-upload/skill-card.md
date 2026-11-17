## Description:

Upload local files or directories to a specified Huawei Cloud OBS bucket, schedule recurring uploads, and list bucket capacity and object counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operators use this skill to inspect OBS bucket storage statistics, upload user-selected local content, or configure recurring uploads to a specified bucket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled-upload cleanup may remove unrelated scheduled jobs.

Mitigation: Before enabling recurring uploads, inspect and back up the scheduled-task configuration, remove only the exact approved job, and stop if the configuration cannot be read.

Risk: The documented permissions may be broader than needed and may include deletion despite claims that deletion is disallowed.

Mitigation: Review the IAM policy and scope it to the required bucket and list, read, and upload actions; omit deletion permissions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-obs-upload)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [IAM policies](artifact/references/iam-policies.md)
- [OBS metrics](artifact/references/obs-metrics.md)
- [Related APIs](artifact/references/related-apis.md)
- [List buckets with stats](artifact/references/taREDACTED-SECRET.md)
- [Scheduled uploads](artifact/references/task-scheduled-upload.md)
- [Upload files](artifact/references/task-upload-file.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [Verification method](artifact/references/verification-method.md)
- [Related bucket creation skill (out of scope)](https://skills.huaweicloud.com/detail/huawei-cloud-obs-bucket-create)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed token or output-size limits are specified.]

## Skill Version(s):

1.0.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
