## Description:

Lightweight local HTTP file server with plugin support. Serves static files from a webroot, mounts plugin directories at URL prefixes via config, and runs index.py entry points as CGI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start and manage a lightweight local HTTP file server for workspace-hosted static files, configured plugin directories, and optional CGI entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enabling CGI allows local index.py files to run as code under the user's account.

Mitigation: Keep CGI disabled unless needed, enable it only for trusted workspace files, and review executable index.py files before use.

Risk: Exposing the server beyond loopback can make local content reachable outside the machine.

Mitigation: Use token authentication and an allowed_hosts configuration before binding to 0.0.0.0 or using tunnels or reverse proxies.

Risk: Authentication tokens may leak if stored in shared or committed configuration files.

Mitigation: Keep tokens out of shared repositories and rotate them if they may have been exposed.

Risk: The plugin hash check is identified in security guidance as unreliable until fixed.

Mitigation: Avoid relying on plugin CGI hash checks as the sole control; use only trusted plugin directories and review plugin code before enabling CGI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/intranet)
- [SETUP.md](SETUP.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; CGI is optional and disabled by default.]

## Skill Version(s):

3.2.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
