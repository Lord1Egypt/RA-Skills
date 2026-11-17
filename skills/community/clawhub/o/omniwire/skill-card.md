## Description:

OmniWire is an infrastructure skill for AI agent swarms with MCP tools for mesh control, remote execution, A2A coordination, VPN management, CyberSync, web scraping, firewall management, and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voidchecksum](https://clawhub.ai/user/voidchecksum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use OmniWire to let agents administer remote machines, coordinate work across a mesh, transfer files, manage services and containers, automate browsers, and synchronize agent configuration or knowledge stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable broad unattended administration of remote machines and persistent services.

Mitigation: Install only for intentional remote-infrastructure administration, tightly gate unattended execution, and scope approved nodes and actions before use.

Risk: The skill handles credentials-adjacent data, including sync stores, cookies, TOTP data, and agent configuration paths.

Mitigation: Avoid syncing secrets or sensitive agent data unless each path and destination is explicitly approved.

Risk: The release installs an npm package that can administer servers over SSH.

Mitigation: Pin and review the npm package before installing, avoid root SSH accounts, and use least-privilege keys.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/voidchecksum/skills/omniwire)
- [ClawHub publisher profile](https://clawhub.ai/user/voidchecksum)
- [NPM package](https://www.npmjs.com/package/omniwire)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or invoke remote-administration workflows that require user approval, least-privilege credentials, and explicit scoping.]

## Skill Version(s):

3.5.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
