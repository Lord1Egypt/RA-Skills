## Description: <br>
终极AI智能体记忆系统，结合写前日志、向量搜索、git-notes、Markdown档案以及可选云备份来帮助代理保留和检索上下文。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent users use this skill to initialize and operate persistent memory workflows for projects, including active session state, curated Markdown archives, daily logs, semantic recall, and optional cloud memory integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can capture broad user or project context, including sensitive information if used without boundaries. <br>
Mitigation: Use the skill only in intended workspaces, keep memory files scoped to non-sensitive projects, and review stored memory regularly. <br>
Risk: Optional SuperMemory and Mem0 integrations may store memory content with third-party services. <br>
Mitigation: Enable those integrations only after accepting their data flows, configure API keys deliberately, and avoid sending sensitive material. <br>
Risk: Vector cleanup guidance can delete local memory data. <br>
Mitigation: Back up memory stores and archives before running destructive cleanup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/maske-elite-memory) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [npm package](https://www.npmjs.com/package/elite-longterm-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and a Node.js CLI that creates Markdown memory files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can create SESSION-STATE.md, MEMORY.md, and daily log files in the current workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
