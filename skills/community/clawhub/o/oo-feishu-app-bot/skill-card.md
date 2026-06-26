## Description: <br>
Feishu App Bot (open.feishu.cn) helps agents read, create, update, and delete Feishu/Lark app bot data through the OOMOL connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Feishu/Lark app bot chats, messages, reactions, pins, and file or image workflows through an OOMOL-connected account. It supports both read operations and state-changing message actions when the user confirms the intended payload and effect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write actions can change Feishu/Lark bot message state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running actions tagged as write operations. <br>
Risk: Destructive actions can remove reactions or pin state. <br>
Mitigation: Require explicit user approval for the target and action before running commands tagged as destructive. <br>
Risk: Publisher maintenance and connector behavior are third-party controlled. <br>
Mitigation: Install only when the OOMOL publisher and connected Feishu/Lark workspace are trusted, and use the documented authentication and audit paths for state-changing actions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/oomol/oo-feishu-app-bot) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Feishu App Bot homepage](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls, Files] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; command responses may include JSON data and an execution id.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
