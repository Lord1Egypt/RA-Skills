## Description: <br>
Helps an agent work in Kimi Group Chat and Sessions by reading group rules, members, recent messages, files, and replying in the correct group or thread context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yurken](https://clawhub.ai/user/yurken) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents in Kimi group-chat workspaces use this skill to gather group context, manage workspace-scoped memory, coordinate bounded peer replies, and send messages or files in the correct group or thread. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Group messages, member lists, attachments, and workspace memory may contain sensitive information. <br>
Mitigation: Use only in intended Kimi group-chat contexts and review or clear .openclaw workspace memory when needed. <br>
Risk: The skill can guide an agent to send group or thread messages and attach files through the Kimi IM CLI. <br>
Mitigation: Review message targets and file attachments before sending, and follow the Coordinator-scoped interaction rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yurken/kimiim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance, Files] <br>
**Output Format:** [Plain text with kimiim-cli command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include workspace-scoped memory and file paths under .openclaw/workspace/kimi-group-chat/{group-name}/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
