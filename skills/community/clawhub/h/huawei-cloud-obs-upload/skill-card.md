## Description: <br>
Upload local files or directories to Huawei Cloud OBS buckets, list OBS buckets with capacity and object count, and schedule periodic uploads via crontab. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to upload files or directories to Huawei Cloud OBS, inspect bucket capacity and object counts, and create recurring upload schedules. It is intended for users who already have Huawei Cloud CLI, obsutil, and appropriate OBS/CES permissions configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled uploads can create persistent cloud transfers. <br>
Mitigation: Confirm the exact local path, bucket, prefix, and schedule before enabling recurrence, and remove the scheduled task when it is no longer needed. <br>
Risk: Broad directory uploads may transfer files that later include secrets or other unintended data. <br>
Mitigation: Use narrow source paths and review the directory contents before upload or scheduling. <br>
Risk: Cloud credentials and excessive permissions can expose Huawei Cloud resources. <br>
Mitigation: Do not share AK/SK values in conversation, configure credentials locally, and prefer least-privilege OBS/CES permissions. <br>
Risk: Remote installation commands can change the local machine. <br>
Mitigation: Review CLI and obsutil install commands before running them. <br>
Risk: Delete operations on OBS buckets or objects are irreversible. <br>
Mitigation: The skill refuses bucket/object delete, batch delete, and empty-bucket operations; use separate manual tooling only after independent review. <br>


## Reference(s): <br>
- [Task 1: List Buckets with Capacity and Object Count](references/task-list-buckets-with-stats.md) <br>
- [Task 2: Upload Local File or Directory to Target Bucket](references/task-upload-file.md) <br>
- [Task 3: Schedule Periodic Upload of Local Directory to Target Bucket](references/task-scheduled-upload.md) <br>
- [Related APIs - Huawei Cloud OBS Object Storage Management](references/related-apis.md) <br>
- [IAM Permission Policies - Huawei Cloud OBS Object Storage Management](references/iam-policies.md) <br>
- [OBS CES Monitoring Metrics Reference - Huawei Cloud OBS Object Storage Management](references/obs-metrics.md) <br>
- [Verification Method - Huawei Cloud OBS Object Storage Management](references/verification-method.md) <br>
- [Acceptance Criteria: huawei-cloud-obs-upload](references/acceptance-criteria.md) <br>
- [CLI Installation Guide - Huawei Cloud OBS Object Storage Management](references/cli-installation-guide.md) <br>
- [Troubleshooting - Huawei Cloud OBS Object Storage Management](references/troubleshooting.md) <br>
- [KooCLI Quick Start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html) <br>
- [obsutil Installation Guide](https://support.huaweicloud.com/utiltg-obs/obs_11_0003.html) <br>
- [OBS API Reference](https://support.huaweicloud.com/api-obs/obs_04_0001.html) <br>
- [CES ShowMetricData API](https://support.huaweicloud.com/api-ces/ces_03_0059.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crontab or Task Scheduler entries and Huawei Cloud CLI/obsutil commands.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
