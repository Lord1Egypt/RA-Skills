## Description: <br>
上传雅思阅读复盘文件到服务器，支持 token 模式（进个人主页）和匿名模式。当用户想要上传已有的复盘 JSON、查看个人复盘仪表板时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and AI assistants use this skill to upload local IELTS reading review JSON files to www.liuxue.online, compare local and server records, and open the resulting progress dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads IELTS review data to www.liuxue.online and can use account tokens. <br>
Mitigation: Install only if that destination and token use are acceptable, and upload only review files the user has intentionally selected. <br>
Risk: Token setup and login flows store or read local account tokens. <br>
Mitigation: Prefer the documented token setup flow, keep token files private, and refresh or remove saved tokens if account access changes. <br>
Risk: Anonymous mode can send a stable identifier derived from local hostname and username. <br>
Mitigation: Use token mode instead, or avoid anonymous mode when local identity-derived identifiers should not be sent. <br>
Risk: The bundled publish script can install the ClawHub CLI and modify local skill installations. <br>
Mitigation: Do not run the publish script unless intentionally publishing or updating a local skill copy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dengjiawei1226/skills/ielts-tuyaya-upload) <br>
- [liuxue.online IELTS dashboard](https://www.liuxue.online/ielts/) <br>
- [liuxue.online IELTS reading dashboard](https://www.liuxue.online/ielts/reading.html) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with shell and Node.js commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt users for JSON file paths, account-token setup, upload confirmation, and follow-up dashboard links.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
