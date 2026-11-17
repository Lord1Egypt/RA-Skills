## Description:

Diagnose suspected false-positive blocks in Huawei Cloud WAF by tracing request events to the blocking rule and providing release options, verification steps, and rollback commands for the user to review and run.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to investigate Huawei Cloud WAF blocks, identify the rule involved, and prepare a safe, reversible response. The skill only queries WAF and presents any release or rollback commands for the user to run.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnosis workflow requires a reporting tool that is installed automatically, and its implementation, data collection, and reporting-disable behavior are unverified.

Mitigation: Review the reporting dependency before use; require a fixed, verified release and documented data collection, or remove the mandatory wrapper. Use read-only WAF credentials and verified packages from Huawei Cloud's official KooCLI guide.

Risk: Whitelist and log-only recommendations can reduce WAF protection if applied too broadly or without confirming a false positive.

Mitigation: Confirm the event and matching rule first, choose the narrowest suitable release option, and review the suggested change and rollback command before applying it.

## Reference(s):

- [Huawei Cloud KooCLI installation and usage guide](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM Policies for WAF False Alarm Diagnosis](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnosis; proposed changes and rollback commands are provided for the user to review and execute.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
