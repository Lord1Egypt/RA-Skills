## Description: <br>
Manage GoList grocery lists via CLI: create, join, switch, share lists, and add or remove items with automatic device and item ID handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniel17903](https://clawhub.ai/user/daniel17903) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to create, join, share, switch, read, and update GoList shopping lists through a Python CLI. It is suited for grocery-list collaboration where the agent manages device IDs, list IDs, item IDs, and timestamps behind the scenes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends shopping-list content, device identifiers, and share-token operations to go-list.app. <br>
Mitigation: Install only if you are comfortable using go-list.app for this data and review proposed CLI actions before execution. <br>
Risk: Share URLs, share tokens, and the local state file can expose or preserve access to list context. <br>
Mitigation: Keep tokens and share URLs private, and remove or isolate ~/.openclaw_golist_state.json on shared machines or when resetting saved context. <br>


## Reference(s): <br>
- [ClawHub GoList release page](https://clawhub.ai/daniel17903/golist) <br>
- [GoList application and API service](https://go-list.app/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist a device ID, active list, and known list context in ~/.openclaw_golist_state.json unless OPENCLAW_STATE_FILE is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
