## Description:

Helps agents prepare and optionally submit PoYo Runway Gen-4.5 video generation requests for text-to-video or single-image guided video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to construct Runway Gen-4.5 payloads for PoYo, submit prepared video-generation jobs when explicitly requested, and guide polling or webhook follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials, private prompts, private image URLs, or callback URLs could be exposed if included in logs, browser code, public repositories, screenshots, or chat output.

Mitigation: Keep POYO_API_KEY server-side, review payloads before submission, and avoid sending confidential prompts, private images, or sensitive callback URLs unless PoYo and the callback receiver are trusted.

Risk: Prepared payloads may submit content to PoYo's external API when the helper script is run.

Mitigation: Make live API calls only after explicit user approval from a trusted shell and verify the JSON payload before submission.

## Reference(s):

- [PoYo Runway Gen-4.5 model page](https://poyo.ai/models/runway-gen-4-5)
- [PoYo Runway Gen-4.5 API docs](https://docs.poyo.ai/api-manual/video-series/runway-gen-4-5)
- [PoYo API key page](https://poyo.ai/dashboard/api-key)
- [Bundled PoYo API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-runway-gen-4-5)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and bash or curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, request mode, duration, aspect ratio, reference-image use, task id, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
