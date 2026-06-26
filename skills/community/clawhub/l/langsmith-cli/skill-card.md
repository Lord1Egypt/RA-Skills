## Description: <br>
Query and analyze LangSmith traces through natural-language questions and structured CLI commands for runs, failures, latency, cost, and prompt comparisons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ralphesber](https://clawhub.ai/user/ralphesber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect LangSmith projects, summarize recent runs, compare traces, and prepare structured trace context for their agent to analyze. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LangSmith traces can contain sensitive prompts, inputs, outputs, errors, or metadata. <br>
Mitigation: Use narrow project, time-window, status, and limit filters, and avoid exposing command output in shared logs, tickets, or transcripts. <br>
Risk: A LangSmith API key could be overexposed if stored persistently or copied into logs. <br>
Mitigation: Use a least-privilege key and prefer session-only environment variables or a secret manager over shell startup files. <br>


## Reference(s): <br>
- [LangSmith API Reference](references/langsmith-api.md) <br>
- [LangSmith API Endpoint](https://api.smith.langchain.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ralphesber/langsmith-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with JSON trace context where applicable] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LANGSMITH_API_KEY and LangSmith project, time-window, status, limit, or run-id command arguments depending on the command.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
