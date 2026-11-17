## Description:

Lint and validate GitLab CI/CD pipeline YAML files for syntax errors, security issues, deprecated patterns, and best-practice violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint, validate, audit, and inspect GitLab CI/CD pipeline YAML before committing or publishing pipeline changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linter reads user-selected YAML files and can recursively scan directories when pointed at a directory path.

Mitigation: Run it only against intended project paths and avoid broad private directories unless that scope is necessary.

Risk: Lint results may be incomplete because this is a local helper rather than GitLab's authoritative CI linting service.

Mitigation: Confirm important pipeline and security decisions with GitLab's own CI linting or a full YAML parser-aware review.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON reports and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include rule severity, rule identifier, line number, message, and summary counts where supported.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
