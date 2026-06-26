## Description: <br>
Knowledge Orchestrator coordinates Zotero, Obsidian, and IMA knowledge-management workflows through a backward-compatible entry point that now forwards users toward the unified `knowledge` skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to search and coordinate personal research material across Zotero, Obsidian, and IMA, while preserving compatibility with older Knowledge Orchestrator commands. It is most relevant for literature search, note lookup, and migration toward the unified `knowledge search/sync/link` workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Zotero library metadata, Obsidian notes, and IMA credentials. <br>
Mitigation: Install only when the publisher is trusted, use least-privilege API keys where possible, and keep credential files private with restrictive filesystem permissions. <br>
Risk: Sync or upload actions may move notes or research material to IMA cloud services. <br>
Mitigation: Prefer the unified `knowledge ...` commands and confirm before any sync or upload action. <br>


## Reference(s): <br>
- [Knowledge Orchestrator ClawHub page](https://clawhub.ai/jirboy/knowledge-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/jirboy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and optional JSON search results from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include Zotero metadata, Obsidian note matches, and IMA status text depending on configured services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
