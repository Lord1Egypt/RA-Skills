## Description:

Convert Markdown files to HTML similar to `marked.js`, `pandoc`, `gomarkdown/markdown`, or similar tools; or writing custom script to convert markdown to html and/or working on web template systems like `jekyll/jekyll`, `gohugoio/hugo`, or similar web templating systems that utilize markdown documents, converting them to html.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert Markdown documents into HTML, generate documentation pages, preview rendered Markdown, and work with Markdown-driven static site or templating systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML from untrusted Markdown can carry unsafe content into a browser or published site.

Mitigation: Sanitize rendered HTML before display or publication, especially when source Markdown is user supplied.

Risk: Broad setup and persistent configuration examples can affect local or project environments.

Mitigation: Prefer project-local, pinned dependencies and review global installs or persistent config before applying commands.

Risk: Static-site server examples can expose local content if bound to a public interface.

Mitigation: Keep development servers on localhost unless remote access is intentional and appropriately controlled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jhauga/skills/markdown-to-html-converter)
- [marked](https://github.com/markedjs/marked)
- [Pandoc](https://github.com/jgm/pandoc)
- [gomarkdown/markdown](https://github.com/gomarkdown/markdown)
- [Jekyll](https://github.com/jekyll/jekyll)
- [Hugo](https://github.com/gohugoio/hugo)
- [Basic Markdown to HTML](references/basic-markdown-to-html.md)
- [Code Blocks to HTML](references/code-blocks-to-html.md)
- [Collapsed Sections to HTML](references/collapsed-sections-to-html.md)
- [Tables to HTML](references/tables-to-html.md)
- [Mathematical Expressions to HTML](references/writing-mathematical-expressions-to-html.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce HTML snippets, CLI commands, Node.js, Go, Ruby, YAML, and static-site configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
