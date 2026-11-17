## Description:

Quickly extract and filter JSON fields using simple path expressions with optional output as raw text, JSON, or tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query JSON files, API responses, configuration data, and JSON Lines-style logs with simpler path expressions than jq. It helps agents propose local CLI commands and concise guidance for extracting nested fields, array items, wildcard matches, and table-formatted results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python CLI reads JSON files explicitly provided by the user, so users may expose sensitive local data if they point it at confidential files.

Mitigation: Run it only on intended local JSON inputs and avoid using confidential files unless the environment and output handling are approved.

Risk: The security guidance notes packaging friction because documented command names do not fully match the shipped files, and the documentation is primarily Chinese.

Mitigation: Review or translate the documentation before use and confirm the installed command path in a local test environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/json-query-tool-kay)
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce raw text, pretty or compact JSON, or simple table output when describing CLI use.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
