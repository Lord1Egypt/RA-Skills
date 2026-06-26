## Description: <br>
Obsidian笔记助手 helps agents create, search, organize, tag, link, and export graph data from local Obsidian Markdown vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage local Obsidian knowledge bases, including creating daily notes, searching notes, auditing tags, checking backlinks, and exporting graph data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify files in a local Obsidian vault. <br>
Mitigation: Confirm the vault path and target filenames, preview generated note content before write actions, and keep normal backups for important notes. <br>
Risk: Search and graph export workflows can surface private note content or relationships in agent output files. <br>
Mitigation: Limit searches and exports to the intended vault scope, review generated output before sharing, and avoid running it on sensitive vaults unless disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/laosi-obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify Markdown note files and JSON graph exports in a configured local Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
