## Description:

Converts Markdown into presentation assets with smart pagination, layout selection, themes, and optional image search or generation for Slidev, HTML, or PPTX outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neutronstar238](https://clawhub.ai/user/neutronstar238)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presenters, and content authors use this skill to turn Markdown documents into structured presentation outputs with themes, layouts, speaker notes, and preview or export guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security review flags unsafe preview and export commands in the skill guidance.

Mitigation: Review generated shell commands before use and prefer a trusted, pinned local Slidev CLI dependency instead of running the generated npx slidew commands.

Risk: Auto-image mode may send document-derived search terms to external image services.

Mitigation: Disable auto-images or use local or approved assets for confidential Markdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neutronstar238/skills/md-to-ppt)
- [Artifact README](artifact/README.md)
- [Example Markdown template](artifact/templates/example.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown presentation files, CSS, README guidance, optional layout-plan JSON, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Slidev, HTML, or PPTX-oriented assets; auto-image mode can use external image search or generation.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
