## Description: <br>
一键生成项目介绍页，支持本地编辑和长图导出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kunyashaw](https://clawhub.ai/user/kunyashaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scan a local project directory, render a project introduction page, and export a long screenshot for sharing or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the project directory provided by the user and may include project metadata in generated or opened HTML. <br>
Mitigation: Run it only on project directories whose contents are appropriate to summarize, and review generated HTML before sharing. <br>
Risk: The security review flags the remote repository clone mode because user input can reach a shell command. <br>
Mitigation: Avoid using the --git or remote-repository mode until clone execution uses a safe argument-array API with URL validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kunyashaw/project-intro-generator) <br>
- [Demo video](https://www.youtube.com/watch?v=6ZRcgbdZSXw) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands] <br>
**Output Format:** [HTML file, PNG image, and text paths or CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read the target project directory and write generated HTML/PNG outputs to that project or requested output paths.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
