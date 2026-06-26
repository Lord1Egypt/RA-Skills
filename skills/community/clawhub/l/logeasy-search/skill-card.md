## Description: <br>
Searches and analyzes LogEase log data for security alerts, network device logs, system logs, aggregation summaries, trend signals, and anomaly investigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x1nq](https://clawhub.ai/user/x1nq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security analysts, and operations teams use this skill to query recent LogEase logs, inspect security and infrastructure events, and generate concise investigation summaries from returned log data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes administrator credentials and can return sensitive log data. <br>
Mitigation: Remove and rotate the published administrator password before use, store runtime credentials outside the skill, and grant only least-privilege access needed for log search. <br>
Risk: The bundled MCP code includes broader platform-control capabilities than a search-only workflow requires. <br>
Mitigation: Deploy only the read-only LogEase search surface by default, and require explicit administrator approval before enabling mutating or general platform API tools. <br>
Risk: Some HTTP clients and examples use internal endpoints or weakened TLS assumptions. <br>
Mitigation: Install only in an authorized internal environment, enforce HTTPS with certificate validation, and treat all returned logs as sensitive operational data. <br>


## Reference(s): <br>
- [LogEase Search ClawHub listing](https://clawhub.ai/x1nq/logeasy-search) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Rizhiyi MCP README](artifact/rizhiyi-mcp/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with shell commands, Python snippets, JSON responses, and concise log-analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Log search output is constrained by the LogEase API response behavior described in the artifact, including relative time ranges and a typical maximum of 100 returned raw rows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
