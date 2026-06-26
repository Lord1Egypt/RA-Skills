## Description: <br>
Pi TUI is a terminal UI framework with differential rendering and synchronized output for flicker-free interactive CLIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building terminal UIs, interactive CLI apps, TUI editors, terminal select lists or settings panels, terminal Markdown rendering, overlays, autocomplete, and inline terminal images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applications using file-path autocomplete may expose local file names inside that application's terminal UI. <br>
Mitigation: Enable file-path autocomplete only where local file-name disclosure is acceptable, and review the npm package through the normal dependency process before use. <br>
Risk: Inline terminal images depend on Kitty or iTerm2 image protocol support and may fall back to placeholders on unsupported terminals. <br>
Mitigation: Test target terminals and provide acceptable non-image fallback behavior for users whose terminals do not support inline image rendering. <br>


## Reference(s): <br>
- [Overlay System](references/overlays.md) <br>
- [Built-in Component API](references/components.md) <br>
- [Autocomplete & Key Detection](references/autocomplete.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with TypeScript examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
