## Description:

Use this skill when the user wants to monitor LLM behavior over time and get alerted when outputs change unexpectedly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swanand33](https://clawhub.ai/user/swanand33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up scheduled behavioral regression checks for LLM applications, capture baseline outputs, detect drift, and configure alerts when monitored prompts change unexpectedly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted test names may cause baseline cleanup to delete JSON files outside the intended baseline folder.

Mitigation: Use only trusted test_suite.yaml files, keep test names simple, run the skill with a low-privilege account, and execute it in a dedicated virtual environment or container.

Risk: Prompts, system prompts, outputs, and alert text may be sent to configured model providers and alert channels.

Mitigation: Do not include secrets, regulated data, or sensitive production prompts unless sharing that data with the selected provider and alert destinations is acceptable.

Risk: Unpinned dependencies, webhooks, email settings, and scheduled runs can change runtime behavior or expose alert data.

Mitigation: Pin dependencies before production use and review webhook URLs, email configuration, and scheduled command settings before enabling monitoring.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/swanand33/skills/llm-regression-monitor)
- [Provider Setup Guide](references/providers.md)
- [test_suite.yaml Field Reference](references/test-suite-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides creation of test_suite.yaml, baseline files, monitor_report.json, monitor_trend.jsonl, trend_warnings.json, and alert configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
