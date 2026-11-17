## Description:

Validate .env files for common issues, including leaked secrets, duplicate variables, empty values, .env.example drift, and syntax errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Env Doctor to audit local or CI .env files for exposed secrets, duplicate or malformed variables, placeholder values, and drift from .env.example templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads .env files that may contain secrets, and terminal or JSON reports can expose sensitive configuration details.

Mitigation: Run it only on files you intend to inspect, limit access to generated reports and CI logs, and treat output as sensitive.

## Reference(s):

- [Env Doctor ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-env-doctor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal report or structured JSON, usually summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes indicate health: 0 healthy, 1 issues, 2 possible secret leaks; reports and CI logs should be treated as sensitive.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
