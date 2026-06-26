## Description: <br>
Helps agents integrate MobTech FlyVerify one-click login into existing iOS projects with minimal CocoaPods-based changes, privacy sequencing, login flow wiring, and project documentation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mobsupport](https://clawhub.ai/user/mobsupport) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers maintaining iOS apps use this skill to inspect an existing project, prepare FlyVerify configuration, add SDK dependencies, wire privacy consent and one-click login flows, and document the integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose or apply changes to iOS project configuration and source files. <br>
Mitigation: Review the proposed file changes before applying them, and keep changes scoped to the FlyVerify integration path. <br>
Risk: FlyVerify appKey and appSecret are sensitive configuration values. <br>
Mitigation: Treat appKey and appSecret as sensitive configuration, avoid exposing them in logs or public documentation, and review where they are stored. <br>
Risk: Dependency installation and build verification can change project state. <br>
Mitigation: Only approve pod install or build commands when ready for dependency and workspace changes, then inspect generated Podfile.lock and workspace updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mobsupport/ios-flyverify-integration) <br>
- [MobTech documentation center](https://www.mob.com/wiki/list) <br>
- [FlyVerify product page](https://www.mob.com/mobService/secverify) <br>
- [FlyVerify iOS integration guide](https://www.mob.com/wiki/detailed?wiki=531&id=78) <br>
- [FlyVerify SDK API documentation](https://www.mob.com/wiki/detailed?wiki=297&id=78) <br>
- [FlyVerify compliance guide](https://www.mob.com/wiki/detailed?wiki=217&id=78) <br>
- [FlyVerify iOS demo](https://github.com/MobClub/FlyVerify_For_iOS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code snippets, shell commands, and configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project files such as Podfile, Info.plist, bridging headers, login code, configuration templates, and FlyVerify_README.md after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
