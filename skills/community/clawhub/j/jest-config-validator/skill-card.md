## Description:

Validate jest.config.ts/js/json and Jest configuration in package.json for deprecated options, transform conflicts, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and DevOps engineers use this skill to audit Jest configuration files, catch deprecated options and transform conflicts, and produce CI-friendly validation output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator reads the config path supplied by the user and may inspect same-directory Jest or package configuration files.

Mitigation: Run it only against intended project directories and review reported findings before making configuration changes.

Risk: Static lint-style findings may be incomplete or conservative for complex JavaScript or TypeScript configuration patterns.

Mitigation: Treat results as review guidance and confirm important changes with the project test suite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/jest-config-validator)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Markdown guidance with optional shell commands and validator output in text, JSON, or summary form]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CI-friendly exit codes: 0 for no errors, 1 for validation errors, and 2 for missing file or parse errors.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
