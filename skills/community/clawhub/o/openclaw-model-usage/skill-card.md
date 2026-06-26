## Description: <br>
Inspect local OpenClaw model usage directly from session logs, including recent model use, token totals, cost summaries, per-agent usage, and daily summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranasalalali](https://clawhub.ai/user/ranasalalali) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local OpenClaw session logs, identify the current or recent model in use, and summarize usage by model, agent, session, day, tokens, and cost. It can return a compact text summary, JSON for automation, or a local HTML dashboard for richer inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated usage summaries and dashboard HTML can expose sensitive local model, token, cost, agent, session, or activity details if shared. <br>
Mitigation: Review and redact summaries or dashboard files before publishing, attaching, or sending them outside the local environment. <br>
Risk: Reports can be misleading when run against fixture or test roots instead of real OpenClaw logs. <br>
Mitigation: Use ~/.openclaw/agents for normal reporting and reserve fixture paths for development or smoke testing. <br>


## Reference(s): <br>
- [OpenClaw model usage discovery](references/discovery.md) <br>
- [OpenClaw Model Usage on ClawHub](https://clawhub.ai/ranasalalali/openclaw-model-usage) <br>
- [Publisher profile](https://clawhub.ai/user/ranasalalali) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown summaries with optional JSON output, shell commands, and generated local HTML dashboard files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw logs under ~/.openclaw/agents by default; dashboard reports are self-contained HTML and may contain sensitive local usage details.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
