## Description: <br>
Track water and sleep with JSON file storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stellarhold170NT](https://clawhub.ai/user/Stellarhold170NT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and personal agent workflows use this skill to record water intake, sleep and wake events, view simple stats, and update or delete recent water records in a local JSON file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node.js commands that write personal water and sleep history to health-data.json. <br>
Mitigation: Install only when local command execution and local storage of this personal log are acceptable. <br>
Risk: Water cup counts are substituted into shell snippets. <br>
Mitigation: Treat cup counts as numbers and do not copy arbitrary text into the command placeholder. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Stellarhold170NT/healthcheck) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Node.js snippets to read and write health-data.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
