## Description:

JSON formatting, validation, and conversion tool. Format, compress, validate JSON, and convert between JSON and YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeter226](https://clawhub.ai/user/freeter226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to format, compress, validate, and convert JSON and YAML while debugging API responses, checking configuration files, or preparing structured data for other tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --file option reads a local path supplied by the user.

Mitigation: Use --file only with files intentionally selected for formatting, validation, or conversion.

Risk: YAML conversion depends on the installed PyYAML package version.

Mitigation: Install the skill in a virtual environment and pin PyYAML to a reviewed version when reproducible builds matter.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-formatted command results from the bundled Python utility]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and PyYAML for YAML conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
