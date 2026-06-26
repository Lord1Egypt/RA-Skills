## Description: <br>
Builds composable skill modules with hub-and-spoke loading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design, audit, and refactor agent skills into modular hub-and-spoke structures that manage token usage and keep documentation maintainable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect many documentation and governance files during repository audits. <br>
Mitigation: Run it in an appropriate repository workspace and request report-only mode when broad inspection is not desired. <br>
Risk: Documentation fixes may change skill guidance or repository standards. <br>
Mitigation: Review proposed diffs before accepting edits, especially for governance or deployment-facing documentation. <br>
Risk: Incorrect modularization advice could introduce misleading or incomplete skill guidance. <br>
Mitigation: Validate recommendations with the documented module validation workflow and human review before deployment. <br>


## Reference(s): <br>
- [Claude Night Market abstract plugin](https://github.com/athola/claude-night-market/tree/master/plugins/abstract) <br>
- [Nm Abstract Modular Skills on ClawHub](https://clawhub.ai/athola/nm-abstract-modular-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository documentation audits or edits; report-only mode can be requested.] <br>

## Skill Version(s): <br>
1.9.12 (source: ClawHub release metadata; artifact frontmatter: 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
