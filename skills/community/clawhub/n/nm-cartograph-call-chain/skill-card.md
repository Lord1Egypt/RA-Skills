## Description:

Traces execution paths through the code graph with criticality scoring and Mermaid charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to trace a function's execution path through a codebase, assess its criticality, and present the flow for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security analysis was partial because two local references could not be resolved, and a scanner reported a local configuration-directory lookup.

Mitigation: Review the referenced local paths and unresolved references, and confirm the lookup is appropriate in the environment where the skill will run.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-cartograph-call-chain)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown with an indented call tree, Mermaid flowchart, and criticality breakdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
