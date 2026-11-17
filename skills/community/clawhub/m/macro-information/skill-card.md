## Description:

Macro-Information queries macroeconomic news and public sentiment data across domestic and international topics, with filtering by sentiment, event tags, heat, and time range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agent operators use this skill to search recent macroeconomic news about topics such as GDP, CPI, central bank policy, trade, inflation, and financial markets. It supports domestic or international macro filters, sentiment filters, event tags, heat metrics, and time windows for macroeconomic monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through chat, local files, shell history, or printed environment/configuration contents.

Mitigation: Use a scoped environment variable or secret store, do not paste API keys into chat, avoid --api-key in shell commands, and do not ask the agent to print .env or config files.

Risk: The skill sends requests to the FEEDAX endpoint and depends on trust in that service.

Mitigation: Review the endpoint and release before installing, and use the skill only when the FEEDAX service is trusted for the intended workflow.

Risk: Default behavior can write timestamped CSV and Markdown result files containing query results.

Mitigation: Use --no-output when local result files are not wanted, and choose an appropriate output directory when files are required.

## Reference(s):

- [ClawHub Macro-Information Skill Page](https://clawhub.ai/longgggggg/skills/macro-information)
- [FEEDAX](https://www.feedax.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Terminal text with optional CSV and Markdown result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can suppress local output files with --no-output; default file outputs are timestamped macro_information CSV and Markdown files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
