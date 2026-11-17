## Description:

Generate Veo videos from natural-language OpenClaw prompts, with background task handling and browser preview when a result link is returned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and video creators use this skill to generate short Veo videos from chat prompts such as "生成视频：...". It is intended for conversational video creation workflows where the agent can submit the request in the background and surface the completed result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads an existing local OpenClaw API key for remote video generation.

Mitigation: Use a dedicated Wanjiedata credential configured explicitly for this skill, and fail closed when that credential is absent.

Risk: The skill calls an under-disclosed remote endpoint.

Mitigation: Disclose the exact remote endpoint before installation and review whether its use is acceptable for the intended prompts and environment.

Risk: The worker automatically opens the generated URL in the user's browser.

Mitigation: Return generated links for user approval before opening them automatically.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/jiege-openclaw-video-v1-2-2)
- [Publisher profile](https://clawhub.ai/user/liangshenghzj888-stack)
- [Remote video API endpoint](https://maas-openapi.wanjiedata.com/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, generated media links]

**Output Format:** [Plain text status messages plus a browser-opened result URL returned by the remote video service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured OpenClaw API key and starts an asynchronous Python worker for each accepted video prompt.]

## Skill Version(s):

1.2.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
