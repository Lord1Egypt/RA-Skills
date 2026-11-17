## Description:

Helps agents prepare, submit, and follow up on PoYo Wan 2.7 video generation and editing tasks through the PoYo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose the correct Wan 2.7 workflow, assemble request payloads, submit trusted payloads, and plan polling or webhook follow-up for PoYo video jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PoYo API keys could be exposed through logs, chat, browser code, screenshots, or public repositories.

Mitigation: Keep POYO_API_KEY in server-side environment variables or a backend secret manager, and avoid echoing it in outputs.

Risk: Private prompts, media URLs, audio, or callback URLs may be shared with PoYo when tasks are submitted.

Mitigation: Submit sensitive prompts, media, audio, or callback URLs only when the user trusts PoYo and the callback receiver.

## Reference(s):

- [PoYo Wan 2.7 Video API Reference](references/api.md)
- [PoYo Wan 2.7 Video Model Page](https://poyo.ai/models/wan-2-7-video)
- [PoYo Wan 2.7 Video API Docs](https://docs.poyo.ai/api-manual/video-series/wan-2-7-video)
- [ClawHub Skill Page](https://clawhub.ai/coolhackboy/skills/poyo-wan-2-7-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload examples and bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected model id, workflow type, request payload or parameter summary, task_id after submission, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
