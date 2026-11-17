## Description:

Validate and lint Prettier configuration files (.prettierrc, .prettierrc.json, .prettierrc.yaml, .prettierrc.toml, package.json#prettier) for structure, invalid options, deprecated fields, override conflicts, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate Prettier configuration files, catch invalid or deprecated options, and produce text, JSON, or summary lint results for local review or CI gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator intentionally exits nonzero when it finds errors, which can fail CI jobs.

Mitigation: Review the lint output before using the command as a CI gate and decide which findings should block the workflow.

Risk: JavaScript-based Prettier config files are detected but not statically validated.

Mitigation: Use JSON, YAML, TOML, or package.json#prettier configs for full static validation, or validate JavaScript configs with complementary project tooling.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional text, JSON, or summary validator output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validator exits with code 0 for no errors, 1 for found errors, and 2 for invalid input or unsupported formats.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
