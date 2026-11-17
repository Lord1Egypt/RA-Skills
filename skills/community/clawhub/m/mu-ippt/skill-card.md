## Description:

Creates and edits PowerPoint presentations across from-scratch deck generation, technical diagrams, consulting templates, and existing-deck editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, business users, and presentation authors use this skill to plan, generate, convert, validate, and edit professional PowerPoint decks from documents, URLs, Markdown, plain text, diagrams, or existing PPTX files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document and Office archive imports can expose the agent environment to unsafe archive extraction or malicious user-provided files.

Mitigation: Run conversions in an isolated workspace, avoid untrusted Office archives, scan inputs before use, and keep generated outputs separate from sensitive files.

Risk: URL conversion can fetch arbitrary network locations, including internal or private URLs.

Mitigation: Restrict network egress, allowlist intended public URLs, and avoid converting private or internal network resources.

Risk: Image generation workflows rely on provider API keys and trusted provider endpoints.

Mitigation: Use provider-specific keys only for trusted endpoints, scope credentials narrowly, and do not include secrets in prompts, documents, or generated artifacts.

Risk: Unpinned dependencies can change behavior or security posture during installation.

Mitigation: Pin and review dependencies before installation in production or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/muippt/skills/mu-ippt)
- [FAQ](docs/faq.md)
- [SVG Pipeline Tools](scripts_ppt/docs/svg-pipeline.md)
- [Source Conversion Tools](scripts_ppt/docs/conversion.md)
- [Image Generation](scripts_ppt/docs/image.md)
- [Project Management](scripts_ppt/docs/project.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown planning and instructions with code blocks, plus generated SVG, PPTX, and support files when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Multi-page decks require workflow routing and user confirmation; generated PPTX outputs are expected to pass visual verification before delivery.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
