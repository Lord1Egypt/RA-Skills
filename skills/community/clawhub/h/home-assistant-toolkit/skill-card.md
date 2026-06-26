## Description: <br>
Home Assistant management skill for controlling devices, creating automations, monitoring health, managing backups, updating HACS, generating dashboards, scanning integrations, and fetching release notes through SSH and the Home Assistant REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vitaliisergin](https://clawhub.ai/user/vitaliisergin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Home Assistant users and smart-home operators use this skill to let an agent inspect, configure, troubleshoot, automate, and maintain a Home Assistant instance. It is suited for local or trusted-network administration where the user is comfortable granting persistent SSH and long-lived API access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent SSH and long-lived Home Assistant API access can grant broad control over devices, configuration, backups, logs, and service calls. <br>
Mitigation: Use a dedicated revocable SSH key and API token, keep access on a trusted network or VPN, and review the scripts before enabling the skill. <br>
Risk: Administrative actions such as restore, backup deletion, restart, dashboard apply, and arbitrary service calls can be disruptive or destructive. <br>
Mitigation: Require explicit manual confirmation before running these actions and keep current backups before changing configuration. <br>
Risk: Password-based SSH configuration can create weaker operational security than key-based access. <br>
Mitigation: Prefer dedicated SSH keys over password authentication and revoke credentials immediately when the skill is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vitaliisergin/home-assistant-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/vitaliisergin) <br>
- [Project homepage](https://github.com/motionbeard/home-assistant-openclaw) <br>
- [Home Assistant Release Notes Reference](references/ha-release-notes.md) <br>
- [Home Assistant State Reference](references/ha-state.json) <br>
- [Installed Integrations Reference](references/user-integrations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML, JSON, and generated local reference files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local scripts that call the user's Home Assistant REST API, SSH host, and public GitHub release API when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
