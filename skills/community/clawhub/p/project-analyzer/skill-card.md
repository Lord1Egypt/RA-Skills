## Description: <br>
Project Analyzer helps agents inspect software projects and generate SDD documentation covering requirements, architecture, detailed design, databases, APIs, and tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whiskeyforsun](https://clawhub.ai/user/whiskeyforsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze an existing codebase and produce structured software design documentation, including SRS, SAD, SDD, DBD, APID, and TSD documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local project files and can surface internal implementation details in generated documentation. <br>
Mitigation: Use it only with projects approved for local analysis and review generated documents before sharing them. <br>
Risk: Apifox integration may send generated API or OpenAPI content to a third-party service. <br>
Mitigation: Before using Apifox, inspect generated API content for secrets, internal endpoints, sample payloads, and credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whiskeyforsun/project-analyzer) <br>
- [Project Analyzer README](README.md) <br>
- [constraints.yaml](references/configs/constraints.yaml) <br>
- [SRS template](references/templates/01-srs.md) <br>
- [SAD template](references/templates/02-sad.md) <br>
- [DBD template](references/templates/04-dbd.md) <br>
- [APID template](references/templates/05-apid.md) <br>
- [TSD template](references/templates/06-tsd.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation files with supporting analysis and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local docs/sdd outputs by default and may generate API, database, architecture, requirements, and test design documentation.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact files also list 5.0.0 in SKILL.md and 1.0.0 in manifest.yaml/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
