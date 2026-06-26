## Description: <br>
Generate SVG images from Graphviz DOT graphs using WebAssembly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guyoung](https://clawhub.ai/user/guyoung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert DOT graph descriptions into SVG diagrams without requiring a system Graphviz binary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an externally downloaded GitHub-hosted WASM component. <br>
Mitigation: Trust, verify, or pin the WASM file before use and keep execution inside the sandbox. <br>


## Reference(s): <br>
- [Graphviz WASM component](https://raw.githubusercontent.com/guyoung/wasm-sandbox-openclaw-skills/main/graphviz/files/graphviz_component.wasm) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with tool-call parameters and SVG output from the sandboxed renderer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns SVG generated from the DOT graph string passed to the WASM sandbox.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
