## Description:

Generates visually styled presentation decks with OpenAI gpt-image-2 from slide outlines or reference PPTX templates, including built-in styles, an HTML viewer, and a 16:9 PPTX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juneyaooo](https://clawhub.ai/user/juneyaooo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and presentation authors use this skill to turn a slide outline or reference PPTX template into image-backed decks for pitches, reports, lectures, and marketing presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Codex backend can delegate untrusted slide text to a full-auto Codex subprocess with broad local authority.

Mitigation: Use the default direct API or native image path when possible, and enable the Codex backend only after reviewing the slide content and local execution context.

Risk: Configured API endpoints can route image generation or vision analysis through unexpected services.

Mitigation: Review `OPENAI_BASE_URL` and `VISION_BASE_URL` before use, and keep credentials in a scoped `.env` rather than a project-wide environment file.

Risk: The legacy root `generate_ppt.py` contradicts the stated credential-scoping behavior.

Mitigation: Use `scripts/generate_ppt.py` as the active entry point and do not run the legacy root script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juneyaooo/skills/gpt-image2-ppt)
- [Artifact README](artifact/README.md)
- [English README](artifact/docs/README.en.md)
- [Install guide](artifact/docs/install.md)
- [OpenAI Images API guide](https://platform.openai.com/docs/guides/images)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts include PNG images, JSON prompts, an HTML viewer, and a 16:9 PPTX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports curated style selection, template-clone workflows, optional single-slide smoke tests, and output directories under the caller workspace.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
