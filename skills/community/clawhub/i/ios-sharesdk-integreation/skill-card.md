## Description:

面向 iOS 工程的 MobTech ShareSDK 集成 skill。默认优先使用 CocoaPods，先扫描工程，再串行确认阻塞项，最后以最小改动完成接入、隐私合规与项目内说明文档落地。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate MobTech ShareSDK into iOS projects, configure CocoaPods dependencies, platform credentials, URL schemes, Universal Links, privacy-gated initialization, and project documentation with minimal changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can collect production ShareSDK and platform credentials in a plaintext ShareSDK_Config.xlsx file.

Mitigation: Use throwaway or restricted app credentials where possible, keep ShareSDK_Config.xlsx out of version control and CI artifacts, and delete or redact it after integration.

Risk: Some provider secrets may be copied into app configuration that is distributed in a mobile app bundle.

Mitigation: Avoid placing provider secrets in a mobile app bundle unless the provider explicitly documents that the value is safe for client distribution.

Risk: The skill can modify iOS project dependencies, Info.plist entries, URL schemes, Universal Links, and initialization code.

Mitigation: Review the proposed minimal change plan before applying edits, and verify that only user-enabled platforms are configured.

## Reference(s):

- [MobTech ShareSDK iOS documentation](https://www.mob.com/wiki/detailed?wiki=4&id=14)
- [MobTech ShareSDK iOS documentation](https://www.mob.com/wiki/detailed?wiki=500&id=14)
- [MobTech ShareSDK related documentation](https://www.mob.com/wiki/detailed?wiki=499&id=14)
- [MobTech ShareSDK related documentation](https://www.mob.com/wiki/detailed?wiki=747&id=14)
- [ShareSDK privacy policy](https://policy.zztfly.com/sdk/share/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and optional generated Excel workbook files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default responses are in Chinese; code, configuration keys, class names, and command names retain their original spelling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
