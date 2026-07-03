## Description: <br>
Auto-generate electrical CAD drawings from survey data and auto-audit against power codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[powerzzjohn](https://clawhub.ai/user/powerzzjohn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Electrical designers and engineers use this skill to turn survey data, sketches, or task briefs for 10kV-and-below power distribution projects into draft CAD drawings, inferred design parameters, equipment lists, and audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CAD and report files may be written to unintended locations or overwrite existing project outputs. <br>
Mitigation: Run the scripts only in an intended project workspace, choose an explicit output directory, and check for existing files before execution. <br>
Risk: Generated drawings, inferred design parameters, and audit reports may be incomplete or incorrect for a regulated electrical project. <br>
Mitigation: Treat outputs as draft engineering assistance and require qualified professional review against applicable company and national codes before use. <br>


## Reference(s): <br>
- [Drawing Symbols Reference](references/drawing_symbols.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Markdown, JSON, CSV, Shell commands, Guidance] <br>
**Output Format:** [DXF drawings, JSON design parameters, Markdown audit report, CSV equipment list, and ZIP package] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ezdxf and pyyaml; generated drawings and audit reports should be reviewed before engineering use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
