## Description: <br>
A lightweight Notion command-line skill for personal developers and knowledge workers to query databases, manage pages and blocks, maintain aliases, and export workspace data from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to operate a single Notion workspace from the terminal for task management, project tracking, comments, page updates, and CSV/JSON/YAML exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update, archive, delete, comment on, and export Notion content. <br>
Mitigation: Use a least-privilege Notion integration shared only with needed databases and require explicit confirmation before updates, archives, deletions, alias changes, comments, or exports. <br>
Risk: The skill depends on an external CLI package installed with npm. <br>
Mitigation: Verify the CLI package source before installation and pin or review package updates in managed environments. <br>
Risk: Broad activation guidance could let an agent operate Notion when the user did not intend workspace changes. <br>
Mitigation: Activate the skill only for intentional Notion workspace operations and confirm write or export actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/notion-cli-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI operations may return tables, CSV, JSON, YAML, status codes, results, and logs depending on command options.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
