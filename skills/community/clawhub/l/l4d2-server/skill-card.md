## Description: <br>
L4D2 Server helps agents manage Left 4 Dead 2 servers by storing server configurations, querying status through A2S, and running RCON commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LaoYutang](https://clawhub.ai/user/LaoYutang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Server administrators and agents use this skill to keep a local list of L4D2 servers, inspect live server status, and send approved RCON administration commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RCON passwords can expose administrative control if stored insecurely or pasted into transcripts. <br>
Mitigation: Protect the password file, avoid sharing secrets in chat or shell history, and prefer trusted networks, VPNs, or SSH tunnels for RCON access. <br>
Risk: RCON commands can change gameplay, kick or ban players, or otherwise affect a live server. <br>
Mitigation: Manually confirm commands that modify gameplay or affect players before execution, and install the skill only for servers you administer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LaoYutang/l4d2-server) <br>
- [Server configuration example](references/server-config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include server status details and RCON command recommendations; commands that affect players or gameplay should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
