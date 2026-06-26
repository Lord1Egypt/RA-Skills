## Description: <br>
Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lbbniu](https://clawhub.ai/user/lbbniu) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, update, validate, and package reusable agent skills with appropriate instructions, references, scripts, and assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can initialize or package directories chosen by the user, which may accidentally include private or unrelated files. <br>
Mitigation: Run scripts only on explicit workspace paths and inspect generated skill archives before publishing or sharing. <br>
Risk: Skill-building guidance can produce incomplete or misleading instructions if accepted without review. <br>
Mitigation: Review and validate generated skills before deployment, including frontmatter, bundled resources, and packaging contents. <br>


## Reference(s): <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/lbbniu/lbbniu-skill-creator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify skill files and package archives when its helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
