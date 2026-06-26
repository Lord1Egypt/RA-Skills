## Description: <br>
Control NordVPN on Linux via the `nordvpn` CLI for connecting, disconnecting, selecting countries, cities, or groups, reading status, changing settings, and managing allowlist entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maciekish](https://clawhub.ai/user/maciekish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to guide an agent in operating a local NordVPN Linux CLI session for region routing, temporary VPN tunneling, connection verification, settings changes, and allowlist management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to change VPN state, routing, connectivity, privacy settings, and allowlist behavior through the local NordVPN CLI. <br>
Mitigation: Review requested connection, settings, and allowlist changes before execution, then verify the resulting state with `nordvpn status` and `nordvpn settings`. <br>
Risk: Using an unexpected or untrusted `nordvpn` binary could affect routing and privacy behavior. <br>
Mitigation: Verify the NordVPN CLI comes from NordVPN or a trusted package source, and use the expected binary path when the install method requires it. <br>


## Reference(s): <br>
- [NordVPN homepage](https://nordvpn.com/) <br>
- [ClawHub NordVPN skill page](https://clawhub.ai/maciekish/nordvpn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should preserve human review for login, settings, allowlist, and connection changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
