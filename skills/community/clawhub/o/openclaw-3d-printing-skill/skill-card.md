## Description: <br>
Create parametric 3D-printable parts and enclosures with CadQuery, export STL or 3MF files, render review previews, and iterate on fit, tolerances, and printability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antoniosilveira](https://clawhub.ai/user/antoniosilveira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and makers use this skill to design functional 3D-printable parts, gather fit requirements, generate CadQuery model code, export STL or 3MF files, render previews, and provide concise print recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and model execution can run local Python code with broad access to the user's environment. <br>
Mitigation: Review the skill before installing, use an isolated Python environment, and run only CadQuery model scripts that were created or reviewed by the user. <br>
Risk: Remote installer commands can execute unreviewed code if copied directly into a shell. <br>
Mitigation: Verify installer sources and avoid piping remote installer output directly to a shell unless the source is trusted. <br>
Risk: Generated parts can have printability or fit issues such as weak walls, poor clearances, non-watertight meshes, or unsupported overhangs. <br>
Mitigation: Use the bundled design review checklist, strict mesh validation, previews, and conservative FDM defaults before relying on printed parts. <br>


## Reference(s): <br>
- [Design Review](references/design-review.md) <br>
- [Requirements](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline code blocks and generated STL, 3MF, PNG, or Python files when modeling is performed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include model paths, preview image paths, key dimensions, slicer settings, orientation guidance, and fit or support warnings.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
