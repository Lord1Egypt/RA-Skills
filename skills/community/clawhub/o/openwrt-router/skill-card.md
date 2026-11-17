## Description:

Manages and monitors OpenWRT routers through the LuCI web interface, including DHCP leases, connected devices, WiFi clients, network status, and package information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nary24](https://clawhub.ai/user/nary24)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and network administrators use this skill to help an agent inspect OpenWRT, ImmortalWrt, and LEDE routers, summarize connected devices and WiFi status, check router health, and prepare LuCI RPC shell commands for approved administrative actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent high-impact administrative access to a router.

Mitigation: Install only when this access is acceptable, avoid root credentials where possible, and require explicit review before configuration changes or package installation.

Risk: Router credentials and LuCI sessions may be exposed when using insecure HTTP or storing passwords in agent-readable files or shell history.

Mitigation: Prefer HTTPS or an encrypted tunnel, keep credentials out of TOOLS.md and shell history, and rotate credentials if they are exposed.

Risk: LuCI RPC shell commands can disrupt network availability if incorrect commands are executed.

Mitigation: Review generated commands before execution and limit routine use to read-only status checks unless a change has been explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nary24/skills/openwrt-router)
- [Publisher Profile](https://clawhub.ai/user/nary24)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce LuCI RPC command sequences that require router credentials and explicit review before configuration changes.]

## Skill Version(s):

1.1.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
