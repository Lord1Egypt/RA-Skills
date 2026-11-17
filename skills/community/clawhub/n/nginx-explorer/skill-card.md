## Description:

Explore nginx-proxied directories to discover tools and utilities by fetching directory listings and README files from a configured nginx URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaojun0](https://clawhub.ai/user/shaojun0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect a trusted nginx-hosted directory of tools, read available README files, and identify utilities that may help with a task when conventional approaches are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent to download, install dependencies for, or execute remote tools without strong trust and approval controls.

Mitigation: Use only a trusted, HTTPS-protected nginx host; require human review of the source and checksum or signature before any downloaded tool is executed.

Risk: Downloaded tools may run in an environment with sensitive credentials or persistent filesystem access.

Mitigation: Run downloaded tools only in a disposable sandbox with no sensitive credentials and clean up temporary files after review.

Risk: Skipping SSL verification can weaken trust in the nginx host connection.

Mitigation: Disable SSL verification skipping for normal use and reserve it only for explicitly trusted internal networks with self-signed certificates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaojun0/skills/nginx-explorer)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured NGINX_URL and curl access to the nginx host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
