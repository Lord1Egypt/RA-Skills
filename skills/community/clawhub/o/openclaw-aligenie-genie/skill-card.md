## Description: <br>
OpenClaw Aligenie Genie lets an OpenClaw agent communicate bidirectionally with Tmall Genie through a configured cloud server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect OpenClaw agents with Tmall Genie, configure the cloud bridge, register agents, poll for Genie requests, and submit replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route Tmall Genie messages and related metadata through a configured cloud server. <br>
Mitigation: Install only when you control and can review the server side, and document what message data is processed by the bridge. <br>
Risk: The release evidence warns that the setup may expose a sensitive agent-control service. <br>
Mitigation: Use HTTPS, restrict firewall access to trusted sources or a VPN, protect API keys, rotate keys when needed, and avoid plaintext key files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-aligenie-genie) <br>
- [Technical specification](artifact/SPEC.md) <br>
- [Deployment guide](artifact/DEPLOY.md) <br>
- [OpenClaw Aligenie client](artifact/genie_client.py) <br>
- [SQLite JDBC releases](https://github.com/xerial/sqlite-jdbc/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python, shell, PowerShell, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Aligenie server URL, API key, and agent ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
