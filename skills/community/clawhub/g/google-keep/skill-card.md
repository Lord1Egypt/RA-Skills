## Description: <br>
Read, create, edit, search, and manage Google Keep notes and lists via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tag-assistant](https://clawhub.ai/user/tag-assistant) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can use this skill to operate Google Keep from a terminal, including note search, creation, editing, checklist updates, labeling, archiving, and JSON export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a long-lived Google master token that can grant broader account access than a notes-only tool needs. <br>
Mitigation: Use a dedicated or low-risk Google account, keep the skill configuration directory private, and remove the stored token and cached state when finished. <br>
Risk: Create, edit, checklist, archive, label, and delete commands can change Google Keep data. <br>
Mitigation: Export or back up important notes before bulk edits or deletes, and review command targets carefully before running write operations. <br>
Risk: The skill depends on unofficial Google Keep and Google Play Services authentication libraries, so compatibility can change outside the skill publisher's control. <br>
Mitigation: Review dependency behavior before deployment and be prepared to re-authenticate or pause use if Google changes the underlying service behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tag-assistant/google-keep) <br>
- [gkeepapi](https://github.com/kiwiz/gkeepapi) <br>
- [gpsoauth](https://github.com/simon-weber/gpsoauth) <br>
- [Google Embedded Setup](https://accounts.google.com/EmbeddedSetup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Configuration instructions] <br>
**Output Format:** [Markdown guidance with CLI commands; runtime output is terminal text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can read and modify Google Keep notes and stores local credential and state files under the skill configuration directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
