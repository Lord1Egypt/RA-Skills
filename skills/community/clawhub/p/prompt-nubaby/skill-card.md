## Description:

Nubaby prompt system for prompt augmentation, routers, dictionaries, dataset captions, prompt tags, compact prompts, video/storyboard prompt shaping, and structured visual tension expansion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurlin1979](https://clawhub.ai/user/arthurlin1979)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to expand short or vague image and video generation requests into structured prompts, tags, dataset captions, compact prompts, and storyboard-oriented prompt text before execution in a downstream ComfyUI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save arbitrary user prompt text as trusted system-level recipes through its learning function.

Mitigation: Require explicit approval, validation, provenance capture, and a deletion or rollback path before allowing recipe updates in shared or production workflows.

Risk: Prompt expansion for portrait, intimate, or school-aesthetic scenes can drift into unsafe or inappropriate visual framing.

Mitigation: Keep the documented adult-only and non-explicit constraints active, and review generated prompts before downstream image or video execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arthurlin1979/skills/prompt-nubaby)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text prompt guidance with structured tags, captions, negative prompts, and mode-specific parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local JSON recipe knowledge base when its learning function is invoked.]

## Skill Version(s):

1.1.0 (source: server release metadata; changelog top entry v1.1, released 2026-03-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
