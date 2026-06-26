## Description: <br>
Deploys and explains five macOS Automator services for Finder workflows: PDF-to-JPG conversion, PNG renaming and conversion, image stitching, RAR extraction, and ordered image renaming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wang-junjian](https://clawhub.ai/user/wang-junjian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
macOS users and support or developer teams use this skill to install, use, or customize local Automator Quick Actions for file conversion, archive extraction, and batch image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact is a guide for local macOS Automator services; the referenced .workflow bundles are not included in the reviewed artifact. <br>
Mitigation: Inspect any .workflow bundles separately before copying them into ~/Library/Services/. <br>
Risk: The skill includes local shell commands that can copy, remove, chmod, and sync files under user-controlled paths. <br>
Mitigation: Test conversions, renames, extraction, and deletion commands on disposable files first, and back up existing Automator services before uninstall or sync steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wang-junjian/macos-automator-services) <br>
- [Apple Automator User Guide](https://support.apple.com/zh-cn/guide/automator/welcome/mac) <br>
- [Apple Terminal User Guide](https://support.apple.com/zh-cn/guide/terminal/welcome/mac) <br>
- [ImageMagick Documentation](https://imagemagick.org/script/) <br>
- [ImageMagick Command-line Tools](https://imagemagick.org/script/command-line-tools.php) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
