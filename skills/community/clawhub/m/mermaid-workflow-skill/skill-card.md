## Description:

Creates Mermaid diagram definition files, renders them to PNG with Mermaid CLI, and inserts the resulting image links into Markdown documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runmanfm-bit](https://clawhub.ai/user/runmanfm-bit)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and technical writers use this skill to create roadmap, architecture, flowchart, sequence, class, state, Gantt, and ER diagrams and place rendered PNGs into Markdown reports or documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The conversion workflow may run Chromium with --no-sandbox or --disable-setuid-sandbox for Mermaid rendering.

Mitigation: Render diagrams only in a disposable isolated container or VM, or use a sandbox-compatible Mermaid CLI setup without disabling Chromium sandboxing.

Risk: The converter can fall back to npx @mermaid-js/mermaid-cli, which may execute an unpinned npm package.

Mitigation: Install a pinned Mermaid CLI version locally with a lockfile and disable or review any automatic npx fallback before use.

Risk: Markdown insertion commands rewrite target Markdown files and can replace placeholders or section content.

Mitigation: Back up or version-control Markdown files before insertion and review diffs before publishing generated documentation.

Risk: Mermaid files supplied by other parties may contain untrusted content processed by the renderer.

Mitigation: Treat external .mmd files as untrusted input and process them only in an isolated environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/runmanfm-bit/skills/mermaid-workflow-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Example workflow](artifact/examples/example_workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples plus generated Mermaid definitions, PNG images, and Markdown image links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .mmd and .png files, generate Puppeteer configuration, and modify target Markdown files when insertion commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
