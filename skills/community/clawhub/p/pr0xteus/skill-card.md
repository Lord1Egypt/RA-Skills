## Description:

Provides trusted self-hosted workloads with operator-approved WireGuard-backed SOCKS5 and HTTP egress through a bearer-protected private API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use pr0xteus to provide trusted self-hosted services with approved country or pool based egress, inspect active proxy cells, and replace failed assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports suspicious setup commands that install executables beyond the declared write scope, a health check that bypasses the configured API endpoint, and an unpinned Docker image; the scan was partial.

Mitigation: Review the setup instructions and health-check endpoint before installing, assess the executable, system-wide changes, sudo use, and image choice, and account for the scan's incomplete coverage.

Risk: Allocated SOCKS5 and HTTP URLs are short-lived bearer capabilities, and control API access uses a bearer token.

Mitigation: Keep proxy URLs and the control token out of logs and public services; obtain the token from a trusted secret store and use only trusted private control endpoints and approved destinations.

## Reference(s):

- [Setup guide](artifact/references/setup.md)
- [Project homepage](https://github.com/psyb0t/pr0xteus)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions, Code]

**Output Format:** [Markdown with shell commands, JSON API examples, YAML configuration, and Go client guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.11.8 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
