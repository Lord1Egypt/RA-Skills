## Description:

Refines architecture designs or execution plans through a context-grounded independent review loop before approval or implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to refine architecture designs and execution plans until scope, ownership, interfaces, completeness, and open gates are clear. It is intended for design convergence before user approval or implementation, not for ordinary code review or trivial one-off answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project context may be shared with an independent reviewer or subagent.

Mitigation: Share only the context needed for review and keep reviewer use purpose-aligned; the skill does not grant execution or persistence authority.

Risk: Review recommendations can influence architecture decisions even when findings are speculative.

Mitigation: Apply materiality and plausibility gates, require evidence and impact for blocking findings, and keep the primary agent responsible for final decisions.

Risk: The workflow may be mistaken for authorization to implement, migrate, deploy, publish, or take destructive action.

Mitigation: Use it only for design and execution-plan refinement; the artifact boundaries state that it does not authorize those actions.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/xukp20/codex-design-review-loop/tree/main/skills/iterate-design-review)
- [ClawHub skill page](https://clawhub.ai/xukp20/skills/iterate-design-review)

## Skill Output:

**Output Type(s):** [guidance, markdown, text]

**Output Format:** [Markdown or structured text review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces iterative review prompts, triage decisions, and concise design or execution-plan refinements; no execution authority.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
