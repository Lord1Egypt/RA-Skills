## Description: <br>
Manages an Obsidian-backed LLM Wiki knowledge base by initializing projects, ingesting source material into Markdown wiki pages, answering wiki-based queries, and running wiki health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to create and maintain persistent Obsidian wiki projects from articles, notes, papers, meetings, and other source material. It supports project setup, source ingestion, wiki-based question answering, and lint-style health checks while preserving raw source files as the reference record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read source files and update wiki pages in an Obsidian vault. <br>
Mitigation: Use a dedicated wiki folder, review planned writes before ingestion, and keep raw source files read-only. <br>
Risk: Wiki pages may contain incorrect synthesis or unresolved contradictions from source material. <br>
Mitigation: Review ingestion summaries, preserve source citations, and keep contradictions explicitly marked rather than silently merged. <br>
Risk: The skill depends on the separate /obsidian integration for file operations. <br>
Mitigation: Install and trust the /obsidian integration before use, and confirm vault paths before allowing writes. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Ingest Logic Reference](references/ingest-logic.md) <br>
- [Scenario Templates Reference](references/templates.md) <br>
- [Andrej Karpathy LLM Wiki Concept](https://x.com/karpathy/status/1793562750870294638) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Markdown wiki file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update multiple wiki pages and append operation logs through the required Obsidian integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
