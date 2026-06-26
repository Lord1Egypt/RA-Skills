## Description: <br>
Generate PPT documents using Python and python-pptx. No third-party API calls, fully open source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiangzhanyou](https://clawhub.ai/user/xiangzhanyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate local PowerPoint presentations from a title and structured slide content, including text and bullet lists, without third-party API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes a .pptx file to a user-specified path, which could overwrite an existing file if the path is reused. <br>
Mitigation: Choose a deliberate output folder and filename, and review the returned path before relying on the file. <br>
Risk: The script depends on python-pptx at runtime. <br>
Mitigation: Install python-pptx from a trusted package source and version before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiangzhanyou/openclaw-ppt-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [PowerPoint .pptx file with JSON status output from the generator script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and python-pptx; generated files are saved to a caller-provided output path or a timestamped default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
