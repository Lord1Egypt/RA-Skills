## Description:

Make HTTP requests from the command line with support for auth (Bearer, Basic, API key), custom headers, JSON/form body, response formatting, timing, and history logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to make command-line HTTP requests for API testing, auth flow checks, webhook debugging, health monitoring, and CI automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential options and custom headers can expose secrets through shell history, process listings, verbose output, or logs.

Mitigation: Review before using real credentials; avoid passing production tokens directly on the command line and avoid verbose output with secrets.

Risk: Skipping TLS verification can make HTTPS requests vulnerable to interception.

Mitigation: Use --no-verify only in controlled local testing and keep certificate verification enabled for normal use.

Risk: Redirects and saved response files can expose authenticated requests or sensitive response content.

Mitigation: Review redirect behavior and output paths before execution, and treat saved response files as sensitive data.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [Terminal text, optional JSON response objects, and optional saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exit codes distinguish successful HTTP responses, HTTP errors, and network or usage errors.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
