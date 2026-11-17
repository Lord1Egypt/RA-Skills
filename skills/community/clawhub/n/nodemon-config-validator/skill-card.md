## Description:

Validate nodemon config files (nodemon.json, .nodemonrc, package.json#nodemonConfig) for watch settings, ignore patterns, exec conflicts, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate Node.js nodemon configuration files, audit watch and ignore behavior, identify exec/script conflicts, and produce CI-friendly findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validator findings can flag exec command shell-injection patterns or configuration conflicts that require project-specific judgment.

Mitigation: Review the reported findings before changing nodemon configuration, especially warnings involving exec commands, broad watch paths, or conflicting config files.

Risk: The skill runs a local Python script against user-supplied nodemon-related config files.

Mitigation: Run it in the intended project workspace and inspect text, JSON, or summary output before using results in CI gates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/nodemon-config-validator)
- [ClawHub publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plus validator output in text, JSON, or summary formats.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes distinguish clean runs, validation errors, and invalid input.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
