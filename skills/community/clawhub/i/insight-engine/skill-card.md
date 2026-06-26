## Description: <br>
Insight Engine collects operational logs, Langfuse traces, Git activity, and control-plane signals, computes statistics in Python, asks an LLM to interpret the structured packet, and writes daily, weekly, or monthly reports to Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn AI system telemetry, evaluation traces, repository activity, and daily memory notes into evidence-backed operational insight reports. It supports scheduled daily, weekly, and monthly reporting, plus dry-run and data-only modes for reviewing the data packet before external API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill can send sensitive local memory and repository context to Anthropic and Notion more broadly than its security notes imply. <br>
Mitigation: Review or disable memory and Git collection before running on private projects, and use --data-only or --dry-run first to inspect what would be sent. <br>
Risk: Operational summaries, Git metadata, and daily OpenClaw memory text may be processed by Anthropic and written to a Notion workspace. <br>
Mitigation: Install only if that data flow is acceptable, use API keys and Notion workspaces you control, and scope configured log, memory, and repository paths to appropriate data. <br>
Risk: Remote telemetry collection can expose data over configured service endpoints. <br>
Mitigation: Prefer HTTPS for any remote Langfuse URL and verify endpoint configuration before live runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/insight-engine) <br>
- [Architecture reference](references/architecture.md) <br>
- [Daily analyst prompt](scripts/prompts/daily_analyst.md) <br>
- [Weekly analyst prompt](scripts/prompts/weekly_analyst.md) <br>
- [Monthly analyst prompt](scripts/prompts/monthly_analyst.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Notion-ready Markdown/plain text reports, JSON data packets in data-only mode, and setup commands or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily, weekly, and monthly modes; dry-run mode uses local Ollama and skips Notion writes; live mode can call Anthropic and write reports to Notion.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
