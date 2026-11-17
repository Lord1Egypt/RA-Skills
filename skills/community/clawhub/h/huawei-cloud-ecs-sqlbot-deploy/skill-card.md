## Description:

Purchases a Huawei Cloud X Instance server and deploys the SQLBot intelligent query application using Python, Huawei Cloud SDK, and Cloud Operations Center.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to create a Huawei Cloud X Instance server, configure access, and deploy SQLBot for intelligent query workflows. It is intended for users who need a guided deployment flow with credential checks, region selection, configuration confirmation, and deployment verification.

### Deployment Geography for Use:

Huawei Cloud regions supported by the skill: China, Asia Pacific, Africa, Latin America, Middle East, and Turkey.

## Known Risks and Mitigations:

Risk: The skill can create billable Huawei Cloud resources without an enforceable approval step.

Mitigation: Review carefully before installing, require an explicit manual dry run or code change before resource creation, and keep the confirmation step mandatory before any deployment action.

Risk: The skill handles cloud credentials and default passwords in ways that can expose sensitive access.

Mitigation: Use only short-lived, least-privilege Huawei credentials, keep AK/SK values out of chat and shell history, remove shared default passwords, and disable password notifications.

Risk: The deployment path downloads and runs a remote installer script.

Mitigation: Verify the remote installer contents before execution and run the skill only in an account and region approved for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-ecs-sqlbot-deploy)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Huawei Cloud X Instance documentation](https://support.huaweicloud.com/productdesc-flexusx/pd_01_0002.html)
- [Huawei Cloud AK/SK authentication guide](https://support.huaweicloud.com/api-iam/iam_01_0001.html)
- [Huawei Cloud pricing calculator](https://www.huaweicloud.com/pricing/calculator.html#/hecs)
- [Huawei Cloud PyPI mirror](https://repo.huaweicloud.com/repository/pypi/simple)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and Python script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger Huawei Cloud API calls that create billable resources after user confirmation.]

## Skill Version(s):

1.0.1 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
