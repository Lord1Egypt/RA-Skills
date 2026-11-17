## Description:

Nano Banana 2 image generation and advanced editing on PoYo / poyo.ai via the PoYo generation API, including text-to-image, image-to-image, multi-reference workflows, and 1K, 2K, or 4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolhackboy](https://clawhub.ai/user/coolhackboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and submit PoYo Nano Banana 2 image generation or editing requests, choose the appropriate model, build request payloads, and report task IDs for later polling or webhook handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can expose the PoYo API key to local process inspection when the key is passed as a command-line argument.

Mitigation: Prefer supplying POYO_API_KEY through the environment, avoid using the helper on shared or heavily monitored machines, and review API-key billing or quota impact before installation.

Risk: Prompts, image URLs, and callback URLs are sent to PoYo during request submission.

Mitigation: Submit only prompts, image URLs, and callback URLs that the user is comfortable sending to PoYo.

## Reference(s):

- [PoYo Nano Banana 2 model page](https://poyo.ai/models/nano-banana-2)
- [PoYo Nano Banana 2 API docs](https://docs.poyo.ai/api-manual/image-series/nano-banana-2-new)
- [PoYo unified task status docs](https://docs.poyo.ai/api-manual/task-management/status)
- [ClawHub skill page](https://clawhub.ai/coolhackboy/skills/poyo-nano-banana-2)
- [API reference](artifact/references/api.md)
- [Frontend notes](artifact/references/frontend-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chosen model, summarized request parameters, reference-image usage, returned task_id, and polling or webhook next steps.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
