## Description:

Autonomous full-cycle app builder that turns a natural-language request into a PRD, architecture, code, deployment, tests, and fix iterations while remembering user preferences and development pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanningwang](https://clawhub.ai/user/hanningwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use mano-afk to autonomously build and verify an application from a natural-language description, including product requirements, architecture, generated source code, deployment scripts, test execution, fix loops, and a final build report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad autonomous build, dependency, deployment, and test authority in generated app workspaces.

Mitigation: Use the skill only in disposable or clearly separated app-build workspaces and avoid connecting it to production databases or production services.

Risk: The Homebrew install path is third-party maintained.

Mitigation: Review the Homebrew tap and source before installing or executing the associated command-line tool.

Risk: Cloud E2E mode can transmit screenshots and task descriptions to external model providers.

Mitigation: Use local E2E mode or leave E2E disabled unless the project screenshots and task descriptions are acceptable to share with the configured cloud provider.

Risk: Learned rules and preferences can persist and influence future generated projects.

Mitigation: Inspect references/rules.md and references/preferences.md after runs and remove any unreviewed or unwanted guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hanningwang/skills/mano-afk)
- [Homepage](https://github.com/Mininglamp-AI/mano-afk)
- [Build Pipeline](references/build-pipeline.md)
- [PRD Template](references/prd-template.md)
- [README Template](references/readme-template.md)
- [Report Template](references/report-template.md)
- [Project Structure Template](references/project-structure.md)
- [Build Rules](references/rules.md)
- [User Preferences](references/preferences.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create PRD.md, README.md, report.md, source files, deploy scripts, local logs, and persistent rules or preferences within the skill and generated project workspace.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
