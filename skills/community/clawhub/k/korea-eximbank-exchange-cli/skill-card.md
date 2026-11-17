## Description:

Guides agents in using the Korea Eximbank OpenAPI exchange-rate CLI to query AP01, AP02, and AP12 tables with date, currency, JSON, and CSV options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install and run a CLI that queries Korea Eximbank exchange-rate data for a chosen date, table, output format, and optional currency filter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI requires a Korea Eximbank API key.

Mitigation: Use only a key intended for this tool and avoid sharing it in prompts, logs, or committed configuration.

Risk: Exchange-rate results may be empty on non-business days or affected by API limits.

Mitigation: Check the API response message and retry with an applicable business date or narrower query when results are missing.

Risk: Users who do not read Korean may miss important API or output details.

Mitigation: Review translated API documentation and command output before relying on results in workflows.

## Reference(s):

- [Korea Eximbank exchangeJSON API](https://www.koreaexim.go.kr/site/program/financial/exchangeJSON)
- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/korea-eximbank-exchange-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided KOREAEXIM_API_KEY environment variable.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
