## Description:

JSON Param Parser helps agents inspect JSON input and report matching field paths and values for a requested parameter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmfeng6](https://clawhub.ai/user/mmfeng6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers can use this skill to locate JSON fields in pasted logs, files, or piped input and get a concise terminal report of matching paths and values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence notes that documentation overstates some formatted JSON, SQL extraction, and enum-summary behavior.

Mitigation: Treat the reliable output as local JSON field lookup results, and verify any SQL extraction guidance or summarized values before using them in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mmfeng6/skills/json-param-parser)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text report with JSON paths, matched values, and similar-key suggestions when no exact match is found]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper runs locally and reads JSON content supplied as an argument, file, or standard input.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
