## Description: <br>
Complete Memory System - Unified integration of all memory features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[717986230](https://clawhub.ai/user/717986230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local persistent memory system with SQLite-backed structured memory, optional vector retrieval, emotion analysis, Theory of Mind utilities, and memory diary workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist memory locally, which can retain private conversations, secrets, or regulated data if users store them. <br>
Mitigation: Use a reviewed database path, avoid storing passwords or regulated data, and define cleanup or deletion procedures before relying on the memory store. <br>
Risk: Optional embedding support sends text to the configured local Ollama endpoint. <br>
Mitigation: Enable Ollama only when the local endpoint and model are trusted, and review what memory text is embedded. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/717986230/memory-complete) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and uses a local SQLite memory database by default; optional Ollama embedding support can call a local Ollama endpoint.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
