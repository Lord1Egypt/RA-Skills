## Description: <br>
Secure Google Docs Management - permission-based create, read, and edit doc content; manage sharing, permissions, rename and delete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to manage Google Docs through the PortEden CLI, including reading, creating, editing, sharing, renaming, exporting, and moving documents to trash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects PortEden to a Google account with Drive access, which can expose document data to the connected CLI workflow. <br>
Mitigation: Install only if PortEden is trusted, use the least-privileged token or profile available, and confirm the active token restrictions before use. <br>
Risk: Editing, sharing publicly, changing permissions, renaming, or deleting documents can affect sensitive files or collaborators. <br>
Mitigation: Verify provider-prefixed document IDs, sharing recipients, public access settings, and deletion intent before executing those commands. <br>


## Reference(s): <br>
- [PortEden homepage](https://porteden.com) <br>
- [ClawHub skill page](https://clawhub.ai/porteden/porteden-docs) <br>
- [PortEden publisher profile](https://clawhub.ai/user/porteden) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference compact JSON output from PortEden commands when users request machine-readable Google Docs results.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
