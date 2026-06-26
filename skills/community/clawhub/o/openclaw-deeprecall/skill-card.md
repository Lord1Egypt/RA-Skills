## Description: <br>
Provides persistent two-tier memory with semantic fact search and raw content retrieval, plus automatic cleanup of temporary session files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hallllllll](https://clawhub.ai/user/Hallllllll) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give AI agents persistent, searchable memory across sessions, including structured fact retrieval and optional raw archive lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived raw memory data in a local database, which can retain sensitive or regulated information. <br>
Mitigation: Avoid processing secrets or regulated data, use --no-store-raw for sensitive files, and plan how to inspect, back up, or delete memory.db. <br>
Risk: Memory files can be sent to an auto-selected LLM provider during summarization. <br>
Mitigation: Choose a trusted or local LLM provider before summarization and test configuration before processing memory files. <br>
Risk: Cleanup can remove temporary raw Markdown files while archived database records remain permanent. <br>
Mitigation: Run cleanup with --dry-run first and verify retention settings before deleting temporary files. <br>


## Reference(s): <br>
- [DeepRecall Skill Documentation](artifact/SKILL.md) <br>
- [DeepRecall Configuration Guide](artifact/CONFIG_GUIDE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Hallllllll/openclaw-deeprecall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory search results, raw archive text, cleanup summaries, and LLM-generated structured fact records.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
