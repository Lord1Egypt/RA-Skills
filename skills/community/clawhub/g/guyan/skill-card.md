## Description: <br>
古言模式 - 极简中文压缩技能。绑定龙虾4号身份，默认古言输出。覆盖：语言压缩 + 角色身份 + 自动触发 + 多智能体调度 + 技术沟通桥接 + 记忆编写。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[golikegod](https://clawhub.ai/user/golikegod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to make an assistant default to concise Chinese 古言 or 文言 output, including persona-bound responses, compressed task coordination, technical summaries, and memory-note drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Compressed 古言 output can reduce clarity in legal, medical, security, or precise technical work. <br>
Mitigation: Use the normal-mode switch when clarity matters more than compression, and review high-stakes outputs before acting on them. <br>
Risk: Persona and formatting rules may over-constrain the assistant's responses. <br>
Mitigation: Treat the style as optional agent behavior and exit the mode with the documented switch when standard communication is needed. <br>
Risk: Generated memory notes may preserve inaccurate or unwanted summaries. <br>
Mitigation: Review generated memory entries before keeping them. <br>
Risk: The hosts-file example could be mistaken for permission to change system network settings. <br>
Mitigation: Do not modify system network settings without an explicit user request and a reviewed diff. <br>


## Reference(s): <br>
- [成语压缩词库](references/chengyu.md) <br>
- [文言单字词库](references/wenyan.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/golikegod/guyan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown or plain text in concise Chinese, with technical commands and logs preserved when present.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to compressed 古言 output and the 龙虾4号 persona until the user requests normal Chinese.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
