## Description: <br>
Generates environmental or special sound effects from text prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to submit text prompts for SFX generation through a Python helper, with optional local or remote media inputs when the selected model supports them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can invoke remote model calls beyond the advertised SFX-only flow. <br>
Mitigation: Review the command before running it and use only the expected SFX model unless the broader behavior has been approved. <br>
Risk: The helper uses an API key and can upload local image or video files when optional media arguments are supplied. <br>
Mitigation: Use a narrowly scoped TEAM_API_KEY, verify TEAM_BASE_URL, and avoid passing private local media paths. <br>


## Reference(s): <br>
- [LrshuAI Sfx Generation on ClawHub](https://clawhub.ai/lrshu/lrshuai-sfx-generation) <br>
- [Publisher profile: lrshu](https://clawhub.ai/user/lrshu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Text] <br>
**Output Format:** [CLI stdout containing JSON responses, status messages, or error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY; TEAM_BASE_URL may override the default remote API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
