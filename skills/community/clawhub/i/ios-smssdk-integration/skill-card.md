## Description:

面向 iOS 工程的 MobTech SMSSDK 短信验证集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成依赖接入、隐私合规、短信验证码发送/校验链路和项目内说明文档落地。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate or troubleshoot MobTech SMSSDK SMS verification in existing iOS apps. It helps plan and apply minimal project changes for CocoaPods dependencies, Info.plist configuration, privacy consent handling, verification-code send and submit flows, and project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated configuration workbook can contain MobTech AppSecret values.

Mitigation: Keep the workbook out of version control and avoid sharing project archives that contain it.

Risk: CocoaPods dependency changes can alter the iOS project's dependency graph.

Mitigation: Review Podfile.lock changes before accepting CocoaPods installation or builds.

Risk: SMSSDK functionality depends on privacy consent handling before SDK use.

Mitigation: Call the MobSDK privacy authorization upload only after the user accepts the app privacy policy and before using SMS verification features.

## Reference(s):

- [MobTech Documentation Center](https://www.mob.com/wiki/list)
- [MobTech SDK Download Center](https://www.mob.com/download)
- [MobTech Create Application](https://www.mob.com/wiki/detailed?wiki=539&id=23)
- [MobTech SMSSDK Integration Guide](https://www.mob.com/wiki/detailed?wiki=110&id=23)
- [MobTech SMSSDK API Documentation](https://www.mob.com/wiki/detailed?wiki=467&id=23)
- [MobTech Compliance Guide](https://www.mob.com/wiki/detailed?wiki=211&id=23)
- [MobTech SMSSDK Extended Business Settings](https://www.mob.com/wiki/detailed?wiki=671&id=23)
- [MobTech SMSSDK Error Codes](https://www.mob.com/wiki/detailed?wiki=468&id=23)
- [App Store Connect Privacy Data Configuration](https://www.mob.com/wiki/detailed?wiki=573&id=23)
- [MobTech Additional App Data Collection Controller](https://www.mob.com/wiki/detailed?wiki=675&id=714)
- [MobTech SMSSDK Privacy Policy](https://policy.zztfly.com/sdk/sms/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown responses with inline code, shell commands, project-file edits, configuration guidance, and generated workbook or README files when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese user-facing responses and keeps code, configuration keys, class names, and command names in their original form.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
