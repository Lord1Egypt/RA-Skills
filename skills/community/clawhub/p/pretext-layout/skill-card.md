## Description: <br>
Integrate, debug, or prototype @chenglou/pretext for browser-based multiline text measurement and manual line layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[royhk920](https://clawhub.ai/user/royhk920) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate @chenglou/pretext into browser-based text measurement, virtualization, and custom canvas or SVG layout workflows. It helps them choose APIs, align measurement inputs with real UI styles, and debug font, white-space, emoji, bidi, and browser runtime constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the optional browser demo scaffold can create or overwrite index.html and demo.mjs in the selected output directory. <br>
Mitigation: Run the scaffold only in a disposable or intended project directory, then review generated files before reuse. <br>
Risk: Direct runtime use is unsupported in pure Node or CLI environments unless a compatible canvas or DOM-backed environment is available. <br>
Mitigation: Confirm browser, OffscreenCanvas, or DOM canvas support before relying on Pretext measurements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/royhk920/pretext-layout) <br>
- [Browser Integration](references/browser-integration.md) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Caveats](references/caveats.md) <br>
- [Portable Integration Patterns](references/project-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code examples and optional generated browser demo files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, node, npm, and python3 when using the bundled scaffold script.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
