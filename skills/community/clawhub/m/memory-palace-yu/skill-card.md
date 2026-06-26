## Description: <br>
Memory Palace activates a user-selected Markdown memory folder so an assistant can load identity notes, knowledge, and methods for personalized conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarkMa84](https://clawhub.ai/user/MarkMa84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and knowledge workers use this skill to let an agent read their own Markdown notes and adapt replies to their identity, style, prior insights, and methods. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected memory folder may contain personal notes, secrets, regulated data, or third-party private information. <br>
Mitigation: Keep sensitive information out of the memory folder and install only when assistant access to that folder is intended. <br>
Risk: A .memory-path file can point the assistant at an unexpected folder. <br>
Mitigation: Review the .memory-path setting before activation and confirm it points only to the intended Markdown memory directory. <br>
Risk: Automatic memory updates can persist inaccurate or unwanted details. <br>
Mitigation: Approve each proposed memory write manually before saving it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarkMa84/memory-palace-yu) <br>
- [Skill instructions](SKILL.md) <br>
- [Memory concept template](examples/memory/00-概念模板.md) <br>
- [Daily memory template](examples/memory/日记录模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and memory note templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The assistant may propose reading from or writing to a user-selected Markdown memory folder; memory writes should be reviewed manually.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
