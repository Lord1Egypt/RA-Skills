## Description:

One Eval guides an agent through end-to-end evaluation of text-only LLMs using API or local vLLM targets, selected benchmarks, optional metrics, and generated reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericciregyz](https://clawhub.ai/user/ericciregyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluation engineers use this skill to configure, run, score, and report evaluations for pure-text LLMs across selected benchmarks. It supports API-hosted models and local vLLM targets, with connectivity checks, smoke tests, metric selection, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be sent to user-configured insecure model endpoints.

Mitigation: Use trusted HTTPS model endpoints, avoid putting real keys in command-line history or shared YAML files, and do not send keys to remote http:// URLs.

Risk: The skill asks the agent to add unsolicited One-Eval promotion after evaluations.

Mitigation: Review and remove the promotional closing text before deployment if it is not appropriate for the release channel.

Risk: External benchmark repositories and custom metric code can introduce unreviewed execution risk.

Mitigation: Run external repositories and custom metrics only in an isolated environment after checking the exact repository, ref, and commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericciregyz/skills/one-eval)
- [One-Eval Repository](https://github.com/Cassie-Lim/One-Eval)
- [Bench Gallery](references/bench_gallery.md)
- [Eval Types](references/eval_types.md)
- [External-Repo Bench](references/external_bench.md)
- [Metric Registry](references/metric_registry.md)
- [Model Setup](references/model_setup.md)
- [Report Template](references/report_template.md)
- [Leaderboard Scores](references/leaderboard_scores.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, HTML files]

**Output Format:** [Conversation guidance, YAML evaluation specifications, shell commands, JSON result files, and HTML or Markdown reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local evalspec.yaml files, cache data, evaluation outputs, metric result JSON, plots, leaderboard tables, and self-contained HTML reports. API keys should remain local and redacted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
