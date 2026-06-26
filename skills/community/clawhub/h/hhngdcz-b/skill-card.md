## Description: <br>
Generates technical project documentation in Markdown under docs/, including overview, architecture, module, API, data model, dependency, and deployment documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhngdcz](https://clawhub.ai/user/hhngdcz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze a codebase and generate structured technical documentation files for project understanding, onboarding, and maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads project files and may generate or update Markdown documentation under docs/. <br>
Mitigation: Install it only for projects where documentation generation is intended, run it on a branch when existing docs matter, and review overwrite choices before allowing changes. <br>
Risk: Generated documentation may be in Chinese, which may not match every project's documentation standards. <br>
Mitigation: Confirm Chinese documentation is acceptable for the project before using the skill or revise the generated docs afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhngdcz/hhngdcz-b) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/hhngdcz) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown files written under docs/ with brief status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces docs/README.md, docs/architecture.md, docs/modules/*.md, docs/api.md, docs/data-model.md, docs/dependencies.md, and docs/deployment.md; generated documentation is written in Chinese with English technical terms preserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
