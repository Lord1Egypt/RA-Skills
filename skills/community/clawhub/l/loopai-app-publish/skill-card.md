## Description: <br>
用于将应用信息（名称、链接、截图、作者、社区等）提交到 App Hub 展示中心。支持创建新的 AI 应用、软件或工具的展示页面。也适用于生成和发布 Loop App、Loop 小程序、Loop 网站、Loop 应用等场景。提交前会自动通过 curl 验证 app_url 是否可访问，不可访问则拒绝提交并提示用户修正。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeamchen](https://clawhub.ai/user/jeamchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and app publishers use this skill to create, validate, inspect, and update App Hub showcase listings for AI applications, tools, Loop apps, Loop mini apps, Loop websites, and related software. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verbose/debug output can expose the local App Hub token while the skill performs authenticated operations. <br>
Mitigation: Do not use --verbose unless token redaction is fixed; avoid sharing logs from authenticated runs. <br>
Risk: The skill can create, read, and update App Hub listings using the user's token. <br>
Mitigation: Install and run only when you trust the skill, and review app IDs plus JSON batch files before execution. <br>
Risk: URL validation uses outbound checks against provided app URLs. <br>
Mitigation: Use public app URLs only for validation and avoid submitting private or sensitive internal URLs. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jeamchen/loopai-app-publish) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [create_app.py](artifact/scripts/create_app.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May validate public URLs and make authenticated App Hub API calls to create, read, or update listings.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
