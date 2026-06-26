## Description: <br>
JSON formatting, validation, and conversion tool. Format, compress, validate JSON, and convert between JSON and YAML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeter226](https://clawhub.ai/user/freeter226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to format, minify, validate, and convert JSON and YAML while debugging API responses, checking configuration files, or preparing data for other tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can read local files when invoked with --file. <br>
Mitigation: Use --file only for files intended to be processed and printed by the formatter. <br>
Risk: YAML conversion depends on PyYAML. <br>
Mitigation: Install a reviewed, pinned PyYAML version before using YAML conversion commands. <br>


## Reference(s): <br>
- [JSON Wizard on ClawHub](https://clawhub.ai/freeter226/json-wizard) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON strings and concise command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces formatted, compressed, validation, or conversion results from user-provided JSON/YAML input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
