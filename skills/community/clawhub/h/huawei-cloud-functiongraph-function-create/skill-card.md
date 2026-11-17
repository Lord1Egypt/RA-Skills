## Description:

Create and invoke FunctionGraph functions on Huawei Cloud. Supports VPC configuration, environment variables, synchronous and asynchronous function invocation. Use this skill when users ask to create, deploy, upload, or invoke cloud functions, serverless functions, or FunctionGraph functions. Triggered by keywords like "create function", "deploy function", "upload function", "invoke function", "create cloud function", "创建函数", "部署函数", "上传函数", "调用函数", "创建云函数", "FunctionGraph function", "serverless function", "function invocation".

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to create and configure Huawei Cloud FunctionGraph functions, then invoke them synchronously or asynchronously. It supports deployment options such as VPC settings and environment variables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification guidance may expose Huawei access-key or secret-key values in accessible logs.

Mitigation: Correct the checklist to check only whether credentials are configured, never print their values, and rotate credentials already exposed in logs.

Risk: Diagnostic verification steps can create or change cloud resources and incur charges.

Mitigation: Prefer read-only checks, use narrowly scoped credentials in a development project, and plan cleanup for resources created during testing.

Risk: Function source code or environment variables uploaded during deployment may contain sensitive information.

Mitigation: Review the source and environment variables before uploading them.

## Reference(s):

- [FunctionGraph Documentation](https://support.huaweicloud.com/functiongraph/)
- [Huawei Cloud FunctionGraph Documentation](https://support.huaweicloud.com/productdesc-functiongraph/index.html)
- [Python SDK Documentation](https://github.com/huaweicloud/huaweicloud-sdk-python-v3)
- [IAM Policies](artifact/references/iam-policies.md)
- [SDK Installation Guide](artifact/references/sdk-installation-guide.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance, Text]

**Output Format:** [Markdown guidance with Python and shell examples; FunctionGraph function URNs and invocation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the requested function configuration and invocation mode.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
