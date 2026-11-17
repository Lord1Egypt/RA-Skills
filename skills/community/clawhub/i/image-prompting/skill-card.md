## Description:

Helps agents craft still-image prompts for composition, consistent characters, edits, virtual try-on, and photoreal personas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pruna-ai](https://clawhub.ai/user/pruna-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to draft and check prompts for still-image generation, character sheets, image edits, virtual try-on, and upscaling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Related-skill installation commands are unpinned and can fetch changed content.

Mitigation: Review related skills before installing and pin versions where possible.

Risk: Avatar/video examples extend beyond still images; paid API calls may transmit prompts, image URLs, and voice text to Pruna.

Mitigation: Review examples before use, obtain consent for shared content, and confirm API costs and data handling before making calls.

## Reference(s):

- [ClawHub image-prompting release](https://clawhub.ai/pruna-ai/skills/image-prompting)
- [Prompt golden rules](references/prompt-golden-rules.md)
- [Image edit prompting](references/p-image-edit-prompting.md)
- [Virtual try-on prompting](references/p-image-try-on-prompting.md)
- [Image quality checklist](references/p-image-quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with prompts, checklists, and optional API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image prompts may specify composition, aspect ratio, reference-image roles, and model settings.]

## Skill Version(s):

1.0.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
