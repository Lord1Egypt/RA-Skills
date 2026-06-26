## Description: <br>
Generates complete music tracks from text descriptions or style requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrshu](https://clawhub.ai/user/lrshu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to invoke a Python helper that submits a music-generation prompt to a remote Team AI API and returns the generation result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, credentials, and optional local media can be sent to a configured remote service. <br>
Mitigation: Use only a trusted TEAM_BASE_URL, provide a scoped and revocable TEAM_API_KEY, and avoid passing local media unless upload is intended. <br>
Risk: The helper exposes broader model and media parameters than the music-generation summary describes. <br>
Mitigation: Review the command before execution and restrict normal use to the documented suno_music model and prompt-only workflow unless broader behavior is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lrshu/lrshuai-music-generation) <br>
- [Default remote API endpoint](https://dlazy.com/api/ai/tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API Calls] <br>
**Output Format:** [Console text with JSON responses from the remote generation API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEAM_API_KEY; optional local image or video inputs may be encoded and sent to the configured remote service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
