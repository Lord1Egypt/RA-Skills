## Description: <br>
Packages H5 game projects into Apple iBook-compatible .wdgt widget ZIP archives, including directory normalization, resource path updates, Info.plist generation, thumbnail generation, and final ZIP packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onedream1985](https://clawhub.ai/user/onedream1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to package an existing H5 game project with index.html and web assets into an iBook Author widget bundle and ZIP archive. It helps prepare the widget directory, Info.plist, thumbnails, resource paths, package structure, and user-facing import guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaging helper can delete and recreate an existing matching .wdgt output folder if the widget name or output path is unsafe. <br>
Mitigation: Use a fresh output directory, choose a simple widget name with only letters, numbers, hyphens, or underscores, and check the resolved target path before running. <br>
Risk: The skill reads local project files and writes generated bundle and ZIP outputs. <br>
Mitigation: Run it only on projects and output locations you trust, then inspect the generated package before importing it into iBook Author. <br>


## Reference(s): <br>
- [iBook Widget Packer on ClawHub](https://clawhub.ai/onedream1985/ibook-widget-packer) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [pack_widget.py](artifact/pack_widget.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, XML and Python snippets, generated widget files, and a .wdgt.zip archive.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local H5 project directory, filesystem write access, Python3, and zip tooling; Pillow is optional for richer thumbnail generation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
