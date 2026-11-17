## Description:

Pp Olx helps agents use the olx-pp-cli Printing Press CLI to query OLX.pl public job-listing API endpoints without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[czarek-commits](https://clawhub.ai/user/czarek-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to install or operate olx-pp-cli for OLX.pl public job-listing queries, inspect available commands, and retrieve structured results through agent-mode JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install and run mutable third-party code through the Printing Press installer and olx-pp-cli.

Mitigation: Install only from trusted sources, pin and verify the installer or CLI version before use, and run olx-pp-cli --version before invoking commands.

Risk: The output delivery option can write command results to local files or send them to arbitrary webhook endpoints.

Mitigation: Review file output paths before allowing writes and use webhook delivery only for intended, trusted endpoints.

Risk: The skill relies on a reverse-engineered public OLX.pl API that may change, fail, or rate limit requests.

Mitigation: Use doctor, help, or dry-run checks before automation, handle non-zero exit codes, and retry rate-limited requests only after waiting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/czarek-commits/skills/pp-olx)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands; CLI executions return JSON in agent mode.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports stdout, file, and webhook delivery sinks when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
