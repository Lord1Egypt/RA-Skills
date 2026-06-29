## Description: <br>
Implements structured usage logging and audit trails for cost and session tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add structured JSONL usage logs, session grouping, audit trails, token and cost summaries, and debugging queries to agent or plugin workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local usage logs may retain sensitive metadata, token counts, cost details, error messages, or session history. <br>
Mitigation: Before using the skill on sensitive projects, confirm log storage location, retained fields, redaction behavior, retention policy, and deletion or disablement process. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-leyline-usage-logging) <br>
- [Leyline Source Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [Session Patterns](modules/session-patterns.md) <br>
- [Log Formats](modules/log-formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, Python, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes JSONL schemas, session management patterns, query commands, and integration snippets.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
