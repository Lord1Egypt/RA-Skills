## Description: <br>
OneDrive lets an agent operate a connected OneDrive account through OOMOL's one_drive connector for drive metadata, item lookup, folder listing, search, file transfers, and controlled write operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent read, search, transfer, upload, rename, move, update, and delete files in a connected OneDrive account with confirmation for state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access files and folders through a connected OneDrive account. <br>
Mitigation: Install it only when the agent should operate OneDrive, and provide explicit file paths, item IDs, and intended actions. <br>
Risk: Write and destructive actions can upload, overwrite, move, rename, update, or delete OneDrive content. <br>
Mitigation: Require user confirmation before uploads, overwrites, moves, deletes, sharing changes, or other state-changing operations. <br>
Risk: Broad activation wording could cause the skill to be selected for more OneDrive-related requests than intended. <br>
Mitigation: Use the skill only for requests that require OneDrive account operations and confirm the exact operation before changing state. <br>


## Reference(s): <br>
- [ClawHub OneDrive skill](https://clawhub.ai/oomol/oo-one-drive) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OneDrive](https://www.microsoft.com/microsoft-365/onedrive/online-cloud-storage) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the oo CLI and return JSON responses; file download actions can produce transferred files.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
