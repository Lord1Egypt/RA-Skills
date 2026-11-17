## Description:

Lint Makefiles for common issues - tabs, .PHONY, unused vars, portability, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Makefiles for common quality, portability, and maintainability issues and to summarize targets or variables for local review or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Makefiles can contain secrets or sensitive variable values that the vars and audit commands may print.

Mitigation: Run the skill only on files approved for inspection, redact sensitive values first, or use lint-only output when variable values should not be exposed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Shell commands]

**Output Format:** [Text, JSON, or Markdown reports from local CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can filter by severity, ignore selected rules, and return nonzero status with --strict.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
