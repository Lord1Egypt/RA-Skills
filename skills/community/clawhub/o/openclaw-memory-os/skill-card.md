## Description: <br>
OpenClaw Memory-OS provides a local conversation and file memory workflow for saving, searching, and recalling personal knowledge through CLI and agent usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhenstaff](https://clawhub.ai/user/zhenstaff) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to install and operate a local memory system that stores selected conversations, notes, files, and searchable personal knowledge under the user's control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversations and files into local memory storage, and the security summary notes inconsistent privacy safeguards. <br>
Mitigation: Keep AUTO-TRIGGER disabled until tested, prefer manual save commands, and review saved memory files regularly. <br>
Risk: Release provenance is unavailable and artifact documentation contains inconsistent version and source references. <br>
Mitigation: Verify the exact npm package and matching source commit before installation or use. <br>
Risk: Stored memories may be readable as plaintext under ~/.memory-os. <br>
Mitigation: Restrict file permissions, collect only specific non-sensitive folders, and add encryption or encrypted storage where confidentiality is required. <br>


## Reference(s): <br>
- [OpenClaw Memory-OS homepage](https://github.com/ZhenRobotics/openclaw-memory-os) <br>
- [OpenClaw Memory-OS README](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install and operate an external npm CLI that writes local JSON memory files under ~/.memory-os/.] <br>

## Skill Version(s): <br>
0.1.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
