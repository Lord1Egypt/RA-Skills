## Description:

Provides guidance for rendering Mermaid diagrams as ASCII or Unicode art with the beautiful-mermaid package, including API usage, layout internals, supported diagram types, troubleshooting, and extension guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joe-rq](https://clawhub.ai/user/joe-rq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand, use, debug, or extend beautiful-mermaid's ASCII renderer for terminal-safe Mermaid diagram output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package installs or unversioned CDN examples can pull changing beautiful-mermaid contents.

Mitigation: Prefer pinned beautiful-mermaid versions and avoid the unversioned CDN example unless the package contents and integrity are trusted.

Risk: ASCII or Unicode rendering may degrade for long labels, dense diagrams, complex routing, nested subgraphs, or terminals without UTF-8 support.

Mitigation: Use the documented padding, ASCII mode, simplified diagrams, supported diagram types, and troubleshooting guidance before relying on rendered output.

Risk: The main documentation is primarily Chinese, which can make review harder for non-Chinese users.

Mitigation: Use translation or bilingual review before adopting guidance in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joe-rq/skills/mermaid-ascii-renderer)
- [Core Systems](references/core-systems.md)
- [Diagram Implementations](references/diagrams.md)
- [Usage and API](references/usage.md)
- [Examples](references/examples.md)
- [Theming](references/theming.md)
- [Unicode and ASCII Characters](references/characters.md)
- [Troubleshooting and Optimization](references/troubleshooting.md)
- [External References](references/resources.md)
- [beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid)
- [mermaid-ascii](https://github.com/AlexanderGrooff/mermaid-ascii)
- [Mermaid documentation](https://mermaid.js.org/intro/)
- [Box-drawing characters](https://en.wikipedia.org/wiki/Box-drawing_characters)
- [ASCII rendering research](https://alexharri.com/blog/ascii-rendering)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript, shell, Mermaid, and ASCII/Unicode text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal-oriented diagram output and implementation guidance; no hidden execution behavior was found in the skill.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
