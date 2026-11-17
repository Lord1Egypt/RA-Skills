## Description:

HAProxy load balancer reference. Frontend binds with ACL routing, backend server pools with health checks, balance algorithms (roundrobin/leastconn/source), SSL termination with SNI, stick-table rate limiting, and stats/Prometheus monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill as a quick HAProxy reference for load-balancing concepts, configuration sections, frontend and backend routing, health checks, TLS settings, stick tables, and monitoring commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample credentials and broadly exposed stats or admin endpoints could be copied into production.

Mitigation: Replace sample credentials and restrict stats and admin access to trusted management networks before use.

Risk: TLS examples include a backend setting that skips certificate verification.

Mitigation: Require certificate verification and configure trusted CA files for backend TLS connections.

Risk: Runtime management examples can disable, reweight, or drain live backends.

Mitigation: Review runtime commands against the target environment and apply them only through approved operational procedures.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/haproxy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reference text with inline shell commands and HAProxy configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command-selected reference output for HAProxy topics such as config, frontend, backend, health, ssl, stick-tables, and stats.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
