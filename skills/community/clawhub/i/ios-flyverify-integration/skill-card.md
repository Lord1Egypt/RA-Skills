## Description:

Guides agents through MobTech FlyVerify one-click-login integration for iOS projects by scanning the project, preferring CocoaPods, wiring privacy and login flows, and adding project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobsupport](https://clawhub.ai/user/mobsupport)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or troubleshoot MobTech FlyVerify one-click login in existing iOS apps while preserving existing privacy-consent and login flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle FlyVerify service credentials in project files or a generated configuration workbook.

Mitigation: Keep FlyVerify_iOS_Config.xlsx out of source control, avoid hard-coding real secrets where possible, and review where appKey and appSecret are stored before committing changes.

Risk: The skill can modify an iOS project dependency graph and build settings while integrating CocoaPods and FlyVerify.

Mitigation: Review the proposed file changes before execution, pin and inspect Podfile.lock changes, and run project build verification after dependency updates.

Risk: Disabling Xcode user script sandboxing can weaken local build isolation.

Mitigation: Avoid disabling ENABLE_USER_SCRIPT_SANDBOXING except temporarily in an isolated build environment when needed to diagnose CocoaPods resource script failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobsupport/skills/ios-flyverify-integration)
- [MobTech documentation center](https://www.mob.com/wiki/list)
- [FlyVerify product page](https://www.mob.com/mobService/secverify)
- [MobTech SDK download center](https://www.mob.com/download)
- [FlyVerify integration guide](https://www.mob.com/wiki/detailed?wiki=531&id=78)
- [FlyVerify SDK API documentation](https://www.mob.com/wiki/detailed?wiki=297&id=78)
- [FlyVerify compliance guide](https://www.mob.com/wiki/detailed?wiki=217&id=78)
- [FlyVerify privacy policy](https://policy.zztfly.com/sdk/verify/privacy)
- [MobTech app creation guide](https://www.mob.com/wiki/detailed?wiki=538&id=78)
- [FlyVerify review process](https://www.mob.com/wiki/detailed?wiki=159&id=78)
- [FlyVerify server integration documentation](https://www.mob.com/wiki/detailed?wiki=157&id=78)
- [FlyVerify iOS demo](https://github.com/MobClub/FlyVerify_For_iOS)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration edits, and generated project documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate a FlyVerify_iOS_Config.xlsx template and a project-level FlyVerify_README.md when used in an iOS project.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
