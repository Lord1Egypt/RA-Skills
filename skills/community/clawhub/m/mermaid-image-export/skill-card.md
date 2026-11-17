## Description:

Exports Mermaid diagrams as PNG, SVG, or PDF images using mermaid-cli for documentation, presentations, print materials, and web embedding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation authors use this skill to convert Mermaid diagram source into publication-ready image files and to batch-export diagrams for docs, slides, web pages, and print materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe setup guidance can lead users to run shell-based installation commands without review.

Mitigation: Review setup commands first, avoid curl or wget pipe-to-shell instructions, and prefer a local pinned mermaid-cli dependency over global npm installation.

Risk: The batch export wrapper can run unintended local commands when given untrusted filenames or arguments.

Mitigation: Use the Python exporter for untrusted inputs, quote and validate filenames, and avoid the shell wrapper unless arguments come from a trusted source.

Risk: PDF and browser rendering depend on Puppeteer and Chrome or Chromium, increasing local execution exposure.

Mitigation: Run rendering in an isolated low-privilege environment and keep the browser and mermaid-cli dependencies pinned and updated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smallnest/skills/mermaid-image-export)
- [Overview](references/overview.md)
- [Installation Guide](references/installation.md)
- [Usage Guide](references/usage.md)
- [Format Specifications](references/formats.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated image files are PNG, SVG, or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch processing, Mermaid themes, custom CSS, custom configuration, dimensions, scaling, and background color settings.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
