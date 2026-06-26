## Description: <br>
Integrates with the macOS Notes app to create, list, read, update, delete, and search notes through a Node.js CLI that bridges to AppleScript. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swancho](https://clawhub.ai/user/swancho) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to let an agent manage Apple Notes through explicit CLI commands for note creation, retrieval, editing, deletion, and search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, update, append to, and delete Apple Notes, including notes that may contain sensitive personal or business information. <br>
Mitigation: Install only when Notes access is intended, use folder-scoped commands where possible, and require explicit approval before update, append, or delete actions. <br>
Risk: Apple Notes does not expose stable IDs, and duplicated note titles can cause actions to target the most recently created matching note. <br>
Mitigation: Use folder and title together when locating notes, review the target note before mutation, and avoid destructive actions when duplicate titles are present. <br>
Risk: Broad searches can expose snippets from sensitive notes. <br>
Mitigation: Prefer folder-scoped searches and avoid broad queries across all notes unless the user has approved the scope. <br>


## Reference(s): <br>
- [Mac Notes Agent ClawHub Listing](https://clawhub.ai/swancho/mac-notes-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses from CLI commands, with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on the default Apple Notes account and may be folder-scoped.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
