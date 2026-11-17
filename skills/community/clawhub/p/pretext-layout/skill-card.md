## Description:

Integrate, debug, or prototype @chenglou/pretext for browser-based multiline text measurement and manual line layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[royhk920](https://clawhub.ai/user/royhk920)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to integrate, prototype, and debug @chenglou/pretext in browser-based applications that need cached multiline text measurement, height prediction, and manual line layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional scaffold script writes index.html and demo.mjs into the selected output directory.

Mitigation: Run the scaffold only in a disposable or empty directory and inspect generated files before adapting them.

Risk: Pretext measurements can be wrong when browser runtime, font loading, font value, line height, or white-space mode do not match the real UI.

Mitigation: Use a browser-backed runtime, wait for fonts when needed, read styles from the target UI, and verify representative multilingual, emoji, and narrow-width samples against live DOM output.

## Reference(s):

- [Browser Integration](references/browser-integration.md)
- [Usage Patterns](references/usage-patterns.md)
- [Caveats](references/caveats.md)
- [Portable Integration Patterns](references/project-examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code examples and optional scaffold commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a minimal browser demo scaffold containing index.html and demo.mjs when the optional scaffold script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
