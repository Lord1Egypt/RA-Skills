## Description:

Query remote databases through Pilot Protocol tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to reach remote PostgreSQL, MySQL, MongoDB, or Redis databases through Pilot Protocol tunnels when direct network access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes database access through Pilot Protocol and depends on the local pilotctl binary, Pilot daemon, and configured database endpoints.

Mitigation: Install and use it only when those components and endpoints are trusted for the target database environment.

Risk: Gateway mappings can leave a path to sensitive database services available longer than intended.

Mitigation: Stop the gateway when finished and handle database credentials and production access with normal operational controls.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-database-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot daemon, configured Pilot Protocol access, and the relevant database client.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
