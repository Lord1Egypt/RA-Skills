## Description: <br>
Converts PowerPoint files on macOS into per-slide PNG screenshots and thumbnail contact sheets with configurable DPI and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxm8023](https://clawhub.ai/user/zhaoxm8023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content teams on macOS use this skill to generate slide screenshots and thumbnail grids from a local PowerPoint file after configuring paths and dependencies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configuration asks for WeChat app credentials that the code does not use or protect. <br>
Mitigation: Do not provide real WeChat app secrets unless the publisher clarifies the need and adds secure handling guidance; keep secrets out of shared config files, screenshots, logs, and version control. <br>
Risk: The tool runs local document conversion commands against user-provided PowerPoint content. <br>
Mitigation: Review and edit the configuration before execution, use trusted local files, and verify generated outputs before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoxm8023/ppt2png) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [PNG image files with local configuration and command-line progress output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local LibreOffice, Ghostscript, Pillow, and a configured PowerPoint file path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
