## Description: <br>
WeChat Mini Program development skill for building, debugging, previewing, testing, publishing, and optimizing mini program projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, modify, debug, preview, test, publish, and optimize WeChat Mini Program projects. It also guides CloudBase integration when the project explicitly uses wx.cloud, Tencent CloudBase, or related mini program cloud workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CloudBase workflows may use npx-based tooling, device-code login, and MCP configuration changes that can affect a user's cloud environment. <br>
Mitigation: Review the MCP configuration, inspect tool schemas before calling them, use interactive authentication, and confirm the target CloudBase environment before making changes. <br>
Risk: Preview, upload, and publish actions can affect WeChat Mini Program or CloudBase release state. <br>
Mitigation: Confirm appid, miniprogramRoot, CloudBase environment, and deployment readiness before running preview, upload, or publish commands. <br>
Risk: Mini Program projects can fail when web authentication patterns, unsupported JavaScript syntax, or mismatched environment settings are introduced. <br>
Mitigation: Keep mini program and web patterns separate, prefer broadly compatible syntax, and validate behavior in WeChat Developer Tools or on a real device. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/binggg/skills/miniprogram-development) <br>
- [CloudBase Mini Program Integration](references/cloudbase-integration.md) <br>
- [Common Pitfalls in WeChat Mini Program Development](references/pitfalls.md) <br>
- [CloudBase WeChat Pay Mini Program Documentation](https://docs.cloudbase.net/integration/wechat-pay-miniprogram/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, JSON, WXML/WXSS, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed project file changes, preview/upload commands, CloudBase configuration guidance, and real-device validation steps.] <br>

## Skill Version(s): <br>
1.28.4 (source: ClawHub release metadata; artifact frontmatter reports 2.23.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
