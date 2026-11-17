## Description:

Pi TUI - Terminal UI framework with differential rendering and synchronized output for flicker-free interactive CLIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build terminal UIs, interactive CLI apps, TUI editors, select lists, settings panels, terminal Markdown rendering, and inline terminal images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a normal but unpinned npm install instruction.

Mitigation: Pin a reviewed package version, use a lockfile, and inspect npm package scripts in an isolated or least-privileged environment before installation.

Risk: Terminal UI integrations can mis-handle raw-mode input, focus, or unsupported image-capable terminals.

Mitigation: Follow the documented Ctrl+C key handling and focus propagation guidance, and provide fallbacks for terminals that do not support inline image protocols.

## Reference(s):

- [Overlay System](artifact/references/overlays.md)
- [Built-in Component API](artifact/references/components.md)
- [Autocomplete & Key Detection](artifact/references/autocomplete.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill guidance; no files are generated unless the consuming agent applies the guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
