## Description: <br>
Advanced JLC EDA / EasyEDA circuit design agent for schematic and PCB-ready work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboabw](https://clawhub.ai/user/boboabw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and electronics engineers use this skill to design, draw, review, and automate JLC EDA / EasyEDA schematics and PCB-ready circuit work with real JLC/LCSC parts and documented verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local EasyEDA bridge can execute code in an open EasyEDA session and mutate real projects. <br>
Mitigation: Use the bridge only for trusted local sessions, keep it off shared or exposed networks, stop it when finished, and require explicit confirmation before edits, deletes, file writes, or manufacturing/order workflows. <br>
Risk: EDA automation can affect the wrong project or document if the active EasyEDA context is not verified. <br>
Mitigation: Confirm the active project, document type, and target window before schematic or PCB operations, then verify placed components, nets, and DRC-relevant checks after changes. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/boboabw/jlc-eda-drawing) <br>
- [Bridge and API](references/bridge-api.md) <br>
- [Design Standards](references/design-standards.md) <br>
- [Parts Strategy](references/parts-strategy.md) <br>
- [Circuit Blocks](references/circuit-blocks.md) <br>
- [EDA Code Patterns](references/eda-code-patterns.md) <br>
- [PCB Workflow](references/pcb-workflow.md) <br>
- [Examples](references/examples.md) <br>
- [EasyEDA API Quick Reference](references/easyeda-api-reference/_quick-reference.md) <br>
- [EasyEDA Official Guides](references/easyeda-official-guides/index.md) <br>
- [EasyEDA API Package](https://image.lceda.cn/files/easyeda-api.zip) <br>
- [Run API Gateway Extension](https://ext.lceda.cn/item/oshwhub/run-api-gateway) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JavaScript snippets, shell commands, configuration steps, and EDA workflow guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide or perform EasyEDA actions through an available local bridge; project-changing actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
