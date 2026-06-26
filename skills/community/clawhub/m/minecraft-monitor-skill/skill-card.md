## Description: <br>
Monitor Minecraft servers by checking online status, player counts, latency, and version information using the Server List Ping protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wmantly](https://clawhub.ai/user/wmantly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, server operators, and automation agents use this skill to check Minecraft server availability, player counts, latency, version information, MOTD, and sample player lists from a supplied host and optional port. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes TCP connections to Minecraft server addresses provided by the user. <br>
Mitigation: Run it only against servers you intend to query and in network environments where outbound Minecraft status checks are permitted. <br>
Risk: Server MOTD and player-name output are untrusted remote text. <br>
Mitigation: Review or sanitize that output before displaying it in dashboards, logs, alerts, or other downstream systems. <br>
Risk: Continuous production monitoring could receive large or unexpected responses from remote servers. <br>
Mitigation: Add stricter response limits and operational monitoring before using the script for continuous production checks. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text status output and Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exit code 0 when the server is online and 1 when it is offline.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
