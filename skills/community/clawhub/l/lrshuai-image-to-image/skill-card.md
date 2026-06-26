## Description: <br>
Image-to-image skill that uses a reference image and text prompt to generate a new image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can invoke this skill when they need an agent to call supported image-generation models with a prompt and optional reference media. The skill requires a TEAM_API_KEY and sends prompts and uploaded media to a third-party remote API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads prompts and reference media to a third-party remote API using a bearer token. <br>
Mitigation: Use a dedicated low-privilege TEAM_API_KEY, avoid sensitive prompts or media, and install only if the dlazy.com service is trusted for the intended data. <br>
Risk: The skill asks the agent to run a Python script directly instead of using the normal OpenClaw runner. <br>
Mitigation: Review the exact command and script behavior before execution, and avoid setting TEAM_BASE_URL unless the endpoint is controlled and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-image-to-image) <br>
- [Remote API endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Console text with JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a Python script that submits generation requests, polls for completion when needed, and prints the final response or error.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
