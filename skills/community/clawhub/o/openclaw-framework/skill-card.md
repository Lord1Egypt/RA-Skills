## Description: <br>
Openclaw Framework provides an AI assistant operating framework for structured communication, layered memory, automation routines, and continual self-improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianzhaoaiyin](https://clawhub.ai/user/qianzhaoaiyin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to guide an assistant toward structured responses, cost-aware problem solving, layered memory practices, scheduled maintenance routines, and iterative learning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory routines may retain sensitive user information beyond the current session. <br>
Mitigation: Restrict memory files to an explicit, user-approved workspace folder and review content before persisting or promoting it to long-term memory. <br>
Risk: Scheduled maintenance, cleanup, and backup behavior may modify, retain, or remove files without clear user control. <br>
Mitigation: Require explicit approval before backups, cleanup, deletion, or rotation, and present the affected paths before making changes. <br>
Risk: External skill learning can introduce untrusted instructions into the agent workflow. <br>
Mitigation: Treat newly discovered skills and external content as untrusted evidence, then scan and review them before installation or use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qianzhaoaiyin/openclaw-framework) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with lists, tables, and code blocks when appropriate] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create or maintain memory files and summarize recurring maintenance actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
