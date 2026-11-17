## Description:

Checks JSON files in a workspace for syntax errors and reports invalid files with parse-error details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to check workspace JSON syntax, identify invalid JSON files, and receive a concise report of parse errors. It is not positioned for tasks that require human judgment beyond syntax validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags broader authority than the local JSON-linting purpose explains, including possible exec and write permissions.

Mitigation: Run the skill only in trusted workspaces, review proposed commands before execution, and prefer read-only local linting when write access is unnecessary.

Risk: The security guidance notes an API key requirement that is not explained by the local validation task.

Mitigation: Avoid providing API keys unless a reviewer confirms they are required; prefer revising the skill to remove unnecessary API-key, network, and write-access language.

Risk: The artifact describes syntax validation, not schema validation or semantic configuration review.

Mitigation: Use schema-specific validation or manual review for configuration correctness after JSON syntax passes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/json-lint)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON report with optional Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scanned file counts, valid and invalid file counts, and parse-error details for invalid JSON files.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter states 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
