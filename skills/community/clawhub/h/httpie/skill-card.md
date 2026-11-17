## Description:

HTTPie helps agents install and use the HTTPie command-line client to build, execute, debug, and troubleshoot HTTP requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and API practitioners use this skill to construct HTTPie commands for REST API debugging, authentication, file transfer, formatted response inspection, session handling, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose installation commands or mutable binary downloads.

Mitigation: Review commands before execution, prefer user-scoped or pinned installations, and avoid curl-to-shell patterns.

Risk: HTTP requests can expose credentials, tokens, cookies, or sensitive request data.

Mitigation: Do not place real secrets directly in commands; use safer secret handling and redact tokens from shared output.

Risk: Persistent HTTPie sessions can store authentication material on disk.

Mitigation: Treat HTTPie session files as sensitive credentials and avoid storing production secrets in reusable sessions.

Risk: Disabling TLS verification can hide certificate or interception problems.

Mitigation: Keep TLS verification enabled except in isolated testing and prefer explicit CA configuration for trusted internal services.

## Reference(s):

- [HTTPie homepage](https://httpie.io)
- [HTTPie CLI documentation](https://httpie.io/docs/cli)
- [ClawHub skill page](https://clawhub.ai/cn-big-cabbage/skills/httpie)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTPie command examples and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose network requests, installation commands, authentication headers, session usage, and file upload or download commands for user review.]

## Skill Version(s):

0.1.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
