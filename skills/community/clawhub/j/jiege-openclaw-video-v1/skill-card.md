## Description:

This skill triggers an OpenClaw video-generation workflow from natural-language prompts and submits jobs to a third-party Veo-compatible video service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to request short video generation directly from chat using a Chinese prompt prefix. It is intended for automated video creation workflows that can tolerate asynchronous job handling and third-party API processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a configured OpenClaw API key and user prompt to a fixed third-party video service.

Mitigation: Use only a dedicated, low-scope API key for the WanjieData video service and avoid running it in profiles that contain unrelated provider keys.

Risk: Returned URLs may be opened automatically without user confirmation.

Mitigation: Require confirmation before opening returned links and validate result URLs before launching a browser.

Risk: Asynchronous jobs do not expose clear status or cancellation controls.

Mitigation: Provide job status, cancellation, and explicit endpoint disclosure before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liangshenghzj888-stack/skills/jiege-openclaw-video-v1)
- [Publisher profile](https://clawhub.ai/user/liangshenghzj888-stack)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, external URLs]

**Output Format:** [Plain text status message with asynchronous background execution and a browser-opened video result URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured OpenClaw API key; sends the user prompt to a fixed third-party video service and uses a lock file to avoid concurrent jobs.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
