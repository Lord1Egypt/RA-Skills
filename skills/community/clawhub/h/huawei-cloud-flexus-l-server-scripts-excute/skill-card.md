## Description:

Manage Huawei Cloud COC scripts and run Shell, Python, or Bat scripts across Flexus L instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operators and developers use the skill to create, inspect, list, and delete COC scripts, then run selected scripts across Huawei Cloud Flexus L instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may select the most recently created script automatically and can execute it on target servers using root by default.

Mitigation: Require an explicit script selection, inspect its contents and target instances, and use a less privileged execution account where possible.

Risk: The bundled smoke test requires access keys as command-line arguments and creates a cloud script.

Mitigation: Use environment variables or secure input for credentials, disclose the cloud mutation before running the smoke test, and remove test scripts afterward.

Risk: Resolved dependency versions and live IAM restrictions remain unverified.

Mitigation: Review dependency versions and confirm that the credentials are limited to the intended instances and operations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-flexus-l-server-scripts-excute)
- [IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
