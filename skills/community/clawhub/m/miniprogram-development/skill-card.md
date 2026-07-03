## Description: <br>
WeChat Mini Program development skill for building, debugging, previewing, testing, publishing, and optimizing mini program projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binggg](https://clawhub.ai/user/binggg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, modify, debug, preview, test, publish, and optimize WeChat Mini Program projects, including CloudBase integrations when the project explicitly uses CloudBase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preview, upload, publish, or CloudBase MCP actions could target the wrong Mini Program appid or CloudBase environment. <br>
Mitigation: Confirm project.config.json, appid, miniprogramRoot, CloudBase environment, and deployment checklist status before preview, upload, publish, or MCP calls. <br>
Risk: Device-code authentication or MCP configuration changes may affect local CloudBase tooling access. <br>
Mitigation: Review mcporter or MCP configuration changes and use interactive device-code authentication instead of embedding long-lived credentials. <br>
Risk: Generated guidance could mix Web authentication patterns into WeChat Mini Program projects. <br>
Mitigation: Use wx.cloud Mini Program APIs and server-side OPENID handling for CloudBase projects, and avoid Web SDK login flows unless the project scope is explicitly Web. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/binggg/skills/miniprogram-development) <br>
- [Current Raw Source](https://cnb.cool/tencent/cloud/cloudbase/cloudbase-skills/-/git/raw/main/skills/cloudbase/references/miniprogram-development/SKILL.md) <br>
- [CloudBase Mini Program Integration](references/cloudbase-integration.md) <br>
- [Common Pitfalls](references/pitfalls.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file changes, preview/upload commands, CloudBase MCP setup, and Mini Program project configuration checks.] <br>

## Skill Version(s): <br>
1.28.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
