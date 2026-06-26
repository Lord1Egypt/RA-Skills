## Description: <br>
LLM-Wiki-skills helps an agent initialize, ingest, query, lint, and maintain a persistent local wiki knowledge base with cross-references, citations, and operation logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1knownothing](https://clawhub.ai/user/1knownothing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill set to turn collected articles, notes, papers, and team materials into an LLM-maintained wiki that can be queried, updated, and checked over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally reads and updates persistent local wiki files, so using a broad workspace could expose unrelated sensitive files to the agent. <br>
Mitigation: Use a dedicated wiki and raw-source folder, and avoid pointing the agent at unrelated private directories. <br>
Risk: Ingest, lint, query filing, and schema maintenance can create or modify multiple wiki pages and logs. <br>
Mitigation: Ask the agent to show planned file changes before applying updates, especially before ingesting sources or filing generated answers back into the wiki. <br>
Risk: Generated summaries, citations, contradictions, and syntheses can contain mistakes or preserve stale claims. <br>
Mitigation: Review generated wiki updates against the original source files before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1knownothing/llm-wiki-skills) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Obsidian cloud sync guide](https://www.bilibili.com/video/BV1fZCyBYEuT/?spm_id_from=333.788.top_right_bar_window_history.content.click&vd_source=2c231d5b43d9ccf0848317adb47c0383) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown files, conversational guidance, wiki citations, and optional tables, Marp slide decks, charts, or wiki pages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can read and update local wiki files, index files, schema files, and logs when the agent is given file-system tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
