## Description:

Use PoYo AI Hailuo 02 for prompt-optimized video generation and image-to-video workflows with the documented PoYo generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare PoYo Hailuo 02 video-generation requests, choose between standard and pro model variants, submit jobs, and retain task IDs for status polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, callback URLs, and job metadata are sent to PoYo during normal use.

Mitigation: Review data before submission and avoid private or internal image and callback URLs unless sharing them with PoYo is acceptable.

Risk: The helper script can expose the API key and submitted payload through command-line arguments or process inspection.

Mitigation: Prefer the POYO_API_KEY environment variable, avoid passing secrets as command-line arguments, and harden or replace the script before sensitive use.

## Reference(s):

- [PoYo Hailuo 02 model page](https://poyo.ai/models/hailuo-02)
- [PoYo Hailuo 02 API docs](https://docs.poyo.ai/api-manual/video-series/hailuo-02)
- [PoYo Hailuo 02 OpenAPI JSON](https://docs.poyo.ai/api-manual/video-series/hailuo-02.json)
- [PoYo task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [Local API reference](references/api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the selected model id, payload summary or final payload, reference-image status, returned task_id, and next polling or webhook step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
