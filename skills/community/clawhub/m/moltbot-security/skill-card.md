## Description: <br>
Security hardening for AI agents - Moltbot, OpenClaw, Cursor, Claude. Lock down gateway, fix permissions, auth, firewalls. Essential for vibe-coding setups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NextFrontierBuilds](https://clawhub.ai/user/NextFrontierBuilds) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to review and harden Moltbot, OpenClaw, and related AI-agent gateway deployments. It provides security checklist guidance, audit commands, configuration examples, and operational safeguards for authentication, permissions, firewalling, SSH, and remote access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes commands that can change firewall, SSH, package, and permission settings. <br>
Mitigation: Run audits without --fix first when possible, confirm console or recovery access before firewall or SSH changes, and avoid sudo commands on production or remote systems unless the effect is understood. <br>
Risk: The skill references remote installer scripts and package update commands. <br>
Mitigation: Inspect remote installer scripts before execution and prefer trusted operating-system or vendor documentation when applying system package changes. <br>


## Reference(s): <br>
- [Moltbot Security ClawHub Listing](https://clawhub.ai/NextFrontierBuilds/moltbot-security) <br>
- [Original exposed gateway research](https://x.com/nickspisak_/status/2016195582180700592) <br>
- [Node.js downloads](https://nodejs.org/) <br>
- [Tailscale installer](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only security hardening guidance; users decide which commands or configuration changes to apply.] <br>

## Skill Version(s): <br>
1.0.3 (source: SKILL.md frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
