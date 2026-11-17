## Description:

Analyzes error logs, extracts structured exception details, classifies errors, derives prevention suggestions, and generates batch summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ractoto](https://clawhub.ai/user/ractoto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to parse stack traces, classify operational failures, inspect recent EvoMap memory logs, and produce concise error-analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The solidify command can send source code, limited platform details, and a bearer token to a configurable remote endpoint.

Mitigation: Use solidify only when publishing is required, verify the destination URL, avoid untrusted A2A_HUB_URL values, and keep A2A_NODE_SECRET or EVOMAP_NODE_SECRET narrowly scoped.

Risk: Evolver mode reads recent .log and .txt files from ~/evolver-memory, which may include sensitive local log content.

Mitigation: Review or redact logs before analysis and avoid evolver mode when only direct log-file analysis is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ractoto/skills/log-analyzer-evomap)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [JSON objects or Markdown/text summaries, with CLI shell commands for local analysis workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary output is capped by maxLogs when requested; evolver mode reads recent .log and .txt files from the local ~/evolver-memory directory.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
