## Description:

Bootstrap a local dev stack for browser preview without root or Docker: install databases and services, debug vanishing background processes, inject multi-line secrets into systemd, and fix the UI-opens-but-login-404s case.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to run and troubleshoot a local web application stack on a machine without root access or Docker, including its database, services, secrets, and browser login flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports passwordless database access in the setup guidance.

Mitigation: Review the database authentication options before use; keep the development database bound to loopback and use authenticated access wherever it could be reachable by other users or hosts.

Risk: The setup guidance disables Go module checksum verification, weakening dependency integrity checks.

Mitigation: Keep dependency integrity checks enabled and verify downloaded tools and archives before installing or extracting them.

Risk: Reusing existing data, changing stored password hashes, and partially inspected local references can affect data integrity or account access.

Mitigation: Review the relevant commands and unresolved references before running them, back up existing data first, and remove temporary credential-update scripts after use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zuoyunlai/skills/local-dev-stack-bootstrap)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with inline shell commands, scripts, and service configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instructional steps include placeholders that must be adapted to the local project and environment.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
