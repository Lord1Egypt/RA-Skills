## Description:

Manage and monitor a local Pi-hole instance by querying the FTL database for statistics and helping run Pi-hole CLI management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1999azzar](https://clawhub.ai/user/1999azzar)

### License/Terms of Use:


## Use Case:

Network administrators and home lab operators use this skill to inspect Pi-hole query statistics, identify top domains or clients, and prepare Pi-hole management commands for status checks, gravity updates, and blocking changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pi-hole management actions can change DNS filtering behavior for the network.

Mitigation: Require explicit user confirmation before enable, disable, gravity update, whitelist, or blacklist operations.

Risk: Local Pi-hole query logs can reveal domain and client activity on the network.

Mitigation: Limit database access to authorized users and avoid sharing raw query details unless the user requests them.

## Reference(s):

- [Pi-hole Database Schema](references/db-schema.md)
- [ClawHub skill page](https://clawhub.ai/1999azzar/skills/pihole-ctl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON statistics, Markdown guidance, and CLI command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require read access to the local Pi-hole FTL database and appropriate permissions for Pi-hole CLI management commands.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
