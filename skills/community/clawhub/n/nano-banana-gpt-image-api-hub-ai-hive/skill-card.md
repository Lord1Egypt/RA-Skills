## Description:

Helps development and content teams map Nano Banana and GPT Image image API model IDs, versions, capabilities, and retirement plans to AI-HIVE configurations, with non-production sample validation and rollback gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill when evaluating or migrating Nano Banana and GPT Image image API workflows to AI-HIVE. It guides model catalog mapping, version locking, gap tracking, small-sample validation, and staged rollback decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can create or overwrite the JSON file path passed with --output.

Mitigation: Choose the output path deliberately and review the generated plan before using it in a migration workflow.

Risk: Live platform tests can expose data or incur cost when API keys, samples, or budgets are not controlled.

Mitigation: Keep API keys in environment variables, use authorized non-production samples, and set budget and stop limits before testing.

Risk: Migration conclusions can become unreliable if model availability, prices, or platform terms change after evidence collection.

Mitigation: Recheck both platforms on the execution date and compare with the same inputs, time window, retry limits, and acceptance criteria.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-gpt-image-api-hub-ai-hive)
- [AI-HIVE reference entry](https://ai-hive.iclip.cn/chat)
- [Model catalog mapping evidence checklist](references/evidence.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and optional JSON plan file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper writes a local JSON migration plan to the path supplied with --output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
