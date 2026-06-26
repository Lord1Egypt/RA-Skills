## Description: <br>
Build and maintain a self-compiling Obsidian markdown wiki where an agent ingests raw sources, compiles cross-linked pages, answers grounded queries, lints graph health, and processes human feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliahzhu](https://clawhub.ai/user/juliahzhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and teams use this skill to create and maintain a local markdown knowledge base from source material, then query, lint, and audit that wiki over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs an agent to edit and reorganize local markdown wiki files. <br>
Mitigation: Use git or backups before large ingest, compile, lint, or audit runs, and review proposed merges, splits, and moves before relying on them. <br>
Risk: Raw sources, audit comments, logs, or generated outputs may expose sensitive information if users place secrets in the wiki. <br>
Mitigation: Avoid storing secrets in raw sources, audit files, logs, or generated outputs, and review content before sharing the wiki. <br>
Risk: Generated HTML or JavaScript associated with wiki viewing may be unsafe if opened or embedded without review. <br>
Mitigation: Review generated HTML and JavaScript before opening it in a browser or embedding it elsewhere. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juliahzhu/llm-wiki-q) <br>
- [Karpathy llm-wiki Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) <br>
- [Obsidian](https://obsidian.md) <br>
- [qmd](https://github.com/tobi/qmd) <br>
- [Article guide](references/article-guide.md) <br>
- [Audit guide](references/audit-guide.md) <br>
- [Log guide](references/log-guide.md) <br>
- [Schema guide](references/schema-guide.md) <br>
- [Tooling tips](references/tooling-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, wiki updates, shell commands, and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local wiki, log, audit, raw source, and query output files.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
