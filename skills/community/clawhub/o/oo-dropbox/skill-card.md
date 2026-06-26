## Description: <br>
Operate Dropbox through an OOMOL-connected account for reading, creating, updating, sharing, moving, restoring, uploading, downloading, and deleting Dropbox data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage Dropbox files, folders, shared links, revisions, tags, and account metadata through the OOMOL Dropbox connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make sensitive Dropbox account changes, including uploads, moves, shared-link changes, restores, and deletes. <br>
Mitigation: Require explicit user confirmation for uploads, moves, edits, sharing changes, destructive actions, and bulk operations before running connector commands. <br>
Risk: Overly broad activation wording may route casual Dropbox mentions into this skill. <br>
Mitigation: Narrow activation wording so the skill is used only when the user clearly asks the agent to operate Dropbox. <br>


## Reference(s): <br>
- [Dropbox homepage](https://www.dropbox.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-dropbox) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the OOMOL oo CLI and return connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
