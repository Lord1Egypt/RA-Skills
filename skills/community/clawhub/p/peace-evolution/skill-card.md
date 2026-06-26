## Description: <br>
Peace Evolution reviews and iterates a Peace Seeds HTML game through a jury-review workflow, applies feedback to generate a new version, and can notify the user through Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxNd](https://clawhub.ai/user/kukuxNd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and game creators use this skill to review a Peace Seeds HTML game across art, performance, security, testing, and cultural criteria, then generate an improved version. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates on Peace Seeds HTML files under /root/.openclaw/workspace/peace*.html and may create a new version. <br>
Mitigation: Confirm the intended file scope before use and review the generated HTML before sharing or relying on it. <br>
Risk: The workflow depends on a jury-review process that can produce subjective or incorrect improvement recommendations. <br>
Mitigation: Use a trusted review process and manually check proposed changes against the project goals. <br>
Risk: Feishu notifications may send generated output to an unintended account or recipient. <br>
Mitigation: Verify the Feishu destination before enabling notifications. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kukuxNd/peace-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown review notes with generated HTML file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May iterate up to 3 rounds and send a Feishu notification when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
