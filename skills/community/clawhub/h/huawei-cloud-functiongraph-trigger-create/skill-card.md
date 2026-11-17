## Description:

Creates scheduled TIMER and event-driven OBS triggers for Huawei Cloud FunctionGraph functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers managing Huawei Cloud FunctionGraph functions use this skill to create scheduled TIMER triggers or OBS object event triggers for existing functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification steps described as read-only can execute a function or leave an additional recurring trigger active.

Mitigation: Review the verification procedure first, approve function execution separately, use an isolated test function with synthetic data, and remove temporary triggers.

Risk: Cloud credentials and permissions can affect the target function and its triggers.

Mitigation: Scope credentials to the intended function and avoid optional lifecycle permissions unless they are needed.

## Reference(s):

- [Cron Expression Reference](references/cron-reference.md)
- [OBS Event Trigger Guide](references/obs-trigger-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [CreateFunctionTrigger API](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_0122.html)
- [FunctionGraph Permissions and Authorization Items](https://support.huaweicloud.com/api-functiongraph/functiongraph_06_1100.html)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [FunctionGraph trigger configuration with a JSON status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a persistent TIMER schedule or OBS event trigger for an existing function.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
