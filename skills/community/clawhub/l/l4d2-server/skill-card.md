## Description:

Helps agents manage Left 4 Dead 2 servers by storing server aliases, querying server status over A2S, and running administrative commands over RCON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laoyutang](https://clawhub.ai/user/laoyutang)

### License/Terms of Use:

MIT-0

## Use Case:

Server administrators and operators use this skill to keep track of Left 4 Dead 2 server connection details, check live server status, and prepare or run RCON administration commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RCON grants live administrative control over a configured Left 4 Dead 2 server.

Mitigation: Install and use the skill only for servers you administer, and manually confirm any command that changes maps, kicks or bans players, toggles cheats, or alters server state.

Risk: RCON passwords can leak through command-line arguments or readable configuration files.

Mitigation: Avoid passing passwords on the command line where possible, restrict configuration file permissions to the owner, and keep secrets out of shared logs or transcripts.

Risk: Exposed RCON access can permit remote server administration by unauthorized parties.

Mitigation: Keep RCON off public networks, use a VPN or SSH tunnel, and restrict firewall access to trusted administrators.

## Reference(s):

- [server-config.example.json](references/server-config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local Python helper scripts to query A2S status or send RCON commands to configured servers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
