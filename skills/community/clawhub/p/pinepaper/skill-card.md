## Description: <br>
PinePaper helps agents create and animate vector-based text, shapes, diagrams, maps, and visualizations on an infinite canvas through Agent Mode and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speaktoarpit](https://clawhub.ai/user/speaktoarpit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to let an agent build, modify, animate, and export PinePaper canvas content such as diagrams, typography, maps, and visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP server can let an agent control PinePaper actions that clear or delete canvas content and export training data. <br>
Mitigation: Enable it only when agent control of PinePaper is intended, verify the package source, and require explicit approval before clearing, resetting, deleting, or exporting training data. <br>
Risk: The release was flagged as suspicious because the training-data export behavior is under-explained. <br>
Mitigation: Review the training-data export workflow and generated outputs before using them in a production or shared environment. <br>


## Reference(s): <br>
- [PinePaper Studio](https://pinepaper.studio) <br>
- [ClawHub PinePaper release](https://clawhub.ai/speaktoarpit/pinepaper) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with JavaScript examples and MCP tool references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API patterns for creating, animating, selecting, clearing, and exporting canvas content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
