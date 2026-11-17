## Description:

Hidream Aigc helps agents call HiDream/OpenClaw image and video generation APIs with prompts, model parameters, and optional local media inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhy2015](https://clawhub.ai/user/zhy2015)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate images and videos through HiDream/OpenClaw models from Python or CLI workflows, while supplying required credentials and prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling is under-disclosed and documented flows may persist or shell-write HIDREAM_AUTHORIZATION tokens.

Mitigation: Prefer a process-scoped HIDREAM_AUTHORIZATION value and avoid asking an agent to write tokens with echo commands.

Risk: Endpoint overrides can direct credentialed requests to an untrusted destination.

Mitigation: Do not set HIDREAM_ENDPOINT or OPENCLAW_ENDPOINT unless the destination is fully trusted.

Risk: Generated media is saved as persistent local data under assets/.

Mitigation: Review and manually clean up generated media files when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhy2015/skills/hidream-api-gen)
- [HiDream/OpenClaw Service](https://vivago.ai)
- [HiDream/OpenClaw Token Page](https://vivago.ai/platform/token)
- [HiDream/OpenClaw Account and Credits](https://vivago.ai/platform/info)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell snippets, JSON responses, and local media file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated media may be downloaded under assets/; API calls require HIDREAM_AUTHORIZATION.]

## Skill Version(s):

0.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
