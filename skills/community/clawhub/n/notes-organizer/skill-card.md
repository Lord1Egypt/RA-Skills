## Description: <br>
A note organization and knowledge-linking tool that analyzes a Markdown notes directory, reorganizes notes according to a chosen classification scheme, and adds Obsidian-style bidirectional links between related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youningnihaobang](https://clawhub.ai/user/youningnihaobang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, students, and knowledge workers use this skill to organize Markdown or Obsidian note vaults, move notes into a selected directory structure, and add simple wiki-style links between related notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bulk move and edit Markdown files in place without strong preview, rollback, or confirmation safeguards. <br>
Mitigation: Run it on a copied or backed-up notes vault first, then review the reorganized files and inserted links before relying on the result. <br>
Risk: The advertised undo and backup behavior should not be treated as a reliable restore mechanism. <br>
Mitigation: Use an external backup or version-controlled copy as the recovery path and treat .organize_log.json as an activity record only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/youningnihaobang/notes-organizer) <br>
- [Skill README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with Obsidian-style links, command-line prompts, and a JSON operation log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on the user-provided notes directory and writes .organize_log.json in that directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
