## Description: <br>
Generate beautiful, professional GitHub README files for your projects with multiple templates, languages, and customization options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and project maintainers use this skill to generate a ready-to-edit GitHub README for a project, including common sections such as badges, installation, usage, contributing, license, and author details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes README.md in the current working directory and can overwrite an existing README. <br>
Mitigation: Run it only in the intended project directory after backing up or committing any existing README.md. <br>
Risk: Documented options such as --output and --lang may not match the shell script behavior. <br>
Mitigation: Check the generated output before publishing and verify option behavior before relying on non-default usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/github-readme-generator) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Generator script](artifact/github-readme-generator.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text] <br>
**Output Format:** [Markdown file plus terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes README.md in the current working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/_meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
