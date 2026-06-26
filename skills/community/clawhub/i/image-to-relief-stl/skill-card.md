## Description: <br>
Turns source images or multi-color mask images into 3D-printable bas-relief STL files by mapping colors or grayscale values to heights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajmwagar](https://clawhub.ai/user/ajmwagar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, makers, and 3D-printing workflows use this skill to convert flat-color or grayscale source images into printable bas-relief STL models. It supports palette-based height mapping, grayscale height mapping, and an optional vector preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional preview path can run unintended local Python code when given a crafted or externally controlled filename. <br>
Mitigation: Use only trusted image paths and avoid --preview-svg for unusual or externally controlled filenames until the preview filename handling is fixed. <br>
Risk: First use downloads Pillow into a cached local virtual environment. <br>
Mitigation: Install and run the skill in a controlled environment with approved package sources and network policy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ajmwagar/image-to-relief-stl) <br>
- [Publisher profile](https://clawhub.ai/user/ajmwagar) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [ASCII STL file with optional SVG preview and terminal path output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; optional preview generation requires potrace and mkbitmap; first use installs Pillow into a cached local virtual environment.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
