## Description:

Generates Chinese script content based on narrative pacing and dialogue mechanisms common in Jiang Wen films, including story synopses, character bios, scene outlines, and scene scripts with dialogue, action, and staging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patches429](https://clawhub.ai/user/patches429)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft Chinese screenplay material with structured synopsis, character, scene-outline, and scene-script outputs. It is intended for prompts about generating, revising, or pacing script scenes and dialogue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad scriptwriting prompts may be steered into a Jiang Wen-inspired Chinese screenplay style even when the user intended a different tone or language.

Mitigation: Ask for the desired language, tone, and stylistic direction when the user request is broad, and override the default style when the user specifies another direction.

Risk: Generated scenes could resemble existing film scenes or dialogue if a user requests close imitation.

Mitigation: Use the skill's originality constraint, avoid copying specific film scenes or lines, and review outputs for close resemblance before publication.

## Reference(s):

- [Examples reference](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/patches429/skills/giggle-generation-scripts)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text screenplay sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May output one complete scene at a time and ask for user confirmation before continuing to the next scene.]

## Skill Version(s):

0.0.10 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
