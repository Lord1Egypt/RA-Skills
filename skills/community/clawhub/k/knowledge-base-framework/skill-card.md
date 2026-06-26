## Description: <br>
KB Framework builds a local hybrid knowledge base with Markdown, PDF, OCR, SQLite, ChromaDB, Obsidian, and optional local LLM support for source-traceable agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minenclown](https://clawhub.ai/user/minenclown) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use KB Framework to index local Markdown, PDFs, OCR output, and Obsidian vaults, then provide agents with source-location pointers, hybrid search, audits, and optional local LLM summaries or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad local file, database, watcher, scheduler, cleanup, and update authority. <br>
Mitigation: Use it in a dedicated environment, keep watched and indexed directories narrow, and avoid the built-in updater unless the release source is trusted. <br>
Risk: Write, delete, watcher, scheduler, or cleanup commands can affect Obsidian vaults and KB databases. <br>
Mitigation: Back up Obsidian vaults and KB databases before enabling those commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minenclown/knowledge-base-framework) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [HOW_TO_KB.md](artifact/HOW_TO_KB.md) <br>
- [SECURITY_FUNCTIONS.txt](artifact/SECURITY_FUNCTIONS.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local file paths, database operation guidance, search commands, and LLM engine configuration.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, artifact SKILL.md, artifact CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
