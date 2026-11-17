## Description:

Manages Huawei Cloud LTS log groups, streams, indexes, transfers, and alarms, and searches logs for diagnosis using the hcloud CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use this skill to search and diagnose Huawei Cloud LTS logs and manage log resources, transfers, and alarms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud credentials could allow unintended changes to LTS resources.

Mitigation: Use the read-only IAM policy for search and diagnostics; grant scoped write access only when needed.

Risk: Deleting a log group can remove its log streams and disrupt log access.

Mitigation: Confirm the exact resource IDs and cascading impact before each destructive action.

Risk: Running a downloaded CLI installer without checking its source exposes the environment to untrusted code.

Mitigation: Verify the hcloud installer source before downloading and executing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-lts-manage)
- [CLI installation guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [LTS alarm reference](references/lts-alarm-reference.md)
- [Verification method](references/verification-method.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results and resource configuration snapshots depend on the requested operation.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
