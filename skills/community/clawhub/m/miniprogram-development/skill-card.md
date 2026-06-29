## Description: <br>
Miniprogram Development helps agents build, debug, preview, test, publish, and optimize WeChat Mini Program projects, including CloudBase workflows when explicitly relevant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide agents through WeChat Mini Program project structure, page and component changes, configuration checks, preview/upload/publish workflows, and CloudBase integration when the project uses CloudBase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CloudBase MCP configuration, npx commands, device-code login, or environment selection can affect cloud resources. <br>
Mitigation: Review and approve MCP configuration, authentication flow, and target environment before execution; do not hard-code secrets. <br>
Risk: Preview, upload, or publish workflows can affect the state of a WeChat Mini Program release. <br>
Mitigation: Confirm project.config.json, appid, miniprogramRoot, and deployment readiness before preview, upload, or publish actions. <br>
Risk: CloudBase-specific guidance can be misapplied to a non-CloudBase mini program or mixed with web authentication patterns. <br>
Mitigation: Confirm the project uses CloudBase before applying wx.cloud patterns, and keep mini program authentication separate from web authentication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/binggg/skills/miniprogram-development) <br>
- [CloudBase Mini Program Integration](references/cloudbase-integration.md) <br>
- [Common Pitfalls in WeChat Mini Program Development](references/pitfalls.md) <br>
- [CloudBase WeChat Pay Mini Program Docs](https://docs.cloudbase.net/integration/wechat-pay-miniprogram/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.28.6 (source: server release metadata; artifact frontmatter version: 2.23.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
