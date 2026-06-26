## Description: <br>
Control and query a configured Home Assistant smart home through natural language, including lights, switches, climate, sensors, cameras, automations, energy monitoring, presence, and home summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nj070574-gif](https://clawhub.ai/user/nj070574-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent query and control their own Home Assistant instance after configuring a URL and long-lived access token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide broad physical smart-home control, including state-changing and privacy-sensitive operations. <br>
Mitigation: Use a dedicated least-privilege Home Assistant account or token, avoid access to locks, alarms, garage doors, cameras, and notification services unless intentionally needed, and require explicit confirmation for state-changing or privacy-sensitive commands. <br>
Risk: The skill requires sensitive Home Assistant credentials. <br>
Mitigation: Store credentials only in the OpenClaw environment or configuration with restricted file permissions, and rotate the long-lived token if it is exposed. <br>
Risk: Disabling SSL verification can weaken connection security for HTTPS deployments. <br>
Mitigation: Prefer a CA certificate over HOME_ASSISTANT_SSL_VERIFY=false when using HTTPS with a self-signed certificate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nj070574-gif/home-assistant-skill) <br>
- [Publisher profile](https://clawhub.ai/user/nj070574-gif) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style guidance with Python snippets, JSON configuration examples, shell commands, Home Assistant service-call results, and camera snapshot URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HOME_ASSISTANT_URL and HOME_ASSISTANT_TOKEN; may read or change smart-home device state through the configured Home Assistant REST API.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
