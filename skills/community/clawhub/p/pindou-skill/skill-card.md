## Description: <br>
Generates printable perler and pixel-bead pattern assets from a photo or text description, including a color-coded grid and purchase list. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ciawevy](https://clawhub.ai/user/ciawevy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn photos or text prompts into printable bead-pattern files, color codes, and a bill of materials for physical perler-style projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials may be exposed if users place real keys directly in source files. <br>
Mitigation: Use environment variables, CLI-provided secrets, or local untracked configuration instead of committing or sharing edited scripts. <br>
Risk: Photos and prompts may be sent to the configured image provider or relay endpoint. <br>
Mitigation: Use a trusted endpoint and avoid uploading private or sensitive images unless that data sharing is acceptable. <br>
Risk: The release has a suspicious security verdict from the authoritative scan evidence. <br>
Mitigation: Review the skill before installation, run it in a constrained environment, and confirm endpoint and credential handling before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ciawevy/pindou-skill) <br>
- [OpenAI Images API documentation](https://platform.openai.com/docs/guides/images) <br>
- [MARD 221 palette](palettes/mard_221.csv) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and generated image, SVG, and CSV file outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected generated artifacts include pattern.png, pattern.svg, bom.csv, grid.json, and intermediate prompt/spec files in an output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
