## Description: <br>
Controls BT-Panel servers through the BT-Panel HTTP API to inspect system status, disk, memory, load, sites, databases, SSL certificates, scheduled tasks, Docker, and arbitrary BT-Panel endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to manage BT-Panel-backed servers from an agent workflow, starting with read-only status checks and requiring confirmation before write operations such as stopping sites, changing configuration, or renewing certificates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad BT-Panel administrative authority using powerful server credentials. <br>
Mitigation: Install only where that authority is acceptable, use a least-privilege token where possible, and review commands before production use. <br>
Risk: A public tunnel or loose allowlist can make the token the primary protection for remote administration. <br>
Mitigation: Restrict IP allowlists tightly, avoid relying on a public tunnel as the only protection, and add network controls such as IP filtering or BasicAuth where appropriate. <br>
Risk: The helper can print or use sensitive BT-Panel tokens. <br>
Mitigation: Keep tokens out of the repository, store local credentials with restrictive permissions, and rotate any token exposed by setup or helper output. <br>
Risk: The raw endpoint path can call broad BT-Panel API actions, including write operations. <br>
Mitigation: Review or remove raw endpoint access for production installs and require explicit confirmation before write or destructive operations. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [BT-Panel endpoint reference](references/endpoints.md) <br>
- [Changelog](docs/changelog.md) <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-baota-control) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with shell commands and summarized JSON results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operational results should be summarized for the user rather than pasted as full raw JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-06-25) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
