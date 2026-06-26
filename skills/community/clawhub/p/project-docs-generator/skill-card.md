## Description: <br>
Analyzes a codebase and helps an agent generate a tailored documentation system with project overview, architecture, module, API, workflow, and PlantUML guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect a project, identify its technology stack and structure, and create documentation plans and starter files for onboarding, architecture, API, module, and workflow documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can accidentally include secrets, internal endpoints, or confidential architecture details. <br>
Mitigation: Review generated files before committing or sharing them, and keep secrets and sensitive internal details out of documentation. <br>
Risk: The skill can write starter documentation files into a target project. <br>
Mitigation: Run it only on projects intended for documentation and inspect file diffs before accepting changes. <br>
Risk: Web-search prompts for unfamiliar frameworks or best practices could expose private repository names or internal architecture details. <br>
Mitigation: Use generic technology terms for searches and avoid private names, internal endpoints, or confidential design details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leonardo-lb/project-docs-generator) <br>
- [Technology detection guide](references/tech-detection.md) <br>
- [Documentation structure guide](references/doc-structure.md) <br>
- [PlantUML diagram patterns](references/diagram-patterns.md) <br>
- [PlantText](https://www.planttext.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, PlantUML diagrams, JSON analysis, shell commands, and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create docs/ files and analyze project metadata; review generated content before committing or sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
