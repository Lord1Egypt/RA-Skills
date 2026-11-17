## Description:

Installs or repairs Hirey Hi on a local OpenClaw host, including MCP setup, local receiver wiring, registration, health checks, and welcome onboarding for people-finding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzlee](https://clawhub.ai/user/yzlee)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to install or repair Hirey Hi so their agent can publish people-finding needs, search for matches, contact leads, and coordinate follow-up across jobs, recruiting, housing, friendship, dating, founders, investors, lawyers, and related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install adds persistent OpenClaw hooks and an MCP server.

Mitigation: Review the host configuration changes before use and remove the managed hooks or MCP server if the install is no longer needed.

Risk: The default service endpoint uses plaintext HTTP.

Mitigation: Avoid sensitive accounts or private matching workflows until an HTTPS endpoint is available.

Risk: The install stores a local bearer token and binds the current chat for future replies.

Mitigation: Use only on hosts where local token storage and chat continuation routing are acceptable.

Risk: The workflow depends on remote onboarding instructions.

Mitigation: Review onboarding output before publishing listings or contacting matches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzlee/skills/openclaw-hi-install)
- [Publisher profile](https://clawhub.ai/user/yzlee)
- [Hirey Hi default service](http://hi.hireyapp.us)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a host install flow that may write persistent OpenClaw hooks, MCP configuration, local package state, and onboarding text.]

## Skill Version(s):

0.1.56 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
