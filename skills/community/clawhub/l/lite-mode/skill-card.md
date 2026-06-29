## Description: <br>
Runs OpenClaw on low-RAM machines (2-4 GB) by trimming context, throttling skills, and checking memory before heavy operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirajmahmudul](https://clawhub.ai/user/mirajmahmudul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to keep agent sessions usable on low-RAM machines by checking free memory, limiting context growth, and throttling heavier capabilities when memory is tight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce shorter responses or skip browser and image tools when memory is low. <br>
Mitigation: Use it when reduced memory use is more important than full capability, and re-run work after memory recovers if skipped tools are needed. <br>
Risk: Long sessions may be summarized to control context size, which can omit older details from the active working context. <br>
Mitigation: Keep critical requirements in recent turns or restate them after context trimming. <br>
Risk: The optional configuration snippet disables heavier tools if copied into a local OpenClaw configuration. <br>
Mitigation: Copy only the needed fields and restore tool settings when low-memory operation is no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirajmahmudul/skills/lite-mode) <br>
- [Project homepage](https://github.com/mirajmahmudul/openclaw-lite-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise responses, memory status reporting, context trimming guidance, and optional low-memory configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
