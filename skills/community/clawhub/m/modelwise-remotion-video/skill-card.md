## Description:

Creates Remotion-based animated demo videos with reusable React animation components, scene transitions, video templates, and aspect-ratio presets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deerleo](https://clawhub.ai/user/deerleo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to create React and Remotion video compositions for product demos, title sequences, data visualizations, and animated social or presentation formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing dependencies and running Remotion can pull npm packages and start local services.

Mitigation: Use an isolated project or container and review or regenerate the lockfile against an approved npm registry before installation.

Risk: Unpinned npx commands and Remotion Studio/runtime behavior may modify project files or contact external services.

Mitigation: Prefer locally installed pinned binaries, review commands before execution, and restrict network or filesystem access where possible.

## Reference(s):

- [Remotion Video Skill Instructions](instructions.md)
- [Basic Usage Example](examples/basic-usage.md)
- [Title Animation Example](examples/title-animation.md)
- [Product Demo Example Data](examples/product-demo.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and TSX code snippets, JSON configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Remotion project files and commands to preview or render videos.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
