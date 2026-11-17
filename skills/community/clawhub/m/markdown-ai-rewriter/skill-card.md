## Description:

Rewrites existing Markdown with AI while preserving document structure, with optional image, video, and music generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to rewrite, polish, de-duplicate, and restyle existing Markdown while preserving headings, code blocks, tables, and images. It can also request provider-backed image, video, or music generation for Markdown publishing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown content may be sent to externally configured AI provider endpoints.

Mitigation: Use only approved providers and endpoints, and avoid confidential Markdown unless the selected provider is approved for that data.

Risk: Custom base URLs may receive full document content.

Mitigation: Treat custom endpoints as sensitive destinations and approve them before use.

Risk: The skill loads the pinned npm package in-process from local node_modules locations.

Mitigation: Review the npm package and launcher behavior, pin dependencies exactly, and avoid running from untrusted project directories.

Risk: Auto-invocation could send documents to providers sooner than intended.

Mitigation: Disable or tightly scope auto-invocation for projects that contain sensitive or unreviewed Markdown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipingme/skills/markdown-ai-rewriter)
- [markdown-ai-rewriter npm package](https://www.npmjs.com/package/markdown-ai-rewriter)
- [markdown-ai-rewriter source repository](https://github.com/sipingme/markdown-ai-rewriter)
- [markdown-ai-rewriter skill repository](https://github.com/sipingme/markdown-ai-rewriter-skill.git)
- [Source audit reference](https://github.com/sipingme/markdown-ai-rewriter/blob/main/src/index.ts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, CLI status text, and command-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit feature flags such as --rewrite, --process-images, or --generate-video; output quality and structure preservation depend on the selected provider and prompt.]

## Skill Version(s):

1.2.5 (source: server release metadata, target metadata, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
