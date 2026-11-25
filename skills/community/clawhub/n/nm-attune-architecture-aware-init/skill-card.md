## Description:

Selects architecture paradigm via research before scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers starting a project with an undecided architecture use this skill to gather requirements, compare architectural paradigms, adapt a scaffold, and document the decision in an ADR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online architecture research may share project details with an external search provider.

Mitigation: Remove secrets and confidential details from research queries, and check that external search fits the project's privacy requirements.

Risk: Broad activation terms may cause the skill to run in workflows where architecture selection is not intended.

Mitigation: Review the activation conditions in the local skill configuration and invoke it when architecture is undecided.

Risk: The security scan had partial coverage because two referenced local paths could not be matched to bundled files.

Mitigation: Check the full installation for those referenced files and review them before relying on the workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-attune-architecture-aware-init)
- [Skill homepage in metadata](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Project files]

**Output Format:** [Markdown briefs and ADRs, code and shell examples, and paradigm-specific project scaffolds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations and scaffolds depend on the project context and selected architecture paradigm.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
