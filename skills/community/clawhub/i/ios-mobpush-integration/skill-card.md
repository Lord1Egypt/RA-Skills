## Description:

Guides agents through MobTech MobPush integration for iOS projects, including project scanning, CocoaPods setup, APNs configuration, privacy compliance, callback wiring, and project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate or troubleshoot MobTech MobPush in existing iOS applications with minimal project changes. It helps plan CocoaPods dependency setup, APNs readiness, privacy-consent wiring, notification callbacks, optional Live Activity support, and project-local documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow collects a MobPush app secret and may place it in project configuration files.

Mitigation: Keep MobPush_iOS_Config.xlsx out of source control, delete or move the populated workbook after use, and treat MOBAppSecret in Info.plist as client-extractable.

Risk: Dependency changes can alter the iOS project build state.

Mitigation: Pin and review the mob_pushsdk version, then run pod install or pod update only after checking the proposed file changes and target selection.

Risk: Incorrect target or privacy-consent placement can break integration or compliance behavior.

Mitigation: Review the workflow before installation and confirm target selection and privacy-consent callback placement before modifying project files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mobsupport/skills/ios-mobpush-integration)
- [MobTech Documentation Center](https://www.mob.com/wiki/list)
- [MobPush Product Page](https://www.mob.com/mobService/mobpush)
- [SDK Download Center](https://www.mob.com/download)
- [Create Application Workflow](https://www.mob.com/wiki/detailed?wiki=494&id=136)
- [MobPush Compliance Guide](https://www.mob.com/wiki/detailed?wiki=501&id=136)
- [MobPush Integration Guide](https://www.mob.com/wiki/detailed?wiki=502&id=136)
- [MobPush SDK API Documentation](https://www.mob.com/wiki/detailed?wiki=503&id=136)
- [APNs Certificate Configuration](https://www.mob.com/wiki/detailed?wiki=504&id=136)
- [App Store Connect Privacy Data Configuration](https://www.mob.com/wiki/detailed?wiki=570&id=136)
- [MobPush Extended Feature Settings](https://www.mob.com/wiki/detailed?wiki=665&id=136)
- [Extended Data Collection Controller Configuration](https://www.mob.com/wiki/detailed?wiki=675&id=714)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, configuration snippets, and proposed shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create project files such as an Excel configuration workbook and MobPush_README.md after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
