## Description: <br>
从本地 OpenClaw 数据生成或迭代 OpenCard 个人名片，读取工作区身份信息、配置和会话统计，渲染 HTML 预览并导出 PNG，且不写入用户档案数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timothyliew2](https://clawhub.ai/user/timothyliew2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to turn local profile, memory, configuration, and usage statistics into a shareable OpenCard profile image. It supports an iterative workflow that collects data, lets the agent draft public-facing copy, renders an HTML preview, and exports a PNG. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw profile and memory files that may contain sensitive personal notes. <br>
Mitigation: Review or redact USER.md, IDENTITY.md, and MEMORY.md before running the workflow or sharing generated output. <br>
Risk: Profile and memory excerpts may be sent to the configured model provider when the agent uses a cloud model to draft card copy. <br>
Mitigation: Use a local model for sensitive notes, or remove sensitive excerpts before copy generation. <br>
Risk: Generated card copy can reveal private context if shared without review. <br>
Mitigation: Preview the HTML and final PNG and remove unwanted personal details before publication. <br>
Risk: Untrusted background input could affect the rendered card or expose request metadata during browser rendering. <br>
Mitigation: Use the default background or a trusted local background path. <br>


## Reference(s): <br>
- [OpenCard data flow](references/data-flow.md) <br>
- [Background card template](references/background-template.html) <br>
- [ClawHub release page](https://clawhub.ai/timothyliew2/open-card) <br>
- [Default background image](https://pub-626ee41d8f1544638070799686c756bf.r2.dev/open-card-bg.png) <br>
- [Node.js](https://nodejs.org/) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON data, HTML preview, and PNG image export with Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw profile and session metadata; generated public copy should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
