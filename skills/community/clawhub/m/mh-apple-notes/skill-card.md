## Description: <br>
Manage Apple Notes via the `memo` CLI on macOS to create, view, edit, delete, search, move, and export notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage local Apple Notes from an agent on macOS through the `memo` command-line tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, edit, export, move, and delete local Apple Notes through the memo CLI. <br>
Mitigation: Install only if the user trusts the upstream memo CLI, confirm before edits, moves, exports, or deletions, and use clear note or folder requests. <br>
Risk: Apple Notes automation access can expose local notes to command-line workflows. <br>
Mitigation: Grant Notes automation permissions only when needed and review macOS privacy settings for the local agent environment. <br>
Risk: The artifact notes that memo cannot edit notes containing images or attachments. <br>
Mitigation: Use the skill for text-oriented notes and handle attachment-heavy notes manually in Notes.app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-apple-notes) <br>
- [memo CLI project](https://github.com/antoniorodr/memo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for macOS Apple Notes operations through the locally installed `memo` CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
