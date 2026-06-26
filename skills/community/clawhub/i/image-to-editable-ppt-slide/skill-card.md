## Description: <br>
Rebuild one or more reference images as visually matching editable PowerPoint slides using native shapes, text, fills, and layout instead of a flat screenshot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benjaminlee](https://clawhub.ai/user/benjaminlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to convert flowcharts, dashboards, infographics, process diagrams, and designed slide images into editable PPT/PPTX decks. It is intended for local reconstruction workflows where editable shapes, text, fills, and layout matter more than embedding a flat screenshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local reference images or specs and writes PPTX, JSON, and script outputs in the workspace. <br>
Mitigation: Use it only in workspaces where those local inputs and generated outputs are acceptable, and review generated files before keeping or sharing them. <br>
Risk: The workflow may run bundled Python helper scripts and may require python-pptx if it is not already installed. <br>
Mitigation: Review the included scripts before execution and install python-pptx only from a trusted package source. <br>
Risk: Editable slide reconstruction can introduce visual or textual differences from the source image. <br>
Mitigation: Perform at least one fidelity review pass and note any approximations before delivering the deck. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/benjaminlee/image-to-editable-ppt-slide) <br>
- [README](artifact/README.md) <br>
- [Examples](artifact/EXAMPLES.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python code, shell commands, JSON specs, and generated PPTX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PPTX, JSON spec, and helper script files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
