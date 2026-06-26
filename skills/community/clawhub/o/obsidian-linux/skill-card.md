## Description: <br>
Work with Obsidian vaults, which are local folders of plain Markdown notes, and automate common note workflows with notesmd-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TriplEight](https://clawhub.ai/user/TriplEight) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and knowledge workers use this skill to inspect, search, create, append, move, and delete Markdown notes in local Obsidian vaults through notesmd-cli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify local Obsidian vault notes, including append, overwrite, move, and delete operations. <br>
Mitigation: Confirm the selected vault, note path, and operation mode before running commands, especially before overwrite, move, or delete operations. <br>
Risk: Vault contents may be exposed in the agent session when notes are searched or printed. <br>
Mitigation: Avoid using the skill on vaults that contain information you do not want exposed to the active agent session. <br>


## Reference(s): <br>
- [Obsidian Help](https://help.obsidian.md) <br>
- [ClawHub skill page](https://clawhub.ai/TriplEight/obsidian-linux) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires notesmd-cli and access to the selected local Obsidian vault; creating notes through the CLI requires Obsidian and its URI handler.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
