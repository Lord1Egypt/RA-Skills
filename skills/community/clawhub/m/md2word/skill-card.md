## Description:

md2word converts Markdown into professionally formatted Word documents, with Chinese document presets for legal documents, service plans, academic papers, reports, and other formal materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Developers, document automation users, and agents use this skill to convert Markdown drafts into styled .docx files with presets for Chinese formal documents, including legal materials, service plans, academic papers, reports, and book-style output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown image links can trigger outbound HTTP or HTTPS requests, including requests to internal network addresses.

Mitigation: Convert only trusted Markdown, or run the skill in an environment without internal-network access when processing third-party documents.

Risk: Local image paths in Markdown can cause readable local files to be embedded into the generated DOCX.

Mitigation: Limit filesystem access to the intended document workspace and review Markdown inputs before conversion.

Risk: Untrusted SVG content is rendered by local tooling and may create parser or resource-exhaustion exposure.

Mitigation: Use trusted SVG content, keep renderer dependencies patched, and run conversions in a restricted environment for untrusted inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/md2word)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [Configuration reference](references/config-reference.md)
- [Style mappings](references/style-mappings.md)
- [Usage examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Files, Configuration]

**Output Format:** [DOCX Word document and optional YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Word documents may embed local images, downloaded external images, rendered Mermaid diagrams, rendered SVG content, tables, footnotes, and preset formatting.]

## Skill Version(s):

1.2.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
