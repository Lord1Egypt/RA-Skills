## Description: <br>
Notesctl manages Apple Notes through deterministic local scripts for creating, listing, searching, exporting, and editing notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clinchcc](https://clawhub.ai/user/clinchcc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to manage Apple Notes with bundled local scripts that create notes, list folders, search note contents, and export selected notes while keeping agent instructions concise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted or unusual Apple Notes folder names could trigger unintended local automation. <br>
Mitigation: Use trusted, simple folder names and review each note operation before execution until folder escaping is fixed. <br>
Risk: Search and export operations can expose private Apple Notes content. <br>
Mitigation: Treat searches and exports as sensitive data access and confirm the requested scope before running them. <br>
Risk: The skill depends on local macOS automation and the memo CLI. <br>
Mitigation: Install only in trusted macOS environments where memo, python3, and osascript are expected and trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clinchcc/notesctl-skill-for-openclaw) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/clinchcc) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and short command receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can export selected Apple Notes to files through an interactive local command.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
