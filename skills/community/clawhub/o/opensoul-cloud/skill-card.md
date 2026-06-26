## Description: <br>
Share anonymized OpenClaw configurations with the OpenSoul community. Use when user wants to share their agent setup, discover how others use OpenClaw, or get inspiration for new capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fnaser](https://clawhub.ai/user/fnaser) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to preview, anonymize, share, browse, import, and delete community agent setup profiles for inspiration and reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive workspace data when preparing a shareable OpenClaw setup. <br>
Mitigation: Run `opensoul share --preview` before upload and inspect the complete anonymized output before confirming any share. <br>
Risk: Credentials stored in `~/.opensoul/credentials.json` identify the user to OpenSoul. <br>
Mitigation: Keep the credentials file private and do not include it in shared, imported, or published files. <br>
Risk: Imported community files may contain unsafe or unsuitable instructions. <br>
Mitigation: Treat imported files as untrusted reference material and review them before adapting any patterns or instructions. <br>
Risk: Remote `OLLAMA_URL` settings can expose workspace summaries to an unintended service. <br>
Mitigation: Prefer local Ollama configuration and avoid remote `OLLAMA_URL` values unless the endpoint is trusted. <br>


## Reference(s): <br>
- [OpenSoul API Reference](artifact/references/api.md) <br>
- [OpenSoul Schema Reference](artifact/references/schema.md) <br>
- [OpenSoul Website](https://opensoul.cloud) <br>
- [ClawHub Skill Page](https://clawhub.ai/fnaser/opensoul-cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, text summaries, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save imported community files locally and may upload anonymized workspace profiles after preview and confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
