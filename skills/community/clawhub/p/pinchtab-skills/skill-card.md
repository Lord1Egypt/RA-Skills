## Description: <br>
通过 PinchTab HTTP API 控制无头或有头 Chrome 浏览器，用于网页自动化、爬虫、表单填充、导航、截图和数据提取 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HelloTomBruce](https://clawhub.ai/user/HelloTomBruce) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to control a local Chrome instance through PinchTab for web navigation, crawling, form filling, screenshots, PDF export, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of a real Chrome instance, which can expose authenticated browser sessions if a saved personal or work profile is used. <br>
Mitigation: Run PinchTab with a dedicated empty browser profile and avoid pointing it at daily-use Chrome profiles. <br>
Risk: An exposed PinchTab API without authentication could allow unauthorized browser control. <br>
Mitigation: Keep the API bound to localhost by default and set BRIDGE_TOKEN before any remote exposure. <br>
Risk: Profile deletion or cleanup commands can remove browser state and should not be executed blindly. <br>
Mitigation: Verify profile paths before running deletion commands and keep automation profiles separate from personal data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/HelloTomBruce/pinchtab-skills) <br>
- [API reference](references/api.md) <br>
- [Environment variables reference](references/env.md) <br>
- [Profile management](references/profiles.md) <br>
- [Security model](TRUST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation commands, API request examples, extracted page text, screenshots, or PDF export guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
