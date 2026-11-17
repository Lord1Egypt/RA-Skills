## Description:

A lightweight JSON syntax checking skill that recursively scans workspace .json files and returns a structured error report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations engineers, data engineers, educators, and CI/CD workflow owners use this skill to scan JSON files, identify syntax errors, and review structured validation results before committing, deploying, or accepting data files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads workspace .json files and may use command execution for parsing.

Mitigation: Run it only on chosen directories and exclude node_modules, .git, dist, and folders that may contain sensitive data.

Risk: The skill text contains broad API, network, conversion, and content-extraction language outside the core JSON linting purpose.

Mitigation: Limit use to local JSON syntax checking and do not treat broader language as permission for unrelated tasks.

Risk: The security verdict is suspicious because the real scope is unclear.

Mitigation: Review the skill before deployment and constrain agent permissions to the minimum needed for reading files and running local JSON parsing commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-lint-tool-free)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON, text, or CSV-style validation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include scan timestamps, file counts, pass rate, and per-file syntax error details.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
