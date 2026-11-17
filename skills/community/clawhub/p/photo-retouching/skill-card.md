## Description:

Runs RunningHub ComfyUI workflows to submit photo retouching jobs, upload image inputs, monitor task status, and retrieve generated results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uiueux](https://clawhub.ai/user/uiueux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run RunningHub-hosted ComfyUI photo retouching or image transformation workflows from an agent, including image upload, task submission, status polling, and result retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes Chrome DevTools automation that can control a local browser session.

Mitigation: Review or remove chrome_automation.py before use, and do not run it against a normal logged-in browser profile.

Risk: API keys and uploaded images are sent to RunningHub workflows.

Mitigation: Prefer RUNNINGHUB_API_KEY, avoid command-line API keys and saved-key storage, and treat uploaded images as shared with RunningHub.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/uiueux/skills/photo-retouching)
- [RunningHub](https://www.runninghub.ai/)
- [RunningHub OpenAPI v2 endpoint](https://www.runninghub.ai/openapi/v2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code snippets, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce RunningHub task IDs, status JSON, image URLs, and local configuration when helper scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
