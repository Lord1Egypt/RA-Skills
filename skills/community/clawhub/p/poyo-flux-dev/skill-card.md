## Description:

Poyo Flux Dev helps agents prepare, validate, and optionally submit PoYo FLUX Dev image-generation or single-image editing requests through the documented PoYo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to build PoYo FLUX Dev text-to-image or single-image editing payloads, check required request fields, and explain polling or webhook follow-up. With explicit user approval and a server-side POYO_API_KEY, it can submit a reviewed JSON payload through the bundled shell helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: POYO_API_KEY could be exposed if placed in browser code, logs, screenshots, chat output, or public repositories.

Mitigation: Keep POYO_API_KEY in a server-side environment variable or secret manager and send it only in the PoYo Authorization header.

Risk: Confidential prompts, private source-image URLs, or private callback URLs could be sent to PoYo or a callback receiver.

Mitigation: Avoid confidential inputs unless the user trusts PoYo and the callback receiver, and review payload JSON before submission.

Risk: A live submission could transfer data or start an unintended image-generation task.

Mitigation: Run the bundled submission helper only after explicit user approval and only against the documented PoYo submit endpoint.

Risk: A submitted source image may be outside the user's processing rights.

Mitigation: Confirm the user has the right to process the source image before preparing or submitting an editing request.

## Reference(s):

- [PoYo FLUX Dev API Reference](references/api.md)
- [PoYo FLUX Dev Model Page](https://poyo.ai/models/flux-dev)
- [PoYo FLUX Dev API Docs](https://docs.poyo.ai/api-manual/image-series/flux-dev)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a PoYo task_id after an approved live submission; otherwise output is guidance and request material only.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
