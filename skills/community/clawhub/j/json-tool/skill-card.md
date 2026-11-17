## Description:

Validate, format, and transform JSON data. Use when user needs to pretty print JSON, validate JSON syntax, minify JSON, extract JSON paths, or convert JSON to other formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate JSON syntax, pretty print or minify JSON files, sort keys, run simple path queries, and convert JSON data to YAML or CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some operations modify the original JSON file or create converted files unless an output path is supplied.

Mitigation: Use the --output option for important files or keep a backup before running format, minify, sort, or conversion operations.

Risk: The local script reads files supplied by the user.

Mitigation: Run it only on intended JSON inputs in a trusted local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/json-tool)
- [Publisher profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that read JSON files and may overwrite or create output files depending on options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
