## Description: <br>
Creates and maintains a standardized project guide system with start.md and guide/ documentation for initialization, changelog and pitfalls updates, and agent context recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RevolGMPHL](https://clawhub.ai/user/RevolGMPHL) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project maintainers use this skill to create a repeatable documentation structure for projects, keep changelogs and pitfalls current, and help agents recover project context in later sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and writes local project documentation files, so it can overwrite or change start.md and guide/ content if pointed at the wrong project root. <br>
Mitigation: Confirm the project root before running scripts, review generated Markdown changes, and avoid --force unless replacing existing documentation is intentional. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/RevolGMPHL/guide-creator) <br>
- [Guide system specification](references/guide-spec.md) <br>
- [Guide template](references/templates/guide-template.md) <br>
- [Start template](references/templates/start-template.md) <br>
- [Changelog template](references/templates/changelog-template.md) <br>
- [Pitfalls template](references/templates/pitfalls-template.md) <br>
- [Sub-document templates](references/templates/sub-doc-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and guidance with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project documentation scaffolds and update entries under start.md and guide/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
