## Description: <br>
Add accurate, publication-ready scale bars to microscopy images given pixel-to-unit calibration data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, imaging practitioners, and developers use this skill to add calibrated scale bars to microscopy images for publication figures or consistent batch annotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or untrusted calibration data can produce a misleading scale bar. <br>
Mitigation: Use trusted pixels-per-unit calibration or verified TIFF XResolution metadata and review the annotated output before publication. <br>
Risk: The local image-processing script reads and writes user-selected file paths, so accidental reads or overwrites are possible if paths are chosen carelessly. <br>
Mitigation: Keep input and output paths inside the intended workspace and choose explicit output filenames. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/microscopy-scale-bar-adder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command-line examples; script execution saves an annotated image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Pillow and trusted calibration data from TIFF metadata or a user-supplied pixels-per-unit value.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
