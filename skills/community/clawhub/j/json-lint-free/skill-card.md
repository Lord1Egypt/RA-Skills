## Description:

Validates JSON files in a workspace and reports syntax errors with file-level details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to check workspace JSON files for syntax errors, especially configuration files that need quick validation and clear error reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags broader execution, write, and API key use than the stated local JSON syntax-checking purpose explains.

Mitigation: Review before installing, use only in a trusted workspace, and approve only explicit files and commands needed for JSON validation.

Risk: The artifact asks for an API key even though local JSON validation should not normally require one.

Mitigation: Do not provide an API key unless the publisher clearly explains why it is required and what data is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-lint-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON report with optional explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scanned file counts, valid and invalid file counts, and per-file parse errors.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
