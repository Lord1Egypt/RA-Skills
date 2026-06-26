## Description: <br>
OpenClaw Memory-OS helps agents capture, store, and search local personal memories from conversations and selected files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local memory store for conversation facts, personal notes, and selected files, then retrieve them through keyword search, timeline views, or CLI/API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation details and imported file contents in a local memory store. <br>
Mitigation: Install only when a persistent local memory store is intended; do not store secrets, and regularly inspect or delete files under ~/.memory-os/. <br>
Risk: The release evidence notes conflicting documentation about automatic saving behavior. <br>
Mitigation: Treat phrases such as "remember", "save", and "记住" as save commands, and review what was stored after memory-triggering conversations. <br>
Risk: Broad imports can capture more personal or project data than intended. <br>
Mitigation: Use specific source paths, avoid importing broad folders such as the whole home or Documents directory, and review collected data before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhenstaff/memory-opportunity) <br>
- [Project homepage](https://github.com/ZhenRobotics/openclaw-memory-opportunity) <br>
- [README documentation](https://github.com/ZhenRobotics/openclaw-memory-opportunity/blob/main/README.md) <br>
- [npm package](https://www.npmjs.com/package/openclaw-memory-opportunity) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, TypeScript snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-management guidance and commands; saved memories are stored as local JSON files under ~/.memory-os/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact package version 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
