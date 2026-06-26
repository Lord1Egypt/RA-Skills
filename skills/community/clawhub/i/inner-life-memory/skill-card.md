## Description: <br>
Inner Life Memory helps an agent carry structured local memory forward across sessions using confidence-scored memories, curiosity tracking, and follow-up questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DKistenev](https://clawhub.ai/user/DKistenev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers install this skill when they want an agent to maintain local memory continuity across sessions, integrate post-session reflections into memory files, and surface pending questions naturally on return. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally retains local memory across sessions, which may preserve sensitive or personal information if users store it there. <br>
Mitigation: Install only when persistent local memory is intended, periodically review the memory files, and avoid storing highly sensitive material unless retention is deliberate. <br>
Risk: The skill depends on inner-life-core initialization and its local state files before use. <br>
Mitigation: Review inner-life-core before running its initialization script, and confirm memory/inner-state.json and memory/drive.json exist before using this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DKistenev/inner-life-memory) <br>
- [openclaw-inner-life homepage](https://github.com/DKistenev/openclaw-inner-life) <br>
- [inner-life-memory source path](https://github.com/DKistenev/openclaw-inner-life/tree/main/skills/inner-life-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with file update instructions and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local memory files; requires jq and initialized inner-life-core state files.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
