## Description: <br>
Provides sunrise, sunset, dawn, dusk, solar noon, golden hour, first light, last light, and day length times for any latitude and longitude worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to retrieve sun-event times for location-aware workflows, scheduling, travel, and planning scenarios. It supports today's solar times or a specified date for any latitude and longitude. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious and notes that an autoreview helper in the skill set can grant nested review tools full local access by default. <br>
Mitigation: Review helper behavior before installation or use, prefer --no-yolo or AUTOREVIEW_YOLO=0 unless full local access is intended, and confirm credentials, targets, and impact before moderation or publishing workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-sunrisesunset) <br>
- [Pipeworx sunrise/sunset MCP endpoint](https://gateway.pipeworx.io/sunrisesunset/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns solar-event timing guidance for the requested coordinates and optional date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
