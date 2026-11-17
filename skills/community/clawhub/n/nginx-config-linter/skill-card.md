## Description:

Lint, validate, and audit nginx configuration files for syntax errors, security issues, and performance problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint nginx configuration files, run security and performance audits, and generate diagnostic reports for local review or CI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive scans can read nginx configuration files outside the intended review scope.

Mitigation: Run recursive mode only on directories selected for audit and exclude unrelated private configuration paths.

Risk: Linter reports can contain false positives or miss configuration issues because they are local diagnostic output.

Mitigation: Review findings before applying changes or enforcing CI gates, and confirm production readiness with nginx's native validation where appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Text, JSON, or Markdown diagnostic reports with issue severity and exit-code behavior.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports lint, security, performance, and full audit modes; recursive scans are optional.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
