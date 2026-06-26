## Description: <br>
Control and monitor a Loxone Miniserver smart home via HTTP API and real-time WebSocket for room and device status, live events, and explicitly requested control commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odrobnik](https://clawhub.ai/user/odrobnik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-home operators use this skill to query Loxone rooms and devices, monitor real-time events, and send user-approved control commands to a configured Miniserver. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send commands that control real smart-home devices. <br>
Mitigation: Require an explicit user request before any control command and keep normal operation read-only. <br>
Risk: The skill needs Loxone Miniserver credentials and can store them in config.json. <br>
Mitigation: Use a least-privilege Loxone account, restrict config.json permissions, and keep the file private. <br>
Risk: One authentication helper can print a live token-bearing WebSocket URL. <br>
Mitigation: Avoid sharing helper output and redact tokens before logs or transcripts are stored. <br>
Risk: Cached structure files may reveal rooms, controls, and other smart-home layout details. <br>
Mitigation: Protect cached files or delete them when they are no longer needed. <br>
Risk: Local HTTP or misconfigured remote access can expose credentials or control traffic. <br>
Mitigation: Prefer HTTPS with certificate verification and use the documented Cloud DNS path for remote access. <br>


## Reference(s): <br>
- [Loxone setup instructions](SETUP.md) <br>
- [ClawHub skill page](https://clawhub.ai/odrobnik/loxone) <br>
- [Skill homepage](https://github.com/odrobnik/loxone-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also surface live status text, JSON event output, and configuration file guidance from the Loxone scripts.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
