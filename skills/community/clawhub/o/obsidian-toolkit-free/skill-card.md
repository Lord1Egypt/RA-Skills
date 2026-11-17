## Description: <br>
Guides an agent through Obsidian vault discovery, note management, basic templates, and plugin setup using obsidian-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Obsidian users and developers use this skill to let an agent find active vaults, search and reorganize notes, create template-based notes, and configure core Obsidian workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to create, move, rename, or delete local Obsidian notes through command-line tools. <br>
Mitigation: Ask for a preview and explicit confirmation before deletes or bulk reorganization, and keep backups or sync history enabled. <br>
Risk: Obsidian files are local, but selected prompts or note contents may still be processed by the configured agent or LLM service. <br>
Mitigation: Avoid sending sensitive note contents unless the agent platform and model routing are approved for that data. <br>


## Reference(s): <br>
- [ClawHub release: Obsidian Toolkit Free](https://clawhub.ai/thcjp/skills/obsidian-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file operations against an Obsidian vault through obsidian-cli.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
