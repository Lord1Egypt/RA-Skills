## Description: <br>
Build and maintain a compiled LLM Wiki inside an Obsidian vault following Karpathy's pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerome-benoit](https://clawhub.ai/user/jerome-benoit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to maintain a compiled wiki in an Obsidian vault: ingesting raw sources, generating interlinked Markdown pages, building indexes, linting wiki health, and answering from already compiled wiki content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad local file access within the resolved Obsidian vault and can create or update wiki content. <br>
Mitigation: Review the resolved vault path before approving writes, keep backups or Git history for the vault, and inspect resulting changes. <br>
Risk: --fix workflows and AGENTS.md updates can change local wiki content and future agent behavior within the vault. <br>
Mitigation: Approve fix workflows only for intended vaults, review AGENTS.md changes before accepting them, and use version control to revert unintended edits. <br>


## Reference(s): <br>
- [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [Agents template](references/agents-template.md) <br>
- [Wiki schema template](references/schema-template.md) <br>
- [Tag taxonomy template](references/taxonomy-template.md) <br>
- [ClawHub release page](https://clawhub.ai/jerome-benoit/obsidian-wiki) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local wiki files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates Obsidian vault content under raw/, wiki/, _meta/, .wiki-meta/, and AGENTS.md according to the selected workflow.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
