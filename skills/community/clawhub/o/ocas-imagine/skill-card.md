## Description:

Imagine is an art-direction engine for text-to-image generation that separates reusable style prompts from changing content prompts to keep image series aesthetically consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

Developers, artists, and creative teams use Imagine to generate text-to-image prompts and images with consistent visual style, extract reusable style prompts from reference images, and manage named styles for image series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes a silent self-update path that can pull remote changes and discard local repository changes without clear user consent.

Mitigation: Disable or remove the updater unless an operator explicitly approves update behavior, and preserve local work before any update is run.

Risk: Prompts, image references, and generated image locations may be written into journals, history, and evidence records.

Mitigation: Avoid sensitive prompts and private image references unless the deployment's journal storage, retention, and access controls are acceptable.

Risk: Image generation depends on the active conversation model being able to emit image attachments.

Mitigation: Confirm text-to-image capability in the runtime before generation and report degraded mode instead of routing to unapproved fallback providers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/indigokarasu/skills/ocas-imagine)
- [Generation Routing Reference](references/api_reference.md)
- [Style Prompt Guide](references/style_prompt_guide.md)
- [Default Styles Library](references/default_styles.md)
- [Imagine Journal Schema](references/journal.md)
- [Imagine Self-Update Procedure](references/self-update-imagine.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Markdown guidance with structured JSON art-direction records, generated image URLs or file paths, and journal files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generation history, evidence, styles, and journals under the skill's configured agent data directories.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata and changelog report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
