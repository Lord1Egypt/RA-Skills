## Description:

Group Director creates short SenseAudio videos from finalized Claw-prepared prompts for Feishu or Lark group chat scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when Claw has already prepared a final video prompt and needs a narrow execution layer to create a SenseAudio video task, poll until completion, and return a plain video URL or plain-text failure message.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable SenseAudio base URL can send the API key and finalized video prompts to an unintended endpoint.

Mitigation: Keep SENSEAUDIO_BASE_URL unset or set only to the real HTTPS SenseAudio host, and use scoped, rotatable API keys.

Risk: Finalized video prompts are sent to the external video provider.

Mitigation: Treat prompts as provider-bound data and avoid including sensitive content unless the runtime and provider use are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hei-maom/skills/group-director)
- [Provider notes](references/provider_notes.md)
- [Claw integration notes](references/integration_cn.md)
- [SenseAudio API endpoint](https://api.senseaudio.cn)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API Calls, Guidance]

**Output Format:** [Plain text or Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a task ID during creation, then a video URL or plain-text error after polling; Feishu/Lark responses should not include raw JSON.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
