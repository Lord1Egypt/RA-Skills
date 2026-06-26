## Description: <br>
Generate technical engineering mechanics sketches, including beams, supports, forces, moments, dimensions, and coordinate systems, as PDF, PNG, or SVG using the MechanicsSketches Python library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MatthiasHBusch](https://clawhub.ai/user/MatthiasHBusch) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, engineers, and technical educators use this skill to create free-body diagrams, structural sketches, and mechanical engineering figures from Python or JSON workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the MechanicsSketches library directly from GitHub can reduce build reproducibility if the upstream dependency changes. <br>
Mitigation: Pin or review the GitHub dependency before installation when reproducible builds are required. <br>
Risk: The helper script reads a user-specified JSON file and writes to a user-specified output path, which can overwrite an existing file at that location. <br>
Mitigation: Provide only intended JSON inputs and choose output paths where creating or replacing a file is acceptable. <br>


## Reference(s): <br>
- [MechanicsSketches API Reference](references/api_reference.md) <br>
- [MechanicsSketches GitHub repository](https://github.com/MatthiasHBusch/MechanicsSketches) <br>
- [ClawHub skill page](https://clawhub.ai/MatthiasHBusch/mechanics-sketches) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PDF, PNG, JPG, or SVG sketch files when the helper script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and changelog, released 2026-02-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
