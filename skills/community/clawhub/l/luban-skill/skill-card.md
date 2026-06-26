## Description: <br>
Helps agents inspect and edit Luban game configuration tables, including enums, Beans, table schemas, fields, rows, imports, exports, validation, and type guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caixukunmax](https://clawhub.ai/user/caixukunmax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical designers, and game teams use this skill to let an agent query, validate, and modify Luban-backed Excel game configuration data without loading whole workbooks into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad writes, updates, deletes, imports, batch operations, and file changes inside the selected Luban data directory. <br>
Mitigation: Keep --data-dir limited to the intended project, require explicit operation previews before writes or deletes, validate after changes, and avoid --force unless backups exist. <br>
Risk: The Luban generation command accepts --luban-cmd and is shell-backed. <br>
Mitigation: Do not pass untrusted or natural-language-derived input to --luban-cmd; use a reviewed, fixed command path for generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caixukunmax/luban-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [REFERENCE.md](references/REFERENCE.md) <br>
- [commands.md](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured operation previews] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate on a user-supplied Luban data directory and may read or mutate Excel and configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact metadata reports 3.8.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
