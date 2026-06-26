## Description: <br>
Local memory system with structured indexing, heuristic recall, auto-write behavior, and optional auto-learning when local knowledge is insufficient. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhelong0907](https://clawhub.ai/user/lizhelong0907) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent users use Memory Master to add a local structured memory workflow for recording decisions, recalling prior context, and maintaining indexed knowledge files across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initialization can rewrite persistent agent control files such as AGENTS.md, MEMORY.md, and HEARTBEAT.md. <br>
Mitigation: Review the templates and initialization behavior first, keep the automatic backup, and run the skill in a disposable workspace before installing it in a primary workspace. <br>
Risk: Persistent instructions can encourage broad automatic behaviors, including web learning and heartbeat routines. <br>
Mitigation: Disable or edit the web-learning and heartbeat sections if those behaviors are not desired for the workspace. <br>
Risk: Local memory and knowledge files can accumulate sensitive project context over time. <br>
Mitigation: Keep generated memory files local, review them periodically, and remove sensitive entries before sharing or archiving a workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lizhelong0907/memory-master) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local workspace memory files, indexes, AGENTS.md, MEMORY.md, and HEARTBEAT.md during initialization.] <br>

## Skill Version(s): <br>
2.6.5 (source: server release evidence and package.json; SKILL.md frontmatter still says 2.6.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
