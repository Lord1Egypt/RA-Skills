## Description: <br>
Install and wire HyperFrames registry blocks and components into compositions, including add-command usage, install locations, block sub-composition wiring, component snippet merging, and registry discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucas-kay8](https://clawhub.ai/user/lucas-kay8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install HyperFrames registry blocks and components, discover available registry items, and wire installed snippets or sub-compositions into project HTML/CSS/JS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wiring guidance may introduce incorrect or unsuitable edits to composition HTML, CSS, or JavaScript. <br>
Mitigation: Review generated snippets and project diffs, then run HyperFrames lint and preview checks before merging changes. <br>
Risk: The skill may suggest running HyperFrames commands or fetching public registry information. <br>
Mitigation: Run commands in the intended project directory and review installed registry files before relying on them. <br>


## Reference(s): <br>
- [Install Locations](references/install-locations.md) <br>
- [Wiring Blocks](references/wiring-blocks.md) <br>
- [Wiring Components](references/wiring-components.md) <br>
- [Registry Discovery](references/discovery.md) <br>
- [Demo HTML Convention](references/demo-html-pattern.md) <br>
- [HyperFrames Registry Manifest](https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json) <br>
- [HyperFrames Configuration Schema](https://hyperframes.heygen.com/schema/hyperframes.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, HTML, CSS, JavaScript, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend reading installed files, running HyperFrames commands, and editing composition files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
