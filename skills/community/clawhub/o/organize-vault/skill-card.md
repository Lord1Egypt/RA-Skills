## Description: <br>
Organizes a Markdown vault by proposing semantic topic folders, moving notes after user confirmation, and creating or updating MOC.md index files without changing note content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanli6](https://clawhub.ai/user/wanli6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to initialize or maintain a git-tracked Markdown knowledge vault by grouping notes into topic folders and maintaining MOC.md indexes. It is intended for vault organization workflows where the user reviews proposed file moves and index updates before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move Markdown notes and create or update MOC.md files in a selected vault. <br>
Mitigation: Start from a clean git state with a recent commit or backup, review the full proposed change list, and confirm only intended file moves and index updates. <br>
Risk: Semantic grouping may place ambiguous notes in an unexpected topic or in misc/. <br>
Mitigation: Review low-confidence classifications and misc/ assignments before approval, and adjust directory choices during the preview step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanli6/organize-vault) <br>
- [Publisher profile](https://clawhub.ai/user/wanli6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command snippets, proposed file-operation previews, and MOC.md index entries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-selected git-tracked Markdown vault and explicit confirmation before moving notes or writing MOC.md files.] <br>

## Skill Version(s): <br>
1.1.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
