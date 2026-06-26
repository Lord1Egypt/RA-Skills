## Description: <br>
Reviews the permissions required by a skill, script, or workflow and proposes least-privilege alternatives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and automation maintainers use this skill to summarize permission footprints, identify excessive permissions, and prepare least-privilege review checklists before acting on scripts, skills, or workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inputs may include sensitive script details, paths, permissions, or operational context. <br>
Mitigation: Provide redacted inputs where possible and include only the material needed for the permission review. <br>
Risk: The helper can write a report file when an output path is supplied. <br>
Mitigation: Choose output paths deliberately, or use stdout or dry-run behavior when reviewing sensitive material. <br>
Risk: Permission recommendations can be incomplete if the provided environment or workflow details are incomplete. <br>
Mitigation: Review the draft, resolve pending confirmation items, and validate changes before applying them to any system. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/permission-footprint-reviewer) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Structured Markdown or JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print to stdout or write a local report file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
