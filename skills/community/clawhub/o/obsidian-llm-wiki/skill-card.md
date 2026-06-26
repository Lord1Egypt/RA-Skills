## Description: <br>
obsidian-llm-wiki helps agents build and maintain a local Obsidian knowledge base from supplied materials, organizing extracted knowledge into linked Markdown wiki pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddiewang-zhhx](https://clawhub.ai/user/eddiewang-zhhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to initialize and maintain Obsidian vaults as structured wiki-style knowledge bases. The skill guides ingestion, querying, health checks, and synthesis workflows for local Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands and overwrite local Obsidian vault files. <br>
Mitigation: Use it with a new or backed-up vault, review the initialization script before execution, and avoid pointing it at a curated vault unless overwrites are acceptable. <br>
Risk: Supplied URLs or local files may be processed by external tools and persisted as Markdown notes. <br>
Mitigation: Review source material and generated notes before retaining or sharing the vault contents. <br>
Risk: Long content passed through obsidian-cli may be truncated. <br>
Mitigation: Use direct file writes for long pages and verify generated files after writing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddiewang-zhhx/obsidian-llm-wiki) <br>
- [obsidian-llm-wiki repository link](https://github.com/clawhub/obsidian-llm-wiki) <br>
- [llm-wiki-skill acknowledgement link](https://github.com/sdyckjq-lab/llm-wiki-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise Markdown guidance with shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Obsidian vault files, templates, indexes, logs, and wiki pages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
