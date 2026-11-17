## Description:

Tracks public AI model benchmark and cost-efficiency data to help agents recommend models for coding, writing, analysis, translation, math, creative, and simple tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notestone](https://clawhub.ai/user/notestone)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to compare model capabilities and cost efficiency, then generate model recommendations, reports, exported JSON, and routing configuration commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-routing or configuration examples can change which models OpenClaw uses for future tasks.

Mitigation: Review generated recommendations and configuration commands before applying them, especially in shared or production OpenClaw workspaces.

Risk: Cron, dashboard, and compute-router workflows can write local files or update another skill's configuration.

Mitigation: Run automation first in a test workspace and verify target paths before enabling scheduled jobs or sync commands.

Risk: Slack alert examples can share model cost or usage information with a configured webhook destination.

Mitigation: Use only approved webhook destinations and remove sensitive spend details before enabling alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/notestone/skills/model-benchmarks)
- [LMSYS Chatbot Arena](https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard)
- [Open LLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- [BigCode Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-leaderboard)
- [Alpaca Eval](https://tatsu-lab.github.io/alpaca_eval/)
- [Integration examples](examples/integration-examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance, CLI text output, JSON exports, Python snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write benchmark cache files, CSV or JSON exports, dashboards, and model-routing configuration when users run the relevant commands or examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
