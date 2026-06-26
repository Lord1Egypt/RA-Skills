## Description: <br>
Supermemory gives AI agents long-term memory by extracting atomic facts from conversations, tracking how knowledge changes over time, and enabling semantic recall across sessions and agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jared-goering](https://clawhub.ai/user/jared-goering) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent, searchable memory to agent workflows. It helps agents recall relevant facts, inspect entity history, and reuse context across sessions and agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory can retain sensitive or regulated conversation facts across sessions. <br>
Mitigation: Define what may be ingested before enabling the skill, avoid secrets or regulated data unless approved, and confirm how stored memories can be inspected, deleted, or separated. <br>
Risk: Fact extraction may send ingested text to an external LLM provider. <br>
Mitigation: Use a controlled LLM API key, review provider and retention requirements, and restrict ingestion to text approved for external processing. <br>
Risk: Automatic memory injection and extraction can reuse stale, incorrect, or unintended context. <br>
Mitigation: Review recalled memories before relying on them for high-impact decisions and use session or agent boundaries where separation matters. <br>
Risk: The local API may expose stored memories if it is reachable outside the intended environment. <br>
Mitigation: Keep the local API private, bind it only to trusted interfaces, and limit access to the memory database and service port. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jared-goering/openclaw-supermemory) <br>
- [PyPI Package](https://pypi.org/project/openclaw-supermemory/) <br>
- [GitHub Repository](https://github.com/jared-goering/openclaw-supermemory) <br>
- [OpenClaw Plugin](https://github.com/jared-goering/openclaw-supermemory/tree/main/plugin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a local Supermemory service and an LLM API key for fact extraction.] <br>

## Skill Version(s): <br>
0.2.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
