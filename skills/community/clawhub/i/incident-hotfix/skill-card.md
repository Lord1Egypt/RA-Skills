## Description:

Coder-focused incident response and hotfix execution for production issues, including reproducible triage, patch and rollback decisions, CI-safe hotfix branches, evidence capture, and postmortem action tracking tied to code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[broedkrummen](https://clawhub.ai/user/broedkrummen)

### License/Terms of Use:


## Use Case:

Developers and on-call engineers use this skill to manage code-level incident hotfixes, create hotfix branches, capture evidence, document rollback plans, and track corrective actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can write outside the intended incident folder when incident IDs contain path separators or other unsafe characters.

Mitigation: Use only simple incident IDs such as INC-1234 and review or patch the scripts before running them.

Risk: Evidence capture can save GitHub environment values into repository evidence files.

Mitigation: Do not run evidence capture in shells or CI jobs containing GitHub tokens or other secrets, and inspect generated evidence before committing, uploading, or sharing it.

## Reference(s):

- [Corrective Actions Template](references/action-template.md)
- [Severity Matrix](references/severity-matrix.md)
- [ClawHub Skill Page](https://clawhub.ai/broedkrummen/skills/incident-hotfix)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and incident document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces incident timeline, rollback, corrective action, and evidence-bundle guidance for repository workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
