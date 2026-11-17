## Description:

Autonomous orchestrator for manifest work items through the development lifecycle

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Summon to process manifest work items through intake, implementation, quality review, and pull request preparation, including resuming interrupted runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External-model delegation may share project data with providers; the partial scan did not verify referenced runtime files.

Mitigation: Review how external-model delegation is enabled and whether project-data sharing with those providers is acceptable before installing.

## Reference(s):

- [Egregore plugin page listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/egregore)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Repository changes and workflow artifacts, including Markdown summaries and pull request text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the manifest work items and the specialist skills used by each pipeline step.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
