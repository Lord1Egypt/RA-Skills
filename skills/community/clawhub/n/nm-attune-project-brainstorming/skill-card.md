## Description:

Guides project ideation via Socratic questioning to produce a validated brief. Use before specification when requirements are unclear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to clarify unclear requirements, compare approaches, record decision rationale, and produce a project brief before specification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically delegates brainstorming context to a separate multi-LLM workflow and continues into specification without confirmation; the delegated providers are not identified and external transmission is not established by the evidence.

Mitigation: Review the handoff and continuation behavior before use; choose the documented --standalone mode when you want to stop after brainstorming.

Risk: Security analysis is partial because some referenced paths could not be resolved, so the available evidence does not establish that the artifact is safe.

Mitigation: Review unresolved references and the full artifact, and complete security review before installation or use.

## Reference(s):

- [ClawHub release: project-brainstorming](https://clawhub.ai/athola/skills/nm-attune-project-brainstorming)
- [Claude Night Market Attune plugin (metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown project brief with structured questions, approach comparisons, and decision rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may continue into a project specification phase after producing the brief.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
