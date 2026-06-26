## Description: <br>
PikaBoard helps agents create, update, list, and manage tasks through the PikaBoard task management API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelstreet](https://clawhub.ai/user/angelstreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to a local PikaBoard task board, manage task status, and keep agent work queues scoped by board. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PikaBoard uses a bearer token, and exposing the real token in shared or version-controlled files can grant unintended task-board access. <br>
Mitigation: Use a dedicated PikaBoard token and avoid placing the real token in shared or version-controlled files such as TOOLS.md. <br>
Risk: Agent automation can modify the wrong tasks or board if board scoping is not configured. <br>
Mitigation: Configure MY_BOARD_ID before allowing an agent to operate and review important task or board changes before automation proceeds. <br>
Risk: The release depends on the PikaBoard repository and npm dependencies installed during setup. <br>
Mitigation: Install only when you trust the PikaBoard repository and its npm dependency chain. <br>


## Reference(s): <br>
- [PikaBoard ClawHub listing](https://clawhub.ai/angelstreet/pikaboard) <br>
- [PikaBoard repository](https://github.com/angelstreet/pikaboard) <br>
- [API documentation pointer](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PikaBoard environment variables, bearer token authentication, and board_id scoping when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
