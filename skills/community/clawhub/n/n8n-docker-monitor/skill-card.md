## Description: <br>
N8N Docker Monitor helps agents inspect n8n Docker container status, recent logs, health, and resource usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yesong-hue](https://clawhub.ai/user/yesong-hue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect n8n services running in Docker, summarize container status, review recent logs, and check health and resource signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recent n8n logs may include URLs, workflow details, or secrets if the application emits them. <br>
Mitigation: Review log output before sharing it outside the operating context. <br>
Risk: The package has inconsistent metadata across release evidence and artifact files. <br>
Mitigation: Confirm the publisher and package identity before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yesong-hue/n8n-docker-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/yesong-hue) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Docker command examples and simple status tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May surface Docker status, recent n8n logs, container health, CPU usage, and memory usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter; artifact metadata also lists 1.0.1 and skill.yaml lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
