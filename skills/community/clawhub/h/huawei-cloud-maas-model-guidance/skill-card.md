## Description:

Guides customers through selecting and invoking Huawei Cloud MaaS models, including API examples, key management, and development-tool integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Huawei Cloud customers use this skill to select MaaS models, prepare API calls, troubleshoot access, and integrate model invocation with development tools. It provides guidance and examples rather than executing commands or creating API keys.

### Deployment Geography for Use:

China (Southwest Guiyang 1 region for MaaS model services)

## Known Risks and Mitigations:

Risk: Remote pipe-to-shell setup examples can execute unreviewed code.

Mitigation: Prefer package-manager installation and inspect any remote script before running it.

Risk: Exposed API keys or overly broad IAM access can compromise cloud resources.

Mitigation: Store keys securely, avoid sharing them in code or logs, and review permissions before granting least-privilege access.

Risk: Prompts, files, images, or business data sent to MaaS or integrated third-party tools may be sensitive.

Mitigation: Send sensitive data only when its use with the chosen service and tool is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-maas-model-guidance)
- [Huawei Cloud MaaS documentation](https://support.huaweicloud.com/productdesc-maas/productdesc_maas_0002.html)
- [Model list](references/model-list.md)
- [API interfaces](references/api-interfaces.md)
- [Code examples](references/code-examples.md)
- [IAM policies](references/iam-policies.md)
- [Development-tool integration](references/dev-tools-integration.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with API examples and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance only; does not execute commands or create API keys.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
