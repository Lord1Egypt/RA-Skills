## Description:

Safe ComfyUI image generation. Use saved or ad-hoc server profiles, paste/upload raw workflow JSON, submit, poll, and serve downloaded outputs locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genortg](https://clawhub.ai/user/genortg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run ComfyUI image-generation workflows from saved or ad-hoc server profiles, submit workflow JSON, poll jobs, and retrieve generated output paths and view URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved server profiles can contain API keys, usernames, or passwords.

Mitigation: Prefer environment-only credentials, avoid saving API keys or passwords in profiles, and delete saved profiles that are no longer needed.

Risk: Generated media can be served by a temporary local viewer without authentication.

Mitigation: Do not run the generated-media viewer on an untrusted network unless it is changed to bind only to localhost and require authentication.

Risk: ComfyUI requests may send prompts and credentials to a configured server.

Mitigation: Use only trusted ComfyUI servers and prefer HTTPS for any non-local server.

## Reference(s):

- [ComfyUI Safe Connector Configuration](artifact/references/CONFIG.md)
- [ComfyUI Safe Connector Endpoints](artifact/references/ENDPOINTS.md)
- [ClawHub skill page](https://clawhub.ai/genortg/skills/openclaw-comfyui-api-runner)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON responses with local file paths, view URLs, and command-oriented guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads generated media under generated/ and can expose temporary local browser view URLs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
