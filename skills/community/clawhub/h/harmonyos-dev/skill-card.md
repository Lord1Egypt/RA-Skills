## Description:

Harmonyos Dev provides Chinese-language guidance for HarmonyOS 5.0-6.1 application development with ArkTS, Stage model configuration, ArkUI, UIAbility lifecycle management, resources, permissions, media, AI integration, and distributed capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhongm](https://clawhub.ai/user/yhongm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to answer HarmonyOS implementation questions, draft ArkTS and ArkUI code, and configure Stage-model modules, permissions, packaging, resources, networking, testing, and release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable examples may include broad or sensitive HarmonyOS permissions.

Mitigation: Treat samples as starting points, remove unused permissions, and avoid background location or floating-window access unless the application clearly needs it.

Risk: Signing and release examples may encourage plaintext signing-secret patterns.

Mitigation: Keep signing keys and passwords out of tracked project files and inject them through local developer configuration or CI secrets.

Risk: Network, distributed sync, remote file, and download examples can affect user data scope and consent.

Mitigation: Review data collection, consent, file handling, and transfer boundaries before adapting these examples in an application.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yhongm/skills/harmonyos-dev)
- [HarmonyOS Developer Guides](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides)
- [ArkTS Language Introduction](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts)
- [ArkUI Basic Syntax Overview](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-basic-syntax-overview)
- [Stage Model Application Configuration](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-configuration-file-stage)
- [Resource Categories and Access](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/resource-categories-and-access)
- [Application Package Overview](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/application-package-overview)
- [HTTP Request Guide](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/http-request)
- [Permission Management](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/app-permission-mgmt)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [App Package Reference](artifact/references/app-package.md)
- [ArkTS Language Reference](artifact/references/arkts-language.md)
- [ArkUI Quick Reference](artifact/references/arkui-quickref.md)
- [HarmonyOS Glossary](artifact/references/glossary.md)
- [Media, AI, and Distributed Development Reference](artifact/references/media-ai-distributed.md)
- [Network and HTTP Reference](artifact/references/network-http.md)
- [Permission, Testing, and Release Reference](artifact/references/permission-testing.md)
- [Resource Management Reference](artifact/references/resource-management.md)
- [Stage Configuration Reference](artifact/references/stage-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with ArkTS, JSON5, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language development guidance with code examples and configuration snippets.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
