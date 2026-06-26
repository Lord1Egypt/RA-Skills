## Description: <br>
Convert PowerPoint PPTX files to high-quality JPG or PNG images with customizable DPI while preserving slide proportions and orientation on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leodai12123](https://clawhub.ai/user/Leodai12123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to convert slide decks into JPG or PNG image files for publishing, review, or downstream processing. It is intended for Windows environments with Microsoft PowerPoint and pywin32 available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PowerPoint opens the presentation locally during export. <br>
Mitigation: Convert only trusted presentations and run the tool in an environment appropriate for handling those files. <br>
Risk: The converter depends on Windows, Microsoft PowerPoint, and pywin32. <br>
Mitigation: Confirm those dependencies are available before use and install pywin32 only from a trusted package source. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Leodai12123/pptx-to-image) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [JPG or PNG image files plus console progress text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Windows, Microsoft PowerPoint, and pywin32; accepts input path, output folder, DPI, image format, and JPG quality options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, and documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
