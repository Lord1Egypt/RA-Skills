## Description: <br>
Google Drive (workspace.google.com). Use this skill for Google Drive requests, including reading, creating, updating, and deleting Drive data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an agent inspect Google Drive content and perform file, shared drive, permission, comment, reply, revision, label, approval, and change workflows through OOMOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Read actions can expose private Google Drive files, permissions, metadata, comments, labels, revisions, and change history to the agent. <br>
Mitigation: Install only for users who want an agent to access their OOMOL-connected Google Drive, and treat read results as sensitive. <br>
Risk: Write and destructive actions can change permissions, comments, labels, files, folders, shared drives, replies, revisions, or trash state. <br>
Mitigation: Inspect the live action schema, review the exact payload and effect, and require explicit user confirmation before state-changing or destructive operations. <br>
Risk: First-time setup may require installing or authenticating the oo CLI. <br>
Mitigation: Verify the oo CLI installer source before setup and only run authentication or connection steps after a relevant command fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-googledrive) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [Google Drive](https://workspace.google.com/products/drive/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Google Drive connector responses as JSON when actions are executed.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
