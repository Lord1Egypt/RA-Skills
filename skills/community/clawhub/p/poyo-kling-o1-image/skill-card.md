## Description:

Kling O1 image editing on PoYo via poyo.ai for reference-image editing, element-guided subject or object control, async task submission, polling, and webhook follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and optionally submit PoYo Kling O1 image-editing payloads with reference images, element descriptors, output settings, polling, and webhook guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, callback URLs, and generated image metadata may be sent to PoYo during use.

Mitigation: Use the skill only with inputs you are comfortable sharing with PoYo and the callback receiver; avoid confidential prompts, source images, callback URLs, and generated URLs unless that trust decision is explicit.

Risk: The skill requires a PoYo API key for live submissions.

Mitigation: Use a scoped PoYo key where possible, keep it in a server-side environment variable or secret manager, and avoid exposing it in browser code, public repositories, logs, screenshots, or chat output.

Risk: The submit script sends the contents of a local payload JSON file to PoYo.

Mitigation: Run the script only on payload files intentionally prepared for submission from a trusted shell.

## Reference(s):

- [PoYo Kling O1 Image model page](https://poyo.ai/models/kling-o1-image)
- [PoYo Kling O1 API docs](https://docs.poyo.ai/api-manual/image-series/kling-o1)
- [Local PoYo Kling O1 Image API reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-kling-o1-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON payloads and bash or curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model id, reference-image and element guidance, selected output settings, task_id from submissions, and polling or webhook next steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
