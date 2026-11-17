## Description:

JSON解析器 helps agents parse and validate JSON from construction APIs, IoT sensors, and BIM exports, then flatten or convert the results into tabular outputs for analysis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and automation teams use this skill to inspect JSON payloads from construction APIs, IoT sensor batches, and BIM exports, validate structure, flatten nested data, and prepare tables or report-ready summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for command execution and file writes without clearly documenting allowed commands or boundaries.

Mitigation: Run it in a constrained workspace and require explicit review before any shell command or file write is performed.

Risk: The skill references an API key requirement without explaining why the key is needed.

Mitigation: Do not provide secrets or broad project access unless the need is confirmed, and prefer scoped or temporary credentials when credentials are required.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/json-parse-engine)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with code snippets, shell commands, and structured JSON or table-processing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file reads, file writes, and command execution; review generated commands and outputs before applying them to sensitive data.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
