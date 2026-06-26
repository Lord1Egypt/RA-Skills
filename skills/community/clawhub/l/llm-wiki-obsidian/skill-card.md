## Description: <br>
Use when the user is working inside an Obsidian or markdown vault and wants to ingest sources, query accumulated knowledge, or maintain a Karpathy-style LLM wiki. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javastarboy](https://clawhub.ai/user/javastarboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers working in Obsidian or markdown vaults use this skill to have an agent ingest sources, query accumulated knowledge, and maintain an evolving LLM wiki with interlinked markdown pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local wiki edits can unintentionally alter many pages in a markdown or Obsidian vault. <br>
Mitigation: Use the skill on a specific vault or directory, keep version control or backups, and request a proposed change list before large ingest, lint, or wiki-wide update operations. <br>
Risk: Optional external tools, plugins, or links may introduce separate trust or data handling considerations. <br>
Mitigation: Treat optional external tools, Obsidian plugins, and links as separate opt-in decisions and review them before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/javastarboy/llm-wiki-obsidian) <br>
- [qmd markdown search engine](https://github.com/tobi/qmd) <br>
- [Tolkien Gateway example wiki](https://tolkiengateway.net/wiki/Main_Page) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance, with optional code or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or modify local markdown wiki files when the user approves a scoped vault workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
