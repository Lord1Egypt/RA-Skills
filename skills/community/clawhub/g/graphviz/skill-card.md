## Description:

Generate SVG images from Graphviz DOT graph descriptions using a WebAssembly Graphviz component.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyoung](https://clawhub.ai/user/guyoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert DOT graph descriptions into display-ready SVG diagrams without requiring a local Graphviz binary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an unverified WebAssembly file from a mutable third-party GitHub URL.

Mitigation: Review the WebAssembly component before installation and prefer a bundled or immutable component with a published SHA-256 or signature check.

Risk: Broad activation could cause the skill to run outside explicit Graphviz or DOT-to-SVG requests.

Mitigation: Limit use to clear Graphviz, DOT, SVG, flowchart, or DOT-to-SVG rendering requests.

## Reference(s):

- [ClawHub Graphviz Skill](https://clawhub.ai/guyoung/skills/graphviz)
- [Graphviz WebAssembly Component URL](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/graphviz/files/graphviz_component.wasm)

## Skill Output:

**Output Type(s):** [Code, Text]

**Output Format:** [SVG XML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The SVG is produced by the WebAssembly component on stdout from a DOT graph string argument.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
