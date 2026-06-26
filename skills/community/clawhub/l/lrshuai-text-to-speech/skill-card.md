## Description: <br>
Converts text prompts into natural-sounding spoken audio through configured text-to-speech model endpoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, agents, and developers use this skill to convert text into spoken output through supported TTS models. It is suited for workflows that need command-line text-to-speech generation with a configured TEAM_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports broader model and file-upload abilities than a simple text-to-speech helper. <br>
Mitigation: Use only the intended TTS model IDs and avoid passing local media files unless the upload to the configured endpoint is intentional. <br>
Risk: The skill sends requests with TEAM_API_KEY to dlazy.com or a configured TEAM_BASE_URL endpoint. <br>
Mitigation: Use a scoped key, verify the endpoint before execution, and rotate or revoke the key if exposure is suspected. <br>
Risk: The security evidence notes that the skill bypasses the normal OpenClaw runner without enough disclosure. <br>
Mitigation: Review the script before use and prefer a version that declares its network, dependency, and runner requirements clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-text-to-speech) <br>
- [Default TEAM_BASE_URL endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Text] <br>
**Output Format:** [Command-line execution with JSON responses printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY; TEAM_BASE_URL can override the default endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
