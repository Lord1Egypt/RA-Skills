## Description:

AgentGuard routes OpenClaw command, file, directory, and HTTP operations through ag_* proxy tools for daemon-backed review, redaction, approval, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxz333zxz](https://clawhub.ai/user/zxz333zxz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use Agentguard to route shell commands, file operations, directory listing, HTTP requests, skill checks, and emergency stop or resume controls through a local AgentGuard daemon for review and audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AgentGuard becomes the gatekeeper for agent command, file, write, and network requests through an opaque local daemon.

Mitigation: Install only when that control model is intentional, keep daemonHost on 127.0.0.1, and review daemon configuration before use.

Risk: Setup can make persistent system changes by installing a binary to /usr/local/bin, starting a daemon, and requiring tools.deny changes in openclaw.json.

Mitigation: Review setup.sh and openclaw.json changes before applying them; rollback by stopping the daemon, removing tools.deny entries, and deleting /usr/local/bin/agentguard.

Risk: The inspected package did not include the referenced daemon binary, so runtime behavior cannot be fully validated from the artifact alone.

Mitigation: Obtain and verify the matching daemon binary and checksum before deployment; avoid relying on the plugin when the daemon is absent or unverifiable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zxz333zxz/skills/jjy-agentguard)
- [AgentGuard homepage](https://www.agentguard.site)
- [OpenClaw plugin documentation](https://docs.openclaw.ai/tools/plugin)
- [OpenClaw agent tools documentation](https://docs.openclaw.ai/plugins/agent-tools)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [OpenClaw tool responses as text, JSON-derived text, and approval or interception messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local AgentGuard daemon; default dashboard port is 19821; artifact metadata limits support to darwin/linux and setup.sh installs only an arm64 binary.]

## Skill Version(s):

1.8.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
