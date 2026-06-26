## Description: <br>
安全優先的通用 Agent 工作框架 | Secure Universal Agent Framework - 自動知識索引、創意建議、關聯系統 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lalawgwg99](https://clawhub.ai/user/lalawgwg99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local workspace knowledge indexing, journal-based suggestion reports, and relationship analysis to an OpenClaw-style agent workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated bundled scripts may rewrite code or affect files outside the advertised indexing workflow. <br>
Mitigation: Review the package before installation and remove or ignore fix.py and fix_final.py unless you explicitly intend to inspect and run them. <br>
Risk: Bundled nested skills include a Telegram reporter that could send private workspace summaries if enabled. <br>
Mitigation: Delete unrelated nested skills you do not intend to use, keep Telegram disabled, or replace the chat ID and review report contents before running daily-observatory-lite. <br>
Risk: Cron-based automation can repeatedly scan local files and generate or transmit reports without interactive review. <br>
Mitigation: Do not enable cron until you have checked which local files are read, which outputs are written, and whether any delivery channel is configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lalawgwg99/nexus-agent-framework) <br>
- [Project homepage](https://github.com/lalawgwg99/nexus-agent-framework) <br>
- [Knowledge index architecture](docs/KNOWLEDGE-INDEX-ARCHITECTURE.md) <br>
- [Idea system usage guide](docs/IDEA-SYSTEM-USAGE.md) <br>
- [Nexus relations specification](docs/NEXUS-RELATIONS.md) <br>
- [Implementation notes](docs/IMPLEMENTATION-NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON or text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local memory index, relationship graph, and idea suggestion files when its scripts are run.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, _meta.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
