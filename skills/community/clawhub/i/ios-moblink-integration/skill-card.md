## Description: <br>
面向 iOS 工程的 MobTech MobLink 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成场景还原依赖接入、Info.plist 配置、隐私合规、getMobId 制作场景、恢复代理回调和项目内说明文档落地。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and iOS engineers use this skill to integrate or troubleshoot MobTech MobLink in existing iOS projects. It helps scan project structure, plan minimal CocoaPods or manual SDK changes, configure Info.plist and privacy consent flow, connect MobId creation, and wire scene restoration callbacks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles privacy-sensitive SDK setup and can add MobLink configuration to an iOS app. <br>
Mitigation: Install it only for projects that intentionally need MobTech MobLink, review the proposed file changes, and complete App Store and privacy disclosures before release. <br>
Risk: MOBAppSecret is written to Info.plist as client-exposed app configuration. <br>
Mitigation: Treat MOBAppSecret as exposed mobile app configuration rather than a server secret, and avoid reusing it for unrelated confidential systems. <br>
Risk: Calling MobLink before user consent can create privacy compliance issues. <br>
Mitigation: Confirm the privacy-consent callback carefully and call uploadPrivacyPermissionStatus only after the user accepts the privacy policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mobsupport/ios-moblink-integration) <br>
- [MobTech documentation center](https://www.mob.com/wiki/list) <br>
- [MobLink product overview](https://www.mob.com/wiki/detailed?wiki=161&id=34) <br>
- [MobLink backend and project configuration](https://www.mob.com/wiki/detailed?wiki=527&id=34) <br>
- [MobLink iOS integration guide](https://www.mob.com/wiki/detailed?wiki=83&id=34) <br>
- [MobLink iOS SDK API](https://www.mob.com/wiki/detailed?wiki=553&id=34) <br>
- [MobLink iOS compliance guide](https://www.mob.com/wiki/detailed?wiki=220&id=34) <br>
- [MobLink Web integration](https://www.mob.com/wiki/detailed?wiki=525&id=34) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks, configuration snippets, shell commands, and generated project documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate an Excel configuration template and a MobLink_README.md file when used in a target iOS project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
