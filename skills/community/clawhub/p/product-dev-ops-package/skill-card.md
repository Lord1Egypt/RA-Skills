## Description: <br>
A product, development, and operations collaboration workflow that guides an agent through product manager, architect, development assistant, and operations manager roles from requirements discovery through release archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scubiry-glitch](https://clawhub.ai/user/scubiry-glitch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, engineering, and operations teams use this skill to structure AI-assisted project intake, requirements discussion, API-first planning, implementation follow-up, operational readiness, and release archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create, move, or update workspace project documents during start and archive flows. <br>
Mitigation: Confirm the target workspace and review planned file changes before using /start, /开工, /archive, or /归档. <br>
Risk: Interview templates may capture personal details, recordings, photos, or customer information. <br>
Mitigation: Collect and retain interview materials only with consent and an approved storage and retention policy. <br>
Risk: Role-based guidance may produce product, API, operations, or release recommendations that are incomplete or incorrect for a specific organization. <br>
Mitigation: Have responsible product, engineering, security, and operations reviewers approve generated plans and documents before implementation or release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scubiry-glitch/product-dev-ops-package) <br>
- [Publisher profile](https://clawhub.ai/user/scubiry-glitch) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [INDEX.md](INDEX.md) <br>
- [Start command](commands/start.md) <br>
- [Workshop command](commands/workshop.md) <br>
- [Archive command](commands/archive.md) <br>
- [External interview template](templates/workshop/external-interview-template.md) <br>
- [OpenAPI template](templates/api/openapi-template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, project document templates, OpenAPI YAML templates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project documentation under projects/[name]/ when the agent follows the workflow.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
