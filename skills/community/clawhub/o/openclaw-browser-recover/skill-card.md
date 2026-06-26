## Description: <br>
Diagnose and recover OpenClaw browser tool timeouts involving gateway ports 18789/18791, Chrome CDP 9222 conflicts, MCP connection closures, and browser-control startup failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sajdijjsid](https://clawhub.ai/user/sajdijjsid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose browser-control failures and choose the next recovery action when browser status, tabs, snapshots, gateway ports, or Chrome CDP connectivity fail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The troubleshooting flow may inspect local gateway status, listening ports, and up to five browser tabs. <br>
Mitigation: Run the checks only when troubleshooting OpenClaw browser-control problems and review any status or tab information before sharing it. <br>
Risk: Restarting the OpenClaw gateway may interrupt active browser-control work. <br>
Mitigation: Limit the recovery flow to one gateway restart unless the user explicitly asks for additional stop/start actions. <br>
Risk: The artifact instructions are primarily written in Chinese. <br>
Mitigation: Non-Chinese readers should translate or review the instructions before relying on the recovery guidance. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest local gateway status checks, listening-port checks, lightweight browser probes, and at most one gateway restart during a recovery flow.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
