## Description: <br>
Controls a hosted OpenClaw instance through the OpenClaw as a Service API for chat, file, terminal, and instance operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fstandhartinger](https://clawhub.ai/user/fstandhartinger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a user's hosted OpenClaw instance over API, including sending chat messages, uploading or editing text files, reading workspace files, running terminal commands, and managing instances. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local text files or folders to a hosted OpenClaw workspace when explicitly asked. <br>
Mitigation: Review upload sources before execution and avoid sending sensitive local files unless they are intended for the target instance. <br>
Risk: Remote terminal commands can change the hosted workspace or expose workspace data. <br>
Mitigation: Review commands before execution, scope OPENCLAW_INSTANCE_ID when multiple instances exist, and inspect command results before taking follow-up actions. <br>
Risk: OPENCLAW_API_KEY grants access to the user's owned OpenClaw instances. <br>
Mitigation: Keep the API key private, provide it only through environment variables, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fstandhartinger/openclaw-api-control) <br>
- [OpenClaw API endpoint](https://openclaw-as-a-service.com/api) <br>
- [OpenClaw API client](artifact/scripts/openclaw_api_client.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON, text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENCLAW_API_KEY; can use OPENCLAW_API_BASE_URL and OPENCLAW_INSTANCE_ID.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
