## Description:

JSON query, validate, diff, transform, format, flatten, and stats toolkit with a jq-like interface using Python stdlib only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when an agent needs to inspect, query, validate, compare, transform, format, flatten, or summarize JSON data through a local Python command-line helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads user-specified JSON and schema files and can write output files when requested.

Mitigation: Run it only on files intended for processing and review any output path before execution.

Risk: Schema validation is a limited JSON Schema draft-07 subset and evidence cautions against using it as a security-critical validator.

Mitigation: Use this validator for convenience checks only; use a vetted JSON Schema validator for security-critical enforcement.

Risk: Untrusted schemas with complex regex patterns may create avoidable validation risk.

Mitigation: Avoid running validation against untrusted schemas with complex patterns, or review schemas before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/json-processor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [Markdown guidance with shell commands; command output may be JSON, text summaries, diffs, or formatted JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3.6+ standard library only; optional output files are written only when requested by command arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
