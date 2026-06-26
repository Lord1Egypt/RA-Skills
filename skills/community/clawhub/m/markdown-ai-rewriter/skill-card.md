## Description: <br>
A Markdown rewriting skill that preserves document structure while using selectable AI providers to rewrite content and optionally generate images, video, or music. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content operators, and writers use this skill to rewrite existing Markdown while preserving headings, code blocks, tables, and media placement. It supports publishing workflows that need provider choice, controlled cost, and optional image, video, or music generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys and input Markdown may be sent to selected third-party model services. <br>
Mitigation: Configure only the provider API key needed for the task and avoid confidential Markdown unless the selected provider is approved for that data. <br>
Risk: Automatic activation and package loading are broader than the documentation clearly scopes. <br>
Mitigation: Review before installing, use trusted project directories, and require confirmation before rewrites or media generation where possible. <br>
Risk: The skill depends on a third-party npm package loaded from the local Node.js environment. <br>
Mitigation: Install the pinned package from a trusted source, keep automatic install and update disabled, and audit the referenced package source before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sipingme/markdown-ai-rewriter) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [npm package](https://www.npmjs.com/package/markdown-ai-rewriter) <br>
- [Source repository](https://github.com/sipingme/markdown-ai-rewriter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI-oriented text; generated media files may be created when image, video, or music options are enabled.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider API credentials and writes rewritten Markdown or generated media to user-selected output paths.] <br>

## Skill Version(s): <br>
1.2.5 (source: evidence release, SKILL.md frontmatter, config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
