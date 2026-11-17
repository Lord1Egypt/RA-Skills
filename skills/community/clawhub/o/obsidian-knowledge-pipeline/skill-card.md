## Description:

Turns URL articles into structured Obsidian knowledge-base entries through a seven-step workflow for fetching, saving raw content, generating images, classifying, compiling wiki nodes, and adding graph links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tracky2009](https://clawhub.ai/user/tracky2009)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base operators use this skill to have an agent convert online articles into Obsidian raw notes, illustrated wiki nodes, classifications, backlinks, and Clippings copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch external web content and use external image-generation services, which may expose source URLs, article text, or prompts outside the local vault.

Mitigation: Avoid confidential URLs unless external fetching and image generation are acceptable, and review the configured image-generation path before running the workflow.

Risk: The workflow can make persistent changes across an Obsidian vault, including raw notes, image mappings, compiled wiki nodes, backlinks, and Clippings content.

Mitigation: Set OBSIDIAN_VAULT_PATH to a test vault first, review planned backlink and Clippings changes, and run against important vaults only after approval.

Risk: Image generation may require DASHSCOPE_API_KEY when using the Wan2.7 path.

Mitigation: Provide credentials only through environment variables and do not embed API keys in skill files, notes, templates, or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tracky2009/skills/obsidian-knowledge-pipeline)
- [Pipeline workflow](artifact/pipeline.md)
- [Classification and wiki standards](artifact/classification.md)
- [Image mapping rules](artifact/image-mapping.md)
- [Raw article template](artifact/templates/raw-article.md)
- [Wiki node template](artifact/templates/wiki-node.md)
- [Mapping entry template](artifact/templates/mapping-entry.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and templates with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces raw article notes, generated image files, mapping records, compiled wiki nodes, backlinks, and Clippings copies within an Obsidian vault.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
