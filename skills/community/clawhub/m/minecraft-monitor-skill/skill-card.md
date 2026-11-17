## Description:

Minecraft Monitor checks Minecraft server online status, player counts, latency, version information, sample player names, and MOTD using the Server List Ping protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wmantly](https://clawhub.ai/user/wmantly)

### License/Terms of Use:


## Use Case:

Developers, server operators, and automation workflows use this skill to check whether Minecraft servers are reachable and to report status, latency, version, player counts, and MOTD without server-side plugins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Minecraft servers can delay responses or print misleading terminal output.

Mitigation: Use explicit timeouts, prefer trusted or expected hosts, and review output before feeding it into automated alerts or dashboards.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Status details include online/offline state, latency, version, player counts, optional sample player list, MOTD, and exit status guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
