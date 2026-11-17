## Description:

Run structured multi-step workflows via FlowForge engine for step-by-step execution, enforced ordering, and persistent workflow state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kagura-agent](https://clawhub.ai/user/kagura-agent)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use FlowForge to run YAML-defined workflows that keep multi-step work ordered, resumable, and explicit across tasks such as code contribution, research, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow YAML task text can steer the agent through auto-discovered workflows.

Mitigation: Review workflows in ./workflows and ~/.flowforge/workflows before execution, and do not let workflow text override normal safety, approval, or review requirements.

Risk: The skill can expand activation scope by adding successful intent mappings and trigger phrases.

Mitigation: Review mapping-table and frontmatter trigger changes before keeping them, especially broad phrases that could activate the skill unexpectedly.

Risk: Workflow execution may involve persistent logs, shell-profile changes, resets, pushes, deploys, or pull request actions.

Mitigation: Ask for explicit user approval before sensitive commands or external actions, and keep persistent workflow logs free of secrets.

## Reference(s):

- [FlowForge Setup Guide](setup.md)
- [FlowForge YAML Format](references/yaml-format.md)
- [Code Contribution Workflow Example](references/examples/code-contribution.yaml)
- [Research Workflow Example](references/examples/research.yaml)
- [Review Workflow Example](references/examples/review.yaml)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code]

**Output Format:** [Markdown with inline shell commands and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workflow YAML files and local workflow mappings when the user needs a new or repeated workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
