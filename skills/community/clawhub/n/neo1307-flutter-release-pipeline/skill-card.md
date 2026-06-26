## Description: <br>
Build and package Flutter Android release artifacts (APK/AAB), collect outputs into a single folder, and produce a short release checklist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to build Flutter Android APK or AAB releases, collect release artifacts, and produce a concise checklist for sharing or Play Store preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill references a project-local PowerShell script that was not included in the reviewed artifact. <br>
Mitigation: Inspect scripts/flutter_release.ps1 in the target project before execution and confirm it only performs the intended Flutter release build and artifact collection steps. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and release checklist text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include artifact paths, file sizes, SHA256 hashes, build errors, and suggested fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
