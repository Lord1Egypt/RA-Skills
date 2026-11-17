## Description:

面向 iOS 工程的 MobTech MobLink 集成 skill。默认先扫描工程，优先使用 CocoaPods，以最小改动完成场景还原依赖接入、Info.plist 配置、隐私合规、getMobId 制作场景、恢复代理回调和项目内说明文档落地。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or troubleshoot MobTech MobLink in iOS projects with minimal project changes. It guides project scanning, CocoaPods or manual SDK integration, Info.plist configuration, privacy-consent placement, scene creation, scene restoration callbacks, and project documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify iOS project files and dependency state while adding MobTech MobLink.

Mitigation: It requires project scanning, presents a minimum-change plan, and gates dependency installation or build commands behind user confirmation.

Risk: Filled MobLink configuration and Info.plist values may contain app-identifying or sensitive configuration.

Mitigation: Review the generated Excel workbook and Info.plist changes before committing, and avoid committing filled configuration workbooks.

Risk: Incorrect privacy-consent placement or optional collection of IDFA, location, WiFi, or IP data can create compliance risk.

Mitigation: Confirm privacy-consent placement and extended data collection settings with the app owner and legal or compliance process before enabling those flows.

Risk: Dependency updates may resolve to unexpected CocoaPods versions.

Mitigation: Review the resolved CocoaPods version and Podfile.lock before accepting dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/ios-moblink-integration)
- [MobTech documentation center](https://www.mob.com/wiki/list)
- [MobLink product overview](https://www.mob.com/wiki/detailed?wiki=161&id=34)
- [MobTech app creation workflow](https://www.mob.com/wiki/detailed?wiki=478&id=34)
- [MobLink dashboard and project configuration](https://www.mob.com/wiki/detailed?wiki=527&id=34)
- [MobLink iOS integration guide](https://www.mob.com/wiki/detailed?wiki=83&id=34)
- [MobLink iOS SDK API](https://www.mob.com/wiki/detailed?wiki=553&id=34)
- [MobLink iOS compliance guide](https://www.mob.com/wiki/detailed?wiki=220&id=34)
- [MobLink extended business feature settings](https://www.mob.com/wiki/detailed?wiki=673&id=34)
- [MobLink web integration](https://www.mob.com/wiki/detailed?wiki=525&id=34)
- [App Store Connect privacy data configuration](https://www.mob.com/wiki/detailed?wiki=574&id=34)
- [Other app data collection controller configuration](https://www.mob.com/wiki/detailed?wiki=675&id=714)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Files, Guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and generated project files such as an Excel configuration template and MobLink_README.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default response language is Chinese; code, configuration keys, class names, and command names remain in their original form.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
