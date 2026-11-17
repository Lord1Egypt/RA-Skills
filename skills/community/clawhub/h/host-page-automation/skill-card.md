## Description:

宿主网页自动化适配工作流。遇到 AI 表单操作、网页字段采集/填充、控制台框架探测、Vue/React/Ext/Angular 页面交互，或 Chat 驱动网页操作时使用。先只读探测，再单项脚本验证和字段映射，最后按需接入对话与确认执行；不建设万能填表引擎。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenjie002](https://clawhub.ai/user/shenjie002)

### License/Terms of Use:

MIT-0

## Use Case:

面向开发者，帮助他们在指定宿主网页中调查框架、控件与字段绑定，并逐步验证页面采集或填充操作；适配范围、写入和业务确认应按用户授权推进。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer may change between releases because the installation instructions do not pin a version.

Mitigation: Pin the reviewed release and verify its checksum or source before installing.

Risk: Browser interactions, queries, or scripts can affect page state and may trigger business side effects.

Mitigation: Limit actions to the approved page and test fields; verify the result before saving or submitting.

## Reference(s):

- [Host Page Automation on ClawHub](https://clawhub.ai/shenjie002/skills/host-page-automation)
- [Publisher profile: shenjie002](https://clawhub.ai/user/shenjie002)
- [Frameworks and Controls Guide](artifact/references/frameworks-and-controls.md)
- [Validation and Delivery Checklist](artifact/references/validation.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Code, Shell commands]

**Output Format:** [Markdown guidance and reports, with JavaScript console snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-specific; distinguishes read-only probes, validated actions, and unverified steps.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
