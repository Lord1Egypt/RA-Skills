## Description:

Creates a standard Nginx/OpenResty reverse proxy config file for a service and reloads the web server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieyuanqing](https://clawhub.ai/user/xieyuanqing)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to generate an Nginx/OpenResty reverse proxy configuration for a named service, domain, and local port, then test and reload the running web server container.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify and reload live Nginx/OpenResty configuration.

Mitigation: Review before use on real servers, run first in a controlled environment, and keep backups of existing Nginx configuration.

Risk: Unsafe input handling could overwrite, delete, or inject server configuration.

Mitigation: Use only trusted service names, domains, ports, container names, and verified config directories; avoid traversal paths and symlinks.

Risk: A failed reload or configuration test can affect service availability if recovery is incomplete.

Mitigation: Test with a temporary candidate config, verify rollback behavior, and restore previous files on failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xieyuanqing/skills/nginx-config-creator)
- [Publisher profile](https://clawhub.ai/user/xieyuanqing)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Shell command output and generated Nginx configuration file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and docker; writes an Nginx/OpenResty .conf file and reports test, reload, and rollback status.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
