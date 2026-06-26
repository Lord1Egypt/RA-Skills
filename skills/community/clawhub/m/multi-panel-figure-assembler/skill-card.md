## Description: <br>
Assemble 6 sub-figures (A-F) into a high-resolution composite figure with consistent labels, padding, and publication-ready DPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research teams use this skill to combine exactly six existing image panels into a reproducible publication-ready composite figure with standardized labels, padding, borders, layout, and DPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency file includes an invalid or obsolete 'pil' package line and unpinned Pillow and numpy dependencies. <br>
Mitigation: Install only in a virtual environment or sandbox, remove the 'pil' line, and pin reviewed Pillow and numpy versions before use. <br>
Risk: The packaged script reads input paths and writes the output path supplied on the command line. <br>
Mitigation: Use only intended local image paths and approved output locations, preferably inside a workspace or sandbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/multi-panel-figure-assembler) <br>
- [Publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Markdown guidance] <br>
**Output Format:** [Composite image file plus concise Markdown status or fallback report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exactly six local image inputs and one output path; supports 2x3 or 3x2 layouts, DPI, label styling, padding, border, and background options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
